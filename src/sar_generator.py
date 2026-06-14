from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_sar(alert):

    styles = getSampleStyleSheet()

    filename = (
        f"outputs/SAR_{alert['transaction_id']}.pdf"
    )

    doc = SimpleDocTemplate(filename)

    elements = []

    elements.append(
        Paragraph(
            "Suspicious Activity Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1,12)
    )

    elements.append(
        Paragraph(
            f"Transaction ID: {alert['transaction_id']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Client ID: {alert['client_id']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Risk Score: {alert['overall_risk_score']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Explanation: {alert['explanation']}",
            styles["Normal"]
        )
    )

    doc.build(elements)