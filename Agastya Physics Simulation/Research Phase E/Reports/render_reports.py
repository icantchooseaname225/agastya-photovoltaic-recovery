"""Historical renderer for the 13 October Phase E report sources and PDFs.
The report text uses the superseded electrostatic Stage 3 / assay Stage 4 map.
Do not regenerate reports for current use until their source Markdown and figure captions are reconciled with AGASTYA_ARCHITECTURE.md.
"""
from __future__ import annotations

import csv
import html
import re
import textwrap
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, Image, KeepTogether, LongTable, NextPageTemplate,
    PageBreak, PageTemplate, Paragraph, Spacer, TableStyle, Preformatted,
)
from reportlab.platypus.tableofcontents import TableOfContents

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "Source_Markdown"
PDFS = BASE / "PDFs"
FIGURES = BASE.parent / "Simulation_Campaign" / "figures"
PDFS.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "navy": colors.HexColor("#103143"),
    "teal": colors.HexColor("#157A83"),
    "copper": colors.HexColor("#C8813B"),
    "ink": colors.HexColor("#243943"),
    "muted": colors.HexColor("#607984"),
    "paper": colors.HexColor("#FBFAF7"),
    "pale": colors.HexColor("#EAF0EE"),
    "line": colors.HexColor("#D5DEDA"),
    "white": colors.white,
}

REPORTS = [
    ("R01_Technical_Research_Dossier.md", "01_AGASTYA_Technical_Research_Dossier.pdf", "AG-R01"),
    ("R02_Thermal_Physics_Chemical_Transformations.md", "02_Thermal_Physics_and_Chemical_Transformations.pdf", "AG-R02"),
    ("R03_Stage4_Mechanism_Process_Analysis.md", "03_Stage4_Mechanism_and_Process_Analysis.pdf", "AG-R03"),
    ("R04_Computational_Modeling_Simulation_Atlas.md", "04_Computational_Modeling_and_Simulation_Atlas.pdf", "AG-R04"),
    ("R05_Materials_Mass_Balance_Recovery_Analysis.md", "05_Materials_Mass_Balance_and_Recovery_Analysis.pdf", "AG-R05"),
    ("R06_Engineering_Feasibility_Next_Priorities.md", "06_Engineering_Feasibility_and_Next_Research_Priorities.pdf", "AG-R06"),
    ("R07_Research_Progress_Development_Record.md", "07_Research_Progress_and_Development_Record.pdf", "AG-R07"),
    ("../REPORT_INDEX.md", "00_AGASTYA_Phase_E_Report_Collection_Index.pdf", "AG-PE-INDEX"),
    ("../Appendices/Appendix_Model_Inputs.md", "08_Appendix_Thermal_Model_Inputs.pdf", "AG-APP-A"),
    ("../Appendices/Appendix_Main_Effect_Results.md", "09_Appendix_Main_Effect_Results.pdf", "AG-APP-B"),
]

CAPTIONS = {
    "process": "Current four-stage architecture from the Phase A charter and Phase D crosswalk. The dashed route is optional thermal delamination before current Stage 2; it is not current Stage 3.",
    "anova": "Main-effect variance shares calculated from the 5,040-row EXP-S3-02 factorial scenario grid. Equal row weights describe this deterministic design only; the residual includes interactions and is not a probability.",
    "mesh": "Relative difference from the 16-cells-per-layer numerical reference for the optional thermal pretreatment model. Coarser meshes are compared across four selected assumed cases; no curve represents measured panel temperatures.",
    "stage4": "Stage 4 is a sampling, assay and accounting workflow. Boxes are proposed records and checks; no AGASTYA assay result exists.",
    "massflow": "Conceptual mass and silver tracking boundary. Stream widths carry no quantitative meaning because actual stream masses and Ag assays are not yet measured.",
}


