import customtkinter as ctk

from ..theme import (
    SIDEBAR_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
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
        self.alert_badges = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self._build_header()
        self._build_navigation()
        self._build_status()

    def _build_header(self):
        ctk.CTkLabel(
            self,
            text="FILE INTEGRITY",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=18,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=0,
            column=0,
            padx=22,
            pady=(28, 2),
            sticky="w",
        )

        ctk.CTkLabel(
            self,
            text="MONITOR",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
                weight="bold",
            ),
            text_color=ACCENT,
        ).grid(
            row=1,
            column=0,
            padx=22,
            pady=(0, 28),
            sticky="w",
        )

    def _build_navigation(self):
        items = [
            ("Dashboard", "dashboard"),
            ("Monitoring", "monitoring"),
            ("Incidents", "incidents"),
            ("Reports", "reports"),
            ("Settings", "settings"),
        ]

        for row, (label, page_name) in enumerate(items, start=2):
            button = ctk.CTkButton(
                self,
                text=label,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#1E293B",
                text_color=TEXT_SECONDARY,
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
                padx=(14, 6),
                pady=4,
                sticky="ew",
            )

            badge = ctk.CTkLabel(
                self,
                text="●",
                text_color="#EF4444",
                font=ctk.CTkFont(size=16, weight="bold"),
                width=10,
                anchor="center",
            )

            badge.grid(
                row=row,
                column=1,
                padx=(0, 14),
                pady=4,
                sticky="e",
            )
            badge.grid_remove()

            self.buttons[page_name] = button
            self.alert_badges[page_name] = badge

    def set_alert(self, page_name, active):
        badge = self.alert_badges.get(page_name)
        if not badge:
            return

        if active:
            badge.grid()
        else:
            badge.grid_remove()

    def set_active(self, page_name):
        for name, button in self.buttons.items():
            if name == page_name:
                button.configure(
                    fg_color=ACCENT,
                    text_color=TEXT_PRIMARY,
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=TEXT_SECONDARY,
                )

    def _build_status(self):
        status = ctk.CTkFrame(
            self,
            fg_color="#111827",
            corner_radius=10,
            border_width=1,
            border_color=BORDER,
        )

        status.grid(
            row=8,
            column=0,
            padx=18,
            pady=20,
            sticky="sew",
        )

        status.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            status,
            text="●",
            text_color="#22C55E",
            font=ctk.CTkFont(size=13),
        ).grid(
            row=0,
            column=0,
            padx=(12, 6),
            pady=(10, 0),
        )

        ctk.CTkLabel(
            status,
            text="Monitoring ready",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=(10, 0),
            sticky="w",
        )

        ctk.CTkLabel(
            status,
            text="No active scan",
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
        ).grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(2, 10),
            sticky="w",
        )