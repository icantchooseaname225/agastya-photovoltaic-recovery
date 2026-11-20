"""Generate ASCII DXF R12 concept sheets and SVG previews for AutoCAD review."""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE2 = HERE.parents[1]
POINTS = STAGE2 / "simulation_outputs" / "perimeter_task_points.csv"
OUT_ARM = HERE / "AGASTYA_STAGE2_ARM_CONCEPT.dxf"
OUT_ELEC = HERE / "AGASTYA_STAGE2_ELECTRICAL_ARCHITECTURE.dxf"
OUT_ARM_SVG = HERE / "AGASTYA_STAGE2_ARM_CONCEPT_PREVIEW.svg"
OUT_ELEC_SVG = HERE / "AGASTYA_STAGE2_ELECTRICAL_ARCHITECTURE_PREVIEW.svg"


class Dxf:
    def __init__(self):
        self.entities: list[tuple[int, object]] = []

    def raw(self, *pairs):
        self.entities.extend(pairs)

    def line(self, layer, x1, y1, x2, y2):
        self.raw((0, "LINE"), (8, layer), (10, x1), (20, y1), (30, 0.0),
                 (11, x2), (21, y2), (31, 0.0))

    def circle(self, layer, x, y, radius):
        self.raw((0, "CIRCLE"), (8, layer), (10, x), (20, y), (30, 0.0), (40, radius))

    def text(self, layer, x, y, height, value):
        # Keep R12 DXF ASCII-safe and use single-line labels.
        value = value.encode("ascii", "replace").decode("ascii")
        self.raw((0, "TEXT"), (8, layer), (10, x), (20, y), (30, 0.0), (40, height), (1, value))

    def rect(self, layer, x1, y1, x2, y2):
        self.polyline(layer, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], True)

    def polyline(self, layer, points, closed=False):
        self.raw((0, "POLYLINE"), (8, layer), (66, 1), (70, 1 if closed else 0))
        for x, y in points:
            self.raw((0, "VERTEX"), (8, layer), (10, x), (20, y), (30, 0.0))
        self.raw((0, "SEQEND"))

    def write(self, path: Path, layers):
        out = [0, "SECTION", 2, "HEADER", 9, "$ACADVER", 1, "AC1009",
               9, "$INSUNITS", 70, 4, 0, "ENDSEC",
               0, "SECTION", 2, "TABLES", 0, "TABLE", 2, "LAYER", 70, len(layers)]
        for name, color in layers:
            out.extend([0, "LAYER", 2, name, 70, 0, 62, color, 6, "CONTINUOUS"])
        out.extend([0, "ENDTAB", 0, "ENDSEC", 0, "SECTION", 2, "ENTITIES"])
        for code, value in self.entities:
            out.extend([code, value])
        out.extend([0, "ENDSEC", 0, "EOF"])
        path.write_text("\n".join(str(value) for value in out) + "\n", encoding="ascii")


def dimension(d, layer, x1, y1, x2, y2, label, tx, ty, h=38):
    d.line(layer, x1, y1, x2, y2)
    d.line(layer, x1 - 18, y1 - 18, x1 + 18, y1 + 18)
    d.line(layer, x2 - 18, y2 - 18, x2 + 18, y2 + 18)
    d.text(layer, tx, ty, h, label)


