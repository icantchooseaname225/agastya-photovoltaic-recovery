const pptxgen = require('pptxgenjs');
const JSZip = require('jszip');
const sharp = require('sharp');
const fs = require('fs');

const OUT = 'D:/Agastya/05_Presentation/Working_Drafts/Build_Utilities/Agastya_Presentation_Enhanced_REBUILT.pptx';
const W = 13.333, H = 7.5;
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Agastya Project Team';
pptx.subject = 'Evidence-led solar module recovery concept';
pptx.title = 'Agastya - Give every solar panel a second chance';
pptx.company = 'Agastya';
pptx.lang = 'en-US';
pptx.theme = {
  headFontFace: 'Cambria', bodyFontFace: 'Arial', lang: 'en-US'
};

const C = {
  ink: '0A252B', ink2: '12383D', dark: '07191E', dark2: '0D282E', dark3: '13373B',
  paper: 'F4F8F6', white: 'FFFFFF', mint: '5CE1C1', teal: '008C83', teal2: '176E6A',
  lime: 'C8F16A', coral: 'FF8066', gold: 'F3C969', steel: '668087', muted: '577077',
  paleMint: 'E4F5EE', paleBlue: 'E7F0F0', paleGold: 'FFF1D2', paleCoral: 'FCE9E3',
  line: 'D5E2DE', slate: 'A8BEC0', cell1: '174A62', cell2: '1E5E73', cell3: '236D7D'
};
const F = { title: 'Cambria', body: 'Arial' };
const ST = pptx.ShapeType;

function rect(s, x, y, w, h, fill, opts = {}) {
  const type = opts.round === false ? ST.rect : ST.roundRect;
  s.addShape(type, {
    x, y, w, h,
    rectRadius: opts.radius || 0.12,
    fill: fill ? { color: fill, transparency: opts.transparency || 0 } : { color: 'FFFFFF', transparency: 100 },
    line: opts.line ? { color: opts.line, width: opts.lineWidth || 0.8, transparency: opts.lineTransparency || 0 } : { color: fill || 'FFFFFF', transparency: 100, width: 0 },
    ...(opts.rotate ? { rotate: opts.rotate } : {})
  });
}
function ellipse(s, x, y, w, h, fill, lineColor, lineWidth = 1, transparency = 0) {
  s.addShape(ST.ellipse, {
    x, y, w, h,
    fill: fill ? { color: fill, transparency } : { color: 'FFFFFF', transparency: 100 },
    line: { color: lineColor || fill || 'FFFFFF', width: lineWidth, transparency: lineColor ? 0 : 100 }
  });
}
function line(s, x1, y1, x2, y2, color, width = 1.2, opts = {}) {
  s.addShape(ST.line, {
    x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color, width, transparency: opts.transparency || 0, ...(opts.dash ? { dash: opts.dash } : {}) }
  });
}
function txt(s, text, x, y, w, h, o = {}) {
  s.addText(text, {
    x, y, w, h, isTextBox: true, margin: 0,
    fontFace: o.fontFace || F.body, fontSize: o.fontSize || 14,
    color: o.color || C.ink, bold: o.bold || false, italic: o.italic || false,
    charSpacing: o.charSpacing || 0,
    breakLine: false, valign: o.valign || 'mid', align: o.align || 'left',
    paraSpaceAfterPt: 0, lineSpacingMultiple: 1.0,
    ...(o.fit ? { fit: o.fit } : {}),
    ...(o.hyperlink ? { hyperlink: { url: o.hyperlink } } : {}),
    ...(o.transparency ? { transparency: o.transparency } : {})
  });
}
function pill(s, label, x, y, w, color, bg, dark = false) {
  rect(s, x, y, w, 0.28, bg, { line: bg, radius: 0.1 });
  txt(s, label.toUpperCase(), x + 0.08, y + 0.015, w - 0.16, 0.24, {
    fontSize: 8.5, bold: true, charSpacing: 0.9, color: color || (dark ? C.mint : C.teal)
  });
}
function card(s, x, y, w, h, dark = false, accent = null) {
  const fill = dark ? C.dark2 : C.white;
  const edge = dark ? '23444A' : C.line;
  rect(s, x, y, w, h, fill, { line: edge, lineWidth: 0.8 });
  if (accent) ellipse(s, x + w - 0.43, y + 0.18, 0.16, 0.16, accent, accent, 0.4);
}

