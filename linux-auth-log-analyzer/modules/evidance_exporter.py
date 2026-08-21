import csv
import os

EVIDENCE_DIR="evidence_data"

def evidence_dir():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)


def export_bruteforce_ips(bruteforce_ips, failed_counts, ip_time_map):
    evidence_dir()
    path = os.path.join(EVIDENCE_DIR, "bruteforce_ips.csv")
    
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ip_address", "failed_attempts", "first_seen", "last_seen"])
        for ip in bruteforce_ips:
            times = ip_time_map.get(ip, [])
            writer.writerow([
                ip,
                failed_counts.get(ip, 0),
                min(times).time() if times else "N/A",
                max(times).time() if times else "N/A"
            ])


def export_time_spikes(time_spikes):
    evidence_dir()
    path = os.path.join(EVIDENCE_DIR, "time_spike_events.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ip", "attempts", "window_start", "window_end"])

        for spike in time_spikes:
            writer.writerow([
                spike["ip"],
                spike["attempts"],
                spike["start_time"].time(),
                spike["end_time"].time()
            ])


def export_suspicious_ips(suspicious_ips):
    evidence_dir()
    path = os.path.join(EVIDENCE_DIR, "suspicious_ips.csv")

    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ip", "indicators"])

        for entry in suspicious_ips:
            writer.writerow([
                entry["ip"],
                "; ".join(entry["reasons"])
            ])