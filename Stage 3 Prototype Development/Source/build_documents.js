const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, BorderStyle, ShadingType
} = require('docx');

const ROOT = 'D:\\Agastya\\Stage 3 Prototype Development';
const FIG = path.join(ROOT, 'Figures');
const NAVY = '17365D', BLUE = '2F75B5', PALE = 'D9EAF7', YELLOW = 'FFF2CC';
const BORDER = { style: BorderStyle.SINGLE, size: 1, color: 'B7C9D6' };

const flowSvg = `
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="620" viewBox="0 0 1600 620">
 <defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0 0L12 6L0 12z" fill="#47647e"/></marker></defs>
 <rect width="1600" height="620" fill="#fff"/>
 <text x="800" y="54" text-anchor="middle" font-family="Arial" font-size="32" font-weight="700" fill="#17365D">AGASTYA — current four-stage process</text>
 <text x="800" y="92" text-anchor="middle" font-family="Arial" font-size="19" fill="#425466">Conceptual process map only • no physical recovery validation is documented</text>
 <g font-family="Arial" text-anchor="middle">
  <rect x="55" y="180" width="330" height="220" rx="18" fill="#D9EAF7" stroke="#17365D" stroke-width="3"/>
  <text x="220" y="230" font-size="26" font-weight="700" fill="#17365D">Stage 1</text><text x="220" y="276" font-size="21" fill="#1f2937">Inspection &amp; routing</text><text x="220" y="321" font-size="16" fill="#425466">Identify • isolate • route</text>
  <rect x="445" y="180" width="330" height="220" rx="18" fill="#D9EAF7" stroke="#17365D" stroke-width="3"/>
  <text x="610" y="230" font-size="26" font-weight="700" fill="#17365D">Stage 2</text><text x="610" y="276" font-size="21" fill="#1f2937">Manual mechanical prep</text><text x="610" y="321" font-size="16" fill="#425466">Frame • J-box • cables</text>
  <rect x="835" y="150" width="330" height="280" rx="18" fill="#E2F0D9" stroke="#548235" stroke-width="3"/>
  <text x="1000" y="205" font-size="26" font-weight="700" fill="#385723">Stage 3</text><text x="1000" y="254" font-size="21" fill="#1f2937">Thermal delamination</text><text x="1000" y="300" font-size="17" fill="#425466">Reference: guarded hot knife</text><text x="1000" y="343" font-size="16" fill="#425466">Glass + cell/EVA/backsheet</text><text x="1000" y="382" font-size="15" fill="#8a3c12">Not validated by AGASTYA</text>
  <rect x="1225" y="150" width="330" height="280" rx="18" fill="#FCE4D6" stroke="#C55A11" stroke-width="3"/>
  <text x="1390" y="205" font-size="26" font-weight="700" fill="#843C0C">Stage 4</text><text x="1390" y="254" font-size="21" fill="#1f2937">Silver removal/recovery</text><text x="1390" y="300" font-size="16" fill="#425466">Route + feed interface open</text><text x="1390" y="343" font-size="16" fill="#425466">Product form to be specified</text><text x="1390" y="382" font-size="15" fill="#8a3c12">No silver recovered</text>
 </g>
 <path d="M386 290H437M776 290H827M1166 290H1217" stroke="#47647e" stroke-width="5" marker-end="url(#arrow)"/>
 <rect x="85" y="500" width="1430" height="72" rx="12" fill="#F2F2F2" stroke="#8996A3" stroke-width="2"/>
 <text x="800" y="529" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#17365D">Cross-stage validation</text>
 <text x="800" y="555" text-anchor="middle" font-family="Arial" font-size="16" fill="#1f2937">Sampling • assay • mass balance • uncertainty • chain of custody</text>
</svg>`;

function para(text, opts = {}) {
  const children = opts.bold ? [new TextRun({ text, bold: true })] : [new TextRun({ text })];
  return new Paragraph({
    children, spacing: { after: opts.after ?? 120, before: opts.before ?? 0, line: 280 },
    alignment: opts.align || AlignmentType.LEFT,
    heading: opts.heading,
    bullet: opts.bullet ? { indent: 360 } : undefined,
    keepNext: opts.keepNext || false,
  });
}

