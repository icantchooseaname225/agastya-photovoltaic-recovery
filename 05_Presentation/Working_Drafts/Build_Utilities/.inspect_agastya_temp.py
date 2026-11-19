from pptx import Presentation
from zipfile import ZipFile
from pathlib import Path
import re

p = Path(r'D:\Agastya\05_Presentation\Existing_Presentations\Agastya_Presentation_Enhanced.pptx')
prs = Presentation(str(p))
print('slides:', len(prs.slides), 'size_inches:', round(prs.slide_width/914400,3), round(prs.slide_height/914400,3), 'bytes:', p.stat().st_size)
W, H = prs.slide_width, prs.slide_height
issues = []
unicode_chars = set()
all_text = []
for n, sl in enumerate(prs.slides, 1):
    strings = []
    for shp in sl.shapes:
        if shp.left < -1000 or shp.top < -1000 or shp.left + shp.width > W + 1500 or shp.top + shp.height > H + 1500:
            issues.append((n, 'bounds', shp.name, tuple(round(v/914400,3) for v in (shp.left,shp.top,shp.width,shp.height))))
        if shp.has_text_frame:
            t = shp.text.strip()
            if t:
                strings.append(t)
                all_text.append(t)
                unicode_chars.update(ch for ch in t if ord(ch) > 127)
    print(f'--- {n:02d} ---')
    print(' | '.join(strings))
with ZipFile(p) as z:
    slide_xml = [n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
    transitions = [n for n in slide_xml if b'<p:transition spd="med"><p:fade/></p:transition>' in z.read(n)]
    notes = [n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
    links = [n for n in z.namelist() if re.fullmatch(r'ppt/slides/_rels/slide\d+\.xml\.rels',n) and b'TargetMode="External"' in z.read(n)]
    print('fade transitions:', len(transitions), 'notes:', len(notes), 'slides with external links:', len(links))
print('unicode in slide text:', sorted(unicode_chars))
print('bounds issues:', issues[:20], 'count=',len(issues))
print('suspect placeholders:', [x for x in all_text if re.search(r'\b(?:TODO|TBD|lorem|ipsum|insert here|placeholder)\b', x, re.I)])

