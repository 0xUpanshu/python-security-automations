import os
import csv

EVIDENCE_DIR = "evidence_data"

def ensure_evidence_dir():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

def write_csv(filename, headers, rows):
    ensure_evidence_dir()
    path = os.path.join(EVIDENCE_DIR, filename)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
