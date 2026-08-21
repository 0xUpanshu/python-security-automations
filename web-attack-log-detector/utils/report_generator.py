def generate_report(results, output_file):
    with open(output_file, "w") as report:
        report.write("--- Web Attack Incident Report ---\n\n")

        sqli = results["SQL Injection"]
        report.write("[SQL Injection Activity]\n")
        report.write(f"Total SQL Injection Attempts: {sqli['count']}\n\n")

        if sqli["ips"]:
            report.write("Attacker IPs:\n")
            for ip, count in sqli["ips"].items():
                report.write(f"- {ip} ({count} attempts)\n")
                report.write("  - Login bypass and database manipulation attempts\n")
        else:
            report.write("No SQL Injection activity detected\n")

        report.write("\n")

        xss = results["XSS"]
        report.write("[XSS Activity]\n")
        report.write(f"Total XSS Attempts: {xss['count']}\n\n")

        if xss["ips"]:
            report.write("Attacker IPs:\n")
            for ip, count in xss["ips"].items():
                report.write(f"- {ip} ({count} attempts)\n")
                report.write("  - Client-side script injection attempts\n")
        else:
            report.write("No XSS activity detected\n")

        report.write("\n")

        path = results["Path Traversal"]
        report.write("[Path Traversal Activity]\n")
        report.write(f"Total Path Traversal Attempts: {path['count']}\n\n")

        if path["ips"]:
            report.write("Attacker IPs:\n")
            for ip, count in path["ips"].items():
                report.write(f"- {ip} ({count} attempts)\n")
                report.write("  - Unauthorized access to sensitive system files\n")
        else:
            report.write("No Path Traversal activity detected\n")

        report.write("\n")

        report.write("[Overall Observation]\n")
        report.write(
            "The detected activities indicate malicious probing and automated scanning behaviour "
            "targeting common web application vulnerabilities.\n"
        )
