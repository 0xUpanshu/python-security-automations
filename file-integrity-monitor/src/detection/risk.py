class RiskEvaluator:

    INDICATOR_WEIGHTS = {
        "double_extension": 20,
        "hidden_file": 10,
        "executable_or_script": 10,
        "high_entropy": 15,
        "yara_match": 30,
        "virustotal_detection": 40,
    }

    def calculate_score(self, analysis: dict) -> int:
        """
        Calculate a risk score from analysis evidence.
        """

        score = 0

        for indicator in analysis.get("indicators", []):
            score += self.INDICATOR_WEIGHTS.get(indicator, 0)

        virustotal = analysis.get("virustotal", {})

        if virustotal.get("known"):
            suspicious = virustotal.get("suspicious", 0)
            malicious = virustotal.get("malicious", 0)

            if suspicious > 0:
                score += 20

            if malicious > 0:
                score += 40

        return min(score, 100)

    def get_severity(self, score: int) -> str:
        """
        Convert a numerical risk score into a severity level.
        """

        if score >= 80:
            return "CRITICAL"

        if score >= 60:
            return "HIGH"

        if score >= 30:
            return "MEDIUM"

        return "LOW"

    def evaluate(self, analysis: dict) -> dict:
        # Produce a complete risk assessment.
        score = self.calculate_score(analysis)
        severity = self.get_severity(score)

        return {
            "score": score,
            "severity": severity,
        }