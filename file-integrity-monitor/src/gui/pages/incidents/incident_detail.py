from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox

from src.reporting.pdf_report import generate_pdf_report

from ...theme import (
    APP_BG,
    CARD_BG,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    ACCENT,
    ACCENT_HOVER,
    DANGER,
    WARNING,
    FONT_FAMILY,
)


class IncidentDetail:
    def __init__(
        self,
        parent,
        incident,
        reports_dir,
    ):
        self.parent = parent
        self.incident = incident
        self.reports_dir = Path(
            reports_dir
        )

        self.window = ctk.CTkToplevel(
            parent
        )

        self.window.title(
            f"Incident "
            f"{incident.get('incident_id', '')}"
        )

        self.window.geometry(
            "720x650"
        )

        self.window.minsize(
            620,
            560,
        )

        self.window.configure(
            fg_color=APP_BG
        )

        self.window.grab_set()

        self._build()

    def _build(self):
        container = ctk.CTkScrollableFrame(
            self.window,
            fg_color="transparent",
        )

        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25,
        )

        incident_id = self.incident.get(
            "incident_id",
            "Unknown Incident",
        )

        created_at = self.incident.get(
            "created_at",
            "Unknown",
        )

        ctk.CTkLabel(
            container,
            text=incident_id,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=24,
                weight="bold",
            ),
            text_color=TEXT_PRIMARY,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            container,
            text=f"Created: {created_at}",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_MUTED,
        ).pack(
            anchor="w",
            pady=(3, 18),
        )

        analysis = self.incident.get(
            "analysis",
            {},
        )

        risk = analysis.get(
            "risk",
            {},
        )

        severity = risk.get(
            "severity",
            "UNKNOWN",
        ).upper()

        self._row(
            container,
            "File",
            analysis.get(
                "file_path",
                "Unknown",
            ),
        )

        self._row(
            container,
            "Change",
            analysis.get(
                "change_type",
                "Unknown",
            ).title(),
        )

        self._row(
            container,
            "Severity",
            severity,
        )

        self._row(
            container,
            "Risk Score",
            str(
                risk.get(
                    "score",
                    0,
                )
            ),
        )

        indicators = analysis.get(
            "indicators",
            [],
        )

        self._row(
            container,
            "Indicators",
            ", ".join(indicators)
            if indicators
            else "None",
        )

        yara_matches = analysis.get(
            "yara_matches",
            [],
        )

        if yara_matches:
            self._row(
                container,
                "YARA Matches",
                ", ".join(yara_matches),
            )

        self._row(
            container,
            "SHA-256",
            analysis.get(
                "sha256",
                "Not available",
            ),
        )

        entropy = analysis.get(
            "entropy"
        )

        if entropy is not None:
            self._row(
                container,
                "Entropy",
                str(entropy),
            )

        virustotal = analysis.get(
            "virustotal",
            {},
        )

        if virustotal:
            vt_text = (
                f"Known: "
                f"{virustotal.get('known', False)}\n"
                f"Malicious: "
                f"{virustotal.get('malicious', 0)}\n"
                f"Suspicious: "
                f"{virustotal.get('suspicious', 0)}"
            )

            self._row(
                container,
                "VirusTotal",
                vt_text,
            )

        ctk.CTkButton(
            container,
            text="Export PDF",
            width=140,
            height=38,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self._export,
        ).pack(
            anchor="w",
            pady=(20, 5),
        )

    def _row(
        self,
        parent,
        label,
        value,
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD_BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
        )

        card.pack(
            fill="x",
            pady=4,
        )

        ctk.CTkLabel(
            card,
            text=label,
            width=120,
            anchor="w",
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
                weight="bold",
            ),
            text_color=TEXT_SECONDARY,
        ).pack(
            side="left",
            padx=(14, 8),
            pady=12,
        )

        ctk.CTkLabel(
            card,
            text=value,
            justify="left",
            anchor="w",
            wraplength=480,
            font=ctk.CTkFont(
                family=FONT_FAMILY,
                size=12,
            ),
            text_color=TEXT_PRIMARY,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 14),
            pady=12,
        )

    def _export(self):
        self.reports_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        incident_id = self.incident.get(
            "incident_id",
            "incident",
        )

        output_path = (
            self.reports_dir
            / f"{incident_id}.pdf"
        )

        try:
            generate_pdf_report(
                self.incident,
                str(output_path),
            )

            messagebox.showinfo(
                "PDF Exported",
                (
                    "Incident report saved at:\n\n"
                    f"{output_path}"
                ),
                parent=self.window,
            )

        except Exception as error:
            messagebox.showerror(
                "Export Failed",
                str(error),
                parent=self.window,
            )