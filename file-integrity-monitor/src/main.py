import os

from .integrity import calculate_hash
from .scanner import scan_directory
from .baseline import save_baseline, load_baseline
from .reporter import save_report

from .detection.analyzer import SecurityAnalyzer
from .alerting.alert_manager import AlertManager


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MONITORED_DIR = os.path.join(BASE_DIR, "sample_files")
BASELINE_PATH = os.path.join(BASE_DIR, "data", "baseline.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def compare_hashes(old, new):
    added = []
    modified = []
    deleted = []

    for file in new:
        if file not in old:
            added.append(file)
        elif old[file] != new[file]:
            modified.append(file)

    for file in old:
        if file not in new:
            deleted.append(file)

    return added, modified, deleted


def analyze_changes(added, modified, deleted):
    """
    Run security analysis on files that currently exist.

    Added and modified files can be analyzed because they
    are present on disk.

    Deleted files cannot be analyzed because their contents
    are no longer available.
    """

    analyzer = SecurityAnalyzer()
    alert_manager = AlertManager()

    security_results = []

    for file_path in added:
        print(f"\n[*] Analyzing added file: {file_path}")

        try:
            result = analyzer.analyze(file_path)
            result["change_type"] = "added"

            security_results.append(result)

            if result["suspicious"]:
                alert_manager.alert(result)

        except Exception as error:
            print(f"[!] Security analysis failed: {file_path}")
            print(f"    Reason: {error}")

    for file_path in modified:
        print(f"\n[*] Analyzing modified file: {file_path}")

        try:
            result = analyzer.analyze(file_path)
            result["change_type"] = "modified"

            security_results.append(result)

            if result["suspicious"]:
                alert_manager.alert(result)

        except Exception as error:
            print(f"[!] Security analysis failed: {file_path}")
            print(f"    Reason: {error}")

    for file_path in deleted:
        print(f"\n[!] Deleted file: {file_path}")

        deleted_result = {
            "file_path": file_path,
            "change_type": "deleted",
            "suspicious": True,
            "indicators": ["file_deleted"],
        }

        security_results.append(deleted_result)

        alert_manager.alert({
            "file_path": file_path,
            "indicators": ["file_deleted"],
            "risk": {
                "score": 50,
                "severity": "HIGH",
            },
        })

    return security_results


def main():
    print("[*] Scanning directory...")

    current_hashes = scan_directory(MONITORED_DIR)
    baseline_hashes = load_baseline(BASELINE_PATH)

    if not baseline_hashes:
        print("[+] Creating baseline...")

        save_baseline(
            current_hashes,
            BASELINE_PATH
        )

        print("[+] Baseline saved.")
        print("[+] Run the program again to detect changes.")

        return

    added, modified, deleted = compare_hashes(
        baseline_hashes,
        current_hashes
    )

    print("\n=== Comparison Report ===")

    print(f"[+] New Files: {added}")
    print(f"[!] Modified Files: {modified}")
    print(f"[-] Deleted Files: {deleted}")

    security_results = analyze_changes(
        added,
        modified,
        deleted
    )

    report_file = save_report(
        added,
        modified,
        deleted,
        REPORTS_DIR
    )

    print(f"\n[+] Report saved at: {report_file}")

    print("\n=== Security Analysis ===")

    for result in security_results:

        print(f"\nFile: {result['file_path']}")
        print(f"Change: {result['change_type']}")
        print(f"Suspicious: {result['suspicious']}")

        if result["indicators"]:
            print(
                f"Indicators: "
                f"{', '.join(result['indicators'])}"
            )


if __name__ == "__main__":
    main()