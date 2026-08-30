import json
from pathlib import Path

import customtkinter as ctk

from src.incidents.manager import IncidentManager
from src.services.monitoring_service import MonitoringService

from src.gui.theme import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_FAMILY,
)

from src.gui.pages.incidents.incident_detail import (
    IncidentDetail,
)

from .summary import DashboardSummary
from .activity import DashboardActivity
from .intigrity import IntegritySection


BASE_DIR = Path(__file__).resolve().parents[4]


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.service = MonitoringService()

        self.incident_manager = IncidentManager(
            str(
                BASE_DIR
                / "data"
                / "incidents.json"
            )
        )

        self.grid_rowconfigure(
            1,
            weight=1,
        )

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self._build_header()
        self._build_content()
        self.refresh()

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            padx=30,
            pady=(28, 10),
            sticky="ew",
        )

        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=28,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=(
                "Overview of your file integrity "
                "monitoring environment."
            ),
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=14,
            ),
            text_color=TEXT_SECONDARY,
        ).pack(
            anchor="w",
            pady=(4, 0),
        )

    def _build_content(self):
        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
        )

        content.grid(
            row=1,
            column=0,
            padx=30,
            pady=(0, 20),
            sticky="nsew",
        )

        content.grid_columnconfigure(
            0,
            weight=1,
        )

        self.summary = DashboardSummary(
            content
        )

        self.summary.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        self.activity = DashboardActivity(
            content,
            self._open_incident,
        )

        self.activity.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        self.integrity = IntegritySection(
            content,
            self.service,
        )

        self.integrity.grid(
            row=2,
            column=0,
            sticky="ew",
        )

    def refresh(self):
        folders = self._get_folders()

        file_count = self._get_file_count()

        incidents = (
            self.incident_manager
            .get_all_incidents()
        )

        reports = self._get_reports()

        self.summary.update(
            folder_count=len(folders),
            file_count=file_count,
            incident_count=len(incidents),
            report_count=len(reports),
        )

        self.activity.update_status(
            folders,
            self._baseline_exists(),
        )

        self.activity.update_incidents(
            incidents
        )

        self.activity.update_folders(
            folders
        )

        self.integrity.refresh()

    def _get_folders(self):
        path = (
            BASE_DIR
            / "data"
            / "monitoring_config.json"
        )

        try:
            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:
                config = json.load(file)

            return config.get(
                "monitored_folders",
                [],
            )

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return []

    def _get_file_count(self):
        path = (
            BASE_DIR
            / "data"
            / "baseline.json"
        )

        if not path.exists():
            return 0

        try:
            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:
                baseline = json.load(file)

            return len(baseline)

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return 0

    def _baseline_exists(self):
        return (
            BASE_DIR
            / "data"
            / "baseline.json"
        ).exists()

    def _get_reports(self):
        reports_dir = (
            BASE_DIR / "reports"
        )

        if not reports_dir.exists():
            return []

        return [
            path
            for path in reports_dir.iterdir()
            if path.is_file()
            and path.suffix.lower()
            in {".pdf", ".txt"}
        ]

    def _open_incident(self, incident):
        IncidentDetail(
            self,
            incident,
            BASE_DIR / "reports",
        )