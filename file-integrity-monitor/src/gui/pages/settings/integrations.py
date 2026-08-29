import customtkinter as ctk

from src.gui.theme import (
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    SUCCESS,
    FONT_FAMILY,
)


class IntegrationSettings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

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
            1,
            weight=1,
        )

        ctk.CTkLabel(
            card,
            text="Integrations",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=18,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(18, 4),
            sticky="w",
        )

        ctk.CTkLabel(
            card,
            text="External services used by the monitoring pipeline.",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=20,
            pady=(0, 16),
            sticky="w",
        )

        self._integration(
            card,
            2,
            "YARA",
            "Detection rules",
        )

        self._integration(
            card,
            3,
            "VirusTotal",
            "File reputation lookup",
        )

        self._integration(
            card,
            4,
            "GitHub",
            "Sample file import",
        )

    def _integration(
        self,
        parent,
        row,
        name,
        description,
    ):
        ctk.CTkLabel(
            parent,
            text=name,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=13,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=row,
            column=0,
            padx=20,
            pady=8,
            sticky="w",
        )

        ctk.CTkLabel(
            parent,
            text=description,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
            text_color=TEXT_MUTED,
        ).grid(
            row=row,
            column=1,
            padx=20,
            pady=8,
            sticky="e",
        )

        ctk.CTkLabel(
            parent,
            text="Available",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
                weight="bold",
            ),
            text_color=SUCCESS,
        ).grid(
            row=row,
            column=2,
            padx=(0, 20),
            pady=8,
        )