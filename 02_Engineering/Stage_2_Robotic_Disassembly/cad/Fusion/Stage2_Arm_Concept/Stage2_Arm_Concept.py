"""Create a non-fabrication AGASTYA Stage 2 arm envelope in Autodesk Fusion.

Run only inside Autodesk Fusion's Scripts and Add-Ins dialog. The generated
model is an assembled, neutral-pose geometry study; it has no joints, motor
mount details, structural sizing, tool model, safety design, or validated
motion. Exported F3D and STEP files are written beside this script in exports/.
"""

import os
import traceback

import adsk.core
import adsk.fusion


# Illustrative design inputs only; edit these constants after measuring the
# accepted module and reviewing real tool/force data. Fusion internal length
# units are centimetres.
MM = 0.1
BASE_PLATE_X_MM = 350.0
BASE_PLATE_Y_MM = 350.0
BASE_PLATE_T_MM = 20.0
PEDESTAL_X_MM = 160.0
PEDESTAL_Y_MM = 160.0
PEDESTAL_H_MM = 650.0
TURNTABLE_D_MM = 250.0
TURNTABLE_T_MM = 60.0
SHOULDER_Z_MM = BASE_PLATE_T_MM + PEDESTAL_H_MM + TURNTABLE_T_MM
LINK1_MM = 1100.0
LINK1_Y_MM = 120.0
LINK1_Z_MM = 100.0
LINK2_MM = 900.0
LINK2_Y_MM = 100.0
LINK2_Z_MM = 80.0
JOINT_D_MM = 230.0
JOINT_T_MM = 100.0
TOOL_FLANGE_X_MM = 120.0
TOOL_FLANGE_Y_MM = 100.0
TOOL_FLANGE_Z_MM = 16.0


def cm(value_mm):
    return value_mm * MM


def point(x_mm, y_mm, z_mm):
    return adsk.core.Point3D.create(cm(x_mm), cm(y_mm), cm(z_mm))


def translation(x_mm=0.0, y_mm=0.0, z_mm=0.0):
    matrix = adsk.core.Matrix3D.create()
    matrix.setToTranslation(adsk.core.Vector3D.create(
        cm(x_mm), cm(y_mm), cm(z_mm)
    ))
    return matrix


def component(root, name, x_mm=0.0, y_mm=0.0, z_mm=0.0):
    occurrence = root.occurrences.addNewComponent(
        translation(x_mm, y_mm, z_mm)
    )
    if not occurrence:
        raise RuntimeError("Fusion could not create component: " + name)
    occurrence.component.name = name
    return occurrence.component


def extrude_profile(comp, sketch, distance_mm, label):
    if sketch.profiles.count < 1:
        raise RuntimeError("No closed profile for " + label)
    profile = sketch.profiles.item(0)
    extrudes = comp.features.extrudeFeatures
    feature_input = extrudes.createInput(
        profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    feature_input.setDistanceExtent(
        False, adsk.core.ValueInput.createByReal(cm(distance_mm))
    )
    feature = extrudes.add(feature_input)
    feature.name = label
    return feature


def rectangle_prism(comp, plane, width_mm, height_mm, length_mm, label):
    sketch = comp.sketches.add(plane)
    sketch.name = label + " profile"
    curves = sketch.sketchCurves.sketchLines
    half_w = cm(width_mm) / 2.0
    half_h = cm(height_mm) / 2.0
    curves.addTwoPointRectangle(
        adsk.core.Point3D.create(-half_w, -half_h, 0),
        adsk.core.Point3D.create(half_w, half_h, 0),
    )
    return extrude_profile(comp, sketch, length_mm, label)


def cylinder(comp, plane, diameter_mm, length_mm, label):
    sketch = comp.sketches.add(plane)
    sketch.name = label + " profile"
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), cm(diameter_mm) / 2.0
    )
    return extrude_profile(comp, sketch, length_mm, label)


