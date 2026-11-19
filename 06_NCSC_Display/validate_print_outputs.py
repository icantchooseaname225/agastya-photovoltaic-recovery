"""Check generated NCSC PDFs for page count, page size and key claim text."""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PRINT = ROOT.parent / "printables"
A1 = [
    "AGASTYA_Poster_01_Problem_and_Question_A1.pdf",
    "AGASTYA_Poster_02_Architecture_A1.pdf",
    "AGASTYA_Poster_03_Evidence_and_Findings_A1.pdf",
    "AGASTYA_Poster_04_Conclusion_and_Next_Steps_A1.pdf",
]
A4 = [
    "AGASTYA_A4_Project_Summary.pdf",
    "AGASTYA_A4_Architecture.pdf",
    "AGASTYA_A4_Evidence_and_Results.pdf",
    "AGASTYA_A4_Attribution_and_Sources.pdf",
]
errors: list[str] = []


def check(name: str, expected: str) -> tuple[str, float, float]:
    path = PRINT / name
    reader = PdfReader(path)
    if len(reader.pages) != 1:
        errors.append(f"{name}: expected one page, found {len(reader.pages)}")
    page = reader.pages[0]
    width, height = float(page.mediabox.width), float(page.mediabox.height)
    target_w, target_h = ((594 / 25.4 * 72), (841 / 25.4 * 72)) if expected == "A1" else ((210 / 25.4 * 72), (297 / 25.4 * 72))
    if abs(width - target_w) > 3 or abs(height - target_h) > 3:
        errors.append(f"{name}: page is {width:.1f}×{height:.1f} pt; expected generated {expected} portrait size")
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    if len(text.strip()) < 120:
        errors.append(f"{name}: extracted text is unexpectedly short")
    if "Dias et al. (2023)" in text or "Sim et al. (2023)" in text:
        errors.append(f"{name}: stale author-year attribution remains")
    return text, width, height


all_text: dict[str, str] = {}
for name in A1:
    all_text[name], w, h = check(name, "A1")
    print(f"{name}: 1 page, {w:.1f}×{h:.1f} pt, text_chars={len(all_text[name])}")
for name in A4:
    all_text[name], w, h = check(name, "A4")
    print(f"{name}: 1 page, {w:.1f}×{h:.1f} pt, text_chars={len(all_text[name])}")

poster3 = all_text[A1[2]].lower()
a4results = all_text[A4[2]].lower()
for label, content in [(A1[2], poster3), (A4[2], a4results)]:
    for phrase in ("600 g/t", "630 g/t", "unresolved"):
        if phrase not in content:
            errors.append(f"{label}: required source-boundary phrase missing: {phrase}")
if "physical samples" not in poster3 or "0" not in poster3:
    errors.append(f"{A1[2]}: evidence poster is missing the zero-sample statement")

if errors:
    raise SystemExit("PDF validation failed:\n- " + "\n- ".join(errors))
print("PDF structural/text checks passed. A rendered visual preview was inspected; student/teacher print proof and event-rule approval remain required.")
