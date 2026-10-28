import json
import os


INPUT_FILE = "data/analysis.json"
REPORT_DIR = "reports"
REPORT_FILE = os.path.join(
    REPORT_DIR,
    "analysis_report.txt"
)


def generate_report():

    # Create reports folder if it does not exist
    os.makedirs(REPORT_DIR, exist_ok=True)

    # Read analysis data
    with open(INPUT_FILE, "r") as file:
        data = json.load(file)

    report = []

    report.append("OS SYSTEM CALL ANALYZER")
    report.append("=======================")
    report.append("")

    report.append(
        f"Trace File: {data['trace_file']}"
    )

    report.append("")

    # System call summary
    report.append("SYSTEM CALL SUMMARY")
    report.append("-------------------")

    report.append(
        f"Total System Calls : "
        f"{data['total_system_calls']}"
    )

    report.append(
        f"Successful Calls   : "
        f"{data['successful_calls']}"
    )

    report.append(
        f"Total Faults       : "
        f"{data['total_faults']}"
    )

    report.append("")

    # System call frequency
    report.append("SYSTEM CALL FREQUENCY")
    report.append("----------------------")

    for syscall, count in \
            data["system_call_frequency"].items():

        report.append(
            f"{syscall:<20} : {count}"
        )

    report.append("")

    # Fault frequency
    report.append("FAULT FREQUENCY")
    report.append("---------------")

    if data["fault_frequency"]:

        for error, count in \
                data["fault_frequency"].items():

            report.append(
                f"{error:<20} : {count}"
            )

    else:

        report.append(
            "No faults detected."
        )

    report.append("")

    # Fault details
    report.append("FAULT DETAILS")
    report.append("-------------")

    if data["faults"]:

        for number, fault in enumerate(
                data["faults"], 1):

            report.append(
                f"Fault {number}"
            )

            report.append(
                f"Error              : "
                f"{fault['error']}"
            )

            report.append(
                f"System Call        : "
                f"{fault['syscall']}"
            )

            report.append(
                f"Description        : "
                f"{fault['description']}"
            )

            report.append(
                f"Category           : "
                f"{fault.get('category', 'Unknown')}"
            )

            report.append(
                f"Severity           : "
                f"{fault.get('severity', 'Unknown')}"
            )

            report.append(
                f"Recommended Action : "
                f"{fault.get('recommended_action', 'N/A')}"
            )

            report.append(
                f"Trace Line         : "
                f"{fault['line']}"
            )

            report.append(
                f"Trace              : "
                f"{fault['trace']}"
            )

            report.append("")

    else:

        report.append(
            "No faults detected."
        )

    # Write report
    with open(
        REPORT_FILE,
        "w"
    ) as file:

        file.write(
            "\n".join(report)
        )

    return REPORT_FILE


if __name__ == "__main__":

    file_path = generate_report()

    print("\nREPORT GENERATED")
    print("================")
    print("Report saved to:")
    print(file_path)