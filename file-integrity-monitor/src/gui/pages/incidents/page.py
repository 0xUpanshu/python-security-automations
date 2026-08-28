from pathlib import Path

import customtkinter as ctk

from src.incidents.manager import IncidentManager
from src.gui.theme import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_FAMILY,
)

from .summary import IncidentSummary
from .incident_list import IncidentList
from .incident_detail import IncidentDetail


BASE_DIR = Path(__file__).resolve().parents[4]


class IncidentsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.manager = IncidentManager(
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
            text="Incidents",
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
                "Detected security events "
                "requiring investigation."
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

        self.summary = IncidentSummary(
            content
        )

        self.summary.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        self.incident_list = IncidentList(
            content,
            self._show_detail,
        )

        self.incident_list.grid(
            row=1,
            column=0,
            sticky="ew",
        )

    def refresh(self):
        incidents = (
            self.manager.get_all_incidents()
        )

        self.summary.update(
            incidents
        )

        self.incident_list.set_incidents(
            incidents
        )

    def _show_detail(self, incident):
        IncidentDetail(
            self,
            incident,
            BASE_DIR / "reports",
        )