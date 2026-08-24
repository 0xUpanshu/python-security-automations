from pathlib import Path

from ..integrity import calculate_hash
from .entropy import calculate_entropy
from .suspicious import analyze_file as analyze_filename
from .yara_scanner import YaraScanner
from .reputation import VirusTotalReputation


class SecurityAnalyzer:

    def __init__(
        self,
        entropy_threshold: float = 7.2,
        yara_rules_directory: str = "config/yara",
    ):
        self.entropy_threshold = entropy_threshold
        self.yara_scanner = YaraScanner(yara_rules_directory)
        self.virustotal = VirusTotalReputation()

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

        # 4. SHA-256 + VirusTotal reputation
        sha256 = calculate_hash(file_path)
        virustotal_result = self.virustotal.check_hash(sha256)

        # 5. Combine indicators
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

        # 6. Return combined result
        return {
            "file_path": str(path),
            "sha256": sha256,
            "suspicious": bool(indicators),
            "indicators": indicators,
            "entropy": round(entropy, 4),
            "high_entropy": high_entropy,
            "yara_matches": yara_matches,
            "yara_available": self.yara_scanner.available,
            "virustotal": virustotal_result,
        }