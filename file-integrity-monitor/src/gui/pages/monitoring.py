from pathlib import Path
import threading

import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES

from ...services.monitoring_service import MonitoringService
from ..theme import (
    PANEL_BG,
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


class MonitoringPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.service = MonitoringService()
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_content()
        self._refresh_view()

    def _build_header(self):
        ctk.CTkLabel(
            self,
            text="Monitoring",
            font=ctk.CTkFont(FONT_FAMILY, 28, "bold"),
            text_color=TEXT_PRIMARY,
        ).grid(
            row=0,
            column=0,
            padx=30,
            pady=(25, 3),
            sticky="w",
        )

        ctk.CTkLabel(
            self,
            text="Configure folders, baselines and security scanning.",
            font=ctk.CTkFont(FONT_FAMILY, 14),
            text_color=TEXT_SECONDARY,
        ).grid(
            row=1,
            column=0,
            padx=30,
            pady=(0, 8),
            sticky="w",
        )

    def _build_content(self):
        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
        )
        content.grid(
            row=2,
            column=0,
            padx=30,
            pady=(8, 20),
            sticky="nsew",
        )
        content.grid_columnconfigure(0, weight=1)

        self._build_demo_card(content)
        self._build_folder_card(content)
        self._build_baseline_card(content)
        self._build_scan_card(content)

    def _card(self, parent, row):
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
        )
        card.grid(
            row=row,
            column=0,
            sticky="ew",
            pady=(0, 16),
        )
        card.grid_columnconfigure(0, weight=1)
        return card

    def _build_demo_card(self, parent):
        card = self._card(parent, 0)

        ctk.CTkLabel(
            card,
            text="Quick Start Demo",
            font=ctk.CTkFont(FONT_FAMILY, 18, "bold"),
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=20, pady=(18, 4), sticky="w")

        ctk.CTkLabel(
            card,
            text=(
                "Choose a folder to monitor.\n"
                "Manual folder selection is used in this portfolio project "
                "to keep the monitoring scope explicit and user-controlled. "
                "Enterprise deployments may configure protected paths "
                "automatically through centralized policies."
            ),
            justify="left",
            wraplength=800,
            font=ctk.CTkFont(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY,
        ).grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        ctk.CTkLabel(
            card,
            text=(
                "For a quick demo, you can use the `sample_files` folder "
                "included in this GitHub repository. It contains safe test "
                "files for demonstrating file changes and security detections."
            ),
            justify="left",
            wraplength=800,
            font=ctk.CTkFont(FONT_FAMILY, 12),
            text_color=TEXT_MUTED,
        ).grid(row=2, column=0, padx=20, pady=(0, 15), sticky="w")

        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="w")

        ctk.CTkButton(
            buttons,
            text="Use Sample Files",
            width=145,
            height=38,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self._use_sample_files,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            buttons,
            text="+ Add Folder",
            width=125,
            height=38,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1E293B",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            command=self._add_folder,
        ).pack(side="left")

        self.drop_area = ctk.CTkFrame(
            card,
            height=85,
            fg_color=PANEL_BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
        )
        self.drop_area.grid(
            row=4,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="ew",
        )

        ctk.CTkLabel(
            self.drop_area,
            text="Drag & drop a folder here",
            font=ctk.CTkFont(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.5, rely=0.5, anchor="center")

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self._handle_drop)

    def _build_folder_card(self, parent):
        card = self._card(parent, 1)

        ctk.CTkLabel(
            card,
            text="Monitored Folders",
            font=ctk.CTkFont(FONT_FAMILY, 18, "bold"),
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=20, pady=(18, 10), sticky="w")

        self.folder_container = ctk.CTkScrollableFrame(
            card,
            height=160,
            fg_color=PANEL_BG,
            corner_radius=8,
        )
        self.folder_container.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="ew",
        )
        self.folder_container.grid_columnconfigure(0, weight=1)

    def _build_baseline_card(self, parent):
        card = self._card(parent, 2)

        ctk.CTkLabel(
            card,
            text="Baseline",
            font=ctk.CTkFont(FONT_FAMILY, 18, "bold"),
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=20, pady=(18, 3), sticky="w")

        ctk.CTkLabel(
            card,
            text="Create a trusted SHA-256 snapshot of monitored folders.",
            font=ctk.CTkFont(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY,
        ).grid(row=1, column=0, padx=20, pady=(0, 12), sticky="w")

        self.baseline_status = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(FONT_FAMILY, 14, "bold"),
        )
        self.baseline_status.grid(row=2, column=0, padx=20, sticky="w")

        self.file_count = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY,
        )
        self.file_count.grid(row=3, column=0, padx=20, pady=(4, 12), sticky="w")

        self.baseline_button = ctk.CTkButton(
            card,
            text="Create Baseline",
            width=160,
            height=40,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self._create_baseline,
        )
        self.baseline_button.grid(
            row=4,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="w",
        )

    def _build_scan_card(self, parent):
        card = self._card(parent, 3)

        ctk.CTkLabel(
            card,
            text="Security Scan",
            font=ctk.CTkFont(FONT_FAMILY, 18, "bold"),
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=20, pady=(18, 3), sticky="w")

        ctk.CTkLabel(
            card,
            text="Compare the current filesystem against the trusted baseline.",
            font=ctk.CTkFont(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY,
        ).grid(row=1, column=0, padx=20, pady=(0, 12), sticky="w")

        self.scan_status = ctk.CTkLabel(
            card,
            text="Ready",
            font=ctk.CTkFont(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY,
        )
        self.scan_status.grid(row=2, column=0, padx=20, pady=(0, 12), sticky="w")

        self.scan_button = ctk.CTkButton(
            card,
            text="Scan Now",
            width=140,
            height=40,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self._start_scan,
        )
        self.scan_button.grid(
            row=3,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="w",
        )

    def _clear_folders(self):
        for widget in self.folder_container.winfo_children():
            widget.destroy()

    def _refresh_view(self):
        folders = self.service.get_folders()
        self._clear_folders()

        if not folders:
            ctk.CTkLabel(
                self.folder_container,
                text="No folders added yet.",
                text_color=TEXT_MUTED,
            ).grid(row=0, column=0, padx=15, pady=45)
        else:
            for row, folder in enumerate(folders):
                frame = ctk.CTkFrame(
                    self.folder_container,
                    fg_color="transparent",
                )
                frame.grid(
                    row=row,
                    column=0,
                    padx=8,
                    pady=5,
                    sticky="ew",
                )
                frame.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(
                    frame,
                    text=folder,
                    anchor="w",
                    text_color=TEXT_PRIMARY,
                ).grid(
                    row=0,
                    column=0,
                    padx=5,
                    sticky="ew",
                )

                ctk.CTkButton(
                    frame,
                    text="Remove",
                    width=75,
                    height=30,
                    corner_radius=7,
                    fg_color="transparent",
                    hover_color="#1E293B",
                    border_width=1,
                    border_color=BORDER,
                    text_color=TEXT_SECONDARY,
                    command=lambda p=folder: self._remove_folder(p),
                ).grid(row=0, column=1, padx=5)

        self.baseline_status.configure(
            text=(
                "● Baseline Available"
                if self.service.baseline_exists()
                else "● Baseline Not Created"
            ),
            text_color=(
                SUCCESS
                if self.service.baseline_exists()
                else TEXT_MUTED
            ),
        )

        self.file_count.configure(
            text=f"Configured folders: {len(folders)}"
        )

    def _add_folder(self):
        folder = filedialog.askdirectory(
            title="Select Folder to Monitor"
        )

        if not folder:
            return

        try:
            self.service.add_folder(folder)
            self._refresh_view()
        except ValueError as error:
            messagebox.showerror("Invalid Folder", str(error))

    def _use_sample_files(self):
        sample_path = (
            Path(__file__).resolve().parents[3]
            / "sample_files"
        )

        if not sample_path.is_dir():
            messagebox.showerror(
                "Sample Files Not Found",
                f"Could not find:\n{sample_path}",
            )
            return

        try:
            self.service.add_folder(str(sample_path))
            self._refresh_view()
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def _handle_drop(self, event):
        paths = self.winfo_toplevel().tk.splitlist(event.data)
        added = 0
        invalid = 0

        for raw_path in paths:
            path = Path(raw_path.strip("{}"))

            if not path.is_dir():
                invalid += 1
                continue

            try:
                if self.service.add_folder(str(path)):
                    added += 1
            except ValueError:
                invalid += 1

        self._refresh_view()

        if invalid and not added:
            messagebox.showwarning(
                "Invalid Drop",
                "Please drop one or more folders.",
            )
        elif added:
            messagebox.showinfo(
                "Folder Added",
                f"{added} folder(s) added to monitoring.",
            )

    def _remove_folder(self, folder):
        if not messagebox.askyesno(
            "Remove Folder",
            f"Stop monitoring this folder?\n\n{folder}",
        ):
            return

        self.service.remove_folder(folder)
        self._refresh_view()

    def _create_baseline(self):
        if not self.service.get_folders():
            messagebox.showwarning(
                "No Folders Configured",
                "Add at least one folder before creating a baseline.",
            )
            return

        self.baseline_button.configure(state="disabled")

        try:
            result = self.service.create_baseline()

            self.baseline_status.configure(
                text="● Baseline Available",
                text_color=SUCCESS,
            )

            self.file_count.configure(
                text=(
                    f"Folders: {result['folder_count']} | "
                    f"Files tracked: {result['file_count']}"
                )
            )

            messagebox.showinfo(
                "Baseline Created",
                (
                    "Baseline created successfully.\n\n"
                    f"Folders: {result['folder_count']}\n"
                    f"Files tracked: {result['file_count']}"
                ),
            )

        except (ValueError, OSError) as error:
            messagebox.showerror(
                "Baseline Creation Failed",
                str(error),
            )
        finally:
            self.baseline_button.configure(state="normal")

    def _start_scan(self):
        if not self.service.baseline_exists():
            messagebox.showwarning(
                "Baseline Required",
                "Create a baseline before running a scan.",
            )
            return

        self.scan_button.configure(state="disabled")
        self.scan_status.configure(
            text="Scanning...",
            text_color=WARNING,
        )

        threading.Thread(
            target=self._scan_worker,
            daemon=True,
        ).start()

    def _scan_worker(self):
        try:
            result = self.service.scan()
            self.after(
                0,
                lambda: self._scan_complete(result),
            )
        except Exception as error:
            self.after(
                0,
                lambda: self._scan_failed(str(error)),
            )

    def _scan_complete(self, result):
        added = len(result["added"])
        modified = len(result["modified"])
        deleted = len(result["deleted"])
        incidents = len(result["incident_ids"])

        self.scan_status.configure(
            text=(
                f"Scan complete  •  "
                f"Added: {added}  •  "
                f"Modified: {modified}  •  "
                f"Deleted: {deleted}  •  "
                f"Incidents: {incidents}"
            ),
            text_color=SUCCESS,
        )

        self.scan_button.configure(state="normal")

        if incidents:
            messagebox.showwarning(
                "Security Incidents Detected",
                (
                    f"{incidents} security incident(s) detected.\n\n"
                    "Open the Incidents page to review the evidence."
                ),
            )
        else:
            messagebox.showinfo(
                "Scan Complete",
                (
                    "No security incidents were detected.\n\n"
                    f"Added: {added}\n"
                    f"Modified: {modified}\n"
                    f"Deleted: {deleted}"
                ),
            )

    def _scan_failed(self, error):
        self.scan_status.configure(
            text="Scan failed",
            text_color="#EF4444",
        )
        self.scan_button.configure(state="normal")

        messagebox.showerror(
            "Scan Failed",
            error,
        )