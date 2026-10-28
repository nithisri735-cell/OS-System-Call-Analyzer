import json
import sys
from collections import Counter
from parser import parse_trace, count_system_calls
from fault_detector import detect_faults
from fault_classifier import classify_fault

OUTPUT_FILE = "data/analysis.json"


def analyze(trace_file):

    # Parse system calls from the selected trace
    system_calls = parse_trace(trace_file)

    # Count system calls
    call_counts = count_system_calls(system_calls)

    # Detect faults
    faults = detect_faults(trace_file)
       
    # Classify each fault
    for fault in faults:

        classification = classify_fault(
            fault["error"]
        )

        fault["category"] = classification["category"]
        fault["severity"] = classification["severity"]
        fault["recommended_action"] = classification["action"]

    

    # Count fault types
    fault_counts = Counter()

    for fault in faults:
        fault_counts[fault["error"]] += 1

    total_calls = len(system_calls)
    total_faults = len(faults)

    # Prepare analysis result
    analysis = {
        "trace_file": trace_file,
        "total_system_calls": total_calls,
        "successful_calls": total_calls - total_faults,
        "total_faults": total_faults,
        "system_call_frequency": dict(call_counts),
        "fault_frequency": dict(fault_counts),
        "faults": faults
    }

    # Save analysis
    with open(OUTPUT_FILE, "w") as file:
        json.dump(analysis, file, indent=4)

    return analysis


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python3 analyzer.py <trace_file>")
        print("\nExample:")
        print("python3 analyzer.py traces/fd_error.log")
        sys.exit(1)

    trace_file = sys.argv[1]

    result = analyze(trace_file)

    print("\nOS SYSTEM CALL ANALYZER")
    print("=======================")

    print("Trace file          :", result["trace_file"])
    print("Total system calls  :", result["total_system_calls"])
    print("Successful calls    :", result["successful_calls"])
    print("Total faults        :", result["total_faults"])

    print("\nSystem Call Frequency:")

    for syscall, count in result["system_call_frequency"].items():
        print(f"  {syscall:<15} {count}")

    print("\nFault Frequency:")

    if result["fault_frequency"]:
        for error, count in result["fault_frequency"].items():
            print(f"  {error:<10} {count}")
    else:
        print("  No faults detected.")

    print("\nAnalysis saved to:")
    print(OUTPUT_FILE)