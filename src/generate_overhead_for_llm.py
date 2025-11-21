"""
Generate the overhead string that would be sent to the LLM for optimization.
Takes a Python file, profiles it, and outputs the complete overhead string.
"""
import os
import subprocess
import sys
import json
import re
import argparse
import shutil

def calculate_memory_usage(dat_file_path):
    """Calculate memory usage from .dat file"""
    with open(dat_file_path, 'r') as file:
        prev_time = 0
        prev_mem_mb = 0
        mem_time_mb_s = 0
        next(file)  # Skip header
        for line in file:
            if not line.startswith('MEM'):
                continue
            parts = line.split()
            mem_in_mb = float(parts[1])
            timestamp = float(parts[2])
            if prev_time > 0:
                time_interval_s = timestamp - prev_time
                mem_time_mb_s += (prev_mem_mb + mem_in_mb) / 2 * time_interval_s
            prev_time = timestamp
            prev_mem_mb = mem_in_mb
        return mem_time_mb_s

def calculate_runtime(dat_file_path):
    """Calculate runtime from .dat file"""
    with open(dat_file_path, 'r') as file:
        start_time = float("inf")
        end_time = float("-inf")
        next(file)  # Skip header
        for line in file:
            if not line.startswith('MEM'):
                continue
            parts = line.split()
            timestamp = float(parts[2])
            start_time = min(start_time, timestamp)
            end_time = max(end_time, timestamp)
        return max(end_time - start_time, 0)

def report_max_memory_usage(dat_file_path):
    """Report max memory usage from .dat file"""
    max_memory_usage = 0
    with open(dat_file_path, 'r') as file:
        next(file)  # Skip header
        for line in file:
            if not line.startswith('MEM'):
                continue
            parts = line.split()
            mem_in_mb = float(parts[1])
            max_memory_usage = max(max_memory_usage, mem_in_mb)
        return max_memory_usage

def get_line_profiler_results(completion_file, entry_point):
    """Get line profiler results for a function"""
    path, filename = os.path.split(completion_file)
    tmp_py_script = os.path.join(path, f"{filename.split('.')[0]}_tmp.py")
    tmp_lprof = os.path.join(path, f"{filename.split('.')[0]}_tmp.py.lprof")
    
    # Read original file
    with open(completion_file, 'r') as f:
        lines = f.readlines()
    
    # Create temporary file with @profile decorator
    with open(tmp_py_script, 'w') as f:
        f.write('from line_profiler import profile\n')
        for line in lines:
            if f"def {entry_point}" in line:
                f.write('@profile\n')
            f.write(line)
    
    try:
        # Run kernprof
        abs_tmp_script = os.path.abspath(tmp_py_script)
        subprocess.run(['kernprof', '-l', abs_tmp_script], 
                      cwd=os.path.dirname(abs_tmp_script),
                      capture_output=True, 
                      text=True, 
                      check=True)
        
        # Get line profiler report
        if os.path.exists(tmp_lprof):
            result = subprocess.run(['python', '-m', 'line_profiler', tmp_lprof], 
                                  capture_output=True, 
                                  text=True)
            line_profiler_results = result.stdout
            # Clean up
            if os.path.exists(tmp_py_script):
                os.remove(tmp_py_script)
            if os.path.exists(tmp_lprof):
                os.remove(tmp_lprof)
            return line_profiler_results
        else:
            return "Line profiler: Profile file not found."
    except Exception as e:
        # Clean up on error
        if os.path.exists(tmp_py_script):
            os.remove(tmp_py_script)
        if os.path.exists(tmp_lprof):
            os.remove(tmp_lprof)
        return f"Line profiler error: {str(e)}"

