"use strict";

// Builds the eight one-page print candidates in D:\Agastya\printables.
// Uses pdf-lib from the Codex bundled Node runtime; no extra package is installed.
// All pages are drafts until the student/teacher and event organizer approve them.

const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
function loadPdfLib() {
  try { return require("pdf-lib"); }
  catch (_) {
    const modulesDir = process.env.CODEX_NODE_MODULES || path.join(os.homedir(), ".cache", "codex-runtimes", "codex-primary-runtime", "dependencies", "node", "node_modules");
    return require(path.join(modulesDir, "pdf-lib"));
  }
}
const { PDFDocument, StandardFonts, rgb } = loadPdfLib();

const ROOT = path.resolve(__dirname, "..", "..");
const DEFAULT_OUTPUT = path.join(ROOT, "printables");
const OUTPUT = path.resolve(process.argv[2] || DEFAULT_OUTPUT);
const M = 72 / 25.4;
const A1 = { w: 594 * M, h: 841 * M };
const A4 = { w: 210 * M, h: 297 * M };
const COLORS = {
  navy: "#10263A", ink: "#172D3D", muted: "#536A79", teal: "#149C93",
  gold: "#E9AD3D", coral: "#D86B58", blue: "#4E7EA3",
  paper: "#F3F6F7", white: "#FFFFFF", pale: "#E5F1F0",
  paleGold: "#FFF3D8", paleBlue: "#E8F0F6", paleCoral: "#F9EAE6",
  line: "#D4DFE3", darkTeal: "#0F756F", softNavy: "#1B3A50"
};

function c(hex) {
  const h = hex.replace("#", "");
  return rgb(parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255);
}
function fillRect(page, width, height, x, top, w, h, color) {
  page.drawRectangle({ x, y: height - top - h, width: w, height: h, color: c(color) });
}
function outlinedRect(page, height, x, top, w, h, fill, stroke, sw = 1) {
  page.drawRectangle({
    x, y: height - top - h, width: w, height: h,
    color: c(fill), borderColor: c(stroke), borderWidth: sw
  });
}
function line(page, height, x1, top1, x2, top2, color, thickness = 1) {
  page.drawLine({
    start: { x: x1, y: height - top1 },
    end: { x: x2, y: height - top2 },
    color: c(color), thickness
  });
}
function circle(page, height, cx, topCenter, r, color) {
  page.drawCircle({ x: cx, y: height - topCenter, size: r, color: c(color) });
}
function wrapLine(text, font, size, maxWidth) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const lines = [];
  let current = "";
  for (const word of words) {
    const candidate = current ? current + " " + word : word;
    if (font.widthOfTextAtSize(candidate, size) <= maxWidth || !current) current = candidate;
    else { lines.push(current); current = word; }
  }
  if (current) lines.push(current);
  return lines;
}
function paragraph(page, text, x, top, width, size, color, font, leading = size * 1.28, maxHeight = Infinity, align = "left") {
  const raw = String(text).split("\n");
  const lines = [];
  for (const part of raw) lines.push(...(part ? wrapLine(part, font, size, width) : [""]));
  const total = lines.length * leading;
  if (total > maxHeight + 0.01) {
    throw new Error("Text does not fit (" + total.toFixed(1) + "pt > " + maxHeight.toFixed(1) + "pt): " + String(text).slice(0, 90));
  }
  lines.forEach((t, i) => {
    let tx = x;
    const tw = font.widthOfTextAtSize(t, size);
    if (align === "center") tx = x + (width - tw) / 2;
    else if (align === "right") tx = x + width - tw;
    page.drawText(t, { x: tx, y: page.getHeight() - top - size - i * leading, size, font, color: c(color) });
  });
  return total;
}
function tag(page, H, text, x, top, color, fontBold, size = 13) {
  const padX = size * 0.75;
  const w = fontBold.widthOfTextAtSize(text.toUpperCase(), size) + 2 * padX;
  fillRect(page, page.getWidth(), H, x, top, w, size * 1.9, color);
  paragraph(page, text.toUpperCase(), x + padX, top + size * 0.35, w - 2 * padX, size, COLORS.white, fontBold, size * 1.1, size * 1.2);
}
function addImage(page, image, x, top, w, h, H, background = COLORS.white) {
  fillRect(page, page.getWidth(), H, x, top, w, h, background);
  const scale = Math.min(w / image.width, h / image.height);
  const iw = image.width * scale;
  const ih = image.height * scale;
  page.drawImage(image, {
    x: x + (w - iw) / 2,
    y: H - top - h + (h - ih) / 2,
    width: iw, height: ih
  });
}
function pageBg(page, dims) {
  fillRect(page, dims.w, dims.h, 0, 0, dims.w, dims.h, COLORS.paper);
}
function brandHeader(page, dims, kicker, title, subtitle, opts = {}) {
  const H = dims.h;
  const hh = opts.height || 410;
  fillRect(page, dims.w, H, 0, 0, dims.w, hh, COLORS.navy);
  circle(page, H, 109, 62, 17, COLORS.teal);
  circle(page, H, 109, 62, 7, COLORS.gold);
  paragraph(page, "AGASTYA", 145, 46, 280, 23, COLORS.white, opts.bold, 23, 26);
  paragraph(page, "SOLAR MATERIAL RECOVERY  /  RESEARCH PROJECT", 145, 76, 600, 13, "#C7D6DE", opts.regular, 13, 16);
  tag(page, H, kicker, 100, 115, opts.tagColor || COLORS.teal, opts.bold, 14);
  paragraph(page, title, 100, 160, opts.titleWidth || 1410, opts.titleSize || 68, COLORS.white, opts.bold, opts.titleLeading || 82, opts.titleHeight || 172);
  paragraph(page, subtitle, 103, opts.subtitleTop || 337, opts.subtitleWidth || 1370, opts.subtitleSize || 25, "#D7E3E8", opts.regular, opts.subtitleLeading || 33, opts.subtitleHeight || 66);
  return hh;
}
function footer(page, dims, text, bold, regular) {
  const H = dims.h;
  const y = H - 81;
  fillRect(page, dims.w, H, 0, y, dims.w, 81, COLORS.navy);
  paragraph(page, "DRAFT PRINT CANDIDATE  •  EVENT SIZE / COUNT NOT CONFIRMED", 74, y + 12, dims.w - 148, 12, COLORS.gold, bold, 15, 18);
  paragraph(page, text, 74, y + 35, dims.w - 148, 10.5, "#E0E9ED", regular, 13, 39);
}
function card(page, H, x, top, w, h, accent, kicker, title, body, regular, bold, opts = {}) {
  outlinedRect(page, H, x, top, w, h, COLORS.white, COLORS.line, 1.2);
  fillRect(page, page.getWidth(), H, x, top, 10, h, accent);
  paragraph(page, kicker.toUpperCase(), x + 28, top + 23, w - 52, opts.kickerSize || 14, accent, bold, 18, 22);
  paragraph(page, title, x + 28, top + 58, w - 52, opts.titleSize || 30, COLORS.ink, bold, opts.titleLeading || 36, opts.titleHeight || 80);
  paragraph(page, body, x + 28, top + (opts.bodyTop || 155), w - 56, opts.bodySize || 21, COLORS.muted, regular, opts.bodyLeading || 29, h - (opts.bodyTop || 155) - 25);
}
function makeDoc() {
  return PDFDocument.create().then(async doc => {
    doc.setAuthor("AGASTYA student research project");
    doc.setSubject("Draft competition print materials; verify event rules and content before printing.");
    doc.setKeywords(["AGASTYA", "photovoltaic recycling", "silver", "research poster", "draft"]);
    const regular = await doc.embedFont(StandardFonts.Helvetica);
    const bold = await doc.embedFont(StandardFonts.HelveticaBold);
    const pv = await doc.embedJpg(fs.readFileSync(path.join(ROOT, "07_Visual_Assets", "01_Original_Photographs", "PV_Panel_Fomanu_2015.jpg")));
    const cells = await doc.embedJpg(fs.readFileSync(path.join(ROOT, "07_Visual_Assets", "01_Original_Photographs", "Silicon_Solar_Cells_Fdenicola_2013.jpg")));
    return { doc, regular, bold, pv, cells };
  });
}

