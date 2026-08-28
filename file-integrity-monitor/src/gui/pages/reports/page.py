from pathlib import Path

import customtkinter as ctk

from src.gui.theme import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_FAMILY,
)

from .summary import ReportSummary
from .report_list import ReportList


BASE_DIR = Path(__file__).resolve().parents[4]
REPORTS_DIR = BASE_DIR / "reports"


class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
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
            text="Reports",
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
                "Review and open generated security reports."
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

        self.summary = ReportSummary(
            content
        )

        self.summary.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        self.report_list = ReportList(
            content
        )

        self.report_list.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.refresh()

    def refresh(self):
        REPORTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        reports = [
            path
            for path in REPORTS_DIR.iterdir()
            if path.is_file()
            and path.suffix.lower() in (
                ".pdf",
                ".txt",
            )
        ]

        self.summary.update(
            reports
        )

        self.report_list.set_reports(
            reports
        )