def add_arm_sheet(d, points):
    layer_panel, layer_arm, layer_reach, layer_dim, layer_note, layer_support = (
        "PANEL", "ARM", "REACH", "DIM", "NOTES", "SUPPORTS"
    )
    half_l, half_w = 1139.0, 567.0
    base_x, base_y = 0.0, -867.0
    d.text(layer_note, -1500, 1450, 76, "AGASTYA STAGE 2 ARM ENVELOPE - CONCEPT ONLY - ALL UNITS MM")
    d.text(layer_note, -1500, 1350, 42, "Illustrative panel 2278 x 1134; 300 mm base stand-off; not measured hardware")
    d.text(layer_note, -1500, 1285, 42, "Four-axis articulated envelope: base yaw, shoulder pitch, elbow pitch, wrist/tool pitch")
    d.polyline(layer_panel, [(-half_l, -half_w), (half_l, -half_w), (half_l, half_w), (-half_l, half_w)], True)
    d.text(layer_panel, -500, 0, 54, "SUPPORTED MODULE - FIXTURE CARRIES PANEL LOAD")
    d.line(layer_support, -half_l, -180, half_l, -180)
    d.line(layer_support, -half_l, 180, half_l, 180)
    d.text(layer_support, -half_l + 40, 200, 34, "illustrative support rail lines only")
    for radius in (1500.0, 2000.0):
        d.circle(layer_reach, base_x, base_y, radius)
    d.rect(layer_arm, base_x - 175, base_y - 175, base_x + 175, base_y + 175)
    d.circle(layer_arm, base_x, base_y, 55)
    d.text(layer_arm, 210, base_y - 25, 38, "arm-base projection")
    # Straightened neutral-pose reach demonstration; it does not represent a path.
    d.line(layer_arm, 0, base_y, 0, base_y + 1100)
    d.line(layer_arm, 0, base_y + 1100, 0, base_y + 2000)
    d.circle(layer_arm, 0, base_y + 1100, 115)
    d.circle(layer_arm, 0, base_y + 2000, 82)
    d.text(layer_arm, 70, base_y + 520, 35, "1100 upper-arm envelope")
    d.text(layer_arm, 70, base_y + 1450, 35, "900 forearm envelope")
    d.text(layer_reach, 700, base_y - 1490, 42, "1500 mm scalar screen")
    d.text(layer_reach, 700, base_y - 2020, 42, "2000 mm scalar screen")
    for row in points:
        d.circle("TASKS", float(row["x_mm"]), float(row["y_mm"]), 13)
    dimension(d, layer_dim, -half_l, half_w + 140, half_l, half_w + 140,
              "2278 mm illustrative", -240, half_w + 170)
    dimension(d, layer_dim, half_l + 170, -half_w, half_l + 170, half_w,
              "1134 mm", half_l + 215, -25)
    d.text(layer_note, -1500, -1050, 40, "Max sampled far-corner radius: 1831.3 mm; 2.0 m radius leaves 168.7 mm scalar margin")
    d.text(layer_note, -1500, -1110, 40, "Margin excludes tool projection, joint limits, pose, link collisions, deflection and guarding")
    d.text(layer_note, -1500, -1170, 40, "Do not manufacture or select actuators from this layout")

    # Side view offset to the right; dimensions follow the Fusion envelope script.
    ox, floor = 3700.0, -500.0
    shoulder_z = 730.0
    d.text(layer_note, ox, 1450, 58, "SIDE ELEVATION - GEOMETRY ENVELOPES")
    d.line(layer_dim, ox - 400, floor, ox + 2600, floor)
    d.text(layer_note, ox - 300, floor - 90, 38, "floor datum (illustrative)")
    d.rect(layer_arm, ox - 175, floor, ox + 175, floor + 20)
    d.rect(layer_arm, ox - 80, floor + 20, ox + 80, floor + 670)
    d.circle(layer_arm, ox, shoulder_z, 115)
    d.rect(layer_arm, ox, shoulder_z - 50, ox + 1100, shoulder_z + 50)
    d.circle(layer_arm, ox + 1100, shoulder_z, 90)
    d.rect(layer_arm, ox + 1100, shoulder_z - 40, ox + 2000, shoulder_z + 40)
    d.circle(layer_arm, ox + 2000, shoulder_z, 67)
    d.rect(layer_arm, ox + 2060, shoulder_z - 50, ox + 2180, shoulder_z + 50)
    d.line(layer_arm, ox + 2180, shoulder_z, ox + 2180, 0)
    d.text(layer_arm, ox + 2200, shoulder_z - 100, 34, "tool approach / tool absent")
    dimension(d, layer_dim, ox, shoulder_z + 260, ox + 1100, shoulder_z + 260,
              "1100 upper arm", ox + 330, shoulder_z + 285, 38)
    dimension(d, layer_dim, ox + 1100, shoulder_z + 260, ox + 2000, shoulder_z + 260,
              "900 forearm", ox + 1390, shoulder_z + 285, 38)
    d.text(layer_note, ox, -750, 38, "Shoulder centre z=730 mm from current script envelope; no IK or load validation")

    # Interface sketches: indicative bolt circles/patterns only.
    dx, dy = 0.0, -2100.0
    d.text(layer_note, dx, dy + 430, 56, "DETAIL A - BASE PLATE OUTLINE (NOT A DRILLING RELEASE)")
    d.rect(layer_arm, dx, dy, dx + 350, dy + 350)
    for x in (dx + 35, dx + 315):
        for y in (dy + 35, dy + 315):
            d.circle(layer_dim, x, y, 6)
    d.text(layer_note, dx, dy - 65, 34, "350 x 350 x 20 envelope; four 12 mm hole placeholders at 280 mm pitch")
    dx2 = 1500.0
    d.text(layer_note, dx2, dy + 430, 56, "DETAIL B - TOOL FLANGE PLACEHOLDER")
    d.rect(layer_arm, dx2, dy, dx2 + 120, dy + 100)
    for x in (dx2 + 20, dx2 + 100):
        for y in (dy + 20, dy + 80):
            d.circle(layer_dim, x, y, 4)
    d.text(layer_note, dx2, dy - 65, 34, "120 x 100 x 16 envelope; 8 mm hole placeholders; actual wrist unselected")
    dx3 = 3100.0
    d.text(layer_note, dx3, dy + 430, 56, "DETAIL C - LINK SECTION ENVELOPES")
    d.rect(layer_arm, dx3, dy, dx3 + 120, dy + 100)
    d.rect(layer_arm, dx3 + 220, dy, dx3 + 320, dy + 80)
    d.text(layer_note, dx3, dy - 65, 34, "Upper 120 x 100; forearm 100 x 80; solid display shapes, no wall thickness")


