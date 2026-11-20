const $ = (selector) => document.querySelector(selector);
const LABELS = ["clean", "dust", "crack", "broken", "burned", "snow", "bird_drop", "other"];
let inspectionRows = [];
let panelRows = [];
let currentImageData = "";
let webcamStream = null;
let currentInspectionRecord = null;
let hardwareStatusRequestId = 0;

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]);
}

function pretty(value) {
  return String(value || "—").replaceAll("_", " ").toLowerCase().replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
}

async function request(path, options = {}) {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 60000);
  try {
    const response = await fetch(path, { ...options, signal: controller.signal });
    let result;
    try {
      result = await response.json();
    } catch {
      throw new Error(`EYE returned an unreadable response (${response.status})`);
    }
    if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`);
    return result;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("The EYE request timed out. The server may still be processing; check the ledger before retrying.");
    }
    if (error instanceof TypeError) {
      throw new Error(`Cannot reach the EYE server at ${window.location.origin}. Check that it is running, then retry.`);
    }
    throw error;
  } finally {
    window.clearTimeout(timeout);
  }
}

function setStatus(element, message, kind = "") {
  element.textContent = message;
  element.className = `inline-status${kind ? ` ${kind}` : ""}`;
}

function updateModalityControls() {
  const rgb = $("#camera-modality").value === "visible_rgb";
  $("#confirmed-visual-label").disabled = !rgb;
  if (!rgb) $("#confirmed-visual-label").value = "";
}

function decisionTag(value) {
  const normalized = String(value || "").toLowerCase();
  return `<span class="decision-tag ${escapeHTML(normalized)}">${escapeHTML(pretty(value))}</span>`;
}

function showPage(page) {
  document.querySelectorAll(".page-view").forEach((element) => element.classList.toggle("active", element.id === `page-${page}`));
  document.querySelectorAll(".nav-item").forEach((element) => element.classList.toggle("active", element.dataset.page === page));
  if (page === "ledger") refreshLedger();
  if (page === "data") refreshData();
  if (page === "materials") window.refreshMaterials?.();
}

function setImage(data, filename = "Captured image") {
  currentImageData = data;
  currentInspectionRecord = null;
  hardwareStatusRequestId += 1;
  $("#hardware-release-panel").hidden = true;
  const preview = $("#image-preview");
  preview.src = data;
  preview.hidden = false;
  $(".empty-image").hidden = true;
  $("#upload-title").textContent = filename;
  $("#upload-detail").textContent = "Image ready for inspection";
  $("#modality-result").textContent = pretty($("#camera-modality").value);
  $("#evidence-title").textContent = "Image ready";
  $("#evidence-index").textContent = "UNSAVED";
  $("#visual-result").textContent = "Pending inspection";
  $("#severity-result").textContent = "Not estimated · no validated field model";
  $("#route-result").textContent = "—";
  $("#sort-destination-result").textContent = "—";
  $("#sort-lane-card").className = "sort-lane-card hold";
  $("#sort-lane-result").textContent = "HOLD · MANUAL CHECK";
  $("#sort-lane-detail").textContent = "Save an inspection to calculate the lane.";
  $("#route-status-result").textContent = "Pending";
  $("#triage-result").textContent = "—";
  $("#technology-result").textContent = "Unknown";
  $("#dimensions-result").textContent = "Not recorded";
  $("#area-result").textContent = "Not calculated";
  $("#junction-result").textContent = "Unknown";
  $("#electrical-result").textContent = "Not tested";
  $("#power-result").textContent = "Not calculated";
  $("#research-estimate-result").textContent = "Not available for RGB";
  $("#integrity-result").textContent = "Pending save";
  $("#final-result").textContent = "—";
  $("#decision-reason").textContent = "Save the inspection to record this image and its evidence.";
  $("#prediction-list").replaceChildren();
}

function renderEvidence(record) {
  $("#panel-technology").value = record.panel_technology || "unknown";
  $("#frame-width").value = record.frame_width_mm ?? "";
  $("#frame-height").value = record.frame_height_mm ?? "";
  $("#rated-power").value = record.rated_power_w ?? "";
  $("#junction-box-location").value = record.junction_box_location || "unknown";
  $("#electrical-test").value = record.electrical_test || "not_tested";
  $("#electrical-method").value = record.electrical_method || "";
  $("#electrical-instrument").value = record.electrical_instrument || "";
  $("#electrical-operator").value = record.electrical_operator || "";
  $("#voltage").value = record.voltage ?? "";
  $("#current").value = record.current ?? "";
  $("#power").value = record.power ?? "";
  $("#confirmed-visual-label").value = record.confirmed_visual_label || "";
  $("#final-route").value = record.final_route || "";
  $("#final-disposition").value = record.final_disposition === "PENDING_REVIEW" ? "" : (record.final_disposition || "");
  $("#reviewer-note").value = record.reviewer_note || "";
  $("#stage2-isolation-confirmed").checked = Boolean(record.stage2_isolation_confirmed);
  $("#camera-modality").value = record.camera_modality || "visible_rgb";
  $("#capture-view").value = record.capture_view || "unspecified";
  $("#camera-sensor-id").value = record.camera_sensor_id || "unknown";
  $("#capture-group-id").value = record.capture_group_id || "";
  updateModalityControls();
  $("#evidence-title").textContent = record.panel_id;
  $("#evidence-index").textContent = `INSPECTION ${String(record.id).padStart(6, "0")}`;
  $("#image-preview").src = record.image_url;
  $("#image-preview").hidden = false;
  $(".empty-image").hidden = true;
  const primaryPredictions = (record.predictions || []).filter((item) => !item.advisory_only);
  const supplementalPredictions = (record.predictions || []).filter((item) => item.advisory_only);
  const top = primaryPredictions[0] || supplementalPredictions[0];
  $("#modality-result").textContent = `${pretty(record.camera_modality || "visible_rgb")} · ${pretty(record.capture_view || "unspecified")}${record.camera_sensor_id ? ` · ${record.camera_sensor_id}` : ""}`;
  $("#visual-result").textContent = top
    ? `${supplementalPredictions.length && !primaryPredictions.length ? "Research hint: " : ""}${pretty(top.label)} · ${Math.round(top.confidence * 100)}%`
    : record.camera_modality && record.camera_modality !== "visible_rgb"
      ? record.camera_modality === "thermal_infrared" ? "No compatible thermal prediction" : "No model for this modality"
      : "Solar model unavailable";
  $("#severity-result").textContent = "Not estimated · research benchmark is not field-calibrated";
  $("#technology-result").textContent = pretty(record.panel_technology);
  $("#dimensions-result").textContent = record.frame_width_mm != null && record.frame_height_mm != null
    ? `${record.frame_width_mm} × ${record.frame_height_mm} mm`
    : "Not recorded";
  const estimates = record.inspection_estimates || {};
  $("#area-result").textContent = estimates.panel_area_m2 == null
    ? "Enter both frame dimensions"
    : `${estimates.panel_area_m2.toFixed(3)} m² · outer frame area`;
  $("#junction-result").textContent = pretty(record.junction_box_location);
  const readings = [
    record.voltage == null ? "" : `${record.voltage} V`,
    record.current == null ? "" : `${record.current} A`,
    record.power == null ? "" : `${record.power} W`,
  ].filter(Boolean).join(" · ");
  $("#electrical-result").textContent = `${pretty(record.electrical_test)}${readings ? ` · ${readings}` : ""}`;
  const powerParts = [];
  if (estimates.power_w != null) {
    powerParts.push(`${estimates.power_w.toFixed(1)} W${estimates.power_source === "voltage_current_product" ? " · V×I calculated" : " · recorded"}`);
  }
  if (estimates.nameplate_output_pct != null) {
    powerParts.push(`${estimates.nameplate_output_pct.toFixed(1)}% of rating · uncorrected snapshot`);
    if (estimates.below_nameplate_pct > 0) powerParts.push(`${estimates.below_nameplate_pct.toFixed(1)}% below nameplate`);
  } else if (record.rated_power_w == null) {
    powerParts.push("Add nameplate watts for comparison");
  }
  $("#power-result").textContent = powerParts.join(" · ") || "Record voltage and current";
  const research = record.power_loss_estimate || {};
  $("#research-estimate-result").textContent = research.status === "research_only"
    ? `${research.estimated_power_loss_pct}% · ${pretty(research.benchmark_band)} · n=${research.training_samples}, ${research.training_cells?.length || 0} cells · MAE ${Number(research.held_out_mae_pct_points).toFixed(1)} pp`
    : research.reason || "Not available for this modality";
  $("#research-estimate-result").title = research.warning || "Research benchmark only; not used for routing or sorting.";
  $("#route-result").textContent = pretty(record.recommended_route);
  const destination = record.sort_recommendation?.destination || "MANUAL_REVIEW";
  $("#sort-destination-result").textContent = `${pretty(destination)} · recommendation only`;
  const lane = record.sort_lane_decision || {};
  const laneState = ["LEFT", "RIGHT"].includes(lane.lane) ? lane.lane.toLowerCase() : "hold";
  $("#sort-lane-card").className = `sort-lane-card ${laneState}`;
  $("#sort-lane-result").textContent = lane.label || "HOLD · MANUAL CHECK";
  $("#sort-lane-detail").textContent = lane.instruction || "No lane transfer is authorized.";
  $("#route-status-result").textContent = `${pretty(record.final_route)}${record.route_source === "manual" ? " · Operator-set" : " · Rule-set"}`;
  $("#triage-result").textContent = pretty(record.recommended_disposition);
  $("#final-result").textContent = pretty(record.final_disposition);
  $("#integrity-result").textContent = record.record_hash ? "Record hash stored · see passport for chain verification" : "Legacy record · no hash";
  $("#decision-reason").textContent = `${record.route_reason || record.decision_reason}${record.reviewer_note ? ` Reviewer: ${record.reviewer_note}` : ""}`;
  const predictions = [...primaryPredictions.slice(0, 3), ...supplementalPredictions.slice(0, 3)];
  $("#prediction-list").innerHTML = predictions.map((item) => {
    const percent = Math.round(item.confidence * 100);
    const sourceNote = item.advisory_only ? '<small title="Not an electrical test or burn diagnosis">Research only · not routed</small>' : "";
    return `<div class="prediction"><span>${escapeHTML(pretty(item.label))}${sourceNote}</span><span class="prediction-track"><span class="prediction-fill" style="display:block;width:${percent}%"></span></span><em>${percent}%</em></div>`;
  }).join("");
  currentInspectionRecord = record;
  refreshHardwareApproval(record);
}

async function refreshHardwareApproval(record) {
  const panel = $("#hardware-release-panel");
  const requestId = ++hardwareStatusRequestId;
  panel.hidden = false;
  $("#hardware-release-state").textContent = "Checking";
  $("#hardware-release-detail").textContent = "Checking backend, inspection, and Arduino readiness…";
  $("#hardware-release-message").textContent = "";
  $("#hardware-release-message").className = "inline-status";
  $("#hardware-approval-fields").hidden = true;
  $("#hardware-release-button").disabled = true;
  $("#hardware-connect-button").hidden = true;
  try {
    const data = await request(`/api/v1/hardware/inspections/${record.id}/release`);
    if (requestId !== hardwareStatusRequestId || currentInspectionRecord?.id !== record.id) return;
    const hardware = data.hardware || {};
    const approval = data.approval;
    const eligibility = data.eligibility || { eligible: false, reason: "Release eligibility is unavailable" };
    $("#hardware-release-state").textContent = approval ? pretty(approval.state) : pretty(hardware.state || "unknown");
    if (approval) {
      $("#hardware-release-detail").textContent = approval.state === "uncertain"
        ? "The command outcome is uncertain. Inspect the gate; this inspection cannot be retried."
        : approval.state === "closed_commanded"
          ? "Arduino acknowledged the release and timed close commands. A position sensor does not verify physical motion."
          : "A one-time release request is already recorded for this inspection.";
      $("#hardware-release-message").textContent = `Approval ${approval.command_id} · ${pretty(approval.state)}`;
      $("#hardware-release-button").disabled = true;
      return;
    }

    $("#hardware-release-detail").textContent = eligibility.reason;
    $("#hardware-connect-button").hidden = !hardware.enabled || Boolean(hardware.ready);
    $("#hardware-approval-fields").hidden = !eligibility.eligible;
    $("#hardware-panel-confirmation").value = "";
    $("#hardware-release-button").disabled = !eligibility.eligible || !hardware.ready;
  } catch (error) {
    if (requestId !== hardwareStatusRequestId) return;
    $("#hardware-release-state").textContent = "Unavailable";
    $("#hardware-release-detail").textContent = error.message;
    $("#hardware-release-message").className = "inline-status error";
  }
}

function renderInspectionRows(rows) {
  const query = $("#ledger-search").value.trim().toLowerCase();
  const filtered = rows.filter((record) => [record.panel_id, record.external_ref, record.recommended_route, record.final_route, record.final_disposition, record.predictions?.[0]?.label].join(" ").toLowerCase().includes(query));
  $("#ledger-body").innerHTML = filtered.map((record) => {
    const primaryPrediction = record.predictions?.find((item) => !item.advisory_only);
    const advisoryPrediction = record.predictions?.find((item) => item.advisory_only);
    const visual = primaryPrediction
      ? `${pretty(primaryPrediction.label)} · ${Math.round(primaryPrediction.confidence * 100)}%`
      : advisoryPrediction
        ? `Research: ${pretty(advisoryPrediction.label)}`
      : `${pretty(record.camera_modality || "visible_rgb")} · not modeled`;
    return `<tr>
      <td><span class="panel-code">${escapeHTML(record.panel_id)}</span>${record.external_ref ? `<span class="sub-cell">${escapeHTML(record.external_ref)}</span>` : ""}</td>
      <td>${escapeHTML(formatDate(record.created_at))}</td>
      <td>${escapeHTML(record.device_id || "PC upload")}</td>
      <td>${escapeHTML(visual)}</td>
      <td>${decisionTag(record.final_route)}</td>
      <td>${decisionTag(record.final_disposition)}</td>
      <td><a class="source-link" href="${escapeHTML(record.image_url)}" target="_blank" rel="noopener">Open</a></td>
      <td><button class="table-action" data-view-inspection="${record.id}">View</button></td>
    </tr>`;
  }).join("");
  $("#ledger-empty").hidden = filtered.length > 0;
}

function renderPanels(rows) {
  $("#panel-existing").innerHTML = `<option value="">New panel ID will be assigned</option>${rows.map((panel) => `<option value="${escapeHTML(panel.panel_id)}">${escapeHTML(panel.panel_id)}${panel.external_ref ? ` · ${escapeHTML(panel.external_ref)}` : ""}</option>`).join("")}`;
  $("#panels-body").innerHTML = rows.map((panel) => `<tr>
    <td><span class="panel-code">${escapeHTML(panel.panel_id)}</span></td>
    <td>${escapeHTML(panel.external_ref || "—")}</td>
    <td>${escapeHTML(formatDate(panel.created_at))}</td>
    <td>${panel.inspection_count}</td>
    <td>${escapeHTML(pretty(panel.last_panel_technology))}</td>
    <td>${panel.frame_width_mm != null && panel.frame_height_mm != null ? `${escapeHTML(panel.frame_width_mm)} × ${escapeHTML(panel.frame_height_mm)}` : "—"}</td>
    <td>${escapeHTML(pretty(panel.junction_box_location))}</td>
    <td>${panel.stage_event_count || 0}${panel.last_stage_code ? `<span class="sub-cell">${escapeHTML(pretty(panel.last_stage_code))} · ${escapeHTML(pretty(panel.last_stage_event_type))}</span>` : ""}</td>
    <td>${panel.last_disposition ? decisionTag(panel.last_disposition) : "—"}${panel.last_route ? `<span class="sub-cell">${escapeHTML(pretty(panel.last_route))}</span>` : ""}</td>
    <td><a class="table-action" href="/api/v1/panels/${encodeURIComponent(panel.panel_id)}/passport" target="_blank" rel="noopener">Passport</a> <button class="table-action" data-inspect-panel="${escapeHTML(panel.panel_id)}">Inspect</button></td>
  </tr>`).join("");
  $("#panels-empty").hidden = rows.length > 0;
  $("#panel-count").textContent = `${rows.length} panels`;
  $("#ledger-summary").innerHTML = `<div class="metric-block"><strong>${rows.length}</strong><span>Registered panels</span></div><div class="metric-block"><strong>${inspectionRows.length}</strong><span>Inspection records</span></div>`;
  $("#footer-counts").textContent = `${rows.length} panels · ${inspectionRows.length} inspections`;
}

async function refreshLedger() {
  try {
    [inspectionRows, panelRows] = await Promise.all([request("/api/inspections"), request("/api/panels")]);
    renderInspectionRows(inspectionRows);
    renderPanels(panelRows);
  } catch (error) {
    $("#ledger-empty").hidden = false;
    $("#ledger-empty").textContent = error.message;
  }
}

async function refreshData() {
  try {
    const data = await request("/api/datasets");
    const imageTotal = data.sources.reduce((sum, source) => sum + source.images, 0);
    $("#dataset-status-row").innerHTML = `
      <div class="metric-block"><strong>${data.sources.length}</strong><span>Raw datasets · ${imageTotal} images</span></div>
      <div class="metric-block"><strong>${data.mapping_rows}</strong><span>Class mappings</span></div>
      <div class="metric-block"><strong>${Object.values(data.processed.train).reduce((a, b) => a + b, 0)}</strong><span>Processed train images</span></div>
      <div class="metric-block"><strong>${data.human_labeled_images ?? 0}</strong><span>Human-confirmed captures</span></div>`;
    $("#mapping-body").innerHTML = data.mappings.map((row) => `<tr>
      <td>${escapeHTML(row.source_id)}<span class="sub-cell">${escapeHTML(row.source_version)}</span></td><td>${escapeHTML(row.original_class)}</td><td>${escapeHTML(row.normalized_class)}</td><td>${escapeHTML(row.task || "RGB image classification")} · ${escapeHTML(row.modality || "visible_rgb")}</td>
      <td>${escapeHTML(row.license)}</td><td><a class="source-link" href="${escapeHTML(/^https?:\/\//i.test(row.source_url) ? row.source_url : "#")}" target="_blank" rel="noopener">Source ↗</a></td>
    </tr>`).join("");
    $("#mapping-empty").hidden = data.mappings.length > 0;
    $("#class-counts").innerHTML = LABELS.map((label) => `<tr><td class="class-cell">${escapeHTML(pretty(label))}</td><td>${data.processed.train[label]}</td><td>${data.processed.validation[label]}</td><td>${data.processed.test[label]}</td></tr>`).join("");
    const benchmarks = data.pv_degradation_benchmarks || [];
    const benchmarkRows = $("#severity-benchmark-folds");
    const benchmarkEmpty = $("#severity-benchmark-empty");
    if (benchmarks.length) {
      const summary = benchmarks.map((benchmark) => `${pretty(benchmark.modality)} ${benchmark.overall_metrics.mae_pct_points.toFixed(2)} points MAE`).join(" · ");
      $("#severity-benchmark-note").textContent = `${summary}. Each uses ${benchmarks[0].samples} samples from ${benchmarks[0].physical_cells.length} physical cells and holds one cell out per fold. Research only: controlled close-up cells, not ESP32 full-panel estimates.`;
      benchmarkRows.innerHTML = benchmarks.flatMap((benchmark) => benchmark.folds.map((fold) => `<tr><td>${escapeHTML(benchmark.modality)}</td><td>${escapeHTML(fold.held_out_cell)}</td><td>${fold.n}</td><td>${fold.mae_pct_points.toFixed(2)}</td><td>${fold.mean_predictor_mae_pct_points.toFixed(2)}</td></tr>`)).join("");
      benchmarkEmpty.hidden = true;
    } else {
      $("#severity-benchmark-note").textContent = "No cell-held-out severity benchmark has been run.";
      benchmarkRows.replaceChildren();
      benchmarkEmpty.hidden = false;
    }
    const thermal = data.thermal_model || { ready: false, message: "No thermal-specific model status available." };
    const thermalMetrics = thermal.evaluation?.test_images
      ? ` Image-level held-out test: ${(thermal.evaluation.test_accuracy * 100).toFixed(1)}% accuracy, ${(thermal.evaluation.test_macro_f1 * 100).toFixed(1)}% macro F1 across ${thermal.evaluation.test_images} images.`
      : "";
    const thermalClasses = thermal.classes?.length ? ` Classes: ${thermal.classes.map(pretty).join(", ")}.` : "";
    $("#thermal-model-note").textContent = `${thermal.message}${thermalMetrics}${thermalClasses}`;
    const surface = data.visible_crop_model || { ready: false, message: "No visible close-up research model status available." };
    const surfaceEvaluation = surface.evaluation;
    const broken = surfaceEvaluation?.per_class?.broken;
    const surfaceMetrics = surfaceEvaluation?.test_images
      ? ` Held-out image-level test: ${(surfaceEvaluation.test_macro_f1 * 100).toFixed(1)}% macro F1 across ${surfaceEvaluation.test_images} images${broken ? `; broken precision ${(broken.precision * 100).toFixed(1)}%, recall ${(broken.recall * 100).toFixed(1)}%, F1 ${(broken.f1 * 100).toFixed(1)}%` : ""}.`
      : "";
    const sourceLicense = surface.source_license_status ? ` Source license: ${surface.source_license_status}.` : "";
    $("#visible-crop-model-note").textContent = `${surface.message}${surfaceMetrics}${sourceLicense}`;
    if ([thermal, surface].some((model) => model.ready && model.loaded === false)) {
      window.setTimeout(refreshData, 2500);
    }
  } catch (error) {
    $("#dataset-status-row").textContent = error.message;
  }
}

async function refreshStatus() {
  try {
    const status = await request("/api/status");
    const banner = $("#model-banner");
    const databaseHealthy = status.database?.healthy !== false;
    banner.classList.toggle("ready", status.model.ready && status.model.loaded !== false && databaseHealthy);
    const evaluation = status.model.evaluation;
    const testSummary = evaluation?.test_images
      ? ` · held-out ${(evaluation.test_accuracy * 100).toFixed(0)}% acc, ${(evaluation.test_macro_f1 * 100).toFixed(0)}% macro F1 (${evaluation.test_images} images)`
      : "";
    const databaseSummary = databaseHealthy ? " · inspection database healthy" : " · inspection database unavailable";
    const hardwareSummary = status.hardware?.enabled
      ? ` · Arduino ${status.hardware.ready ? "ready" : status.hardware.state}`
      : " · Arduino gate disabled";
    banner.querySelector("span:last-child").textContent = `${status.model.message}${testSummary}${databaseSummary}${hardwareSummary}`;
    $("#sidebar-model").textContent = !databaseHealthy
      ? "Inspection database unavailable"
      : status.model.ready
      ? (status.model.loaded === false ? "RGB checkpoint available · warming" : "RGB screen ready · review required")
      : "RGB model unavailable";
    $("#footer-counts").textContent = `${status.panels} panels · ${status.inspections} inspections`;
    if (status.model.ready && status.model.loaded === false) {
      window.setTimeout(refreshStatus, 2500);
    }
    await refreshHardwareSettings();
  } catch (error) {
    $("#sidebar-model").textContent = "App API unavailable";
    const banner = $("#model-banner");
    banner.classList.remove("ready");
    banner.querySelector("span:last-child").textContent = `Cannot reach EYE API: ${error.message}`;
  }
}

async function refreshHardwareSettings() {
  try {
    const hardware = await request("/api/v1/hardware/status");
    const portInput = $("#hardware-port");
    if (document.activeElement !== portInput) portInput.value = hardware.port || "";
    $("#hardware-settings-state").textContent = `${pretty(hardware.state)}${hardware.port ? ` · ${hardware.port}` : ""}`;
    $("#hardware-enable-button").hidden = Boolean(hardware.enabled);
    $("#hardware-enable-button").disabled = hardware.state === "misconfigured" || !/^COM[1-9]\d*$/i.test(portInput.value.trim());
    $("#hardware-global-connect-button").hidden = !hardware.enabled || Boolean(hardware.ready);
    $("#hardware-disable-button").hidden = !hardware.enabled;
    $("#hardware-settings-detail").textContent = hardware.enabled
      ? (hardware.ready
        ? "Arduino is ready. Each release still requires a separate eligible inspection and operator confirmation."
        : hardware.message || "Gate enabled for this session. Connect the configured Arduino to continue.")
      : "Gate activation is off by default. Enter the Uno/Nano COM port from Windows Device Manager. This setting lasts for this server session.";
  } catch (error) {
    $("#hardware-settings-state").textContent = "Unavailable";
    $("#hardware-settings-detail").textContent = error.message;
  }
}

async function configureHardware(enabled) {
  const port = $("#hardware-port").value.trim();
  if (enabled && !/^COM[1-9]\d*$/i.test(port)) {
    setStatus($("#hardware-settings-message"), "Enter the Arduino COM port shown by Windows, for example COM5.", "error");
    return;
  }
  const buttons = ["#hardware-enable-button", "#hardware-disable-button"];
  buttons.forEach((selector) => { $(selector).disabled = true; });
  setStatus($("#hardware-settings-message"), enabled ? "Enabling gate controls for this server session…" : "Disabling gate controls…");
  try {
    const result = await request("/api/v1/hardware/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled, port }),
    });
    setStatus($("#hardware-settings-message"), enabled
      ? `Gate enabled for this session on ${result.hardware.port}; connect the Arduino to continue.`
      : "Gate disabled for this session.", "success");
  } catch (error) {
    setStatus($("#hardware-settings-message"), error.message, "error");
  } finally {
    await refreshHardwareSettings();
    if (currentInspectionRecord) await refreshHardwareApproval(currentInspectionRecord);
    $("#hardware-enable-button").disabled = !/^COM[1-9]\d*$/i.test($("#hardware-port").value.trim());
    $("#hardware-disable-button").disabled = false;
  }
}

$("#image-file").addEventListener("change", (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  if (file.size > 16 * 1024 * 1024) {
    setStatus($("#capture-status"), "Image exceeds the 16 MB limit", "error");
    event.target.value = "";
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    setImage(String(reader.result), file.name);
    setStatus($("#capture-status"), "Image ready", "success");
  };
  reader.onerror = () => setStatus($("#capture-status"), "Could not read this image", "error");
  reader.readAsDataURL(file);
});

$("#camera-modality").addEventListener("change", () => {
  updateModalityControls();
  $("#modality-result").textContent = pretty($("#camera-modality").value);
});

$("#capture-button").addEventListener("click", async () => {
  const button = $("#capture-button");
  button.disabled = true;
  setStatus($("#capture-status"), "Connecting to camera…");
  try {
    const result = await request("/api/capture", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ camera_url: $("#camera-url").value }),
    });
    $("#image-file").value = "";
    setImage(result.image_data);
    setStatus($("#capture-status"), "Image captured from ESP32", "success");
  } catch (error) {
    setStatus($("#capture-status"), error.message, "error");
  } finally {
    button.disabled = false;
  }
});

function stopWebcam() {
  if (webcamStream) webcamStream.getTracks().forEach((track) => track.stop());
  webcamStream = null;
  $("#webcam-preview").srcObject = null;
  $("#webcam-preview").hidden = true;
  $("#webcam-start").disabled = false;
  $("#webcam-capture").disabled = true;
  $("#webcam-stop").disabled = true;
  $("#webcam-stream-info").textContent = "Not connected";
  $("#webcam-advanced").hidden = true;
}

function selectedWebcamResolution() {
  const [width, height] = $("#webcam-resolution").value.split("x").map(Number);
  return { width, height };
}

function webcamSensorId(label) {
  const id = String(label || "")
    .normalize("NFKD")
    .replace(/[^A-Za-z0-9_.:-]+/g, "-")
    .replace(/^[^A-Za-z0-9]+/, "")
    .replace(/-+$/, "")
    .slice(0, 80);
  return id || "usb-webcam";
}

async function refreshWebcamDevices(activeDeviceId = "") {
  const select = $("#webcam-device");
  const devices = await navigator.mediaDevices.enumerateDevices();
  const cameras = devices.filter((device) => device.kind === "videoinput");
  select.innerHTML = `<option value="">System default</option>${cameras.map((camera, index) =>
    `<option value="${escapeHTML(camera.deviceId)}">${escapeHTML(camera.label || `Camera ${index + 1}`)}</option>`).join("")}`;
  if (activeDeviceId && cameras.some((camera) => camera.deviceId === activeDeviceId)) {
    select.value = activeDeviceId;
  }
}

function updateWebcamReadout() {
  if (!webcamStream) return;
  const track = webcamStream.getVideoTracks()[0];
  const settings = track.getSettings();
  const video = $("#webcam-preview");
  const width = settings.width || video.videoWidth;
  const height = settings.height || video.videoHeight;
  const fps = settings.frameRate ? ` · ${Math.round(settings.frameRate)} fps` : "";
  $("#webcam-stream-info").textContent = width && height ? `${width} × ${height}${fps}` : "Reading camera mode…";
  $("#camera-sensor-id").value = webcamSensorId(track.label);
  renderWebcamCapabilities(track);
}

function renderWebcamCapabilities(track) {
  const advanced = $("#webcam-advanced");
  const zoomWrap = $("#webcam-zoom-wrap");
  const focusWrap = $("#webcam-focus-wrap");
  zoomWrap.hidden = true;
  focusWrap.hidden = true;
  try {
    const caps = track.getCapabilities?.() || {};
    if (caps.zoom && Number.isFinite(caps.zoom.min) && Number.isFinite(caps.zoom.max)) {
      const zoom = $("#webcam-zoom");
      zoom.min = caps.zoom.min;
      zoom.max = caps.zoom.max;
      zoom.step = caps.zoom.step || Math.max((caps.zoom.max - caps.zoom.min) / 50, 0.1);
      zoom.value = track.getSettings().zoom ?? caps.zoom.min;
      zoomWrap.hidden = false;
    }
    if (Array.isArray(caps.focusMode) && caps.focusMode.length) {
      const focus = $("#webcam-focus");
      focus.innerHTML = caps.focusMode.map((mode) =>
        `<option value="${escapeHTML(mode)}">${escapeHTML(pretty(mode))}</option>`).join("");
      const selected = track.getSettings().focusMode;
      if (selected && caps.focusMode.includes(selected)) focus.value = selected;
      focusWrap.hidden = false;
    }
    advanced.hidden = zoomWrap.hidden && focusWrap.hidden;
  } catch (_) {
    advanced.hidden = true;
  }
}

async function startWebcam() {
  const button = $("#webcam-start");
  button.disabled = true;
  setStatus($("#capture-status"), "Requesting webcam access…");
  try {
    if (!navigator.mediaDevices?.getUserMedia) {
      throw new Error("Webcam access needs a supported browser on localhost or HTTPS.");
    }
    if (webcamStream) {
      const old = webcamStream;
      webcamStream = null;
      old.getTracks().forEach((track) => track.stop());
    }
    const resolution = selectedWebcamResolution();
    const videoConstraints = {
      width: { ideal: resolution.width }, height: { ideal: resolution.height },
      frameRate: { ideal: 30, max: 30 },
    };
    if ($("#webcam-device").value) videoConstraints.deviceId = { exact: $("#webcam-device").value };
    webcamStream = await navigator.mediaDevices.getUserMedia({ video: videoConstraints, audio: false });
    const video = $("#webcam-preview");
    video.srcObject = webcamStream;
    video.hidden = false;
    await video.play();
    await refreshWebcamDevices(webcamStream.getVideoTracks()[0].getSettings().deviceId || "");
    $("#camera-modality").value = "visible_rgb";
    $("#capture-view").value = "front";
    updateModalityControls();
    $("#webcam-capture").disabled = false;
    $("#webcam-stop").disabled = false;
    updateWebcamReadout();
    setStatus($("#capture-status"), "Webcam connected · confirm framing and focus, then capture", "success");
  } catch (error) {
    stopWebcam();
    setStatus($("#capture-status"), error.name === "NotAllowedError"
      ? "Camera permission was denied; allow access in the browser and try again."
      : error.name === "OverconstrainedError"
        ? "That camera cannot provide the selected mode. Choose 720p or 480p and try again."
        : error.message || "Could not connect to the webcam", "error");
  }
}

$("#webcam-start").addEventListener("click", startWebcam);
$("#webcam-device").addEventListener("change", () => { if (webcamStream) startWebcam(); });
$("#webcam-resolution").addEventListener("change", () => { if (webcamStream) startWebcam(); });

async function applyWebcamConstraint(constraint) {
  const track = webcamStream?.getVideoTracks()[0];
  if (!track) return;
  try {
    await track.applyConstraints({ advanced: [constraint] });
    updateWebcamReadout();
  } catch (_) {
    setStatus($("#webcam-quality"), "This camera does not support that control; use its hardware controls or change distance/light.", "error");
  }
}

$("#webcam-zoom").addEventListener("input", (event) => {
  applyWebcamConstraint({ zoom: Number(event.target.value) });
});
$("#webcam-focus").addEventListener("change", (event) => {
  applyWebcamConstraint({ focusMode: event.target.value });
});

function inspectFrameQuality(canvas) {
  const width = 160;
  const height = 120;
  const sample = document.createElement("canvas");
  sample.width = width;
  sample.height = height;
  const context = sample.getContext("2d", { willReadFrequently: true });
  context.drawImage(canvas, 0, 0, width, height);
  const pixels = context.getImageData(0, 0, width, height).data;
  const gray = new Float32Array(width * height);
  let light = 0;
  let dark = 0;
  let clipped = 0;
  for (let i = 0, p = 0; i < pixels.length; i += 4, p += 1) {
    const value = 0.2126 * pixels[i] + 0.7152 * pixels[i + 1] + 0.0722 * pixels[i + 2];
    gray[p] = value;
    light += value;
    if (value < 24) dark += 1;
    if (value > 246) clipped += 1;
  }
  let lapSum = 0;
  let lapSquared = 0;
  let count = 0;
  for (let y = 1; y < height - 1; y += 1) {
    for (let x = 1; x < width - 1; x += 1) {
      const i = y * width + x;
      const lap = gray[i - width] + gray[i - 1] - 4 * gray[i] + gray[i + 1] + gray[i + width];
      lapSum += lap;
      lapSquared += lap * lap;
      count += 1;
    }
  }
  const sharpness = lapSquared / count - (lapSum / count) ** 2;
  const total = width * height;
  const average = light / total;
  const warnings = [];
  if (average < 48 || dark / total > 0.25) warnings.push("dim; add diffuse light");
  if (clipped / total > 0.18) warnings.push("highlights/shadows clipped; reduce glare or improve lighting");
  if (sharpness < 55) warnings.push("low edge detail; steady camera and refocus/retake closer");
  const resolution = `${canvas.width} × ${canvas.height}`;
  const message = `Captured ${resolution} · ${warnings.length ? warnings.join("; ") : "basic exposure and edge-detail checks look usable"}. These checks are indicative, not a validated quality score.`;
  $("#webcam-quality").textContent = message;
  $("#webcam-quality").classList.toggle("warning", warnings.length > 0);
  return { resolution, warnings };
}

$("#webcam-capture").addEventListener("click", async () => {
  const video = $("#webcam-preview");
  if (!webcamStream || !video.videoWidth || !video.videoHeight) {
    setStatus($("#capture-status"), "Wait for the webcam preview, then try again", "error");
    return;
  }
  const button = $("#webcam-capture");
  button.disabled = true;
  try {
    const canvas = $("#webcam-canvas");
    let photo = null;
    const track = webcamStream.getVideoTracks()[0];
    if (window.ImageCapture) {
      try { photo = await new ImageCapture(track).takePhoto(); } catch (_) { photo = null; }
    }
    if (photo) {
      const bitmap = await createImageBitmap(photo);
      canvas.width = bitmap.width;
      canvas.height = bitmap.height;
      canvas.getContext("2d").drawImage(bitmap, 0, 0);
      bitmap.close();
    } else {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    }
    const image = canvas.toDataURL("image/jpeg", 0.9);
    if (image.length > 16 * 1024 * 1024 * 4 / 3) {
      setStatus($("#capture-status"), "Webcam frame exceeds the 16 MB limit", "error");
      return;
    }
    const quality = inspectFrameQuality(canvas);
    $("#image-file").value = "";
    setImage(image, `Webcam capture · ${quality.resolution}`);
    setStatus($("#capture-status"), "Webcam image ready for inspection", quality.warnings.length ? "error" : "success");
  } catch (error) {
    setStatus($("#capture-status"), error.message || "Could not capture a webcam frame", "error");
  } finally {
    button.disabled = !webcamStream;
  }
});

$("#webcam-stop").addEventListener("click", () => {
  stopWebcam();
  setStatus($("#capture-status"), "Webcam disconnected");
});
window.addEventListener("beforeunload", stopWebcam);

$("#panel-existing").addEventListener("change", (event) => {
  const hasExisting = Boolean(event.target.value);
  $("#external-ref").disabled = hasExisting;
  if (hasExisting) $("#external-ref").value = "";
  const selected = panelRows.find((panel) => panel.panel_id === event.target.value);
  $("#panel-technology").value = selected?.last_panel_technology || "unknown";
  $("#frame-width").value = selected?.frame_width_mm ?? "";
  $("#frame-height").value = selected?.frame_height_mm ?? "";
  $("#rated-power").value = selected?.rated_power_w ?? "";
  $("#junction-box-location").value = selected?.junction_box_location || "unknown";
});

$("#inspection-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!currentImageData) {
    setStatus($("#save-status"), "Choose or capture an image first", "error");
    return;
  }
  const button = $("#save-button");
  button.disabled = true;
  setStatus($("#save-status"), "Analyzing and saving…");
  const body = {
    image_data: currentImageData,
    camera_modality: $("#camera-modality").value,
    capture_view: $("#capture-view").value,
    camera_sensor_id: $("#camera-sensor-id").value.trim(),
    capture_group_id: $("#capture-group-id").value.trim(),
    panel_technology: $("#panel-technology").value,
    frame_width_mm: $("#frame-width").value,
    frame_height_mm: $("#frame-height").value,
    rated_power_w: $("#rated-power").value,
    junction_box_location: $("#junction-box-location").value,
    panel_id: $("#panel-existing").value,
    external_ref: $("#external-ref").value.trim(),
    electrical_test: $("#electrical-test").value,
    electrical_method: $("#electrical-method").value.trim(),
    electrical_instrument: $("#electrical-instrument").value.trim(),
    electrical_operator: $("#electrical-operator").value.trim(),
    voltage: $("#voltage").value,
    current: $("#current").value,
    power: $("#power").value,
    final_disposition: $("#final-disposition").value,
    final_route: $("#final-route").value,
    confirmed_visual_label: $("#confirmed-visual-label").value,
    stage2_isolation_confirmed: $("#stage2-isolation-confirmed").checked,
    reviewer_note: $("#reviewer-note").value,
  };
  try {
    const record = await request("/api/inspect", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    });
    panelRows = await request("/api/panels");
    $("#panel-existing").innerHTML = `<option value="">New panel ID will be assigned</option>${panelRows.map((panel) => `<option value="${escapeHTML(panel.panel_id)}">${escapeHTML(panel.panel_id)}${panel.external_ref ? ` · ${escapeHTML(panel.external_ref)}` : ""}</option>`).join("")}`;
    $("#panel-existing").value = record.panel_id;
    $("#external-ref").value = "";
    $("#external-ref").disabled = true;
    $("#final-disposition").value = "";
    $("#final-route").value = "";
    $("#reviewer-note").value = "";
    $("#confirmed-visual-label").value = "";
    $("#stage2-isolation-confirmed").checked = false;
    $("#electrical-method").value = "";
    $("#electrical-instrument").value = "";
    $("#electrical-operator").value = "";
    renderEvidence(record);
    setStatus($("#save-status"), `Saved as ${record.panel_id}`, "success");
    refreshStatus();
  } catch (error) {
    setStatus($("#save-status"), error.message, "error");
  } finally {
    button.disabled = false;
  }
});

$("#hardware-connect-button").addEventListener("click", async () => {
  const button = $("#hardware-connect-button");
  button.disabled = true;
  setStatus($("#hardware-release-message"), "Checking the configured Arduino port…");
  try {
    const result = await request("/api/v1/hardware/connect", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: "{}",
    });
    setStatus($("#hardware-release-message"), result.hardware?.message || "Arduino is ready", "success");
  } catch (error) {
    setStatus($("#hardware-release-message"), error.message, "error");
  } finally {
    button.disabled = false;
    if (currentInspectionRecord) await refreshHardwareApproval(currentInspectionRecord);
  }
});

$("#hardware-enable-button").addEventListener("click", () => configureHardware(true));
$("#hardware-disable-button").addEventListener("click", () => configureHardware(false));
$("#hardware-port").addEventListener("input", () => {
  $("#hardware-enable-button").disabled = !/^COM[1-9]\d*$/i.test($("#hardware-port").value.trim());
});
$("#hardware-global-connect-button").addEventListener("click", async () => {
  const button = $("#hardware-global-connect-button");
  button.disabled = true;
  setStatus($("#hardware-settings-message"), "Checking the configured Arduino port…");
  try {
    const result = await request("/api/v1/hardware/connect", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: "{}",
    });
    setStatus($("#hardware-settings-message"), result.hardware?.message || "Arduino is ready", "success");
  } catch (error) {
    setStatus($("#hardware-settings-message"), error.message, "error");
  } finally {
    button.disabled = false;
    await refreshHardwareSettings();
    if (currentInspectionRecord) await refreshHardwareApproval(currentInspectionRecord);
  }
});

$("#hardware-release-button").addEventListener("click", async () => {
  const record = currentInspectionRecord;
  if (!record) return;
  const operatorId = $("#hardware-operator-id").value.trim();
  const panelConfirmation = $("#hardware-panel-confirmation").value.trim();
  if (!operatorId || panelConfirmation !== record.panel_id) {
    setStatus($("#hardware-release-message"), "Enter an operator ID and type the exact panel ID.", "error");
    return;
  }
  const button = $("#hardware-release-button");
  button.disabled = true;
  setStatus($("#hardware-release-message"), "Recording one-time approval and waiting for Arduino acknowledgement…");
  try {
    const result = await request(`/api/v1/hardware/inspections/${record.id}/release`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ operator_id: operatorId, panel_id_confirmation: panelConfirmation }),
    });
    setStatus($("#hardware-release-message"), result.message, "success");
  } catch (error) {
    setStatus($("#hardware-release-message"), error.message, "error");
  } finally {
    await refreshHardwareApproval(record);
  }
});

$("#ledger-search").addEventListener("input", () => renderInspectionRows(inspectionRows));
document.querySelectorAll(".nav-item").forEach((button) => button.addEventListener("click", () => showPage(button.dataset.page)));
document.querySelectorAll("[data-goto]").forEach((button) => button.addEventListener("click", () => showPage(button.dataset.goto)));
document.addEventListener("click", async (event) => {
  const viewButton = event.target.closest("[data-view-inspection]");
  const inspectButton = event.target.closest("[data-inspect-panel]");
  if (viewButton) {
    try {
      const record = await request(`/api/inspections/${viewButton.dataset.viewInspection}`);
      showPage("inspect");
      renderEvidence(record);
    } catch (error) {
      window.alert(error.message);
    }
  }
  if (inspectButton) {
    showPage("inspect");
    $("#panel-existing").value = inspectButton.dataset.inspectPanel;
    const selected = panelRows.find((panel) => panel.panel_id === inspectButton.dataset.inspectPanel);
    $("#panel-technology").value = selected?.last_panel_technology || "unknown";
    $("#frame-width").value = selected?.frame_width_mm ?? "";
    $("#frame-height").value = selected?.frame_height_mm ?? "";
    $("#rated-power").value = selected?.rated_power_w ?? "";
    $("#junction-box-location").value = selected?.junction_box_location || "unknown";
    $("#external-ref").value = "";
    $("#external-ref").disabled = true;
  }
});

function updateClock() {
  $("#clock").textContent = new Date().toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
}
updateClock();
window.setInterval(updateClock, 30_000);
refreshStatus();
request("/api/panels").then((rows) => {
  panelRows = rows;
  $("#panel-existing").innerHTML = `<option value="">New panel ID will be assigned</option>${rows.map((panel) => `<option value="${escapeHTML(panel.panel_id)}">${escapeHTML(panel.panel_id)}${panel.external_ref ? ` · ${escapeHTML(panel.external_ref)}` : ""}</option>`).join("")}`;
}).catch(() => {});