function table(headers, rows) {
  const widths = headers.map(() => 9000 / headers.length);
  const makeCell = (value, i, header = false) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    margins: { top: 70, bottom: 70, left: 90, right: 90 },
    shading: header ? { type: ShadingType.CLEAR, fill: NAVY } : undefined,
    children: [new Paragraph({
      spacing: { after: 0, line: 240 },
      children: [new TextRun({ text: String(value ?? ''), bold: header, color: header ? 'FFFFFF' : '222222', size: 18 })],
    })],
  });
  const allRows = [new TableRow({ children: headers.map((v, i) => makeCell(v, i, true)), tableHeader: true })];
  rows.forEach(row => allRows.push(new TableRow({ children: row.map((v, i) => makeCell(v, i)), cantSplit: true })));
  return new Table({
    width: { size: 9000, type: WidthType.DXA }, columnWidths: widths, rows: allRows,
    borders: { top: BORDER, bottom: BORDER, left: BORDER, right: BORDER, insideHorizontal: BORDER, insideVertical: BORDER },
  });
}

function heading(text, level = 1) {
  const style = level === 1 ? HeadingLevel.HEADING_1 : level === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3;
  return new Paragraph({ text, heading: style, spacing: { before: 240, after: 100 }, keepNext: true });
}

function buildDoc(title, subtitle, sections) {
  const children = [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: title, bold: true, size: 34, color: NAVY })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: subtitle, italics: true, size: 20, color: '555555' })] }),
    new Paragraph({ spacing: { after: 180 }, shading: { fill: YELLOW }, children: [new TextRun({ text: 'Architecture correction — 16 October 2026: Stage 3 is thermal treatment/delamination; Stage 4 is silver removal/recovery. No AGASTYA thermal or silver-recovery trial is claimed.', bold: true, size: 19 })] }),
  ];
  for (const section of sections) {
    children.push(heading(section.title, 1));
    if (section.text) children.push(para(section.text));
    if (section.bullets) for (const item of section.bullets) children.push(para(item, { bullet: true }));
    if (section.table) children.push(table(section.table.headers, section.table.rows));
    if (section.note) children.push(para(section.note, { bold: true }));
  }
  return new Document({
    creator: 'AGASTYA project', title, description: subtitle,
    styles: { default: { document: { run: { font: 'Arial', size: 20, color: '222222' }, paragraph: { spacing: { line: 280 } } } } },
    sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, children }],
  });
}

