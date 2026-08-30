import customtkinter as ctk

from src.gui.theme import (
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    FONT_FAMILY,
)


class ReportSummary(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.grid_columnconfigure(
            (0, 1),
            weight=1,
        )

        self.total_value = self._create_card(
            0,
            "Total Reports",
            "▤",
        )

        self.pdf_value = self._create_card(
            1,
            "PDF Reports",
            "▱",
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

    def update(self, reports):
        self.total_value.configure(
            text=str(len(reports))
        )

        pdf_count = sum(
            1
            for report in reports
            if report.suffix.lower() == ".pdf"
        )

        self.pdf_value.configure(
            text=str(pdf_count)
        )