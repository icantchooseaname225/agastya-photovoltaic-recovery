"""Conservative first-stage sorting rules for the Agastya recovery line."""

DISPOSITIONS = (
    "PENDING_REVIEW",
    "REUSE_CANDIDATE",
    "SERVICE_AND_RETEST",
    "ROUTED_TO_STAGE_2",
    "MANUALLY_INSPECTED",
    "ROUTE_TO_LICENSED_HANDLER",
    "REUSED",
    "REPAIRED",
)
SORT_ROUTES = (
    "HUMAN_REVIEW",
    "SAFETY_HOLD",
    "ELECTRICAL_TEST_REQUIRED",
    "SERVICE_AND_RETEST",
    "SECOND_LIFE_REVIEW",
    "STAGE_2_CSI",
    "LICENSED_THIN_FILM_HANDLER",
)
STRUCTURAL_DEFECTS = {"crack", "cracking", "broken", "burned"}
MAINTENANCE_CONDITIONS = {"dust", "snow", "bird_drop"}
PANEL_TECHNOLOGIES = ("unknown", "c_si", "thin_film", "other")
MIN_CONFIDENCE = 0.75
MIN_MARGIN = 0.12
OTHER_BROKEN_REVIEW_THRESHOLD = 0.50
SORT_DESTINATIONS = {
    "HUMAN_REVIEW": "MANUAL_REVIEW",
    "SAFETY_HOLD": "QUARANTINE",
    "ELECTRICAL_TEST_REQUIRED": "ELECTRICAL_TEST_STATION",
    "SERVICE_AND_RETEST": "SERVICE_RETEST_AREA",
    "SECOND_LIFE_REVIEW": "REUSE_ASSESSMENT",
    "STAGE_2_CSI": "STAGE_2_RECYCLING_INTAKE",
    "LICENSED_THIN_FILM_HANDLER": "LICENSED_HANDLER",
}


def sort_destination(route):
    """Map a triage route to a physical lane label; never issues a motor command."""
    return SORT_DESTINATIONS.get(route, "MANUAL_REVIEW")


def sort_lane_decision(route, panel_technology="unknown", electrical_test="not_tested",
                       stage2_isolation_confirmed=False, confirmed_visual_label=None):
    """Return a two-lane tabletop decision, defaulting to hold and never actuating hardware."""
    base = {
        "route": route or "HUMAN_REVIEW",
        "destination": sort_destination(route),
        "state": "DRY_RUN",
        "actuator_commanded": False,
    }
    if (route == "SECOND_LIFE_REVIEW" and panel_technology == "c_si"
            and electrical_test == "pass" and confirmed_visual_label not in STRUCTURAL_DEFECTS):
        return {
            **base,
            "lane": "LEFT",
            "decision": "REUSE_CANDIDATE",
            "label": "LEFT · REUSE CANDIDATE",
            "instruction": "Move to the left-side reuse-review area; this is not reuse approval.",
        }
    if route == "STAGE_2_CSI" and panel_technology == "c_si" and stage2_isolation_confirmed:
        return {
            **base,
            "lane": "RIGHT",
            "decision": "RECYCLE_CANDIDATE",
            "label": "RIGHT · STAGE 2 RECYCLING",
            "instruction": "Move to the right-side Stage 2 intake; operator and safety interlocks still govern handling.",
        }
    return {
        **base,
        "lane": "HOLD",
        "decision": "HUMAN_REVIEW",
        "label": "HOLD · MANUAL CHECK",
        "instruction": "Do not transfer yet. Resolve missing evidence, safety review, or the separate licensed-handler route.",
    }


