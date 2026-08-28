import customtkinter as ctk

from ...theme import (
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    FONT_FAMILY,
)


class IncidentSummary(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.grid_columnconfigure(
            (0, 1, 2),
            weight=1,
        )

        self.total_value = self._create_card(
            0,
            "Total Incidents",
            "◈",
        )

        self.high_value = self._create_card(
            1,
            "High",
            "▲",
        )

        self.medium_value = self._create_card(
            2,
            "Medium",
            "●",
        )

    def _create_card(
        self,
        column,
        title,
        icon,
    ):
        card = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="ew",
        )

        card.grid_columnconfigure(
            1,
            weight=1,
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=20,
                weight="bold",
            ),
            text_color=ACCENT,
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(16, 10),
            pady=16,
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=0,
            column=1,
            pady=(14, 0),
            sticky="w",
        )

        value = ctk.CTkLabel(
            card,
            text="0",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=22,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        )

        value.grid(
            row=1,
            column=1,
            pady=(0, 14),
            sticky="w",
        )

        return value

    def update(self, incidents):
        high = 0
        medium = 0

        for incident in incidents:
            severity = (
                incident
                .get("analysis", {})
                .get("risk", {})
                .get("severity", "")
                .upper()
            )

            if severity == "HIGH":
                high += 1
            elif severity == "MEDIUM":
                medium += 1

        self.total_value.configure(
            text=str(len(incidents))
        )

        self.high_value.configure(
            text=str(high)
        )

        self.medium_value.configure(
            text=str(medium)
        )