def add_box(d, x, y, w, h, title, lines):
    d.rect("BLOCKS", x, y, x + w, y + h)
    d.text("TEXT", x + 15, y + h - 28, 20, title)
    for idx, line in enumerate(lines):
        d.text("TEXT", x + 15, y + h - 55 - idx * 24, 16, line)


def add_electrical_sheet(d):
    d.text("TEXT", 0, 520, 40, "AGASTYA STAGE 2 ELECTRICAL ARCHITECTURE - CONCEPT ONLY - NOT A WIRING RELEASE")
    d.text("TEXT", 0, 475, 22, "Production cell architecture (top): OEM robot controller and safety system required; part numbers unselected")
    add_box(d, 0, 260, 170, 115, "FACILITY POWER", ["qualified supply + isolation", "rating pending robot selection"])
    add_box(d, 250, 260, 190, 115, "SAFETY RELAY / PLC", ["guard + dual-channel E-stop", "STO/contactors per OEM data"])
    add_box(d, 520, 260, 195, 115, "ROBOT CONTROL", ["controller + joint drives", "manufacturer-selected system"])
    add_box(d, 805, 260, 180, 115, "4-AXIS ARM", ["base / shoulder / elbow / wrist", "payload and axes not selected"])
    d.line("POWER", 170, 315, 250, 315)
    d.line("SAFETY", 170, 285, 250, 285)
    d.line("POWER", 440, 315, 520, 315)
    d.line("SIGNAL", 715, 315, 805, 315)
    add_box(d, 0, 40, 170, 115, "E-STOP + GUARDS", ["hardwired safety devices", "ratings and PL/SIL TBD"])
    add_box(d, 250, 40, 190, 115, "AGASTYA-EYE", ["inspection / provenance only", "never a safety-rated input"])
    add_box(d, 520, 40, 195, 115, "CELL SEQUENCE", ["reviewed discrete requests", "no EYE-to-servo bypass"])
    d.line("SAFETY", 85, 155, 85, 260)
    d.line("SIGNAL", 170, 95, 520, 95)
    d.line("SIGNAL", 440, 95, 520, 95)
    d.text("NOTES", 0, 5, 18, "E-stop/guard chain is separate from EYE, application UI, and normal motion commands.")

    d.text("TEXT", 0, -110, 28, "BENCH DEMONSTRATOR ONLY (separate from process cell; unloaded tabletop fixture required)")
    add_box(d, 0, -345, 170, 120, "5 V LOGIC", ["Arduino Mega", "USB or regulated logic"])
    add_box(d, 250, -345, 180, 120, "PWM SIGNAL", ["PCA9685 optional", "signal only; no servo power"])
    add_box(d, 510, -345, 180, 120, "SERVO RAIL", ["separately rated DC supply", "voltage/current TBD"])
    add_box(d, 770, -345, 215, 120, "4 SERVO JOINTS", ["J1 base, J2 shoulder", "J3 elbow, J4 wrist"])
    d.line("SIGNAL", 170, -280, 250, -280)
    d.line("SIGNAL", 430, -280, 770, -280)
    d.line("POWER", 690, -320, 770, -320)
    add_box(d, 250, -525, 180, 110, "NC E-STOP LOOP", ["hardware relay coil", "GPIO is status only"])
    add_box(d, 510, -525, 180, 110, "HARDWARE CUT", ["rated DC power device", "voltage/current TBD"])
    add_box(d, 770, -525, 215, 110, "LIMIT INPUTS", ["two per axis, NC", "software plus stops"])
    d.line("SAFETY", 430, -470, 510, -470)
    d.line("POWER", 600, -415, 600, -345)
    d.text("NOTES", 700, -400, 16, "E-stop drops external servo rail")
    d.text("NOTES", 770, -560, 16, "see Mega pin map CSV")
    d.text("NOTES", 0, -590, 18, "Cutting servo power can let a gravity axis fall. Use unloaded arm, catch/support, guarding and adult review.")
    d.text("NOTES", 0, -625, 18, "This is a functional architecture drawing, not a certified safety circuit or mains-wiring instruction.")


