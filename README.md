# OS System Call Activity and Fault Analyser

## 1. Project Overview

The OS System Call Activity and Fault Analyser is a Linux-based tool developed to monitor, analyse, and visualize system calls made by C programs.

The project uses the `strace` utility to capture system-call activity. The captured trace is then parsed and analysed to identify system calls and detect common operating-system-level faults.

The analyser classifies detected faults based on their error codes and provides their severity and recommended actions.

A Flask-based web dashboard is provided to display the analysis results in a user-friendly manner.

---

## 2. Objectives

The main objectives of this project are:

- To trace system calls made by programs in Linux.
- To identify and count system calls.
- To detect system-call failures.
- To classify common error conditions.
- To assign severity levels to detected faults.
- To provide recommended actions for detected faults.
- To visualize system-call and fault information through a web dashboard.
- To generate a text-based analysis report.

---

## 3. Technologies Used

- Operating System: Kali Linux
- Programming Language: Python
- C Programming Language
- Flask
- strace
- HTML
- CSS
- JavaScript
- JSON
- GCC
- VS Code

---

## 4. System Architecture

The project follows the following workflow:

    C Test Program
          |
          v
        strace
          |
          v
    System Call Trace
          |
          v
       Parser
          |
          v
    Fault Detector
          |
          v
    Fault Classifier
          |
          v
       Analyzer
          |
          v
    analysis.json
       /       \
      /         \
     v           v
Web Dashboard   Report Generator
                    |
                    v
             analysis_report.txt

---

## 5. Project Structure

```text
OS-System-Call-Analyzer/
│
├── app.py
├── analyzer.py
├── parser.py
├── fault_detector.py
├── fault_classifier.py
├── tracer.py
├── report_generator.py
│
├── test_programs/
│   ├── normal.c
│   ├── file_error.c
│   ├── permission_error.c
│   ├── fd_error.c
│   ├── normal
│   ├── file_error
│   ├── permission_error
│   └── fd_error
│
├── traces/
│   ├── normal.log
│   ├── file_error.log
│   ├── permission_error.log
│   └── fd_error.log
│
├── data/
│   └── analysis.json
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── reports/
│   └── analysis_report.txt
│
└── README.md