def create_design(app):
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        raise RuntimeError("Could not access the new Fusion design")
    root = design.rootComponent

    # Floor plate and pedestal envelope.
    base = component(root, "BASE-01 floor plate", 0, 0, 0)
    rectangle_prism(
        base, base.xYConstructionPlane,
        BASE_PLATE_X_MM, BASE_PLATE_Y_MM, BASE_PLATE_T_MM,
        "350 x 350 x 20 envelope",
    )

    pedestal = component(root, "PEDESTAL-01", 0, 0, BASE_PLATE_T_MM)
    rectangle_prism(
        pedestal, pedestal.xYConstructionPlane,
        PEDESTAL_X_MM, PEDESTAL_Y_MM, PEDESTAL_H_MM,
        "160 x 160 x 650 envelope",
    )

    turntable = component(
        root, "J1 base yaw envelope", 0, 0,
        BASE_PLATE_T_MM + PEDESTAL_H_MM,
    )
    cylinder(
        turntable, turntable.xYConstructionPlane,
        TURNTABLE_D_MM, TURNTABLE_T_MM, "base yaw housing envelope",
    )

    # A four-axis articulated layout: base yaw, shoulder pitch, elbow pitch,
    # and wrist/tool pitch. Cylinders are simple keep-out envelopes, not motors.
    shoulder = component(root, "J2 shoulder housing envelope", 0, 0, SHOULDER_Z_MM)
    cylinder(
        shoulder, shoulder.xZConstructionPlane,
        JOINT_D_MM, JOINT_T_MM, "shoulder joint envelope",
    )

    link1 = component(root, "LINK-01 upper arm envelope", 0, 0, SHOULDER_Z_MM)
    rectangle_prism(
        link1, link1.yZConstructionPlane,
        LINK1_Y_MM, LINK1_Z_MM, LINK1_MM,
        "1100 long upper-arm envelope",
    )

    elbow = component(root, "J3 elbow housing envelope", LINK1_MM, 0, SHOULDER_Z_MM)
    cylinder(
        elbow, elbow.xZConstructionPlane,
        JOINT_D_MM * 0.78, JOINT_T_MM, "elbow joint envelope",
    )

    link2 = component(root, "LINK-02 forearm envelope", LINK1_MM, 0, SHOULDER_Z_MM)
    rectangle_prism(
        link2, link2.yZConstructionPlane,
        LINK2_Y_MM, LINK2_Z_MM, LINK2_MM,
        "900 long forearm envelope",
    )

    wrist_x = LINK1_MM + LINK2_MM
    wrist = component(root, "J4 wrist housing envelope", wrist_x, 0, SHOULDER_Z_MM)
    cylinder(
        wrist, wrist.xZConstructionPlane,
        JOINT_D_MM * 0.58, JOINT_T_MM * 0.8, "wrist joint envelope",
    )

    flange = component(root, "TOOL-00 unselected interface envelope", wrist_x + 60, 0, SHOULDER_Z_MM)
    rectangle_prism(
        flange, flange.yZConstructionPlane,
        TOOL_FLANGE_Y_MM, TOOL_FLANGE_Z_MM, TOOL_FLANGE_X_MM,
        "tool adapter placeholder",
    )

    return doc, design


def export_design(design):
    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "exports")
    os.makedirs(output_dir, exist_ok=True)
    export_manager = design.exportManager
    root = design.rootComponent
    f3d_path = os.path.join(output_dir, "AGASTYA_Stage2_Arm_Concept.f3d")
    step_path = os.path.join(output_dir, "AGASTYA_Stage2_Arm_Concept.step")
    f3d_options = export_manager.createFusionArchiveExportOptions(f3d_path, root)
    step_options = export_manager.createSTEPExportOptions(step_path, root)
    if not f3d_options or not step_options:
        raise RuntimeError("Fusion could not create F3D/STEP export options")
    if not export_manager.execute(f3d_options):
        raise RuntimeError("Fusion F3D export failed")
    if not export_manager.execute(step_options):
        raise RuntimeError("Fusion STEP export failed")
    return f3d_path, step_path


def run(_context):
    app = adsk.core.Application.get()
    ui = app.userInterface if app else None
    try:
        _doc, design = create_design(app)
        f3d_path, step_path = export_design(design)
        ui.messageBox(
            "Concept geometry exported. These are non-fabrication envelopes.\n\n"
            "F3D: " + f3d_path + "\nSTEP: " + step_path
        )
    except Exception:
        if ui:
            ui.messageBox("Fusion concept script stopped:\n" + traceback.format_exc())


def stop(_context):
    """Required Fusion script entry point; this script does not persist UI."""
    return
