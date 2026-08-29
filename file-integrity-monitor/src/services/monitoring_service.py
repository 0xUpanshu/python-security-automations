import json
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import Request, urlopen

from ..alerting.alert_manager import AlertManager
from ..baseline import load_baseline, save_baseline
from ..detection.analyzer import SecurityAnalyzer
from ..incidents.manager import IncidentManager
from ..scanner import scan_directory


BASE_DIR = Path(__file__).resolve().parents[2]


class MonitoringService:
    def __init__(self):
        self.config_path = (
            BASE_DIR / "data" / "monitoring_config.json"
        )
        self.baseline_path = (
            BASE_DIR / "data" / "baseline.json"
        )
        self.incident_path = (
            BASE_DIR / "data" / "incidents.json"
        )
        self.import_dir = (
            BASE_DIR / "data" / "github_imports"
        )

        self.config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.import_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.config_path.exists():
            self._save_config({
                "monitored_folders": []
            })

    def _read_config(self):
        try:
            with open(
                self.config_path,
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return {
                "monitored_folders": []
            }

    def _save_config(self, config):
        with open(
            self.config_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                config,
                file,
                indent=4,
            )

    def get_folders(self):
        return self._read_config().get(
            "monitored_folders",
            [],
        )

    def add_folder(self, folder_path):
        folder = Path(
            folder_path
        ).resolve()

        if not folder.is_dir():
            raise ValueError(
                f"Invalid folder: {folder_path}"
            )

        folders = self.get_folders()
        folder = str(folder)

        if folder in folders:
            return False

        folders.append(folder)

        self._save_config({
            "monitored_folders": folders
        })

        return True

    def remove_folder(self, folder_path):
        folder = str(
            Path(folder_path).resolve()
        )

        folders = self.get_folders()

        if folder not in folders:
            return False

        folders.remove(folder)

        self._save_config({
            "monitored_folders": folders
        })

        return True

    def import_github_file(self, url):
        parsed = urlparse(url)

        if parsed.scheme not in {
            "http",
            "https",
        }:
            raise ValueError(
                "Invalid URL."
            )

        hostname = parsed.netloc.lower()

        if hostname in {
            "github.com",
            "www.github.com",
        }:
            parts = parsed.path.strip(
                "/"
            ).split("/")

            if (
                len(parts) < 5
                or parts[2] != "blob"
            ):
                raise ValueError(
                    "Please drop a GitHub file link."
                )

            owner = parts[0]
            repo = parts[1]
            branch = parts[3]
            file_path = "/".join(
                parts[4:]
            )

            raw_url = (
                "https://raw.githubusercontent.com/"
                f"{owner}/{repo}/{branch}/{file_path}"
            )

        elif hostname == "raw.githubusercontent.com":
            parts = parsed.path.strip(
                "/"
            ).split("/")

            if len(parts) < 4:
                raise ValueError(
                    "Invalid GitHub raw file URL."
                )

            file_path = "/".join(
                parts[3:]
            )

            raw_url = url

        else:
            raise ValueError(
                "Only GitHub URLs are supported."
            )

        filename = Path(
            unquote(file_path)
        ).name

        if not filename:
            raise ValueError(
                "Could not determine the file name."
            )

        destination = (
            self.import_dir / filename
        )

        request = Request(
            raw_url,
            headers={
                "User-Agent":
                    "File-Integrity-Monitor"
            },
        )

        try:
            with urlopen(
                request,
                timeout=15,
            ) as response:
                data = response.read()

        except Exception as error:
            raise ValueError(
                "Could not download GitHub file: "
                f"{error}"
            )

        if not data:
            raise ValueError(
                "The GitHub file is empty."
            )

        destination.write_bytes(data)

        self.add_folder(
            str(self.import_dir)
        )

        return str(destination)

    def _scan_folders(self):
        folders = self.get_folders()

        if not folders:
            raise ValueError(
                "No monitored folders configured."
            )

        hashes = {}

        for folder in folders:
            hashes.update(
                scan_directory(folder)
            )

        return hashes

    def create_baseline(self):
        current_hashes = (
            self._scan_folders()
        )

        save_baseline(
            current_hashes,
            str(self.baseline_path),
        )

        return {
            "folder_count": len(
                self.get_folders()
            ),
            "file_count": len(
                current_hashes
            ),
        }

    def baseline_exists(self):
        return self.baseline_path.exists()

    def get_integrity_status(self):
        folders = self.get_folders()

        if not folders:
            return []

        if not self.baseline_exists():
            return []

        baseline = load_baseline(
            str(self.baseline_path)
        )

        try:
            current = self._scan_folders()
        except ValueError:
            return []

        results = []

        all_files = (
            set(baseline)
            | set(current)
        )

        for file_path in sorted(all_files):
            in_baseline = (
                file_path in baseline
            )

            in_current = (
                file_path in current
            )

            if in_baseline and in_current:
                baseline_hash = (
                    baseline[file_path]
                )

                current_hash = (
                    current[file_path]
                )

                if (
                    baseline_hash
                    == current_hash
                ):
                    status = "unchanged"
                else:
                    status = "modified"

                results.append({
                    "file_path": file_path,
                    "status": status,
                    "baseline_hash": baseline_hash,
                    "current_hash": current_hash,
                })

            elif in_current:
                results.append({
                    "file_path": file_path,
                    "status": "added",
                    "baseline_hash": None,
                    "current_hash": current[file_path],
                })

            else:
                results.append({
                    "file_path": file_path,
                    "status": "deleted",
                    "baseline_hash": baseline[file_path],
                    "current_hash": None,
                })

        return results

    def scan(self):
        if not self.baseline_exists():
            raise ValueError(
                "Create a baseline before scanning."
            )

        baseline = load_baseline(
            str(self.baseline_path)
        )

        current = self._scan_folders()

        added = [
            path
            for path in current
            if path not in baseline
        ]

        modified = [
            path
            for path in current
            if (
                path in baseline
                and baseline[path] != current[path]
            )
        ]

        deleted = [
            path
            for path in baseline
            if path not in current
        ]

        analyzer = SecurityAnalyzer()

        incidents = IncidentManager(
            str(self.incident_path)
        )

        alerts = AlertManager()

        security_results = []
        incident_ids = []

        for path in added + modified:
            try:
                result = analyzer.analyze(
                    path
                )

                result["change_type"] = (
                    "added"
                    if path in added
                    else "modified"
                )

                security_results.append(
                    result
                )

                if result["suspicious"]:
                    incident = (
                        incidents.create_incident(
                            result
                        )
                    )

                    incident_ids.append(
                        incident["incident_id"]
                    )

                    alerts.alert(result)

            except Exception as error:
                security_results.append({
                    "file_path": path,
                    "change_type": (
                        "added"
                        if path in added
                        else "modified"
                    ),
                    "suspicious": False,
                    "indicators": [],
                    "error": str(error),
                })

        for path in deleted:
            result = {
                "file_path": path,
                "change_type": "deleted",
                "suspicious": True,
                "indicators": [
                    "file_deleted"
                ],
                "risk": {
                    "score": 50,
                    "severity": "HIGH",
                },
            }

            incident = (
                incidents.create_incident(
                    result
                )
            )

            incident_ids.append(
                incident["incident_id"]
            )

            alerts.alert(result)

            security_results.append(
                result
            )

        return {
            "added": added,
            "modified": modified,
            "deleted": deleted,
            "security_results": security_results,
            "incident_ids": incident_ids,
        }