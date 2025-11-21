print("start")

import argparse
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI
from code_efficiency_calculator import calculate_code_execution_efficiency
from datasets import load_dataset
from output_utils import (
    ensure_subdir,
    find_existing_result,
    overhead_path,
    resolve_stage_dir,
    result_path,
    write_json,
    STAGE_OPTIMIZATION,
    STAGE_GENERATION,
)

PROFILE_TMP_DIR = "./tmp"

os.makedirs(PROFILE_TMP_DIR, exist_ok=True)


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


def construct_prompt_template(inputs, model, tokenizer):
    tokenizer.pad_token = tokenizer.eos_token
    input_tokens = tokenizer.batch_encode_plus(
        inputs,
        padding=True,
        return_tensors="pt",
    ).to(model.device)
    for t in input_tokens:
        if torch.is_tensor(input_tokens[t]):
            input_tokens[t] = input_tokens[t].to(model.device)
    try:
        sequences = model.generate(**input_tokens, max_new_tokens=512, do_sample=True)
        generated_texts = tokenizer.batch_decode(sequences, skip_special_tokens=True)
        for i in range(len(generated_texts)):
            if inputs[i] in generated_texts[i]:
                generated_texts[i] = generated_texts[i].replace(inputs[i], "")
    except Exception:
        generated_texts = ["" for _ in range(len(inputs))]
    return generated_texts


def fetch_completion(data_entry_lists, client, model_name):
    """Fetch completions using OpenAI chat models."""
    completion_lists = []
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
        else:
            test_case = ""
            task_description = ""

        prompt = prompt_construction(task_description, test_case, completion, overhead)
        try:
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                timeout=100,
            )
            completion_lists.append(resp.choices[0].message.content)
        except Exception:
            completion_lists.append("")

    for i in range(len(data_entry_lists)):
        data_entry_lists[i]["tmp_completion"] = completion_lists[i]
    return data_entry_lists


def get_completion_file_path(data_entry, base_dir=PROFILE_TMP_DIR):
    if "task_id" in data_entry and "HumanEval" in str(data_entry["task_id"]):
        problem_idx = data_entry["task_id"].split("/")[1]
    elif data_entry.get("dataset") == "MBPP":
        problem_idx = data_entry.get("task_id")
    else:
        problem_idx = data_entry.get("problem_idx")
    if problem_idx is None:
        return None
    return os.path.normpath(os.path.join(base_dir, f"{problem_idx}.py"))


