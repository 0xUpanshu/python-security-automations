def build_ip_time_map(events):
    ip_time_map={}

    for event in events:
        ip=event.get("ip")
        time = event.get("time")

        if not ip or not time:
            continue

        ip_time_map.setdefault(ip, []).append(time)

    return ip_time_map