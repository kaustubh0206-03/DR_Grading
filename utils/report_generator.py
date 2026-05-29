import os
import io
from datetime import datetime
import numpy as np

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

from utils.preprocessing import DR_CLASSES
from utils.clinical import get_severity_info

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "reports")

COLORS = {
    "No DR":            (16, 185, 129),
    "Mild DR":          (245, 158, 11),
    "Moderate DR":      (249, 115, 22),
    "Severe DR":        (239, 68, 68),
    "Proliferative DR": (168, 85, 247),
}

RISK_COLORS = {
    "Low":          (16, 185, 129),
    "Low-Moderate": (245, 158, 11),
    "Moderate":     (249, 115, 22),
    "High":         (239, 68, 68),
    "Critical":     (168, 85, 247),
}

UNICODE_REPLACEMENTS = {
    '\u2014': '-',   # em dash
    '\u2013': '-',   # en dash
    '\u2018': "'",   # left single quote
    '\u2019': "'",   # right single quote
    '\u201c': '"',   # left double quote
    '\u201d': '"',   # right double quote
    '\u2026': '...',  # ellipsis
    '\u2022': '*',   # bullet
    '\u00a0': ' ',   # non-breaking space
    '\u2023': '+',   # triangular bullet
    '\u25B8': '-',   # small right-pointing triangle
    '\u00b7': '-',   # middle dot
    '\u2032': "'",   # prime
    '\u2033': '"',   # double prime
    '\u2192': '->',  # rightwards arrow
    '\u2190': '<-',  # leftwards arrow
    '\u2194': '<->', # left right arrow
    '\u2265': '>=',  # greater than or equal to
    '\u2264': '<=',  # less than or equal to
    '\u2260': '!=',  # not equal to
    '\u221e': 'inf', # infinity
    '\u2103': 'C',   # degree celsius
    '\u00b0': ' deg', # degree sign
}


def _sanitize(text):
    """Sanitize text for FPDF latin-1 encoding compatibility."""
    if not isinstance(text, str):
        text = str(text)
    for old, new in UNICODE_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text


class DrReport(FPDF if FPDF_AVAILABLE else object):
    def header(self):
        if self.page_no() == 1:
            self.set_fill_color(15, 23, 42)
            self.rect(0, 0, 210, 48, 'F')
            self.set_font("Helvetica", "B", 22)
            self.set_text_color(37, 99, 235)
            self.cell(0, 14, "DR GRADING", ln=True, align="C")
            self.set_font("Helvetica", "", 10)
            self.set_text_color(148, 163, 184)
            self.cell(0, 7, "Diabetic Retinopathy Screening Report", ln=True, align="C")
            self.set_font("Helvetica", "", 7)
            self.set_text_color(100, 116, 139)
            self.cell(0, 5, "AI-Assisted Clinical Decision Support System", ln=True, align="C")
            self.ln(8)
        else:
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, "DR GRADING  |  Diabetic Retinopathy Screening Report", align="R")
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  DR GRADING v2.0", align="C")

    def section_title(self, title):
        self.set_x(self.l_margin)
        self.set_fill_color(241, 245, 249)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(15, 23, 42)
        self.cell(0, 8, f"  {_sanitize(title)}", ln=True, fill=True)
        self.ln(2)

    def info_row(self, label, value, color=(37, 99, 235)):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 116, 139)
        self.cell(50, 6, _sanitize(label))
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*color)
        self.cell(0, 6, _sanitize(str(value)), ln=True)

    def safe_multi_cell(self, w, h, txt):
        self.set_x(self.l_margin)
        self.multi_cell(w, h, _sanitize(txt))

    def color_bar(self, width, color_rgb, label="", value=""):
        self.set_x(self.l_margin)
        r, g, b = color_rgb
        self.set_fill_color(r, g, b)
        self.rect(self.get_x(), self.get_y(), width, 5, 'F')
        self.ln(6)
        if label:
            self.set_font("Helvetica", "", 7)
            self.set_text_color(100, 116, 139)
            self.cell(0, 4, f"{label}: {value}", ln=True)


