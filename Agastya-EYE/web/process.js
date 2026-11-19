(() => {
  const stageData = {
    2: {
      label: "STAGE 2 · DE-FRAMING + DE-JUNCTIONING",
      output: "Aluminium frame, junction box/cables, and the remaining laminate",
      note: "Conceptual station; not a built or validated Agastya machine.",
      steps: [
        ["Panel is identified and supported", "Stage 1 measurements guide how the panel is held. The panel is isolated and supported before dismantling."],
        ["The frame is released", "The thesis proposes one station to remove the aluminium perimeter frame. The exact tool depends on whether a module is clipped or screwed together."],
        ["The junction box and cables are removed", "The rear junction box and output cables are separated and collected. Their materials should be recorded as separate streams."],
        ["The laminate moves to Stage 3", "After frame and junction-box removal, the remaining glass/EVA/cell/backsheet stack is handed to the thermal-separation stage."],
      ],
    },
    3: {
      label: "STAGE 3 · THERMAL GLASS SEPARATION",
      output: "Front glass sheet plus cell/EVA/backsheet laminate",
      note: "Hot-knife separation is the current design baseline. The Agastya station has not been validated.",
      steps: [
        ["The flat panel is guided into the station", "The initial build plan is for supported, flat crystalline-silicon panels after Stage 2. Guides keep the glass and laminate supported through the cut."],
        ["A heated blade follows the glass interface", "The thesis describes a heated blade near the glass/EVA boundary. The blade separates the front sheet; the exact temperature and speed still need supervised measurement."],
        ["Glass and laminate follow separate paths", "The glass sheet is collected separately. The remaining output still contains cells, EVA and backsheet; it is not EVA-free cell material."],
      ],
    },
    4: {
      label: "STAGE 4 · SILVER REMOVAL / ROUTE OPEN",
      output: "Silver-bearing product and residual stream; actual form depends on the selected route",
      note: "Stage 4 purpose is fixed; method, feed preparation, product form, facility and receiver criteria are unresolved.",
      steps: [
        ["Confirm the Stage 3 feed record", "Identify the actual cell-bearing material, its source, condition and measured mass. The hot-knife reference does not establish EVA-free cells or silver liberation."],
        ["Define the required product form", "Specify whether the project requires a silver-bearing solution, concentrate or recovered solid, and identify the intended qualified receiver."],
        ["Compare qualified routes against the real feed", "Use literature and facility capability to compare candidate methods, hazards, waste streams, costs and acceptance requirements. No route is selected in this walkthrough."],
        ["Plan measurement across every stage", "Use representative sampling, a matrix-validated assay, measured stream masses, uncertainty and mass balance to judge each future trial. No assay or recovery result is represented here."],
      ],
    },
  };

  let activeStage = 2;
  let activeStep = 0;
  let playTimer = null;
  const $ = (selector) => document.querySelector(selector);
  const tabs = [...document.querySelectorAll(".process-tab")];

  function stop() {
    if (playTimer) window.clearInterval(playTimer);
    playTimer = null;
    const play = $("#process-play");
    if (play) play.textContent = "▶ Play";
  }

  function render() {
    const stage = stageData[activeStage];
    const [title, copy] = stage.steps[activeStep];
    $("#process-stage-label").textContent = stage.label;
    $("#process-step-title").textContent = title;
    $("#process-step-copy").textContent = copy;
    $("#process-output").textContent = stage.output;
    $("#process-status-note span").textContent = stage.note;
    $("#process-step-count").textContent = `Step ${activeStep + 1} of ${stage.steps.length}`;
    $("#process-back").disabled = activeStep === 0;
    $("#process-next").disabled = activeStep === stage.steps.length - 1;
    tabs.forEach((tab) => {
      const selected = Number(tab.dataset.stage) === activeStage;
      tab.classList.toggle("active", selected);
      tab.setAttribute("aria-pressed", String(selected));
    });
    document.querySelectorAll(".process-diagram").forEach((diagram) => {
      const selected = Number(diagram.dataset.diagram) === activeStage;
      diagram.classList.toggle("active", selected);
      if (selected) diagram.dataset.step = String(activeStep + 1);
      else diagram.removeAttribute("data-step");
    });
  }

  tabs.forEach((tab) => tab.addEventListener("click", () => {
    stop();
    activeStage = Number(tab.dataset.stage);
    activeStep = 0;
    render();
  }));
  $("#process-back").addEventListener("click", () => { stop(); activeStep = Math.max(0, activeStep - 1); render(); });
  $("#process-next").addEventListener("click", () => { stop(); activeStep = Math.min(stageData[activeStage].steps.length - 1, activeStep + 1); render(); });
  $("#process-reset").addEventListener("click", () => { stop(); activeStep = 0; render(); });
  $("#process-play").addEventListener("click", () => {
    if (playTimer) { stop(); return; }
    if (activeStep === stageData[activeStage].steps.length - 1) activeStep = 0;
    render();
    $("#process-play").textContent = "Ⅱ Pause";
    playTimer = window.setInterval(() => {
      if (activeStep >= stageData[activeStage].steps.length - 1) { stop(); return; }
      activeStep += 1;
      render();
      $("#process-play").textContent = "Ⅱ Pause";
    }, 1900);
  });
  render();
})();
