from src.incidents.manager import IncidentManager


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
