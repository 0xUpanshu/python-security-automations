from pathlib import Path

from .entropy import calculate_entropy, is_high_entropy
from .suspicious import analyze_file as analyze_filename


class SecurityAnalyzer:


    def __init__(self, entropy_threshold: float = 7.2):
        self.entropy_threshold = entropy_threshold

    def analyze(self, file_path: str) -> dict:

        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Filename / metadata heuristics
        filename_result = analyze_filename(file_path)

        # Entropy analysis
        entropy = calculate_entropy(file_path)
        high_entropy = entropy >= self.entropy_threshold

        indicators = list(filename_result["indicators"])

        if high_entropy:
            indicators.append("high_entropy")

        return {
            "file_path": str(path),
            "suspicious": bool(indicators),
            "indicators": indicators,
            "entropy": round(entropy, 4),
            "high_entropy": high_entropy,
        }