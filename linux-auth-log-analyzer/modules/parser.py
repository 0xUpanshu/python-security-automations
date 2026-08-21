import re
from datetime import datetime
def parser_auth_log(file_path):
    events = []

    ip_pattern = re.compile(r'from (\d+\.\d+\.\d+\.\d+)')
    user_pattern = re.compile(r'for (invalid user )?(\w+)')
    timematch_pattern = re.compile(r'^(\w+\s+\d+\s+\d+:\d+:\d+)')

    with open(file_path, "r") as file:
        for line in file:
            if "Failed password" in line:
                ip_match = ip_pattern.search(line)
                user_match = user_pattern.search(line)
                time_match = timematch_pattern.search(line)  

                if ip_match and user_match and time_match:
                    timestamp = datetime.strptime(
                        time_match.group(1),
                        "%b %d %H:%M:%S"
                    )

                if ip_match and user_match:
                    event = {
                        "ip": ip_match.group(1),
                        "user": user_match.group(2),
                        "time": timestamp,
                        "raw": line.strip()
                    }
                    events.append(event)

    return events
