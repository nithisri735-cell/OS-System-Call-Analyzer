from flask import Flask, render_template, jsonify, request, send_file
import json
import os
import subprocess
from report_generator import generate_report

app = Flask(__name__)

ANALYSIS_FILE = "data/analysis.json"

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
    analysis = load_analysis()
    return render_template(
        "index.html",
        analysis=analysis
    )


@app.route("/run", methods=["POST"])
def run_analysis():

    data = request.get_json()
    program = data.get("program")

    if program not in PROGRAMS:
        return jsonify({
            "success": False,
            "message": "Invalid program selected."
        }), 400

    program_name = PROGRAMS[program]

    trace_file = f"traces/{program_name}.log"

    try:

        # Run strace
        result = subprocess.run(
            [
                "strace",
                "-o",
                trace_file,
                f"./{program_name}"
            ],
            cwd="test_programs",
            capture_output=True,
            text=True
        )

        # Run analyzer
        subprocess.run(
            [
                "python3",
                "analyzer.py",
                trace_file
            ],
            capture_output=True,
            text=True
        )

        return jsonify({
            "success": True,
            "program": program_name,
            "output": result.stderr
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
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

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )