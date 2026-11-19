from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = Path(__file__).resolve().parents[1]
NAVY = "17365D"
BLUE = "2F75B5"
PALE = "D9EAF7"
YELLOW = "FFF2CC"
WHITE = "FFFFFF"
LINE = Side(style="thin", color="B7C9D6")


def base_sheet(ws, title, note, headers, widths=None):
    ws.sheet_view.showGridLines = False
    n = len(headers)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n)
    c = ws.cell(1, 1, title)
    c.font = Font(name="Arial", size=15, bold=True, color=WHITE)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 28
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n)
    c = ws.cell(2, 1, note)
    c.font = Font(name="Arial", size=10, italic=True, color="404040")
    c.fill = PatternFill("solid", fgColor=YELLOW)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[2].height = 42
    for i, label in enumerate(headers, 1):
        cell = ws.cell(4, i, label)
        cell.font = Font(name="Arial", size=10, bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = Border(bottom=LINE)
        if widths and label in widths:
            ws.column_dimensions[get_column_letter(i)].width = widths[label]
    ws.row_dimensions[4].height = 34
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:{get_column_letter(n)}4"


def add_rows(ws, rows):
    for r, row in enumerate(rows, 5):
        for c, value in enumerate(row, 1):
            cell = ws.cell(r, c, value)
            cell.font = Font(name="Arial", size=10, color="222222")
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=LINE)
    if rows:
        ws.auto_filter.ref = f"A4:{get_column_letter(ws.max_column)}{ws.max_row}"
        safe_name = "".join(ch for ch in ws.title if ch.isalnum()) or "Sheet"
        table = Table(displayName=f"Tbl{safe_name}", ref=f"A4:{get_column_letter(ws.max_column)}{ws.max_row}")
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
        ws.add_table(table)