const iconBodies = {
  sun: '<circle cx="128" cy="128" r="39"/><path d="M128 18v31M128 207v31M18 128h31M207 128h31M50 50l22 22M184 184l22 22M206 50l-22 22M72 184l-22 22"/>',
  eye: '<path d="M20 128s38-57 108-57 108 57 108 57-38 57-108 57S20 128 20 128z"/><circle cx="128" cy="128" r="25"/>',
  camera: '<path d="M32 78h40l15-20h82l15 20h40v112H32z"/><circle cx="128" cy="132" r="35"/><path d="M48 96h24"/>',
  check: '<path d="M49 129l48 48 110-117"/>',
  layers: '<path d="M23 80l105-55 105 55-105 55z"/><path d="M23 128l105 55 105-55M23 174l105 55 105-55"/>',
  panel: '<rect x="31" y="43" width="194" height="138" rx="8"/><path d="M31 89h194M31 135h194M95 43v138M160 43v138M128 181v38M91 219h74"/>',
  sieve: '<path d="M36 60h184M48 105h160M60 150h136M73 195h110"/><path d="M52 45v30M80 45v30M108 45v30M136 45v30M164 45v30M192 45v30M70 90v30M98 90v30M126 90v30M154 90v30M182 90v30M88 135v30M116 135v30M144 135v30M172 135v30"/>',
  flask: '<path d="M90 28h76M105 28v66L47 199a18 18 0 0 0 16 27h130a18 18 0 0 0 16-27l-58-105V28"/><path d="M72 171h112M89 144h78"/>',
  shield: '<path d="M128 24l78 31v54c0 54-33 92-78 121-45-29-78-67-78-121V55z"/><path d="M87 124l28 28 57-62"/>',
  database: '<ellipse cx="128" cy="54" rx="80" ry="30"/><path d="M48 54v65c0 17 36 31 80 31s80-14 80-31V54M48 119v65c0 17 36 31 80 31s80-14 80-31v-65"/><path d="M48 119c0 17 36 31 80 31s80-14 80-31"/>',
  truck: '<path d="M28 69h125v104H28zM153 101h44l31 36v36h-75z"/><circle cx="77" cy="187" r="20"/><circle cx="189" cy="187" r="20"/><path d="M176 104v35h44"/>',
  clipboard: '<path d="M76 43h-27v176h158V43h-27M91 29h74v38H91z"/><path d="M80 108h79M80 144h79M80 180h51"/>',
  target: '<circle cx="128" cy="128" r="99"/><circle cx="128" cy="128" r="61"/><circle cx="128" cy="128" r="22"/><path d="M128 128l71-71"/>',
  molecule: '<circle cx="63" cy="69" r="20"/><circle cx="190" cy="73" r="20"/><circle cx="89" cy="190" r="20"/><circle cx="192" cy="183" r="20"/><path d="M82 77l88-1M74 88l8 80M104 186l67-2M177 91l9 72"/>',
  warning: '<path d="M128 26L235 216H21z"/><path d="M128 88v57M128 177v2"/>',
  handoff: '<path d="M27 128h152M135 80l48 48-48 48"/><path d="M35 76v104"/>',
  ruler: '<path d="M32 176L176 32l48 48L80 224z"/><path d="M129 79l16 16M105 103l16 16M81 127l16 16M57 151l16 16"/>'
};
const iconCache = new Map();
async function iconPng(name, color) {
  const key = `${name}:${color}`;
  if (iconCache.has(key)) return iconCache.get(key);
  const body = iconBodies[name] || iconBodies.layers;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><g fill="none" stroke="#${color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">${body}</g></svg>`;
  const png = await sharp(Buffer.from(svg)).resize(512, 512).png().toBuffer();
  const data = `image/png;base64,${png.toString('base64')}`;
  iconCache.set(key, data);
  return data;
}
async function addIcon(s, name, x, y, size, color, bg = null) {
  if (bg) ellipse(s, x, y, size, size, bg, bg, 0.3);
  const inset = bg ? size * 0.22 : 0;
  const d = await iconPng(name, color);
  s.addImage({ data: d, x: x + inset, y: y + inset, w: size - 2 * inset, h: size - 2 * inset });
}

function setBg(s, color) { s.background = { color }; }
function header(s, num, kicker, title, subtitle, dark = false, titleSize = 31) {
  const main = dark ? C.white : C.ink;
  const sub = dark ? 'BDD0CF' : C.muted;
  txt(s, `${String(num).padStart(2, '0')}  /  ${kicker.toUpperCase()}`, 0.68, 0.34, 11.9, 0.24, {
    fontSize: 9, bold: true, charSpacing: 1.6, color: dark ? C.mint : C.teal
  });
  txt(s, title, 0.68, 0.72, 12.0, 0.6, { fontFace: F.title, fontSize: titleSize, bold: true, color: main });
  if (subtitle) txt(s, subtitle, 0.7, 1.39, 11.85, 0.36, { fontSize: 14.5, color: sub });
}
function footer(s, num, dark = false) {
  const tone = dark ? 'A7BFBE' : '6E8588';
  const mark = dark ? C.mint : C.teal;
  rect(s, 0.7, 7.05, 0.10, 0.10, mark, { round: false });
  rect(s, 0.82, 7.05, 0.10, 0.10, dark ? C.lime : C.gold, { round: false });
  txt(s, 'AGASTYA  /  SCIENCE COMPETITION', 1.02, 6.99, 4.3, 0.2, { fontSize: 8, bold: true, charSpacing: 0.65, color: tone });
  txt(s, String(num).padStart(2, '0'), 12.1, 6.98, 0.55, 0.2, { fontSize: 9, bold: true, color: tone, align: 'right' });
}
function note(s, text) { s.addNotes(text); }

async function buildDeck() {

// 01 - Cover
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  ellipse(s, 8.02, 0.55, 4.82, 4.82, null, '1E5657', 1, 100);
  ellipse(s, 8.38, 0.91, 4.10, 4.10, null, '143C43', 0.8, 100);
  ellipse(s, 11.62, 0.92, 0.16, 0.16, C.lime, C.lime, 0.5);
  ellipse(s, 8.03, 4.64, 0.11, 0.11, C.coral, C.coral, 0.4);
  // A crisp, schematic PV module as the hero illustration.
  rect(s, 8.28, 1.28, 4.35, 3.20, '10363E', { line: '367A77', lineWidth: 1.6 });
  rect(s, 8.47, 1.47, 3.97, 2.80, '0B2630', { line: '1D5158', lineWidth: 0.8 });
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 4; c++) {
      const shades = [C.cell1, C.cell2, C.cell3];
      rect(s, 8.62 + c * 0.94, 1.64 + r * 0.84, 0.82, 0.70, shades[(r + c) % shades.length], { line: '4C8A8D', lineWidth: 0.65, radius: 0.04 });
      line(s, 8.68 + c * 0.94, 2.28 + r * 0.84, 9.34 + c * 0.94, 1.70 + r * 0.84, '63AAA2', 0.35, { transparency: 40 });
    }
  }
  // Simplified laminate edge and separate glass/laminate outputs.
  rect(s, 8.48, 4.44, 1.72, 0.18, '86DAD0', { line: '86DAD0', radius: 0.04 });
  rect(s, 8.68, 4.67, 1.72, 0.15, '59767C', { line: '59767C', radius: 0.04 });
  rect(s, 8.88, 4.87, 1.72, 0.13, '354D55', { line: '354D55', radius: 0.04 });
  txt(s, 'PV MATERIALS / A TRACEABLE HAND-OFF', 8.54, 5.24, 4.1, 0.22, { fontSize: 8.8, color: 'A6CECA', bold: true, charSpacing: 1.0, align: 'center' });

  txt(s, '12 OCTOBER 2026  /  SCIENCE COMPETITION', 0.78, 0.77, 6.6, 0.28, { fontSize: 10, bold: true, charSpacing: 1.55, color: C.mint });
  txt(s, 'AGASTYA', 0.75, 1.37, 6.9, 0.92, { fontFace: F.title, fontSize: 51, bold: true, color: C.white });
  txt(s, 'Give every solar panel\na second chance.', 0.8, 2.45, 6.9, 1.38, { fontFace: F.title, fontSize: 30, bold: true, color: C.lime });
  txt(s, 'A mobile, vision-guided concept for responsible end-of-life solar panel processing.', 0.82, 4.03, 6.45, 0.77, { fontSize: 17, color: 'D9E7E4', valign: 'top' });
  const steps = [
    ['01', 'INSPECT', C.mint], ['02', 'SEPARATE', C.lime], ['03', 'MEASURE', C.gold], ['04', 'HAND OFF', C.coral]
  ];
  steps.forEach((a, i) => {
    const x = 0.82 + i * 1.62;
    ellipse(s, x, 5.42, 0.36, 0.36, a[2], a[2], 0.5);
    txt(s, a[0], x, 5.49, 0.36, 0.18, { fontSize: 9, bold: true, color: C.dark, align: 'center' });
    txt(s, a[1], x + 0.46, 5.47, 1.10, 0.20, { fontSize: 9.2, bold: true, charSpacing: 0.6, color: 'DBE9E6' });
  });
  txt(s, 'A research-led concept, not a validated recycling line.', 0.82, 6.45, 6.5, 0.28, { fontSize: 11, color: 'A8BFBE', italic: true });
  txt(s, 'DESIGN + SOFTWARE DEMO', 10.1, 6.63, 2.55, 0.2, { fontSize: 8.5, color: 'BBD0CF', bold: true, charSpacing: 1.0, align: 'right' });
  note(s, 'Opening: introduce Agastya as a research-led concept for the careful recovery and hand-off of end-of-life crystalline-silicon PV materials. Be explicit that this is not a validated recycling line. Project status in this presentation is based on records through 9 October 2026.');
}

// 02 - Materials puzzle
{
  const s = pptx.addSlide(); setBg(s, C.paper);
  header(s, 2, 'The materials challenge', 'A solar module hides many different materials.', 'One panel combines high-volume layers with very small target fractions.');
  card(s, 0.7, 2.02, 7.15, 4.55, false);
  pill(s, 'SIMPLIFIED CRYSTALLINE-SILICON CROSS-SECTION', 0.98, 2.26, 3.55, C.teal, C.paleMint);
  const layers = [
    { y: 2.83, h: 0.55, fill: 'D9E8E9', label: 'TEMPERED FRONT GLASS', sub: 'Protective, high-mass layer', color: C.ink },
    { y: 3.48, h: 0.36, fill: 'B5DCCF', label: 'EVA ENCAPSULANT', sub: 'Bonded polymer', color: C.ink },
    { y: 3.95, h: 0.75, fill: '174F63', label: 'SILICON CELLS + METAL CONTACTS', sub: 'Printed silver traces and copper ribbon', color: C.white },
    { y: 4.82, h: 0.36, fill: 'B5DCCF', label: 'EVA ENCAPSULANT', sub: 'Second bonded layer', color: C.ink },
    { y: 5.29, h: 0.58, fill: '7B9094', label: 'POLYMER BACKSHEET', sub: 'Weather barrier', color: C.white }
  ];
  layers.forEach((a, i) => {
    rect(s, 1.0, a.y, 4.33, a.h, a.fill, { line: 'C6D7D5', lineWidth: 0.55, radius: 0.07 });
    if (i === 2) {
      for (let c = 0; c < 5; c++) rect(s, 1.18 + c * 0.78, 4.09, 0.68, 0.47, c % 2 ? C.cell2 : C.cell1, { line: '75B0A8', lineWidth: 0.5, radius: 0.04 });
      line(s, 1.14, 4.32, 5.2, 4.32, 'D9C773', 1.1);
    }
    txt(s, a.label, 5.62, a.y + (i === 2 ? 0.09 : 0.02), 1.95, 0.20, { fontSize: 10.5, bold: true, color: a.color });
    txt(s, a.sub, 5.62, a.y + (i === 2 ? 0.36 : 0.25), 1.92, 0.2, { fontSize: 9.3, color: i === 2 || i === 4 ? 'DCE7E5' : C.muted });
  });
  txt(s, 'Aluminium frame and junction box sit around the laminate.', 1.0, 6.12, 6.3, 0.2, { fontSize: 10.3, color: C.muted, italic: true });

  card(s, 8.13, 2.02, 4.48, 2.06, false);
  ellipse(s, 8.42, 2.33, 0.58, 0.58, C.paleMint, C.paleMint, 0.4);
  await addIcon(s, 'layers', 8.52, 2.43, 0.38, C.teal);
  txt(s, 'AROUND 70%', 9.22, 2.28, 2.85, 0.53, { fontFace: F.title, fontSize: 30, bold: true, color: C.ink });
  txt(s, 'of module mass is glass', 9.24, 2.89, 2.92, 0.32, { fontSize: 14.5, color: C.muted });
  txt(s, 'Volume matters. A useful process must handle the bulky layers, not just the valuable ones.', 8.43, 3.46, 3.83, 0.40, { fontSize: 11.5, color: C.ink2, valign: 'top' });

  card(s, 8.13, 4.30, 4.48, 2.27, false);
  ellipse(s, 8.42, 4.62, 0.58, 0.58, C.paleGold, C.paleGold, 0.4);
  await addIcon(s, 'molecule', 8.52, 4.72, 0.38, 'A77722');
  txt(s, 'LESS THAN 1%', 9.22, 4.57, 3.08, 0.53, { fontFace: F.title, fontSize: 27, bold: true, color: C.ink });
  txt(s, 'of module mass is silver', 9.24, 5.18, 2.92, 0.32, { fontSize: 14.5, color: C.muted });
  txt(s, 'A small fraction can carry value, but its presence is not proof of a recoverable product.', 8.43, 5.76, 3.83, 0.47, { fontSize: 11.5, color: C.ink2, valign: 'top' });
  txt(s, 'Composition figures are illustrative thesis estimates for c-Si modules, not measurements from Agastya feed. Actual construction varies.', 0.72, 6.72, 11.85, 0.2, { fontSize: 8.5, color: C.muted, italic: true });
  footer(s, 2);
  note(s, 'Explain that module composition varies by design and age. The approximately 70 percent glass and less-than-1-percent silver figures are illustrative values from the Agastya thesis, Section 3.2, Figure 3.1. They are not measured values for an Agastya sample. Aluminum frame and junction box are shown outside the simplified laminate.');
}

// 03 - Triage before recycling
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  header(s, 3, 'Protect value first', 'The first recovery step is a decision.', 'Inspect and review before destructive processing.', true, 33);
  const rows = [
    ['01', 'INSPECT', 'Capture identified panel views and visible condition.', 'camera', C.mint],
    ['02', 'VERIFY', 'Use separate, correctly rated measurements when needed.', 'ruler', C.lime],
    ['03', 'REVIEW', 'A person confirms the route; reuse stays on the table.', 'check', C.gold]
  ];
  for (let i = 0; i < rows.length; i++) {
    const a = rows[i];
    const y = 2.06 + i * 1.30;
    card(s, 0.72, y, 6.45, 1.08, true);
    ellipse(s, 0.98, y + 0.27, 0.48, 0.48, C.dark3, C.dark3, 0.5);
    txt(s, a[0], 0.98, y + 0.39, 0.48, 0.18, { fontSize: 9.5, color: a[4], bold: true, align: 'center' });
    await addIcon(s, a[3], 1.66, y + 0.29, 0.45, a[4]);
    txt(s, a[1], 2.28, y + 0.18, 1.28, 0.28, { fontSize: 15, bold: true, charSpacing: 0.7, color: C.white });
    txt(s, a[2], 3.52, y + 0.17, 3.30, 0.62, { fontSize: 13.2, color: 'C5D8D5' });
  }
  card(s, 7.52, 2.06, 5.08, 3.68, true, C.mint);
  pill(s, 'EARLY MODEL EVIDENCE', 7.88, 2.34, 2.36, C.mint, C.dark3, true);
  txt(s, '84.6%', 7.93, 2.93, 1.86, 0.58, { fontFace: F.title, fontSize: 34, bold: true, color: C.white });
  txt(s, 'accuracy', 7.95, 3.52, 1.85, 0.24, { fontSize: 12, color: 'BDCFCE' });
  line(s, 10.12, 2.94, 10.12, 3.95, '315258', 1.0);
  txt(s, '83.5%', 10.42, 2.93, 1.82, 0.58, { fontFace: F.title, fontSize: 34, bold: true, color: C.lime });
  txt(s, 'macro-F1', 10.44, 3.52, 1.85, 0.24, { fontSize: 12, color: 'BDCFCE' });
  rect(s, 7.88, 4.05, 4.34, 0.015, '315258', { round: false });
  txt(s, '104 images in a grouped internal holdout', 7.92, 4.30, 4.18, 0.31, { fontSize: 13, bold: true, color: C.white });
  txt(s, 'Not field accuracy. RGB images do not measure voltage, current, or silver. EYE remains advisory; people make routing decisions.', 7.92, 4.76, 4.18, 0.70, { fontSize: 12.1, color: 'C5D8D5', valign: 'top' });
  pill(s, 'HUMAN REVIEW STAYS IN CONTROL', 7.91, 5.29, 2.93, C.lime, '243E3C', true);
  footer(s, 3, true);
  note(s, 'The RGB model metrics are the Agastya-EYE full-panel RGB grouped holdout results: 104 images, 84.6 percent accuracy and 83.5 percent macro-F1. They are not field validation and they do not measure voltage, current, condition severity, silver content, or reuse value. An appropriately rated instrument and qualified operator are needed for real-module electrical measurements. EYE is advisory and human reviewed. Source: Agastya-EYE README and model evaluation report.');
}

// 04 - Four-stage concept and evidence status
{
  const s = pptx.addSlide(); setBg(s, C.paper);
  header(s, 4, 'The concept', 'Four stages. Four different evidence levels.', 'The hand-off is clearer when each operation is labelled honestly.');
  const stages = [
    { n: '01', title: 'INSPECT', desc: 'EYE images, panel passport, and human-reviewed triage.', status: 'SOFTWARE DEMO', color: C.teal, icon: 'camera' },
    { n: '02', title: 'DE-FRAME', desc: 'Remove frame and junction box as a design step.', status: 'DESIGN', color: '5B7980', icon: 'ruler' },
    { n: '03', title: 'SEPARATE GLASS', desc: 'Separate front glass from the bonded laminate.', status: 'RESEARCH PLAN', color: '9A7B31', icon: 'layers' },
    { n: '04', title: 'PRE-CONCENTRATE', desc: 'Test contained size cuts and assay every output.', status: 'HYPOTHESIS', color: 'B35A45', icon: 'sieve' }
  ];
  for (let i = 0; i < stages.length; i++) {
    const a = stages[i], x = 0.70 + i * 3.10;
    card(s, x, 2.09, 2.82, 3.05, false);
    ellipse(s, x + 0.25, 2.34, 0.48, 0.48, C.paleMint, C.paleMint, 0.4);
    txt(s, a.n, x + 0.25, 2.46, 0.48, 0.16, { fontSize: 9.5, bold: true, color: a.color, align: 'center' });
    await addIcon(s, a.icon, x + 2.08, 2.32, 0.46, a.color);
    txt(s, a.title, x + 0.26, 3.03, 2.32, 0.50, { fontFace: F.title, fontSize: 17, bold: true, color: C.ink, valign: 'top' });
    txt(s, a.desc, x + 0.26, 3.66, 2.28, 0.69, { fontSize: 12.5, color: C.muted, valign: 'top' });
    pill(s, a.status, x + 0.25, 4.56, 2.14, a.color, i === 3 ? C.paleCoral : C.paleMint);
  }
  // Evidence boundary hand-off
  card(s, 0.70, 5.52, 11.92, 1.08, true);
  await addIcon(s, 'handoff', 0.98, 5.80, 0.48, C.mint);
  txt(s, 'CURRENT STAGE 3 HAND-OFF', 1.67, 5.73, 2.18, 0.21, { fontSize: 9, bold: true, charSpacing: 1.0, color: C.mint });
  txt(s, 'Separated front glass', 1.68, 6.05, 2.85, 0.24, { fontSize: 14, bold: true, color: C.white });
  txt(s, '+', 4.63, 6.02, 0.28, 0.25, { fontSize: 17, bold: true, color: C.lime, align: 'center' });
  txt(s, 'Cell / EVA / backsheet laminate', 5.10, 6.05, 3.50, 0.24, { fontSize: 14, bold: true, color: C.white });
  txt(s, 'NOT AN ESTABLISHED ECS FEED', 9.05, 5.89, 3.15, 0.22, { fontSize: 9.2, bold: true, color: C.gold, charSpacing: 0.7, align: 'right' });
  txt(s, 'No physical Stage 3 or Stage 4 PV-processing trial is documented.', 9.05, 6.18, 3.15, 0.20, { fontSize: 9.4, color: 'BED0CF', align: 'right' });
  footer(s, 4);
  note(s, 'Stage 1 is a software demonstration with a human-reviewed workflow. The other physical process stages remain design, research plan, or hypothesis rather than validated process. The Stage 3 target output in the project build plan is separated front glass and a cell/EVA/backsheet laminate. The proposed heated roller remains unvalidated. No physical PV-processing trial is documented. Sources: Stage 3 Build Plan; Stage 4 Research Completion Brief, updated 9 October 2026.');
}

// 05 - Research pivot
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  header(s, 5, 'The research pivot', 'The actual feed changed the Stage 4 answer.', 'A separator cannot fix a mismatch between the claimed feed and the real material.', true, 32);
  card(s, 0.72, 2.12, 4.22, 3.57, true, C.coral);
  pill(s, 'EARLIER THESIS ASSUMPTION', 1.02, 2.39, 2.65, C.coral, '3E2D2D', true);
  txt(s, 'EVA-stripped\ncell fragments', 1.03, 2.92, 3.48, 0.80, { fontFace: F.title, fontSize: 23, bold: true, color: C.white, valign: 'top' });
  line(s, 1.05, 3.97, 4.43, 3.97, '506A6D', 1.0);
  await addIcon(s, 'panel', 1.08, 4.25, 0.54, C.coral);
  txt(s, 'ROTATING EDDY-CURRENT SEPARATOR', 1.82, 4.29, 2.58, 0.26, { fontSize: 10.5, bold: true, color: 'F0C1B6' });
  txt(s, 'Claimed silver separation', 1.82, 4.65, 2.63, 0.29, { fontSize: 13.2, color: C.white });
  pill(s, 'NOT SUPPORTED FOR Ag FROM Si', 1.05, 5.14, 3.22, C.coral, '3E2D2D', true);

  ellipse(s, 5.25, 3.36, 1.05, 1.05, '3A2B2B', '6B4A43', 0.8);
  await addIcon(s, 'warning', 5.49, 3.60, 0.56, C.coral);
  txt(s, 'FEED\nGAP', 5.28, 4.58, 1.00, 0.56, { fontSize: 10, bold: true, color: 'F4C1B5', align: 'center' });

  card(s, 6.70, 2.12, 5.90, 3.57, true, C.mint);
  pill(s, 'CURRENT RESEARCH HYPOTHESIS', 7.02, 2.39, 2.84, C.mint, '1B3B3D', true);
  const path = [
    ['01', 'Traceable Stage 3 laminate'],
    ['02', 'Supervised, contained size reduction'],
    ['03', 'Multi-cut dry classification'],
    ['04', 'Assay-defined mixed hand-off fraction']
  ];
  path.forEach((a, i) => {
    const y = 2.95 + i * 0.56;
    ellipse(s, 7.05, y + 0.02, 0.31, 0.31, i === 3 ? C.lime : C.dark3, i === 3 ? C.lime : C.dark3, 0.5);
    txt(s, a[0], 7.05, y + 0.08, 0.31, 0.14, { fontSize: 8, bold: true, color: i === 3 ? C.dark : C.mint, align: 'center' });
    txt(s, a[1], 7.56, y, 4.62, 0.36, { fontSize: 14, bold: i === 3, color: i === 3 ? C.lime : C.white });
    if (i < 3) line(s, 7.205, y + 0.33, 7.205, y + 0.54, '436165', 1.0);
  });
  txt(s, 'Keep ECS conditional. Test only if characterization finds liberated conductors in its accepted range.', 7.04, 5.20, 5.13, 0.32, { fontSize: 10.9, color: 'C5D8D5', valign: 'top' });

  rect(s, 0.73, 5.99, 11.88, 0.63, '142F34', { line: '244C4E', lineWidth: 0.7 });
  txt(s, 'A conventional ECS can sort suitable liberated conductors from nonconductors; it is not evidence of silver-from-silicon separation.', 1.02, 6.15, 11.25, 0.28, { fontSize: 12.1, color: 'DBE8E5', align: 'center' });
  footer(s, 5, true);
  note(s, 'The Stage 4 review found the thesis feed assumption unsupported. Stage 3 records show front glass plus cell/EVA/backsheet laminate; a heated roller is unvalidated. A conventional eddy-current separator can sort suitable liberated conductive particles from nonconductors, but the reviewed material did not show it separating printed silver from silicon or turning this laminate into a silver product. The recommended next research hypothesis is a supervised, contained size-classification study with all streams retained and assayed. ECS stays conditional on actual feed characterization. This is not a trial instruction or equipment specification. Source: Stage 4 Research Completion Brief, updated 9 October 2026; Agastya thesis, Section 3.4.5.');
}

// 06 - Potential advantages
{
  const s = pptx.addSlide(); setBg(s, C.paper);
  header(s, 6, 'Advantages', 'What is promising about the Agastya design?', 'These are potential design advantages, not measured outcomes.', false, 31);
  pill(s, 'POTENTIAL ADVANTAGES - NOT PROVEN BENEFITS', 0.72, 1.82, 3.68, C.teal, C.paleMint);
  const items = [
    { x: 0.72, y: 2.30, icon: 'check', color: C.teal, tint: C.paleMint, title: 'Triage before teardown', body: 'A visual review plus separate checks can keep a second-life route visible before destructive recycling.' },
    { x: 6.80, y: 2.30, icon: 'truck', color: '4F7780', tint: C.paleBlue, title: 'Designed for distributed sites', body: 'A mobile concept could help aggregate small, scattered sources. Transport savings have not been measured.' },
    { x: 0.72, y: 4.20, icon: 'layers', color: '8B712F', tint: C.paleGold, title: 'Dry onboard boundary', body: 'The current concept avoids onboard acid or solvent processing; specialist downstream work stays external.' },
    { x: 6.80, y: 4.20, icon: 'database', color: '9B5C4A', tint: C.paleCoral, title: 'A traceability foundation', body: 'Panel passports and ordered stage records can support lineage, measured outputs, and accountable hand-off.' }
  ];
  for (const a of items) {
    card(s, a.x, a.y, 5.81, 1.62, false);
    ellipse(s, a.x + 0.25, a.y + 0.42, 0.68, 0.68, a.tint, a.tint, 0.4);
    await addIcon(s, a.icon, a.x + 0.40, a.y + 0.57, 0.38, a.color);
    txt(s, a.title, a.x + 1.12, a.y + 0.26, 4.27, 0.32, { fontFace: F.title, fontSize: 18, bold: true, color: C.ink });
    txt(s, a.body, a.x + 1.12, a.y + 0.70, 4.28, 0.62, { fontSize: 13, color: C.muted, valign: 'top' });
  }
  txt(s, 'A fair comparison still needs a measured baseline against a qualified stationary route.', 0.76, 6.27, 11.82, 0.29, { fontSize: 12.2, bold: true, color: C.ink2, align: 'center' });
  footer(s, 6);
  note(s, 'Use conditional language. The mobile architecture, reuse-first triage, dry onboard boundary, and traceability records are promising design features. None establishes transport savings, environmental benefit, operational throughput, lower cost, or a better recovery result. A fair evaluation would compare an agreed feed and receiver pathway against an appropriate existing route.');
}

// 07 - Limitations / disadvantages
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  header(s, 7, 'Disadvantages and limitations', 'The open gaps are as important as the idea.', 'A competition claim is stronger when the unfinished work is visible.', true, 32);
  const items = [
    { x: 0.72, y: 2.07, icon: 'warning', color: C.coral, title: 'No validated recycling line', body: 'No physical Stage 3 or Stage 4 PV-processing trial is documented. Throughput, yield, and energy remain unmeasured.' },
    { x: 6.80, y: 2.07, icon: 'layers', color: C.gold, title: 'The feed does not match the claim', body: 'The current laminate still contains cell, EVA, and backsheet layers. It is not an established ECS feed.' },
    { x: 0.72, y: 4.02, icon: 'camera', color: C.mint, title: 'The AI evidence is limited', body: 'The 104-image holdout is not field validation. RGB imagery cannot assay silver or replace electrical testing.' },
    { x: 6.80, y: 4.02, icon: 'target', color: '84B7D0', title: 'Feasibility is still unknown', body: 'Feed access, supervised facility, assay quote, receiver acceptance, transport, and local costs are unverified.' }
  ];
  for (const a of items) {
    card(s, a.x, a.y, 5.81, 1.64, true, a.color);
    ellipse(s, a.x + 0.24, a.y + 0.40, 0.68, 0.68, C.dark3, C.dark3, 0.4);
    await addIcon(s, a.icon, a.x + 0.39, a.y + 0.55, 0.38, a.color);
    txt(s, a.title, a.x + 1.10, a.y + 0.25, 4.33, 0.32, { fontFace: F.title, fontSize: 17.5, bold: true, color: C.white });
    txt(s, a.body, a.x + 1.10, a.y + 0.70, 4.35, 0.64, { fontSize: 12.7, color: 'C0D2D0', valign: 'top' });
  }
  txt(s, 'UNKNOWN IN OUR RECORDS DOES NOT MEAN UNAVAILABLE IN THE REAL WORLD.', 1.02, 6.13, 11.20, 0.25, { fontSize: 10.3, bold: true, charSpacing: 0.65, color: C.lime, align: 'center' });
  footer(s, 7, true);
  note(s, 'Explicit disadvantages and limitations: no physical PV-processing validation, no measured throughput, energy, yield or unit economics; Stage 3 laminate is not an established ECS feed; model performance is an internal grouped holdout, not a field test; and real feed, facility, assay, receiver and local cost status is unverified in project records. Say unknown or unverified, not unavailable.');
}

// 08 - Route comparison
{
  const s = pptx.addSlide(); setBg(s, C.paper);
  header(s, 8, 'Choose by target', 'Different material targets need different routes.', 'Keep dry pre-concentration, conductive sorting, and silver extraction separate.', false, 31);
  const cards = [
    { x: 0.70, color: C.teal, tint: C.paleMint, icon: 'sieve', badge: 'BEST-ALIGNED HYPOTHESIS', title: 'Dry size classification', target: 'Smaller mixed Ag-bearing hand-off fraction', body: 'Contained size cuts on traceable laminate; retain and assay every fraction.', fit: 'Unproven on Agastya feed' },
    { x: 4.78, color: '5A7981', tint: C.paleBlue, icon: 'panel', badge: 'CONDITIONAL COMPARATOR', title: 'Eddy-current sorting', target: 'Coarse conductive / nonconductive split', body: 'Consider only if characterization finds liberated particles in the separator range.', fit: 'Not silver-from-silicon' },
    { x: 8.86, color: 'B35A45', tint: C.paleCoral, icon: 'flask', badge: 'LAB BENCHMARK ONLY', title: 'Froth flotation', target: 'Higher-grade silver concentrate', body: 'Wet, reagent-based research path on prepared and delaminated cell feed.', fit: 'Outside dry mobile boundary' }
  ];
  for (let i = 0; i < cards.length; i++) {
    const a = cards[i];
    card(s, a.x, 2.05, 3.76, 4.35, false, a.color);
    ellipse(s, a.x + 0.25, 2.30, 0.64, 0.64, a.tint, a.tint, 0.4);
    await addIcon(s, a.icon, a.x + 0.38, 2.43, 0.38, a.color);
    pill(s, a.badge, a.x + 1.00, 2.46, 2.43, a.color, a.tint);
    txt(s, a.title, a.x + 0.27, 3.12, 3.20, 0.46, { fontFace: F.title, fontSize: 19, bold: true, color: C.ink });
    txt(s, 'TARGET', a.x + 0.28, 3.73, 1.02, 0.20, { fontSize: 8.6, bold: true, charSpacing: 0.8, color: a.color });
    txt(s, a.target, a.x + 0.28, 3.98, 3.18, 0.47, { fontSize: 12.4, bold: true, color: C.ink2, valign: 'top' });
    txt(s, a.body, a.x + 0.28, 4.56, 3.18, 0.65, { fontSize: 11.4, color: C.muted, valign: 'top' });
    line(s, a.x + 0.28, 5.33, a.x + 3.45, 5.33, C.line, 0.75);
    txt(s, 'FIT NOW', a.x + 0.28, 5.50, 1.0, 0.18, { fontSize: 8.6, bold: true, charSpacing: 0.8, color: a.color });
    txt(s, a.fit, a.x + 0.28, 5.76, 3.18, 0.30, { fontSize: 12.2, bold: true, color: C.ink });
  }
  rect(s, 0.70, 6.56, 11.92, 0.32, C.ink, { line: C.ink });
  txt(s, 'PUBLISHED FLOTATION BENCHMARK: 97.55% Ag recovery / 32.2 times upgrade in one tap-water rougher test; not an Agastya result.', 0.91, 6.61, 11.48, 0.19, { fontSize: 9.4, bold: true, color: C.white, align: 'center' });
  footer(s, 8);
  note(s, 'The Stage 4 literature review ranks contained comminution and multi-cut dry classification as the best-aligned hypothesis for a smaller mixed fraction, but explicitly unverified on Agastya laminate. A conventional ECS is only a later conditional comparator for an eligible liberated conductor stream, not an Ag-from-Si separator. The 2026 Saffarian, Galvin and Firouzi flotation paper reports 97.55 percent Ag recovery and 32.2 times upgrade for one tap-water rougher test on prepared feed; a separate rougher-cleaner result is approximately 47 wt percent Ag at 86.5 percent recovery. These are separate laboratory results on prepared/delaminated material and not Agastya outcomes. Flotation uses water and reagents and is outside the current dry mobile boundary. DOI: https://doi.org/10.1016/j.mineng.2026.110189');
}

// 09 - Experiment design and measures
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  header(s, 9, 'A defensible test', 'A fair test follows every fraction.', 'Compare matched portions of the same traceable feed; do not discard dust or residues.', true, 33);
  // left-hand study logic
  card(s, 0.72, 2.10, 6.15, 4.28, true);
  pill(s, 'STUDY OUTLINE ONLY', 1.02, 2.36, 1.82, C.lime, C.dark3, true);
  ellipse(s, 1.07, 3.15, 0.56, 0.56, '18434A', '18434A', 0.4);
  await addIcon(s, 'panel', 1.18, 3.26, 0.34, C.mint);
  txt(s, 'Traceable, characterized feed', 1.82, 3.20, 4.43, 0.35, { fontSize: 14, bold: true, color: C.white });
  line(s, 1.35, 3.74, 1.35, 4.05, '426265', 1.2);
  line(s, 1.35, 4.05, 2.08, 4.05, '426265', 1.2);
  line(s, 1.35, 4.05, 4.42, 4.05, '426265', 1.2);
  card(s, 1.02, 4.16, 2.65, 1.18, true);
  txt(s, 'BASELINE', 1.28, 4.39, 2.15, 0.22, { fontSize: 10, bold: true, charSpacing: 0.8, color: C.mint });
  txt(s, 'Untreated aliquot\nfeed assay + mass', 1.28, 4.72, 2.15, 0.48, { fontSize: 12, color: 'D4E2DF', valign: 'top' });
  card(s, 3.98, 4.16, 2.60, 1.18, true);
  txt(s, 'COMPARISON', 4.25, 4.39, 2.07, 0.22, { fontSize: 10, bold: true, charSpacing: 0.8, color: C.lime });
  txt(s, 'Matched feed; all cuts, dust, samples, and residues retained', 4.25, 4.72, 2.07, 0.48, { fontSize: 11.2, color: 'D4E2DF', valign: 'top' });
  txt(s, 'Only after facility approval, agreed sampling, and receiver criteria.', 1.05, 5.70, 5.46, 0.33, { fontSize: 10.6, italic: true, color: 'AFC7C4', align: 'center' });

  card(s, 7.15, 2.10, 5.46, 4.28, true, C.lime);
  pill(s, 'REPORT THESE SEPARATELY', 7.48, 2.36, 2.65, C.mint, C.dark3, true);
  const metrics = [
    ['Ag grade', 'Ag mass / fraction mass'], ['Ag recovery', 'Ag in target / Ag in feed'],
    ['Mass yield', 'Target mass / feed mass'], ['Enrichment', 'Product grade / feed grade'],
    ['Mass closure', 'Account for all inputs and outputs'], ['Uncertainty', 'Sampling + assay variation'],
    ['Energy + time', 'Meter actual operation'], ['Actual cost', 'Include facility + hand-off']
  ];
  metrics.forEach((a, i) => {
    const col = i % 2, row = Math.floor(i / 2), x = 7.48 + col * 2.47, y = 2.94 + row * 0.73;
    rect(s, x, y, 2.25, 0.60, '12343A', { line: '25494D', lineWidth: 0.65 });
    txt(s, a[0], x + 0.12, y + 0.09, 2.00, 0.20, { fontSize: 10.7, bold: true, color: i < 4 ? C.lime : C.mint });
    txt(s, a[1], x + 0.12, y + 0.33, 2.00, 0.18, { fontSize: 8.7, color: 'C3D6D3' });
  });
  footer(s, 9, true);
  note(s, 'This is a study-design outline for an appropriately qualified, supervisor-approved facility, not instructions to operate a crusher or separator. Before any physical work, agree the target, feed identity, receiver specification, facility approval, containment, assay method, sample preparation, uncertainty, and mass-closure tolerance. Compare an untreated aliquot with matched-feed size-classification results and retain every size cut, sample withdrawal, dust catch, and residue. Report Ag grade, Ag recovery, mass yield, enrichment, mass closure, uncertainty, energy, time, actual cost, and receiver acceptance separately. Source: Stage 4 Research Completion Brief.');
}

// 10 - Material data lineage
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  header(s, 10, 'The data layer', 'Give every output a parent and a passport.', 'A measurement is useful only when it remains attached to the material it describes.', true, 32);
  const nodes = [
    ['PANEL', 'panel_id', 'camera'],
    ['STAGE EVENT', 'measured record', 'clipboard'],
    ['STREAM / BATCH', 'parent IDs + mass', 'layers'],
    ['ALIQUOT / CUT', 'prep + size range', 'sieve'],
    ['ASSAY', 'method + lab', 'flask'],
    ['RECEIVER LOT', 'acceptance record', 'handoff']
  ];
  for (let i = 0; i < nodes.length; i++) {
    const x = 0.64 + i * 2.02;
    card(s, x, 2.45, 1.77, 2.00, true, i === 4 ? C.lime : C.mint);
    ellipse(s, x + 0.54, 2.70, 0.68, 0.68, '163C41', '163C41', 0.4);
    await addIcon(s, nodes[i][2], x + 0.69, 2.85, 0.38, i === 4 ? C.lime : C.mint);
    txt(s, nodes[i][0], x + 0.12, 3.58, 1.53, 0.29, { fontSize: 10.1, bold: true, color: C.white, align: 'center' });
    txt(s, nodes[i][1], x + 0.10, 3.97, 1.57, 0.20, { fontSize: 9.6, color: 'B9CECC', align: 'center' });
    if (i < nodes.length - 1) {
      line(s, x + 1.79, 3.44, x + 1.98, 3.44, C.lime, 1.1);
      ellipse(s, x + 1.92, 3.38, 0.11, 0.11, C.lime, C.lime, 0.3);
    }
  }
  card(s, 0.72, 4.92, 5.79, 1.39, true);
  pill(s, 'EYE TODAY', 1.02, 5.16, 1.23, C.mint, C.dark3, true);
  txt(s, 'Panel passports, image provenance, human-reviewed routes, and ordered Stage 2-4 event records.', 1.03, 5.55, 5.05, 0.51, { fontSize: 12.2, color: 'D2E1DE', valign: 'top' });
  card(s, 6.82, 4.92, 5.79, 1.39, true);
  pill(s, 'NEXT SOFTWARE STEP', 7.12, 5.16, 2.11, C.lime, '263E3A', true);
  txt(s, 'Track splits, pooled batches, aliquots, assay lineage, and deterministic mass balance without overwriting source records.', 7.13, 5.55, 5.10, 0.52, { fontSize: 12.2, color: 'D2E1DE', valign: 'top' });
  txt(s, 'RGB IMAGE IS NOT AN ELEMENTAL ASSAY. LABORATORY ASSAY REMAINS THE GROUND TRUTH.', 1.0, 6.56, 11.32, 0.22, { fontSize: 9.4, bold: true, charSpacing: 0.7, color: C.gold, align: 'center' });
  footer(s, 10, true);
  note(s, 'The existing EYE software has panel passports, image provenance, human-reviewed routing, and ordered measured Stage 2-4 event records. The next software gap is lineage through stream, batch, aliquot, fraction, assay, and receiver lot, plus deterministic calculations with provenance and uncertainty. Build calculations before process machine learning; there is no Agastya Stage 4 assay dataset. RGB images cannot predict silver grade. Sources: Agastya-EYE README; Stage 4 Software and Model Research; Stage Software Roadmap, 7 October 2026.');
}

// 11 - Safety and full accounting
{
  const s = pptx.addSlide(); setBg(s, C.paper);
  header(s, 11, 'Boundaries and responsibility', 'A strong result counts what the process leaves behind.', 'Safety, utilities, residues, and the real hand-off belong in the measurement boundary.');
  const items = [
    { x: 0.72, y: 2.08, icon: 'shield', color: C.teal, tint: C.paleMint, title: 'People and containment', body: 'Glass edges and fine dust need facility-approved handling, capture, and supervision. No school or home size-reduction trial.' },
    { x: 6.80, y: 2.08, icon: 'sun', color: '957329', tint: C.paleGold, title: 'Real energy and time', body: 'Meter actual electricity and elapsed time. Do not substitute thesis setpoints or modeled throughput for measurements.' },
    { x: 0.72, y: 4.01, icon: 'layers', color: '4F7880', tint: C.paleBlue, title: 'Every residue accounted for', body: 'Label and weigh all cuts, dust catches, withdrawn samples, cleaning residues, and rejected streams.' },
    { x: 6.80, y: 4.01, icon: 'handoff', color: 'A45F4D', tint: C.paleCoral, title: 'A real downstream route', body: 'Record transport, actual fees, packaging, receiver limits, and written acceptance for each material form.' }
  ];
  for (const a of items) {
    card(s, a.x, a.y, 5.81, 1.62, false);
    ellipse(s, a.x + 0.24, a.y + 0.43, 0.65, 0.65, a.tint, a.tint, 0.4);
    await addIcon(s, a.icon, a.x + 0.38, a.y + 0.57, 0.38, a.color);
    txt(s, a.title, a.x + 1.10, a.y + 0.25, 4.35, 0.31, { fontFace: F.title, fontSize: 17.5, bold: true, color: C.ink });
    txt(s, a.body, a.x + 1.10, a.y + 0.68, 4.33, 0.67, { fontSize: 12.2, color: C.muted, valign: 'top' });
  }
  rect(s, 0.72, 6.05, 11.89, 0.58, C.paleGold, { line: 'E8D39F', lineWidth: 0.6 });
  await addIcon(s, 'warning', 0.93, 6.17, 0.34, '9C7520');
  txt(s, 'No validated environmental benefit, cost per kilogram, throughput, or payback claim yet.', 1.47, 6.19, 10.72, 0.24, { fontSize: 12, bold: true, color: C.ink, align: 'center' });
  footer(s, 11);
  note(s, 'Safety and environmental performance are not implied by the word mobile or dry. The project record has no physical PV processing trial. A real study needs facility-approved containment, glass and dust controls, supervision, sample retention, appropriate residual handling, and energy/time measurement. Costs and receiver acceptance are unknown until quotes and written specifications are obtained. Do not claim a net environmental benefit, unit cost, throughput, or payback without a measured boundary. Source: Stage 4 Research Completion Brief; EYE hardware and safety limits in README.');
}

// 12 - Four gates
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  header(s, 12, 'Readiness gates', 'Four gates before any physical trial.', 'Close one unknown at a time, before equipment is selected or operated.', true, 33);
  const gates = [
    { x: 0.72, y: 2.08, n: '01', color: C.mint, icon: 'panel', title: 'VERIFY THE FEED', body: 'Traceable c-Si identity, Stage 3 parent record, dry mass, layers, and representative sample.' },
    { x: 6.80, y: 2.08, n: '02', color: C.lime, icon: 'shield', title: 'SECURE A FACILITY', body: 'Named supervisor, permitted operation, enclosure, dust and glass controls, and residue plan.' },
    { x: 0.72, y: 4.02, n: '03', color: C.gold, icon: 'flask', title: 'AGREE THE ASSAY', body: 'Method, sample preparation, detection limits, uncertainty, and closure tolerance agreed first.' },
    { x: 6.80, y: 4.02, n: '04', color: C.coral, icon: 'handoff', title: 'CONFIRM A RECEIVER', body: 'Written material form, contaminants, batch size, packaging, and acceptance criteria.' }
  ];
  for (const a of gates) {
    card(s, a.x, a.y, 5.81, 1.63, true);
    ellipse(s, a.x + 0.24, a.y + 0.43, 0.58, 0.58, '1A3B40', '1A3B40', 0.4);
    txt(s, a.n, a.x + 0.24, a.y + 0.59, 0.58, 0.16, { fontSize: 9, bold: true, color: a.color, align: 'center' });
    await addIcon(s, a.icon, a.x + 0.98, a.y + 0.51, 0.40, a.color);
    txt(s, a.title, a.x + 1.57, a.y + 0.24, 3.87, 0.31, { fontSize: 13.2, bold: true, charSpacing: 0.5, color: C.white });
    txt(s, a.body, a.x + 1.57, a.y + 0.68, 3.87, 0.67, { fontSize: 12.2, color: 'C1D3D1', valign: 'top' });
  }
  card(s, 0.72, 5.97, 11.89, 0.67, true, C.lime);
  txt(s, 'GO ONLY IF THE RECEIVER ACCEPTS IT, ASSAYS SHOW REPEATABLE IMPROVEMENT, AND MASS CLOSES WITHIN THE AGREED TOLERANCE.', 1.02, 6.16, 11.26, 0.27, { fontSize: 10.5, bold: true, color: C.lime, align: 'center' });
  footer(s, 12, true);
  note(s, 'Before any physical study, verify actual feed, facility, assay, and receiver as four separate gates. The decision rule in the Stage 4 brief is to continue only with the lowest-complexity route that is accepted by the named receiver, demonstrates repeatable assay-backed improvement over untreated feed, closes mass within the agreed tolerance, and is permitted by the facility. ECS remains only if it adds measurable benefit on an eligible feed. If these gates are not met, document a no-go rather than claim a marketable product.');
}

// 13 - Close and collaboration ask
{
  const s = pptx.addSlide(); setBg(s, C.dark);
  ellipse(s, 0.65, 1.09, 6.2, 5.6, null, '174447', 1.1, 100);
  ellipse(s, 1.05, 1.47, 5.4, 4.82, null, '11363D', 0.8, 100);
  txt(s, 'OUR NEXT MILESTONE', 0.83, 0.82, 5.8, 0.25, { fontSize: 9.5, bold: true, charSpacing: 1.65, color: C.mint });
  txt(s, 'Measure first.\nChoose the route second.', 0.81, 1.47, 6.15, 1.65, { fontFace: F.title, fontSize: 36, bold: true, color: C.white, valign: 'top' });
  txt(s, 'A carefully controlled sample can tell us whether a safe, traceable fraction has a real hand-off.', 0.85, 3.50, 5.62, 0.77, { fontSize: 17, color: 'CBDDD9', valign: 'top' });
  await addIcon(s, 'target', 2.46, 4.77, 1.22, C.lime);
  ellipse(s, 4.14, 5.16, 0.16, 0.16, C.coral, C.coral, 0.4);
  ellipse(s, 1.56, 5.67, 0.12, 0.12, C.mint, C.mint, 0.4);
  txt(s, 'The right answer may be a clear no-go.', 0.84, 6.30, 5.52, 0.28, { fontSize: 12, bold: true, italic: true, color: C.lime });

  txt(s, 'WHAT WOULD UNLOCK THE NEXT STUDY?', 7.20, 1.19, 5.14, 0.26, { fontSize: 10, bold: true, charSpacing: 1.2, color: C.gold });
  const asks = [
    ['01', 'Traceable c-Si laminate sample'],
    ['02', 'Qualified, supervised facility'],
    ['03', 'Silver assay + receiver specification']
  ];
  asks.forEach((a, i) => {
    const y = 1.82 + i * 1.12;
    card(s, 7.18, y, 5.14, 0.84, true);
    ellipse(s, 7.43, y + 0.21, 0.42, 0.42, '193A3F', '193A3F', 0.4);
    txt(s, a[0], 7.43, y + 0.32, 0.42, 0.15, { fontSize: 8.5, bold: true, color: i === 2 ? C.lime : C.mint, align: 'center' });
    txt(s, a[1], 8.08, y + 0.20, 3.95, 0.43, { fontSize: 14.2, bold: true, color: C.white });
  });
  txt(s, 'THANK YOU', 7.22, 5.59, 2.02, 0.40, { fontFace: F.title, fontSize: 24, bold: true, color: C.mint });
  txt(s, 'Questions welcome', 7.23, 6.07, 2.48, 0.30, { fontSize: 14, color: 'C5D8D5' });
  txt(s, 'DESIGN THE PATH  /  MEASURE THE MATERIAL', 9.33, 6.20, 2.95, 0.25, { fontSize: 9, bold: true, charSpacing: 0.7, color: C.lime, align: 'right' });
  note(s, 'Close by asking for three possible partners or inputs: a traceable c-Si laminate sample; access to a qualified, supervised facility; and a silver assay method plus a written receiver specification. Emphasize that the next milestone is a controlled study, not equipment procurement. A no-go outcome is acceptable and scientifically useful. Invite questions.');
}

// 14 - Sources
{
  const s = pptx.addSlide(); setBg(s, C.paper);
  header(s, 14, 'Sources', 'Project records and primary research.', 'Numbers and process claims are labelled by evidence type; published results are not Agastya results.');
  const left = [
    ['Agastya project thesis', 'August 2026. Module composition estimates and the earlier Stage 4 concept.'],
    ['Stage 3 Build Plan + Thermal Development', 'Glass separation boundary; thermal values remain assumptions until measured.'],
    ['Stage 4 Research Completion Brief', 'Desk review 8 October; updated 9 October 2026. Current feed, route, and readiness gates.'],
    ['Agastya-EYE README + RGB evaluation', 'Software behavior, grouped holdout metrics, and model limitations.']
  ];
  const right = [
    ['IEA PVPS Task 12 (2026)', 'Advances in Photovoltaic Module Recycling: Third Update to Empirical LCI Data.', 'https://iea-pvps.org/key-topics/t12-advances-module-recycling-3rd-edition-2026/'],
    ['Saffarian, Galvin + Firouzi (2026)', 'Rethinking silver recovery pathways in end-of-life PV recycling using froth flotation. Minerals Engineering 242, 110189.', 'https://doi.org/10.1016/j.mineng.2026.110189']
  ];
  txt(s, 'AGASTYA PROJECT RECORD', 0.74, 1.99, 5.45, 0.23, { fontSize: 9.5, bold: true, charSpacing: 1.15, color: C.teal });
  txt(s, 'PUBLIC RESEARCH', 6.86, 1.99, 5.65, 0.23, { fontSize: 9.5, bold: true, charSpacing: 1.15, color: C.teal });
  for (let i = 0; i < left.length; i++) {
    const y = 2.35 + i * 0.97;
    card(s, 0.72, y, 5.80, 0.82, false);
    txt(s, left[i][0], 0.96, y + 0.11, 5.28, 0.24, { fontSize: 12.2, bold: true, color: C.ink });
    txt(s, left[i][1], 0.96, y + 0.42, 5.27, 0.27, { fontSize: 9.8, color: C.muted, valign: 'top' });
  }
  for (let i = 0; i < right.length; i++) {
    const y = 2.35 + i * 1.38;
    card(s, 6.82, y, 5.79, 1.18, false);
    txt(s, right[i][0], 7.07, y + 0.13, 5.28, 0.25, { fontSize: 12.0, bold: true, color: C.teal, hyperlink: right[i][2] });
    txt(s, right[i][1], 7.07, y + 0.49, 5.25, 0.45, { fontSize: 10.1, color: C.muted, valign: 'top' });
  }
  card(s, 6.82, 5.16, 5.79, 1.34, true);
  txt(s, 'EVIDENCE LABELS USED IN THIS DECK', 7.10, 5.39, 5.15, 0.22, { fontSize: 9.4, bold: true, charSpacing: 0.8, color: C.mint });
  txt(s, 'Project record  /  Published benchmark  /  Design assumption  /  Unverified hypothesis', 7.10, 5.80, 5.16, 0.48, { fontSize: 12.3, bold: true, color: C.white, valign: 'top' });
  txt(s, 'PROJECT FILES REVIEWED THROUGH 9 OCTOBER 2026. FLOTATION METRICS ARE SEPARATE LAB TESTS, NOT PERFORMANCE CLAIMS.', 0.84, 6.59, 11.70, 0.22, { fontSize: 8.9, bold: true, charSpacing: 0.4, color: C.ink2, align: 'center' });
  footer(s, 14);
  note(s, 'External links are embedded on the IEA PVPS and journal titles. The thesis and Stage 3/4/EYE project records are in the main Agastya project folder. The IEA PVPS 2026 update says mechanical recycling remains dominant commercially and notes gaps in energy, output quality characterization, and harmonized boundaries. The flotation metrics quoted earlier come from the cited 2026 laboratory paper and must remain tied to their separate test conditions.');
}

}

async function main() {
  await buildDeck();
  await pptx.writeFile({ fileName: OUT });
  let zip = await JSZip.loadAsync(fs.readFileSync(OUT));
  for (let i = 1; i <= pptx._slides.length; i++) {
    const part = `ppt/slides/slide${i}.xml`;
    let xml = await zip.file(part).async('string');
    if (xml.includes('<p:transition')) xml = xml.replace(/<p:transition[\s\S]*?<\/p:transition>/, '<p:transition spd="med"><p:fade/></p:transition>');
    else if (xml.includes('</p:clrMapOvr>')) xml = xml.replace('</p:clrMapOvr>', '</p:clrMapOvr><p:transition spd="med"><p:fade/></p:transition>');
    else throw new Error(`Could not locate transition insertion point in ${part}`);
    zip.file(part, xml);
  }
  const out = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE', compressionOptions: { level: 6 } });
  fs.writeFileSync(OUT, out);
  console.log(`Wrote ${OUT} (${pptx._slides.length} slides, one consistent fade transition per slide).`);
}
main().catch(err => { console.error(err); process.exit(1); });

