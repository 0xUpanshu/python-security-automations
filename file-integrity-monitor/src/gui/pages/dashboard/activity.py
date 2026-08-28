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
    WARNING,
    DANGER,
    SUCCESS,
    FONT_FAMILY,
)


class DashboardActivity(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_incident,
    ):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.on_incident = on_incident

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self._build_sections()

    def _build_sections(self):
        self._build_status()
        self._build_incidents()
        self._build_folders()

    def _section(self, row, title):
        card = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
        )

        card.grid(
            row=row,
            column=0,
            sticky="ew",
            pady=(0, 16),
        )

        card.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=18,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 12),
            sticky="w",
        )

        return card

    def _build_status(self):
        card = self._section(
            0,
            "Security Status",
        )

        self.status = ctk.CTkLabel(
            card,
            text="Checking...",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=14,
                weight="bold",
            ),
        )

        self.status.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 18),
            sticky="w",
        )

    def _build_incidents(self):
        self.incident_card = self._section(
            1,
            "Recent Incidents",
        )

        self.incident_container = ctk.CTkFrame(
            self.incident_card,
            fg_color="transparent",
        )

        self.incident_container.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 18),
            sticky="ew",
        )

        self.incident_container.grid_columnconfigure(
            0,
            weight=1,
        )

    def _build_folders(self):
        self.folder_card = self._section(
            2,
            "Monitored Folders",
        )

        self.folder_container = ctk.CTkFrame(
            self.folder_card,
            fg_color="transparent",
        )

        self.folder_container.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 18),
            sticky="ew",
        )

        self.folder_container.grid_columnconfigure(
            0,
            weight=1,
        )

    def update_status(
        self,
        folders,
        baseline_exists,
    ):
        if not folders:
            self.status.configure(
                text="● No monitoring folder configured",
                text_color=TEXT_MUTED,
            )
        elif not baseline_exists:
            self.status.configure(
                text="● Monitoring configured — baseline required",
                text_color=WARNING,
            )
        else:
            self.status.configure(
                text="● Monitoring ready",
                text_color=SUCCESS,
            )

    def update_incidents(self, incidents):
        for widget in (
            self.incident_container
            .winfo_children()
        ):
            widget.destroy()

        recent = list(
            reversed(incidents)
        )[:5]

        if not recent:
            ctk.CTkLabel(
                self.incident_container,
                text="No security incidents detected.",
                text_color=TEXT_MUTED,
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=13,
                ),
            ).grid(
                row=0,
                column=0,
                pady=12,
                sticky="w",
            )

            return

        for row, incident in enumerate(
            recent
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

            file_path = analysis.get(
                "file_path",
                "Unknown file",
            )

            filename = Path(
                file_path
            ).name

            item = ctk.CTkFrame(
                self.incident_container,
                fg_color=PANEL_BG,
                border_width=1,
                border_color=BORDER,
                corner_radius=8,
            )

            item.grid(
                row=row,
                column=0,
                pady=4,
                sticky="ew",
            )

            item.grid_columnconfigure(
                1,
                weight=1,
            )

            ctk.CTkLabel(
                item,
                text=incident.get(
                    "incident_id",
                    "Unknown",
                ),
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=12,
                    weight="bold",
                ),
                text_color=TEXT_PRIMARY,
            ).grid(
                row=0,
                column=0,
                padx=14,
                pady=(10, 2),
                sticky="w",
            )

            ctk.CTkLabel(
                item,
                text=filename,
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=11,
                ),
                text_color=TEXT_SECONDARY,
            ).grid(
                row=1,
                column=0,
                padx=14,
                pady=(0, 10),
                sticky="w",
            )

            ctk.CTkLabel(
                item,
                text=severity,
                width=70,
                height=25,
                corner_radius=6,
                fg_color=self._severity_color(
                    severity
                ),
                text_color="#FFFFFF",
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=10,
                    weight="bold",
                ),
            ).grid(
                row=0,
                column=1,
                rowspan=2,
                padx=5,
            )

            ctk.CTkButton(
                item,
                text="View",
                width=65,
                height=28,
                corner_radius=7,
                fg_color="transparent",
                hover_color="#1E293B",
                border_width=1,
                border_color=BORDER,
                text_color=TEXT_PRIMARY,
                command=lambda i=incident: (
                    self.on_incident(i)
                ),
            ).grid(
                row=0,
                column=2,
                rowspan=2,
                padx=(8, 14),
            )

    def update_folders(self, folders):
        for widget in (
            self.folder_container
            .winfo_children()
        ):
            widget.destroy()

        if not folders:
            ctk.CTkLabel(
                self.folder_container,
                text="No folders configured.",
                text_color=TEXT_MUTED,
            ).grid(
                row=0,
                column=0,
                pady=10,
                sticky="w",
            )

            return

        for row, folder in enumerate(
            folders
        ):
            ctk.CTkLabel(
                self.folder_container,
                text=f"●  {folder}",
                text_color=TEXT_SECONDARY,
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=12,
                ),
            ).grid(
                row=row,
                column=0,
                pady=4,
                sticky="w",
            )

    def _severity_color(self, severity):
        if severity == "HIGH":
            return DANGER

        if severity == "MEDIUM":
            return WARNING

        if severity == "LOW":
            return ACCENT

        return TEXT_MUTED