def make_bom():
    wb = Workbook()
    ws = wb.active
    ws.title = "Thermal station BOM"
    headers = ["Block", "Component", "Purpose", "Required specification / selection gate", "Qty", "Price INR", "Price status / source", "Essential?", "Alternative / notes"]
    base_sheet(ws, "AGASTYA Stage 3 — Thermal BOM", "Current map: Stage 3 thermal delamination; Stage 4 silver removal. This BOM is a planning list, not an approved purchase list. Active station and safety items require host review and quotes.", headers, {"Block": 18, "Component": 30, "Purpose": 32, "Required specification / selection gate": 52, "Qty": 8, "Price INR": 14, "Price status / source": 42, "Essential?": 14, "Alternative / notes": 46})
    rows = [
        ["Feed/support", "Rigid flat support table", "Support flat module/coupon through blade entry and output separation", "Dimension to actual module/coupon; stable, noncombustible, cleanable; no unsupported glass overhang", 1, None, "Fabrication quote required", "Yes", "Cold fixture can be prototyped before heater selection."],
        ["Feed/support", "Side guides and controlled feed", "Maintain repeatable path and feed rate", "Adjustable to known feed geometry; guarded pinch points; jam procedure", 1, None, "Facility-specific quote required", "Yes", "Manual feed only if approved by host."],
        ["Thermal tool", "Fixed hot knife / blade assembly", "Apply localized heat at glass/EVA boundary", "Rated industrial/lab unit selected by facility; replaceable blade; controlled contact geometry", 1, None, "Quote required; no hobby cutter substitution", "Yes", "No wiring design or heater model selected."],
        ["Thermal control", "Controller and independent over-temperature limit", "Maintain approved tool condition and cut off on fault", "Compatible with selected tool; separate limit function; reviewed by qualified electrical supervisor", 1, None, "Quote required", "Yes", "Control display alone is not an independent safety limit."],
        ["Guarding", "Hot-zone and feed guards / accessible stop", "Reduce access to heat, pinch points and blade", "Facility-designed guards, stop, safe jam/cooldown procedure", 1, None, "Quote required", "Yes", "Must be reviewed against actual machine."],
        ["Output handling", "Supported glass and laminate collection", "Keep separated streams supported and identifiable", "Two stable trays/supports; prevent free fall, impact and cross-contamination", 2, None, "Estimate/host stock", "Yes", "Material compatibility to be checked."],
        ["Measurement", "Dual-channel thermometry and suitable probes", "Record tool and interface temperatures separately", "Probe range, attachment, response time and calibration/check suited to host process", 1, None, "Local quote/borrow required", "Yes", "No price verified in accessible listing."],
        ["Measurement", "Plug-in AC energy meter", "Exploratory whole-run energy logging if load compatible", "Rated for approved supply/load; not a calibrated power analyzer", 1, 1499, "Reference listing checked 2026-10-03: https://www.amicikart.com/products/amicisense-digital-socket-power-meter-energy-monitor-for-voltage-amps-frequency-test-16a-capacity-with-real-time-cost-calculation", "Yes", "Use only if facility approves; borrow a calibrated analyzer if available."],
        ["Measurement", "Bench/platform scale", "Weigh feed and separated outputs", "Resolution/platform size appropriate to coupon and stream mass; checked/calibrated", 1, 11682, "Lower listed configuration reference checked 2026-10-03: https://www.hindustanscale.com/product/bluetooth-enabled-customized-scale/", "Yes", "May need a smaller-resolution balance for coupon/debris mass."],
        ["Measurement", "Feed-speed/time measurement", "Measure process and transfer timing", "Defined start/stop event; speed method suits host feed", 1, None, "Borrow/quote required", "Yes", "Simple stopwatch is acceptable only for stated resolution."],
        ["Optional", "Force/load measurement", "Characterize peeling or drive load where relevant", "Range and calibration compatible with the setup", 1, None, "Optional borrow/quote", "No", "Do not add unless force is part of the research question."],
        ["Safety / operations", "PPE, signage, cleanup and approved waste containers", "Facility-specified protection and controlled housekeeping", "Selected by EHS after material and process review", 1, None, "Quote/host stock required", "Yes", "No generic PPE specification replaces facility review."],
        ["Facility", "Supervised thermal station access and EHS review", "Provide safe equipment, operator and waste pathway", "Written facility acceptance, scope and access terms", 1, None, "Quote/access fee unknown", "Yes", "Required for active PV thermal trials."],
    ]
    add_rows(ws, rows)
    ws2 = wb.create_sheet("Boundary and notes")
    ws2.append(["Topic", "Current statement"])
    ws2.append(["Stage 3", "Thermal treatment/delamination; working reference is guarded fixed hot knife for front glass separation."])
    ws2.append(["First expected output", "Sheet glass plus cell/EVA/backsheet laminate. This is not EVA-free cell material."])
    ws2.append(["Stage 4", "Silver removal/recovery. Method and feed specification remain open."])
    ws2.append(["No trials", "No Agastya hardware build, thermal trial, energy measurement, silver-removal trial or assay is documented."])
    ws2.append(["Known priced references", "Energy meter ₹1,499 + scale ₹11,682 = ₹13,181 partial instrument reference; excludes core machine, thermometer/probes, facility, safety, calibration, delivery and supplies."])
    ws2.append(["Procurement gate", "Do not purchase until host dimensions, approved station, rated electrical supply, guards, ventilation, supervision and waste requirements are known."])
    ws2.column_dimensions["A"].width = 28
    ws2.column_dimensions["B"].width = 110
    for row in ws2.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    for cell in ws2[1]:
        cell.font = Font(bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY)
    wb.save(ROOT / "Stage_3_Bill_of_Materials.xlsx")


def make_cost_model():
    wb = Workbook()
    ws = wb.active
    ws.title = "Reference costs"
    headers = ["Cost item", "Low INR", "High INR", "Basis/status", "Source / limitation"]
    base_sheet(ws, "Stage 3 Thermal — Cost Model", "No complete prototype estimate is defensible until a host supplies station, safety, facility and calibration quotes. Blank values mean quote required, not zero.", headers, {"Cost item": 36, "Low INR": 16, "High INR": 16, "Basis/status": 40, "Source / limitation": 90})
    rows = [
        ["Plug-in energy meter", 1499, 1499, "Reference price checked 2026-10-03", "AmiciKart 16 A listing; exploratory only if compatible and approved. Not a calibrated lab analyzer."],
        ["Bench/platform scale", 11682, 11682, "Lower listing configuration checked 2026-10-03", "Hindustan Scale; resolution/platform suitability and current price require verification."],
        ["Dual-channel thermometer and probes", None, None, "Quote/borrow required", "No accessible price confirmed; probe type, range and check/calibration required."],
        ["Hot knife, heater/control, independent limit", None, None, "Host-specific quote required", "No tool or wiring design selected; must match approved facility and feed geometry."],
        ["Fixture/feed support and guards", None, None, "Host-specific fabrication quote required", "Dimensions and risk controls not yet defined."],
        ["Facility access, operator, EHS review", None, None, "Quote/access terms required", "Not confirmed in workspace."],
        ["Consumables, delivery, calibration, waste", None, None, "Quote required", "Do not assume these are zero."],
        ["Known priced reference subtotal", "=SUM(B5:B6)", "=SUM(C5:C6)", "Partial only", "Excludes all quote-required core costs and is not a Stage 3 machine total."],
    ]
    add_rows(ws, rows)
    ws2 = wb.create_sheet("Scenarios")
    headers2 = ["Scenario", "Scope", "Priced equipment subtotal INR", "Thermal station/facility INR", "Calibration/safety/waste INR", "Total status", "What it can demonstrate"]
    base_sheet(ws2, "Development Scenarios", "Scenario totals stay open until written quotes and host inventory are available.", headers2, {"Scenario": 30, "Scope": 45, "Priced equipment subtotal INR": 25, "Thermal station/facility INR": 25, "Calibration/safety/waste INR": 25, "Total status": 25, "What it can demonstrate": 65})
    add_rows(ws2, [
        ["A — cold fixture", "Support, guides, templates and data workflow", None, None, None, "Local material/quote required", "Handling and interface only; no thermal or PV performance claim."],
        ["B — supervised coupon study", "Host hot knife, guarded coupon feed, temperature/energy/mass logging", None, None, None, "Quote required", "Thermal separation quality on specified coupons if trial is approved."],
        ["C — research extension", "Repeatable feed plus separate roller/heat-reuse study", None, None, None, "Quote required after B", "Roller effect and heat reuse only after a defined outcome and baseline."],
    ])
    wb.save(ROOT / "Stage_3_Prototype_Cost_Model.xlsx")


def make_references():
    wb = Workbook()
    ws = wb.active
    ws.title = "Evidence register"
    headers = ["ID", "Source", "Year", "Evidence type", "Claim / result", "Relevance to Stage 3", "Quality / transfer limit", "Link"]
    base_sheet(ws, "Stage 3 Thermal Evidence Register", "Literature values belong to the cited equipment and material. They are not Agastya measurements or recommended setpoints.", headers, {"ID": 10, "Source": 48, "Year": 10, "Evidence type": 28, "Claim / result": 55, "Relevance to Stage 3": 46, "Quality / transfer limit": 58, "Link": 64})
    rows = [
        ["T1", "Frischknecht, Komoto & Doi, IEA PVPS Task 12-25:2023", 2023, "Pilot process LCA", "Hot-knife glass separation; about 50 s/module; 0.035 kWh/kg for reported treatment system.", "Process benchmark and boundary example.", "Fair data quality; value covers broader take-back/hot-knife treatment, not isolated Stage 3 energy.", "https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf"],
        ["T2", "NPC Incorporated, Solar Panel Recycling Machine", None, "Manufacturer description", "Describes glass separator at about 60 s/panel and 300 °C knife; separate EVA scraping equipment.", "Confirms glass separation and EVA removal are distinct operations.", "Supplier claim; not independent or an Agastya specification.", "https://www.npcgroup.net/eng/solarproduct/dismantling"],
        ["T3", "NEDO/NPC development account", 2025, "Technology development account", "Discusses fixed-knife/feed development and edge-entry challenges.", "Informs conceptual station blocks.", "Development description is not a ready-to-copy drawing or validation for Agastya.", "https://webmagazine.nedo.go.jp/practical-realization/articles/202503NPC/"],
        ["T4", "Saitta et al., Effect of Temperature on Glass Delamination", 2026, "Peer-reviewed coupon study", "100/140 °C heating for 60 min followed by mechanical peel; condition-specific coupon results.", "Alternative slow thermal-softening comparison.", "Different heating/peel method and material; not a sub-minute process claim.", "https://doi.org/10.3390/green1010002"],
        ["T5", "Pyrolysis mechanism and recycling strategy of end-of-life PV modules", 2023, "Thermal decomposition study", "Reports EVA decomposition stages at substantially higher temperatures than softening-assisted separation.", "Separates pyrolysis from hot-knife delamination.", "Different objective and process; not an Agastya operating target.", "https://doi.org/10.1016/j.polymdegradstab.2023.110545"],
        ["P1", "AGASTYA STAGE3_BUILD_PLAN.md and STAGE3_THERMAL_DEVELOPMENT.md", 2026, "Project design/research note", "Fixed guarded hot knife; first output glass plus cell/EVA/backsheet laminate; no thermal validation.", "Current Stage 3 prototype boundary.", "Planning documents; no equipment, trial or measured result.", "../Build Files and Steps/Stage 3/STAGE3_BUILD_PLAN.md"],
        ["P2", "AGASTYA_ARCHITECTURE.md", 2026, "Project architecture", "Stage 3 thermal; Stage 4 silver removal/recovery.", "Controls current numbering.", "Stage 4 method and interface remain open.", "../AGASTYA_ARCHITECTURE.md"],
    ]
    add_rows(ws, rows)
    wb.save(ROOT / "Stage_3_References_and_Evidence_Register.xlsx")


