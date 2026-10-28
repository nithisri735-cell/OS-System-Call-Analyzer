import subprocess
import os


def run_trace(program_name):
    project_dir = os.getcwd()

    program_path = os.path.join(project_dir, "test_programs", program_name)
    trace_path = os.path.join(
        project_dir,
        "traces",
        os.path.splitext(program_name)[0] + ".log"
    )

    os.makedirs(os.path.join(project_dir, "traces"), exist_ok=True)

    if not os.path.exists(program_path):
        print("Program not found:", program_path)
        return None

    print("\nRunning:", program_name)
    print("Capturing system calls...")

    try:
        result = subprocess.run(
            ["strace", "-o", trace_path, "./" + program_name],
            cwd=os.path.join(project_dir, "test_programs"),
            capture_output=True,
            text=True
        )

        print("\nProgram output:")

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        if os.path.exists(trace_path):
            print("Trace saved to:", trace_path)
        else:
            print("Trace file was not created.")

        return trace_path

    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":

    print("OS SYSTEM CALL TRACER")
    print("=====================")

    print("\nAvailable programs:")
    print("1. normal")
    print("2. file_error")
    print("3. permission_error")
    print("4. fd_error")

    choice = input("\nEnter your choice: ")

    programs = {
        "1": "normal",
        "2": "file_error",
        "3": "permission_error",
        "4": "fd_error"
    }

    if choice in programs:
        run_trace(programs[choice])
    else:
        print("Invalid choice.")