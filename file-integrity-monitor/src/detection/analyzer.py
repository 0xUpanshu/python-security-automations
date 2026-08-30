from pathlib import Path

from ..integrity import calculate_hash
from .entropy import calculate_entropy
from .suspicious import analyze_file as analyze_filename
from .yara_scanner import YaraScanner
from .reputation import VirusTotalReputation
from .risk import RiskEvaluator
from .indicators import extract_public_ipv4_addresses


class SecurityAnalyzer:

    def __init__(
        self,
        entropy_threshold: float = 7.2,
        yara_rules_directory: str = "config/yara",
    ):
        self.entropy_threshold = entropy_threshold
        self.yara_scanner = YaraScanner(yara_rules_directory)
        self.virustotal = VirusTotalReputation()
        self.risk_evaluator = RiskEvaluator()

    def analyze(self, file_path: str) -> dict:

        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # 1. Filename / metadata analysis
        filename_result = analyze_filename(file_path)

        # 2. Entropy analysis
        entropy = calculate_entropy(file_path)
        high_entropy = entropy >= self.entropy_threshold

        # 3. YARA analysis
        yara_matches = self.yara_scanner.scan_file(file_path)

        # 4. SHA-256 + VirusTotal file reputation
        sha256 = calculate_hash(file_path)
        virustotal_result = self.virustotal.check_hash(sha256)

        # 5. Extract public IPv4 addresses
        with open(file_path, "r", errors="ignore") as file:
            content = file.read()

        public_ips = extract_public_ipv4_addresses(content)

        # 6. Check IP reputation
        ip_reputation = []

        for ip_address in public_ips:
            result = self.virustotal.check_ip(ip_address)
            ip_reputation.append(result)

        # 7. Combine detection indicators
        indicators = list(filename_result["indicators"])

        if high_entropy:
            indicators.append("high_entropy")

        if yara_matches:
            indicators.append("yara_match")

        if virustotal_result["known"] and (
            virustotal_result["malicious"] > 0
            or virustotal_result["suspicious"] > 0
        ):
            indicators.append("virustotal_detection")

        if any(
            result["known"] and result["malicious"] > 0
            for result in ip_reputation
        ):
            indicators.append("malicious_ip")

        # 8. Build analysis result
        analysis = {
            "file_path": str(path),
            "sha256": sha256,
            "suspicious": bool(indicators),
            "indicators": indicators,
            "entropy": round(entropy, 4),
            "high_entropy": high_entropy,
            "yara_matches": yara_matches,
            "yara_available": self.yara_scanner.available,
            "virustotal": virustotal_result,
            "public_ips": public_ips,
            "ip_reputation": ip_reputation,
        }

        # 9. Calculate risk
        risk = self.risk_evaluator.evaluate(analysis)

        analysis["risk"] = risk

        return analysis