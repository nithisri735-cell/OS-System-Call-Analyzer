
from flask import Flask, render_template, jsonify, request, send_file
import json
import os
import subprocess
from report_generator import generate_report

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_FILE = os.path.join(BASE_DIR, "data", "analysis.json")

PROGRAMS = {
    "normal": "normal",
    "file_error": "file_error",
    "permission_error": "permission_error",
    "fd_error": "fd_error"
}


def load_analysis():
    if not os.path.exists(ANALYSIS_FILE):
        return {
            "total_system_calls": 0,
            "successful_calls": 0,
            "total_faults": 0,
            "system_call_frequency": {},
            "fault_frequency": {},
            "faults": []
        }

    with open(ANALYSIS_FILE, "r") as file:
        return json.load(file)


@app.route("/")
def home():
    return render_template("index.html", analysis=load_analysis())


@app.route("/run", methods=["POST"])
def run_analysis():
    data = request.get_json(silent=True) or {}
    program = data.get("program")

    if program not in PROGRAMS:
        return jsonify({
            "success": False,
            "message": "Invalid program selected."
        }), 400

    program_name = PROGRAMS[program]
    trace_file = os.path.join(BASE_DIR, "traces", f"{program_name}.log")
    executable = os.path.join(BASE_DIR, "test_programs", program_name)

    try:
        result = subprocess.run(
            ["strace", "-o", trace_file, executable],
            cwd=os.path.join(BASE_DIR, "test_programs"),
            capture_output=True,
            timeout=10,
            check=False
        )

        if not os.path.exists(trace_file):
            return jsonify({
                "success": False,
                "message": "System-call trace was not created."
            }), 500

        analysis_result = subprocess.run(
            ["python3", os.path.join(BASE_DIR, "analyzer.py"), trace_file],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )

        if analysis_result.returncode != 0:
            return jsonify({
                "success": False,
                "message": analysis_result.stderr or "Analysis failed."
            }), 500

        return jsonify({
            "success": True,
            "program": program_name,
            "output": result.stderr.decode("utf-8", errors="replace")
})

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "message": "Analysis timed out."
        }), 504

    except (OSError, subprocess.SubprocessError) as error:
        app.logger.exception("Failed to run analysis")
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@app.route("/api/analysis")
def api_analysis():
    return jsonify(load_analysis())


@app.route("/generate-report")
def generate_report_route():
    try:
        report_file = generate_report()
        return send_file(
            report_file,
            as_attachment=True,
            download_name="analysis_report.txt"
        )
    except Exception:
        app.logger.exception("Report generation failed")
        return jsonify({
            "success": False,
            "message": "Could not generate the report."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
