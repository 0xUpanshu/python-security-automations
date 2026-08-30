# File Integrity Monitor

A Python-based security project that monitors folders for unauthorized file changes and suspicious activity. It creates a trusted baseline using SHA-256 hashing, detects modified, added, and deleted files, and performs local security analysis to identify potentially malicious behavior.

This project was built to demonstrate practical cybersecurity automation, file integrity monitoring, and incident handling in a portfolio-ready format.

---

## Overview

File Integrity Monitoring (FIM) is a core security control used to detect tampering, unauthorized changes, and suspicious activity in files that should remain unchanged.

This project helps monitor critical directories by:

- creating a trusted baseline of file hashes
- detecting changes in real time
- identifying new, modified, and deleted files
- analyzing suspicious file characteristics
- generating security incidents and reports

---

## Key Features

- SHA-256-based integrity verification
- Baseline creation and comparison
- Detection of modified, added, and deleted files
- Real-time filesystem monitoring using Watchdog
- Suspicious file and script analysis
- YARA-based detection rules
- Risk scoring and incident creation
- PDF report generation
- GitHub file import support
- GUI-based monitoring and configuration
- Optional VirusTotal integration

---

## Why This Project Matters

This project addresses a real security challenge: detecting whether important files have changed unexpectedly and whether those changes may indicate malicious activity.

It combines two important areas:

1. File integrity monitoring for change detection
2. Security analysis to evaluate whether a change is suspicious

This makes it a useful example of automatic monitoring and threat detection in a cybersecurity workflow.

---

## Tech Stack

- Python
- CustomTkinter for the desktop interface
- TkinterDnD2 for drag-and-drop support
- Watchdog for filesystem event monitoring
- SHA-256 for hashing and integrity verification
- YARA for suspicious pattern detection
- ReportLab for PDF reporting
- JSON for local configuration and incident storage
- Optional VirusTotal API for external threat intelligence

---

## How It Works

```text
Monitored Folder
       |
       v
SHA-256 Hash Calculation
       |
       v
Trusted Baseline
       |
       v
File Change Detected
       |
       v
Compare Current State with Baseline
       |
       +----------------------+
       |                      |
       v                      v
  Unchanged          Modified / Added / Deleted
                            |
                            v
                  Security Analysis
                            |
                            v
                     Incident / Report
```

The workflow is straightforward:

1. A folder is added for monitoring.
2. A baseline is created from the trusted state of files.
3. The application monitors the folder for changes.
4. Current hashes are recalculated and compared with the baseline.
5. Suspicious files are analyzed for indicators such as suspicious extensions or script patterns.
6. Relevant incidents and reports are generated.

---

## Project Structure

```text
file-integrity-monitor/
├── src/
│   ├── alerting/
│   ├── detection/
│   ├── gui/
│   ├── incidents/
│   ├── reporting/
│   ├── services/
│   ├── baseline.py
│   ├── scanner.py
│   └── main.py
├── data/
│   ├── baseline.json
│   ├── incidents.json
│   ├── monitoring_config.json
│   └── github_imports/
├── sample_files/
├── screenshots/
├── requirements.txt
├── .gitignore
├── README.md
└── .env.example
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd file-integrity-monitor
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m src.main
```

---

## Example Workflow

1. Add a folder to monitor.
2. Create a baseline for the folder.
3. Modify, add, or delete a file.
4. The application detects the change.
5. Security checks identify suspicious indicators.
6. An incident is created and reported.

This simulates a realistic monitoring and detection workflow used in security operations.

---

## Security Capabilities

The project is designed to detect a range of integrity and security concerns, including:

- file tampering
- added suspicious files
- deleted files from monitored directories
- double-extension filenames
- PowerShell or script-related indicators
- suspicious patterns matched by YARA rules
- risk-based incident classification

---

## Project Highlights

This project demonstrates hands-on experience in:

- cybersecurity automation
- file integrity monitoring
- cryptographic hashing
- event-driven monitoring
- threat detection workflows
- incident management
- report generation
- Python application development for security tools

---

## Optional Enhancements

- VirusTotal API integration for external file reputation checks
- Expanded YARA rule sets
- Database-backed incident storage
- Centralized logging and alerting
- Remote or enterprise-scale monitoring support

---

## License

This project is intended for educational, portfolio, and cybersecurity learning purposes.