def get_memory_profiler_results(completion_file, entry_point):
    """Get memory profiler results - matches code_efficiency_calculator.py approach"""
    path, filename = os.path.split(completion_file)
    tmp_memory_script = os.path.join(path, f"{filename.split('.')[0]}_memory.py")
    
    # Read original file
    with open(completion_file, 'r') as f:
        full_code = f.read()
    
    # Memory profiler packages (from code_efficiency_calculator.py)
    memory_profiler_pkgs = """from collections import defaultdict, deque
from memory_profiler import profile
import io
profile_stream = io.StringIO()
PROFILE_PRECISION = 1
import re
import sys
import linecache
"""
    
    # Add @profile decorator to entry point function
    # Preserve the full code including main block
    lines = full_code.split('\n')
    new_lines = []
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line.startswith(f"def {entry_point}"):
            indent = len(line) - len(stripped_line)
            new_lines.append(' ' * indent + '@profile(stream=profile_stream, precision=PROFILE_PRECISION)')
        new_lines.append(line)
    
    full_code_with_profile = '\n'.join(new_lines)
    
    # Memory profiler prompt (parsing code from code_efficiency_calculator.py)
    memory_profiler_prompt = """
def parse_profile_table(profile_table: str):
    table = {"filename": None, "rows": []}
    for line in profile_table.strip().split("\\n"):
        if line.startswith("Filename:"):
            table["filename"] = line.split(": ")[1]
        elif re.match(r"^\\s*\\d+", line):
            parts = re.split(r"\\s{2,}", line.strip(), maxsplit=4)
            if len(parts) == 5 and "iB" in parts[1] and "iB" in parts[2]:
                table["rows"].append({
                    "line": int(parts[0]),
                    "mem_usage": parts[1],
                    "increment": parts[2],
                    "occurrences": int(parts[3]),
                    "line_contents": parts[4],
                })
            else:
                parts = re.split(r"\\s{2,}", line.strip(), maxsplit=1)
                table["rows"].append({
                    "line": int(parts[0]),
                    "line_contents": parts[1] if len(parts) == 2 else "",
                })
    return table

def print_averaged_results(profile_log: str, precision: int = 1):
    tables = [parse_profile_table(table) for table in profile_log.split("\\n\\n\\n")]
    averaged_table = defaultdict(lambda: defaultdict(list))

    for table in tables:
        filename = table["filename"]
        for row in table["rows"]:
            line = row["line"]
            if "mem_usage" in row:
                mem_usage = float(row["mem_usage"].split()[0])
                increment = float(row["increment"].split()[0])
                occurrences = row["occurrences"]
                averaged_table[filename][line].append((mem_usage, increment, occurrences))
            else:
                averaged_table[filename][line].append(tuple())

    stream = sys.stdout
    template = '{0:>6} {1:>12} {2:>12}  {3:>10}   {4:<}'

    for filename, lines in averaged_table.items():
        header = template.format('Line #', 'Mem usage', 'Increment', 'Occurrences', 'Line Contents')
        stream.write(u'Filename: ' + filename + '\\n\\n')
        stream.write(header + u'\\n')
        stream.write(u'=' * len(header) + '\\n')
        all_lines = linecache.getlines(filename)
        float_format = u'{{0}}.{{1}}f'.format(precision + 4, precision)
        template_mem = u'{{0:' + float_format + '}} MiB'
        for lineno, mem_values in lines.items():
            if any([len(m) == 0 for m in mem_values]):
                tmp = template.format(lineno, "", "", "", all_lines[lineno - 1])
            else:
                mem_usage_sum = sum(m[0] for m in mem_values)
                increment_sum = sum(m[1] for m in mem_values)
                occurrences_sum = sum(m[2] for m in mem_values)
                count = len(mem_values)

                avg_mem_usage = mem_usage_sum / count
                avg_increment = increment_sum / count
                avg_occurrences = occurrences_sum / count

                avg_mem_usage_str = template_mem.format(avg_mem_usage)
                avg_increment_str = template_mem.format(avg_increment)

                tmp = template.format(lineno, avg_mem_usage_str, avg_increment_str, int(avg_occurrences), all_lines[lineno - 1])
            stream.write(tmp)

print_averaged_results(profile_stream.getvalue(), precision=PROFILE_PRECISION)
"""
    
    # Combine all parts
    completion_code = memory_profiler_pkgs + full_code_with_profile + memory_profiler_prompt
    
    with open(tmp_memory_script, 'w') as f:
        f.write(completion_code)
    
    try:
        # Use timeout command (check for gtimeout on macOS or timeout on Linux)
        timeout_cmd = 'gtimeout' if shutil.which('gtimeout') else 'timeout'
        # Increase timeout to 30 seconds to allow longer-running code to complete
        result = subprocess.run([timeout_cmd, "30", "python", tmp_memory_script], 
                              capture_output=True, 
                              text=True, 
                              timeout=35)
        memory_report = result.stdout
        # Clean up
        if os.path.exists(tmp_memory_script):
            os.remove(tmp_memory_script)
        return memory_report if memory_report.strip() else "Memory profiler: No output generated."
    except subprocess.TimeoutExpired:
        if os.path.exists(tmp_memory_script):
            os.remove(tmp_memory_script)
        return "The script didn't finish within the timeout period."
    except Exception as e:
        if os.path.exists(tmp_memory_script):
            os.remove(tmp_memory_script)
        return f"Memory profiler error: {str(e)}"

