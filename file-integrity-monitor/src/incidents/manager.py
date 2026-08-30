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

    def _find_existing_incident(
        self,
        incidents: list,
        analysis: dict,
    ):
        file_path = str(
            analysis.get("file_path", "")
        )
        change_type = analysis.get("change_type")
        current_hash = analysis.get("current_hash")
        baseline_hash = analysis.get("baseline_hash")
        sha256 = analysis.get("sha256")

        for incident in incidents:
            previous_analysis = incident.get("analysis", {})

            if previous_analysis.get("file_path") != file_path:
                continue

            previous_change_type = previous_analysis.get("change_type")
            previous_current_hash = previous_analysis.get("current_hash")
            previous_baseline_hash = previous_analysis.get("baseline_hash")
            previous_sha256 = previous_analysis.get("sha256")

            same_hash = (
                previous_current_hash == current_hash
                or previous_sha256 == sha256
            )
            same_state = (
                previous_change_type == change_type
                and previous_current_hash == current_hash
                and previous_baseline_hash == baseline_hash
            )

            if same_hash or same_state:
                return incident

        return None

    def create_incident(
        self,
        analysis: dict,
    ) -> dict:

        incidents = self._load()

        existing = self._find_existing_incident(
            incidents,
            analysis,
        )

        if existing is not None:
            return existing

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