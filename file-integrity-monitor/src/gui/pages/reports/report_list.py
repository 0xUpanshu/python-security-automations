import os
from pathlib import Path
from datetime import datetime

import customtkinter as ctk
from tkinter import messagebox

from src.gui.theme import (
    PANEL_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT,
    ACCENT_HOVER,
    FONT_FAMILY,
)


class ReportList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.reports = []

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
            text="Generated Reports",
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

        self.sort_var = ctk.StringVar(
            value="Newest"
        )

        ctk.CTkOptionMenu(
            header,
            variable=self.sort_var,
            values=[
                "Newest",
                "Oldest",
                "Name",
            ],
            width=120,
            height=32,
            corner_radius=7,
            fg_color=PANEL_BG,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color=PANEL_BG,
            dropdown_hover_color="#1E293B",
            command=self._sort,
        ).grid(
            row=0,
            column=1,
        )

    def set_reports(self, reports):
        self.reports = list(reports)
        self._sort(
            self.sort_var.get()
        )

    def _sort(self, value):
        if value == "Oldest":
            reports = sorted(
                self.reports,
                key=lambda p: p.stat().st_mtime,
            )

        elif value == "Name":
            reports = sorted(
                self.reports,
                key=lambda p: p.name.lower(),
            )

        else:
            reports = sorted(
                self.reports,
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )

        self._render(reports)

    def _render(self, reports):
        for widget in self.container.winfo_children():
            widget.destroy()

        if not reports:
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
                text="No reports generated yet.",
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

        for row, report in enumerate(reports):
            self._create_row(
                report,
                row,
            )

    def _create_row(self, report, row):
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
            text="▱",
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
            pady=14,
        )

        ctk.CTkLabel(
            item,
            text=report.name,
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

        timestamp = datetime.fromtimestamp(
            report.stat().st_mtime
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        ctk.CTkLabel(
            item,
            text=f"Generated {timestamp}",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
            text_color=TEXT_MUTED,
        ).grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 12),
            sticky="w",
        )

        ctk.CTkLabel(
            item,
            text=report.suffix.upper().replace(
                ".",
                "",
            ),
            width=55,
            height=26,
            corner_radius=6,
            fg_color=ACCENT,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=10,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=5,
        )

        ctk.CTkButton(
            item,
            text="Open",
            width=75,
            height=30,
            corner_radius=7,
            fg_color="transparent",
            hover_color="#1E293B",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            command=lambda p=report: self._open(p),
        ).grid(
            row=0,
            column=3,
            rowspan=2,
            padx=(8, 15),
        )

    def _open(self, report):
        try:
            os.startfile(str(report))
        except OSError as error:
            ctk.CTkMessagebox(
                title="Unable to Open Report",
                message=str(error),
            )