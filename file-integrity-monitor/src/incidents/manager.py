import json
import os
from datetime import datetime


class IncidentManager:

    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):

        # Create the storage directory/file if they do not exist.

        directory = os.path.dirname(self.storage_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.storage_path):
            self._save([])

    def _load(self) -> list:
        # Load all stored incidents.

        try:
            with open(self.storage_path, "r", encoding="utf-8") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, incidents: list):
        # Persist incident history to disk.

        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(
                incidents,
                file,
                indent=4
            )

    def _generate_incident_id(self, incidents: list) -> str:
    
        # Generate a sequential incident ID.
        year = datetime.now().year

        incident_number = len(incidents) + 1

        return f"INC-{year}-{incident_number:04d}"

    def create_incident(self, analysis: dict) -> dict:

        incidents = self._load()

        incident = {
            "incident_id": self._generate_incident_id(incidents),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "analysis": analysis,
        }

        incidents.append(incident)

        self._save(incidents)

        return incident

    def get_all_incidents(self) -> list:
        # Return all stored incidents

        return self._load()

    def get_incident(self, incident_id: str):
        # Return one incident by ID

        incidents = self._load()

        for incident in incidents:
            if incident["incident_id"] == incident_id:
                return incident

        return None