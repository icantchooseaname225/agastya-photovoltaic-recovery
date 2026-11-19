(() => {
  const $ = (selector) => document.querySelector(selector);
  let materialRecords = [];
  let runReports = [];

  function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[character]);
  }

  function value(id) { return $(`#${id}`).value.trim(); }
  function numberOrNull(id) { const raw = value(id); return raw ? Number(raw) : null; }
  function ids(id) { return value(id).split(",").map((item) => item.trim()).filter(Boolean); }
  function display(number, digits = 2) { return number == null ? "—" : Number(number).toFixed(digits); }
  function post(url, body) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
      .then(async (response) => { const result = await response.json(); if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`); return result; });
  }
  function status(id, message, error = false) {
    const element = $(`#${id}`);
    element.textContent = message;
    element.className = `inline-status${error ? " error" : " success"}`;
  }

  function renderRecords() {
    const body = $("#material-records-body");
    body.innerHTML = materialRecords.slice().reverse().map((record) => {
      const label = record.record_type === "assay"
        ? `${record.analyte} · ${(record.mass_fraction * 100).toFixed(3)}%`
        : record.material_label || record.target_description || "Process run";
      const mass = record.mass_g == null ? "—" : `${display(record.mass_g, 3)} g ${record.mass_basis || ""}`;
      const parent = record.parent_record_ids?.join(", ") || record.sample_id || record.feed_record_ids?.join(", ") || "—";
      return `<tr><td><span class="panel-code">${escapeHTML(record.record_id)}</span></td><td>${escapeHTML(record.record_type)}</td><td>${escapeHTML(label)}</td><td>${escapeHTML(mass)}</td><td>${escapeHTML(parent)}</td><td>${escapeHTML(record.route_code || "—")}</td><td>${escapeHTML(record.record_hash?.slice(0, 12) || "—")}</td></tr>`;
    }).join("");
    $("#material-records-empty").hidden = materialRecords.length > 0;
    $("#material-record-count").textContent = `${materialRecords.length} immutable records`;
  }

  function targetSummary(report) {
    const metrics = report.route_metrics || {};
    if (report.route_code === "direct_comminution") {
      return `Ag recovery ${display(metrics.ag_recovery_percent)}% · grade ${display(metrics.target_ag_grade_percent, 3)}%`;
    }
    return `Cell recovery ${display(metrics.intact_cell_recovery_percent)}% · polymer ${display(metrics.target_residual_polymer_grade_percent)}%`;
  }

  function renderRuns() {
    const body = $("#material-runs-body");
    body.innerHTML = runReports.map((report) => `<tr>
      <td><button class="table-action" type="button" data-material-report="${escapeHTML(report.run_id)}">${escapeHTML(report.run_id)}</button></td>
      <td>${escapeHTML(report.route_code.replaceAll("_", " "))}<span class="sub-cell">${escapeHTML(report.target_description || report.route_metrics?.target || "Target not described")}</span></td>
      <td>${report.mass_closure_percent == null ? "—" : `${display(report.mass_closure_percent)}%`}</td>
      <td>${escapeHTML(targetSummary(report))}</td>
      <td>${report.specific_energy_kwh_per_kg_feed == null ? "—" : `${display(report.specific_energy_kwh_per_kg_feed, 4)} kWh/kg`}</td>
      <td>${report.cost_inr_per_kg_feed == null ? "—" : `₹${display(report.cost_inr_per_kg_feed)}`}</td>
      <td>${escapeHTML(report.receiver_status)}</td></tr>`).join("");
    $("#material-runs-empty").hidden = runReports.length > 0;
  }

  function renderReport(report) {
    const metrics = report.route_metrics || {};
    const lines = report.route_code === "direct_comminution"
      ? [
        ["Feed Ag grade", metrics.feed_ag_grade_percent, "%"],
        ["Target Ag grade", metrics.target_ag_grade_percent, "%"],
        ["Ag recovery", metrics.ag_recovery_percent, "%"],
        ["Enrichment ratio", metrics.enrichment_ratio, "×"],
        ["Cost / recovered Ag", metrics.cost_inr_per_kg_recovered_ag, "INR/kg Ag"],
      ]
      : [
        ["Intact-cell recovery", metrics.intact_cell_recovery_percent, "%"],
        ["Target residual-polymer grade", metrics.target_residual_polymer_grade_percent, "%"],
      ];
    const formulaItems = Object.entries(metrics.formulas || {}).map(([label, formula]) =>
      `<li><strong>${escapeHTML(label)}</strong>: ${escapeHTML(formula)}</li>`).join("");
    const flags = (report.flags || []).map((flag) => `<li>${escapeHTML(flag)}</li>`).join("");
    $("#material-run-detail").innerHTML = `<div class="report-heading"><strong>${escapeHTML(report.run_id)} · ${escapeHTML(report.route_code.replaceAll("_", " "))}</strong><span>Ledger integrity: ${escapeHTML(report.integrity.status)}</span></div>
      <div class="report-metrics">${lines.map(([label, amount, unit]) => `<div class="metric-block"><strong>${display(amount, 3)}${unit === "×" ? " ×" : unit === "%" ? "%" : ""}</strong><span>${escapeHTML(label)}${unit === "INR/kg Ag" && amount != null ? ` · ₹${display(amount)} ${unit}` : ""}</span></div>`).join("")}
      <div class="metric-block"><strong>${report.mass_closure_percent == null ? "—" : `${display(report.mass_closure_percent)}%`}</strong><span>Mass closure</span></div>
      <div class="metric-block"><strong>${report.specific_energy_kwh_per_kg_feed == null ? "—" : `${display(report.specific_energy_kwh_per_kg_feed, 4)} kWh/kg`}</strong><span>Specific energy</span></div></div>
      <div class="report-columns"><div><h3>Equations</h3><ul>${formulaItems}</ul></div><div><h3>Data gaps</h3><ul>${flags || "<li>No calculation flags.</li>"}</ul></div></div>
      <p class="section-caption">Mass closure = ${escapeHTML(report.mass_closure_formula)}. No process target is inferred where required mass or assay evidence is absent.</p>`;
  }

  window.refreshMaterials = async function refreshMaterials() {
    try {
      const [recordsResponse, reportsResponse] = await Promise.all([
        fetch("/api/material/records"), fetch("/api/material/compare"),
      ]);
      if (!recordsResponse.ok || !reportsResponse.ok) throw new Error("Material ledger unavailable");
      materialRecords = await recordsResponse.json();
      runReports = await reportsResponse.json();
      renderRecords();
      renderRuns();
    } catch (error) {
      status("mat-record-status", error.message, true);
    }
  };

  $("#material-record-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const body = {
      record_id: value("mat-record-id") || undefined,
      record_type: value("mat-record-type"), parent_record_ids: ids("mat-parents"),
      panel_ids: ids("mat-panels"), stage_event_ids: ids("mat-events"),
      material_label: value("mat-label"), mass_g: Number(value("mat-mass")),
      mass_basis: value("mat-basis"), route_code: value("mat-route") || null,
      size_min_mm: numberOrNull("mat-size-min"), size_max_mm: numberOrNull("mat-size-max"),
      operator_id: value("mat-operator"), instrument_id: value("mat-instrument"),
      calibration_ref: value("mat-calibration"),
    };
    try {
      const saved = await post("/api/material/records", body);
      $("#mat-record-id").value = "";
      $("#mat-parents").value = "";
      $("#mat-label").value = "";
      $("#mat-mass").value = "";
      status("mat-record-status", `Saved ${saved.record_id}`);
      await window.refreshMaterials();
    } catch (error) { status("mat-record-status", error.message, true); }
  });

  $("#material-assay-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const saved = await post("/api/material/assays", {
        sample_id: value("assay-sample"), analyte: value("assay-analyte"),
        mass_fraction: Number(value("assay-fraction")),
        uncertainty_fraction: numberOrNull("assay-uncertainty"),
        detection_limit_fraction: numberOrNull("assay-detection"),
        method: value("assay-method"), laboratory: value("assay-lab"),
        instrument_id: value("assay-instrument"), calibration_ref: value("assay-calibration"),
        operator_id: value("assay-operator"),
      });
      $("#assay-sample").value = "";
      $("#assay-fraction").value = "";
      status("assay-status", `Saved ${saved.record_id}`);
      await window.refreshMaterials();
    } catch (error) { status("assay-status", error.message, true); }
  });

  $("#material-run-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const saved = await post("/api/material/runs", {
        record_id: value("run-id") || undefined, route_code: value("run-route"),
        feed_record_ids: ids("run-feeds"), output_record_ids: ids("run-outputs"),
        target_output_ids: ids("run-targets"), outputs_complete: $("#run-complete").checked,
        target_description: value("run-target-description"), energy_kwh: numberOrNull("run-energy"),
        duration_min: numberOrNull("run-duration"), cost_inr: numberOrNull("run-cost"),
        operator_id: value("run-operator"), instrument_id: value("run-instrument"),
        calibration_ref: value("run-calibration"), method: value("run-method"),
        receiver_status: value("run-receiver"),
      });
      $("#run-id").value = "";
      status("run-status", `Saved ${saved.record_id}`);
      await window.refreshMaterials();
      const report = runReports.find((item) => item.run_id === saved.record_id);
      if (report) renderReport(report);
    } catch (error) { status("run-status", error.message, true); }
  });

  $("#material-runs-body").addEventListener("click", (event) => {
    const button = event.target.closest("[data-material-report]");
    const report = runReports.find((item) => item.run_id === button?.dataset.materialReport);
    if (report) renderReport(report);
  });

  $("#export-materials").addEventListener("click", () => {
    const file = new Blob([JSON.stringify({ exported_at: new Date().toISOString(), records: materialRecords, route_reports: runReports }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(file);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "agastya-material-trials.json";
    anchor.click();
    URL.revokeObjectURL(url);
  });
})();
