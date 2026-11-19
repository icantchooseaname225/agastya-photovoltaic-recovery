const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const OUT = path.resolve(__dirname, "..");
const P = pptxgen;
let pptx = new P();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "AGASTYA research team";
pptx.subject = "Evidence-bounded photovoltaic silver recovery research";
pptx.title = "AGASTYA — measured pathways for PV material recovery";
pptx.company = "AGASTYA";
pptx.lang = "en-IN";
pptx.theme = { headFontFace: "Arial", bodyFontFace: "Arial", lang: "en-IN" };

const C = { navy:"0B1F33", deep:"071825", teal:"13A89E", gold:"F3B544", coral:"DB6B57", ink:"14283B", muted:"526778", light:"F4F7F8", pale:"E4F0F1", line:"D6E0E5", white:"FFFFFF", green:"397A68", blue:"4C7DA5" };
const IMG_PANEL = path.join(OUT,"..","07_Visual_Assets","01_Original_Photographs","PV_Panel_Fomanu_2015.jpg");
const IMG_CELLS = path.join(OUT,"..","07_Visual_Assets","01_Original_Photographs","Silicon_Solar_Cells_Fdenicola_2013.jpg");
const evidence = [];
const assets = [];
const speaker = [];
function text(s,t,x,y,w,h,o={}) {
  s.addText(t,{x,y,w,h,fontFace:"Arial",fontSize: o.size||16,color:o.color||C.ink,bold:!!o.bold,margin:o.margin===undefined?0.04:o.margin,fit:"shrink",valign:o.valign||"mid",align:o.align||"left",breakLine:false,paraSpaceAfterPt:0,...o});
}
function shape(s,type,x,y,w,h,fill,line=C.line,extra={}) {
  s.addShape(type,{x,y,w,h,rectRadius:0.08,fill:{color:fill},line:{color:line,width:1},...extra});
}
function card(s,x,y,w,h,title,body,tag,accent=C.teal,dark=false) {
  const bg=dark?"102B3D":C.white, fg=dark?C.white:C.ink, sub=dark?"D5E1E7":C.muted;
  shape(s,pptx.ShapeType.roundRect,x,y,w,h,bg,dark?"244759":C.line);
  shape(s,pptx.ShapeType.rect,x,y,0.08,h,accent,accent);
  if(tag) text(s,tag.toUpperCase(),x+0.22,y+0.12,w-0.4,0.2,{size:9,bold:true,color:accent,charSpacing:1});
  text(s,title,x+0.22,y+(tag?0.38:0.18),w-0.43,0.42,{size:17,bold:true,color:fg,valign:"mid"});
  text(s,body,x+0.22,y+(tag?0.84:0.68),w-0.43,h-(tag?0.96:0.8),{size:13.5,color:sub,valign:"top",breakLine:false});
}
function photo(s,file,x,y,w,h,caption,credit,altText) {
  if (!fs.existsSync(file)) throw new Error(`Missing presentation image: ${file}`);
  s.addImage({path:file,x,y,w,h,altText});
  s.addShape(pptx.ShapeType.rect,{x,y,w,h,fill:{color:C.white,transparency:100},line:{color:"BFCFD6",width:1.1}});
  text(s,caption,x+0.02,y+h+0.09,w-0.04,0.18,{size:9.5,bold:true,color:C.ink});
  text(s,credit,x+0.02,y+h+0.25,w-0.04,0.39,{size:7.5,color:C.muted,valign:"top"});
}
function header(s,spec,n,dark=false) {
  s.background={color:dark?C.deep:C.light};
  text(s,spec.kicker.toUpperCase(),0.68,0.25,11.7,0.2,{size:9,bold:true,color:dark?C.gold:C.teal,charSpacing:1.3});
  text(s,spec.title,0.68,0.59,12.0,0.6,{size:29,bold:true,color:dark?C.white:C.navy,valign:"mid"});
  if(spec.sub) text(s,spec.sub,0.7,1.24,11.9,0.38,{size:14,color:dark?"D2E0E5":C.muted});
  text(s,"AGASTYA  •  RESEARCH DESIGN  •  20 OCT 2026",0.68,7.17,10.8,0.16,{size:8,color:dark?"AFC0CA":"6E7D88",charSpacing:0.45});
  text(s,String(n).padStart(2,"0"),12.22,7.13,0.46,0.22,{size:9,bold:true,color:dark?C.gold:C.teal,align:"right"});
}
function addNotes(s,spec,deck,n) {
  const note=(spec.notes||"") + "\nEvidence boundary: all literature values are study-specific. No AGASTYA physical recovery result is claimed.";
  s.addNotes(note);
  speaker.push("## "+deck+" — Slide "+n+": "+spec.title+"\n\n"+note+"\n");
  if(spec.source) evidence.push([deck,n,spec.title,spec.claim||spec.source,spec.source,spec.limit||"Literature result or project calculation; not an AGASTYA physical result."]);
}
function slideFor(spec,n,deck) {
  const s=pptx.addSlide(); const dark=spec.type==="cover"||spec.type==="closing";
  header(s,spec,n,dark);
  const W=12.1, x0=0.65, y0=1.83;
  if(spec.type==="cover"||spec.type==="closing") {
    if(spec.type==="cover") {
      text(s,spec.hero,0.78,1.8,5.35,1.35,{size:35,bold:true,color:C.white,valign:"mid",breakLine:false});
      text(s,spec.body,0.81,3.36,5.05,0.92,{size:17,color:"D8E4E8",valign:"top"});
      shape(s,pptx.ShapeType.roundRect,0.82,4.68,5.5,0.5,"143347","285267");
      text(s,spec.status,1.02,4.82,5.1,0.2,{size:10.5,bold:true,color:C.gold});
      photo(s,IMG_PANEL,6.75,1.55,5.84,3.89,"Illustrative PV installation • not an AGASTYA sample","Fomanu (2015), Wikimedia Commons: commons.wikimedia.org/wiki/File:PV_Panel.jpg | CC BY-SA 4.0: creativecommons.org/licenses/by-sa/4.0", "Photovoltaic panels in a snowy landscape; illustrative external image, not AGASTYA equipment.");
      shape(s,pptx.ShapeType.roundRect,0.82,5.62,5.35,0.76,"102B3D","244759");
      text(s,"Question first",1.03,5.76,1.65,0.21,{size:11,bold:true,color:C.teal});
      text(s,"Which step moves silver-bearing material—and what can we actually prove?",2.65,5.72,3.26,0.39,{size:12.5,bold:true,color:C.white});
    } else {
      text(s,spec.hero,0.84,1.88,5.35,0.72,{size:34,bold:true,color:C.white,valign:"mid",breakLine:false});
      text(s,spec.body,0.87,2.84,5.2,0.94,{size:17,color:"D8E4E8",valign:"top"});
      shape(s,pptx.ShapeType.roundRect,0.88,4.15,5.45,0.56,"143347","285267");
      text(s,spec.status,1.08,4.32,5.05,0.22,{size:10.5,bold:true,color:C.gold});
      text(s,"Thank you",0.92,5.13,4.6,0.56,{size:27,bold:true,color:C.white});
      text(s,"Trace each claim to a source, input, calculation or measurement.",0.95,5.92,5.45,0.48,{size:14,color:"D8E4E8"});
      card(s,7.02,1.9,5.45,1.95,"The defensible claim",spec.left,"Conclusion",C.teal,true);
      card(s,7.02,4.16,5.45,1.95,"The next measurement",spec.right,"Next step",C.gold,true);
    }
  } else if(spec.type==="layers") {
    spec.items.forEach((a,i)=>{const yy=1.95+i*0.78; shape(s,pptx.ShapeType.roundRect,0.86,yy,5.78,0.58,a[2],a[2]); text(s,a[0],1.08,yy+0.07,5.2,0.22,{size:12.5,bold:true,color:C.white}); text(s,a[1],1.08,yy+0.32,5.2,0.17,{size:9.5,color:"EAF0F3"});});
    photo(s,IMG_CELLS,7.28,1.95,4.95,3.70,"Silicon solar-cell material • illustrative close-up","Fdenicola (2013), Wikimedia Commons: commons.wikimedia.org/wiki/File:Solar_cell01.JPG | CC BY-SA 4.0: creativecommons.org/licenses/by-sa/4.0", "Close-up photograph of silicon solar cells; illustrative external image, not an AGASTYA sample.");
    shape(s,pptx.ShapeType.roundRect,7.28,6.23,4.95,0.62,C.white,C.line);
    text(s,"WHY RECOVERY IS DIFFICULT",7.47,6.32,4.55,0.18,{size:9,bold:true,color:C.gold,charSpacing:0.7});
    text(s,"Small contacts sit inside bonded, mixed-material layers.",7.47,6.51,4.55,0.22,{size:11.5,bold:true,color:C.ink});
    text(s,"Silver in cell metallization is not the same as silver recovered as a product.",0.9,5.45,5.75,0.65,{size:14,bold:true,color:C.navy,valign:"mid"});
  } else if(spec.type==="portfolio") {
    const cols=[0.82,6.83], rows=[1.92,3.61];
    spec.cards.forEach((a,i)=>card(s,cols[i%2],rows[Math.floor(i/2)],5.68,1.38,a[0],a[1],a[2],[C.teal,C.gold,C.blue,C.coral][i]));
    shape(s,pptx.ShapeType.roundRect,1.18,5.48,10.95,0.72,"102B3D","244759");
    text(s,"Supporting evidence",1.45,5.66,2.25,0.24,{size:12,bold:true,color:C.gold});
    text(s,spec.bottom,3.72,5.62,8.05,0.38,{size:13,bold:true,color:C.white});
  } else if(spec.type==="eye") {
    const steps=spec.steps, startX=0.84, stepW=2.62, gap=0.23;
    steps.forEach((a,i)=>{
      const xx=startX+i*(stepW+gap);
      shape(s,pptx.ShapeType.roundRect,xx,2.10,stepW,1.22,i===3?C.navy:C.white,i===3?C.navy:C.line);
      text(s,String(i+1).padStart(2,"0"),xx+0.16,2.24,0.44,0.22,{size:11,bold:true,color:i===3?C.gold:C.teal});
      text(s,a[0],xx+0.16,2.54,stepW-0.32,0.27,{size:14,bold:true,color:i===3?C.white:C.ink});
      text(s,a[1],xx+0.16,2.91,stepW-0.32,0.24,{size:9.5,color:i===3?"D5E1E7":C.muted});
      if(i<3) shape(s,pptx.ShapeType.chevron,xx+stepW+0.035,2.57,0.15,0.24,C.gold,C.gold);
    });
    card(s,0.93,3.9,5.58,1.55,"What EYE contributes",spec.left,"Inspection + traceability",C.teal);
    card(s,6.83,3.9,5.58,1.55,"What EYE cannot establish",spec.right,"Limits",C.coral);
    text(s,spec.bottom,1.0,5.9,11.25,0.42,{size:13,bold:true,color:C.navy,align:"center"});
  } else if(spec.type==="thermal") {
    const px=0.94, py=2.02;
    shape(s,pptx.ShapeType.roundRect,px,py,5.05,3.55,C.white,C.line);
    text(s,"REDUCED THERMAL MODEL",px+0.24,py+0.2,4.55,0.23,{size:10,bold:true,color:C.teal,charSpacing:0.8});
    const stack=[["Glass",C.blue],["Front EVA",C.gold],["Silicon cell",C.teal],["Rear EVA",C.gold],["Backsheet",C.coral]];
    stack.forEach((a,i)=>{
      const yy=py+0.68+i*0.45;
      shape(s,pptx.ShapeType.roundRect,px+0.46,yy,2.5,0.29,a[1],a[1]);
      text(s,a[0],px+0.58,yy+0.04,2.25,0.18,{size:10.5,bold:true,color:C.white});
    });
    shape(s,pptx.ShapeType.chevron,px+3.2,py+1.47,0.42,0.48,C.gold,C.gold);
    text(s,"5 thermal nodes\n1-D heat transfer\nforward Euler time steps",px+3.73,py+1.19,1.1,0.94,{size:11,bold:true,color:C.ink,valign:"mid"});
    text(s,"Illustrative model structure • not a drawing of a tested apparatus",px+0.45,py+3.0,4.35,0.24,{size:9.5,color:C.muted,align:"center"});
    card(s,6.55,2.02,5.76,1.3,"What was computed","Temperature and sensible-heat scenarios over assumed material properties, contact conditions and dwell times.","Executed numerical model",C.teal);
    card(s,6.55,3.58,5.76,1.3,"What was not computed","No peel force, adhesion failure, EVA chemistry, fumes, safety, machine power or delamination quality.","Model boundary",C.coral);
    shape(s,pptx.ShapeType.roundRect,6.55,5.2,5.76,0.62,"FFF4DA","EBD59C");
    text(s,spec.bottom,6.76,5.36,5.35,0.26,{size:11.5,bold:true,color:C.navy,align:"center"});
    text(s,"The thermal model informs Stage 3 heat-transfer questions; it does not model peel quality or silver recovery.",0.98,6.05,11.25,0.46,{size:12.5,bold:true,color:C.navy,align:"center"});
  } else if(spec.type==="simulations") {
    const cols=[0.82,6.83], rows=[1.92,3.57];
    spec.cards.forEach((a,i)=>card(s,cols[i%2],rows[Math.floor(i/2)],5.68,1.4,a[0],a[1],a[2],[C.teal,C.gold,C.blue,C.coral][i]));
    shape(s,pptx.ShapeType.roundRect,1.18,5.48,10.95,0.72,"FFF4DA","EBD59C");
    text(s,spec.bottom,1.4,5.62,10.5,0.4,{size:11.5,bold:true,color:C.navy,align:"center"});
  } else if(spec.type==="flow") {
    const labels=spec.items; const w=2.12,gap=0.25;
    labels.forEach((a,i)=>{const xx=0.72+i*(w+gap); shape(s,pptx.ShapeType.roundRect,xx,2.45,w,1.08,i===4?C.navy:C.white,i===4?C.navy:C.line); text(s,String(i+1).padStart(2,"0"),xx+0.14,2.6,0.42,0.22,{size:11,bold:true,color:i===4?C.gold:C.teal}); text(s,a[0],xx+0.14,2.87,w-0.25,0.28,{size:13,bold:true,color:i===4?C.white:C.ink}); text(s,a[1],xx+0.14,3.25,w-0.28,0.18,{size:9.5,color:i===4?"D5E1E7":C.muted}); if(i<4) shape(s,pptx.ShapeType.chevron,xx+w+0.05,2.82,0.16,0.22,C.gold,C.gold);});
    card(s,1.0,4.32,5.3,1.26,"Research question",spec.body,"Aim",C.teal);
    card(s,6.8,4.32,5.3,1.26,"Primary objectives",spec.side,"Plan",C.gold);
  } else if(spec.type==="stages") {
    spec.items.forEach((a,i)=>{const xx=0.78+(i%2)*6.05, yy=1.98+Math.floor(i/2)*1.54; card(s,xx,yy,5.65,1.28,a[0],a[1],a[2],[C.teal,C.gold,C.blue,C.coral][i]);});
    shape(s,pptx.ShapeType.roundRect,2.0,5.28,9.25,0.62,"FFF4DA","EBD59C");
    text(s,"Sampling, assay, mass balance and uncertainty validate every stage.",2.18,5.45,8.9,0.2,{size:12,bold:true,color:C.ink,align:"center"});
  } else if(spec.type==="bars") {
    const chartX=1.0, chartY=2.15, chartW=7.4, barH=0.58;
    spec.bars.forEach((b,i)=>{const yy=chartY+i*1.05; text(s,b.label,chartX,yy,2.0,0.23,{size:12,bold:true}); shape(s,pptx.ShapeType.roundRect,chartX+2.15,yy,chartW-2.2,barH,C.white,C.line); shape(s,pptx.ShapeType.roundRect,chartX+2.15,yy,Math.max(.18,(chartW-2.2)*b.value/100),barH,b.color,b.color); text(s,b.value+"%",chartX+6.95,yy+0.13,0.8,0.25,{size:15,bold:true,color:C.navy,align:"right"}); text(s,b.note,chartX+2.18,yy+0.65,chartW-2.3,0.22,{size:9.5,color:C.muted});});
    card(s,9.0,2.18,3.1,1.25,"Independent feeds","Different studies and sieve definitions.","Basis",C.gold);
    card(s,9.0,3.72,3.1,1.25,"Not a prediction","Do not average these percentages or apply them to AGASTYA.","Limit",C.coral);
    text(s,"Ag partition into the reported fine fraction — study-specific",1.02,5.55,8.0,0.26,{size:11,bold:true,color:C.muted});
  } else if(spec.type==="comparison") {
    spec.cards.forEach((a,i)=>card(s,0.75+i*4.05,2.12,3.75,2.7,a[0],a[1],a[2],[C.teal,C.gold,C.coral][i]));
    shape(s,pptx.ShapeType.roundRect,1.5,5.34,10.3,0.64,"E5F1F1","C7DEDE");
    text(s,spec.callout,1.72,5.5,9.9,0.22,{size:12,bold:true,color:C.navy,align:"center"});
  } else if(spec.type==="equations") {
    spec.cards.forEach((a,i)=>{const xx=0.8+(i%2)*6.05, yy=1.98+Math.floor(i/2)*1.47; card(s,xx,yy,5.65,1.22,a[0],a[1],a[2],[C.teal,C.gold,C.blue,C.coral][i]);});
  } else if(spec.type==="scenarios") {
    const cardW=3.82, gap=0.36, startX=(13.333-(3*cardW+2*gap))/2;
    spec.cards.forEach((a,i)=>{const xx=startX+i*(cardW+gap); shape(s,pptx.ShapeType.roundRect,xx,2.18,cardW,2.45,C.white,C.line); text(s,a[0],xx+0.16,2.42,cardW-0.32,0.42,{size:11,bold:true,color:C.muted,align:"center",valign:"mid"}); text(s,a[1],xx+0.14,2.98,cardW-0.28,0.58,{size:i===2?18:27,bold:true,color:i===0?C.teal:(i===1?C.gold:C.coral),align:"center",valign:"mid"}); text(s,a[2],xx+0.2,3.7,cardW-0.4,0.72,{size:10.5,color:C.muted,align:"center",valign:"mid"});});
    text(s,"Separate published bases • not a pooled range • not an AGASTYA assay",1.2,5.15,10.7,0.3,{size:14,bold:true,color:C.coral,align:"center"});
  } else if(spec.type==="tools") {
    card(s,0.82,2.0,5.5,2.95,"Actually executed",spec.left,"Software",C.teal);
    card(s,6.95,2.0,5.5,2.95,"Not executed",spec.right,"Evidence boundary",C.coral);
    text(s,spec.bottom,1.1,5.4,11.1,0.45,{size:15,bold:true,color:C.navy,align:"center"});
  } else if(spec.type==="scorecard") {
    spec.cards.forEach((a,i)=>{const xx=0.78+i*3.03; shape(s,pptx.ShapeType.roundRect,xx,2.15,2.75,1.4,C.white,C.line); text(s,a[0],xx+0.18,2.38,2.4,0.48,{size:25,bold:true,color:a[2]||C.teal,align:"center"}); text(s,a[1],xx+0.15,2.99,2.45,0.32,{size:10.5,bold:true,color:C.muted,align:"center"});});
    card(s,1.0,4.16,5.25,1.25,"What the project establishes",spec.left,"Conclusion",C.teal);
    card(s,6.92,4.16,5.25,1.25,"What is still missing",spec.right,"Boundary",C.coral);
  } else if(spec.type==="gates") {
    spec.items.forEach((a,i)=>{const xx=0.62+i*3.15; card(s,xx,2.0,2.88,2.38,a[0],a[1],String(i+1).padStart(2,"0"),[C.teal,C.gold,C.blue,C.coral][i]);});
    shape(s,pptx.ShapeType.roundRect,1.4,5.1,10.5,0.67,"FFF4DA","EBD59C");
    text(s,spec.callout,1.6,5.29,10.1,0.24,{size:12,bold:true,color:C.navy,align:"center"});
  } else if(spec.type==="tradeoffs") {
    card(s,0.88,2.12,5.2,2.75,"Potential value",spec.left,"Question to investigate",C.teal);
    shape(s,pptx.ShapeType.ellipse,6.22,2.75,0.9,0.9,C.gold,C.gold);
    text(s,"?",6.47,2.94,0.4,0.42,{size:24,bold:true,color:C.navy,align:"center"});
    card(s,7.25,2.12,5.2,2.75,"Costs and burdens",spec.right,"Measure and disclose",C.coral);
    text(s,spec.bottom,1.0,5.45,11.3,0.36,{size:14,bold:true,color:C.navy,align:"center"});
  } else if(spec.type==="references") {
    spec.items.forEach((a,i)=>{const yy=1.95+i*0.72; shape(s,pptx.ShapeType.ellipse,0.87,yy+0.09,0.22,0.22,[C.teal,C.gold,C.blue,C.coral][i%4],[C.teal,C.gold,C.blue,C.coral][i%4]); text(s,a[0],1.25,yy,10.6,0.26,{size:13,bold:true,color:C.ink}); text(s,a[1],1.25,yy+0.31,10.65,0.2,{size:9.5,color:C.muted});});
  }
  addNotes(s,spec,deck,n);
  assets.push([deck,n,spec.title,spec.visual||"PowerPoint-native vector shapes and text",spec.provenance||"No external photograph; any diagram is conceptual"]);
  return s;
}

