import customtkinter as ctk

from ..theme import (
    SIDEBAR_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT,
    ACCENT_SOFT,
    FONT_FAMILY,
)

class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, on_navigate):
        super().__init__(
            parent,
            fg_color=SIDEBAR_BG,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
            width=220,
        )

        self.on_navigate = on_navigate
        self.buttons = {}

        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_navigation()
        self._build_status()

    def _build_header(self):
        title = ctk.CTkLabel(
            self,
            text="FILE INTEGRITY",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=18,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        )

        title.grid(
            row=0,
            column=0,
            padx=22,
            pady=(28, 2),
            sticky="w",
        )

        subtitle = ctk.CTkLabel(
            self,
            text="MONITOR",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
                weight="bold",
            ),
            text_color=ACCENT,
        )

        subtitle.grid(
            row=1,
            column=0,
            padx=22,
            pady=(0, 28),
            sticky="w",
        )

    def _build_navigation(self):
        buttons = [
            ("Dashboard", "dashboard"),
            ("Monitoring", "monitoring"),
            ("Incidents", "incidents"),
            ("Reports", "reports"),
            ("Settings", "settings"),
        ]

        for row, (label, page_name) in enumerate(buttons, start=2):

            button = ctk.CTkButton(
                self,
                text=label,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                hover_color=ACCENT_SOFT,
                text_color=TEXT_SECONDARY,
                border_spacing=14,
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=14,
                    weight="bold",
                ),
                command=lambda name=page_name: self.on_navigate(name),
            )

            button.grid(
                row=row,
                column=0,
                padx=14,
                pady=4,
                sticky="ew",
            )

            setattr(
                self,
                f"{page_name}_button",
                button,
            )
            self.buttons[page_name] = button

        self.set_active("dashboard")

    def set_active(self, page_name):
        for name, button in self.buttons.items():
            is_active = name == page_name
            button.configure(
                fg_color=ACCENT_SOFT if is_active else "transparent",
                text_color=TEXT_PRIMARY if is_active else TEXT_SECONDARY,
            )

    def _build_status(self):
        status_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        status_frame.grid(
            row=8,
            column=0,
            padx=18,
            pady=(30, 20),
            sticky="ew",
        )

        indicator = ctk.CTkLabel(
            status_frame,
            text="●",
            text_color=ACCENT,
            font=ctk.CTkFont(size=13),
        )

        indicator.grid(
            row=0,
            column=0,
            padx=(0, 7),
        )

        label = ctk.CTkLabel(
            status_frame,
            text="Monitoring ready",
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
        )

        label.grid(
            row=0,
            column=1,
            sticky="w",
        )