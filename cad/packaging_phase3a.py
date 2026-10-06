"""Dependency-light calculations for the Phase 3A packaging study.

Phase 3A changes packaging around the accepted motion classes.  It does not
select a new guide family, screw lead, controller, spindle, or structural
part geometry.  The calculations deliberately treat the two-carriage group
as a swept body; rail length is therefore not allowed to collapse to merely
the requested tool travel.
"""

from __future__ import annotations

from dataclasses import dataclass

from cad.motion_phase3 import rail_class_lookup, screw_critical_speed_rpm
from cad.parameters import (
    PHASE2_SKELETON_PARAMETERS,
    PHASE3_MOTION_PARAMETERS,
    Phase3APackagingVariant,
)


@dataclass(frozen=True)
class AxisPackagingStudy:
    """Swept-travel and screw screen for one Phase 3A axis."""

    axis: str
    travel_mm: float
    rail_class: str
    block_length_mm: float
    carriage_center_offsets_mm: tuple[float, float]
    carriage_group_span_mm: float
    declared_end_margin_mm: float
    minimum_rail_length_mm: float
    rail_length_mm: float
    actual_end_margin_mm: float
    screw_lead_mm: float
    screw_length_mm: float
    screw_unsupported_length_mm: float
    critical_speed_rpm: float
    screened_max_feed_mm_min: float
    commissioning_feed_mm_min: float
    feed_margin_mm_min: float

    @property
    def rail_travel_passes(self) -> bool:
        return self.actual_end_margin_mm >= self.declared_end_margin_mm - 1e-6

    @property
    def feed_screen_passes(self) -> bool:
        return self.feed_margin_mm_min >= -1e-6


@dataclass(frozen=True)
class BedPackagingStudy:
    """Moving-bed support, PCB margin, and guide-support relationship."""

    bed_support_mm: tuple[float, float, float]
    working_area_mm: tuple[float, float]
    pcb_edge_margin_mm: tuple[float, float]
    y_rail_center_spacing_mm: float
    transverse_bed_overhang_mm: float
    longitudinal_bed_overhang_mm: float
    swept_bed_end_clearance_mm: float
    bed_to_y_motor_clearance_mm: float
    tool_to_bed_clearance_mm: tuple[float, float]
    spindle_swept_body_clearance_mm: tuple[float, float]
    low_profile_workholding_margin_mm: float
    vacuum_perimeter_status: str


@dataclass(frozen=True)
class ZStackStudy:
    """Vertical envelope stack, reported as overlapping maxima rather than a fake sum."""

    bed_support_drop_mm: float
    spoilboard_drop_mm: float
    pcb_max_thickness_mm: float
    tool_stickout_mm: float
    spindle_envelope_length_mm: float
    tool_and_spindle_top_mm: float
    z_carriage_group_min_mm: float
    z_carriage_group_max_mm: float
    z_rail_min_mm: float
    z_rail_max_mm: float
    z_fixed_support_top_mm: float
    z_motor_top_mm: float
    y_motor_bottom_mm: float
    gantry_top_mm: float
    package_min_z_mm: float
    package_max_z_mm: float
    package_height_mm: float


@dataclass(frozen=True)
class Phase3APackagingStudy:
    """All calculated Phase 3A results for one packaging variant."""

    variant_id: str
    axes: tuple[AxisPackagingStudy, ...]
    bed: BedPackagingStudy
    z_stack: ZStackStudy
    body_envelope_mm: tuple[float, float, float]
    service_footprint_mm: tuple[float, float, float]


def _axis_values(
    variant: Phase3APackagingVariant,
    axis_name: str,
) -> tuple[float, float, float, tuple[float, float], float]:
    """Return travel, rail, screw, carriage offsets, and feed for one axis."""

    index = {"X": 0, "Y": 1, "Z": 2}[axis_name]
    offsets = {
        "X": variant.x_carriage_center_offsets_mm,
        "Y": variant.y_carriage_center_offsets_mm,
        "Z": variant.z_carriage_center_offsets_mm,
    }[axis_name]
    return (
        variant.tool_travel_mm[index],
        variant.rail_lengths_mm[index],
        variant.screw_lengths_mm[index],
        offsets,
        variant.commissioning_feeds_mm_min[index],
    )


def carriage_group_span_mm(rail_class: str, center_offsets_mm: tuple[float, float]) -> float:
    """Return the physical length of two blocks along their rail direction."""

    rail = rail_class_lookup(rail_class)
    if len(center_offsets_mm) != 2 or center_offsets_mm[0] >= center_offsets_mm[1]:
        raise ValueError("two ordered carriage center offsets are required")
    center_spacing = center_offsets_mm[1] - center_offsets_mm[0]
    if center_spacing < rail.block_length_mm:
        raise ValueError(
            f"{rail_class} carriage centers overlap: {center_spacing:g} mm "
            f"< {rail.block_length_mm:g} mm block length"
        )
    return center_spacing + rail.block_length_mm