def register_fonts() -> None:
    font_root = Path(r"C:\Windows\Fonts")
    paths = {
        "AGRegular": font_root / "arial.ttf",
        "AGBold": font_root / "arialbd.ttf",
        "AGItalic": font_root / "ariali.ttf",
        "AGBoldItalic": font_root / "arialbi.ttf",
        "AGMono": font_root / "consola.ttf",
    }
    for name, path in paths.items():
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))
    needed = {"AGRegular", "AGBold", "AGItalic", "AGMono"}
    if not needed.issubset(set(pdfmetrics.getRegisteredFontNames())):
        raise RuntimeError("Required Arial/Consolas fonts were not found; PDF font embedding cannot be guaranteed.")
    pdfmetrics.registerFontFamily("AGRegular", normal="AGRegular", bold="AGBold", italic="AGItalic", boldItalic="AGBoldItalic")


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="AGBody", fontName="AGRegular", fontSize=9.2, leading=13.2, textColor=PALETTE["ink"], spaceAfter=6.5, allowWidows=0, allowOrphans=0))
    s.add(ParagraphStyle(name="AGH1", fontName="AGBold", fontSize=16, leading=20, textColor=PALETTE["navy"], spaceBefore=15, spaceAfter=7, keepWithNext=True))
    s.add(ParagraphStyle(name="AGH2", fontName="AGBold", fontSize=11.4, leading=14.4, textColor=PALETTE["teal"], spaceBefore=9, spaceAfter=4.5, keepWithNext=True))
    s.add(ParagraphStyle(name="AGH3", fontName="AGBold", fontSize=9.8, leading=12, textColor=PALETTE["navy"], spaceBefore=7, spaceAfter=3, keepWithNext=True))
    s.add(ParagraphStyle(name="AGMeta", fontName="AGRegular", fontSize=8.2, leading=11, textColor=PALETTE["muted"], spaceAfter=2))
    s.add(ParagraphStyle(name="AGCaption", fontName="AGItalic", fontSize=8.1, leading=10.5, textColor=PALETTE["muted"], spaceBefore=4, spaceAfter=9, alignment=TA_LEFT))
    s.add(ParagraphStyle(name="AGCell", fontName="AGRegular", fontSize=7.7, leading=9.4, textColor=PALETTE["ink"], spaceAfter=0))
    s.add(ParagraphStyle(name="AGCellHead", fontName="AGBold", fontSize=7.8, leading=9.4, textColor=PALETTE["white"], spaceAfter=0))
    s.add(ParagraphStyle(name="AGBullet", parent=s["AGBody"], leftIndent=12, firstLineIndent=-8, spaceAfter=3.2))
    s.add(ParagraphStyle(name="AGCode", fontName="AGMono", fontSize=7.5, leading=9.4, textColor=PALETTE["ink"], backColor=PALETTE["pale"], borderColor=PALETTE["line"], borderWidth=0.4, borderPadding=6, leftIndent=6, rightIndent=6, spaceBefore=3, spaceAfter=8))
    s.add(ParagraphStyle(name="AGTOC0", fontName="AGBold", fontSize=10.1, leading=15, textColor=PALETTE["navy"], leftIndent=0, firstLineIndent=0, spaceBefore=3))
    s.add(ParagraphStyle(name="AGTOC1", fontName="AGRegular", fontSize=8.6, leading=12, textColor=PALETTE["ink"], leftIndent=17, firstLineIndent=0))
    s.add(ParagraphStyle(name="AGTOCTitle", fontName="AGBold", fontSize=20, leading=24, textColor=PALETTE["navy"], spaceAfter=15))
    return s


def para_markup(source: str) -> str:
    # Escape ordinary text first, then convert the small Markdown inline subset.
    break_token = "\ue100"
    value = html.escape(source.replace("<br/>", break_token), quote=False)
    value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<link href="\2" color="#157A83">\1</link>', value)
    value = re.sub(
        r"\[([^\]]+)\]\((?!https?://|mailto:)([^)]+)\)",
        lambda match: f'<font color="#157A83">{match.group(1)}</font> ({Path(match.group(2).split("#", 1)[0]).name})',
        value,
    )
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", value)
    value = re.sub(r"`([^`]+)`", r'<font name="AGMono">\1</font>', value)
    value = value.replace(break_token, "<br/>")
    return value


