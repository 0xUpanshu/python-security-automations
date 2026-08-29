import customtkinter as ctk

from src.gui.theme import (
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT,
    ACCENT_HOVER,
    DANGER,
    FONT_FAMILY,
)


class FolderSection(ctk.CTkFrame):
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
            text="Monitored Folders",
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
                "Folders whose files will be "
                "tracked for integrity changes."
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

        self.list_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )

        self.list_frame.grid(
            row=2,
            column=0,
            padx=20,
            pady=(0, 10),
            sticky="ew",
        )

        self.list_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.add_button = ctk.CTkButton(
            card,
            text="Add Folder",
            width=120,
            height=34,
            corner_radius=7,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.add_folder,
        )

        self.add_button.grid(
            row=3,
            column=0,
            padx=20,
            pady=(4, 20),
            sticky="w",
        )

        self.refresh()

    def add_folder(self):
        from tkinter import filedialog

        folder = filedialog.askdirectory(
            title="Select folder to monitor"
        )

        if not folder:
            return

        try:
            added = self.service.add_folder(
                folder
            )

            if added:
                self.refresh()
                self.on_change()

        except ValueError as error:
            self._show_error(
                str(error)
            )

    def remove_folder(self, folder):
        if self.service.remove_folder(
            folder
        ):
            self.refresh()
            self.on_change()

    def refresh(self):
        for widget in (
            self.list_frame.winfo_children()
        ):
            widget.destroy()

        folders = self.service.get_folders()

        if not folders:
            ctk.CTkLabel(
                self.list_frame,
                text="No folders are currently monitored.",
                font=ctk.CTkFont(
                    family=FONT_FAMILY,
                    size=12,
                ),
                text_color=TEXT_MUTED,
            ).grid(
                row=0,
                column=0,
                pady=10,
                sticky="w",
            )
            return

        for row, folder in enumerate(
            folders
        ):
            self._folder_row(
                folder,
                row,
            )

    def _folder_row(self, folder, row):
        item = ctk.CTkFrame(
            self.list_frame,
            fg_color="#111B27",
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
            0,
            weight=1,
        )

        ctk.CTkLabel(
            item,
            text=folder,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=11,
            ),
            text_color=TEXT_PRIMARY,
            anchor="w",
        ).grid(
            row=0,
            column=0,
            padx=14,
            pady=11,
            sticky="ew",
        )

        ctk.CTkButton(
            item,
            text="Remove",
            width=75,
            height=28,
            corner_radius=6,
            fg_color="transparent",
            hover_color=DANGER,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            command=lambda: self.remove_folder(
                folder
            ),
        ).grid(
            row=0,
            column=1,
            padx=(5, 12),
        )

    def _show_error(self, message):
        from tkinter import messagebox

        messagebox.showerror(
            "Folder Error",
            message,
        )