#!/usr/bin/env python3
"""Create a simple R12 DXF plan view from the illustrative Stage 2 reach screen."""
from __future__ import annotations
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_IN = HERE / "simulation_outputs" / "perimeter_task_points.csv"
DXF_OUT = HERE / "simulation_outputs" / "concept_workcell_plan.dxf"

class Dxf:
    def __init__(self):
        self.entities = []
    def raw(self, *pairs):
        self.entities.extend(pairs)
    def line(self, layer, x1, y1, x2, y2):
        self.raw((0,"LINE"),(8,layer),(10,x1),(20,y1),(30,0.0),(11,x2),(21,y2),(31,0.0))
    def circle(self, layer, x, y, r):
        self.raw((0,"CIRCLE"),(8,layer),(10,x),(20,y),(30,0.0),(40,r))
    def text(self, layer, x, y, height, label):
        self.raw((0,"TEXT"),(8,layer),(10,x),(20,y),(30,0.0),(40,height),(1,label))
    def polyline(self, layer, points, closed=True):
        self.raw((0,"POLYLINE"),(8,layer),(66,1),(70,1 if closed else 0))
        for x,y in points:
            self.raw((0,"VERTEX"),(8,layer),(10,x),(20,y),(30,0.0))
        self.raw((0,"SEQEND"),(8,layer))
    def write(self, path):
        layers = [
            ("0",7),("PANEL",7),("SUPPORTS",8),("ARM_BASE",1),
            ("REACH_1500",30),("REACH_2000",6),("TASK_POINTS",5),
            ("DIMENSIONS",2),("NOTES",7)
        ]
        out = [0,"SECTION",2,"HEADER",9,"$ACADVER",1,"AC1009",0,"ENDSEC",
               0,"SECTION",2,"TABLES",0,"TABLE",2,"LAYER",70,len(layers)]
        for name,color in layers:
            out.extend([0,"LAYER",2,name,70,0,62,color,6,"CONTINUOUS"])
        out.extend([0,"ENDTAB",0,"ENDSEC",0,"SECTION",2,"ENTITIES"])
        for code,value in self.entities:
            out.extend([code, value])
        out.extend([0,"ENDSEC",0,"EOF"])
        with path.open("w",encoding="ascii",newline="\n") as f:
            for value in out:
                f.write(str(value)+"\n")

def main():
    rows = list(csv.DictReader(CSV_IN.open(newline="",encoding="utf-8-sig")))
    # Keep the same illustrative coordinate frame as the reach-screen model.
    half_l, half_w, base_y = 2278.0/2, 1134.0/2, -(1134.0/2+300.0)
    d = Dxf()
    d.polyline("PANEL",[(-half_l,-half_w),(half_l,-half_w),(half_l,half_w),(-half_l,half_w)])
    d.text("NOTES",-half_l,half_w+110,70,"STAGE 2 WORKCELL PLAN - CONCEPT ONLY - MILLIMETRES")
    d.text("NOTES",-half_l,half_w+30,45,"Illustrative panel 2278 x 1134; fixed base 300 beyond near long edge")
    d.text("NOTES",-half_l,-half_w-190,45,"No robot links, IK, tool pose, collision, payload, force, guarding, or fabrication detail")
    d.text("NOTES",-half_l,-half_w-250,45,"Reach circles are scalar top-view screens only; panel and station dimensions are assumptions")
    # Two simple support rails under the panel are layout placeholders, not sized parts.
    d.line("SUPPORTS",-half_l,-180,half_l,-180)
    d.line("SUPPORTS",-half_l,180,half_l,180)
    d.text("NOTES",-half_l+30,195,38,"illustrative support rails")
    d.circle("REACH_1500",0,base_y,1500)
    d.circle("REACH_2000",0,base_y,2000)
    d.polyline("ARM_BASE",[(-150,base_y-150),(150,base_y-150),(150,base_y+150),(-150,base_y+150)])
    d.circle("ARM_BASE",0,base_y,55)
    d.text("NOTES",185,base_y,45,"candidate arm-base projection")
    for row in rows:
        d.circle("TASK_POINTS",float(row["x_mm"]),float(row["y_mm"]),14)
    # Dimension lines and extension ticks for panel envelope.
    dim_y=half_w+245
    d.line("DIMENSIONS",-half_l,dim_y,half_l,dim_y)
    for x in (-half_l,half_l): d.line("DIMENSIONS",x,half_w,x,dim_y+55)
    d.text("DIMENSIONS",-180,dim_y+25,50,"2278 mm (illustrative)")
    dim_x=half_l+230
    d.line("DIMENSIONS",dim_x,-half_w,dim_x,half_w)
    for y in (-half_w,half_w): d.line("DIMENSIONS",half_l,y,dim_x+55,y)
    d.text("DIMENSIONS",dim_x+35,-65,48,"1134 mm")
    d.write(DXF_OUT)
    # Basic output accounting for a reproducible creation record.
    text=DXF_OUT.read_text(encoding="ascii")
    print(f"DXF={DXF_OUT}")
    print(f"sampled_task_points={len(rows)}")
    print(f"entities={text.count(chr(10)+'0'+chr(10))}")
    print(f"bytes={DXF_OUT.stat().st_size}")

if __name__ == "__main__":
    main()