def parse_table(lines: list[str], avail_width: float, styles_dict):
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return None
    ncol = max(map(len, rows))
    rows = [row + [""] * (ncol - len(row)) for row in rows]
    data = []
    for ridx, row in enumerate(rows):
        st = styles_dict["AGCellHead"] if ridx == 0 else styles_dict["AGCell"]
        data.append([Paragraph(para_markup(cell), st) for cell in row])
    maxlens = [max(len(row[i]) for row in rows) for i in range(ncol)]
    weights = [max(10, min(44, max(10, len(rows[0][i]) * 1.5, maxlens[i] * 0.55))) for i in range(ncol)]
    total = sum(weights)
    widths = [avail_width * w / total for w in weights]
    table = LongTable(data, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALETTE["navy"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALETTE["paper"]]),
        ("GRID", (0, 0), (-1, -1), 0.35, PALETTE["line"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.2),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, PALETTE["teal"]),
    ]))
    return table


def rounded_box(c, x, y, w, h, title, subtitle="", fill=None, stroke=None, title_color=None, title_size=8.8):
    fill = fill or PALETTE["white"]
    stroke = stroke or PALETTE["teal"]
    title_color = title_color or PALETTE["navy"]
    c.setLineWidth(1.1)
    c.setStrokeColor(stroke)
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    c.setFillColor(title_color)
    c.setFont("AGBold", title_size)
    title_lines = title.split("\n")
    top = y + h - 18
    for i, line in enumerate(title_lines):
        c.drawCentredString(x + w / 2, top - i * 11, line)
    if subtitle:
        c.setFont("AGRegular", 6.7)
        c.setFillColor(PALETTE["muted"])
        for j, line in enumerate(subtitle.split("\n")):
            c.drawCentredString(x + w / 2, y + 11 + (len(subtitle.split("\n")) - 1 - j) * 8, line)


def arrow(c, x1, y1, x2, y2, dashed=False, color=None):
    color = color or PALETTE["teal"]
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.2)
    if dashed:
        c.setDash(4, 3)
    c.line(x1, y1, x2, y2)
    angle = __import__("math").atan2(y2 - y1, x2 - x1)
    size = 5
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - size * __import__("math").cos(angle - 0.45), y2 - size * __import__("math").sin(angle - 0.45))
    p.lineTo(x2 - size * __import__("math").cos(angle + 0.45), y2 - size * __import__("math").sin(angle + 0.45))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


