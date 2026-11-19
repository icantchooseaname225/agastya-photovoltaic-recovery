from pathlib import Path
from datetime import datetime
from collections import Counter
import csv,os

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
CSV_PATH=OUT/"file_inventory.csv"
SUMMARY_PATH=OUT/"file_inventory_summary.md"

def category(rel):
    return rel.parts[0] if len(rel.parts)>1 else "Project root"

rows=[]
for base,dirs,files in os.walk(ROOT):
    dirs[:] = sorted(d for d in dirs if d not in {".git"})
    for name in files:
        p=Path(base)/name
        try:
            st=p.stat()
            rel=p.relative_to(ROOT)
            rows.append([rel.as_posix(),category(rel),p.suffix.lower() or "[no extension]",st.st_size,datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec="seconds")])
        except (OSError,ValueError) as exc:
            rel=p.relative_to(ROOT).as_posix()
            rows.append([rel,category(Path(rel)),p.suffix.lower() or "[no extension]","",f"STAT_ERROR: {exc}"])
with CSV_PATH.open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f)
    w.writerow(["relative_path","top_level_category","extension","size_bytes","modified_local"])
    w.writerows(sorted(rows,key=lambda r:r[0].casefold()))
ext=Counter(r[2] for r in rows)
cats=Counter(r[1] for r in rows)
total=sum(r[3] for r in rows if isinstance(r[3],int))
lines=[
"# AGASTYA file inventory summary",
"",
f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
f"Files inventoried: {len(rows):,}",
f"Combined file size: {total:,} bytes ({total/1_000_000_000:.3f} GB decimal)",
"",
"## Files by top-level category",
""
]
lines += [f"- {k}: {v:,}" for k,v in sorted(cats.items())]
lines += ["","## Most common file extensions",""]
lines += [f"- {k}: {v:,}" for k,v in ext.most_common(15)]
lines += ["","The CSV records every file path, category, extension, byte size and local modification time. It includes datasets and supporting media; counts may include generated caches and build dependencies."]
SUMMARY_PATH.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Inventoried {len(rows):,} files; {total:,} bytes; wrote {CSV_PATH.name} and {SUMMARY_PATH.name}")
