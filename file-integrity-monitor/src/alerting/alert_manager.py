from datetime import datetime

from ..utils.logger import get_logger


class AlertManager:

    def __init__(self):
        self.logger = get_logger("AlertManager")

    def alert(self, analysis: dict) -> None:       

        # Generate an alert from a security analysis result.

        risk = analysis.get("risk", {})

        score = risk.get("score", 0)
        severity = risk.get("severity", "LOW")

        file_path = analysis.get("file_path", "Unknown")
        indicators = analysis.get("indicators", [])

        timestamp = datetime.now().isoformat(timespec="seconds")

        message = (
            f"[{severity}] File: {file_path} | "
            f"Score: {score} | "
            f"Indicators: {', '.join(indicators) or 'None'}"
        )

        if severity in {"HIGH", "CRITICAL"}:
            self.logger.error(message)
        elif severity == "MEDIUM":
            self.logger.warning(message)
        else:
            self.logger.info(message)

        print(f"{timestamp} | {message}")