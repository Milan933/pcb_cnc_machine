"""Review-only Phase 3A compact packaging skeletons.

The model contains outer structural bounds and nominal component envelopes
only.  It is deliberately separate from the Phase 3 motion skeleton because
the Phase 3A variants are a packaging study, not a silent rewrite of the
owner-review motion baseline or a production structural model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cad.architecture import ArchitectureId
from cad.motion_phase3 import rail_class_lookup
from cad.packaging_phase3a import phase3a_variant_by_id
from cad.parameters import (
    PHASE2_SKELETON_PARAMETERS,
    PHASE3A_PACKAGING_VARIANTS,
    PHASE3_MOTION_PARAMETERS,
    Phase3APackagingVariant,
)

from .architecture_skeleton import (
    SkeletonComponent,
    SkeletonModel,
    _box,
    _build123d,
    _cylinder,
    _component,
    _reference_tube,
    unexpected_interferences,
)


def _centered_box(
    build123d: Any,
    name: str,
    size: tuple[float, float, float],
    center: tuple[float, float, float],
    notes: str,
) -> SkeletonComponent:
    return _component(
        build123d,
        name,
        "motion-reference",
        _box(
            build123d,
            name,
            size,
            tuple(coordinate - extent / 2.0 for coordinate, extent in zip(center, size)),
        ),
        notes,
    )


def _named_box(
    build123d: Any,
    name: str,
    size: tuple[float, float, float],
    minimum: tuple[float, float, float],
    category: str,
    notes: str,
) -> SkeletonComponent:
    return _component(build123d, name, category, _box(build123d, name, size, minimum), notes)


def _reference_axis(
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


def _envelope(
    envelopes: tuple[tuple[str, tuple[float, float, float]], ...],
    axis: str,
) -> tuple[float, float, float]:
    for name, size in envelopes:
        if name == axis:
            return size
    raise KeyError(f"No Phase 3A bearing envelope for {axis}")


def _structural_packaging_bound(
    build123d: Any,
    variant: Phase3APackagingVariant,
) -> SkeletonComponent:
    """Make one compound structural bound to keep collision semantics small."""

    body_x, body_y, body_z = variant.body_envelope_mm
    body = _box(
        build123d,
        "phase3a_body_packaging_bound",
        (body_x, body_y, body_z),
        (-body_x / 2.0, -body_y / 2.0, variant.body_min_z_mm),
    )
    outer = variant.gantry_outer_width_mm
    side = variant.gantry_side_width_mm
    clear = outer - 2.0 * side
    beam = _box(
        build123d,
        "phase3a_fixed_gantry_crossbeam_bound",
        (clear, variant.gantry_depth_mm, variant.gantry_height_mm),
        (-clear / 2.0, -variant.gantry_depth_mm / 2.0, variant.gantry_bottom_z_mm),
    )
    left = _box(
        build123d,
        "phase3a_fixed_gantry_left_bound",
        (side, variant.gantry_depth_mm, variant.gantry_bottom_z_mm - variant.body_min_z_mm),
        (-outer / 2.0, -variant.gantry_depth_mm / 2.0, variant.body_min_z_mm),
    )
    right = _box(
        build123d,
        "phase3a_fixed_gantry_right_bound",
        (side, variant.gantry_depth_mm, variant.gantry_bottom_z_mm - variant.body_min_z_mm),
        (outer / 2.0 - side, -variant.gantry_depth_mm / 2.0, variant.body_min_z_mm),
    )
    structural = build123d.Compound(children=[body, left, right, beam])
    structural.label = "phase3a_fixed_gantry_packaging_bound"
    return _component(
        build123d,
        "phase3a_fixed_gantry_packaging_bound",
        "structural",
        structural,
        "Outer fixed-gantry/moving-bed packaging bound only; wall, rib, fastener, "
        "rail-seat, and print-orientation geometry are intentionally absent.",
    )


def _x_components(
    build123d: Any,
    variant: Phase3APackagingVariant,
) -> list[SkeletonComponent]:
    axis = next(item for item in PHASE3_MOTION_PARAMETERS.axes if item.axis == "X")
    rail = rail_class_lookup(axis.rail_class)
    rail_width, rail_height = next(
        envelope for name, envelope in PHASE3_MOTION_PARAMETERS.rail_reference_envelopes_mm if name == axis.rail_class
    )
    length = variant.rail_lengths_mm[0]
    rail_y = variant.x_rail_center_y_mm
    rail_z = variant.x_rail_center_z_mm
    screw_y = rail_y - rail_width / 2.0 - PHASE3_MOTION_PARAMETERS.reference_screw_diameter_mm
    support = _envelope(variant.bearing_fixed_envelopes_mm, "X")
    floating = _envelope(variant.bearing_floating_envelopes_mm, "X")
    coupler = next(
        envelope for name, envelope in PHASE3_MOTION_PARAMETERS.reference_coupler_envelopes_mm if name == "X"
    )
    motor_cross = PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm[0]
    motor_axis = PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm[2]
    parts: list[SkeletonComponent] = []
    for rail_index, rail_z_offset in enumerate((-axis.rail_center_spacing_mm / 2.0, axis.rail_center_spacing_mm / 2.0), start=1):
        z = rail_z + rail_z_offset
        parts.append(
            _named_box(
                build123d,
                f"phase3a_x_rail_{rail_index}",
                (length, rail_width, rail_height),
                (-length / 2.0, rail_y - rail_width / 2.0, z - rail_height / 2.0),
                "motion-reference",
                "MGN12H nominal rail envelope; the length includes the swept two-block group and declared end margins.",
            )
        )
        for carriage_index, offset in enumerate(variant.x_carriage_center_offsets_mm, start=1):
            parts.append(
                _centered_box(
                    build123d,
                    f"phase3a_x_carriage_{(rail_index - 1) * 2 + carriage_index}",
                    (rail.block_length_mm, rail.assembly_width_mm, rail.assembly_height_mm),
                    (offset, rail_y, z),
                    "Two MGN12H blocks per rail; the swept group is validated separately from this mid-position view.",
                )
            )
    screw_center = (0.0, screw_y, rail_z)
    fixed_center = (-length / 2.0, screw_y, rail_z)
    floating_center = (length / 2.0, screw_y, rail_z)
    parts.extend(
        (
            _reference_axis(
                build123d,
                "phase3a_x_screw",
                "x",
                variant.screw_lengths_mm[0],
                screw_center,
                PHASE3_MOTION_PARAMETERS.reference_screw_diameter_mm,
                "T8x4 screw envelope; unsupported length is screened separately and fixed/floating ends remain required.",
            ),
            _centered_box(
                build123d,
                "phase3a_x_nut",
                PHASE3_MOTION_PARAMETERS.reference_nut_envelope_mm,
                screw_center,
                "Replaceable preloaded X nut envelope; split/spring construction is not modeled.",
            ),
            _centered_box(build123d, "phase3a_x_fixed_bearing", support, fixed_center, "Fixed X axial bearing cartridge envelope."),
            _centered_box(build123d, "phase3a_x_floating_bearing", floating, floating_center, "Floating X radial bearing cartridge envelope; axial float is required."),
            _centered_box(
                build123d,
                "phase3a_x_coupler",
                coupler,
                (-length / 2.0, screw_y, rail_z),
                "Flexible direct 5-to-8 mm coupler envelope; it carries torque only.",
            ),
            _named_box(
                build123d,
                "phase3a_x_nema17",
                (motor_axis, motor_cross, motor_cross),
                (-length / 2.0 - variant.x_motor_recess_mm, screw_y - motor_cross / 2.0, rail_z - motor_cross / 2.0),
                "motion-reference",
                "Direct axial owner-supplied generic NEMA17 interface recessed into the side structure; rear connector/wiring and cover access remain to be proven.",
            ),
        )
    )
    return parts


def _y_components(
    build123d: Any,
    variant: Phase3APackagingVariant,
) -> list[SkeletonComponent]:
    axis = next(item for item in PHASE3_MOTION_PARAMETERS.axes if item.axis == "Y")
    rail = rail_class_lookup(axis.rail_class)
    rail_width, rail_height = next(
        envelope for name, envelope in PHASE3_MOTION_PARAMETERS.rail_reference_envelopes_mm if name == axis.rail_class
    )
    length = variant.rail_lengths_mm[1]
    rail_z = variant.y_rail_center_z_mm
    screw_z = rail_z - rail_height - PHASE3_MOTION_PARAMETERS.reference_screw_diameter_mm
    support = _envelope(variant.bearing_fixed_envelopes_mm, "Y")
    floating = _envelope(variant.bearing_floating_envelopes_mm, "Y")
    coupler = next(
        envelope for name, envelope in PHASE3_MOTION_PARAMETERS.reference_coupler_envelopes_mm if name == "Y"
    )
    motor_cross = PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm[0]
    motor_axis = PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm[2]
    parts: list[SkeletonComponent] = []
    for rail_index, x in enumerate((-axis.rail_center_spacing_mm / 2.0, axis.rail_center_spacing_mm / 2.0), start=1):
        parts.append(
            _named_box(
                build123d,
                f"phase3a_y_rail_{rail_index}",
                (rail_width, length, rail_height),
                (x - rail_width / 2.0, -length / 2.0, rail_z - rail_height / 2.0),
                "motion-reference",
                "MGN12H nominal moving-bed rail envelope; transverse spacing remains 220 mm.",
            )
        )
        for carriage_index, offset in enumerate(variant.y_carriage_center_offsets_mm, start=1):
            parts.append(
                _centered_box(
                    build123d,
                    f"phase3a_y_carriage_{(rail_index - 1) * 2 + carriage_index}",
                    (rail.assembly_width_mm, rail.block_length_mm, rail.assembly_height_mm),
                    (x, offset, rail_z),
                    "Two MGN12H blocks per rail; bed overhang is allowed and reported by the packaging study.",
                )
            )
    screw_center = (0.0, 0.0, screw_z)
    fixed_center = (0.0, -length / 2.0, screw_z)
    floating_center = (0.0, length / 2.0, screw_z)
    motor_min_y = -length / 2.0 - variant.y_motor_protrusion_mm
    parts.extend(
        (
            _reference_axis(
                build123d,
                "phase3a_y_screw",
                "y",
                variant.screw_lengths_mm[1],
                screw_center,
                PHASE3_MOTION_PARAMETERS.reference_screw_diameter_mm,
                "T8x4 screw envelope below the moving bed; the centered single screw is retained.",
            ),
            _centered_box(
                build123d,
                "phase3a_y_nut",
                PHASE3_MOTION_PARAMETERS.reference_nut_envelope_mm,
                screw_center,
                "Replaceable preloaded Y nut envelope below the bed datum.",
            ),
            _centered_box(build123d, "phase3a_y_fixed_bearing", support, fixed_center, "Fixed Y axial bearing cartridge envelope at the front end."),
            _centered_box(build123d, "phase3a_y_floating_bearing", floating, floating_center, "Floating Y radial bearing cartridge envelope at the rear end."),
            _centered_box(
                build123d,
                "phase3a_y_coupler",
                coupler,
                fixed_center,
                "Flexible direct 5-to-8 mm coupler envelope; it is not an axial support.",
            ),
            _named_box(
                build123d,
                "phase3a_y_nema17",
                (motor_cross, motor_axis, motor_cross),
                (-motor_cross / 2.0, motor_min_y, variant.y_motor_center_z_mm - motor_cross / 2.0),
                "motion-reference",
                "Direct axial owner-supplied generic NEMA17 interface partly recessed into the front cross-member; rear connector/wiring and front service cover are required.",
            ),
            _named_box(
                build123d,
                "phase3a_moving_bed_support",
                variant.bed_support_mm,
                (-variant.bed_support_mm[0] / 2.0, -variant.bed_support_mm[1] / 2.0, -variant.bed_support_mm[2]),
                "motion-reference",
                "Moving-bed support envelope; PCB remains 200 x 150 mm and the guide carriages do not need full bed coverage.",
            ),
            _named_box(
                build123d,
                "phase3a_spoilboard",
                variant.spoilboard_mm,
                (-variant.spoilboard_mm[0] / 2.0, -variant.spoilboard_mm[1] / 2.0, -variant.spoilboard_mm[2]),
                "motion-reference",
                "Replaceable spoilboard envelope; thickness and clamping details remain open.",
            ),
            _named_box(
                build123d,
                "phase3a_swept_bed_envelope",
                (
                    variant.bed_support_mm[0],
                    variant.bed_support_mm[1] + variant.tool_travel_mm[1],
                    variant.bed_support_mm[2],
                ),
                (
                    -variant.bed_support_mm[0] / 2.0,
                    -(variant.bed_support_mm[1] + variant.tool_travel_mm[1]) / 2.0,
                    -variant.bed_support_mm[2],
                ),
                "motion-reference",
                "Union of the moving-bed support at both ends of full Y travel; used to expose front/rear and motor clearance.",
            ),
        )
    )
    return parts


def _z_components(
    build123d: Any,
    variant: Phase3APackagingVariant,
) -> list[SkeletonComponent]:
    axis = next(item for item in PHASE3_MOTION_PARAMETERS.axes if item.axis == "Z")
    rail = rail_class_lookup(axis.rail_class)
    rail_width, rail_height = next(
        envelope for name, envelope in PHASE3_MOTION_PARAMETERS.rail_reference_envelopes_mm if name == axis.rail_class
    )
    length = variant.rail_lengths_mm[2]
    z_center = variant.z_screw_center_z_mm
    rail_y = variant.z_rail_center_y_mm
    screw_y = rail_y + variant.z_screw_center_offset_y_mm
    support = _envelope(variant.bearing_fixed_envelopes_mm, "Z")
    floating = _envelope(variant.bearing_floating_envelopes_mm, "Z")
    coupler = next(
        envelope for name, envelope in PHASE3_MOTION_PARAMETERS.reference_coupler_envelopes_mm if name == "Z"
    )
    motor = PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm
    rail_base = z_center - length / 2.0
    parts: list[SkeletonComponent] = []
    for rail_index, x in enumerate((-axis.rail_center_spacing_mm / 2.0, axis.rail_center_spacing_mm / 2.0), start=1):
        parts.append(
            _named_box(
                build123d,
                f"phase3a_z_rail_{rail_index}",
                (rail_height, rail_width, length),
                (x - rail_height / 2.0, rail_y - rail_width / 2.0, rail_base),
                "motion-reference",
                "MGN9H nominal Z rail envelope; the short rail still includes the two-block swept group.",
            )
        )
        for carriage_index, offset in enumerate(variant.z_carriage_center_offsets_mm, start=1):
            parts.append(
                _centered_box(
                    build123d,
                    f"phase3a_z_carriage_{(rail_index - 1) * 2 + carriage_index}",
                    (rail.assembly_width_mm, rail.assembly_width_mm, rail.block_length_mm),
                    (x, rail_y, z_center + offset),
                    "Two MGN9H blocks per rail; MGN12 remains a stiffness fallback after coupon evidence.",
                )
            )
    screw_center = (0.0, screw_y, z_center)
    fixed_center = (0.0, screw_y, z_center + variant.screw_lengths_mm[2] / 2.0)
    floating_center = (0.0, screw_y, z_center - variant.screw_lengths_mm[2] / 2.0)
    fixed_top = fixed_center[2] + support[2] / 2.0
    motor_min_z = fixed_top + PHASE3_MOTION_PARAMETERS.reference_motor_clearance_mm
    spindle_mount_min = variant.gantry_bottom_z_mm + 20.0
    parts.extend(
        (
            _reference_axis(
                build123d,
                "phase3a_z_screw",
                "z",
                variant.screw_lengths_mm[2],
                screw_center,
                PHASE3_MOTION_PARAMETERS.reference_screw_diameter_mm,
                "T8x2 screw envelope; the fixed upper support carries axial load and the lower support floats radially.",
            ),
            _centered_box(build123d, "phase3a_z_nut", PHASE3_MOTION_PARAMETERS.reference_nut_envelope_mm, screw_center, "Preloaded Z nut envelope; gravity-hold and drag tests remain required."),
            _centered_box(build123d, "phase3a_z_fixed_bearing", support, fixed_center, "Fixed Z axial bearing cartridge envelope."),
            _centered_box(build123d, "phase3a_z_floating_bearing", floating, floating_center, "Floating Z radial bearing cartridge envelope."),
            _centered_box(build123d, "phase3a_z_coupler", coupler, fixed_center, "Flexible direct 5-to-8 mm Z coupler envelope."),
            _named_box(
                build123d,
                "phase3a_z_nema17",
                motor,
                (-motor[0] / 2.0, screw_y - motor[1] / 2.0, motor_min_z),
                "motion-reference",
                "Direct axial owner-supplied generic NEMA17 interface in a removable upper pocket; body length remains a 40-48 mm screen and rear connector/wiring access is required.",
            ),
            _named_box(
                build123d,
                "phase3a_spindle_mount",
                PHASE3_MOTION_PARAMETERS.spindle_mount_envelope_mm,
                (
                    -PHASE3_MOTION_PARAMETERS.spindle_mount_envelope_mm[0] / 2.0,
                    -20.0 - PHASE3_MOTION_PARAMETERS.spindle_mount_envelope_mm[1] / 2.0,
                    spindle_mount_min,
                ),
                "motion-reference",
                "Generic spindle clamp envelope; actual diameter, mass, runout, and cable exit remain unresolved.",
            ),
        )
    )
    return parts


def _process_components(
    build123d: Any,
    variant: Phase3APackagingVariant,
) -> list[SkeletonComponent]:
    tx, ty, tz = variant.tool_travel_mm
    wx, wy = variant.working_area_mm
    spindle_y = -20.0
    spindle_bottom = PHASE2_SKELETON_PARAMETERS.tool_stickout_mm
    spindle_diameter = PHASE2_SKELETON_PARAMETERS.spindle_envelope_diameter_mm
    spindle_length = PHASE2_SKELETON_PARAMETERS.spindle_envelope_length_mm
    limit_size = 12.0
    return [
        _named_box(
            build123d,
            "phase3a_pcb_working_area",
            (wx, wy, 2.0),
            (-wx / 2.0, -wy / 2.0, 0.0),
            "process-envelope",
            "Required PCB working area; this remains 200 x 150 mm in all variants.",
        ),
        _named_box(
            build123d,
            "phase3a_tool_point_travel",
            (tx, ty, tz),
            (-tx / 2.0, -ty / 2.0, -tz),
            "process-envelope",
            "Screened tool-point travel envelope; P3 reduces XY access margin and needs owner confirmation.",
        ),
        _component(
            build123d,
            "phase3a_spindle_envelope",
            "motion-reference",
            _cylinder(
                build123d,
                "phase3a_spindle_envelope",
                PHASE2_SKELETON_PARAMETERS.spindle_envelope_diameter_mm / 2.0,
                PHASE2_SKELETON_PARAMETERS.spindle_envelope_length_mm,
                (0.0, spindle_y, spindle_bottom),
            ),
            "Maximum screening spindle envelope; no spindle is selected.",
        ),
        _component(
            build123d,
            "phase3a_tool_envelope",
            "process-envelope",
            _cylinder(
                build123d,
                "phase3a_tool_envelope",
                3.0,
                PHASE2_SKELETON_PARAMETERS.tool_stickout_mm,
                (0.0, spindle_y, 0.0),
            ),
            "Tool stickout reference for clearance review; cutter geometry is not selected.",
        ),
        _named_box(
            build123d,
            "phase3a_spindle_xy_swept_envelope",
            (tx + spindle_diameter, ty + spindle_diameter, spindle_length),
            (-(tx + spindle_diameter) / 2.0, -(ty + spindle_diameter) / 2.0, spindle_bottom),
            "motion-reference",
            "Conservative XY union of the generic spindle envelope over screened tool-point travel.",
        ),
        _centered_box(
            build123d,
            "phase3a_x_home_limit",
            (limit_size, limit_size, limit_size),
            (
                -variant.body_envelope_mm[0] / 2.0 + variant.home_limit_clearance_mm + limit_size / 2.0,
                variant.x_rail_center_y_mm,
                variant.x_rail_center_z_mm,
            ),
            "X home/limit switch reference with declared service clearance; switch type is unresolved.",
        ),
        _centered_box(
            build123d,
            "phase3a_y_home_limit",
            (limit_size, limit_size, limit_size),
            (
                0.0,
                -variant.body_envelope_mm[1] / 2.0 + variant.home_limit_clearance_mm + limit_size / 2.0,
                variant.y_rail_center_z_mm,
            ),
            "Y home/limit switch reference at the negative/front end; moving-bed cable access remains open.",
        ),
        _centered_box(
            build123d,
            "phase3a_z_home_limit",
            (limit_size, limit_size, limit_size),
            (
                0.0,
                variant.z_rail_center_y_mm + variant.z_screw_center_offset_y_mm,
                variant.body_max_z_mm - variant.home_limit_clearance_mm - limit_size / 2.0,
            ),
            "Z positive-home switch reference above the moving head; final pull-off and guarding remain unresolved.",
        ),
    ]


def build_packaging_skeleton(
    variant: Phase3APackagingVariant | str,
    variants: tuple[Phase3APackagingVariant, ...] = PHASE3A_PACKAGING_VARIANTS,
) -> SkeletonModel:
    """Build one deterministic Phase 3A packaging review model."""

    build123d = _build123d()
    selected = (
        phase3a_variant_by_id(variant, variants)
        if isinstance(variant, str)
        else variant
    )
    components: list[SkeletonComponent] = [_structural_packaging_bound(build123d, selected)]
    components.extend(_process_components(build123d, selected))
    components.extend(_x_components(build123d, selected))
    components.extend(_y_components(build123d, selected))
    components.extend(_z_components(build123d, selected))
    return SkeletonModel(
        candidate_id=ArchitectureId.A,
        components=tuple(components),
        expected_interference_pairs=tuple(),
        variant=f"phase3a-{selected.variant_id.lower()}",
    )


def export_packaging_skeleton(model: SkeletonModel, output_dir: Path) -> dict[str, Path]:
    """Export review-only Phase 3A derivatives to an explicit temporary folder."""

    build123d = _build123d()
    output_dir.mkdir(parents=True, exist_ok=True)
    step_path = output_dir / f"{model.variant}-packaging-skeleton.step"
    stl_path = output_dir / f"{model.variant}-packaging-skeleton.stl"
    build123d.export_step(model.compound, step_path)
    build123d.export_stl(model.compound, stl_path, tolerance=0.01, angular_tolerance=0.2)
    return {"step": step_path, "stl": stl_path}


def packaging_model_interferences(model: SkeletonModel) -> tuple[dict[str, Any], ...]:
    """Expose the common interference helper with a Phase 3A-specific name."""

    return unexpected_interferences(model)
