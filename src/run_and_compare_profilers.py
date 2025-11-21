"""
Run and compare original profiler vs scalene, timing both.
"""
import argparse
import os
import re
import subprocess
import time

from output_utils import ensure_subdir, resolve_results_dir


parser = argparse.ArgumentParser(description="Compare custom profiler vs Scalene.")
parser.add_argument("--test_file", type=str, default="src/test_code.py", help="Path to the Python file to profile.")
parser.add_argument("--entry_point", type=str, default="slow_compute_primes", help="Entry point function for the original profiler.")
parser.add_argument(
    "--output_dir",
    type=str,
    default=None,
    help="Base directory for profiler outputs (defaults to <repo>/outputs/results/profiler_reports).",
)
args = parser.parse_args()

output_root = resolve_results_dir(args.output_dir).parent
output_dir = ensure_subdir(output_root, "profiler_reports")
orig_output = output_dir / "orig_prof.txt"
scalene_output = output_dir / "scalene_prof.txt"

print("Running original profiler...")
start = time.time()
result = subprocess.run(
    ["python", "src/generate_overhead_for_llm.py", args.test_file, "--entry_point", args.entry_point, "--output", str(orig_output)],
    capture_output=True,
    text=True,
)
orig_time = time.time() - start
print(f"Original profiler: {orig_time:.2f}s")
if result.returncode != 0:
    print(f"Error: {result.stderr}")

print("\nRunning scalene...")
start = time.time()
env = os.environ.copy()
env["COLUMNS"] = "1000"
result = subprocess.run(
    ["python", "-m", "scalene", "--cli", "--outfile", str(scalene_output), args.test_file],
    capture_output=True,
    text=True,
    env=env,
)

scalene_time = time.time() - start
print(f"Scalene: {scalene_time:.2f}s")

if scalene_output.exists():
    with scalene_output.open("r") as f:
        content = f.read()
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    clean_output = ansi_escape.sub("", content)
    with scalene_output.open("w") as f:
        f.write(clean_output)


# Show quick snippets from both profilers to compare “line-level” details.
def preview(path, label):
    if not path.exists():
        print(f"{label} missing at {path}")
        return
    print(f"\n[{label} preview] {path}")
    try:
        with path.open("r") as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                print(line.rstrip())
    except Exception as e:
        print(f"Could not read {label}: {e}")


preview(orig_output, "Original profiler")
preview(scalene_output, "Scalene profiler")

print("\nResults saved to:")
print(f"  Original: {orig_output}")
print(f"  Scalene: {scalene_output}")