def recommend_route(predictions, electrical_test="not_tested", panel_technology="unknown",
                    confirmed_visual_label=None):
    """Return an operational next-step route, not a recycling/reuse certification."""
    if electrical_test == "fail":
        return "SAFETY_HOLD", (
            "A documented electrical test failed. Hold for qualified safety review before any downstream handling."
        )

    if confirmed_visual_label in STRUCTURAL_DEFECTS:
        label = confirmed_visual_label.replace("_", " ")
        return "SAFETY_HOLD", f"Operator-confirmed {label}; hold for physical safety assessment before handling."

    if predictions:
        top = predictions[0]
        runner_up = float(predictions[1]["confidence"]) if len(predictions) > 1 else 0.0
        confidence = float(top["confidence"])
        if (top["label"] in STRUCTURAL_DEFECTS and confidence >= MIN_CONFIDENCE
                and confidence - runner_up >= MIN_MARGIN):
            label = top["label"].replace("_", " ")
            return "SAFETY_HOLD", f"Possible {label} requires a physical safety assessment before handling."

    other_confidence = max(
        (float(item.get("confidence", 0.0)) for item in (predictions or [])
         if item.get("label") == "other"),
        default=0.0,
    )

    if other_confidence > OTHER_BROKEN_REVIEW_THRESHOLD:
        return "SAFETY_HOLD", (
            f"Flag as potentially broken for review: the broad 'other' class is {other_confidence:.0%} (>50%). "
            "This is not a confirmed broken label; physically inspect the panel before choosing a process route."
        )

    if panel_technology == "thin_film":
        return "LICENSED_THIN_FILM_HANDLER", (
            "Keep thin-film modules intact and route to a licensed handler; do not send through the c-Si line."
        )

    if panel_technology != "c_si":
        return "HUMAN_REVIEW", "Confirm panel technology before selecting a downstream process."

    if confirmed_visual_label in MAINTENANCE_CONDITIONS:
        label = confirmed_visual_label.replace("_", " ")
        return "SERVICE_AND_RETEST", f"Operator-confirmed {label}; clean or service, then repeat visual and electrical checks."

    if confirmed_visual_label == "clean":
        if electrical_test == "pass":
            return "SECOND_LIFE_REVIEW", (
                "Operator-confirmed clean appearance and documented electrical test support second-life review; a human still approves reuse."
            )
        return "ELECTRICAL_TEST_REQUIRED", (
            "A clean image is not proof of output. Complete a qualified, documented electrical test before reuse review."
        )

    if not predictions:
        return "HUMAN_REVIEW", "No solar-trained visual model is available; inspect the panel manually."

    top = predictions[0]
    label = top["label"]
    confidence = float(top["confidence"])
    runner_up = float(predictions[1]["confidence"]) if len(predictions) > 1 else 0.0
    margin = confidence - runner_up
    if confidence < MIN_CONFIDENCE or margin < MIN_MARGIN:
        return "HUMAN_REVIEW", (
            f"Visual result is uncertain ({confidence:.0%} top confidence, {margin:.0%} margin); inspect manually."
        )

    if label in MAINTENANCE_CONDITIONS:
        return "SERVICE_AND_RETEST", (
            f"Possible {label.replace('_', ' ')}; clean or service, then repeat visual and electrical checks."
        )

    if label == "clean":
        if electrical_test == "pass":
            return "SECOND_LIFE_REVIEW", (
                "Visual and documented electrical checks support second-life review; a human still approves reuse."
            )
        return "ELECTRICAL_TEST_REQUIRED", (
            "A clean image is not proof of output. Complete a qualified, documented electrical test before reuse review."
        )

    return "HUMAN_REVIEW", "The available visual evidence is not specific enough to select a process route."


def recommend(predictions, electrical_test="not_tested", panel_technology="unknown",
              confirmed_visual_label=None):
    """Compatibility field for older clients; final disposition remains pending human review."""
    route, reason = recommend_route(
        predictions, electrical_test, panel_technology, confirmed_visual_label
    )
    if route == "LICENSED_THIN_FILM_HANDLER":
        return "ROUTE_TO_LICENSED_HANDLER", reason
    if route == "SECOND_LIFE_REVIEW":
        return "REUSE_CANDIDATE", reason
    if route in ("SERVICE_AND_RETEST", "STAGE_2_CSI"):
        return route, reason
    if route == "SAFETY_HOLD":
        return "PENDING_REVIEW", reason
    return "PENDING_REVIEW", reason