async function poster01(ctx) {
  const { doc, regular: r, bold: b, pv, cells } = ctx;
  const p = doc.addPage([A1.w, A1.h]); const H = A1.h; pageBg(p, A1);
  brandHeader(p, A1, "01  /  THE CHALLENGE", "Can we recover silver\nfrom end-of-life PV?", "AGASTYA studies the route from panel identity to a verified silver-bearing fraction.", {
    bold: b, regular: r, titleSize: 55, titleLeading: 67, titleHeight: 145, titleWidth: 790,
    subtitleTop: 330, subtitleWidth: 795, subtitleSize: 23, subtitleLeading: 29
  });
  addImage(p, pv, 980, 67, 610, 270, H);
  paragraph(p, "ILLUSTRATIVE PV MODULE PHOTO — NOT AGASTYA EQUIPMENT", 982, 345, 600, 12, COLORS.gold, b, 15, 17);
  const cw = 462, gap = 49, xs = [100, 100 + cw + gap, 100 + 2 * (cw + gap)];
  card(p, H, xs[0], 470, cw, 306, COLORS.teal, "01  /  MATERIAL SYSTEM", "A bonded stack", "Glass, encapsulant, silicon cells, contacts, backsheet, frame and junction box enter the recovery question together.", r, b, { bodyTop: 151, bodySize: 22, bodyLeading: 30 });
  card(p, H, xs[1], 470, cw, 306, COLORS.gold, "02  /  TARGET", "Silver is a small component", "Printed silver contacts sit on cell material. A visible contact is not the same as a separated, weighed or assayed product.", r, b, { bodyTop: 151, bodySize: 22, bodyLeading: 30 });
  card(p, H, xs[2], 470, cw, 306, COLORS.blue, "03  /  EVIDENCE GAP", "Every stream matters", "A defensible claim needs feed and output masses, representative assays, uncertainty and an accounted residual.", r, b, { bodyTop: 151, bodySize: 22, bodyLeading: 30 });
  paragraph(p, "WHERE THE CONTACTS ARE", 100, 844, 610, 25, COLORS.teal, b, 30, 35);
  addImage(p, cells, 100, 892, 570, 335, H);
  paragraph(p, "Illustrative silicon-cell photograph; not an AGASTYA sample or silver assay.", 100, 1236, 570, 14, COLORS.muted, r, 18, 30);
  paragraph(p, "Silicon cells commonly carry printed metal contacts. Their appearance alone cannot establish silver content, liberation or purity. Those require a defined feed and an appropriate assay.", 730, 900, 835, 27, COLORS.ink, r, 38, 210);
  outlinedRect(p, H, 730, 1125, 835, 104, COLORS.paleBlue, COLORS.paleBlue, 0);
  paragraph(p, "MATERIAL FLOW  >  SEPARATION  >  ASSAY  >  ACCOUNTING", 760, 1154, 775, 21, COLORS.navy, b, 27, 42);
  fillRect(p, A1.w, H, 100, 1322, A1.w - 200, 318, COLORS.navy);
  tag(p, H, "AGASTYA RESEARCH QUESTION", 145, 1360, COLORS.teal, b, 16);
  paragraph(p, "For a defined feed, which step partitions silver-bearing material while keeping mass and silver balances traceable?", 145, 1422, 1370, 40, COLORS.white, b, 53, 165);
  paragraph(p, "CURRENT PROJECT SNAPSHOT", 100, 1710, 600, 26, COLORS.navy, b, 32, 40);
  const stats = [
    ["14", "registered evidence records"],
    ["5", "recovery routes compared"],
    ["200,080", "historical virtual records*"],
    ["0", "physical AGASTYA sample assays"]
  ];
  const sw = 344, sg = 32, sx = [100, 100 + sw + sg, 100 + 2 * (sw + sg), 100 + 3 * (sw + sg)];
  stats.forEach((s, i) => {
    outlinedRect(p, H, sx[i], 1765, sw, 220, COLORS.white, COLORS.line, 1);
    paragraph(p, s[0], sx[i] + 24, 1798, sw - 48, i === 2 ? 43 : 55, [COLORS.teal, COLORS.gold, COLORS.blue, COLORS.coral][i], b, 61, 67);
    paragraph(p, s[1], sx[i] + 24, 1880, sw - 48, 20, COLORS.ink, b, 27, 62);
  });
  paragraph(p, "*Model/scenario outputs, not physical samples, independent experiments or validated recovery predictions.", 102, 2025, 1450, 21, COLORS.muted, r, 28, 34);
  footer(p, A1, "Photo credits: Fomanu, “PV Panel,” and Fdenicola, “Solar cell01.JPG,” Wikimedia Commons, CC BY-SA 4.0. Source details: 07_Visual_Assets/VISUAL_ASSET_REGISTER.csv.", b, r);
}

