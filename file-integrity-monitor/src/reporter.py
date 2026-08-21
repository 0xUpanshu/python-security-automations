import os
from datetime import datetime

def save_report(added, modified, deleted, reports_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(reports_dir, f"report_{timestamp}.txt")

    with open(report_path, 'w') as report_file:
        report_file.write("=== File Integrity Monitoring Report ===\n")
        report_file.write(f"Generated at: {timestamp}\n\n")

        report_file.write("[+] New Files:\n")
        for file in added:
            report_file.write(f"{file}\n")

        report_file.write("\n[!] Modified Files:\n")
        for file in modified:
            report_file.write(f"{file}\n")

        report_file.write("\n[-] Deleted Files:\n")
        for file in deleted:
            report_file.write(f"{file}\n")

    return report_path
