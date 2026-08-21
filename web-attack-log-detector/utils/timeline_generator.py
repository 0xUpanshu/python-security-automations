import csv
import os
from datetime import datetime

EVIDENCE_DIR = "evidence_data"

def timeline_generate():
    timeline = []

    for file in os.listdir(EVIDENCE_DIR):
        if not file.endswith(".csv"):
            continue

        path = os.path.join(EVIDENCE_DIR, file)

        with open(path, "r") as f:
            reader = csv.reader(f)
            headers = next(reader, None)

            for row in reader:
                timeline.append([
                    file,
                    row[0],
                    row[-1]
                ])

    out = os.path.join(EVIDENCE_DIR, "timeline.csv")
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "ip", "event"])
        writer.writerows(timeline)
