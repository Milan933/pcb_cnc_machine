"""Review-only Phase 3 motion-layout skeleton.

This module adds nominal rail, carriage, screw, bearing-support, coupler,
motor, spindle, and bed envelopes to the accepted Architecture A skeleton.
The shapes are packaging references only: they are not supplier-specific
machining geometry, printed structural parts, or manufacturing exports.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cad.architecture import ArchitectureId
from cad.motion_phase3 import rail_class_lookup
from cad.parameters import PHASE2A_PARAMETERS, PHASE2_SKELETON_PARAMETERS, PHASE3_MOTION_PARAMETERS, Phase3MotionParameters

from .architecture_skeleton import (
    SkeletonComponent,
    SkeletonModel,
    _box,
    _build123d,
    _component,
    _reference_tube,
    build_skeleton,
)


def _nominal_box(
    build123d: Any,
    name: str,
    size: tuple[float, float, float],
    minimum: tuple[float, float, float],
    notes: str,
) -> SkeletonComponent:
    return _component(
        build123d,
        name,
        "motion-reference",
        _box(build123d, name, size, minimum),
        notes,
    )


def _nominal_axis_reference(
    build123d: Any,
    name: str,
    axis: str,
    length_mm: float,
    center: tuple[float, float, float],
    diameter_mm: float,
    notes: str,
) -> SkeletonComponent:
    return _component(
        build123d,
        name,
        "motion-reference",
        _reference_tube(build123d, name, axis, length_mm, center, diameter_mm),
        notes,
    )


def _reference_rail_profile(
    parameters: Phase3MotionParameters,
    rail_class: str,
) -> tuple[float, float]:
    """Return the nominal rail width and top-height reference."""

    for class_name, envelope in parameters.rail_reference_envelopes_mm:
        if class_name == rail_class:
            return envelope
    raise KeyError(f"No rail reference envelope for {rail_class}")


def _axis_support_envelope(
    parameters: Phase3MotionParameters,
    axis_name: str,
) -> tuple[float, float, float]:
    for name, envelope in parameters.reference_bearing_support_envelopes_mm:
        if name == axis_name:
            return envelope
    raise KeyError(f"No bearing support envelope for {axis_name}")


def _axis_coupler_envelope(
    parameters: Phase3MotionParameters,
    axis_name: str,
) -> tuple[float, float, float]:
    for name, envelope in parameters.reference_coupler_envelopes_mm:
        if name == axis_name:
            return envelope
    raise KeyError(f"No coupler envelope for {axis_name}")


def _x_motion_components(
    build123d: Any,
    parameters: Phase3MotionParameters,
) -> list[SkeletonComponent]:
    axis = next(item for item in parameters.axes if item.axis == "X")
    rail = rail_class_lookup(axis.rail_class, parameters.rail_classes)
    rail_width, rail_height = _reference_rail_profile(parameters, axis.rail_class)
    rail_y = parameters.x_rail_center_y_mm
    rail_z_center = parameters.x_rail_center_z_mm
    support_size = _axis_support_envelope(parameters, "X")
    coupler_size = _axis_coupler_envelope(parameters, "X")
    motor_size = parameters.reference_motor_envelope_mm
    nut_size = parameters.reference_nut_envelope_mm
    parts: list[SkeletonComponent] = []
    for index, z in enumerate(
        (
            rail_z_center - axis.rail_center_spacing_mm / 2.0,
            rail_z_center + axis.rail_center_spacing_mm / 2.0,
        ),
        start=1,
    ):
        parts.append(
            _nominal_box(
                build123d,
                f"x_rail_{index}",
                (axis.rail_length_mm, rail_width, rail_height),
                (-axis.rail_length_mm / 2.0, rail_y - rail_width / 2.0, z - rail_height / 2.0),
                "MGN12 rail envelope; exact profile, preload, end cut, and seat are vendor and measurement dependent.",
            )
        )
        parts.append(
            _nominal_box(
                build123d,
                f"x_carriage_{index * 2 - 1}",
                (rail.block_length_mm, rail.assembly_width_mm, rail.assembly_height_mm),
                (-rail.block_length_mm / 2.0, rail_y - rail.assembly_width_mm / 2.0, z - rail.assembly_height_mm / 2.0),
                "Long-block MGN12H carriage envelope at the nominal X mid-position.",
            )
        )
        parts.append(
            _nominal_box(
                build123d,
                f"x_carriage_{index * 2}",
                (rail.block_length_mm, rail.assembly_width_mm, rail.assembly_height_mm),
                (rail.block_length_mm / 2.0, rail_y - rail.assembly_width_mm / 2.0, z - rail.assembly_height_mm / 2.0),
                "Second X carriage envelope; the moving Z plate must bridge both rails.",
            )
        )
    screw_center = (0.0, rail_y - rail.assembly_width_mm / 2.0 - parameters.reference_screw_diameter_mm, rail_z_center)
    fixed_min_x = -axis.screw_length_mm / 2.0 - support_size[0]
    floating_min_x = axis.screw_length_mm / 2.0
    fixed_min_y = screw_center[1] - support_size[1] / 2.0
    fixed_min_z = screw_center[2] - support_size[2] / 2.0
    motor_min_x = fixed_min_x - parameters.reference_motor_clearance_mm - motor_size[0]
    parts.extend(
        (
            _nominal_axis_reference(
                build123d,
                "x_screw",
                "x",
                axis.screw_length_mm,
                screw_center,
                parameters.reference_screw_diameter_mm,
                "T8x4 screw envelope; reference diameter and end support span only.",
            ),
            _nominal_box(
                build123d,
                "x_nut",
                nut_size,
                tuple(value - size / 2.0 for value, size in zip(screw_center, nut_size)),
                "Adjustable anti-backlash nut envelope; split/spring construction is not modeled.",
            ),
            _nominal_box(
                build123d,
                "x_fixed_bearing_support",
                support_size,
                (fixed_min_x, fixed_min_y, fixed_min_z),
                "Fixed-end 8 mm axial bearing support envelope at the motor side.",
            ),
            _nominal_box(
                build123d,
                "x_floating_bearing_support",
                support_size,
                (floating_min_x, fixed_min_y, fixed_min_z),
                "Floating 8 mm radial bearing support envelope; axial float is required.",
            ),
            _nominal_box(
                build123d,
                "x_coupler",
                coupler_size,
                (-axis.screw_length_mm / 2.0, screw_center[1] - coupler_size[1] / 2.0, screw_center[2] - coupler_size[2] / 2.0),
                "Flexible 5-to-8 mm coupler envelope; it carries torque only.",
            ),
            _nominal_box(
                build123d,
                "x_nema17",
                motor_size,
                (motor_min_x, screw_center[1] - motor_size[1] / 2.0, screw_center[2] - motor_size[2] / 2.0),
                "40-48 mm NEMA17 body envelope; owned motor identity remains unresolved.",
            ),
        )
    )
    return parts


def _y_motion_components(
    build123d: Any,
    parameters: Phase3MotionParameters,
) -> list[SkeletonComponent]:
    axis = next(item for item in parameters.axes if item.axis == "Y")
    rail = rail_class_lookup(axis.rail_class, parameters.rail_classes)
    rail_width, rail_height = _reference_rail_profile(parameters, axis.rail_class)
    rail_z = parameters.y_rail_center_z_mm
    support_size = _axis_support_envelope(parameters, "Y")
    coupler_size = _axis_coupler_envelope(parameters, "Y")
    motor_size = parameters.reference_motor_envelope_mm
    motor_axis_size = (motor_size[0], motor_size[2], motor_size[1])
    nut_size = parameters.reference_nut_envelope_mm
    parts: list[SkeletonComponent] = []
    for index, x in enumerate(
        (-axis.rail_center_spacing_mm / 2.0, axis.rail_center_spacing_mm / 2.0),
        start=1,
    ):
        parts.append(
            _nominal_box(
                build123d,
                f"y_rail_{index}",
                (rail_width, axis.rail_length_mm, rail_height),
                (x - rail_width / 2.0, -axis.rail_length_mm / 2.0, rail_z - rail_height / 2.0),
                "MGN12 rail envelope under the moving bed; exact seat and preload remain open.",
            )
        )
        for carriage_index, y in enumerate(parameters.y_carriage_center_offsets_mm, start=1):
            parts.append(
                _nominal_box(
                    build123d,
                    f"y_carriage_{(index - 1) * 2 + carriage_index}",
                    (rail.assembly_width_mm, rail.block_length_mm, rail.assembly_height_mm),
                    (x - rail.assembly_width_mm / 2.0, y - rail.block_length_mm / 2.0, rail_z - rail.assembly_height_mm / 2.0),
                    "Long-block MGN12H carriage envelope; two carriages per rail spread bed pitch loads.",
                )
            )
    screw_center = (0.0, 0.0, rail_z - parameters.reference_screw_diameter_mm - rail_height)
    fixed_min_y = -axis.screw_length_mm / 2.0 - parameters.reference_end_clearance_mm - support_size[1]
    floating_min_y = axis.screw_length_mm / 2.0 + parameters.reference_end_clearance_mm
    fixed_min_x = screw_center[0] - support_size[0] / 2.0
    fixed_min_z = screw_center[2] - support_size[2] / 2.0
    motor_min_y = fixed_min_y - parameters.reference_motor_clearance_mm - motor_size[1]
    parts.extend(
        (
            _nominal_axis_reference(
                build123d,
                "y_screw",
                "y",
                axis.screw_length_mm,
                screw_center,
                parameters.reference_screw_diameter_mm,
                "T8x4 centered Y screw envelope; a second screw is not the baseline.",
            ),
            _nominal_box(
                build123d,
                "y_nut",
                nut_size,
                tuple(value - size / 2.0 for value, size in zip(screw_center, nut_size)),
                "Adjustable anti-backlash Y nut envelope below the bed centerline.",
            ),
            _nominal_box(
                build123d,
                "y_fixed_bearing_support",
                support_size,
                (fixed_min_x, fixed_min_y, fixed_min_z),
                "Fixed-end 8 mm axial bearing support at the front/motor end.",
            ),
            _nominal_box(
                build123d,
                "y_floating_bearing_support",
                support_size,
                (fixed_min_x, floating_min_y, fixed_min_z),
                "Floating rear radial support with axial float.",
            ),
            _nominal_box(
                build123d,
                "y_coupler",
                coupler_size,
                (screw_center[0] - coupler_size[0] / 2.0, -axis.screw_length_mm / 2.0 - coupler_size[1] / 2.0, screw_center[2] - coupler_size[2] / 2.0),
                "Flexible 5-to-8 mm coupler envelope; no axial bearing function.",
            ),
            _nominal_box(
                build123d,
                "y_nema17",
                motor_axis_size,
                (-motor_axis_size[0] / 2.0, motor_min_y, screw_center[2] - motor_axis_size[2] / 2.0),
                "40-48 mm NEMA17 body envelope for the moving-bed axis.",
            ),
            _nominal_box(
                build123d,
                "phase3_moving_bed_support_envelope",
                parameters.moving_bed_support_mm,
                (
                    -parameters.moving_bed_support_mm[0] / 2.0,
                    -parameters.moving_bed_support_mm[1] / 2.0,
                    -parameters.moving_bed_support_mm[2],
                ),
                "240 x 190 x 8 mm moving support envelope; PCB and clamp margin are retained.",
            ),
        )
    )
    return parts


def _z_motion_components(
    build123d: Any,
    parameters: Phase3MotionParameters,
) -> list[SkeletonComponent]:
    axis = next(item for item in parameters.axes if item.axis == "Z")
    rail = rail_class_lookup(axis.rail_class, parameters.rail_classes)
    rail_width, rail_height = _reference_rail_profile(parameters, axis.rail_class)
    z_center = parameters.x_rail_center_z_mm
    rail_y = parameters.z_rail_center_y_mm
    support_size = _axis_support_envelope(parameters, "Z")
    coupler_size = _axis_coupler_envelope(parameters, "Z")
    motor_size = parameters.reference_motor_envelope_mm
    nut_size = parameters.reference_nut_envelope_mm
    lower_support_size = parameters.reference_lower_bearing_support_envelope_mm
    parts: list[SkeletonComponent] = []
    for index, x in enumerate(
        (-axis.rail_center_spacing_mm / 2.0, axis.rail_center_spacing_mm / 2.0),
        start=1,
    ):
        parts.append(
            _nominal_box(
                build123d,
                f"z_rail_{index}",
                (rail_height, rail_width, axis.rail_length_mm),
                (x - rail_height / 2.0, rail_y - rail_width / 2.0, parameters.z_rail_base_z_mm),
                "MGN9H short Z rail envelope; MGN12 is the stiffness fallback if coupon evidence requires it.",
            )
        )
        for carriage_index, z in enumerate((z_center - 20.0, z_center + 20.0), start=1):
            parts.append(
                _nominal_box(
                    build123d,
                    f"z_carriage_{(index - 1) * 2 + carriage_index}",
                    (rail.assembly_width_mm, rail.assembly_width_mm, rail.block_length_mm),
                    (x - rail.assembly_width_mm / 2.0, rail_y - rail.assembly_width_mm / 2.0, z - rail.block_length_mm / 2.0),
                    "MGN9H carriage envelope; four blocks establish a separated short-Z guide plane.",
                )
            )
    screw_center = (0.0, rail_y + parameters.z_screw_center_offset_y_mm, z_center)
    fixed_min_z = z_center + axis.screw_length_mm / 2.0 - support_size[2] / 2.0
    floating_min_z = z_center - axis.screw_length_mm / 2.0 - parameters.reference_lower_support_overlap_mm
    fixed_min_x = screw_center[0] - support_size[0] / 2.0
    fixed_min_y = screw_center[1] - support_size[1] / 2.0
    motor_min_z = fixed_min_z + support_size[2] + parameters.reference_motor_clearance_mm
    parts.extend(
        (
            _nominal_axis_reference(
                build123d,
                "z_screw",
                "z",
                axis.screw_length_mm,
                screw_center,
                parameters.reference_screw_diameter_mm,
                "T8x2 centered Z screw envelope; the lower bearing remains radially floating.",
            ),
            _nominal_box(
                build123d,
                "z_nut",
                nut_size,
                tuple(value - size / 2.0 for value, size in zip(screw_center, nut_size)),
                "Preloaded Z nut envelope; gravity-hold and drag tests are required.",
            ),
            _nominal_box(
                build123d,
                "z_fixed_bearing_support",
                support_size,
                (fixed_min_x, fixed_min_y, fixed_min_z),
                "Upper fixed Z support carrying axial load through the bearing pair.",
            ),
            _nominal_box(
                build123d,
                "z_floating_bearing_support",
                lower_support_size,
                (
                    -lower_support_size[0] / 2.0,
                    screw_center[1] - lower_support_size[1] / 2.0,
                    floating_min_z,
                ),
                "Lower radial-only support; thermal growth must not be over-constrained.",
            ),
            _nominal_box(
                build123d,
                "z_coupler",
                coupler_size,
                (
                    screw_center[0] - coupler_size[0] / 2.0,
                    screw_center[1] - coupler_size[1] / 2.0,
                    fixed_min_z - coupler_size[2] + support_size[2] - parameters.reference_motor_clearance_mm,
                ),
                "Flexible 5-to-8 mm coupler envelope above the fixed bearing.",
            ),
            _nominal_box(
                build123d,
                "z_nema17",
                motor_size,
                (-motor_size[0] / 2.0, screw_center[1] - motor_size[1] / 2.0, motor_min_z),
                "40-48 mm NEMA17 body envelope at the upper Z motor end.",
            ),
            _nominal_box(
                build123d,
                "phase3_spindle_mount_envelope",
                parameters.spindle_mount_envelope_mm,
                (
                    -parameters.spindle_mount_envelope_mm[0] / 2.0,
                    rail_y - parameters.spindle_mount_envelope_mm[1] / 2.0,
                    parameters.spindle_mount_min_z_mm,
                ),
                "Generic spindle clamp/mount envelope; diameter, runout, mass, and thermal interface remain unresolved.",
            ),
        )
    )
    return parts


def build_motion_skeleton(
    parameters: Phase3MotionParameters = PHASE3_MOTION_PARAMETERS,
) -> SkeletonModel:
    """Build Architecture A plus nominal Phase 3 motion reference envelopes."""

    build123d = _build123d()
    base = build_skeleton(
        ArchitectureId.A,
        PHASE2_SKELETON_PARAMETERS,
        structural_variant="phase2a",
        phase2a_parameters=PHASE2A_PARAMETERS,
    )
    components = list(base.components)
    components.extend(_x_motion_components(build123d, parameters))
    components.extend(_y_motion_components(build123d, parameters))
    components.extend(_z_motion_components(build123d, parameters))
    return SkeletonModel(
        candidate_id=ArchitectureId.A,
        components=tuple(components),
        expected_interference_pairs=base.expected_interference_pairs,
        variant="phase3-motion",
    )


def export_motion_skeleton(model: SkeletonModel, output_dir: Path) -> dict[str, Path]:
    """Export review-only Phase 3 derivatives outside the repository."""

    build123d = _build123d()
    output_dir.mkdir(parents=True, exist_ok=True)
    step_path = output_dir / "phase3-a-motion-skeleton.step"
    stl_path = output_dir / "phase3-a-motion-skeleton.stl"
    build123d.export_step(model.compound, step_path)
    build123d.export_stl(
        model.compound,
        stl_path,
        tolerance=0.01,
        angular_tolerance=0.2,
    )
    return {"step": step_path, "stl": stl_path}
