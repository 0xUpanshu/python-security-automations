import os

import requests
from dotenv import load_dotenv


load_dotenv()


class VirusTotalReputation:

    API_URL = "https://www.virustotal.com/api/v3"

    def __init__(self):
        self.api_key = os.getenv("VIRUSTOTAL_API_KEY")
        self.available = bool(self.api_key)

    def _headers(self):
        """
        Build HTTP headers required by the VirusTotal API.
        """

        return {
            "x-apikey": self.api_key,
            "Accept": "application/json",
        }

    def check_hash(self, sha256: str) -> dict:


        # If No file is uploaded. Only the hash is sent to VirusTotal.
        if not self.available:
            return {
                "available": False,
                "known": False,
                "malicious": 0,
                "suspicious": 0,
                "total_engines": 0,
            }

        url = f"{self.API_URL}/files/{sha256}"

        try:
            response = requests.get(
                url,
                headers=self._headers(),
                timeout=10,
            )

            # VirusTotal does not know this hash.
            if response.status_code == 404:
                return {
                    "available": True,
                    "known": False,
                    "malicious": 0,
                    "suspicious": 0,
                    "total_engines": 0,
                }

            response.raise_for_status()

            data = response.json()

            stats = data["data"]["attributes"]["last_analysis_stats"]

            return {
                "available": True,
                "known": True,
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "total_engines": sum(stats.values()),
            }

        except requests.RequestException:
            return {
                "available": False,
                "known": False,
                "malicious": 0,
                "suspicious": 0,
                "total_engines": 0,
            }