def minimum_rail_length_mm(
    travel_mm: float,
    carriage_group_span_mm_value: float,
    end_margin_mm: float,
) -> float:
    """Return travel plus the swept two-block group and both end margins."""

    if travel_mm <= 0 or carriage_group_span_mm_value <= 0 or end_margin_mm < 0:
        raise ValueError("travel, group span, and end margin are out of range")
    return travel_mm + carriage_group_span_mm_value + 2.0 * end_margin_mm


def _axis_study(variant: Phase3APackagingVariant, axis_name: str) -> AxisPackagingStudy:
    baseline_axis = next(axis for axis in PHASE3_MOTION_PARAMETERS.axes if axis.axis == axis_name)
    travel, rail_length, screw_length, offsets, commissioning_feed = _axis_values(variant, axis_name)
    block = rail_class_lookup(baseline_axis.rail_class)
    group_span = carriage_group_span_mm(baseline_axis.rail_class, offsets)
    index = {"X": 0, "Y": 1, "Z": 2}[axis_name]
    declared_margin = variant.rail_end_margin_mm[index]
    minimum_length = minimum_rail_length_mm(travel, group_span, declared_margin)
    actual_margin = (rail_length - travel - group_span) / 2.0
    critical_speed = screw_critical_speed_rpm(
        variant.screw_unsupported_lengths_mm[index],
        PHASE3_MOTION_PARAMETERS.screw_root_diameter_mm,
        PHASE3_MOTION_PARAMETERS.screw_youngs_modulus_n_per_mm2,
        PHASE3_MOTION_PARAMETERS.screw_density_kg_per_mm3,
    )
    screened_max_feed = (
        PHASE3_MOTION_PARAMETERS.critical_speed_margin
        * critical_speed
        * baseline_axis.screw_lead_mm
    )
    return AxisPackagingStudy(
        axis=axis_name,
        travel_mm=travel,
        rail_class=baseline_axis.rail_class,
        block_length_mm=block.block_length_mm,
        carriage_center_offsets_mm=offsets,
        carriage_group_span_mm=group_span,
        declared_end_margin_mm=declared_margin,
        minimum_rail_length_mm=minimum_length,
        rail_length_mm=rail_length,
        actual_end_margin_mm=actual_margin,
        screw_lead_mm=baseline_axis.screw_lead_mm,
        screw_length_mm=screw_length,
        screw_unsupported_length_mm=variant.screw_unsupported_lengths_mm[index],
        critical_speed_rpm=critical_speed,
        screened_max_feed_mm_min=screened_max_feed,
        commissioning_feed_mm_min=commissioning_feed,
        feed_margin_mm_min=screened_max_feed - commissioning_feed,
    )


def _bed_study(
    variant: Phase3APackagingVariant,
    y_axis: AxisPackagingStudy,
) -> BedPackagingStudy:
    bed_x, bed_y, _ = variant.bed_support_mm
    pcb_x, pcb_y = variant.working_area_mm
    margin_x = (bed_x - pcb_x) / 2.0
    margin_y = (bed_y - pcb_y) / 2.0
    y_group_overhang = (bed_y - y_axis.carriage_group_span_mm) / 2.0
    transverse_overhang = (
        bed_x - next(axis for axis in PHASE3_MOTION_PARAMETERS.axes if axis.axis == "Y").rail_center_spacing_mm
    ) / 2.0
    low_profile_margin = min(margin_x, margin_y)
    swept_bed_end_clearance = (
        variant.body_envelope_mm[1] - bed_y - variant.tool_travel_mm[1]
    ) / 2.0
    y_motor_top = (
        variant.y_motor_center_z_mm
        + PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm[0] / 2.0
    )
    bed_to_y_motor_clearance = -variant.bed_support_mm[2] - y_motor_top
    tool_to_bed_clearance = (
        (bed_x - variant.tool_travel_mm[0]) / 2.0,
        (bed_y - variant.tool_travel_mm[1]) / 2.0,
    )
    spindle_diameter = PHASE2_SKELETON_PARAMETERS.spindle_envelope_diameter_mm
    spindle_swept_body_clearance = (
        (variant.body_envelope_mm[0] - variant.tool_travel_mm[0] - spindle_diameter) / 2.0,
        (variant.body_envelope_mm[1] - variant.tool_travel_mm[1] - spindle_diameter) / 2.0,
    )
    if low_profile_margin >= 15.0:
        vacuum_status = "perimeter remains plausible for a future low-profile vacuum study"
    elif low_profile_margin >= 10.0:
        vacuum_status = "vacuum perimeter is conditional; tape or edge clamps are the default"
    else:
        vacuum_status = "vacuum perimeter is not supported by this compact bed screen"
    return BedPackagingStudy(
        bed_support_mm=variant.bed_support_mm,
        working_area_mm=variant.working_area_mm,
        pcb_edge_margin_mm=(margin_x, margin_y),
        y_rail_center_spacing_mm=next(
            axis for axis in PHASE3_MOTION_PARAMETERS.axes if axis.axis == "Y"
        ).rail_center_spacing_mm,
        transverse_bed_overhang_mm=transverse_overhang,
        longitudinal_bed_overhang_mm=y_group_overhang,
        swept_bed_end_clearance_mm=swept_bed_end_clearance,
        bed_to_y_motor_clearance_mm=bed_to_y_motor_clearance,
        tool_to_bed_clearance_mm=tool_to_bed_clearance,
        spindle_swept_body_clearance_mm=spindle_swept_body_clearance,
        low_profile_workholding_margin_mm=low_profile_margin,
        vacuum_perimeter_status=vacuum_status,
    )


