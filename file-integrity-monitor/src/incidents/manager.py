import json
import os
from datetime import datetime


class IncidentManager:

    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        directory = os.path.dirname(
            self.storage_path
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True,
            )

        if not os.path.exists(
            self.storage_path
        ):
            self._save([])

    def _load(self) -> list:
        try:
            with open(
                self.storage_path,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            return data if isinstance(
                data,
                list,
            ) else []

        except (
            json.JSONDecodeError,
            OSError,
        ):
            return []

    def _save(self, incidents: list):
        with open(
            self.storage_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                incidents,
                file,
                indent=4,
            )

    def _generate_incident_id(
        self,
        incidents: list,
    ) -> str:
        year = datetime.now().year

        incident_number = (
            len(incidents) + 1
        )

        return (
            f"INC-{year}-"
            f"{incident_number:04d}"
        )

    def create_incident(
        self,
        analysis: dict,
    ) -> dict:

        incidents = self._load()

        incident = {
            "incident_id":
                self._generate_incident_id(
                    incidents
                ),

            "created_at":
                datetime.now().isoformat(
                    timespec="seconds"
                ),

            "analysis": analysis,
        }

        incidents.append(
            incident
        )

        self._save(
            incidents
        )

        return incident

    def get_all_incidents(self) -> list:
        return self._load()

    def get_incident(
        self,
        incident_id: str,
    ):
        incidents = self._load()

        for incident in incidents:
            if (
                incident.get(
                    "incident_id"
                )
                == incident_id
            ):
                return incident

        return None