const master = [
{type:"cover",kicker:"PV material recovery • research status",title:"AGASTYA",sub:"",hero:"Measure the material.\nThen choose the route.",body:"A research framework for inspecting end-of-life solar panels and testing a traceable route for silver-bearing material.",status:"RESEARCH CONCEPT • NO AGASTYA RECOVERY RESULT",notes:"Introduce AGASTYA as a research and engineering concept. The cover photograph is illustrative only; it is not an AGASTYA panel or apparatus. State clearly that no physical silver-recovery trial or assay has been completed.",visual:"External photovoltaic-panel photograph",provenance:"Fomanu, ‘PV Panel.jpg’ (2015), Wikimedia Commons, https://commons.wikimedia.org/wiki/File:PV_Panel.jpg, CC BY-SA 4.0. Illustrative image; not AGASTYA equipment."},
{type:"layers",kicker:"01 • the problem",title:"A panel is a mixed material system",sub:"Small metal contacts sit inside bonded, high-mass layers.",items:[["FRONT GLASS","Protective, high-mass sheet",C.blue],["CELL + Ag CONTACTS","Silver is printed on silicon cells",C.gold],["EVA ENCAPSULANT","Polymer bonds the laminate",C.teal],["BACKSHEET / FRAME","Polymer, aluminium and junction box",C.coral]],source:"Agastya thesis; Mulazzani et al. 2022, DOI 10.3390/en15228419",claim:"Crystalline-silicon module construction and silver as cell metallization",limit:"Illustrative construction; actual module composition varies. No AGASTYA panel assay.",visual:"External solar-cell photograph and native material-layer diagram",provenance:"Fdenicola, ‘Solar cell01.JPG’ (2013), Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Solar_cell01.JPG, CC BY-SA 4.0. Illustrative cells only; not an AGASTYA sample."},
{type:"portfolio",kicker:"02 • the AGASTYA project",title:"One project, four connected workstreams",sub:"Inspection, process research, measurement and evidence each have a different job.",cards:[["Inspect + record","AGASTYA-EYE creates a human-reviewed panel inspection record and material passport.","DIGITAL TOOL"],["Prepare material","Manual preparation, thermal delamination, then Stage 4 silver removal with its route open.","PROCESS RESEARCH"],["Evaluate separation","Stage 4 removes silver from characterized feed; method, preparation and product form remain open.","UNVALIDATED"],["Verify + report","Qualified assays, weighed streams and uncertainty are needed before silver-recovery claims.","MEASUREMENT GATE"]],bottom:"Literature • historical thermal/size analyses • accounting code • safety and NCSC planning",source:"AGASTYA project index, current engineering overview, EYE README, and data guide",claim:"Current AGASTYA components and evidence workstreams",limit:"This map combines active software and documentation with proposed, unvalidated process stages."},
{type:"flow",kicker:"03 • research question",title:"What can a material balance prove?",sub:"Each measurement must stay attached to the material stream it describes.",items:[["Identify","sample + source"],["Weigh","all streams"],["Separate","matched feed"],["Assay","qualified lab"],["Calculate","yield + Ag"]],body:"How can a defined PV feed be prepared and silver removed with traceable mass and silver balances?",side:"Define the Stage 3 output; compare Stage 4 silver-removal routes only against characterized feed and measured balances.",source:"AGASTYA Phase B/C accounting model",claim:"Research question and proposed material-accounting method",limit:"Plan only; no physical sample or assay data."},
{type:"stages",kicker:"04 • current architecture",title:"Four stages, one evidence chain",sub:"This is the current charter; older files use different stage numbers.",items:[["01  Inspection + routing","Identify and inspect the module; route it for reuse, hold or Stage 2 preparation.","NO UNIT OPERATION TESTED"],["02  Manual mechanical preparation","Remove accessible components and prepare a traceable laminate feed for Stage 3.","VIRTUAL SCENARIOS ONLY"],["03  Thermal treatment / delamination","Reference output: sheet glass plus cell/EVA/backsheet laminate; no Ag liberation is implied.","LITERATURE REFERENCE"],["04  Silver removal / recovery","Route open; define the feed, product form, facility and receiver criteria.","ROUTE OPEN"]],source:"AGASTYA architecture crosswalk and current engineering overview",claim:"Current four-stage project architecture",limit:"Proposed system; stage performance is not validated."},
{type:"eye",kicker:"05 • AGASTYA-EYE",title:"An inspection and record tool—not a silver detector",sub:"EYE supports the Stage 1 intake; it is separate from material separation.",steps:[["Capture","Panel photos + context"],["Review","Operator checks evidence"],["Record","Versioned material passport"],["Route","Human-reviewed handoff"]],left:"The app records image provenance, operator-entered dimensions and nameplate/electrical observations, plus stage events. Optional low-voltage sensor data are documented separately.",right:"A camera cannot measure voltage, size or silver. The image classifier is experimental and does not confirm defects, composition, recovery or purity. No actuator is commanded.",bottom:"Computer-vision suggestions remain advisory; the operator makes the route decision.",source:"Agastya-EYE README, Stage 1 app documentation, and current charter",claim:"Documented EYE application and data boundaries",limit:"App documentation does not establish real-camera accuracy, physical sorting performance or silver detection.",notes:"Explain that EYE is a digital panel passport and inspection tool. It is not part of silver extraction chemistry and does not measure Ag. The project documents image capture, human-reviewed routing and optional low-voltage sensor records."},
{type:"thermal",kicker:"06 • Stage 3 thermal reference",title:"Thermal delamination is the Stage 3 reference",sub:"A hot knife may split glass from laminate; the reduced model cannot tell whether peeling succeeds.",bottom:"Historical virtual models only • 0 Agastya panels, coupons or assay samples.",source:"Agastya Physics Simulation procedures/results; Stage 3 thermal development notes; IEA PVPS pilot assessment",claim:"Scope and limits of the historical thermal model and optional pretreatment",limit:"The 1-D five-node model does not validate delamination quality, safe settings, fumes, heater energy or retained-heat savings.",notes:"Stage 3 is thermal treatment/delamination; the guarded hot-knife is a literature-based reference, not a built or validated Agastya machine. IEA PVPS Task 12-25:2023, full report reviewed 20 October 2026, describes a pilot-plant inventory with fair data quality; downstream Cu/Ag recovery is further treatment outside its boundary. https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf. NPC (checked 20 October 2026) claims sheet-glass separation for non-broken modules at about 60 seconds per panel with a 300 C knife; this is a vendor claim, not an Agastya setting: https://www.npcgroup.net/eng/solarproduct/dismantling. The numerical model is assumption-based and does not model peel quality, silver recovery, safety or actual heater energy. A 1-D five-node RC model was executed with explicit forward Euler time steps, using assumed literature properties and conditions. It generated historical virtual rows only. The solver does not model fracture, peel force, fume exposure, operator safety, machine power, actual heater energy per panel or separation quality. Do not present the displayed layer stack as apparatus."},
{type:"simulations",kicker:"07 • numerical model data",title:"What the historical 200,080 rows actually contain",sub:"Sensitivity sweeps, time histories and conditional arithmetic—not independent experiments.",cards:[["Routing + balance • 1,536 rows","384 hand-off cases plus 1,152 glass/laminate splits; assumed inputs and mass closure by construction.","HISTORICAL ROUTING + MASS CASES"],["Thermal model • 7,080 rows","5,040 sweeps + 1,944 snapshots + 32 timestep checks + 64 cooldown outputs; no peel-quality prediction.","THERMAL MODEL → CURRENT STAGE 3"],["Feed-prep scenarios • 129,220 rows","129,024 assumed-feed size splits + 196 inverse-cut cases; no measured particle-size feed.","SIZE MODEL → HISTORICAL FEED PREP"],["Ag arithmetic • 62,208 rows","Literature arithmetic and conditional-grade scenarios; no Agastya assay or Stage 4 removal model.","CONDITIONAL CALCULATIONS"]],bottom:"Total includes 36 capacity cases: 200,080 rows. Timestep checks differ by ≤0.155 °C; numerical sensitivity is not physical validation.",source:"Agastya Physics Simulation/PROCEDURES_AND_RESULTS.md, data_dictionary.csv and saved simulation outputs",claim:"Counts and scope of legacy virtual scenario, thermal, size and conditional silver calculations",limit:"All rows are model/scenario outputs. They are not physical observations, independent replicates, measured PSD, assays, or AGASTYA performance."},
{type:"bars",kicker:"08 • literature evidence",title:"Silver can partition into fine fractions",sub:"Published percentages belong to distinct study feeds and screen definitions.",bars:[{label:"Sim 2022 • EVAc",value:70,note:"Up to 70% of study-feed Ag in F4",color:C.teal},{label:"Sim 2022 • MP",value:80,note:"Up to 80% of separate study-feed Ag in F4",color:C.blue},{label:"Juyo Salazar 2024",value:94.12,note:"Ag reported in <0.25 mm fraction for its feed",color:C.gold}],source:"Sim et al. 2022, DOI 10.1016/j.wasman.2022.11.023; Juyo Salazar et al. 2024, DOI 10.1016/j.susmat.2024.e01047",claim:"Study-specific Ag partition to fine size classes",limit:"Not product grade, not a universal recovery interval, and not an AGASTYA result."},
{type:"comparison",kicker:"09 • Stage 4 route comparison",title:"Electrostatic evidence is incomplete for silver",sub:"A plausible mechanism still needs a mass-based silver balance.",cards:[["What one PV study reports","Ag, Al and Si could be co-concentrated; abstract reports 38 kV and 75 rpm.","DIRECT BUT INCOMPLETE"],["What is missing","Accessible abstract does not provide mass-weighted Ag recovery, product grade or full product masses.","KEY METRICS"],["Separate silicon result","Another paper reports 91.0% Si proportion and 48.9% Si recovery. Those are not Ag metrics.","DO NOT SUBSTITUTE"]],callout:"ELECTROSTATIC SEPARATION IS AN UNSELECTED COMPARATOR — NOT AN AGASTYA RECOVERY RESULT.",source:"de Souza & Veit 2023, DOI 10.1016/j.cec.2023.100027; Li et al. 2023, DOI 10.1016/j.jclepro.2023.137908",claim:"Electrostatic PV scrap evidence and limits",limit:"de Souza & Veit reports co-concentration in a different prepared feed; no accessible Ag recovery/grade or complete balance. This is a Stage 4 comparator, not an Agastya route or Stage 3."},
{type:"comparison",kicker:"10 • direct silver benchmark",title:"A strong result on a different feed",sub:"Bench flotation results show what assay-based reporting can look like.",cards:[["Tap-water rougher","97.55 ± 0.03% Ag recovery; 32.2 ± 2.3× upgrade; triplicate bench tests.","REPORTED BY AUTHORS"],["Rougher–cleaner","46.7 ± 1.5 wt% Ag concentrate at 86.5 ± 2.8% recovery.","SEPARATE CONDITION"],["Feed boundary","Prepared, delaminated and ground cells; reagents at 150 g/t. Not whole-panel or AGASTYA feed.","NOT TRANSFERABLE"]],callout:"Published flotation benchmark • do not multiply by unrelated AGASTYA stage yields.",source:"Saffarian, Galvin & Firouzi 2026, DOI 10.1016/j.mineng.2026.110189",claim:"Reported silver flotation recovery, upgrade, grade and study feed",limit:"Bench study on prepared cell feed; not AGASTYA performance or school-scale method."},
{type:"equations",kicker:"11 • All-stage measurement",title:"Four different quantities answer four questions",sub:"Sampling, assays and mass accounting validate every stage and support the silver balance.",cards:[["Mass yield","Target stream mass ÷ feed mass × 100","HOW MUCH MATERIAL"],["Ag grade","Ag mass in product ÷ product mass × 100","HOW RICH"],["Ag recovery","Ag mass in target ÷ Ag mass in feed × 100","HOW MUCH Ag"],["Balance residual","Input mass − outputs − recorded loss","WHAT IS UNACCOUNTED"]],source:"AGASTYA Phase B/C accounting definitions; EPA methods listed in evidence register as assay references",claim:"Definitions used by AGASTYA accounting validation",limit:"No AGASTYA assay or measured stream mass exists."},
{type:"scenarios",kicker:"12 • normalized literature arithmetic",title:"Reference values have different limits",sub:"Normalization shows arithmetic only; it does not create an AGASTYA feed assay.",cards:[["Review composition • 300 ppm","0.300 g Ag / kg","Secondary-source scenario; sample basis unresolved"],["Dias abstract • 600 g/t","0.600 g Ag / kg","Publisher abstract; distinct study basis"],["630 g/t excerpt","UNRESOLVED","Secondary conclusion excerpt; not used as verified input"]],source:"Mulazzani et al. 2022, DOI 10.3390/en15228419; Dias et al. 2016, DOI 10.1016/j.wasman.2016.03.016",claim:"Source-qualified normalized arithmetic for distinct literature values",limit:"The 300 ppm provenance and 600/630 g/t discrepancy/denominator need further review. None is an AGASTYA assay."},
{type:"tools",kicker:"13 • programmes and simulations",title:"The tools match the evidence we have",sub:"Use a reduced model for sensitivity analysis; choose solvers only after inputs exist.",left:"CPython 3.14.4 generated the historical simulation/scenario files and accounting checks.\n\nNumPy 2.5.3 vectorized the five-node thermal RC model, integrated with explicit forward Euler.\n\nPowerShell 7.6.5 launched scripts; it did not calculate the physics.",right:"No Ansys Maxwell, Rocky, DEM, CFD, finite-element, electrostatic or chemistry solver was run.\n\nNo sample CAD, charge-to-mass characterization, assay instrument output or approved lab access is documented.",bottom:"200,080 historical virtual rows • 0 panels • 0 coupons • 0 particle or assay samples",source:"Local runtime audit; simulation procedures/results; software inventory",claim:"Actually used software and model scope",limit:"No multiphysics solver, physical trial or assay run in this phase."},
{type:"scorecard",kicker:"14 • project status",title:"What is done — and what is not",sub:"These counts describe documented work and software checks, not experiments.",cards:[["14","evidence records",C.teal],["3","literature arithmetic rows",C.blue],["28/28","accounting tests pass",C.gold],["42/42","EYE software tests pass",C.green]],left:"Source-qualified research, route comparison, thermal/size sensitivities, accounting definitions and transparent unknowns are documented.",right:"0 physical samples • 0 assays • 0 electrostatic/chemistry solver runs. Three known failure guards remain in the legacy Phase A validation kernel.",source:"Phase B/C data, accounting suite and EYE test results",claim:"Counts of source records, arithmetic rows and executed software test suites",limit:"Software tests do not establish hardware behavior, model accuracy or recovery performance."},
{type:"gates",kicker:"15 • next validation plan",title:"Close the evidence gaps in order",sub:"This is a future supervised plan, not a completed experiment.",items:[["Identify the feed","Source, technology, condition, sample ID and custody."],["Confirm sample + host","Verify traceable c-Si feed, facility acceptance, supervision and waste route."],["Plan thermal Stage 3","Cold fixture review; approved instruments and supervised trial plan."],["Plan Stage 3 trial","Approved facility, guarded fixture, calibrated temperature/time/mass records."]],callout:"No test until facility, supervisor, safety controls, assay and disposal are confirmed.",source:"AGASTYA validation plan v2",claim:"Proposed staged validation gates",limit:"Not performed; requires an authorized supervised facility."},
{type:"tradeoffs",kicker:"16 • sustainability",title:"Environmental benefit must be measured",sub:"Recovery is only one part of a responsible route.",left:"Potential questions: preserve second-life options; reduce mixed-material disposal; quantify what share of Ag enters a useful stream; compare local transport and handoff.",right:"Measure the burdens too: energy, time, dust, rejects, packaging, transport, reagents, wastewater and receiver limits. No lifecycle, cost or emissions benefit is established.",bottom:"A useful result can be a clear no-go when the material balance or handoff fails.",source:"AGASTYA sustainability boundary and reviewed PV recycling literature",claim:"Proposed sustainability comparison boundary",limit:"Potential benefits only; no measured environmental or economic result."},
{type:"references",kicker:"17 • sources and evidence",title:"Primary references used in this deck",sub:"Study results are attributed to their reported feed and methods.",items:[["Sim et al. (2022) • crush-and-sieve PV recycling","Waste Management • DOI 10.1016/j.wasman.2022.11.023"],["de Souza & Veit (2023) • electrostatic Ag/Al/Si co-concentration","Circular Economy • DOI 10.1016/j.cec.2023.100027"],["Saffarian et al. (2026) • flotation","Minerals Engineering 242 • DOI 10.1016/j.mineng.2026.110189"],["Juyo Salazar et al. (2024) • fine fraction","Sustainable Materials and Technologies • DOI 10.1016/j.susmat.2024.e01047"],["Mulazzani et al. (2022) • module composition review","Energies 15(22) • DOI 10.3390/en15228419"],["Dias et al. (2016) • Ag benchmark","Waste Management • DOI 10.1016/j.wasman.2016.03.016"],["NCSC Activity Guidebook 2026–27 • DST","Official guide: dst.gov.in/sites/default/files/Activity-Guidebook-for-NCSC-2026-27_0.pdf"]],source:"Primary research and official DST guidebook listing",claim:"References for evidence claims in this presentation",limit:"Full extraction status and source boundaries are recorded in the evidence database."},
{type:"closing",kicker:"CONCLUSION • NEXT MEASUREMENT",title:"Build the evidence chain first",sub:"",hero:"A clear route.",body:"A measured stream, a qualified assay and a closed, honest balance are the next proof points.",status:"CURRENT CLAIM: RESEARCH FRAMEWORK • NO RECOVERY RESULT",left:"We have a literature-grounded architecture and a tested accounting framework. Published routes use different feed and metric bases.",right:"Next: define the Stage 3/4 interface, confirm a traceable feed and qualified host, then measure streams and assay every stage.",notes:"Close by stating what is established and what is not. Invite questions about the measurement plan, not a claimed silver yield."}
];

