from utils.evidance_csv import write_csv
import re

SQLI_KEYWORDS = ["'", " OR ", "--", "UNION", "SELECT"]
TIME_REGEX = r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+\-]\d{4})\]'

def detect_sqli(log_file):
    count = 0
    attacker_ips = {}
    events = []

    with open(log_file, "r") as file:
        for line in file:
            if any(keyword.lower() in line.lower() for keyword in SQLI_KEYWORDS):
                count += 1
                ip = line.split(" ")[0]
                attacker_ips[ip] = attacker_ips.get(ip, 0) + 1

                time_match = re.search(TIME_REGEX, line)
                timestamp = time_match.group(1) if time_match else "N/A"

                events.append([timestamp, ip, "SQL Injection", line.strip()])

    write_csv("sqli_summary.csv",
              ["timestamp", "ip_address", "attack_type", "log_entry"],
              events)
    
    return count, attacker_ips