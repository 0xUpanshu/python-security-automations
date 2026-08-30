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


class IntegritySection(ctk.CTkFrame):
    def __init__(self, parent, service):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.service = service
        self.results = []

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

        header = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 12),
            sticky="ew",
        )

        header.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            header,
            text="File Integrity",
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
            text="Baseline and current SHA-256 state",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=1,
            column=0,
            pady=(3, 0),
            sticky="w",
        )

        ctk.CTkButton(
            header,
            text="Refresh",
            width=85,
            height=30,
            corner_radius=7,
            fg_color=ACCENT,
            hover_color=ACCENT,
            command=self.refresh,
        ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(10, 0),
        )

        self.container = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        self.container.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="ew",
        )

        self.container.grid_columnconfigure(
            0,
            weight=1,
        )

    def refresh(self):
        try:
            self.results = (
                self.service.get_integrity_status()
            )
        except ValueError:
            self.results = []

        self._render()

    def _render(self):
        for widget in (
            self.container.winfo_children()
        ):
            widget.destroy()

        if not self.results:
            ctk.CTkLabel(
                self.container,
                text="No baseline data available.",
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=13,
                ),
                text_color=TEXT_MUTED,
            ).grid(
                row=0,
                column=0,
                pady=20,
                sticky="w",
            )

            return

        for row, result in enumerate(
            self.results
        ):
            self._create_file_row(
                result,
                row,
            )

    def _create_file_row(self, result, row):
        file_path = result["file_path"]
        status = result["status"]
        filename = Path(file_path).name

        item = ctk.CTkFrame(
            self.container,
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
            text=self._icon(status),
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=17,
                weight="bold",
            ),
            text_color=self._color(status),
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(14, 10),
            pady=12,
        )

        ctk.CTkLabel(
            item,
            text=filename,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=(10, 2),
            sticky="w",
        )

        ctk.CTkLabel(
            item,
            text=status.upper(),
            width=85,
            height=25,
            corner_radius=6,
            fg_color=self._color(status),
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=10,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=(10, 2),
        )

        ctk.CTkButton(
            item,
            text="Hash Details",
            width=105,
            height=28,
            corner_radius=7,
            fg_color="transparent",
            hover_color="#1E293B",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            command=lambda r=result: (
                self._show_hash_details(r)
            ),
        ).grid(
            row=0,
            column=3,
            rowspan=2,
            padx=(8, 14),
        )

        ctk.CTkLabel(
            item,
            text=file_path,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=10,
            ),
            text_color=TEXT_MUTED,
            anchor="w",
        ).grid(
            row=1,
            column=1,
            pady=(0, 10),
            sticky="w",
        )

    def _show_hash_details(self, result):
        window = ctk.CTkToplevel(self)

        window.title("Hash Details")
        window.geometry("720x360")
        window.configure(
            fg_color=CARD_BG
        )

        window.grab_set()

        container = ctk.CTkFrame(
            window,
            fg_color="transparent",
        )

        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25,
        )

        ctk.CTkLabel(
            container,
            text=Path(
                result["file_path"]
            ).name,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=20,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            container,
            text=result["file_path"],
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
            text_color=TEXT_MUTED,
        ).pack(
            anchor="w",
            pady=(3, 20),
        )

        self._hash_row(
            container,
            "Status",
            result["status"].upper(),
        )

        self._hash_row(
            container,
            "Baseline SHA-256",
            result["baseline_hash"] or "—",
        )

        self._hash_row(
            container,
            "Current SHA-256",
            result["current_hash"] or "—",
        )

    def _hash_row(self, parent, label, value):
        frame = ctk.CTkFrame(
            parent,
            fg_color=PANEL_BG,
            corner_radius=7,
        )

        frame.pack(
            fill="x",
            pady=4,
        )

        ctk.CTkLabel(
            frame,
            text=label,
            width=145,
            anchor="w",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
                weight="bold",
            ),
            text_color=TEXT_SECONDARY,
        ).pack(
            side="left",
            padx=(12, 8),
            pady=11,
        )

        ctk.CTkLabel(
            frame,
            text=value,
            anchor="w",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=10,
            ),
            text_color=TEXT_PRIMARY,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12),
            pady=11,
        )

    def _icon(self, status):
        return {
            "unchanged": "●",
            "modified": "●",
            "added": "+",
            "deleted": "×",
        }.get(status, "○")

    def _color(self, status):
        return {
            "unchanged": SUCCESS,
            "modified": WARNING,
            "added": ACCENT,
            "deleted": DANGER,
        }.get(status, TEXT_MUTED)