async function poster02(ctx) {
  const { doc, regular: r, bold: b } = ctx;
  const p = doc.addPage([A1.w, A1.h]); const H = A1.h; pageBg(p, A1);
  brandHeader(p, A1, "02  /  PROPOSED ARCHITECTURE", "Four stages. One evidence chain.", "The numbered stages describe a research plan; they do not represent validated equipment or performance.", { bold: b, regular: r, titleSize: 70, titleLeading: 84, titleHeight: 90, subtitleTop: 281, subtitleSize: 24 });
  const stages = [
    { n: "01", color: COLORS.teal, title: "Inspect and route", tag: "IDENTITY + TRIAGE", body: "Record module type, visible condition, origin and sample ID. Keep repair, reuse and second-life options visible before choosing a recovery route.", out: "Record: panel passport\nDecision: retain or route\nGate: provenance" },
    { n: "02", color: COLORS.gold, title: "Liberate and classify", tag: "FEED PREPARATION", body: "Establish a contained preparation baseline. Define size cuts, retain all fractions and dust, and record the mass and identity of each stream.", out: "Input: traceable feed\nOutputs: retained size cuts\nGate: mass accounted" },
    { n: "03", color: COLORS.blue, title: "Test candidate separation", tag: "UNVALIDATED CANDIDATE", body: "Electrostatic separation is a candidate to test. A PV-scrap study reports Ag/Al/Si co-concentration; it does not establish silver-only selectivity or an AGASTYA recovery.", out: "Question: partitioning?\nNeed: stream masses + assays\nGate: matched feed evidence" },
    { n: "04", color: COLORS.coral, title: "Assay and account", tag: "MEASUREMENT GATE", body: "Use a qualified method for all relevant streams. Report mass yield, silver grade, silver recovery, residual and uncertainty as separate quantities.", out: "Output: verified balance\nRecord: method + QA/QC\nGate: review before claims" }
  ];
  const x = 100, w = 1484, y0 = 450, rh = 345, gap = 31;
  line(p, H, 170, y0 + 132, 170, y0 + 3 * (rh + gap) + 132, COLORS.line, 5);
  stages.forEach((s, i) => {
    const y = y0 + i * (rh + gap);
    outlinedRect(p, H, x, y, w, rh, COLORS.white, COLORS.line, 1.2);
    circle(p, H, 170, y + 98, 47, s.color);
    paragraph(p, s.n, 129, y + 75, 82, 37, COLORS.white, b, 42, 50, "center");
    tag(p, H, s.tag, 267, y + 41, s.color, b, 13);
    paragraph(p, s.title, 267, y + 91, 730, 36, COLORS.ink, b, 45, 50);
    paragraph(p, s.body, 267, y + 154, 760, 23, COLORS.muted, r, 32, 151);
    fillRect(p, A1.w, H, 1070, y + 34, 2, rh - 68, COLORS.line);
    paragraph(p, "HAND-OFF", 1110, y + 49, 390, 14, s.color, b, 19, 24);
    paragraph(p, s.out, 1110, y + 92, 400, 22, COLORS.ink, b, 32, 150);
  });
  paragraph(p, "TRACEABILITY FOLLOWS THE MATERIAL", 100, 1986, 780, 23, COLORS.navy, b, 30, 35);
  const labels = ["Panel ID", "Stage event", "Stream / batch", "Aliquot ID", "Assay record", "Receiver lot"];
  const bx = 100, by = 2035, boxW = 205, boxGap = 44, boxH = 82;
  labels.forEach((lab, i) => {
    const xx = bx + i * (boxW + boxGap);
    outlinedRect(p, H, xx, by, boxW, boxH, i % 2 ? COLORS.paleBlue : COLORS.pale, COLORS.line, 1);
    paragraph(p, lab, xx + 10, by + 26, boxW - 20, 17, COLORS.navy, b, 23, 30, "center");
    if (i < labels.length - 1) paragraph(p, ">", xx + boxW + 6, by + 22, 34, 27, COLORS.teal, b, 32, 35, "center");
  });
  paragraph(p, "Thermal delamination is optional feed-preparation research outside these four stages. No AGASTYA operating setpoint is validated.", 102, 2150, 1480, 26, COLORS.muted, r, 35, 90);
  footer(p, A1, "Sources: AGASTYA Architecture Crosswalk (2026-10-10); Phase B/C validation plan; de Souza & Veit (2023), DOI 10.1016/j.cec.2023.100027.", b, r);
}