class VectorDiagram(Flowable):
    def __init__(self, name: str, width: float):
        super().__init__()
        self.name = name
        self.width = width
        self.height = 180 if name != "massflow" else 210

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.width, self.height
        c.setFillColor(PALETTE["paper"])
        c.roundRect(0, 0, w, h, 9, fill=1, stroke=0)
        if self.name == "process":
            boxw = (w - 36) / 4
            xs = [8 + i * (boxw + 6.7) for i in range(4)]
            yy = 98
            labels = [
                ("Stage 1", "Disassembly &\nrouting"),
                ("Stage 2", "Liberation &\nclassification"),
                ("Stage 3", "Electrostatic\nseparation"),
                ("Stage 4", "Sampling, assay\n& accounting"),
            ]
            for x, (title, sub) in zip(xs, labels):
                rounded_box(c, x, yy, boxw, 56, title, sub)
            for i in range(3):
                arrow(c, xs[i] + boxw + 1, yy + 28, xs[i + 1] - 2, yy + 28)
            optw = boxw * 1.75
            optx = (w - optw) / 2
            rounded_box(c, optx, 17, optw, 43, "Optional thermal pretreatment", "hot knife / delamination; upstream of current Stage 2", fill=colors.HexColor("#F5EEE5"), stroke=PALETTE["copper"], title_color=PALETTE["navy"])
            arrow(c, xs[0] + boxw * .72, yy - 2, optx + 5, 58, dashed=True, color=PALETTE["copper"])
            arrow(c, optx + optw - 5, 58, xs[1] + boxw * .28, yy - 2, dashed=True, color=PALETTE["copper"])
            c.setFont("AGItalic", 6.5); c.setFillColor(PALETTE["muted"])
            c.drawCentredString(w / 2, 5, "Proposed process map; operation yields and stream masses are not measured")
        elif self.name == "stage4":
            boxw = (w - 36) / 4
            xs = [8 + i * (boxw + 6.7) for i in range(4)]
            yy = 72
            items = [
                ("All streams", "feed, products, rejects,\ndust and losses"),
                ("Representative split", "IDs, homogenization,\nretained sample"),
                ("Matrix-valid assay", "preparation, QA/QC,\nlimits and uncertainty"),
                ("Reconciled ledger", "mass / Ag closure,\ngrade and recovery"),
            ]
            for x, (title, sub) in zip(xs, items):
                rounded_box(c, x, yy, boxw, 67, title, sub, fill=PALETTE["white"])
            for i in range(3):
                arrow(c, xs[i] + boxw + 1, yy + 33, xs[i + 1] - 2, yy + 33)
            c.setFont("AGBold", 7.6); c.setFillColor(PALETTE["copper"])
            c.drawCentredString(w / 2, 34, "STAGE 4 OUTPUT = AUDITABLE DATA; NO SILVER REFINING STEP")
        elif self.name == "massflow":
            c.setFont("AGBold", 8.3); c.setFillColor(PALETTE["navy"])
            c.drawString(11, h - 18, "UNQUANTIFIED STREAMS · MEASURE MASS AND ASSAY BEFORE CLAIMING RECOVERY")
            boxw = (w - 48) / 5
            xs = [8 + i * (boxw + 6) for i in range(5)]
            yy = 112
            items = ["Identified\nfeed", "Stage 1\nrouting", "Stage 2\nliberation", "Stage 3\nseparation", "Stage 4\nassay"]
            for i, (x, label) in enumerate(zip(xs, items)):
                rounded_box(c, x, yy, boxw, 52, label, "mass / Ag unknown", fill=PALETTE["white"], stroke=PALETTE["teal"] if i < 4 else PALETTE["copper"])
            for i in range(4):
                arrow(c, xs[i] + boxw + 1, yy + 25, xs[i + 1] - 2, yy + 25)
            branches = [
                (1, "Glass / frame /\nbox / laminate"),
                (2, "Size fractions +\ndust / residue"),
                (3, "Concentrate +\nmiddlings / rejects"),
            ]
            for index, label in branches:
                bx = xs[index]
                center = bx + boxw / 2
                c.setStrokeColor(PALETTE["line"]); c.setDash(2, 2); c.line(center, yy, center, 70); c.setDash()
                rounded_box(c, bx, 17, boxw, 52, label, "weigh + assay", fill=colors.HexColor("#F2F5F4"), stroke=PALETTE["muted"], title_size=7.7)
            c.setFont("AGItalic", 6.8); c.setFillColor(PALETTE["muted"])
            c.drawCentredString(w / 2, 7, "Capture dust and equipment residue; widths are schematic and imply no yield, Ag split or purity")
        c.restoreState()


