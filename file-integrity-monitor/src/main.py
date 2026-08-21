import os
from scanner import scan_directory
from baseline import save_baseline, load_baseline
from reporter import save_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONITORED_DIR = os.path.join(BASE_DIR, "monitored_dir")
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


if __name__ == "__main__":
    print("[*] Scanning directory...")
    current_hashes = scan_directory(MONITORED_DIR)
    baseline_hashes = load_baseline(BASELINE_PATH)

    if not baseline_hashes:
        print("[+] Creating baseline...")
        save_baseline(current_hashes, BASELINE_PATH)
        print("[+] Baseline saved. Run again to compare.")
    else:
        added, modified, deleted = compare_hashes(baseline_hashes, current_hashes)

        print("\n=== Comparison Report ===")
        print(f"[+] New Files: {added}")
        print(f"[!] Modified Files: {modified}")
        print(f"[-] Deleted Files: {deleted}")

report_file = save_report(added, modified, deleted, REPORTS_DIR)
print(f"\n[+] Report saved at: {report_file}")
