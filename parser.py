import re
from collections import Counter

TRACE_FILE = None


def parse_trace(trace_file):
    system_calls = []

    with open(trace_file, "r") as file:
        for line in file:
            line = line.strip()

            match = re.match(r"^(\w+)\(.*\)\s+=\s+(.+)$", line)

            if match:
                syscall = match.group(1)
                result = match.group(2)

                system_calls.append({
                    "syscall": syscall,
                    "result": result
                })

    return system_calls


def count_system_calls(system_calls):
    counts = Counter()

    for call in system_calls:
        counts[call["syscall"]] += 1

    return counts


if __name__ == "__main__":
    calls = parse_trace()
    counts = count_system_calls(calls)

    print("\nSYSTEM CALL ANALYSIS")
    print("--------------------")

    print("Total system calls:", len(calls))

    print("\nSystem call frequency:")

    for syscall, count in counts.most_common():
        print(f"{syscall:<15} {count}")