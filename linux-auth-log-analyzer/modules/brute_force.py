from datetime import timedelta

def get_event_time(event):
    return event["time"]


def detect_bruteforce(events, threshold=5, window_minutes=5):
    bruteforce_ips = []
    events.sort(key=get_event_time)

    for i in range(len(events)):
        current_ip = events[i]["ip"]
        start_time = events[i]["time"]
        count = 1

        for j in range(i + 1, len(events)):
            if events[j]["ip"] == current_ip:
                time_diff = events[j]["time"] - start_time

                if time_diff <= timedelta(minutes=window_minutes):
                    count += 1
                    if count >= threshold:
                        bruteforce_ips.append(current_ip)
                        break
                else:
                    break

    return list(set(bruteforce_ips))