async function poster03(ctx) {
  const { doc, regular: r, bold: b } = ctx;
  const p = doc.addPage([A1.w, A1.h]); const H = A1.h; pageBg(p, A1);
  brandHeader(p, A1, "03  /  EVIDENCE + STATUS", "Published numbers have boundaries.", "Literature findings describe their own feed and method. They are comparators, not AGASTYA results.", { bold: b, regular: r, titleSize: 68, titleLeading: 82, titleHeight: 90, subtitleTop: 281, subtitleSize: 24 });
  const y = 450, h = 745, w = 462, xs = [100, 611, 1122];
  const evidenceCards = [
    { x: xs[0], color: COLORS.teal, tag: "STAGE 2  /  SIZE PARTITION", title: "Silver in fines" },
    { x: xs[1], color: COLORS.blue, tag: "STAGE 3  /  ELECTROSTATIC", title: "Co-concentration" },
    { x: xs[2], color: COLORS.gold, tag: "BENCHMARK  /  FLOTATION", title: "A measured comparator" }
  ];
  evidenceCards.forEach(e => {
    outlinedRect(p, H, e.x, y, w, h, COLORS.white, COLORS.line, 1.2);
    fillRect(p, A1.w, H, e.x, y, 10, h, e.color);
    paragraph(p, e.tag, e.x + 28, y + 23, w - 52, 14, e.color, b, 18, 22);
    paragraph(p, e.title, e.x + 28, y + 58, w - 52, 30, COLORS.ink, b, 37, 48);
  });
  // The size shares are visibly tied to separate published feed categories.
  paragraph(p, "UP TO THIS STUDY-SPECIFIC SHARE OF FEED Ag", xs[0] + 28, y + 111, w - 52, 13, COLORS.muted, b, 17, 22);
  const statY = y + 142, statW = 194;
  outlinedRect(p, H, xs[0] + 28, statY, statW, 128, COLORS.pale, COLORS.pale, 0);
  outlinedRect(p, H, xs[0] + 232, statY, statW, 128, COLORS.paleGold, COLORS.paleGold, 0);
  paragraph(p, "70%", xs[0] + 42, statY + 17, statW - 28, 40, COLORS.teal, b, 48, 56);
  paragraph(p, "EVAc feed / F4 finest", xs[0] + 42, statY + 77, statW - 28, 15, COLORS.ink, b, 20, 25);
  paragraph(p, "80%", xs[0] + 246, statY + 17, statW - 28, 40, COLORS.gold, b, 48, 56);
  paragraph(p, "MP feed / F4 finest", xs[0] + 246, statY + 77, statW - 28, 15, COLORS.ink, b, 20, 25);
  outlinedRect(p, H, xs[0] + 28, y + 291, w - 56, 132, COLORS.paleBlue, COLORS.paleBlue, 0);
  paragraph(p, "94.12%", xs[0] + 45, y + 308, 170, 39, COLORS.blue, b, 47, 54);
  paragraph(p, "Ag in <0.25 mm fines\nJuyo Salazar et al. (2024)", xs[0] + 220, y + 311, 205, 16, COLORS.ink, b, 21, 50);
  paragraph(p, "These are study-specific Ag distributions into size fractions, not product grade, purity or an AGASTYA forecast.", xs[0] + 31, y + 455, w - 62, 19, COLORS.muted, r, 27, 150);

  // Element chips make the reported co-concentration claim legible without implying selectivity.
  const chipCenters = [xs[1] + 100, xs[1] + 231, xs[1] + 362];
  const chipColors = [COLORS.blue, COLORS.gold, COLORS.teal];
  ["Ag", "Al", "Si"].forEach((t, i) => {
    circle(p, H, chipCenters[i], y + 205, 43, chipColors[i]);
    paragraph(p, t, chipCenters[i] - 30, y + 185, 60, 31, COLORS.white, b, 38, 45, "center");
  });
  paragraph(p, "+", xs[1] + 151, y + 187, 30, 29, COLORS.muted, b, 35, 40, "center");
  paragraph(p, "+", xs[1] + 282, y + 187, 30, 29, COLORS.muted, b, 35, 40, "center");
  paragraph(p, "de Souza & Veit (2023) report Ag, Al and Si co-concentration from processed PV scraps.", xs[1] + 31, y + 286, w - 62, 19, COLORS.ink, r, 27, 125);
  outlinedRect(p, H, xs[1] + 28, y + 436, w - 56, 112, COLORS.pale, COLORS.pale, 0);
  paragraph(p, "SUPPORTED", xs[1] + 45, y + 452, w - 90, 13, COLORS.darkTeal, b, 17, 20);
  paragraph(p, "Ag-bearing mixed fraction", xs[1] + 45, y + 482, w - 90, 20, COLORS.ink, b, 26, 32);
  outlinedRect(p, H, xs[1] + 28, y + 565, w - 56, 143, COLORS.paleCoral, COLORS.paleCoral, 0);
  paragraph(p, "NOT ESTABLISHED", xs[1] + 45, y + 580, w - 90, 13, COLORS.coral, b, 17, 20);
  paragraph(p, "A complete mass-weighted Ag recovery, product grade or silver-only selectivity.", xs[1] + 45, y + 610, w - 90, 18, COLORS.ink, r, 25, 83);

  paragraph(p, "TAP-WATER ROUGHER", xs[2] + 28, y + 112, w - 52, 13, COLORS.muted, b, 17, 22);
  paragraph(p, "97.55 ± 0.03%", xs[2] + 28, y + 142, w - 52, 34, COLORS.gold, b, 42, 50);
  paragraph(p, "reported Ag recovery", xs[2] + 28, y + 191, w - 52, 17, COLORS.ink, b, 22, 27);
  paragraph(p, "32.2 ± 2.3× upgrade", xs[2] + 28, y + 240, w - 52, 26, COLORS.blue, b, 33, 42);
  line(p, H, xs[2] + 28, y + 292, xs[2] + w - 28, y + 292, COLORS.line, 1.4);
  paragraph(p, "ROUGHER-CLEANER CASE", xs[2] + 28, y + 314, w - 52, 13, COLORS.muted, b, 17, 22);
  paragraph(p, "46.7 ± 1.5 wt% Ag", xs[2] + 28, y + 344, w - 52, 29, COLORS.ink, b, 36, 44);
  paragraph(p, "at 86.5 ± 2.8% recovery", xs[2] + 28, y + 389, w - 52, 19, COLORS.ink, b, 25, 30);
  outlinedRect(p, H, xs[2] + 28, y + 454, w - 56, 230, COLORS.paleGold, COLORS.paleGold, 0);
  paragraph(p, "STUDY BOUNDARY", xs[2] + 45, y + 473, w - 90, 13, "#9A6917", b, 17, 22);
  paragraph(p, "Prepared, delaminated and ground cell feed; laboratory flotation with reagents. These results are not a whole-panel test, AGASTYA result or school procedure.", xs[2] + 45, y + 505, w - 90, 18, COLORS.ink, r, 25, 165);
  paragraph(p, "KEEP THESE FOUR METRICS DISTINCT", 100, 1240, 800, 25, COLORS.navy, b, 31, 38);
  const metrics = [
    ["Ag partition", "Where feed silver reports across output streams."],
    ["Mass yield", "Output mass divided by input mass."],
    ["Ag grade", "Silver fraction in one product stream."],
    ["Ag recovery", "Feed silver captured in a defined product."]
  ];
  const mw = 344, mg = 32;
  metrics.forEach((m, i) => {
    const xx = 100 + i * (mw + mg);
    outlinedRect(p, H, xx, 1295, mw, 184, COLORS.white, COLORS.line, 1);
    paragraph(p, m[0], xx + 20, 1321, mw - 40, 21, [COLORS.teal, COLORS.gold, COLORS.blue, COLORS.coral][i], b, 26, 32);
    paragraph(p, m[1], xx + 20, 1365, mw - 40, 18, COLORS.muted, r, 25, 85);
  });
  paragraph(p, "WHAT AGASTYA HAS PRODUCED", 100, 1538, 700, 25, COLORS.navy, b, 31, 38);
  const facts = [
    ["14", "source records in the evidence register"],
    ["5", "candidate routes compared"],
    ["200,080", "historical virtual model/scenario records"],
    ["0", "physical samples assayed for AGASTYA"]
  ];
  const fw = 344;
  facts.forEach((f, i) => {
    const xx = 100 + i * (fw + mg);
    outlinedRect(p, H, xx, 1590, fw, 342, COLORS.white, COLORS.line, 1);
    paragraph(p, f[0], xx + 20, 1640, fw - 40, i === 2 ? 40 : 54, [COLORS.teal, COLORS.gold, COLORS.blue, COLORS.coral][i], b, 62, 70);
    paragraph(p, f[1], xx + 20, 1725, fw - 40, 19, COLORS.ink, b, 26, 100);
    if (i === 2) paragraph(p, "Virtual outputs, not independent specimens, physical experiments or validated recovery predictions.", xx + 20, 1815, fw - 40, 16, COLORS.muted, r, 22, 72);
  });
  paragraph(p, "Conclusion: no universal route ranking follows from unlike feeds and endpoints. Matched tests and assays are still needed.", 102, 1995, 1480, 31, COLORS.navy, b, 39, 90);
  footer(p, A1, "Studies: Sim et al. (2022), DOI 10.1016/j.wasman.2022.11.023; Juyo Salazar et al. (2024), DOI 10.1016/j.susmat.2024.e01047; de Souza & Veit (2023), DOI 10.1016/j.cec.2023.100027; Saffarian et al. (2026), DOI 10.1016/j.mineng.2026.110189.", b, r);
}