def make_test_template():
    wb = Workbook()
    ws = wb.active
    fields = ["trial_id", "date_time", "operator", "facility", "source_panel_id", "coupon_id", "module_technology", "construction", "coupon_length_mm", "coupon_width_mm", "input_mass_g", "ambient_temp_C", "blade_setpoint_C", "blade_measured_temp_C", "interface_temp_C", "feed_speed_mm_s", "cut_length_mm", "warmup_time_s", "process_time_s", "transfer_delay_s", "energy_watt_hour", "instrument_ids", "calibration_or_check_refs", "glass_mass_g", "laminate_mass_g", "debris_mass_g", "mass_closure_percent", "glass_damage_score", "separation_completeness_score", "cell_damage_notes", "backsheet_condition", "EVA_residue_location_or_measure", "photo_refs", "deviation_or_hold", "safety_review_ref", "notes"]
    base_sheet(ws, "Stage 3 Thermal Trial Data Template", "Blank template only. Do not enter literature values as trial observations. Stage 3 thermal; Stage 4 silver removal. Active trials require facility approval.", fields, {field: (20 if len(field) < 24 else 28) for field in fields})
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:{get_column_letter(len(fields))}4"
    ws.row_dimensions[4].height = 66
    for i, field in enumerate(fields, 1):
        ws.cell(4, i).alignment = Alignment(text_rotation=45, wrap_text=True, horizontal="center", vertical="center")
    ws2 = wb.create_sheet("Field guide")
    ws2.append(["Field", "Definition / entry rule"])
    guides = [
        ("trial_id", "Unique ID; no data row in this template is an experiment."),
        ("source_panel_id / coupon_id", "Maintain parent-child sample lineage; record unknown module construction as unknown."),
        ("blade_setpoint_C / blade_measured_temp_C / interface_temp_C", "Separate the controller setting, actual tool reading, and material/interface reading."),
        ("energy_watt_hour", "Metered energy over the defined boundary; note whether warm-up and standby are included."),
        ("mass closure", "Use input mass and all collected output streams; document withdrawn samples and losses."),
        ("quality scores", "Define ordinal rubric before trial; do not infer EVA-free purity from visual inspection."),
        ("deviation_or_hold", "Record failed, interrupted, or unsafe runs; preserve raw observations."),
        ("Stage 4 interface", "Record stream identity and condition only. Silver-removal performance is measured separately in Stage 4."),
    ]
    for row in guides:
        ws2.append(row)
    ws2.column_dimensions["A"].width = 34
    ws2.column_dimensions["B"].width = 110
    for cell in ws2[1]:
        cell.font = Font(bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY)
    for row in ws2.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(ROOT / "Stage_3_Test_Data_Template.xlsx")


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    make_bom()
    make_cost_model()
    make_references()
    make_test_template()
    print("Built four Stage 3 thermal planning workbooks.")

