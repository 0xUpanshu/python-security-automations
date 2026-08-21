def is_private_ip(ip):

    private_range = (
        ip.startswith("10."), 
        ip.startswith("192.168."),
        ip.startswith("172.16")
        )
    
    return any(private_range)

def detect_suspicious_ips (events, failed_count, bruteforce_ips):
    suspicious = []
    ip_users= {}

    for event in events:
        ip = event["ip"]
        user = event ["user"]

        if ip not in ip_users:
            ip_users[ip] = set()

            ip_users[ip].add(user)
    for ip, count in failed_count.items():
        reasons = []

        if count >= 2:
            reasons.append("Multiple failed login attempts")

        if ip in bruteforce_ips:
            reasons.append("Bruteforce behaviour detected")

        if len(ip_users.get(ip, [])) > 1:
            reasons.append("Multiple users attempted from this IP")
        
        if not is_private_ip(ip):
            reasons.append("Public IP address")

        if reasons:
            suspicious.append({
                "ip":ip,
                "reasons": reasons
            })

        return suspicious