class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, title, report_id, toc, **kwargs):
        super().__init__(filename, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=19 * mm, bottomMargin=16 * mm, title=title, author="AGASTYA project research record", subject="AGASTYA Phase E technical report", **kwargs)
        self.report_id = report_id
        self.toc = toc
        cover = Frame(0, 0, A4[0], A4[1], id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        body = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="Cover", frames=[cover], onPage=self.draw_cover),
            PageTemplate(id="Body", frames=[body], onPage=self.draw_body),
        ])

    def draw_cover(self, canvas, doc):
        c = canvas
        c.saveState()
        c.setFillColor(PALETTE["paper"]); c.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        c.setFillColor(PALETTE["navy"]); c.rect(0, A4[1] - 15 * mm, A4[0], 15 * mm, fill=1, stroke=0)
        c.setFillColor(PALETTE["teal"]); c.rect(0, 0, 8 * mm, A4[1], fill=1, stroke=0)
        c.setFillColor(PALETTE["white"]); c.setFont("AGBold", 10)
        c.drawString(24 * mm, A4[1] - 10 * mm, "AGASTYA  /  MATERIALS RECOVERY RESEARCH")
        # Abstract layer/transport motif, deliberately not a measured result.
        cx, cy = A4[0] - 52 * mm, A4[1] - 62 * mm
        for r, color, width in [(31 * mm, PALETTE["line"], 0.7), (22 * mm, PALETTE["teal"], 1.3), (12 * mm, PALETTE["copper"], 1.4)]:
            c.setStrokeColor(color); c.setLineWidth(width); c.circle(cx, cy, r, fill=0, stroke=1)
        c.setStrokeColor(PALETTE["line"]); c.setLineWidth(0.6)
        for yy in [cy - 22 * mm, cy - 12 * mm, cy - 2 * mm, cy + 8 * mm, cy + 18 * mm]:
            c.line(cx - 38 * mm, yy, cx + 36 * mm, yy)
        c.setFillColor(PALETTE["copper"]); c.circle(cx, cy, 2.3 * mm, fill=1, stroke=0)
        c.setFillColor(PALETTE["teal"]); c.rect(24 * mm, A4[1] - 95 * mm, 21 * mm, 2.3 * mm, fill=1, stroke=0)
        c.setFillColor(PALETTE["muted"]); c.setFont("AGBold", 8.3)
        c.drawString(24 * mm, A4[1] - 82 * mm, "ENGINEERING RESEARCH  /  PHASE E  /  13 OCTOBER 2026")
        title = doc.title
        lines = textwrap.wrap(title, width=31)
        y = A4[1] - 117 * mm
        c.setFillColor(PALETTE["navy"]); c.setFont("AGBold", 25)
        for line in lines[:3]:
            c.drawString(24 * mm, y, line)
            y -= 12 * mm
        c.setFillColor(PALETTE["ink"]); c.setFont("AGRegular", 11)
        c.drawString(24 * mm, y - 2 * mm, "Research dossier | reproducible calculations | explicit evidence limits")
        c.setStrokeColor(PALETTE["line"]); c.line(24 * mm, 46 * mm, A4[0] - 22 * mm, 46 * mm)
        c.setFillColor(PALETTE["navy"]); c.setFont("AGBold", 9)
        c.drawString(24 * mm, 37 * mm, doc.report_id)
        c.setFillColor(PALETTE["muted"]); c.setFont("AGRegular", 8.4)
        c.drawRightString(A4[0] - 22 * mm, 37 * mm, "Prepared from available AGASTYA records")
        c.setFont("AGItalic", 7.6)
        c.drawString(24 * mm, 26 * mm, "No institutional affiliation, laboratory endorsement or physical recovery result is claimed.")
        c.restoreState()

    def draw_body(self, canvas, doc):
        c = canvas
        c.saveState()
        c.setStrokeColor(PALETTE["teal"]); c.setLineWidth(1.2)
        c.line(self.leftMargin, A4[1] - 13.2 * mm, A4[0] - self.rightMargin, A4[1] - 13.2 * mm)
        c.setFillColor(PALETTE["navy"]); c.setFont("AGBold", 7.5)
        c.drawString(self.leftMargin, A4[1] - 10.2 * mm, "AGASTYA  /  TECHNICAL RESEARCH")
        c.setFillColor(PALETTE["muted"]); c.setFont("AGRegular", 7.2)
        c.drawRightString(A4[0] - self.rightMargin, A4[1] - 10.2 * mm, self.report_id)
        c.setStrokeColor(PALETTE["line"]); c.setLineWidth(0.6)
        c.line(self.leftMargin, 11 * mm, A4[0] - self.rightMargin, 11 * mm)
        c.setFillColor(PALETTE["muted"]); c.setFont("AGRegular", 7)
        c.drawString(self.leftMargin, 7 * mm, "Evidence is labeled by source and method; model output is not physical validation.")
        c.drawRightString(A4[0] - self.rightMargin, 7 * mm, f"{max(1, c.getPageNumber() - 1)}")
        c.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ("AGH1", "AGH2"):
            level = 0 if flowable.style.name == "AGH1" else 1
            text = flowable.getPlainText()
            self.notify("TOCEntry", (level, text, self.page))