def write_svg_arm(path, points):
    # SVG preview of the top-view envelope; DXF remains the AutoCAD drawing.
    scale = 0.11
    width, height = 940, 700
    cx, cy = 470, 350
    def sx(x): return cx + x * scale
    def sy(y): return cy - y * scale
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
              '<rect width="100%" height="100%" fill="#fff"/>',
              '<style>text{font-family:Arial,sans-serif;fill:#223;}.title{font-size:17px;font-weight:bold}.small{font-size:12px}.tiny{font-size:9px}</style>',
              '<text x="20" y="28" class="title">AGASTYA Stage 2 arm envelope — plan view (concept only)</text>',
              '<text x="20" y="48" class="small">2278 × 1134 mm assumed panel; 300 mm stand-off; nominal 2 m reach circle</text>']
    for rad, color, dash in [(1500, "#b99a34", "5 4"), (2000, "#2b799c", "")]:
        chunks.append(f'<circle cx="{sx(0)}" cy="{sy(-867)}" r="{rad*scale}" fill="none" stroke="{color}" stroke-width="1.4" stroke-dasharray="{dash}"/>')
    x1, y1, x2, y2 = sx(-1139), sy(567), sx(1139), sy(-567)
    chunks.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="#e9f1f5" stroke="#31465a" stroke-width="2"/>')
    chunks.append(f'<text x="{sx(-650)}" y="{sy(0)}" class="small">supported PV module</text>')
    for row in points:
        x, y = sx(float(row['x_mm'])), sy(float(row['y_mm']))
        chunks.append(f'<circle cx="{x}" cy="{y}" r="2" fill="#b64242"/>')
    bx, by = sx(0), sy(-867)
    chunks.append(f'<rect x="{bx-9}" y="{by-9}" width="18" height="18" fill="#b54c37" stroke="#5d2520"/>')
    # Show straightened link envelope, not a robot trajectory.
    chunks.append(f'<line x1="{bx}" y1="{by}" x2="{sx(0)}" y2="{sy(233)}" stroke="#8d4533" stroke-width="9"/>')
    chunks.append(f'<line x1="{sx(0)}" y1="{sy(233)}" x2="{sx(0)}" y2="{sy(1133)}" stroke="#d27946" stroke-width="8"/>')
    chunks.append(f'<circle cx="{sx(0)}" cy="{sy(233)}" r="{115*scale}" fill="#fff" stroke="#543" stroke-width="2"/>')
    chunks.append(f'<circle cx="{bx}" cy="{by}" r="{82*scale}" fill="#fff" stroke="#543" stroke-width="2"/>')
    chunks.append('<text x="22" y="628" class="small">Straight arm pose is illustrative. Reach circle is a 2D distance screen, not validated motion.</text>')
    chunks.append('<text x="22" y="649" class="tiny">No link collisions, IK, tool pose, load/force, guarding, material or actuator selection.</text>')
    chunks.append('</svg>')
    path.write_text("\n".join(chunks), encoding="utf-8")


