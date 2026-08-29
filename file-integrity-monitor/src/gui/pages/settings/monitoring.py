import customtkinter as ctk

from src.services.monitoring_service import MonitoringService
from src.gui.theme import (
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT,
    ACCENT_HOVER,
    WARNING,
    SUCCESS,
    FONT_FAMILY,
)


class MonitoringSettings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.service = MonitoringService()

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self._build()

    def _build(self):
        card = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
        )

        card.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        card.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            card,
            text="Monitoring",
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
            pady=(18, 4),
            sticky="w",
        )

        ctk.CTkLabel(
            card,
            text="Current monitoring configuration.",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 16),
            sticky="w",
        )

        self.folder_value = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_PRIMARY,
            anchor="w",
        )

        self.folder_value.grid(
            row=2,
            column=0,
            padx=20,
            pady=6,
            sticky="w",
        )

        self.baseline_value = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_PRIMARY,
            anchor="w",
        )

        self.baseline_value.grid(
            row=3,
            column=0,
            padx=20,
            pady=6,
            sticky="w",
        )

        ctk.CTkButton(
            card,
            text="Refresh",
            width=100,
            height=32,
            corner_radius=7,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.refresh,
        ).grid(
            row=2,
            column=1,
            rowspan=2,
            padx=(10, 20),
        )

        self.refresh()

    def refresh(self):
        folders = self.service.get_folders()

        if folders:
            self.folder_value.configure(
                text=(
                    f"Monitored folders: "
                    f"{len(folders)}"
                ),
                text_color=SUCCESS,
            )
        else:
            self.folder_value.configure(
                text="Monitored folders: None",
                text_color=WARNING,
            )

        if self.service.baseline_exists():
            self.baseline_value.configure(
                text="Baseline: Available",
                text_color=SUCCESS,
            )
        else:
            self.baseline_value.configure(
                text="Baseline: Not created",
                text_color=WARNING,
            )