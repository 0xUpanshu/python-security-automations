def count_failed_logins(events):
    ip_counter ={}

    for event in events:
        ip = event["ip"]

        if ip in ip_counter:
            ip_counter[ip]+= 1
        else:
            ip_counter[ip] = 1
    return ip_counter