def generate_overhead_string(py_file, entry_point=None, max_execution_time=30):
    """
    Generate the overhead string that would be sent to the LLM.
    
    Args:
        py_file: Path to Python file to profile
        entry_point: Function name to profile (if None, tries to detect)
        max_execution_time: Maximum execution time in seconds
    
    Returns:
        overhead string with all profiling information
    """
    if not os.path.exists(py_file):
        return f"Error: File {py_file} not found."
    
    # Detect entry point if not provided
    if entry_point is None:
        with open(py_file, 'r') as f:
            content = f.read()
            # Find first function definition
            match = re.search(r'def\s+(\w+)\s*\(', content)
            if match:
                entry_point = match.group(1)
            else:
                return "Error: Could not detect function to profile. Please specify --entry_point"
    
    print(f"Profiling file: {py_file}")
    print(f"Entry point: {entry_point}")
    print(f"Max execution time: {max_execution_time}s")
    print()
    
    # Create tmp directory
    os.makedirs("./tmp/", exist_ok=True)
    
    # Step 1: Measure basic performance metrics
    print("Step 1: Measuring basic performance metrics...")
    try:
        # Get the directory of this script and measure_code_performance.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        measure_script = os.path.join(script_dir, 'measure_code_performance.py')
        abs_py_file = os.path.abspath(py_file)
        
        result = subprocess.run(
            ['python', measure_script, abs_py_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout.strip()
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            perf_data = json.loads(json_match.group())
        else:
            perf_data = json.loads(output)
        
        if perf_data['success']:
            memory_usage = perf_data['memory_mb_s']
            execution_time = perf_data['execution_time']
            max_memory_peak = perf_data['peak_memory_mb']
            print(f"  ✓ Memory usage: {memory_usage} MB*s")
            print(f"  ✓ Execution time: {execution_time} s")
            print(f"  ✓ Max memory peak: {max_memory_peak} MB")
        else:
            raise Exception(perf_data.get('error', 'Unknown error'))
            
    except Exception as e:
        print(f"  ✗ Performance measurement error: {e}")
        memory_usage = 0.0
        execution_time = 0.0
        max_memory_peak = 0.0
    
    # Step 2: Get line profiler results
    print("\nStep 2: Running line profiler...")
    line_profiler_results = get_line_profiler_results(py_file, entry_point)
    if "error" not in line_profiler_results.lower():
        print("  ✓ Line profiler completed")
    else:
        print(f"  ✗ {line_profiler_results}")
    
    # Step 3: Get memory profiler results
    print("\nStep 3: Running memory profiler...")
    memory_report = get_memory_profiler_results(py_file, entry_point)
    if "error" not in memory_report.lower():
        print("  ✓ Memory profiler completed")
    else:
        print(f"  ✗ {memory_report}")
    
    # Step 4: Create the overhead string (WITHOUT comments - what LLM should receive)
    overhead = f"""
The total memory usage during the code execution is: {memory_usage} MB*s.
The total execution time is: {execution_time} s.
The maximum memory peak requirement is: {max_memory_peak} MB.
The line_profiler results are: 
{line_profiler_results}
The memory profiler results are: 
{memory_report}
"""
    
    return overhead

def main():
    parser = argparse.ArgumentParser(description='Generate overhead string for LLM optimization prompt')
    parser.add_argument('py_file', type=str, help='Path to Python file to profile')
    parser.add_argument('--entry_point', type=str, default=None, 
                       help='Function name to profile (auto-detected if not provided)')
    parser.add_argument('--max_execution_time', type=int, default=30,
                       help='Maximum execution time in seconds (default: 30)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output file path (default: print to stdout)')
    
    args = parser.parse_args()
    
    overhead = generate_overhead_string(
        args.py_file, 
        args.entry_point, 
        args.max_execution_time
    )
    
    print("\n" + "="*80)
    print("OVERHEAD STRING (as would be sent to LLM):")
    print("="*80)
    print(overhead)
    print("="*80)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(overhead)
        print(f"\nOverhead string saved to: {args.output}")

if __name__ == "__main__":
    main()