def figure_flowable(name, width, figure_number):
    if name in ("process", "stage4", "massflow"):
        graphic = VectorDiagram(name, width)
    elif name == "anova":
        graphic = Image(str(FIGURES / "PE-SIM-001_main_effect_variance.png"), width=width, height=width * 1130 / 1800)
    elif name == "mesh":
        graphic = Image(str(FIGURES / "PE-SIM-002_spatial_refinement.png"), width=width, height=width * 1260 / 1800)
    else:
        raise ValueError(f"Unknown report figure: {name}")
    cap = Paragraph(f"<b>Figure {figure_number}.</b> {para_markup(CAPTIONS[name])}", styles_dict["AGCaption"])
    return KeepTogether([graphic, cap, Spacer(1, 3)])


def make_story(markdown_path: Path, report_id: str):
    raw = markdown_path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), markdown_path.stem.replace("_", " "))
    # Keep only content after document-level title and metadata lines.
    start = next((idx for idx, line in enumerate(lines) if line.startswith("## ")), len(lines))
    body_lines = lines[start:]
    story = [Spacer(1, 1), NextPageTemplate("Body"), PageBreak(), Paragraph("Contents", styles_dict["AGTOCTitle"])]
    toc = TableOfContents()
    toc.levelStyles = [styles_dict["AGTOC0"], styles_dict["AGTOC1"]]
    toc.dotsMinLevel = 0
    story.extend([toc, PageBreak()])
    figure_count = 0
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        if not line.strip():
            i += 1; continue
        if line.strip() == "{{PAGEBREAK}}":
            story.append(PageBreak())
            i += 1; continue
        if line.startswith("{{FIGURE:"):
            name = line.split(":", 1)[1].split("}", 1)[0].strip().lower()
            figure_count += 1
            story.append(figure_flowable(name, A4[0] - 36 * mm, figure_count))
            i += 1; continue
        if line.startswith("```"):
            code = []
            i += 1
            while i < len(body_lines) and not body_lines[i].startswith("```"):
                code.append(body_lines[i]); i += 1
            story.append(Preformatted("\n".join(code), styles_dict["AGCode"], maxLineLength=105))
            i += 1; continue
        if line.lstrip().startswith("|"):
            block = []
            while i < len(body_lines) and body_lines[i].lstrip().startswith("|"):
                block.append(body_lines[i]); i += 1
            tbl = parse_table(block, A4[0] - 36 * mm, styles_dict)
            if tbl:
                story.extend([Spacer(1, 3), tbl, Spacer(1, 7)])
            continue
        if line.startswith("### ") or line.startswith("## ") or line.startswith("#### "):
            if line.startswith("#### "):
                level, title_text, style = 3, line[5:].strip(), styles_dict["AGH3"]
            elif line.startswith("### "):
                level, title_text, style = 2, line[4:].strip(), styles_dict["AGH2"]
            else:
                level, title_text, style = 1, line[3:].strip(), styles_dict["AGH1"]
            story.append(Paragraph(para_markup(title_text), style))
            i += 1; continue
        if re.match(r"^\s*[-*] ", line) or re.match(r"^\s*\d+\. ", line):
            ordered = bool(re.match(r"^\s*\d+\. ", line))
            items = []
            while i < len(body_lines) and (re.match(r"^\s*[-*] ", body_lines[i]) or re.match(r"^\s*\d+\. ", body_lines[i])):
                item = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", body_lines[i]).strip()
                items.append(Paragraph(("• " if not ordered else "") + para_markup(item), styles_dict["AGBullet"]))
                i += 1
            story.extend(items)
            continue
        # Merge ordinary wrapped Markdown lines into a paragraph; two trailing
        # spaces create a deliberate line break (used for equations).
        parts = []
        while i < len(body_lines) and body_lines[i].strip() and not body_lines[i].startswith(("## ", "### ", "#### ", "{{FIGURE:", "```")) and not body_lines[i].lstrip().startswith("|") and not re.match(r"^\s*(?:[-*]|\d+\.)\s+", body_lines[i]):
            current = body_lines[i]
            if current.endswith("  "):
                parts.append(current.rstrip() + "<br/>")
            else:
                parts.append(current.strip())
            i += 1
        text = " ".join(parts).replace(" <br/>", "<br/>")
        if text.strip():
            story.append(Paragraph(para_markup(text), styles_dict["AGBody"]))
    return title, story


