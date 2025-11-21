print("start")

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from tqdm import tqdm
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
from code_efficiency_calculator import calculate_code_execution_efficiency
from datasets import load_dataset
from output_utils import (
    find_existing_result,
    overhead_path,
    resolve_stage_dir,
    result_path,
    ensure_subdir,
    write_json,
    STAGE_OPTIMIZATION,
    STAGE_GENERATION,
)

PROFILE_TMP_DIR = "./tmp"

os.makedirs(PROFILE_TMP_DIR, exist_ok=True)


def get_completion_file_path(data_entry, base_dir=PROFILE_TMP_DIR):
    """Infer the temp script path used for profiling."""
    if "task_id" in data_entry and "HumanEval" in str(data_entry["task_id"]):
        problem_idx = data_entry["task_id"].split("/")[1]
    elif data_entry.get("dataset") == "MBPP":
        problem_idx = data_entry.get("task_id")
    else:
        problem_idx = data_entry.get("problem_idx")
    if problem_idx is None:
        return None
    return os.path.normpath(os.path.join(base_dir, f"{problem_idx}.py"))


def generate_scalene_overhead(script_path, output_dir, timeout=30):
    """Profile a script with Scalene and return cleaned report text."""
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(script_path))[0]
    scalene_output = os.path.join(output_dir, f"{base_name}_scalene.txt")
    env = os.environ.copy()
    env["COLUMNS"] = env.get("COLUMNS", "1000")
    try:
        subprocess.run(
            ["python", "-m", "scalene", "--cli", "--outfile", scalene_output, script_path],
            check=True,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "Scalene profiling timed out."
    except subprocess.CalledProcessError as exc:
        return f"Scalene profiling failed: {exc.stderr.strip()}"

    if not os.path.exists(scalene_output):
        return "Scalene report missing: no output file produced."

    with open(scalene_output, "r") as f:
        content = f.read()

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    clean_output = ansi_escape.sub("", content)
    return clean_output if clean_output.strip() else "Scalene produced empty output."


batch_size = 8
def prompt_construction(task_description, test_case, completion, overhead_prompt):
    prompt = f"""
Optimize the efficiency of the following Python code based on the task, test case, and overhead analysis provided. Ensure the optimized code can pass the given test case.

Task Description:
{task_description}

Test Case:
{test_case}

Original Code:
```python
{completion}
```
Overhead Analysis:
{overhead_prompt}
Optimization Rules:
- Encapsulate the optimized code within a Python code block (i.e., ```python\n[Your Code Here]\n```).
- Do not include the test case within the code block.
- Focus solely on code optimization; test cases are already provided.
- Ensure the provided test case passes with your optimized solution.
"""
    return prompt


def construct_prompt_template(inputs,model,tokenizer):

    tokenizer.pad_token = tokenizer.eos_token
    input_tokens = tokenizer.batch_encode_plus(
    inputs,
    padding=True,
    return_tensors="pt",
    
    ).to(model.device)
    for t in input_tokens:
        if torch.is_tensor(input_tokens[t]):
            input_tokens[t] = input_tokens[t].to(model.device)
    # input_tokens.pop("token_type_ids")
    try:
        sequences = model.generate(
        **input_tokens, max_new_tokens=512, do_sample=True
        )
        generated_texts = tokenizer.batch_decode(sequences, skip_special_tokens=True)
        for i in range(len(generated_texts)):
            if inputs[i] in generated_texts[i]:
                generated_texts[i] = generated_texts[i].replace(inputs[i], "")
    except:
        generated_texts = ["" for i in range(len(inputs))]

    return generated_texts

# Function to fetch completion
def fetch_completion(data_entry_lists, model,tokenizer):
    inputs_batchs = []
    for data_entry in data_entry_lists:
        if "overhead" not in data_entry.keys():
            overhead = "The code execution failed."
        else:
            overhead = data_entry["overhead"]
        
        completion = data_entry["completion"]
        if data_entry["dataset"] == "EffiBench":
            test_case = data_entry["small_test_cases"]
            task_description = data_entry["markdown_description"]
        elif data_entry["dataset"] == "HumanEval":
            test_case = data_entry["open_test_cases"]
            task_description = data_entry["prompt"]
        elif data_entry["dataset"] == "MBPP":
            test_case = "\n".join(data_entry["test_list"])
            task_description = data_entry["prompt"]
            
        prompt = prompt_construction(task_description, test_case, completion, overhead)
        inputs_batchs.append(prompt)

    completion_lists = construct_prompt_template(inputs_batchs,model,tokenizer)
    for i in range(len(data_entry_lists)):
        data_entry_lists[i]["tmp_completion"] = completion_lists[i]
    return data_entry_lists


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--checkpoint", type=str, default="m-a-p/OpenCodeInterpreter-DS-33B", required=True)
    args.add_argument("--batch_size", type=int, default=16)
    args.add_argument("--epoch", type=int, default=5)
    args.add_argument("--dataset", type=str, required=True)
    args.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Base directory for generated results (defaults to <repo>/outputs/results).",
    )
    args.add_argument(
        "--profiler",
        type=str,
        default="scalene",
        help="Profiler tag for naming outputs (defaults to scalene).",
    )
    args = args.parse_args()

    batch_size = args.batch_size
    checkpoint = args.checkpoint
    epoch = args.epoch
    print("Checkpoint: ",checkpoint)
    model_name = checkpoint.split("/")[-1]
    stage_dir_opt = resolve_stage_dir(STAGE_OPTIMIZATION, args.output_dir)
    stage_dir_gen = resolve_stage_dir(STAGE_GENERATION, args.output_dir)
    legacy_results_dir = (Path(__file__).resolve().parent.parent / "results").resolve()
    scalene_output_dir = ensure_subdir(stage_dir_opt.parent, "scalene_reports")
    model = AutoModelForCausalLM.from_pretrained(checkpoint,device_map = "auto",trust_remote_code=True,torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(checkpoint,trust_remote_code=True)
    overhead_dict = {
        "overhead": [],
        "memory_usage": [],
        "execution_time": [],
        "max_memory_peak": [],
        "correct": [],
    }
    dataset_path = find_existing_result(
        args.dataset,
        model_name,
        stage_dir_gen,
        profiler="none",
        legacy_dirs=[legacy_results_dir],
    )
    if dataset_path is None:
        raise FileNotFoundError(f"Dataset file not found in {stage_dir_gen} (or legacy {legacy_results_dir})")
    with open(dataset_path, "r") as f:
        dataset = json.load(f)
    if args.dataset == "HumanEval":
        humaneval_open_testcases = load_dataset("openai_humaneval",split="test")
        tmp_open_test_cases = {}
        for i in range(len(humaneval_open_testcases)):
            tmp_open_test_cases[humaneval_open_testcases[i]["entry_point"]] = humaneval_open_testcases[i]["test"] + f"\ncheck{humaneval_open_testcases[i]['entry_point']}"
        for i in range(len(dataset)):
            dataset[i]["open_test_cases"] = tmp_open_test_cases[dataset[i]["entry_point"]]


    for i in tqdm(range(len(dataset))):
        overhead, memory_usage, execution_time, max_memory_peak,executable = calculate_code_execution_efficiency(dataset[i],evaluation_code=True, path=PROFILE_TMP_DIR)
        scalene_overhead = None
        script_path = get_completion_file_path(dataset[i], PROFILE_TMP_DIR)
        if executable and script_path and os.path.exists(script_path):
            scalene_overhead = generate_scalene_overhead(script_path, scalene_output_dir)
        if executable:
            dataset[i]["overhead"] = scalene_overhead or overhead
            dataset[i]["memory_usage"] = memory_usage
            dataset[i]["execution_time"] = execution_time
            dataset[i]["max_memory_peak"] = max_memory_peak
            dataset[i]["executable"] = executable

    dataset = [entry for entry in dataset if "executable" in entry.keys() and entry["executable"]]
    total_memory_usage = 0
    total_execution_time = 0
    total_max_memory_peak = 0
    normalize_total_memory_usage = 0
    normalize_total_execution_time = 0
    normalize_total_max_memory_peak = 0
    correct = 0
    for i in tqdm(range(len(dataset))):
        if "executable" in dataset[i].keys() and dataset[i]["executable"]:
            total_memory_usage += dataset[i]["memory_usage"]
            total_execution_time += dataset[i]["execution_time"]
            total_max_memory_peak += dataset[i]["max_memory_peak"]
            correct+=1

    if correct==0:
        correct=1
    total_overhead = f"""
The total memory usage during the code execution is: {round(total_memory_usage/correct,2)} MB*s.
The total execution time is: {round(total_execution_time/correct,2)} s.
The maximum memory peak requirement is: {round(total_max_memory_peak/correct,2)} MB.
"""
    overhead_dict["overhead"].append(total_overhead)
    overhead_dict["memory_usage"].append(round(total_memory_usage/correct,2))
    overhead_dict["execution_time"].append(round(total_execution_time/correct,2))
    overhead_dict["max_memory_peak"].append(round(total_max_memory_peak/correct,2))
    overhead_dict["correct"].append(correct)

    for current_epoch in range(1, epoch+1):
        for i in tqdm(range(0,len(dataset),batch_size)):
            dataset[i:i+batch_size] = fetch_completion(dataset[i:i+batch_size],model,tokenizer)

        total_memory_usage = 0
        total_execution_time = 0
        total_max_memory_peak = 0
        normalize_total_memory_usage = 0
        normalize_total_execution_time = 0
        normalize_total_max_memory_peak = 0
        correct = 0
        for i in range(len(dataset)):
            tmp_code = dataset[i]["completion"]
            dataset[i]["completion"] = dataset[i]["tmp_completion"]
            overhead, memory_usage, execution_time, max_memory_peak,executable = calculate_code_execution_efficiency(dataset[i],evaluation_code=True, path=PROFILE_TMP_DIR)
            scalene_overhead = None
            script_path = get_completion_file_path(dataset[i], PROFILE_TMP_DIR)
            if executable and script_path and os.path.exists(script_path):
                scalene_overhead = generate_scalene_overhead(script_path, scalene_output_dir)

            if (("memory_usage" not in dataset[i].keys()) or (memory_usage < dataset[i]["memory_usage"])) and executable:
                dataset[i]["memory_usage"] = memory_usage
                dataset[i]["execution_time"] = execution_time
                dataset[i]["max_memory_peak"] = max_memory_peak
                dataset[i]["overhead"] = scalene_overhead or overhead
                dataset[i]["executable"] = executable
            else:
                dataset[i]["completion"] = tmp_code
            if "executable" in dataset[i].keys() and dataset[i]["executable"]:
                total_memory_usage += dataset[i]["memory_usage"]
                total_execution_time += dataset[i]["execution_time"]
                total_max_memory_peak += dataset[i]["max_memory_peak"]

                correct+=1
        if correct==0:
            # tolerence
            correct+=1
        total_overhead = f"""
The total memory usage during the code execution is: {round(total_memory_usage/correct,2)} MB*s.
The total execution time is: {round(total_execution_time/correct,2)} s.
The maximum memory peak requirement is: {round(total_max_memory_peak/correct,2)} MB.
"""
        overhead_dict["overhead"].append(total_overhead)
        overhead_dict["memory_usage"].append(round(total_memory_usage/correct,2))
        overhead_dict["execution_time"].append(round(total_execution_time/correct,2))
        overhead_dict["max_memory_peak"].append(round(total_max_memory_peak/correct,2))
        overhead_dict["correct"].append(correct)

        write_json(
            dataset,
            result_path(
                args.dataset,
                model_name,
                stage_dir_opt,
                profiler=args.profiler,
                epoch=current_epoch,
            ),
        )

    write_json(
        overhead_dict,
        overhead_path(args.dataset, model_name, stage_dir_opt, profiler=args.profiler),
    )
