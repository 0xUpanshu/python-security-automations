from datetime import timedelta


def detect_time_spikes(events, window_seconds=60, threshold=5):
    """ Detects time-based spikes of failed login attempts per IP."""

    ip_timestamps = {}

    for event in events:
        ip = event["ip"]
        timestamp = event["time"]

        if ip not in ip_timestamps:
            ip_timestamps[ip] = []

        ip_timestamps[ip].append(timestamp)

    spikes = []

    for ip, timestamps in ip_timestamps.items():
        timestamps.sort()

        start = 0

        for end in range(len(timestamps)):
            while timestamps[end] - timestamps[start] > timedelta(seconds=window_seconds):
                start += 1

            attempts_in_window = end - start + 1

            if attempts_in_window >= threshold:
                spikes.append({
                    "ip": ip,
                    "attempts": attempts_in_window,
                    "start_time": timestamps[start],
                    "end_time": timestamps[end]
                })
                break  

    return spikes
