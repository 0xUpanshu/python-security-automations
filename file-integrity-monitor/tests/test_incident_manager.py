from pathlib import Path

from src.baseline import save_baseline
from src.incidents.manager import IncidentManager
from src.integrity import calculate_hash
from src.services import monitoring_service as monitoring_service_module
from src.services.monitoring_service import MonitoringService


def test_duplicate_incident_for_same_file_is_not_recreated(tmp_path):
    storage = tmp_path / "incidents.json"
    manager = IncidentManager(str(storage))

    analysis = {
        "file_path": "/tmp/invoice.pdf.exe",
        "change_type": "added",
        "suspicious": True,
        "current_hash": "abc123",
        "baseline_hash": None,
        "risk": {"score": 90, "severity": "HIGH"},
    }

    first = manager.create_incident(analysis)
    second = manager.create_incident({**analysis})

    incidents = manager.get_all_incidents()

    assert len(incidents) == 1
    assert first["incident_id"] == second["incident_id"]


def test_scan_flags_double_extension_even_when_file_is_unchanged(tmp_path):
    folder = tmp_path / "sample"
    folder.mkdir()

    file_path = folder / "invoice.pdf.exe"
    file_path.write_bytes(b"malicious payload")

    file_hash = calculate_hash(str(file_path))

    service = MonitoringService()
    service.config_path = tmp_path / "monitoring_config.json"
    service.baseline_path = tmp_path / "baseline.json"
    service.incident_path = tmp_path / "incidents.json"
    service.scan_state_path = tmp_path / "scan_state.json"

    service.get_folders = lambda: [str(folder)]
    service._scan_folders = lambda: {str(file_path): file_hash}

    save_baseline({str(file_path): file_hash}, str(service.baseline_path))

    service.scan()

    incidents = IncidentManager(str(service.incident_path)).get_all_incidents()
    assert any(
        incident.get("analysis", {}).get("file_path") == str(file_path)
        and "double_extension" in incident.get("analysis", {}).get("indicators", [])
        for incident in incidents
    )


def test_incident_creation_generates_pdf_report(tmp_path, monkeypatch):
    folder = tmp_path / "sample"
    folder.mkdir()

    file_path = folder / "invoice.pdf.exe"
    file_path.write_bytes(b"malicious payload")
    file_hash = calculate_hash(str(file_path))

    monkeypatch.setattr(monitoring_service_module, "BASE_DIR", tmp_path)

    service = MonitoringService()
    service.config_path = tmp_path / "monitoring_config.json"
    service.baseline_path = tmp_path / "baseline.json"
    service.incident_path = tmp_path / "incidents.json"
    service.scan_state_path = tmp_path / "scan_state.json"

    service.get_folders = lambda: [str(folder)]
    service._scan_folders = lambda: {str(file_path): file_hash}

    save_baseline({str(file_path): file_hash}, str(service.baseline_path))

    def fake_analyze(self, path):
        return {
            "file_path": path,
            "sha256": file_hash,
            "suspicious": True,
            "indicators": ["double_extension"],
            "entropy": 8.5,
            "high_entropy": True,
            "yara_matches": [],
            "yara_available": False,
            "virustotal": {"available": False, "known": False, "malicious": 0, "suspicious": 0, "total_engines": 0},
            "public_ips": [],
            "ip_reputation": [],
            "risk": {"score": 80, "severity": "HIGH"},
        }

    monkeypatch.setattr(
        monitoring_service_module.SecurityAnalyzer,
        "analyze",
        fake_analyze,
    )

    service.scan()

    report_dir = tmp_path / "reports"
    assert any(report_dir.glob("*.pdf"))