const docs = [
  ['Stage_3_Scientific_Review.docx', 'Stage 3 Thermal Scientific Review', 'Evidence review and research boundary', [
    { title: 'Purpose and boundary', text: 'Stage 3 thermally separates front glass from prepared crystalline-silicon photovoltaic modules. The working reference is a fixed, guarded hot knife with controlled feed/support. The first expected output is sheet glass plus a cell/EVA/backsheet laminate. This is not proof of EVA-free cells, liberated silver, or a silver product.' },
    { title: 'Evidence reviewed', table: { headers: ['Source', 'Reported result', 'Use and limit'], rows: [
      ['IEA PVPS Task 12 (2023), hot-knife LCA', 'Pilot process separates glass and laminate; about 50 s/module. 0.035 kWh/kg applies to the reported take-back/hot-knife treatment boundary.', 'Process benchmark only; not an isolated Stage 3 heater measurement or Agastya result.'],
      ['NPC equipment / NEDO development account', 'Manufacturer describes about 60 s/panel and a 300 °C knife; fixed-knife feed concept addresses practical handling issues.', 'Supplier/development evidence; settings and geometry are not Agastya specifications.'],
      ['Saitta et al. (2026), thermal-assisted delamination', 'Small coupons heated at 100 or 140 °C for 60 min, then mechanically peeled; results depend on tested module and method.', 'Useful comparison for slower thermal-softening tests; not a sub-minute hot-knife result.'],
      ['EVA pyrolysis study (2023)', 'Decomposition stages reported around 284–411 °C and 378–527 °C.', 'Different process from softening-assisted mechanical separation; not a proposed Agastya setpoint.'],
    ] } },
    { title: 'Is thermal Stage 3 needed?', text: 'It is a plausible process step if front-glass separation is required before Stage 4. A controlled comparison should include a no-heat mechanical baseline where feasible and the simplest suitable thermal condition. Keep Stage 3 only if the intended glass/laminate split improves the downstream silver-removal interface enough to justify its energy, cost, breakage, and safety burden.' },
    { title: 'Alternative routes', table: { headers: ['Route', 'Can demonstrate', 'Limit'], rows: [
      ['Cold fixture / manual separation control', 'Handling, support, cut-path access and data workflow.', 'Does not test thermal assistance.'],
      ['Low-temperature long-dwell comparison', 'Thermal softening plus mechanical peel under supervised lab conditions.', 'Published hour-long coupon tests do not establish production throughput.'],
      ['Guarded fixed hot knife', 'Continuous glass-to-laminate separation on eligible flat feed.', 'Needs a designed, guarded host fixture and actual feed tests.'],
      ['Pyrolysis or chemical delamination', 'Potentially different liberation routes in specialist research.', 'Outside the hot-knife prototype; hazardous emissions or chemicals require a qualified facility.'],
    ] } },
    { title: 'Evidence boundary', text: 'Literature temperatures, cycle times, and energy values are specific to their test systems. Agastya has no validated thermal window, separation quality, energy per panel, throughput, silver liberation, or heat-reuse result. Stage 4 is silver removal/recovery; its method and required Stage 3 feed condition remain open.' },
  ]],
  ['Stage_3_Prototype_Engineering_Design.docx', 'Stage 3 Thermal Prototype Engineering Design', 'Guarded fixed hot-knife concept for supervised coupon work', [
    { title: 'Recommended concept', text: 'Use a fixed hot knife and controlled panel/coupon feed so the tool acts at the glass/EVA boundary while the two outputs remain supported. The first prototype should be coupon-scale and instrumented. Do not copy a commercial temperature, blade shape, feed speed, or machine geometry without checking the host equipment and actual module.' },
    { title: 'Functional blocks', table: { headers: ['Block', 'Function', 'Design gate'], rows: [
      ['Feed/support', 'Hold a flat eligible module/coupon and guide the entry path.', 'Cold alignment and jam-removal review before heating.'],
      ['Blade and heating assembly', 'Apply localized heat along the bonded interface.', 'Host-selected rated equipment, sensor placement, independent over-temperature protection, and supervisor approval.'],
      ['Separation/collection', 'Support glass and cell/EVA/backsheet laminate into distinct collection areas.', 'No free drop, collision, or unsupported sharp glass.'],
      ['Instrumentation', 'Log tool/interface temperature, electrical energy, time, feed speed, mass, and optional force.', 'Record instrument IDs, checks/calibration, and data boundary.'],
      ['Guard/stop', 'Control access to hot surfaces, moving feed, pinch points, and sharp edges.', 'Facility-reviewed guards, accessible stop, emergency response, and restart procedure.'],
    ] } },
    { title: 'Design options', table: { headers: ['Option', 'Scope', 'Cost status'], rows: [
      ['Minimum-cost demonstrator', 'Cold fixture, templates, traceability and surrogate handling.', 'Low cost but no thermal or PV performance claim.'],
      ['Recommended coupon prototype', 'Supervised use of a qualified guarded hot-knife station with temperature, energy and mass logging.', 'Station/facility quote required; partial instrumentation references are not a total.'],
      ['Research extension', 'Repeatable panel feed plus a separately tested heated roller/heat-reuse comparison.', 'Higher cost and complexity; defer until the knife output is repeatable and Stage 4 feed target is defined.'],
    ] } },
    { title: 'Measurement locations', bullets: [
      'Measure blade/tool temperature separately from interface/material temperature; a controller setpoint is not the laminate temperature.',
      'Meter heater electricity over a defined run boundary and distinguish warm-up, processing and standby when possible.',
      'Measure input and each output mass; record glass cracking, separation completeness, cell/backsheet damage and EVA residue location.',
      'Record module/coupon identity, construction, dimensions, condition, feed speed, process time, force/load if available, and deviations.',
    ] },
    { title: 'Stage 4 interface', text: 'The baseline hot-knife output still contains EVA and backsheet. Stage 4 is silver removal/recovery, but its accepted feed and product form have not been specified. Any additional liberation or polymer removal must be named as a separate operation and validated; it must not be assumed to occur in the hot-knife step.' },
  ]],
  ['Stage_3_Build_and_Test_Plan.docx', 'Stage 3 Build and Test Plan', 'Gated path from cold fixture to measured thermal separation', [
    { title: 'Phased plan', table: { headers: ['Phase', 'Work and deliverable', 'Gate to proceed'], rows: [
      ['A. Requirements', 'Freeze module/feed, desired glass and laminate outputs, Stage 4 feed need, scoring rubric and facility roles.', 'Written interface and host inventory.'],
      ['B. Cold fixture', 'Build/check support, guides, blade holder mock-up, guards and collection path without heat.', 'Alignment, clearance, jam access and operator sequence reviewed.'],
      ['C. Instrumented coupons', 'At an approved facility, compare an unheated control where feasible and approved thermal conditions; weigh and assess every stream.', 'Repeatable coupons, reviewed risks, traceable instruments/data.'],
      ['D. Whole-panel confirmation', 'Only after coupon repeatability, run eligible whole panels and record full cycle, energy, output quality and mass closure.', 'Whole-panel output meets predeclared criteria across repeated panels.'],
      ['E. Roller/heat reuse study', 'Separate follow-up with a defined EVA-removal outcome and warm-feed/no-warm-feed controls.', 'Demonstrated quality with lower metered external energy; no double counting.'],
    ] } },
    { title: 'Coupon study measurements', bullets: [
      'Use traceable coupons and record source panel, construction, geometry and condition.',
      'Record blade setpoint and measured blade temperature, interface/material temperature, time, feed speed, energy, force/load if available, and transfer delay.',
      'Weigh glass, laminate and debris. Score glass condition, separation completeness, cell/backsheet damage, and EVA residue separately.',
      'Repeat promising settings on independent coupons; do not treat repeated cuts from one coupon as independent panels.',
      'Preserve raw observations and photos with sample IDs; record holds and deviations rather than silently discarding runs.',
    ] },
    { title: 'Cost and procurement', text: 'Do not buy a heater or fabricate the active station until the host confirms feed geometry, equipment rating, electrical supply, guards, ventilation, supervision, instrumentation, and waste route. The cost workbook separates previously checked instrument references from quote-required station and facility costs; it does not present a complete prototype total.' },
    { title: 'No-go conditions', bullets: [
      'No responsible supervisor, facility risk review, approved feed, or emergency response.',
      'Unknown or unsuitable module construction, unstable/broken panel, or uncontained sharp-glass risk.',
      'No independent over-temperature protection, accessible stop, suitable guards, or adequate ventilation review.',
      'No traceable temperature and electrical-energy measurements or safe output collection path.',
    ] },
  ]],
  ['Stage_3_Safety_and_Risk_Assessment.docx', 'Stage 3 Safety and Risk Assessment', 'Hazard review for a proposed supervised thermal station', [
    { title: 'Safety boundary', text: 'This document is a planning checklist, not an operating permit or construction drawing. Active heating of PV material belongs only in an appropriately equipped facility under its responsible supervisor. No household oven, open flame, improvised thermal enclosure, or homemade fume-treatment system is suitable.' },
    { title: 'Main hazards and required review', table: { headers: ['Hazard', 'Potential harm', 'Required control review'], rows: [
      ['Hot blade/surface and heater power', 'Burns, fire, electric shock, uncontrolled heating.', 'Rated equipment, guarded hot zone, independent over-temperature protection, electrical inspection, accessible stop, safe cool-down.'],
      ['Moving feed and pinch points', 'Entrapment or crush injury.', 'Fixed guarding, controlled access, safe jam procedure, no reaching into moving mechanism.'],
      ['Broken glass/sharp edges', 'Cuts and eye injury.', 'Panel condition screening, stable supports, barriers, appropriate tools/PPE, controlled collection.'],
      ['Polymer heating/fumes', 'Irritation or exposure to unknown decomposition products.', 'Keep process below deliberate decomposition; review actual materials and ventilation/exhaust with EHS; stop if unexpected smoke/odor occurs.'],
      ['PV electrical residues/materials', 'Residual charge, damaged backsheet, metals or contaminants.', 'Qualified intake/isolation, feed identification, contained handling and approved waste route.'],
      ['Stage 4 silver-removal chemistry (if chosen)', 'Chemical exposure, incompatible waste, heat/reaction hazards.', 'Separate route-specific risk assessment and qualified chemical facility; no student-scale improvised extraction.'],
    ] } },
    { title: 'Before active heating', bullets: [
      'The facility supervisor reviews the actual machine, panel/coupon, controls, guarding, electrical supply, ventilation, emergency response and cleanup.',
      'Confirm independent temperature limit and stop function; a software display or EYE event logger is not a safety control.',
      'Rehearse cold handling, support, collection and jam response before energizing equipment.',
      'Agree broken-glass, polymer residue, dust and contaminated waste handling before the test.',
    ] },
    { title: 'Student role', text: 'Student-appropriate work may include desk research, data sheets, cold fixture evaluation and analysis of approved facility data. A trained adult/facility operator controls active heating, machine operation, electrical checks, PV feed admission, cleanup and waste disposition.' },
  ]],
  ['Stage_3_Simulation_and_Calculation_Notes.docx', 'Stage 3 Simulation and Calculation Notes', 'Thermal-energy accounting, measurements and model limits', [
    { title: 'Material sensible heat', text: 'For layers that actually change temperature, estimate Q_sensible = Σ m_i ∫ cp_i(T) dT. A constant-property approximation is Q = Σ m_i cp_i ΔT_i. Heating the full EVA mass to the knife setpoint is not a valid assumption for localized hot-knife contact unless measured.' },
    { title: 'Electrical energy', text: 'Measure E_electric = ∫ V(t) I(t) dt over a declared run boundary. For stable loads, an approximate P_avg × time may be reported with the assumption stated. Separate warm-up, processing and standby where the meter permits. Report energy per panel only for a defined batch and panel count.' },
    { title: 'Losses and heat reuse', bullets: [
      'Partition model energy into material heating, equipment thermal mass and losses; estimate convection, radiation and conduction only when properties and geometry are known.',
      'Measure stream exit/contact temperatures and transfer delay before claiming retained heat is useful to a second operation.',
      'A heat-reuse claim requires equivalent output quality with lower metered external energy and no unacceptable material damage.',
      'The heated roller is a separate experiment; do not count retained heat in both operations.',
    ] },
    { title: 'Throughput and uncertainty', text: 'Energy-limited capacity = available Stage 3 energy/day ÷ measured kWh/panel. Cycle-limited capacity = shift seconds ÷ measured seconds/panel. Feasible throughput is the lower bound after accounting for handling and downtime. Propagate measurement uncertainty in mass, temperature, energy, time and feed geometry; do not convert simulation assumptions into performance claims.' },
    { title: 'Existing model boundary', text: 'The project contains a custom one-dimensional thermal model and historical scenario/time-history rows. They are virtual calculations, not experiments. The model does not predict peel fracture, glass breakage, EVA removal, fumes, silver liberation, machine safety, or Stage 4 silver recovery. Validate model outputs against measured coupon data before using them to select a design.' },
    { title: 'Stage 4 silver balance', text: 'For the downstream silver-removal step, the validation record should distinguish Ag input, Ag in each product/residue stream, assay uncertainty and unaccounted mass. Grade, recovery, enrichment and product purity are separate metrics. Sampling and assay support Stage 4; they do not replace the silver-removal operation.' },
  ]],
];

async function main() {
  fs.mkdirSync(FIG, { recursive: true });
  fs.writeFileSync(path.join(FIG, 'Stage_3_Architecture_Decision.svg'), flowSvg, 'utf8');
  await sharp(Buffer.from(flowSvg)).png().toFile(path.join(FIG, 'Stage_3_Architecture_Decision.png'));
  for (const [filename, title, subtitle, sections] of docs) {
    const buffer = await Packer.toBuffer(buildDoc(title, subtitle, sections));
    fs.writeFileSync(path.join(ROOT, filename), buffer);
  }
  process.stdout.write(`Built ${docs.length} thermal Stage 3 DOCX files and updated the four-stage SVG/PNG.\n`);
}

main().catch(err => { console.error(err); process.exitCode = 1; });

