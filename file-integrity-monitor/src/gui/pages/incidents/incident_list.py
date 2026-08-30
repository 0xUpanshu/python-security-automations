from pathlib import Path

import customtkinter as ctk

from src.gui.theme import (
    PANEL_BG,
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT,
    ACCENT_HOVER,
    WARNING,
    DANGER,
    FONT_FAMILY,
)


class IncidentList(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_select,
    ):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.on_select = on_select
        self.incidents = []

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self._build_header()

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.container.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.container.grid_columnconfigure(
            0,
            weight=1,
        )

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            pady=(0, 12),
            sticky="ew",
        )

        header.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            header,
            text="Recent Incidents",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=18,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            header,
            text="Sort by:",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=0,
            column=1,
            padx=(10, 8),
        )

        self.filter_var = ctk.StringVar(
            value="All"
        )

        self.filter_menu = ctk.CTkOptionMenu(
            header,
            variable=self.filter_var,
            values=[
                "All",
                "High",
                "Medium",
                "Low",
                "Newest",
                "Oldest",
            ],
            width=125,
            height=32,
            corner_radius=7,
            fg_color=PANEL_BG,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color=PANEL_BG,
            dropdown_hover_color="#1E293B",
            command=self._filter,
        )

        self.filter_menu.grid(
            row=0,
            column=2,
        )

    def set_incidents(self, incidents):
        self.incidents = list(incidents)
        self._filter(
            self.filter_var.get()
        )

    def _filter(self, value):
        if value in (
            "High",
            "Medium",
            "Low",
        ):
            incidents = [
                incident
                for incident in self.incidents
                if incident
                .get("analysis", {})
                .get("risk", {})
                .get("severity", "")
                .upper()
                == value.upper()
            ]

        elif value == "Newest":
            incidents = sorted(
                self.incidents,
                key=lambda item: item.get(
                    "created_at",
                    "",
                ),
                reverse=True,
            )

        elif value == "Oldest":
            incidents = sorted(
                self.incidents,
                key=lambda item: item.get(
                    "created_at",
                    "",
                ),
            )

        else:
            incidents = list(
                reversed(self.incidents)
            )

        self._render(incidents)

    def _render(self, incidents):
        for widget in self.container.winfo_children():
            widget.destroy()

        if not incidents:
            empty = ctk.CTkFrame(
                self.container,
                fg_color=PANEL_BG,
                corner_radius=8,
            )

            empty.grid(
                row=0,
                column=0,
                sticky="ew",
            )

            ctk.CTkLabel(
                empty,
                text="No incidents found.",
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=13,
                ),
                text_color=TEXT_MUTED,
            ).pack(
                padx=20,
                pady=35,
            )

            return

        for row, incident in enumerate(
            incidents
        ):
            self._create_row(
                incident,
                row,
            )

    def _create_row(
        self,
        incident,
        row,
    ):
        analysis = incident.get(
            "analysis",
            {},
        )

        risk = analysis.get(
            "risk",
            {},
        )

        severity = risk.get(
            "severity",
            "UNKNOWN",
        ).upper()

        score = risk.get(
            "score",
            0,
        )

        file_path = analysis.get(
            "file_path",
            "Unknown file",
        )

        change_type = analysis.get(
            "change_type",
            "unknown",
        )

        filename = Path(
            file_path
        ).name

        item = ctk.CTkFrame(
            self.container,
            fg_color=PANEL_BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=9,
        )

        item.grid(
            row=row,
            column=0,
            pady=5,
            sticky="ew",
        )

        item.grid_columnconfigure(
            1,
            weight=1,
        )

        ctk.CTkLabel(
            item,
            text=self._icon(severity),
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=18,
                weight="bold",
            ),
            text_color=self._color(severity),
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(15, 10),
            pady=14,
        )

        ctk.CTkLabel(
            item,
            text=incident.get(
                "incident_id",
                "Unknown",
            ),
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=13,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=(12, 2),
            sticky="w",
        )

        ctk.CTkLabel(
            item,
            text=filename,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 12),
            sticky="w",
        )

        ctk.CTkLabel(
            item,
            text=severity,
            width=75,
            height=27,
            corner_radius=6,
            fg_color=self._color(severity),
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=(12, 2),
        )

        ctk.CTkLabel(
            item,
            text=(
                f"{change_type.title()}  •  "
                f"Score {score}"
            ),
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
            text_color=TEXT_MUTED,
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=(0, 12),
        )

        ctk.CTkButton(
            item,
            text="View",
            width=70,
            height=30,
            corner_radius=7,
            fg_color="transparent",
            hover_color="#1E293B",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            command=lambda i=incident: (
                self.on_select(i)
            ),
        ).grid(
            row=0,
            column=3,
            rowspan=2,
            padx=(8, 15),
        )

    def _icon(self, severity):
        if severity == "HIGH":
            return "▲"

        if severity == "MEDIUM":
            return "●"

        if severity == "LOW":
            return "◆"

        return "○"

    def _color(self, severity):
        if severity == "HIGH":
            return DANGER

        if severity == "MEDIUM":
            return WARNING

        if severity == "LOW":
            return ACCENT

        return TEXT_MUTED