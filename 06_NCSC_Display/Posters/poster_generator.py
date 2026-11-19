from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A1, A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
POSTERS = ROOT / "Posters"
PRINT = ROOT.parent / "printables"
POSTERS.mkdir(parents=True, exist_ok=True)
PRINT.mkdir(parents=True, exist_ok=True)
NAVY=colors.HexColor("#0B1F33"); TEAL=colors.HexColor("#13A89E"); GOLD=colors.HexColor("#F3B544")
CORAL=colors.HexColor("#DB6B57"); INK=colors.HexColor("#14283B"); MUTED=colors.HexColor("#526778")
LIGHT=colors.HexColor("#F4F7F8"); PALE=colors.HexColor("#E4F0F1"); WHITE=colors.white; BLUE=colors.HexColor("#4C7DA5")
W,H=594*mm,841*mm

def paragraph(c,txt,x,top,w,maxh,size=16,color=INK,bold=False,leading=None,page_height=None):
    page_height = H if page_height is None else page_height
    fs=size
    while fs>=11:
        st=ParagraphStyle("p",fontName="Helvetica-Bold" if bold else "Helvetica",fontSize=fs,leading=leading or fs*1.3,textColor=color,spaceAfter=0)
        p=Paragraph(txt,st)
        aw,ah=p.wrap(w*mm,maxh*mm)
        if ah <= maxh*mm:
            p.drawOn(c,x*mm,page_height-top*mm-ah)
            return ah/mm
        fs-=1
    st=ParagraphStyle("p",fontName="Helvetica",fontSize=11,leading=14,textColor=color)
    p=Paragraph(txt,st); _,ah=p.wrap(w*mm,maxh*mm); p.drawOn(c,x*mm,page_height-top*mm-ah)
    return ah/mm

def rect(c,x,top,w,h,fill,stroke=None,r=5,page_height=None):
    page_height = H if page_height is None else page_height
    c.setFillColor(fill); c.setStrokeColor(stroke or fill); c.roundRect(x*mm,(page_height-(top+h)*mm),w*mm,h*mm,r*mm,fill=1,stroke=1)

def header(c,title,subtitle,kicker):
    c.setFillColor(NAVY); c.rect(0,H-119*mm,W,119*mm,fill=1,stroke=0)
    paragraph(c,kicker.upper(),27,17,535,10,12,GOLD,True)
    paragraph(c,title,27,36,540,34,36,WHITE,True,43)
    paragraph(c,subtitle,28,82,525,22,18,colors.HexColor("#D7E4E9"),False,24)

def footer(c,sources):
    c.setFillColor(NAVY); c.rect(0,0,W,27*mm,fill=1,stroke=0)
    paragraph(c,"WORKING LAYOUT | A1 PORTRAIT (594 x 841 mm) | CONFIRM REQUIRED SIZE / COUNT WITH THE ORGANISER BEFORE PRINT",22,817,550,9,9,GOLD,True,11)
    paragraph(c,sources,22,828,550,12,10,WHITE,False,12)

def card(c,x,top,w,h,title,body,tag,color=TEAL,body_size=15):
    rect(c,x,top,w,h,WHITE,colors.HexColor("#D6E0E5"),4)
    c.setFillColor(color); c.roundRect(x*mm,(H-(top+h)*mm),5*mm,h*mm,2*mm,fill=1,stroke=0)
    paragraph(c,tag.upper(),x+14,top+12,w-26,8,12,color,True,14)
    paragraph(c,title,x+14,top+25,w-26,24,22,INK,True,27)
    paragraph(c,body,x+14,top+51,w-27,h-63,max(body_size,18),MUTED,False,max(body_size,18)*1.35)

def save(c):
    c.showPage(); c.save()

# Poster 1: problem and question
c=canvas.Canvas(str(PRINT/"AGASTYA_Poster_01_Problem_and_Question_A1.pdf"),pagesize=(W,H),pageCompression=1)
header(c,"Make silver-recovery claims testable","A research framework for end-of-life crystalline-silicon photovoltaic panels","Poster 1 | Problem and research question")
card(c,25,140,258,175,"The problem","A PV module is a bonded material system: glass, encapsulant, silicon cells with metal contacts, polymer backsheet, aluminium frame and junction box. The silver target is attached to cell material; seeing it does not prove a recoverable product.","Context",TEAL,16)
card(c,311,140,258,175,"The evidence gap","A useful recovery claim needs the mass and Ag assay of the feed and every output. Literature values use different feeds, particle cuts and endpoints; they cannot be copied into an AGASTYA balance.","Why measure?",GOLD,16)
# conceptual section
rect(c,25,337,544,184,PALE,PALE,4)
paragraph(c,"CONCEPTUAL LAYER STACK | NOT A PHOTOGRAPH OR BUILT PROTOTYPE",39,350,500,10,11,TEAL,True)
layers=[("FRONT GLASS",BLUE),("CELL + PRINTED Ag CONTACTS",GOLD),("EVA ENCAPSULANT",TEAL),("BACKSHEET + FRAME",CORAL)]
for i,(label,col) in enumerate(layers):
    yy=372+i*30
    rect(c,46,yy,252,21,col,col,2)
    paragraph(c,label,56,yy+4,230,14,11,WHITE,True)
