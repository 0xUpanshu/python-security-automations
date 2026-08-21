from modules.parser import parser_auth_log
from modules.failed_logins import count_failed_logins
from modules.brute_force import detect_bruteforce
from modules.suspicious_ip import detect_suspicious_ips
from modules.time_spike import detect_time_spikes
from modules.report_generator import generate_incident_report
from modules.evidance_exporter import (export_bruteforce_ips,export_time_spikes,export_suspicious_ips)
from modules.ip_time_map import build_ip_time_map

from modules.report_generator import generate_incident_report 

events = parser_auth_log("logs/sample_auth.log")
ip_time_map = build_ip_time_map(events)
failed = count_failed_logins(events)
bruteforce = detect_bruteforce(events)
spikes = detect_time_spikes(events)
suspicious = detect_suspicious_ips(events, failed, bruteforce)

export_bruteforce_ips(bruteforce, failed, ip_time_map)
export_time_spikes(spikes)
export_suspicious_ips(suspicious)

generate_incident_report(failed, bruteforce, spikes, suspicious)

