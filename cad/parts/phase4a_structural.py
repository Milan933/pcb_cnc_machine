"""Phase 4A PETG structural optimization candidates.

Phase 4A deliberately lives beside, rather than overwrites, the Phase 4
preliminary concept.  The O1/O2/O3 builders reuse the accepted P2 coordinates
and hardware envelopes, then consolidate only the printed force-loop geometry
that has a defensible printability and service boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cad.assembly.architecture_skeleton import SkeletonComponent
from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS, ParameterStatus
from cad.parts.phase4_structural import (
    _box,
    _closed_box,
    _compound,
    _build123d,
    build_phase4_structural_parts,
)


VARIANT_ORDER = ("O1", "O2", "O3")
SELECTED_PHASE4A_VARIANT = "O2"


@dataclass(frozen=True)
class Phase4AOptimizationVariant:
    """Owner-review description of one structural optimization level."""

    variant_id: str
    title: str
    description: str
    serviceability: str
    alignment_risk: str
    assembly_complexity: str


PHASE4A_VARIANTS = (
    Phase4AOptimizationVariant(
        "O1",
        "conservative consolidation",
        "Integrate the X/Z bearing and motor support structure into the X carriage while leaving the Phase 4 base and gantry decomposition intact.",
        "Very high; all base, gantry, bearing, foot, and accessory modules remain replaceable.",
        "Low change from Phase 4; existing rail-seat datums are retained.",
        "Low change; one new X/Z backbone part and two fewer service shells.",
    ),
    Phase4AOptimizationVariant(
        "O2",
        "balanced optimization",
        "Integrate each base side with its Y rail carrier and perimeter members, integrate each beam half with its tower, and make the X/Z support a coherent backbone while retaining replaceable hardware modules.",
        "High; motors, bearings, rails, screws, spindle clamp, feet, and electronics remain serviceable.",
        "Moderate and inspectable; two 300 mm base modules require conditioning, datum inspection, and shimming.",
        "Moderate; fewer structural seams, with two integrated base modules and two integrated gantry modules.",
    ),
    Phase4AOptimizationVariant(
        "O3",
        "aggressive integration",
        "Integrate each base, Y carrier, tower, beam half, and X screw-support envelope into two 300 mm side modules; remove printed feet/electronics rail and absorb X bearing pockets.",
        "Reduced; bearing pockets and table interfaces are no longer independent printed modules.",
        "Highest; large 300 mm integrated parts and embedded bearing datums increase conditioning and replacement risk.",
        "Lowest part count but highest handling, inspection, and repair complexity.",
    ),
)


BASE_CLASSIFICATION = {
    "base_front_left": "CRITICAL STRUCTURAL",
    "base_front_right": "CRITICAL STRUCTURAL",
    "base_rear_left": "CRITICAL STRUCTURAL",
    "base_rear_right": "CRITICAL STRUCTURAL",
    "base_left_side_member": "CRITICAL STRUCTURAL",
    "base_right_side_member": "CRITICAL STRUCTURAL",
    "base_y_rail_carrier_left": "CRITICAL STRUCTURAL",
    "base_y_rail_carrier_right": "CRITICAL STRUCTURAL",
    "base_center_tie": "CRITICAL STRUCTURAL",
    "gantry_tower_left": "CRITICAL STRUCTURAL",
    "gantry_tower_right": "CRITICAL STRUCTURAL",
    "gantry_beam_left": "CRITICAL STRUCTURAL",
    "gantry_beam_right": "CRITICAL STRUCTURAL",
    "x_carriage_plate": "CRITICAL STRUCTURAL",
    "z_carriage_plate": "CRITICAL STRUCTURAL",
    "moving_bed_frame": "CRITICAL STRUCTURAL",
    "y_motor_service_pocket": "SECONDARY STRUCTURAL",
    "y_fixed_bearing_cartridge": "SECONDARY STRUCTURAL",
    "y_floating_bearing_cartridge": "SECONDARY STRUCTURAL",
    "x_fixed_bearing_cartridge": "SECONDARY STRUCTURAL",
    "x_floating_bearing_cartridge": "SECONDARY STRUCTURAL",
    "z_fixed_bearing_support": "SECONDARY STRUCTURAL",
    "z_motor_service_cartridge": "SECONDARY STRUCTURAL",
    "machine_foot_front_left": "MOUNT / INTERFACE",
    "machine_foot_front_right": "MOUNT / INTERFACE",
    "machine_foot_rear_left": "MOUNT / INTERFACE",
    "machine_foot_rear_right": "MOUNT / INTERFACE",
    "spindle_mount_concept": "MOUNT / INTERFACE",
    "electronics_mount_rail": "NON-STRUCTURAL",
}


PRIMARY_LOOP_BY_VARIANT = {
    "O1": {
        "base_front_left",
        "base_front_right",
        "base_rear_left",
        "base_rear_right",
        "base_left_side_member",
        "base_right_side_member",
        "base_y_rail_carrier_left",
        "base_y_rail_carrier_right",
        "base_center_tie",
        "gantry_tower_left",
        "gantry_tower_right",
        "gantry_beam_left",
        "gantry_beam_right",
        "x_z_backbone",
        "z_carriage_plate",
        "spindle_mount_concept",
        "moving_bed_frame",
    },
    "O2": {
        "base_left_integrated",
        "base_right_integrated",
        "base_center_tie",
        "gantry_left_integrated",
        "gantry_right_integrated",
        "x_z_backbone",
        "z_carriage_plate",
        "spindle_mount_concept",
        "moving_bed_frame",
    },
    "O3": {
        "base_gantry_left",
        "base_gantry_right",
        "base_center_tie",
        "x_z_backbone",
        "z_carriage_plate",
        "spindle_mount_concept",
        "moving_bed_frame",
    },
}

# Pair-level count: mirrored/two-sided contacts are intentionally counted as
# separate interfaces so the before/after count is auditable and conservative.
PRIMARY_LOOP_JOINT_COUNT_BY_VARIANT = {"O1": 17, "O2": 7, "O3": 5}


@dataclass(frozen=True)
class Phase4APartRecord:
    """Preliminary manufacturing and load-path record for one Phase 4A part."""

    part_id: str
    title: str
    role: str
    classification: str
    nominal_bbox_mm: tuple[float, float, float]
    print_orientation: str
    print_orientation_extents_mm: tuple[float, float, float]
    support_requirement: str
    brim_requirement: str
    warping_risk: str
    layer_load_concern: str
    notes: str
    direct_force_loop: bool
    serviceable: bool
    status: ParameterStatus = ParameterStatus.PRELIMINARY
    mandatory: bool = True


_CUSTOM_META = {
    "base_left_integrated": (
        "integrated left base/Y rail module",
        "integrated base side, front/rear perimeter, and left Y rail carrier",
        "flat on a 150 x 300 mm XY footprint; rail datum upward",
        "No support; inspect closed walls and continuous rail web.",
        "Required at the 300 mm preferred boundary",
        "medium-high over the 300 mm Y axis",
        "Longitudinal layers carry Y rail and base shear; use a conditioned datum strip.",
        "Combines four former critical parts while retaining a removable center tie and hardware interfaces.",
    ),
    "base_right_integrated": (
        "integrated right base/Y rail module",
        "integrated base side, front/rear perimeter, and right Y rail carrier",
        "flat on a 150 x 300 mm XY footprint; rail datum upward",
        "No support; inspect closed walls and continuous rail web.",
        "Required at the 300 mm preferred boundary",
        "medium-high over the 300 mm Y axis",
        "Longitudinal layers carry Y rail and base shear; use a conditioned datum strip.",
        "Mirror of the left module; the 300 mm footprint is retained as an explicit risk.",
    ),
    "gantry_left_integrated": (
        "integrated left gantry side",
        "continuous left tower and left X torsion-beam half",
        "flat or side-supported on a 180 x 122 mm XY footprint",
        "No support in the closed section; bridge and shoulder coupons required.",
        "Optional brim after warp study",
        "medium-high; tower-to-beam transition is tall",
        "Layers follow X; a thick printed shoulder/gusset carries tower-to-beam shear without a PETG joint.",
        "Eliminates the left beam-to-tower PETG joint while keeping the J1 center split and rail pads.",
    ),
    "gantry_right_integrated": (
        "integrated right gantry side",
        "continuous right tower and right X torsion-beam half",
        "flat or side-supported on a 172 x 122 mm XY footprint",
        "No support in the closed section; bridge and socket cleanup required.",
        "Optional brim after warp study",
        "medium-high; tower-to-beam transition is tall",
        "Layers follow X; a thick printed shoulder/gusset carries tower-to-beam shear without a PETG joint.",
        "Mirror of the left module; J1 remains a serviceable center interface.",
    ),
    "x_z_backbone": (
        "integrated X/Z support backbone",
        "X carriage with integrated Z screw-support and motor-interface structure",
        "upright on a 90 x 54 mm XY footprint with the guide ribs vertical",
        "No support; top web and bearing datums require post-print inspection.",
        "Recommended",
        "medium-high because the part is 201 mm tall",
        "Guide reactions stay in one ribbed backplate; the Z motor and bearing hardware remain removable.",
        "Eliminates two small printed adapters and shortens the X-to-Z load path without removing service hardware.",
    ),
    "base_gantry_left": (
        "integrated left base/gantry side",
        "continuous left base/Y carrier/tower/beam half with absorbed X bearing pocket",
        "flat on a 189 x 300 mm XY footprint; tower upright in the same print",
        "No support in the concept; printer-specific 300 mm warp and tower datum proof required.",
        "Required and printer-specific",
        "high; largest integrated structural print",
        "Continuous side force loop but difficult conditioning and repair; bearing datum is no longer a separate PETG cartridge.",
        "Aggressive option only; service and alignment risk are intentionally visible.",
    ),
    "base_gantry_right": (
        "integrated right base/gantry side",
        "continuous right base/Y carrier/tower/beam half with absorbed X bearing pocket",
        "flat on a 189 x 300 mm XY footprint; tower upright in the same print",
        "No support in the concept; printer-specific 300 mm warp and tower datum proof required.",
        "Required and printer-specific",
        "high; largest integrated structural print",
        "Continuous side force loop but difficult conditioning and repair; bearing datum is no longer a separate PETG cartridge.",
        "Mirror of the aggressive left module; retained only for O3 comparison.",
    ),
}


def _bbox_tuple(shape: Any) -> tuple[float, float, float]:
    bbox = shape.bounding_box()
    return tuple(round(float(getattr(bbox.size, axis)), 3) for axis in ("X", "Y", "Z"))


def _optimized_box(build123d: Any, name: str, size: tuple[float, float, float], minimum: tuple[float, float, float]) -> Any:
    return _box(build123d, name, size, minimum)


def _optimized_base_module(build123d: Any, side: str, baseline: dict[str, Any]) -> Any:
    """Build one continuous base/Y rail side with a thin connecting web."""

    if side == "left":
        front_name, rear_name, side_name, carrier_name = (
            "base_front_left",
            "base_rear_left",
            "base_left_side_member",
            "base_y_rail_carrier_left",
        )
        side_x = -174.0
        carrier_x = -124.0
        front_x = -174.0
    else:
        front_name, rear_name, side_name, carrier_name = (
            "base_front_right",
            "base_rear_right",
            "base_right_side_member",
            "base_y_rail_carrier_right",
        )
        side_x = 126.0
        carrier_x = 96.0
        front_x = 24.0

    # Five-millimetre walls reduce unnecessary shell material while retaining
    # a closed section and broad base faces.  The real wall/perimeter recipe
    # remains a print-process item, not a release slicer freeze.
    front = _closed_box(build123d, f"phase4a_{side}_front", (150.0, 32.0, 36.0), (front_x, -150.0, -56.0), 5.0)
    rear = _closed_box(build123d, f"phase4a_{side}_rear", (150.0, 32.0, 36.0), (front_x, 118.0, -56.0), 5.0)
    side_member = _closed_box(build123d, f"phase4a_{side}_side", (48.0, 236.0, 36.0), (side_x, -118.0, -56.0), 5.0)
    carrier = baseline[carrier_name]
    # The web bridges the two-millimetre concept gap between the side shell
    # and carrier. It is a continuous shear path, not a thin decorative rib.
    web_x = side_x + 44.0 if side == "left" else carrier_x + 24.0
    web = _optimized_box(
        build123d,
        f"phase4a_{side}_rail_web",
        (14.0, 236.0, 16.0),
        (web_x, -118.0, -37.25),
    )
    result = _compound(build123d, f"base_{side}_integrated", [front, rear, side_member, carrier, web])
    result.label = f"base_{side}_integrated"
    return result


def _optimized_tower(build123d: Any, side: str) -> Any:
    center_x = -142.0 if side == "left" else 142.0
    width = PHASE4_STRUCTURAL_PARAMETERS.gantry_tower_width_mm
    minimum_x = center_x - width / 2.0
    outer = _optimized_box(build123d, f"phase4a_{side}_tower_outer", (width, 90.0, 62.0), (minimum_x, -10.0, -20.0))
    cavity = _optimized_box(build123d, f"phase4a_{side}_tower_cavity", (width - 22.0, 70.0, 50.0), (minimum_x + 11.0, 0.0, -14.0))
    shoulder = _optimized_box(build123d, f"phase4a_{side}_tower_shoulder", (width, 90.0, 8.0), (minimum_x, -10.0, 34.0))
    return _compound(build123d, f"phase4a_{side}_tower", [outer.cut(cavity), shoulder])


def _optimized_beam(build123d: Any, side: str) -> Any:
    if side == "left":
        main = _closed_box(build123d, "phase4a_beam_left_main", (172.0, 90.0, 90.0), (-172.0, -10.0, 42.0), 5.0)
        tongue = _optimized_box(build123d, "phase4a_beam_left_tongue", (8.0, 40.0, 60.0), (0.0, 15.0, 57.0))
        pads = [
            _optimized_box(build123d, "phase4a_beam_left_lower_pad", (172.0, 32.0, 14.0), (-172.0, -42.0, 47.0)),
            _optimized_box(build123d, "phase4a_beam_left_upper_pad", (172.0, 32.0, 14.0), (-172.0, -42.0, 107.0)),
        ]
    else:
        main = _closed_box(build123d, "phase4a_beam_right_main", (172.0, 90.0, 90.0), (0.0, -10.0, 42.0), 5.0)
        groove = _optimized_box(build123d, "phase4a_beam_right_groove", (8.0, 40.0, 60.0), (0.0, 15.0, 57.0))
        main = main.cut(groove)
        tongue = None
        pads = [
            _optimized_box(build123d, "phase4a_beam_right_lower_pad", (172.0, 32.0, 14.0), (0.0, -42.0, 47.0)),
            _optimized_box(build123d, "phase4a_beam_right_upper_pad", (172.0, 32.0, 14.0), (0.0, -42.0, 107.0)),
        ]
    pieces = [main, *pads]
    if tongue is not None:
        pieces.append(tongue)
    return _compound(build123d, f"gantry_{side}_beam", pieces)


def _optimized_gantry_module(build123d: Any, side: str) -> Any:
    tower = _optimized_tower(build123d, side)
    beam = _optimized_beam(build123d, side)
    center_x = -142.0 if side == "left" else 142.0
    minimum_x = center_x - 27.0
    # Eight millimetres of overlapping shoulder/gusset makes the tower-to-beam
    # path one printed part instead of a fastener-dominated PETG interface.
    shoulder = _optimized_box(
        build123d,
        f"phase4a_{side}_beam_tower_gusset",
        (54.0, 90.0, 8.0),
        (minimum_x, -10.0, 38.0),
    )
    result = _compound(build123d, f"gantry_{side}_integrated", [tower, beam, shoulder])
    result.label = f"gantry_{side}_integrated"
    return result


def _optimized_xz_backbone(build123d: Any, baseline: dict[str, Any]) -> Any:
    x_plate = baseline["x_carriage_plate"]
    z_support = baseline["z_fixed_bearing_support"]
    z_motor = baseline["z_motor_service_cartridge"]
    upper_web = _optimized_box(build123d, "phase4a_xz_upper_web", (70.0, 54.0, 8.0), (-35.0, -48.0, 138.0))
    motor_web = _optimized_box(build123d, "phase4a_xz_motor_web", (70.0, 50.0, 8.0), (-35.0, -48.0, 170.0))
    result = _compound(build123d, "x_z_backbone", [x_plate, z_support, z_motor, upper_web, motor_web])
    result.label = "x_z_backbone"
    return result


def _optimized_bed(build123d: Any) -> Any:
    """Build a lighter closed perimeter/rib bed with a retained nut boss."""

    bed_z = -8.0
    pieces = [
        _optimized_box(build123d, "phase4a_bed_front", (230.0, 14.0, 10.0), (-115.0, -90.0, bed_z)),
        _optimized_box(build123d, "phase4a_bed_rear", (230.0, 14.0, 10.0), (-115.0, 76.0, bed_z)),
        _optimized_box(build123d, "phase4a_bed_left", (14.0, 152.0, 10.0), (-115.0, -76.0, bed_z)),
        _optimized_box(build123d, "phase4a_bed_right", (14.0, 152.0, 10.0), (101.0, -76.0, bed_z)),
    ]
    for index, x in enumerate((-55.0, 0.0, 55.0), start=1):
        pieces.append(_optimized_box(build123d, f"phase4a_bed_cross_rib_{index}", (12.0, 126.0, 10.0), (x - 6.0, -63.0, bed_z)))
    pieces.append(_optimized_box(build123d, "phase4a_bed_center_web", (10.0, 126.0, 10.0), (-5.0, -63.0, bed_z)))
    pieces.append(_optimized_box(build123d, "phase4a_bed_y_nut_boss", (40.0, 32.0, 26.0), (-20.0, -16.0, -26.0)))
    for index, (x, y) in enumerate(((-110.0, -40.0), (110.0, -40.0), (-110.0, 40.0), (110.0, 40.0)), start=1):
        pieces.append(_optimized_box(build123d, f"phase4a_bed_carriage_pad_{index}", (10.0, 32.0, 10.0), (x - 5.0, y - 16.0, bed_z)))
    result = _compound(build123d, "moving_bed_frame", pieces)
    result.label = "moving_bed_frame"
    return result


def _shape_map(variant_id: str) -> dict[str, Any]:
    if variant_id not in VARIANT_ORDER:
        raise ValueError(f"Unknown Phase 4A variant: {variant_id}")
    build123d = _build123d()
    baseline_components = build_phase4_structural_parts()
    baseline = {component.name: component.shape for component in baseline_components}

    if variant_id == "O1":
        result = dict(baseline)
        result.pop("x_carriage_plate")
        result.pop("z_fixed_bearing_support")
        result.pop("z_motor_service_cartridge")
        result["x_z_backbone"] = _optimized_xz_backbone(build123d, baseline)
        return result

    left_base = _optimized_base_module(build123d, "left", baseline)
    right_base = _optimized_base_module(build123d, "right", baseline)
    left_gantry = _optimized_gantry_module(build123d, "left")
    right_gantry = _optimized_gantry_module(build123d, "right")
    xz_backbone = _optimized_xz_backbone(build123d, baseline)
    bed = _optimized_bed(build123d)

    if variant_id == "O2":
        return {
            "base_left_integrated": left_base,
            "base_right_integrated": right_base,
            "base_center_tie": baseline["base_center_tie"],
            "y_motor_service_pocket": baseline["y_motor_service_pocket"],
            "y_fixed_bearing_cartridge": baseline["y_fixed_bearing_cartridge"],
            "y_floating_bearing_cartridge": baseline["y_floating_bearing_cartridge"],
            "machine_foot_front_left": baseline["machine_foot_front_left"],
            "machine_foot_front_right": baseline["machine_foot_front_right"],
            "machine_foot_rear_left": baseline["machine_foot_rear_left"],
            "machine_foot_rear_right": baseline["machine_foot_rear_right"],
            "electronics_mount_rail": baseline["electronics_mount_rail"],
            "gantry_left_integrated": left_gantry,
            "gantry_right_integrated": right_gantry,
            "x_fixed_bearing_cartridge": baseline["x_fixed_bearing_cartridge"],
            "x_floating_bearing_cartridge": baseline["x_floating_bearing_cartridge"],
            "x_z_backbone": xz_backbone,
            "z_carriage_plate": baseline["z_carriage_plate"],
            "spindle_mount_concept": baseline["spindle_mount_concept"],
            "moving_bed_frame": bed,
        }

    # O3 is a comparison screen, not the selected build.  The bearing pockets
    # are absorbed into the integrated side modules, but the metal bearings
    # remain replaceable through their pocket openings.
    left_bearing_bridge = _optimized_box(build123d, "phase4a_o3_left_base_tower_bridge", (54.0, 90.0, 8.0), (-169.0, -10.0, -24.0))
    right_bearing_bridge = _optimized_box(build123d, "phase4a_o3_right_base_tower_bridge", (54.0, 90.0, 8.0), (115.0, -10.0, -24.0))
    left_integrated = _compound(
        build123d,
        "base_gantry_left",
        [left_base, left_gantry, baseline["x_fixed_bearing_cartridge"], left_bearing_bridge],
    )
    right_integrated = _compound(
        build123d,
        "base_gantry_right",
        [right_base, right_gantry, baseline["x_floating_bearing_cartridge"], right_bearing_bridge],
    )
    return {
        "base_gantry_left": left_integrated,
        "base_gantry_right": right_integrated,
        "base_center_tie": baseline["base_center_tie"],
        "y_motor_service_pocket": baseline["y_motor_service_pocket"],
        "y_fixed_bearing_cartridge": baseline["y_fixed_bearing_cartridge"],
        "y_floating_bearing_cartridge": baseline["y_floating_bearing_cartridge"],
        "x_z_backbone": xz_backbone,
        "z_carriage_plate": baseline["z_carriage_plate"],
        "spindle_mount_concept": baseline["spindle_mount_concept"],
        "moving_bed_frame": bed,
    }


def build_phase4a_structural_parts(variant_id: str = SELECTED_PHASE4A_VARIANT) -> tuple[SkeletonComponent, ...]:
    """Build one Phase 4A variant as named, unfused review components."""

    shapes = _shape_map(variant_id)
    components: list[SkeletonComponent] = []
    for part_id, shape in shapes.items():
        shape.label = part_id
        classification = phase4a_classification(part_id, variant_id)
        components.append(
            SkeletonComponent(
                name=part_id,
                category="structural",
                shape=shape,
                notes=(
                    f"PRELIMINARY Phase 4A {variant_id} review geometry; {classification}. "
                    "Not manufacturing-ready; measured hardware, inserts, print coupons, and physical force-loop evidence remain open."
                ),
            )
        )
    return tuple(components)


def phase4a_classification(part_id: str, variant_id: str = SELECTED_PHASE4A_VARIANT) -> str:
    """Return the controlled review classification for a Phase 4A part."""

    if part_id in {
        "base_left_integrated",
        "base_right_integrated",
        "base_gantry_left",
        "base_gantry_right",
        "base_center_tie",
        "gantry_left_integrated",
        "gantry_right_integrated",
        "x_z_backbone",
        "z_carriage_plate",
        "moving_bed_frame",
    }:
        return "CRITICAL STRUCTURAL"
    if part_id == "spindle_mount_concept" or part_id.startswith("machine_foot"):
        return "MOUNT / INTERFACE"
    if part_id == "electronics_mount_rail":
        return "NON-STRUCTURAL"
    # O1 intentionally retains the Phase 4 decomposition for the base and
    # gantry.  Preserve those controlled classifications instead of silently
    # turning them into secondary parts merely because they are unchanged.
    return BASE_CLASSIFICATION.get(part_id, "SECONDARY STRUCTURAL")


def phase4a_primary_loop_parts(variant_id: str = SELECTED_PHASE4A_VARIANT) -> frozenset[str]:
    return frozenset(PRIMARY_LOOP_BY_VARIANT[variant_id])


def phase4a_part_records(
    components: tuple[SkeletonComponent, ...] | None = None,
    variant_id: str = SELECTED_PHASE4A_VARIANT,
) -> tuple[Phase4APartRecord, ...]:
    """Return records using actual built bounding boxes and explicit process notes."""

    components = components or build_phase4a_structural_parts(variant_id)
    baseline_by_id = {part.part_id: part for part in PHASE4_STRUCTURAL_PARAMETERS.print_parts}
    primary = phase4a_primary_loop_parts(variant_id)
    serviceable_ids = {
        "y_motor_service_pocket",
        "y_fixed_bearing_cartridge",
        "y_floating_bearing_cartridge",
        "x_fixed_bearing_cartridge",
        "x_floating_bearing_cartridge",
        "machine_foot_front_left",
        "machine_foot_front_right",
        "machine_foot_rear_left",
        "machine_foot_rear_right",
        "electronics_mount_rail",
        "spindle_mount_concept",
        "z_carriage_plate",
    }
    records: list[Phase4APartRecord] = []
    for component in components:
        bbox = _bbox_tuple(component.shape)
        custom = _CUSTOM_META.get(component.name)
        if custom is not None:
            title, role, orientation, support, brim, warping, layer_load, notes = custom
        else:
            baseline = baseline_by_id.get(component.name)
            if baseline is None:
                raise KeyError(f"No Phase 4A metadata for {component.name}")
            title = baseline.title
            role = baseline.role
            orientation = baseline.print_orientation
            support = baseline.support_requirement
            brim = baseline.brim_requirement
            warping = baseline.warping_risk
            layer_load = baseline.layer_load_concern
            notes = baseline.notes
        records.append(
            Phase4APartRecord(
                part_id=component.name,
                title=title,
                role=role,
                classification=phase4a_classification(component.name, variant_id),
                nominal_bbox_mm=bbox,
                print_orientation=orientation,
                print_orientation_extents_mm=bbox,
                support_requirement=support,
                brim_requirement=brim,
                warping_risk=warping,
                layer_load_concern=layer_load,
                notes=notes,
                direct_force_loop=component.name in primary,
                serviceable=component.name in serviceable_ids,
            )
        )
    return tuple(sorted(records, key=lambda record: record.part_id))


__all__ = [
    "PHASE4A_VARIANTS",
    "PRIMARY_LOOP_BY_VARIANT",
    "PRIMARY_LOOP_JOINT_COUNT_BY_VARIANT",
    "SELECTED_PHASE4A_VARIANT",
    "Phase4AOptimizationVariant",
    "Phase4APartRecord",
    "build_phase4a_structural_parts",
    "phase4a_classification",
    "phase4a_part_records",
    "phase4a_primary_loop_parts",
]