const short = [
master[0],
master[2],
master[4],
master[5],
master[6],
master[7],
master[8],
master[9],
master[10],
master[11],
master[13],
master[14],
master[15],
master[17],
master[18]
];

async function build(specs,file,name) {
  const deckSpeaker=[];
  const startNotes=speaker.length;
  specs.forEach((sp,i)=>slideFor(sp,i+1,name));
  await pptx.writeFile({fileName:path.join(OUT,file)});
  return {startNotes,endNotes:speaker.length};
}
(async()=>{
  // New presentation object per deck, since PptxGenJS owns a single slide list.
  // Draft generator only: never overwrite the artifact-reviewed r2 final files.
  const generated = "Working_Drafts/Generated";
  fs.mkdirSync(path.join(OUT,generated),{recursive:true});
  await build(master,`${generated}/AGASTYA_MASTER_PRESENTATION_DRAFT_2026-10-20.pptx`,"MASTER");
  pptx = new P();
  pptx.layout="LAYOUT_WIDE"; pptx.author="AGASTYA research team"; pptx.title="AGASTYA — NCSC research summary"; pptx.lang="en-IN"; pptx.theme={headFontFace:"Arial",bodyFontFace:"Arial",lang:"en-IN"};
  short.forEach((sp,i)=>slideFor(sp,i+1,"NCSC SHORT"));
  await pptx.writeFile({fileName:path.join(OUT,generated,"AGASTYA_NCSC_SHORT_PRESENTATION_DRAFT_2026-10-20.pptx")});
  fs.writeFileSync(path.join(OUT,generated,"AGASTYA_PRESENTATION_SPEAKER_NOTES_DRAFT_2026-10-20.md"),"# AGASTYA speaker notes draft\n\n"+speaker.join("\n"),"utf8");
  const csv=(rows)=>rows.map(row=>row.map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(",")).join("\r\n")+"\r\n";
  fs.writeFileSync(path.join(OUT,generated,"AGASTYA_SLIDE_EVIDENCE_REGISTER_DRAFT_2026-10-20.csv"),csv([["deck","slide","title","claim","source","limitation"],...evidence]),"utf8");
  fs.writeFileSync(path.join(OUT,generated,"AGASTYA_VISUAL_ASSET_REGISTER_DRAFT_2026-10-20.csv"),csv([["deck","slide","visual","asset type","provenance"],...assets]),"utf8");
  console.log("Built master and NCSC short presentations; notes and registers written.");
})().catch(e=>{console.error(e);process.exit(1);});

