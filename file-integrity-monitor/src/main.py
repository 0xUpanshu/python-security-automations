import os

from .scanner import scan_directory
from .baseline import save_baseline, load_baseline

from .detection.analyzer import SecurityAnalyzer
from .alerting.alert_manager import AlertManager
from .incidents.manager import IncidentManager


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MONITORED_DIR = os.path.join(BASE_DIR, "sample_files")
BASELINE_PATH = os.path.join(BASE_DIR, "data", "baseline.json")
INCIDENTS_PATH = os.path.join(BASE_DIR, "data", "incidents.json")
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


def analyze_changes(
    added,
    modified,
    deleted,
    incident_manager,
):
    
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

                incident = incident_manager.create_incident(result)

                alert_manager.alert(result)

                print(
                    f"[!] Incident created: "
                    f"{incident['incident_id']}"
                )

        except Exception as error:

            print(
                f"[!] Security analysis failed: "
                f"{file_path}"
            )

            print(f"    Reason: {error}")

    for file_path in modified:

        print(f"\n[*] Analyzing modified file: {file_path}")

        try:
            result = analyzer.analyze(file_path)
            result["change_type"] = "modified"

            security_results.append(result)

            if result["suspicious"]:

                incident = incident_manager.create_incident(result)

                alert_manager.alert(result)

                print(
                    f"[!] Incident created: "
                    f"{incident['incident_id']}"
                )

        except Exception as error:

            print(
                f"[!] Security analysis failed: "
                f"{file_path}"
            )

            print(f"    Reason: {error}")

    for file_path in deleted:

        print(f"\n[!] Deleted file: {file_path}")

        deleted_result = {
            "file_path": file_path,
            "change_type": "deleted",
            "suspicious": True,
            "indicators": ["file_deleted"],
            "risk": {
                "score": 50,
                "severity": "HIGH",
            },
        }

        security_results.append(deleted_result)

        incident = incident_manager.create_incident(
            deleted_result
        )

        alert_manager.alert(deleted_result)

        print(
            f"[!] Incident created: "
            f"{incident['incident_id']}"
        )

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
        print(
            "[+] Run the program again "
            "to detect changes."
        )

        return

    added, modified, deleted = compare_hashes(
        baseline_hashes,
        current_hashes
    )

    print("\n=== Comparison Report ===")

    print(f"[+] New Files: {added}")
    print(f"[!] Modified Files: {modified}")
    print(f"[-] Deleted Files: {deleted}")

    incident_manager = IncidentManager(
        INCIDENTS_PATH
    )

    security_results = analyze_changes(
        added,
        modified,
        deleted,
        incident_manager,
    )

    print("\n=== Security Analysis ===")

    for result in security_results:

        print(
            f"\nFile: "
            f"{result['file_path']}"
        )

        print(
            f"Change: "
            f"{result['change_type']}"
        )

        print(
            f"Suspicious: "
            f"{result['suspicious']}"
        )

        if result["indicators"]:

            print(
                f"Indicators: "
                f"{', '.join(result['indicators'])}"
            )


if __name__ == "__main__":
    main()