def generate_scalene_overhead(script_path, output_dir, timeout=30, runs=1):
    """Run Scalene on a script and return cleaned report."""
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(script_path))[0]
    scalene_output = os.path.join(output_dir, f"{base_name}_scalene.txt")
    target_path = os.path.abspath(script_path)

    # If we need multiple runs, build a tiny wrapper to execute the target repeatedly.
    wrapper_path = None
    if runs > 1:
        wrapper_fd, wrapper_path = tempfile.mkstemp(suffix=".py", prefix=f"{base_name}_scalene_wrap_", dir=PROFILE_TMP_DIR)
        with os.fdopen(wrapper_fd, "w") as f:
            f.write(
                "import runpy\n"
                f"TARGET = {target_path!r}\n"
                f"for _ in range({runs}):\n"
                "    runpy.run_path(TARGET, run_name='__main__')\n"
            )
        target_path = wrapper_path

    env = os.environ.copy()
    env["COLUMNS"] = env.get("COLUMNS", "1000")
    try:
        subprocess.run(
            ["python", "-m", "scalene", "--cli", "--outfile", scalene_output, target_path],
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
    finally:
        if wrapper_path and os.path.exists(wrapper_path):
            os.remove(wrapper_path)

    if not os.path.exists(scalene_output):
        return "Scalene report missing: no output file produced."

    with open(scalene_output, "r") as f:
        content = f.read()

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    clean_output = ansi_escape.sub("", content)
    return clean_output if clean_output.strip() else "Scalene produced empty output."


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--checkpoint", type=str, default="gpt-4o", required=True)
    args.add_argument("--batch_size", type=int, default=16)
    args.add_argument("--epoch", type=int, default=5)
    args.add_argument("--dataset", type=str, required=True)
    args.add_argument("--sample_size", type=int, default=20, help="Number of examples to process (<= total dataset).")
    args.add_argument("--seed", type=int, default=42, help="Seed for sampling subset.")
    args.add_argument("--use_scalene", action="store_true", help="Use Scalene profiling for overhead text.")
    args.add_argument("--no_shuffle", action="store_true", help="Use the first N items instead of shuffling before sampling.")
    args.add_argument(
        "--scalene_runs",
        type=int,
        default=1,
        help="Number of times to run each script when collecting Scalene overhead (helps generate usable reports for short scripts).",
    )
    args.add_argument(
        "--prefer_scalene_overhead",
        action="store_true",
        help="If set, replace the overhead text with the Scalene report when available.",
    )
    args.add_argument("--input_file", type=str, default=None, help="Path to input JSON (defaults to <output_dir>/<dataset>_<model>.json).")
    args.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Base directory for generated results (defaults to <repo>/outputs/results).",
    )
    args.add_argument(
        "--profiler",
        type=str,
        default=None,
        help="Profiler tag for naming optimization outputs. Defaults to 'scalene' when --use_scalene, otherwise 'none'.",
    )
    args = args.parse_args()

    batch_size = args.batch_size
    checkpoint = args.checkpoint
    epoch = args.epoch
    print("Checkpoint: ", checkpoint)
    model_name = checkpoint.split("/")[-1]
    stage_dir_opt = resolve_stage_dir(STAGE_OPTIMIZATION, args.output_dir)
    stage_dir_gen = resolve_stage_dir(STAGE_GENERATION, args.output_dir)
    output_root = stage_dir_opt.parent
    scalene_output_dir = ensure_subdir(output_root, "scalene_reports")
    profiler_tag = args.profiler or ("scalene" if args.use_scalene else "none")
    # Use OpenAI chat models when checkpoint does not look like an HF path.
    use_openai = checkpoint.startswith("gpt-")
    client = None
    model = None
    tokenizer = None
    if use_openai:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))
    else:
        model = AutoModelForCausalLM.from_pretrained(
            checkpoint, device_map="auto", trust_remote_code=True, torch_dtype=torch.float16
        )
        tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
    overhead_dict = {
        "overhead": [],
        "memory_usage": [],
        "execution_time": [],
        "max_memory_peak": [],
        "correct": [],
    }
    legacy_results_dir = (Path(__file__).resolve().parent.parent / "results").resolve()
    if args.input_file:
        input_path = Path(args.input_file).expanduser()
    else:
        existing = find_existing_result(
            args.dataset,
            model_name,
            stage_dir_gen,
            profiler=profiler_tag,
            legacy_dirs=[legacy_results_dir],
        )
        if existing is None:
            raise FileNotFoundError(f"Dataset file not found in {stage_dir_gen} (or legacy {legacy_results_dir})")
        input_path = existing
    with open(input_path, "r") as f:
        dataset = json.load(f)
    if args.dataset == "HumanEval":
        humaneval_open_testcases = load_dataset("openai_humaneval", split="test")
        tmp_open_test_cases = {}
        for i in range(len(humaneval_open_testcases)):
            tmp_open_test_cases[humaneval_open_testcases[i]["entry_point"]] = (
                humaneval_open_testcases[i]["test"] + f"\ncheck{humaneval_open_testcases[i]['entry_point']}"
            )
        for i in range(len(dataset)):
            dataset[i]["open_test_cases"] = tmp_open_test_cases[dataset[i]["entry_point"]]

    # Sample a small subset to keep runs lightweight.
    if args.sample_size > 0 and len(dataset) > args.sample_size:
        if not args.no_shuffle:
            random.seed(args.seed)
            random.shuffle(dataset)
        dataset = dataset[: args.sample_size]

    for i in tqdm(range(len(dataset))):
        try:
            overhead, memory_usage, execution_time, max_memory_peak, executable = calculate_code_execution_efficiency(
                dataset[i], evaluation_code=True, path=PROFILE_TMP_DIR
            )
            scalene_overhead = None
            if args.use_scalene:
                script_path = get_completion_file_path(dataset[i], PROFILE_TMP_DIR)
                if executable and script_path and os.path.exists(script_path):
                    scalene_overhead = generate_scalene_overhead(
                        script_path, output_dir=scalene_output_dir, runs=args.scalene_runs
                    )
            if executable:
                if args.use_scalene and args.prefer_scalene_overhead and scalene_overhead:
                    dataset[i]["overhead"] = scalene_overhead
                else:
                    dataset[i]["overhead"] = scalene_overhead or overhead
                dataset[i]["memory_usage"] = memory_usage
                dataset[i]["execution_time"] = execution_time
                dataset[i]["max_memory_peak"] = max_memory_peak
                dataset[i]["executable"] = executable
            else:
                # Mark as not executable
                dataset[i]["executable"] = False
        except Exception as e:
            # Mark as not executable on error
            dataset[i]["executable"] = False
            # Optionally log the error (uncomment if needed for debugging)
            # print(f"[RunSmallEffi] Error processing entry {dataset[i].get('problem_idx', 'unknown')}: {e}")

    dataset = [entry for entry in dataset if "executable" in entry.keys() and entry["executable"]]
    print(f"[debug] executable entries after initial profiling: {len(dataset)}")

    # Optionally persist the profiled baseline (with Scalene overhead when enabled) before optimization.
    if args.use_scalene:
        scalene_baseline_dir = ensure_subdir(output_root, "scalene_baseline")
        baseline_path = scalene_baseline_dir / f"{args.dataset}_{model_name}_baseline.json"
        write_json(dataset, baseline_path)

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
            correct += 1

    if correct == 0:
        correct = 1
    total_overhead = f"""
The total memory usage during the code execution is: {round(total_memory_usage/correct,2)} MB*s.
The total execution time is: {round(total_execution_time/correct,2)} s.
The maximum memory peak requirement is: {round(total_max_memory_peak/correct,2)} MB.
"""
    overhead_dict["overhead"].append(total_overhead)
    overhead_dict["memory_usage"].append(round(total_memory_usage / correct, 2))
    overhead_dict["execution_time"].append(round(total_execution_time / correct, 2))
    overhead_dict["max_memory_peak"].append(round(total_max_memory_peak / correct, 2))
    overhead_dict["correct"].append(correct)

    for current_epoch in range(1, epoch + 1):
        for i in tqdm(range(0, len(dataset), batch_size)):
            if use_openai:
                dataset[i : i + batch_size] = fetch_completion(dataset[i : i + batch_size], client, checkpoint)
            else:
                dataset[i : i + batch_size] = fetch_completion(dataset[i : i + batch_size], model, tokenizer)

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
            overhead, memory_usage, execution_time, max_memory_peak, executable = calculate_code_execution_efficiency(
                dataset[i], evaluation_code=True, path=PROFILE_TMP_DIR
            )
            scalene_overhead = None
            if args.use_scalene:
                script_path = get_completion_file_path(dataset[i], PROFILE_TMP_DIR)
                if executable and script_path and os.path.exists(script_path):
                    scalene_overhead = generate_scalene_overhead(
                        script_path, output_dir=scalene_output_dir, runs=args.scalene_runs
                    )

            if (("memory_usage" not in dataset[i].keys()) or (memory_usage < dataset[i]["memory_usage"])) and executable:
                dataset[i]["memory_usage"] = memory_usage
                dataset[i]["execution_time"] = execution_time
                dataset[i]["max_memory_peak"] = max_memory_peak
                if args.use_scalene and args.prefer_scalene_overhead and scalene_overhead:
                    dataset[i]["overhead"] = scalene_overhead
                else:
                    dataset[i]["overhead"] = scalene_overhead or overhead
                dataset[i]["executable"] = executable
            else:
                dataset[i]["completion"] = tmp_code
            if "executable" in dataset[i].keys() and dataset[i]["executable"]:
                total_memory_usage += dataset[i]["memory_usage"]
                total_execution_time += dataset[i]["execution_time"]
                total_max_memory_peak += dataset[i]["max_memory_peak"]

                correct += 1
        if correct == 0:
            correct += 1
        total_overhead = f"""
The total memory usage during the code execution is: {round(total_memory_usage/correct,2)} MB*s.
The total execution time is: {round(total_execution_time/correct,2)} s.
The maximum memory peak requirement is: {round(total_max_memory_peak/correct,2)} MB.
"""
        overhead_dict["overhead"].append(total_overhead)
        overhead_dict["memory_usage"].append(round(total_memory_usage / correct, 2))
        overhead_dict["execution_time"].append(round(total_execution_time / correct, 2))
        overhead_dict["max_memory_peak"].append(round(total_max_memory_peak / correct, 2))
        overhead_dict["correct"].append(correct)

        write_json(
            dataset,
            result_path(
                args.dataset,
                model_name,
                stage_dir_opt,
                profiler=profiler_tag,
                epoch=current_epoch,
            ),
        )

    write_json(
        overhead_dict,
        overhead_path(args.dataset, model_name, stage_dir_opt, profiler=profiler_tag),
    )