def _z_stack(variant: Phase3APackagingVariant) -> ZStackStudy:
    z_axis = next(axis for axis in PHASE3_MOTION_PARAMETERS.axes if axis.axis == "Z")
    z_rail = rail_class_lookup(z_axis.rail_class)
    z_fixed = dict(variant.bearing_fixed_envelopes_mm)["Z"]
    z_center = variant.z_screw_center_z_mm
    z_rail_min = z_center - variant.rail_lengths_mm[2] / 2.0
    z_rail_max = z_center + variant.rail_lengths_mm[2] / 2.0
    z_carriage_min = z_center + min(variant.z_carriage_center_offsets_mm) - z_rail.block_length_mm / 2.0
    z_carriage_max = z_center + max(variant.z_carriage_center_offsets_mm) + z_rail.block_length_mm / 2.0
    z_fixed_center = z_center + variant.screw_lengths_mm[2] / 2.0
    z_fixed_top = z_fixed_center + z_fixed[2] / 2.0
    z_motor_top = (
        z_fixed_top
        + PHASE3_MOTION_PARAMETERS.reference_motor_clearance_mm
        + PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm[2]
    )
    y_motor_bottom = (
        variant.y_motor_center_z_mm
        - PHASE3_MOTION_PARAMETERS.reference_motor_envelope_mm[0] / 2.0
    )
    gantry_top = variant.gantry_bottom_z_mm + variant.gantry_height_mm
    tool_and_spindle_top = (
        PHASE2_SKELETON_PARAMETERS.tool_stickout_mm
        + PHASE2_SKELETON_PARAMETERS.spindle_envelope_length_mm
    )
    return ZStackStudy(
        bed_support_drop_mm=variant.bed_support_mm[2],
        spoilboard_drop_mm=variant.spoilboard_mm[2],
        pcb_max_thickness_mm=2.0,
        tool_stickout_mm=PHASE2_SKELETON_PARAMETERS.tool_stickout_mm,
        spindle_envelope_length_mm=PHASE2_SKELETON_PARAMETERS.spindle_envelope_length_mm,
        tool_and_spindle_top_mm=tool_and_spindle_top,
        z_carriage_group_min_mm=z_carriage_min,
        z_carriage_group_max_mm=z_carriage_max,
        z_rail_min_mm=z_rail_min,
        z_rail_max_mm=z_rail_max,
        z_fixed_support_top_mm=z_fixed_top,
        z_motor_top_mm=z_motor_top,
        y_motor_bottom_mm=y_motor_bottom,
        gantry_top_mm=gantry_top,
        package_min_z_mm=variant.body_min_z_mm,
        package_max_z_mm=variant.body_max_z_mm,
        package_height_mm=variant.body_max_z_mm - variant.body_min_z_mm,
    )


def phase3a_packaging_study(
    variant: Phase3APackagingVariant,
) -> Phase3APackagingStudy:
    """Calculate rail sweep, bed, screw, and Z-stack evidence."""

    axes = tuple(_axis_study(variant, name) for name in ("X", "Y", "Z"))
    return Phase3APackagingStudy(
        variant_id=variant.variant_id,
        axes=axes,
        bed=_bed_study(variant, axes[1]),
        z_stack=_z_stack(variant),
        body_envelope_mm=variant.body_envelope_mm,
        service_footprint_mm=variant.service_footprint_mm,
    )


def phase3a_variant_by_id(
    variant_id: str,
    variants: tuple[Phase3APackagingVariant, ...],
) -> Phase3APackagingVariant:
    """Resolve a packaging variant by stable ID."""

    for variant in variants:
        if variant.variant_id == variant_id:
            return variant
    raise KeyError(f"Unknown Phase 3A packaging variant: {variant_id}")
