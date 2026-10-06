"""Complete Phase 5 local printable PETG structural parts.

The Phase 4A geometry was a review assembly.  This module is the
manufacturing-CAD continuation: every stable part ID below is a local,
single-solid parametric candidate.  Assembly placement is intentionally kept
out of this module so local STL files remain slicer-ready and reproducible.

All dimensions that depend on unmeasured rail, bearing, screw, insert,
spindle, or controller hardware are screening dimensions and are marked
``PROVISIONAL_HARDWARE_DIMENSION`` in the inventory metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cad.parameters import PHASE5_COMPLETE_PARAMETERS

from .phase5_structural import build_phase5_base_pair


PHASE5_COMPLETE_PART_IDS = (
    "base_left_integrated",
    "base_right_integrated",
    "base_center_tie",
    "y_motor_service_pocket",
    "y_fixed_bearing_cartridge",
    "y_floating_bearing_cartridge",
    "machine_foot_front_left",
    "machine_foot_front_right",
    "machine_foot_rear_left",
    "machine_foot_rear_right",
    "electronics_mount_rail",
    "gantry_left_integrated",
    "gantry_right_integrated",
    "x_fixed_bearing_cartridge",
    "x_floating_bearing_cartridge",
    "x_z_backbone",
    "z_carriage_plate",
    "spindle_mount_concept",
    "moving_bed_frame",
)


@dataclass(frozen=True)
class Phase5PartDefinition:
    """Stable inventory metadata for one printable structural part."""

    part_number: str
    part_id: str
    description: str
    quantity: int
    material: str
    maturity: str
    print_orientation: str
    support_strategy: str
    interface_status: str
    critical: bool
    notes: str


def _definition(
    number: int,
    part_id: str,
    description: str,
    *,
    quantity: int = 1,
    orientation: str = "flat on the broad XY datum; Z is print-up",
    support: str = "No support preferred; validate bridges and use brim only if required",
    critical: bool = False,
    notes: str = "",
) -> Phase5PartDefinition:
    return Phase5PartDefinition(
        part_number=f"PCNC-P{number:03d}",
        part_id=part_id,
        description=description,
        quantity=quantity,
        material="PETG",
        maturity="PROTOTYPE-STL",
        print_orientation=orientation,
        support_strategy=support,
        interface_status="PROVISIONAL_HARDWARE_DIMENSION",
        critical=critical,
        notes=notes,
    )


PHASE5_COMPLETE_PART_DEFINITIONS = (
    _definition(1, "base_left_integrated", "left integrated base, Y rail and tower load path", critical=True),
    _definition(2, "base_right_integrated", "right integrated base, Y rail and tower load path", critical=True),
    _definition(3, "base_center_tie", "transverse base shear tie", critical=True),
    _definition(4, "y_motor_service_pocket", "removable Y motor and coupler service mount", notes="NEMA17 face and shaft opening are screening geometry."),
    _definition(5, "y_fixed_bearing_cartridge", "Y fixed-end bearing cartridge", notes="Bearing bore and axial stack remain provisional."),
    _definition(6, "y_floating_bearing_cartridge", "Y floating-end bearing cartridge", notes="Radial-only support; axial float is intentional."),
    _definition(7, "machine_foot_front_left", "front-left leveling foot interface"),
    _definition(8, "machine_foot_front_right", "front-right leveling foot interface"),
    _definition(9, "machine_foot_rear_left", "rear-left leveling foot interface"),
    _definition(10, "machine_foot_rear_right", "rear-right leveling foot interface"),
    _definition(11, "electronics_mount_rail", "rear electronics and cable-service mounting rail"),
    _definition(12, "gantry_left_integrated", "left fixed gantry tower and X beam segment", critical=True, orientation="flat on beam side or broad XY face; inspect tower-to-base datum"),
    _definition(13, "gantry_right_integrated", "right fixed gantry tower and X beam socket segment", critical=True, orientation="flat on beam side or broad XY face; inspect socket and tower datum"),
    _definition(14, "x_fixed_bearing_cartridge", "X fixed-end bearing cartridge", notes="T8 bearing pocket remains provisional."),
    _definition(15, "x_floating_bearing_cartridge", "X floating-end bearing cartridge", notes="Radial-only support; axial float is intentional."),
    _definition(16, "x_z_backbone", "X carriage and dual Z rail backplate", critical=True, orientation="upright or on the back datum; condition the rail seats"),
    _definition(17, "z_carriage_plate", "moving Z carriage and spindle force-loop plate", critical=True, orientation="upright on the back datum; keep spindle interface face accessible"),
    _definition(18, "spindle_mount_concept", "modular parametric spindle clamp mount", critical=True, orientation="upright on the rear plate; ring axes remain vertical"),
    _definition(19, "moving_bed_frame", "ribbed moving Y bed with screw nut and carriage pads", critical=True),
)


def _build123d() -> Any:
    try:
        import build123d
    except ImportError as exc:  # pragma: no cover - CAD runner only
        raise RuntimeError(
            "Complete manufacturing geometry requires build123d. Install the "
            "pinned dependency from requirements/cad-phase-2.txt."
        ) from exc
    return build123d


def _box(bd: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], label: str) -> Any:
    shape = bd.Box(*size, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)).located(bd.Location(minimum))
    shape.label = label
    return shape


def _cylinder_axis(
    bd: Any,
    radius: float,
    length: float,
    start: tuple[float, float, float],
    axis: str,
    label: str,
) -> Any:
    rotations = {"x": (0.0, 90.0, 0.0), "y": (-90.0, 0.0, 0.0), "z": (0.0, 0.0, 0.0)}
    if axis not in rotations:
        raise ValueError(f"Unsupported cylinder axis: {axis}")
    shape = bd.Cylinder(
        radius,
        length,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    ).located(bd.Location(start, rotations[axis]))
    shape.label = label
    return shape


def _fuse_all(shapes: list[Any]) -> Any:
    if not shapes:
        raise ValueError("A printable part needs at least one solid")
    result = shapes[0]
    for shape in shapes[1:]:
        result = result.fuse(shape)
    return result


def _closed_box(bd: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], wall: float, label: str) -> Any:
    if min(size) <= 2.0 * wall:
        raise ValueError(f"{label}: wall is too large for section")
    outer = _box(bd, size, minimum, f"{label}_outer")
    inner = _box(
        bd,
        tuple(value - 2.0 * wall for value in size),
        tuple(value + wall for value in minimum),
        f"{label}_cavity",
    )
    result = outer.cut(inner)
    result.label = label
    return result


def _bearing_cartridge(bd: Any, label: str, *, outer_x: float = 52.0, outer_y: float = 50.0, outer_z: float = 38.0) -> Any:
    """Build a serviceable Y-axis cartridge with a provisional through-bore."""

    body = _box(bd, (outer_x, outer_y, outer_z), (0.0, 0.0, 0.0), f"{label}_body")
    flange = _box(bd, (outer_x + 4.0, 8.0, outer_z - 6.0), (-2.0, 0.0, 3.0), f"{label}_flange")
    result = _fuse_all([body, flange])
    result = result.cut(_cylinder_axis(bd, 12.0, outer_y + 2.0, (outer_x / 2.0, -1.0, outer_z / 2.0), "y", f"{label}_bearing_bore"))
    result.label = label
    return result


def _build_center_tie(bd: Any) -> Any:
    body = _box(bd, (252.0, 24.0, 30.0), (0.0, 0.0, 0.0), "base_center_tie_body")
    ribs = [
        _box(bd, (252.0, 5.0, 8.0), (0.0, y, 0.0), f"base_center_tie_rib_{index}")
        for index, y in enumerate((5.0, 14.0), start=1)
    ]
    result = _fuse_all([body, *ribs])
    for index, x in enumerate((24.0, 228.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 32.0, (x, 12.0, -1.0), "z", f"base_center_tie_hole_{index}"))
    result.label = "base_center_tie"
    return result


def _build_y_motor_pocket(bd: Any) -> Any:
    body = _closed_box(bd, (70.0, 45.0, 62.0), (0.0, 0.0, 0.0), 5.0, "y_motor_service_pocket")
    plate = _box(bd, (70.0, 8.0, 62.0), (0.0, 0.0, 0.0), "y_motor_face_plate")
    result = _fuse_all([body, plate])
    result = result.cut(_cylinder_axis(bd, 13.0, 10.0, (35.0, -1.0, 31.0), "y", "y_motor_shaft_opening"))
    for index, x in enumerate((14.0, 56.0), start=1):
        for z in (10.0, 52.0):
            result = result.cut(_cylinder_axis(bd, 2.25, 10.0, (x, -1.0, z), "y", f"y_motor_mount_{index}_{z}"))
    result.label = "y_motor_service_pocket"
    return result


def _build_foot(bd: Any, label: str) -> Any:
    body = _box(bd, (50.0, 50.0, 20.0), (0.0, 0.0, 0.0), label)
    cap = _box(bd, (42.0, 42.0, 4.0), (4.0, 4.0, 20.0), f"{label}_cap")
    result = _fuse_all([body, cap])
    result = result.cut(_cylinder_axis(bd, 2.25, 26.0, (25.0, 25.0, -1.0), "z", f"{label}_mount_hole"))
    result.label = label
    return result


def _build_electronics_rail(bd: Any) -> Any:
    body = _box(bd, (220.0, 40.0, 12.0), (0.0, 0.0, 0.0), "electronics_mount_rail_body")
    upper = _box(bd, (200.0, 24.0, 8.0), (10.0, 8.0, 12.0), "electronics_mount_rail_upper")
    result = _fuse_all([body, upper])
    for index, x in enumerate((20.0, 200.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 22.0, (x, 20.0, -1.0), "z", f"electronics_mount_hole_{index}"))
    result.label = "electronics_mount_rail"
    return result


def _build_gantry_left(bd: Any) -> Any:
    tower = _closed_box(bd, (54.0, 70.0, 70.0), (0.0, 0.0, 0.0), 6.0, "gantry_left_tower")
    beam = _closed_box(bd, (172.0, 70.0, 90.0), (0.0, 0.0, 60.0), 6.0, "gantry_left_beam")
    rail_lower = _box(bd, (172.0, 10.0, 14.0), (0.0, 0.0, 70.0), "gantry_left_x_lower_seat")
    rail_upper = _box(bd, (172.0, 10.0, 14.0), (0.0, 0.0, 130.0), "gantry_left_x_upper_seat")
    shoulder = _box(bd, (62.0, 70.0, 8.0), (0.0, 0.0, 52.0), "gantry_left_tower_shoulder")
    tongue = _closed_box(bd, (36.0, 38.0, 50.0), (164.0, 16.0, 84.0), 5.0, "gantry_left_tongue")
    result = _fuse_all([tower, beam, rail_lower, rail_upper, shoulder, tongue])
    result.label = "gantry_left_integrated"
    return result


def _build_gantry_right(bd: Any) -> Any:
    tower = _closed_box(bd, (54.0, 70.0, 70.0), (126.0, 0.0, 0.0), 6.0, "gantry_right_tower")
    beam = _closed_box(bd, (172.0, 70.0, 90.0), (8.0, 0.0, 60.0), 6.0, "gantry_right_beam")
    socket = _box(bd, (24.0, 38.0, 50.0), (8.0, 16.0, 84.0), "gantry_right_tongue_socket")
    beam = beam.cut(socket)
    rail_lower = _box(bd, (172.0, 10.0, 14.0), (8.0, 0.0, 70.0), "gantry_right_x_lower_seat")
    rail_upper = _box(bd, (172.0, 10.0, 14.0), (8.0, 0.0, 130.0), "gantry_right_x_upper_seat")
    shoulder = _box(bd, (62.0, 70.0, 8.0), (118.0, 0.0, 52.0), "gantry_right_tower_shoulder")
    result = _fuse_all([tower, beam, rail_lower, rail_upper, shoulder])
    result.label = "gantry_right_integrated"
    return result


def _build_x_bearing(bd: Any, label: str) -> Any:
    body = _box(bd, (50.0, 70.0, 50.0), (0.0, 0.0, 0.0), f"{label}_body")
    flange = _box(bd, (8.0, 80.0, 42.0), (0.0, -5.0, 4.0), f"{label}_flange")
    result = _fuse_all([body, flange])
    result = result.cut(_cylinder_axis(bd, 12.0, 52.0, (-1.0, 35.0, 25.0), "x", f"{label}_bearing_bore"))
    result.label = label
    return result


def _build_x_z_backbone(bd: Any) -> Any:
    back = _box(bd, (90.0, 14.0, 130.0), (0.0, 0.0, 0.0), "x_z_backbone_backplate")
    left_rib = _closed_box(bd, (16.0, 48.0, 130.0), (0.0, 0.0, 0.0), 4.0, "x_z_backbone_left_rib")
    right_rib = _closed_box(bd, (16.0, 48.0, 130.0), (74.0, 0.0, 0.0), 4.0, "x_z_backbone_right_rib")
    lower = _box(bd, (90.0, 32.0, 14.0), (0.0, 0.0, 0.0), "x_z_backbone_lower_cross_rib")
    upper = _box(bd, (90.0, 32.0, 14.0), (0.0, 0.0, 116.0), "x_z_backbone_upper_cross_rib")
    rail_left = _box(bd, (14.0, 10.0, 130.0), (8.0, 0.0, 0.0), "x_z_backbone_z_left_seat")
    rail_right = _box(bd, (14.0, 10.0, 130.0), (68.0, 0.0, 0.0), "x_z_backbone_z_right_seat")
    ears = [
        _box(bd, (24.0, 30.0, 8.0), (x, 0.0, z), f"x_z_backbone_mount_{index}")
        for index, (x, z) in enumerate(((0.0, 0.0), (66.0, 0.0), (0.0, 122.0), (66.0, 122.0)), start=1)
    ]
    result = _fuse_all([back, left_rib, right_rib, lower, upper, rail_left, rail_right, *ears])
    result.label = "x_z_backbone"
    return result


def _build_z_carriage(bd: Any) -> Any:
    back = _box(bd, (90.0, 12.0, 100.0), (0.0, 0.0, 0.0), "z_carriage_backplate")
    front = _box(bd, (90.0, 12.0, 100.0), (0.0, 68.0, 0.0), "z_carriage_front_interface")
    ribs = [
        _box(bd, (12.0, 56.0, 100.0), (x, 12.0, 0.0), f"z_carriage_side_rib_{index}")
        for index, x in enumerate((0.0, 78.0), start=1)
    ]
    cross = [
        _box(bd, (90.0, 56.0, 10.0), (0.0, 12.0, z), f"z_carriage_cross_rib_{index}")
        for index, z in enumerate((12.0, 45.0, 78.0), start=1)
    ]
    result = _fuse_all([back, front, *ribs, *cross])
    result.label = "z_carriage_plate"
    return result


def _build_spindle_mount(bd: Any) -> Any:
    plate = _box(bd, (90.0, 12.0, 70.0), (0.0, 0.0, 0.0), "spindle_mount_rear_plate")
    lower = bd.Cylinder(32.0, 12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).located(bd.Location((45.0, 35.0, 22.0)))
    upper = bd.Cylinder(32.0, 12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).located(bd.Location((45.0, 35.0, 48.0)))
    bore_lower = bd.Cylinder(26.0, 14.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).located(bd.Location((45.0, 35.0, 21.0)))
    bore_upper = bd.Cylinder(26.0, 14.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).located(bd.Location((45.0, 35.0, 47.0)))
    rings = lower.cut(bore_lower).fuse(upper.cut(bore_upper))
    ears = [
        _box(bd, (12.0, 18.0, 18.0), (5.0, 8.0, z), f"spindle_mount_ear_{index}")
        for index, z in enumerate((16.0, 48.0), start=1)
    ]
    result = _fuse_all([plate, rings, *ears])
    result = result.cut(_cylinder_axis(bd, 2.25, 22.0, (10.0, -1.0, 31.0), "y", "spindle_mount_clamp_slot"))
    result.label = "spindle_mount_concept"
    return result


def _build_moving_bed(bd: Any) -> Any:
    width, depth = 240.0, 180.0
    front = _box(bd, (width, 14.0, 20.0), (0.0, 0.0, 0.0), "moving_bed_front_beam")
    rear = _box(bd, (width, 14.0, 20.0), (0.0, depth - 14.0, 0.0), "moving_bed_rear_beam")
    left = _box(bd, (14.0, depth - 28.0, 20.0), (0.0, 14.0, 0.0), "moving_bed_left_beam")
    right = _box(bd, (14.0, depth - 28.0, 20.0), (width - 14.0, 14.0, 0.0), "moving_bed_right_beam")
    skin = _box(bd, (width - 28.0, depth - 28.0, 5.0), (14.0, 14.0, 15.0), "moving_bed_datum_skin")
    ribs = [
        _box(bd, (width - 28.0, 8.0, 15.0), (14.0, y, 0.0), f"moving_bed_cross_rib_{index}")
        for index, y in enumerate((42.0, 86.0, 130.0), start=1)
    ]
    nut_boss = _box(bd, (52.0, 50.0, 12.0), (94.0, 65.0, 0.0), "moving_bed_y_nut_boss")
    carriage_pads = [
        _box(bd, (24.0, 30.0, 6.0), (x, y, 20.0), f"moving_bed_carriage_pad_{index}")
        for index, (x, y) in enumerate(((0.0, 36.0), (216.0, 36.0), (0.0, 114.0), (216.0, 114.0)), start=1)
    ]
    result = _fuse_all([front, rear, left, right, skin, *ribs, nut_boss, *carriage_pads])
    for index, (x, y) in enumerate(((12.0, 51.0), (228.0, 51.0), (12.0, 129.0), (228.0, 129.0)), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 28.0, (x, y, -1.0), "z", f"moving_bed_carriage_hole_{index}"))
    result.label = "moving_bed_frame"
    return result


def build_phase5_complete_structural_parts() -> dict[str, Any]:
    """Return all 19 actual local printable solids keyed by stable part ID."""

    bd = _build123d()
    parts = dict(build_phase5_base_pair())
    parts.update(
        {
            "base_center_tie": _build_center_tie(bd),
            "y_motor_service_pocket": _build_y_motor_pocket(bd),
            "y_fixed_bearing_cartridge": _bearing_cartridge(bd, "y_fixed_bearing_cartridge"),
            "y_floating_bearing_cartridge": _bearing_cartridge(bd, "y_floating_bearing_cartridge", outer_z=34.0),
            "machine_foot_front_left": _build_foot(bd, "machine_foot_front_left"),
            "machine_foot_front_right": _build_foot(bd, "machine_foot_front_right"),
            "machine_foot_rear_left": _build_foot(bd, "machine_foot_rear_left"),
            "machine_foot_rear_right": _build_foot(bd, "machine_foot_rear_right"),
            "electronics_mount_rail": _build_electronics_rail(bd),
            "gantry_left_integrated": _build_gantry_left(bd),
            "gantry_right_integrated": _build_gantry_right(bd),
            "x_fixed_bearing_cartridge": _build_x_bearing(bd, "x_fixed_bearing_cartridge"),
            "x_floating_bearing_cartridge": _build_x_bearing(bd, "x_floating_bearing_cartridge"),
            "x_z_backbone": _build_x_z_backbone(bd),
            "z_carriage_plate": _build_z_carriage(bd),
            "spindle_mount_concept": _build_spindle_mount(bd),
            "moving_bed_frame": _build_moving_bed(bd),
        }
    )
    missing = [part_id for part_id in PHASE5_COMPLETE_PART_IDS if part_id not in parts]
    extra = [part_id for part_id in parts if part_id not in PHASE5_COMPLETE_PART_IDS]
    if missing or extra:
        raise RuntimeError(f"Complete structural part contract mismatch: missing={missing}, extra={extra}")
    return {part_id: parts[part_id] for part_id in PHASE5_COMPLETE_PART_IDS}


__all__ = [
    "PHASE5_COMPLETE_PART_DEFINITIONS",
    "PHASE5_COMPLETE_PART_IDS",
    "Phase5PartDefinition",
    "build_phase5_complete_structural_parts",
]
