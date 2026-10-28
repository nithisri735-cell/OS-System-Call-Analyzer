import re


FAULT_CODES = {
    "ENOENT": "File or directory not found",
    "EACCES": "Permission denied",
    "EPERM": "Operation not permitted",
    "EBADF": "Bad file descriptor",
    "EINVAL": "Invalid argument",
    "ENOMEM": "Out of memory",
    "ENOSPC": "No space left on device",
    "EEXIST": "File already exists"
}


def detect_faults(trace_file):
    faults = []

    with open(trace_file, "r") as file:
        for line_number, line in enumerate(file, start=1):

            # Ignore Linux startup check for /etc/ld.so.preload
            if "/etc/ld.so.preload" in line:
                continue

            for code, description in FAULT_CODES.items():

                if code in line:
                    match = re.match(r"^(\w+)\(", line.strip())

                    syscall = match.group(1) if match else "unknown"

                    faults.append({
                        "line": line_number,
                        "syscall": syscall,
                        "error": code,
                        "description": description,
                        "trace": line.strip()
                    })

    return faults


if __name__ == "__main__":

    trace_file = "traces/trace.log"

    faults = detect_faults(trace_file)

    print("\nFAULT ANALYSIS")
    print("--------------")

    print("Total faults:", len(faults))

    if faults:
        for fault in faults:
            print(f"\nLine      : {fault['line']}")
            print(f"System call: {fault['syscall']}")
            print(f"Error     : {fault['error']}")
            print(f"Description: {fault['description']}")
    else:
        print("No faults detected.")