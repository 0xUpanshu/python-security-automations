import customtkinter as ctk

from src.services.monitoring_service import (
    MonitoringService,
)

from src.gui.theme import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_FAMILY,
)

from .monitoring import MonitoringSettings
from .integrations import IntegrationSettings


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.service = MonitoringService()

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
            text="Settings",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=28,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=(
                "Configure monitoring, detection "
                "and external integrations."
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

        self.monitoring = MonitoringSettings(
            content
        )

        self.monitoring.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        self.integrations = IntegrationSettings(
            content
        )

        self.integrations.grid(
            row=1,
            column=0,
            sticky="ew",
        )