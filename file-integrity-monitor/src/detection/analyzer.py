from pathlib import Path

from .entropy import calculate_entropy
from .suspicious import analyze_file as analyze_filename
from .yara_scanner import YaraScanner


class SecurityAnalyzer:

    def __init__(
        self,
        entropy_threshold: float = 7.2,
        yara_rules_directory: str = "config/yara",
    ):
        self.entropy_threshold = entropy_threshold
        self.yara_scanner = YaraScanner(yara_rules_directory)

    def analyze(self, file_path: str) -> dict:

        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Filename / metadata analysis
        filename_result = analyze_filename(file_path)

        # Entropy analysis
        entropy = calculate_entropy(file_path)
        high_entropy = entropy >= self.entropy_threshold

        # YARA analysis
        yara_matches = self.yara_scanner.scan_file(file_path)

        # Combine all indicators
        indicators = list(filename_result["indicators"])

        if high_entropy:
            indicators.append("high_entropy")

        if yara_matches:
            indicators.append("yara_match")

        return {
            "file_path": str(path),
            "suspicious": bool(indicators),
            "indicators": indicators,
            "entropy": round(entropy, 4),
            "high_entropy": high_entropy,
            "yara_matches": yara_matches,
        }