def generate_pdf_report(filename, predicted_class, confidence, probabilities,
                        quality_info=None, patient_data=None,
                        clinical_note="", recommendation="",
                        gradcam_image=None):
    if not FPDF_AVAILABLE:
        return generate_text_report(filename, predicted_class, confidence, probabilities, quality_info)

    pdf = DrReport()
    pdf.alias_nb_pages()

    severity = get_severity_info(predicted_class)
    class_color = COLORS.get(predicted_class, (37, 99, 235))
    pd_data = patient_data or {}

    # Page 1
    pdf.add_page()
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)

    # Patient Information
    pdf.section_title("PATIENT INFORMATION")
    pdf.info_row("Patient ID:", pd_data.get("patient_id", "N/A"))
    pdf.info_row("Age:", str(pd_data.get("age", "N/A")))
    pdf.info_row("Gender:", pd_data.get("gender", "N/A"))
    pdf.info_row("Scan Date:", pd_data.get("scan_date", datetime.now().strftime("%Y-%m-%d %H:%M")))
    pdf.info_row("Examination:", pd_data.get("exam_number", "N/A"))
    pdf.ln(4)

    # Screening Results
    pdf.section_title("SCREENING RESULTS")
    pdf.info_row("Diagnosis:", predicted_class, class_color)
    pdf.info_row("Severity:", severity.get("severity", ""), class_color)
    pdf.info_row("Risk Level:", severity.get("risk", ""), RISK_COLORS.get(severity.get("risk", "Low"), (100, 116, 139)))
    pdf.info_row("Confidence:", f"{confidence*100:.1f}%", class_color)

    # Confidence bar
    bar_w = int(confidence * 80)
    pdf.ln(2)
    pdf.color_bar(bar_w, class_color, "Confidence", f"{confidence*100:.1f}%")
    pdf.ln(4)

    # Class Probabilities
    pdf.section_title("CLASS PROBABILITIES")
    classes = ["No DR", "Mild DR", "Moderate DR", "Severe DR", "Proliferative DR"]
    for i, (cls, prob) in enumerate(zip(classes, probabilities)):
        c = COLORS.get(cls, (37, 99, 235))
        pdf.info_row(f"  {cls}:", f"{prob*100:.1f}%", c)
        bar_w = int(prob * 80)
        pdf.color_bar(bar_w, c)

    # Clinical Note
    pdf.section_title("CLINICAL ASSESSMENT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)
    note_text = clinical_note or "No clinical notes available."
    note_lines = note_text.split(". ")
    for line in note_lines:
        if line.strip():
            txt = line.strip() + ("." if not line.endswith(".") else "")
            pdf.safe_multi_cell(0, 5, txt)
    pdf.ln(4)

    # Recommendation
    pdf.section_title("RECOMMENDATION")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*class_color)
    rec = recommendation or severity.get("follow_up", "Consult ophthalmologist.")
    pdf.safe_multi_cell(0, 5, rec)
    pdf.ln(2)

    # Image Quality
    if quality_info:
        pdf.section_title("IMAGE QUALITY ASSESSMENT")
        q = quality_info
        q_score = q.get("quality_score", "N/A")
        q_color = (16, 185, 129) if q_score == "Excellent" else \
                  (245, 158, 11) if q_score == "Acceptable" else \
                  (239, 68, 68)
        pdf.info_row("Quality:", q_score, q_color)
        pdf.info_row("Brightness:", str(q.get("brightness", "N/A")))
        pdf.info_row("Contrast:", str(q.get("contrast", "N/A")))
        pdf.info_row("Blur Score:", str(q.get("blur_score", "N/A")))

    # GradCAM page
    if gradcam_image is not None:
        pdf.add_page()
        pdf.section_title("EXPLAINABLE AI - GRAD-CAM ANALYSIS")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(30, 41, 59)
        pdf.safe_multi_cell(0, 5, "Gradient-weighted Class Activation Mapping (Grad-CAM) highlights the regions "
                      "the model focused on during prediction. Warmer colors indicate higher activation.")
        pdf.ln(3)
        img_path = os.path.join(REPORT_DIR, "_temp_gradcam.png")
        try:
            gradcam_image.save(img_path)
            pdf.image(img_path, x=30, w=150)
            os.remove(img_path)
        except Exception:
            pass

    # Model Information
    pdf.section_title("MODEL INFORMATION")
    pdf.info_row("Architecture:", "Hybrid CNN + Vision Transformer")
    pdf.info_row("Input Size:", "456 x 456 x 3")
    pdf.info_row("Output Classes:", "5 (No DR / Mild / Moderate / Severe / PDR)")
    pdf.info_row("Framework:", "TensorFlow / Keras")
    pdf.info_row("Version:", "DR GRADING v2.0")

    # Disclaimer
    pdf.ln(4)
    pdf.set_fill_color(254, 242, 242)
    pdf.set_text_color(185, 28, 28)
    pdf.set_font("Helvetica", "I", 7)
    pdf.cell(0, 6, "  DISCLAIMER", ln=True, fill=True)
    pdf.set_fill_color(254, 242, 242)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(185, 28, 28)
    pdf.safe_multi_cell(0, 4, "  This report is generated by an AI-assisted screening system and is intended "
                  "for research and clinical decision support purposes only. All findings must be "
                  "reviewed and confirmed by a qualified ophthalmologist. This is not a definitive "
                  "diagnostic tool.", )

    pdf_bytes = bytes(pdf.output(dest='S'))
    return pdf_bytes


def generate_text_report(filename, predicted_class, confidence, probabilities, quality_info):
    from utils.clinical import get_severity_info, get_clinical_note
    severity = get_severity_info(predicted_class)
    note = get_clinical_note(predicted_class)
    lines = [
        "=" * 60,
        "          DR GRADING - Screening Report",
        "=" * 60,
        f"Date       : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"File       : {filename}",
        f"Diagnosis  : {predicted_class}",
        f"Severity   : {severity.get('severity', '')}",
        f"Risk       : {severity.get('risk', '')}",
        f"Confidence : {confidence*100:.1f}%",
        "",
        "Class Probabilities:",
    ]
    for cls, prob in zip(DR_CLASSES, probabilities):
        lines.append(f"  {cls:<20} {prob*100:.1f}%")
    lines += [
        "",
        "Clinical Assessment:",
        f"  {note}",
        "",
        "Recommendation:",
        f"  {severity.get('follow_up', '')}",
        "",
        "Image Quality:",
        f"  Score      : {quality_info.get('quality_score', 'N/A')}",
        "",
        "Model: Hybrid CNN + Vision Transformer | v2.0",
        "=" * 60,
    ]
    return "\n".join(lines).encode()