def write_diagram_sources():
    folder = FIGURES / "diagrams"
    folder.mkdir(parents=True, exist_ok=True)
    common = '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="540" viewBox="0 0 1500 540"><rect width="1500" height="540" fill="#FBFAF7"/>'
    def box(x, y, w, h, title, sub, stroke="#157A83", fill="#FFFFFF"):
        title_lines = title.split("|")
        text = "".join(f'<text x="{x+w/2}" y="{y+28+i*25}" text-anchor="middle" font-family="Arial" font-size="22" font-weight="700" fill="#103143">{html.escape(t)}</text>' for i,t in enumerate(title_lines))
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="3"/>{text}<text x="{x+w/2}" y="{y+h-18}" text-anchor="middle" font-family="Arial" font-size="15" fill="#607984">{html.escape(sub)}</text>'
    process = common
    labels = [(40,"Stage 1|Disassembly","routing"),(405,"Stage 2|Liberation","classification"),(770,"Stage 3|Electrostatic","candidate"),(1135,"Stage 4|Sampling + assay","accounting")]
    for x, t, sub in labels:
        process += box(x,130,300,115,t,sub)
    for x in (342,707,1072):
        process += f'<path d="M{x} 188 H{x+48}" stroke="#157A83" stroke-width="4" marker-end="url(#a)"/>'
    process += '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0 L0 6 L9 3 z" fill="#157A83"/></marker></defs>'
    process += box(520,350,460,95,"Optional thermal pretreatment","upstream of Stage 2; not current Stage 3","#C8813B","#F5EEE5")
    process += '<path d="M190 246 C190 385 480 395 515 395 M985 395 C1050 395 1290 390 1290 250" fill="none" stroke="#C8813B" stroke-width="3" stroke-dasharray="10 8" marker-end="url(#a)"/>'
    process += '<text x="750" y="510" text-anchor="middle" font-family="Arial" font-size="18" fill="#607984">Project process map; measured yields and stream masses are not available</text></svg>'
    (folder / "four_stage_process_map.svg").write_text(process, encoding="utf-8")
    (folder / "stage4_assay_workflow.svg").write_text(common + box(35,190,300,120,"All streams","weigh + identify") + box(405,190,300,120,"Representative sample","split + retain") + box(775,190,300,120,"Matrix-valid assay","preparation + QA/QC") + box(1145,190,300,120,"Reconciled ledger","grade + recovery + residuals") + ''.join(f'<path d="M{x} 250 H{x+65}" stroke="#157A83" stroke-width="4" marker-end="url(#a)"/>' for x in (338,708,1078)) + '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0 L0 6 L9 3 z" fill="#157A83"/></marker></defs><text x="750" y="430" text-anchor="middle" font-family="Arial" font-size="19" fill="#C8813B">Stage 4 creates an auditable measurement record; no silver refining is performed.</text></svg>', encoding="utf-8")
    (folder / "unquantified_material_flow.svg").write_text(common + ''.join(box(15+i*298,160,270,115,title,sub) for i,(title,sub) in enumerate([("Module feed","Ag inventory unknown"),("Stage 1","component streams unknown"),("Stage 2","size classes unknown"),("Stage 3","bins and losses unknown"),("Stage 4","assay and balance")])) + ''.join(f'<path d="M{286+i*298} 218 H{305+i*298}" stroke="#157A83" stroke-width="4" marker-end="url(#a)"/>' for i in range(4)) + '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0 L0 6 L9 3 z" fill="#157A83"/></marker></defs><text x="750" y="405" text-anchor="middle" font-family="Arial" font-size="19" fill="#607984">Schematic only — widths do not encode mass or silver recovery.</text></svg>', encoding="utf-8")


