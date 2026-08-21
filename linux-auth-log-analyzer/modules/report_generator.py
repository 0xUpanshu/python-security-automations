import os

REPORT_DIR="reports"
def report_dir():
    os.mkdir(REPORT_DIR, exist_ok=True)

def generate_incident_report(
        failed_counts,
        bruteforce_ips, 
        time_spikes, 
        suspecious_ips,
        output_file=os.path.join(REPORT_DIR, "incident_report.txt")
):
    with open(output_file,"w") as report:
        report.write("---Linux Incident Report---\n\n")

        total_failed = sum(failed_counts.values())
        report.write(f"Total Failed Login Attempts: {total_failed}\n\n")

        report.write ("Bruteforce IPs Detected:\n")
        if bruteforce_ips:
            for bf_ip in bruteforce_ips:
                report.write(f"- {bf_ip} ({failed_counts.get(bf_ip, 0)} attempts)\n")
        else:
            report.write("None Detected\n")
        report.write("\n")

        report.write("Time-based Spikes Detected:\n")
        if time_spikes:
            for spike in time_spikes:
                report.write(
                    f"- IP: {spike['ip']}, Attempts: {spike['attempts']}, "
                    f"From: {spike['start_time'].time()} To: {spike['end_time'].time()}\n"
                )
        else:
            report.write("No time based spikes detected\n\n")
        report.write("\n")

        report.write("Suspicious IPs Identified:\n")
        if suspecious_ips:
            for entry in suspecious_ips:
                report.write(f"- IP: {entry['ip']}\n")
                for reason in entry["reasons"]:
                    report.write(f"  - {reason}\n")
        else:
            report.write("None identified\n")

    print(f"[+] Incident report generated: {output_file}")
