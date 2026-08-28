import customtkinter as ctk

from src.gui.theme import (
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    FONT_FAMILY,
)


class DashboardSummary(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1,
        )

        self.folder_value = self._card(
            0,
            "Monitored Folders",
            "▣",
        )

        self.file_value = self._card(
            1,
            "Tracked Files",
            "□",
        )

        self.incident_value = self._card(
            2,
            "Incidents",
            "▲",
        )

        self.report_value = self._card(
            3,
            "Reports",
            "▱",
        )

    def _card(self, column, title, icon):
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
            padx=(15, 10),
            pady=16,
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=0,
            column=1,
            pady=(13, 0),
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
            pady=(0, 13),
            sticky="w",
        )

        return value

    def update(
        self,
        folder_count,
        file_count,
        incident_count,
        report_count,
    ):
        self.folder_value.configure(
            text=str(folder_count)
        )

        self.file_value.configure(
            text=str(file_count)
        )

        self.incident_value.configure(
            text=str(incident_count)
        )

        self.report_value.configure(
            text=str(report_count)
        )