async function poster04(ctx) {
  const { doc, regular: r, bold: b } = ctx;
  const p = doc.addPage([A1.w, A1.h]); const H = A1.h; pageBg(p, A1);
  brandHeader(p, A1, "04  /  CONCLUSION + NEXT TEST", "Measure first. Choose the route second.", "The immediate goal is a safe, traceable study design with an assay that can answer the question.", { bold: b, regular: r, titleSize: 63, titleLeading: 77, titleHeight: 90, subtitleTop: 281, subtitleSize: 24 });
  card(p, H, 100, 450, 710, 340, COLORS.teal, "SUPPORTED TODAY", "A research framework", "The project has a documented four-stage concept, a literature review and an accounting framework that separates mass yield, silver grade, silver recovery and residual.", r, b, { titleSize: 33, titleHeight: 80, bodyTop: 173, bodySize: 23, bodyLeading: 31 });
  card(p, H, 874, 450, 710, 340, COLORS.coral, "NOT ESTABLISHED", "No AGASTYA performance result", "No physical feed sample, assay, recovered silver, purity result or validated electrostatic prediction is documented. Throughput, cost and environmental performance are also unknown.", r, b, { titleSize: 33, titleHeight: 80, bodyTop: 173, bodySize: 23, bodyLeading: 31 });
  paragraph(p, "FOUR GATES BEFORE ANY RECOVERY CLAIM", 100, 850, 1000, 25, COLORS.navy, b, 32, 38);
  const gates = [
    ["01", "Define the sample", "Document source, PV technology, condition, permission, sample ID and chain of custody.", COLORS.teal],
    ["02", "Weigh every stream", "Set the feed and output boundaries; retain and weigh all fractions, dust and residues.", COLORS.gold],
    ["03", "Agree the assay", "Use a qualified lab and pre-agreed sample preparation, blanks, duplicates, QA/QC and reporting limits.", COLORS.blue],
    ["04", "Close and review", "Calculate mass yield, Ag grade, Ag recovery, residual and uncertainty separately before interpretation.", COLORS.coral]
  ];
  gates.forEach((g, i) => {
    const yy = 910 + i * 211;
    outlinedRect(p, H, 100, yy, 1484, 177, COLORS.white, COLORS.line, 1);
    circle(p, H, 170, yy + 88, 42, g[3]);
    paragraph(p, g[0], 130, yy + 69, 80, 32, COLORS.white, b, 38, 45, "center");
    paragraph(p, g[1], 255, yy + 35, 500, 31, COLORS.ink, b, 39, 45);
    paragraph(p, g[2], 255, yy + 88, 1210, 21, COLORS.muted, r, 29, 70);
  });
  outlinedRect(p, H, 100, 1782, 1484, 270, COLORS.paleGold, "#E9D8AE", 1);
  tag(p, H, "STOP / REVIEW RULE", 133, 1814, COLORS.coral, b, 14);
  paragraph(p, "Pause if sample identity, safety controls or assay quality checks fail. Do not force an incomplete balance to close.", 133, 1874, 1380, 31, COLORS.navy, b, 41, 100);
  paragraph(p, "A documented no-go is a valid research outcome.", 133, 1980, 1380, 30, COLORS.darkTeal, b, 38, 45);
  footer(p, A1, "Future physical work requires an authorized facility, trained supervision, site-specific safety review and suitable analytical methods. No chemical or high-voltage student build is proposed.", b, r);
}

