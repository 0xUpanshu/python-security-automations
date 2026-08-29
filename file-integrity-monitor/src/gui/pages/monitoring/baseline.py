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


class BaselineSection(ctk.CTkFrame):
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
        self.refresh()

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
            text="Baseline",
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
                "Create a trusted SHA-256 snapshot "
                "of the monitored files."
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

        self.status = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=13,
                weight="bold",
            ),
        )

        self.status.grid(
            row=2,
            column=0,
            padx=20,
            pady=5,
            sticky="w",
        )

        self.details = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
            text_color=TEXT_MUTED,
        )

        self.details.grid(
            row=3,
            column=0,
            padx=20,
            pady=(0, 12),
            sticky="w",
        )

        self.create_button = ctk.CTkButton(
            card,
            text="Create Baseline",
            width=140,
            height=34,
            corner_radius=7,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.create_baseline,
        )

        self.create_button.grid(
            row=4,
            column=0,
            padx=20,
            pady=(2, 20),
            sticky="w",
        )

    def create_baseline(self):
        try:
            result = (
                self.service.create_baseline()
            )

            self.status.configure(
                text="● Baseline Available",
                text_color=SUCCESS,
            )

            self.details.configure(
                text=(
                    f"Folders: "
                    f"{result['folder_count']}  |  "
                    f"Files tracked: "
                    f"{result['file_count']}"
                )
            )

            self.create_button.configure(
                state="disabled"
            )

            self.on_change()

        except ValueError as error:
            self._show_error(
                str(error)
            )

    def refresh(self):
        if not self.service.baseline_exists():
            self.status.configure(
                text="● Baseline Not Created",
                text_color=WARNING,
            )

            self.details.configure(
                text="Create a baseline before scanning."
            )

            self.create_button.configure(
                state="normal"
            )

            return

        try:
            count = len(
                self.service.get_integrity_status()
            )
        except ValueError:
            count = 0

        self.status.configure(
            text="● Baseline Available",
            text_color=SUCCESS,
        )

        self.details.configure(
            text=(
                f"Files tracked: {count}"
            )
        )

        self.create_button.configure(
            state="disabled"
        )

    def _show_error(self, message):
        from tkinter import messagebox

        messagebox.showerror(
            "Baseline Error",
            message,
        )