from utils.evidance_csv import write_csv
import re

XSS_KEYWORDS = ["<script", "</script", "javascript:", "onerror=", "onload=", "<img"]
TIME_REGEX = r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+\-]\d{4})\]'

def detect_xss(log_file):
    count = 0
    attacker_ips = {}
    events = []

    with open(log_file, "r") as file:
        for line in file:
            lower_line = line.lower()

            if any(keyword in lower_line for keyword in XSS_KEYWORDS):
                count += 1
                ip = line.split(" ")[0]
                attacker_ips[ip] = attacker_ips.get(ip, 0) + 1

                time_match = re.search(TIME_REGEX, line)
                timestamp = time_match.group(1) if time_match else "N/A"

                events.append([timestamp, ip, "XSS", line.strip()])

    write_csv("xss_summary.csv",
              ["timestamp", "ip_address", "attack_type", "log_entry"], events)

    return count, attacker_ips