paragraph(c,"MATERIAL STREAMS MUST KEEP THEIR IDS",332,380,210,12,12,NAVY,True)
paragraph(c,"Panel -> laminate -> size fractions -> aliquots -> assay -> receiver lot",332,401,210,45,17,INK,True,23)
card(c,25,545,258,150,"Research question","For a defined feed, which separation step partitions silver-bearing material while keeping the mass and silver balances traceable?","Question",BLUE,16)
card(c,311,545,258,150,"Current conclusion","AGASTYA has an evidence review and accounting framework. No AGASTYA sample, assay, recovered silver or separator performance is documented.","Status",CORAL,16)
paragraph(c,"NEXT MEASUREMENT: IDENTIFY A SAFE, TRACEABLE SAMPLE; WEIGH EACH STREAM; OBTAIN QUALIFIED Ag ASSAYS.",40,723,510,20,16,NAVY,True,19)
footer(c,"Sources: AGASTYA Phase B/C evidence database; Mulazzani et al. (2022), DOI 10.3390/en15228419. Layer drawing is a conceptual schematic.")
save(c)

# Poster 2: architecture
c=canvas.Canvas(str(PRINT/"AGASTYA_Poster_02_Architecture_A1.pdf"),pagesize=(W,H),pageCompression=1)
header(c,"Four stages. One evidence chain.","Current charter stages are numbered consistently; thermal delamination is optional pretreatment.","Poster 2 | Proposed system architecture")
stages=[
("01 | INSPECT + ROUTE","Panel passport, visible condition, human-reviewed decision; keep second-life options visible.","Input: identified module","DESIGN / SOFTWARE",TEAL),
("02 | LIBERATE + CLASSIFY","Manual preparation baseline; contained size cuts are a research comparison, with every fraction retained.","Input: traceable laminate","RESEARCH PLAN",GOLD),
("03 | CANDIDATE SEPARATION","Electrostatic separation is a testable candidate. Silver selectivity is not established for AGASTYA.","Input: characterized fraction","UNVALIDATED",BLUE),
("04 | ASSAY + ACCOUNT","Weigh and assay all outputs; calculate mass yield, Ag grade, Ag recovery and residual separately.","Input: labeled streams","MEASUREMENT GATE",CORAL)]
for i,(title,body,inp,tag,col) in enumerate(stages):
    x=25+(i%2)*286; top=145+(i//2)*190
    card(c,x,top,258,160,title,body,tag,col,15)
    paragraph(c,inp,x+15,top+137,225,15,10,NAVY,True)
# handoff strip
rect(c,25,548,544,137,NAVY,NAVY,5)
paragraph(c,"TRACEABILITY HAND-OFF",43,562,500,12,12,GOLD,True)
labels=["Panel ID","Stage event","Stream / batch","Aliquot","Assay","Receiver lot"]
for i,lbl in enumerate(labels):
    x=40+i*87
    rect(c,x,591,75,38,colors.HexColor("#173449"),colors.HexColor("#35566A"),4)
    paragraph(c,lbl,x+4,602,67,17,10,WHITE,True)
    if i<5:
        paragraph(c,">",x+75,600,10,20,16,GOLD,True)
paragraph(c,"Thermal delamination sits outside the numbered recovery stages as a possible feed-preparation step. Older documents use a different numbering; see the architecture crosswalk.",42,653,500,24,12,colors.HexColor("#DBE5EA"),False,16)
paragraph(c,"NO PROCESS IS VALIDATED UNTIL ITS MATERIAL INPUTS, OUTPUTS AND HAND-OFF ARE MEASURED.",40,725,510,20,16,NAVY,True)
footer(c,"Sources: AGASTYA Architecture Crosswalk (2026-10-10); Phase B/C validation plan. All stages shown are design/research boundaries, not proven performance.")
save(c)

# Poster 3: evidence and findings
c=canvas.Canvas(str(PRINT/"AGASTYA_Poster_03_Evidence_and_Findings_A1.pdf"),pagesize=(W,H),pageCompression=1)
header(c,"Published results are not AGASTYA results.","Keep recovery, grade, mass yield and size partition separate.","Poster 3 | Evidence and current findings")
# evidence cards
card(c,25,145,258,168,"Mechanical size partition","Sim et al. report up to 70% and 80% of feed Ag in F4 for two separate study categories. Juyo Salazar et al. report 94.12% of Ag in a <0.25 mm fraction for its feed.","Direct Ag partition",TEAL,14)
card(c,311,145,258,168,"Electrostatic PV scrap","de Souza & Veit report Ag/Al/Si co-concentration. The accessible abstract does not give mass-based Ag recovery, product grade or a complete product split.","Incomplete Ag metric",GOLD,14)
card(c,25,333,258,168,"Silver-focused flotation","Saffarian et al. report 97.55 +/- 0.03% recovery and 32.2 +/- 2.3x upgrade in a tap-water rougher test on prepared cell feed.","Bench comparator",BLUE,14)
card(c,311,333,258,168,"Silver reference values","Review scenario: 300 ppm, with unresolved sample basis. Dias publisher abstract: 600 g/t. A secondary excerpt gives 630 g/t; discrepancy unresolved.","Arithmetic only",CORAL,14)
for i,(big,lab,col) in enumerate([
    ("14","source records reviewed",TEAL),
    ("5","candidate routes compared",GOLD),
    ("11","executed literature arithmetic rows",BLUE),
    ("0","physical AGASTYA samples",CORAL)
]):
    x=39+(i%2)*286
    top=145+(i//2)*188
    paragraph(c,big,x,top+112,230,24,22,col,True,27)
    paragraph(c,lab,x,top+140,230,13,10,MUTED,True,12)
rect(c,25,525,544,158,PALE,PALE,4)
paragraph(c,"WHAT THE CURRENT AGASTYA ANALYSIS ACTUALLY PRODUCED",40,540,500,14,12,TEAL,True)
metrics=[("14","source records"),("5","routes compared"),("11","arithmetic rows"),("0","physical samples")]
for i,(v,lbl) in enumerate(metrics):
    x=42+i*132
    paragraph(c,v,x,570,117,27,24,NAVY,True,28)
    paragraph(c,lbl,x,605,117,28,11,MUTED,True,14)
paragraph(c,"0 assays | 0 electrostatic / chemistry solver runs | no AGASTYA recovery or purity result",42,646,510,18,14,CORAL,True)
paragraph(c,"CONCLUSION: NO UNIVERSAL ROUTE RANKING. DIFFERENT FEEDS AND ENDPOINTS REQUIRE MATCHED TESTS.",40,716,510,20,15,NAVY,True)
footer(c,"Sources: Sim et al. 2022 (10.1016/j.wasman.2022.11.023); Juyo Salazar et al. 2024 (10.1016/j.susmat.2024.e01047); de Souza & Veit 2023 (10.1016/j.cec.2023.100027); Saffarian et al. 2026 (10.1016/j.mineng.2026.110189); Dias et al. 2016; Mwase et al. 2024.")
save(c)

# Poster 4: conclusion and next test
c=canvas.Canvas(str(PRINT/"AGASTYA_Poster_04_Conclusion_and_Next_Steps_A1.pdf"),pagesize=(W,H),pageCompression=1)
header(c,"Measure first. Choose the route second.","The next study should close one evidence gap at a time.","Poster 4 | Conclusion and validation plan")
card(c,25,145,258,168,"What we can say","A traceable four-stage concept and literature-grounded comparison are documented. The accounting model distinguishes mass yield, grade, recovery and residual.","Established",TEAL,15)
card(c,311,145,258,168,"What we cannot say","No AGASTYA silver recovery, product purity, throughput, safe operating setpoint, cost, environmental benefit or solver prediction is validated.","Not established",CORAL,15)
gates=[
("1 | DEFINE","Sample origin, technology, condition, ID and chain of custody."),
("2 | WEIGH","Every input/output stream, size fraction, dust catch and loss."),
("3 | ASSAY","Qualified lab; agreed prep, QA/QC, limits and duplicates."),
("4 | BALANCE","Separate grade, yield, recovery, residual and uncertainty.")
]
for i,(title,body) in enumerate(gates):
    y=340+i*74
    rect(c,45,y,505,60,WHITE,colors.HexColor("#D6E0E5"),4)
    paragraph(c,title,62,y+13,105,23,14,[TEAL,GOLD,BLUE,CORAL][i],True,17)
    paragraph(c,body,180,y+11,350,37,14,INK,False,18)
rect(c,25,663,544,62,colors.HexColor("#FFF4DA"),colors.HexColor("#EBD59C"),4)
paragraph(c,"STOP IF SAMPLE ID, SAFETY CONTROLS OR ASSAY QA/QC FAIL. NEVER FORCE A BALANCE TO CLOSE.",40,682,510,24,15,NAVY,True,19)
paragraph(c,"A useful result may be a clear no-go.",40,746,510,26,18,TEAL,True,22)
footer(c,"Sources: AGASTYA Phase B/C validation plan. Any future physical trial requires an authorized, supervised facility and a site-specific safety review.")
save(c)

# A4 companion sheets
def a4(name,title,sub,blocks,source):
    c=canvas.Canvas(str(PRINT/name),pagesize=A4,pageCompression=1); w,h=A4
    c.setFillColor(NAVY); c.rect(0,h-48*mm,w,48*mm,fill=1,stroke=0)
    paragraph(c,title,14,12,180,17,21,WHITE,True,25,page_height=h)
    paragraph(c,sub,14,32,180,12,10,colors.HexColor("#D7E4E9"),False,13,page_height=h)
    y=60
    for tag,head,body,col in blocks:
        rect(c,14,y,182,42,WHITE,colors.HexColor("#D6E0E5"),3,page_height=h)
        paragraph(c,tag.upper(),20,y+5,168,7,8,col,True,10,page_height=h)
        paragraph(c,head,20,y+13,168,10,12,INK,True,14,page_height=h)
        paragraph(c,body,20,y+24,168,15,9.5,MUTED,False,12,page_height=h)
        y+=48
    c.setFillColor(NAVY); c.rect(0,0,w,18*mm,fill=1,stroke=0)
    paragraph(c,source,12,279,185,11,7,WHITE,False,8,page_height=h)
    paragraph(c,"WORKING MATERIAL | CONFIRM EVENT-SPECIFIC RULES",12,288,185,7,7.5,GOLD,True,9,page_height=h)
    save(c)

a4("AGASTYA_A4_Project_Summary.pdf","AGASTYA | project summary","Research framework for end-of-life PV material recovery",
   [("Problem","Mixed materials, small Ag target","Panel layers are bonded; a visible metal contact is not a recovered product.",TEAL),
    ("Question","Can each stream be traced?","Define a feed, weigh every output, assay it, and report residuals honestly.",GOLD),
    ("Current evidence","Research only","14 source records, five route comparisons and 11 executed literature arithmetic rows.",BLUE),
    ("Current limit","No physical result","No AGASTYA sample, assay or electrostatic/chemistry solver run is documented.",CORAL)],"Sources: AGASTYA Phase B/C report; literature cited in evidence database.")
a4("AGASTYA_A4_Architecture.pdf","Four-stage architecture","Current charter sequence | thermal delamination is optional pretreatment",
   [("Stage 1","Inspect and route","Panel identity, visible condition and human-reviewed triage.",TEAL),
    ("Stage 2","Liberate and classify","Manual baseline; compare defined and retained size fractions.",GOLD),
    ("Stage 3","Candidate separation","Electrostatic route remains a hypothesis until measured.",BLUE),
    ("Stage 4","Assay and account","Separate mass yield, Ag grade, recovery and balance residual.",CORAL)],"Source: AGASTYA architecture crosswalk. Proposed stages; not validated performance.")
a4("AGASTYA_A4_Evidence_and_Results.pdf","Evidence and current results","Literature metrics remain attached to each study's own feed",
   [("Size partition","70%, 80%, 94.12%","Different studies and size classes; not an AGASTYA recovery.",TEAL),
    ("Electrostatic","Ag co-concentration reported","Accessible abstract lacks mass-based Ag recovery and product grade.",GOLD),
    ("Flotation","97.55% Ag recovery","Bench test on prepared PV-cell feed using reagents; comparator only.",BLUE),
    ("References","300 ppm; 600 g/t; 630 g/t","Different bases; 300 ppm provenance and 600/630 discrepancy unresolved.",CORAL)],"Sources: Sim 2022; Juyo Salazar 2024; de Souza & Veit 2023; Saffarian 2026; Dias 2016; Mulazzani 2022.")
a4("AGASTYA_A4_Attribution_and_Sources.pdf","Attribution and sources","No third-party photos or experimental images are used in these layouts",
   [("Project files","AGASTYA Phase B/C","Data tables, architecture crosswalk, simulation and logbook are local project records.",TEAL),
    ("Literature","Primary studies","DOIs and extraction boundaries are listed in SOURCE_EVIDENCE_REGISTER.csv.",GOLD),
    ("Visuals","Original vector diagrams","Layer schematic and process diagrams are conceptual illustrations created for this project.",BLUE),
    ("Competition","NCSC guide","Official DST guidebook PDF; confirm dimensions, deadlines and category with coordinator.",CORAL)],"Official guide: dst.gov.in/sites/default/files/Activity-Guidebook-for-NCSC-2026-27_0.pdf")
print("Created four A1 poster PDFs and four A4 companion sheets.")
