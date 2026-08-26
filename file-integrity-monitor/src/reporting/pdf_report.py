from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors


def generate_pdf_report(
    incident: dict,
    output_path: str,
) -> str:
    
    # Here Generate a PDF incident report from stored incident data.


    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    analysis = incident.get(
        "analysis",
        {}
    )

    risk = analysis.get(
        "risk",
        {}
    )

    virustotal = analysis.get(
        "virustotal",
        {}
    )

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    story = []

    story.append(
        Paragraph(
            "File Integrity Monitor",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Security Incident Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    incident_data = [
        ["Incident ID", incident.get("incident_id", "Unknown")],
        ["Detected", incident.get("created_at", "Unknown")],
        ["Change Type", analysis.get("change_type", "Unknown")],
        ["File", analysis.get("file_path", "Unknown")],
        ["SHA-256", analysis.get("sha256", "Not available")],
        ["Risk Score", f'{risk.get("score", 0)} / 100'],
        ["Severity", risk.get("severity", "UNKNOWN")],
    ]

    table = Table(
        incident_data,
        colWidths=[40 * mm, 130 * mm],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Detection Indicators",
            styles["Heading2"]
        )
    )

    indicators = analysis.get(
        "indicators",
        []
    )

    if indicators:
        for indicator in indicators:
            story.append(
                Paragraph(
                    f"• {indicator}",
                    styles["BodyText"]
                )
            )
    else:
        story.append(
            Paragraph(
                "None",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Entropy Analysis",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f'Entropy: {analysis.get("entropy", "N/A")}',
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f'High Entropy: {analysis.get("high_entropy", False)}',
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "YARA Analysis",
            styles["Heading2"]
        )
    )

    yara_matches = analysis.get(
        "yara_matches",
        []
    )

    if yara_matches:
        for match in yara_matches:
            story.append(
                Paragraph(
                    f"• {match}",
                    styles["BodyText"]
                )
            )
    else:
        story.append(
            Paragraph(
                "None",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "VirusTotal File Reputation",
            styles["Heading2"]
        )
    )

    vt_data = [
        ["Available", str(virustotal.get("available", False))],
        ["Known", str(virustotal.get("known", False))],
        ["Malicious", str(virustotal.get("malicious", 0))],
        ["Suspicious", str(virustotal.get("suspicious", 0))],
        ["Total Engines", str(virustotal.get("total_engines", 0))],
    ]

    vt_table = Table(
        vt_data,
        colWidths=[50 * mm, 120 * mm],
    )

    vt_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ]
        )
    )

    story.append(vt_table)

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Public IP Addresses",
            styles["Heading2"]
        )
    )

    public_ips = analysis.get(
        "public_ips",
        []
    )

    if public_ips:
        for ip in public_ips:
            story.append(
                Paragraph(
                    f"• {ip}",
                    styles["BodyText"]
                )
            )
    else:
        story.append(
            Paragraph(
                "None",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Report generated from the stored incident record. "
            "The monitored file was not rescanned during report "
            "generation.",
            styles["BodyText"]
        )
    )

    document.build(story)

    return str(output)