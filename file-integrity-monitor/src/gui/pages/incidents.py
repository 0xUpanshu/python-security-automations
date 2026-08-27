import customtkinter as ctk

from ..theme import TEXT_PRIMARY, TEXT_SECONDARY, FONT_FAMILY


class IncidentsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
        )

        title = ctk.CTkLabel(
            self,
            text="Incidents",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=28,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        )

        title.pack(
            anchor="w",
            pady=(10, 4),
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Review detected security incidents and investigation evidence.",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=14,
            ),
            text_color=TEXT_SECONDARY,
        )

        subtitle.pack(
            anchor="w",
        )