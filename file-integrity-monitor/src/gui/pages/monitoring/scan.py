import customtkinter as ctk

from src.gui.theme import (
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT,
    ACCENT_HOVER,
    SUCCESS,
    WARNING,
    FONT_FAMILY,
)


class ScanSection(ctk.CTkFrame):
    def __init__(self, parent, service, on_change):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        self.service = service
        self.on_change = on_change

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
            text="Security Scan",
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
            pady=(18, 3),
            sticky="w",
        )

        ctk.CTkLabel(
            card,
            text=(
                "Compare the current filesystem "
                "against the trusted baseline."
            ),
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="w",
        )

        self.result = ctk.CTkLabel(
            card,
            text="No scan performed.",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_MUTED,
            anchor="w",
            justify="left",
        )

        self.result.grid(
            row=2,
            column=0,
            padx=20,
            pady=(0, 12),
            sticky="w",
        )

        ctk.CTkButton(
            card,
            text="Run Security Scan",
            width=155,
            height=34,
            corner_radius=7,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.run_scan,
        ).grid(
            row=3,
            column=0,
            padx=20,
            pady=(2, 20),
            sticky="w",
        )

    def run_scan(self):
        try:
            result = self.service.scan()

            added = len(
                result["added"]
            )

            modified = len(
                result["modified"]
            )

            deleted = len(
                result["deleted"]
            )

            incidents = len(
                result["incident_ids"]
            )

            self.result.configure(
                text=(
                    f"Added: {added}   |   "
                    f"Modified: {modified}   |   "
                    f"Deleted: {deleted}   |   "
                    f"Incidents: {incidents}"
                ),
                text_color=(
                    WARNING
                    if incidents
                    else SUCCESS
                ),
            )

            self.on_change()

        except ValueError as error:
            self._show_error(
                str(error)
            )

    def _show_error(self, message):
        from tkinter import messagebox

        messagebox.showerror(
            "Scan Error",
            message,
        )