def write_svg_electrical(path):
    width, height = 1100, 620
    items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#fff"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#223}.title{font-size:18px;font-weight:bold}.label{font-size:13px}.small{font-size:11px}.box{fill:#f2f4f6;stroke:#475569;stroke-width:1.5}</style>',
             '<text x="24" y="30" class="title">AGASTYA Stage 2 — two distinct electrical scopes</text>',
             '<text x="24" y="58" class="label">Process cell (upper): safety-rated robot controller architecture; all devices TBD</text>']
    boxes = [
        (25,100,190,84,"Facility supply",["isolation / ratings TBD"]),
        (285,100,200,84,"Safety relay / PLC",["guard + E-stop", "STO per OEM design"]),
        (555,100,210,84,"Robot controller",["joint drives / OEM selected"]),
        (835,100,220,84,"Four-axis arm",["payload and axes TBD"]),
        (25,235,190,84,"E-stop + guard",["hardwired, reviewed"]),
        (285,235,200,84,"AGASTYA-EYE",["inspection only", "not a safety input"]),
        (555,235,210,84,"Cell sequence",["reviewed discrete request"]),
    ]
    for x,y,w,h,title,lines in boxes:
        items.append(f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>')
        items.append(f'<text x="{x+12}" y="{y+25}" class="label">{escape(title)}</text>')
        for j,line in enumerate(lines): items.append(f'<text x="{x+12}" y="{y+47+j*18}" class="small">{escape(line)}</text>')
    for x1,y1,x2,y2,color in [(215,142,285,142,"#a34b36"),(485,142,555,142,"#a34b36"),(765,142,835,142,"#334155"),(120,184,120,235,"#a34b36"),(215,277,555,277,"#357a68"),(485,277,555,277,"#357a68")]:
        items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"/>')
    items.append('<text x="24" y="355" class="label">Low-load classroom demonstrator only (lower): use an unloaded guarded fixture; not for PV process tasks</text>')
    items.extend(['<rect class="box" x="25" y="390" width="210" height="88" rx="4"/>','<text x="38" y="420" class="label">Arduino Mega</text>','<text x="38" y="444" class="small">logic / manual jog scaffold</text>',
                  '<rect class="box" x="315" y="390" width="210" height="88" rx="4"/>','<text x="328" y="420" class="label">PCA9685 (optional)</text>','<text x="328" y="444" class="small">PWM signals only</text>',
                  '<rect class="box" x="610" y="390" width="210" height="88" rx="4"/>','<text x="623" y="420" class="label">Separate servo supply</text>','<text x="623" y="444" class="small">voltage/current TBD</text>',
                  '<rect class="box" x="900" y="390" width="155" height="88" rx="4"/>','<text x="913" y="420" class="label">J1–J4 servos</text>','<text x="913" y="444" class="small">light demo only</text>'])
    for x1,x2,y,color in [(235,315,434,"#334155"),(525,900,434,"#334155"),(820,900,455,"#a34b36")]:
        items.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="2"/>')
    items.append('<text x="25" y="520" class="small">E-stop NC contact should also drop a suitably rated servo-power device; GPIO reports state only.</text>')
    items.append('<text x="25" y="540" class="small">Power removal may let a gravity axis fall. Add a mechanical catch/support and adult-reviewed guards.</text>')
    items.append('<text x="25" y="580" class="small">Architecture sketch only — not a certified safety circuit, electrical schematic or mains-wiring guide.</text>')
    items.append('</svg>')
    path.write_text("\n".join(items), encoding="utf-8")


def main():
    with POINTS.open(newline="", encoding="utf-8-sig") as stream:
        points = list(csv.DictReader(stream))
    arm = Dxf()
    add_arm_sheet(arm, points)
    arm.write(OUT_ARM, [("0", 7), ("PANEL", 7), ("SUPPORTS", 8), ("ARM", 1),
                        ("REACH", 6), ("TASKS", 5), ("DIM", 2), ("NOTES", 7)])
    elec = Dxf()
    add_electrical_sheet(elec)
    elec.write(OUT_ELEC, [("0", 7), ("BLOCKS", 7), ("TEXT", 7), ("POWER", 1),
                          ("SAFETY", 1), ("SIGNAL", 5), ("NOTES", 8)])
    write_svg_arm(OUT_ARM_SVG, points)
    write_svg_electrical(OUT_ELEC_SVG)
    print(f"arm_dxf={OUT_ARM}")
    print(f"electrical_dxf={OUT_ELEC}")
    print(f"task_points={len(points)}")
    print(f"arm_entities={len(arm.entities)} electrical_entities={len(elec.entities)}")


if __name__ == "__main__":
    main()