function a4Header(page, dims, title, subtitle, bold, regular, image) {
  const H = dims.h;
  fillRect(page, dims.w, H, 0, 0, dims.w, 151, COLORS.navy);
  circle(page, H, 42, 34, 10, COLORS.teal); circle(page, H, 42, 34, 4, COLORS.gold);
  paragraph(page, "AGASTYA  /  RESEARCH PROJECT", 62, 23, 280, 13, COLORS.white, bold, 16, 18);
  paragraph(page, title, 38, 56, image ? 330 : 520, 25, COLORS.white, bold, 31, 36);
  paragraph(page, subtitle, 39, 103, image ? 325 : 520, 11.5, "#D7E3E8", regular, 15, 33);
  if (image) addImage(page, image, 397, 20, 160, 108, H);
}
function a4Footer(page, dims, text, bold, regular) {
  const H = dims.h, top = H - 55;
  fillRect(page, dims.w, H, 0, top, dims.w, 55, COLORS.navy);
  paragraph(page, "DRAFT • Confirm local rules and proof at 100% before printing.", 34, top + 8, dims.w - 68, 9, COLORS.gold, bold, 11, 13);
  paragraph(page, text, 34, top + 25, dims.w - 68, 7.7, "#E0E9ED", regular, 9.5, 23);
}
function a4Card(page, H, r, b, x, top, w, h, accent, kicker, title, body, opts = {}) {
  outlinedRect(page, H, x, top, w, h, COLORS.white, COLORS.line, 1);
  fillRect(page, page.getWidth(), H, x, top, 6, h, accent);
  paragraph(page, kicker.toUpperCase(), x + 17, top + 9, w - 31, 8.4, accent, b, 10, 12);
  paragraph(page, title, x + 17, top + 25, w - 31, opts.titleSize || 13.2, COLORS.ink, b, 16, 19);
  paragraph(page, body, x + 17, top + 46, w - 31, opts.bodySize || 10.1, COLORS.muted, r, opts.leading || 13.2, h - 51);
}
async function a4Summary(ctx) {
  const { doc, regular: r, bold: b, pv } = ctx;
  const p = doc.addPage([A4.w, A4.h]); const H = A4.h; pageBg(p, A4);
  a4Header(p, A4, "Project overview", "Research framework for end-of-life photovoltaic material recovery.", b, r, pv);
  const blocks = [
    ["THE PROBLEM", "A bonded material system", "Silver contacts are attached to silicon cells inside a layered module. Separating a silver-bearing fraction is not the same as producing pure silver.", COLORS.teal],
    ["THE QUESTION", "Which step partitions silver?", "For a defined feed, can a candidate step move silver into a traceable fraction while preserving mass and silver accounting?", COLORS.gold],
    ["THE PLAN", "Four proposed stages", "Inspect and route > liberate and classify > test candidate separation > assay and account. The process has not been physically validated by AGASTYA.", COLORS.blue],
    ["CURRENT STATUS", "Research and models only", "14 evidence records and five route comparisons. Historical virtual records are not physical samples or independent experiments. No AGASTYA assay or recovery result exists.", COLORS.coral]
  ];
  blocks.forEach((v, i) => a4Card(p, H, r, b, 38, 173 + i * 142, 519, 127, v[3], v[0], v[1], v[2], { bodySize: 10.2, leading: 13.4 }));
  a4Footer(p, A4, "Illustrative photo: Fomanu, Wikimedia Commons, CC BY-SA 4.0; not AGASTYA equipment. Source: 07_Visual_Assets/VISUAL_ASSET_REGISTER.csv.", b, r);
}
async function a4Architecture(ctx) {
  const { doc, regular: r, bold: b, cells } = ctx;
  const p = doc.addPage([A4.w, A4.h]); const H = A4.h; pageBg(p, A4);
  a4Header(p, A4, "Proposed process", "Four numbered stages; thermal delamination is optional pretreatment.", b, r, cells);
  const blocks = [
    ["01  /  INSPECT + ROUTE", "Identity and triage", "Record module type, visible condition, origin and sample ID. Preserve a reuse or repair route where suitable.", COLORS.teal],
    ["02  /  LIBERATE + CLASSIFY", "Prepare traceable feed", "Define size cuts, retain fractions and dust, and record the identity and mass of every stream.", COLORS.gold],
    ["03  /  CANDIDATE SEPARATION", "Test, do not assume", "Electrostatic separation is a candidate. Literature reports co-concentration of Ag, Al and Si, not silver-only selectivity.", COLORS.blue],
    ["04  /  ASSAY + ACCOUNT", "Verify material flows", "Report mass yield, silver grade, silver recovery, residual and uncertainty as distinct quantities.", COLORS.coral]
  ];
  blocks.forEach((v, i) => a4Card(p, H, r, b, 38, 173 + i * 142, 519, 127, v[3], v[0], v[1], v[2], { bodySize: 10.2, leading: 13.4 }));
  a4Footer(p, A4, "Illustrative silicon-cell photo: Fdenicola, Wikimedia Commons, CC BY-SA 4.0; not an AGASTYA sample or assay.", b, r);
}
async function a4Evidence(ctx) {
  const { doc, regular: r, bold: b } = ctx;
  const p = doc.addPage([A4.w, A4.h]); const H = A4.h; pageBg(p, A4);
  a4Header(p, A4, "Evidence and status", "Published findings stay attached to their feed and method.", b, r, null);
  const blocks = [
    ["SIZE CLASSIFICATION", "Silver partition to fines", "Sim et al. (2022): up to 70% and 80% of feed Ag in F4 for two separate categories. Juyo Salazar et al. (2024): 94.12% of Ag in a <0.25 mm fraction. These are not product grade or AGASTYA results.", COLORS.teal],
    ["ELECTROSTATIC", "Ag / Al / Si co-concentration", "de Souza & Veit (2023) report co-concentration from PV scraps. Accessible evidence does not establish a complete Ag recovery or product-grade balance.", COLORS.blue],
    ["FLOTATION COMPARATOR", "Prepared cell-feed result", "Saffarian et al. (2026): rougher 97.55 ± 0.03% Ag recovery and 32.2 ± 2.3× upgrade; a cleaner case reported 46.7 ± 1.5 wt% Ag at 86.5 ± 2.8% recovery. Laboratory feed and reagents; not transferable to AGASTYA.", COLORS.gold],
    ["AGASTYA MEASUREMENTS", "No physical silver result", "Evidence register: 14 records; route comparisons: five. Historical 200,080 virtual records are model/scenario outputs. Physical AGASTYA samples assayed: 0.", COLORS.coral]
  ];
  blocks.forEach((v, i) => a4Card(p, H, r, b, 38, 173 + i * 142, 519, 127, v[3], v[0], v[1], v[2], { bodySize: 9.7, leading: 12.2 }));
  a4Footer(p, A4, "See 01_Research/03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv for citations, study scope and limitations.", b, r);
}
async function a4Sources(ctx) {
  const { doc, regular: r, bold: b } = ctx;
  const p = doc.addPage([A4.w, A4.h]); const H = A4.h; pageBg(p, A4);
  a4Header(p, A4, "Sources and image credits", "Short display references; full evidence register remains digital.", b, r, null);
  const refs = [
    ["SIZE PARTITION", "Sim et al. (2022). A facile crush-and-sieve treatment for recycling end-of-life photovoltaics. Waste Management 156, 97–106. DOI: 10.1016/j.wasman.2022.11.023.", COLORS.teal],
    ["SIZE PARTITION", "Juyo Salazar et al. (2024). Streamlined process with a sustainable approach for photovoltaic module recycling. Sustainable Materials and Technologies 41, e01047. DOI: 10.1016/j.susmat.2024.e01047.", COLORS.gold],
    ["ELECTROSTATIC", "de Souza & Veit (2023). Study of electrostatic separation to concentrate silver, aluminum, and silicon from solar panel scraps. Circular Economy 2(1), 100027. DOI: 10.1016/j.cec.2023.100027.", COLORS.blue],
    ["FLOTATION COMPARATOR", "Saffarian, Galvin & Firouzi (2026). Rethinking silver recovery pathways in end-of-life photovoltaic recycling using froth flotation. Minerals Engineering 242, 110189. DOI: 10.1016/j.mineng.2026.110189.", COLORS.coral],
    ["PHOTO CREDIT", "Fomanu, “PV Panel”; Wikimedia Commons, CC BY-SA 4.0. commons.wikimedia.org/wiki/File:PV_Panel.jpg", COLORS.teal],
    ["PHOTO CREDIT", "Fdenicola, “Solar cell01.JPG”; Wikimedia Commons, CC BY-SA 4.0. commons.wikimedia.org/wiki/File:Solar_cell01.JPG. Photos are illustrative, not AGASTYA equipment or samples.", COLORS.blue]
  ];
  refs.forEach((v, i) => {
    const yy = 169 + i * 92;
    outlinedRect(p, H, 38, yy, 519, 82, COLORS.white, COLORS.line, 1);
    fillRect(p, A4.w, H, 38, yy, 6, 82, v[2]);
    paragraph(p, v[0], 55, yy + 8, 480, 8.2, v[2], b, 10, 12);
    paragraph(p, v[1], 55, yy + 24, 480, 9.1, COLORS.ink, r, 11.5, 52);
  });
  a4Footer(p, A4, "Full claims, method descriptions and limitations: 01_Research/03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv.", b, r);
}

