"use strict";

// Structural check for the eight draft PDFs in the root printables folder.
// Text box fitting is enforced during PDF generation; these checks verify
// the saved files contain one page each at the intended dimensions.

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
const { PDFDocument } = loadPdfLib();
const PRINT = path.resolve(__dirname, "..", "printables");
const mm = 72 / 25.4;
const files = [
  ["AGASTYA_A1_01_Problem_and_Research_Question_DRAFT.pdf", 594 * mm, 841 * mm],
  ["AGASTYA_A1_02_Proposed_Process_Architecture_DRAFT.pdf", 594 * mm, 841 * mm],
  ["AGASTYA_A1_03_Literature_Evidence_and_Project_Status_DRAFT.pdf", 594 * mm, 841 * mm],
  ["AGASTYA_A1_04_Conclusion_and_Validation_Plan_DRAFT.pdf", 594 * mm, 841 * mm],
  ["AGASTYA_A4_01_Project_Overview_DRAFT.pdf", 210 * mm, 297 * mm],
  ["AGASTYA_A4_02_Process_Architecture_DRAFT.pdf", 210 * mm, 297 * mm],
  ["AGASTYA_A4_03_Evidence_and_Status_DRAFT.pdf", 210 * mm, 297 * mm],
  ["AGASTYA_A4_04_Sources_and_Image_Credits_DRAFT.pdf", 210 * mm, 297 * mm]
];

async function main() {
  const errors = [];
  const expected = new Set(files.map(row => row[0]));
  const actual = fs.readdirSync(PRINT).filter(name => name.toLowerCase().endsWith(".pdf")).sort();
  for (const name of actual) if (!expected.has(name)) errors.push("Unexpected PDF in printables: " + name);
  for (const [name, targetW, targetH] of files) {
    const file = path.join(PRINT, name);
    if (!fs.existsSync(file)) { errors.push("Missing PDF: " + name); continue; }
    const bytes = fs.readFileSync(file);
    if (bytes.length < 1500) { errors.push("PDF is unexpectedly small: " + name); continue; }
    try {
      const pdf = await PDFDocument.load(bytes);
      const pages = pdf.getPages();
      if (pages.length !== 1) errors.push(name + ": expected 1 page, found " + pages.length);
      if (pages.length) {
        const w = pages[0].getWidth(), h = pages[0].getHeight();
        if (Math.abs(w - targetW) > 0.1 || Math.abs(h - targetH) > 0.1) {
          errors.push(name + ": expected " + targetW.toFixed(2) + " × " + targetH.toFixed(2) + " pt, found " + w.toFixed(2) + " × " + h.toFixed(2) + " pt");
        }
      }
    } catch (err) {
      errors.push(name + ": could not load: " + err.message);
    }
  }
  if (errors.length) throw new Error("Printable validation failed:\n- " + errors.join("\n- "));
  console.log("Validated " + files.length + " one-page PDFs: 4 A1 portrait (594 × 841 mm) and 4 A4 portrait (210 × 297 mm).");
  console.log("These are draft layouts; the check does not establish NCSC requirements or student/teacher approval.");
}
main().catch(err => { console.error(err.stack || err); process.exit(1); });
