from pathlib import Path
from urllib.parse import unquote
import csv,re

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/"link_check_results.csv"
pattern=re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
rows=[]
skip={"99_Archive","Agastya Thermal/.stage3-build/node_modules"}
for md in ROOT.rglob("*.md"):
    rel=md.relative_to(ROOT)
    if rel.parts and (rel.parts[0]=="99_Archive" or "node_modules" in rel.parts or "__pycache__" in rel.parts):
        continue
    try: text=md.read_text(encoding="utf-8-sig")
    except Exception as exc:
        rows.append([str(rel),"","READ_ERROR",str(exc)]); continue
    for raw in pattern.findall(text):
        target=raw.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://","https://","mailto:","tel:","data:")):
            continue
        target=unquote(target.split("#",1)[0])
        if not target:
            continue
        resolved=(md.parent/target).resolve()
        status="OK" if resolved.exists() else "BROKEN"
        rows.append([str(rel),raw,status,str(resolved.relative_to(ROOT)) if str(resolved).startswith(str(ROOT)) else str(resolved)])
with OUT.open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["markdown_file","link_target","status","resolved_target"]); w.writerows(rows)
bad=[r for r in rows if r[2]!="OK"]
print(f"checked {len(rows)} local links across markdown; {len(bad)} broken/failed")
for r in bad[:100]: print(" | ".join(r))