async function main() {
  fs.mkdirSync(OUTPUT, { recursive: true });
  const ctx = await makeDoc();
  const builders = [
    ["AGASTYA_A1_01_Problem_and_Research_Question_DRAFT.pdf", poster01],
    ["AGASTYA_A1_02_Proposed_Process_Architecture_DRAFT.pdf", poster02],
    ["AGASTYA_A1_03_Literature_Evidence_and_Project_Status_DRAFT.pdf", poster03],
    ["AGASTYA_A1_04_Conclusion_and_Validation_Plan_DRAFT.pdf", poster04],
    ["AGASTYA_A4_01_Project_Overview_DRAFT.pdf", a4Summary],
    ["AGASTYA_A4_02_Process_Architecture_DRAFT.pdf", a4Architecture],
    ["AGASTYA_A4_03_Evidence_and_Status_DRAFT.pdf", a4Evidence],
    ["AGASTYA_A4_04_Sources_and_Image_Credits_DRAFT.pdf", a4Sources]
  ];
  for (const [filename, builder] of builders) {
    const before = ctx.doc.getPageCount();
    await builder(ctx);
    if (ctx.doc.getPageCount() !== before + 1) throw new Error("Expected one page for " + filename);
  }
  const bytes = await ctx.doc.save();
  // Split each page into its own one-page PDF so every printable is a discrete file.
  const source = await PDFDocument.load(bytes);
  for (let i = 0; i < builders.length; i++) {
    const out = await PDFDocument.create();
    const [copied] = await out.copyPages(source, [i]);
    out.addPage(copied);
    out.setAuthor("AGASTYA student research project");
    out.setSubject("Draft print candidate; verify event rules and content before printing.");
    out.setTitle(builders[i][0].replace(/\.pdf$/i, ""));
    const outputBytes = await out.save();
    fs.writeFileSync(path.join(OUTPUT, builders[i][0]), outputBytes);
  }
  console.log("Created " + builders.length + " one-page A1/A4 draft printables in " + OUTPUT);
}

main().catch(err => { console.error(err.stack || err); process.exit(1); });