def build_all():
    global styles_dict
    register_fonts()
    styles_dict = styles()
    write_diagram_sources()
    qa_rows = []
    for source_name, pdf_name, report_id in REPORTS:
        source_path = SOURCE / source_name
        title, story = make_story(source_path, report_id)
        toc = next(flowable for flowable in story if isinstance(flowable, TableOfContents))
        output = PDFS / pdf_name
        doc = ReportDoc(str(output), title, report_id, toc)
        doc.multiBuild(story, maxPasses=5)
        reader = PdfReader(str(output), strict=True)
        pages = len(reader.pages)
        extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
        page_sizes_ok = all(abs(float(page.mediabox.width) - A4[0]) < 1 and abs(float(page.mediabox.height) - A4[1]) < 1 for page in reader.pages)
        blank_pages = [n + 1 for n, page in enumerate(reader.pages) if len((page.extract_text() or "").strip()) < 35]
        source_title = title.strip()
        extracted_normalized = re.sub(r"\s+", " ", extracted).lower()
        source_title_normalized = re.sub(r"\s+", " ", source_title).lower()
        text_ok = source_title_normalized in extracted_normalized and report_id in extracted and "Contents" in extracted
        embedded_font = b"FontFile2" in output.read_bytes()
        qa_rows.append({
            "PDF": str(output), "Report ID": report_id, "Title": title,
            "Pages": pages, "File size bytes": output.stat().st_size,
            "A4 page sizes": page_sizes_ok, "Blank_or_near_blank_pages": ";".join(map(str, blank_pages)),
            "Title_ID_TOC_text_check": text_ok, "Embedded_TTF_font_detected": embedded_font,
            "Replacement_character_present": "\ufffd" in extracted,
        })
        print(f"Rendered {pdf_name}: {pages} pages, {output.stat().st_size:,} bytes")
    qa_path = BASE / "PDF_QA_REPORT.csv"
    with qa_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(qa_rows[0]))
        writer.writeheader(); writer.writerows(qa_rows)
    failures = [row for row in qa_rows if not row["A4 page sizes"] or row["Blank_or_near_blank_pages"] or not row["Title_ID_TOC_text_check"] or not row["Embedded_TTF_font_detected"] or row["Replacement_character_present"]]
    if failures:
        raise RuntimeError(f"PDF quality checks found {len(failures)} issue(s); see {qa_path}")
    print(f"PDF structural, text, font and page-size checks passed for {len(qa_rows)} PDFs. QA: {qa_path}")


if __name__ == "__main__":
    build_all()
