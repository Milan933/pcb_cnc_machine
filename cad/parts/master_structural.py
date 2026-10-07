"""Coherent PETG structure derived from the Phase 5 master hardware layout.

The master machine is laid out first in ``cad.assembly.master_machine``.  The
parts below are split from that structural body at load-path and service
boundaries.  Their local geometry contains rail seats, shoulders, ribs,
fastener clearances, and replaceable-interface provisions; it is not a set of
post-hoc visual blocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cad.parameters import PHASE5_MASTER_PARAMETERS


MASTER_PART_IDS = (
    "base_left_integrated",
    "base_right_integrated",
    "base_center_tie",
    "y_motor_service_pocket",
    "y_fixed_bearing_cartridge",
    "y_floating_bearing_cartridge",
    "y_rear_bearing_bridge",
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
class MasterPartDefinition:
    """Review inventory metadata for one derived PETG part."""

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
    orientation: str = "broad datum face on the Voron bed; Z is print-up",
    support: str = "No support preferred; validate bridges, use brim only after calibration",
    critical: bool = False,
    notes: str = "",
) -> MasterPartDefinition:
    return MasterPartDefinition(
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


MASTER_PART_DEFINITIONS = (
    _definition(1, "base_left_integrated", "left base side derived around Y rail, foot, and gantry datums", critical=True, notes="320 mm Y extent is a conditional Voron print; the master machine requires the full 310 mm Y rail envelope."),
    _definition(2, "base_right_integrated", "right base side derived around Y rail, foot, and gantry datums", critical=True, notes="Mirrored split of the coherent base side; verify rail shoulder and printed datum after measurement."),
    _definition(3, "base_center_tie", "indexed base shear tie joining the two Y support bodies", critical=True, notes="M4 preload is not the locating feature; end shoulders and mating faces carry shear."),
    _definition(4, "y_motor_service_pocket", "Y drive service block with NEMA17 and fixed-bearing interfaces", notes="Motor body length and coupler access remain owner-stock dependent."),
    _definition(5, "y_fixed_bearing_cartridge", "Y drive-end fixed bearing housing", notes="Two-bearing axial location is represented by the master architecture; exact retainers remain provisional."),
    _definition(6, "y_floating_bearing_cartridge", "Y far-end radial/floating bearing housing", notes="Axial float is intentional and must not be closed by PETG preload."),
    _definition(7, "y_rear_bearing_bridge", "rear Y floating-bearing bridge anchored to the left base side", critical=True, notes="Dedicated printed support for the floating bearing; not a text-only support claim."),
    _definition(8, "machine_foot_front_left", "front-left support foot and through-fastener interface"),
    _definition(9, "machine_foot_front_right", "front-right support foot and through-fastener interface"),
    _definition(10, "machine_foot_rear_left", "rear-left support foot and through-fastener interface"),
    _definition(11, "machine_foot_rear_right", "rear-right support foot and through-fastener interface"),
    _definition(12, "electronics_mount_rail", "rear electronics bracket with controller, airflow, and cable-service datums", notes="Arduino Mega is dimensionally derived; CNC Shield footprint remains flexible until identified."),
    _definition(13, "gantry_left_integrated", "left fixed gantry tower and keyed X-beam half", critical=True, orientation="tower base on the broad datum; inspect keyed beam joint and rail seats", notes="The beam tongue is a shear feature; M4 fasteners provide clamp preload."),
    _definition(14, "gantry_right_integrated", "right fixed gantry tower and keyed X-beam half", critical=True, orientation="tower base on the broad datum; inspect keyed beam socket and rail seats", notes="The beam socket is deliberately derived after the master span was established."),
    _definition(15, "x_fixed_bearing_cartridge", "X drive-end fixed bearing housing and motor service interface", notes="Motor, coupler, journal, and bearing are represented as separable master components."),
    _definition(16, "x_floating_bearing_cartridge", "X far-end floating bearing housing", notes="Radial support only; preserve axial float and service access."),
    _definition(17, "x_z_backbone", "moving X/Z backbone derived around four X carriages and two Z rails", critical=True, orientation="rear/back datum on bed; preserve rail seats and carriage fastener access", notes="The Z guide plane and spindle clamp plane are one master force loop."),
    _definition(18, "z_carriage_plate", "moving Z carriage frame derived around MGN9H blocks and replaceable clamp module", critical=True, orientation="rear datum on bed; clamp interface faces remain accessible", notes="The spindle clamp is replaceable without redesigning the Z guide plate."),
    _definition(19, "spindle_mount_concept", "replaceable standard Z-carriage spindle-clamp module", critical=True, orientation="rear plate on the bed; ring bores print-up and are reamed/inspected after printing", notes="45 mm SycoTec 5045 AC-ER11 candidate is represented; 25/40/52 mm clamp variants remain supported."),
    _definition(20, "moving_bed_frame", "ribbed moving Y bed derived around carriages, nut, spoilboard, PCB, and probe", critical=True, notes="The bed is a machine-level moving member; workholding and cable provisions are not decorative."),
)


def _build123d() -> Any:
    try:
        import build123d
    except ImportError as exc:  # pragma: no cover - CAD runner only
        raise RuntimeError("Master structural geometry requires build123d.") from exc
    return build123d


def _box(bd: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], label: str) -> Any:
    shape = bd.Box(*size, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)).located(bd.Location(minimum))
    shape.label = label
    return shape


def _cylinder_axis(bd: Any, radius: float, length: float, start: tuple[float, float, float], axis: str, label: str) -> Any:
    rotations = {"x": (0.0, 90.0, 0.0), "y": (-90.0, 0.0, 0.0), "z": (0.0, 0.0, 0.0)}
    shape = bd.Cylinder(radius, length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).located(bd.Location(start, rotations[axis]))
    shape.label = label
    return shape


def _fuse_all(shapes: list[Any]) -> Any:
    if not shapes:
        raise ValueError("A structural part needs at least one solid.")
    result = shapes[0]
    for shape in shapes[1:]:
        result = result.fuse(shape)
    return result


def _closed_box(bd: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], wall: float, label: str) -> Any:
    outer = _box(bd, size, minimum, f"{label}_outer")
    inner = _box(bd, tuple(value - 2.0 * wall for value in size), tuple(value + wall for value in minimum), f"{label}_inner")
    result = outer.cut(inner)
    result.label = label
    return result


def _build_base_left(bd: Any) -> Any:
    p = PHASE5_MASTER_PARAMETERS
    w, length, height = p.base_side_width_mm, p.base_length_mm, p.base_side_height_mm
    floor = _box(bd, (w, length, 14.0), (0.0, 0.0, 0.0), "base_floor")
    outer_wall = _box(bd, (18.0, length, height), (0.0, 0.0, 0.0), "base_outer_wall")
    rail_deck = _box(bd, (34.0, length, 10.0), (38.0, 0.0, 42.0), "base_y_rail_deck")
    rail_shoulder = _box(bd, (4.0, length, 6.0), (38.0, 0.0, 52.0), "base_y_rail_shoulder")
    inner_web = _box(bd, (10.0, length, 35.0), (24.0, 0.0, 14.0), "base_inner_web")
    ribs = [_box(bd, (54.0, 12.0, 30.0), (12.0, y, 14.0), f"base_cross_rib_{index}") for index, y in enumerate((24.0, 96.0, 168.0, 240.0, 284.0), start=1)]
    end_walls = [_box(bd, (w, 18.0, 30.0), (0.0, y, 14.0), f"base_end_wall_{index}") for index, y in enumerate((0.0, length - 18.0), start=1)]
    tie_land = _box(bd, (28.0, 36.0, 16.0), (58.0, 142.0, 14.0), "base_center_tie_land")
    result = _fuse_all([floor, outer_wall, rail_deck, rail_shoulder, inner_web, *ribs, *end_walls, tie_land])
    # Representative M4 foot and center-tie clearances.  They are clearance
    # holes, not precision locating pins.
    for index, (x, y) in enumerate(((12.0, 20.0), (12.0, length - 20.0), (66.0, 160.0)), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, height + 2.0, (x, y, -1.0), "z", f"base_m4_clearance_{index}"))
    result.label = "base_left_integrated"
    return result


def build_base_side(side: str) -> Any:
    bd = _build123d()
    left = _build_base_left(bd)
    if side == "left":
        result = left
    elif side == "right":
        result = bd.mirror(left, about=bd.Plane(origin=(PHASE5_MASTER_PARAMETERS.base_side_width_mm / 2.0, 0.0, 0.0), z_dir=(1.0, 0.0, 0.0)))
    else:
        raise ValueError(f"Unknown base side {side!r}")
    result.label = f"base_{side}_integrated"
    return result


def _build_center_tie(bd: Any) -> Any:
    body = _box(bd, (260.0, 28.0, 20.0), (0.0, 0.0, 0.0), "base_center_tie_body")
    upper = _box(bd, (220.0, 16.0, 12.0), (20.0, 6.0, 20.0), "base_center_tie_upper")
    end_keys = [_box(bd, (28.0, 36.0, 12.0), (index, -4.0, 4.0), f"base_center_tie_key_{index}") for index in (0.0, 232.0)]
    result = _fuse_all([body, upper, *end_keys])
    for index, x in enumerate((20.0, 240.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 34.0, (x, 14.0, -1.0), "z", f"base_center_tie_hole_{index}"))
    result.label = "base_center_tie"
    return result


def _build_y_motor_service_pocket(bd: Any) -> Any:
    body = _closed_box(bd, (60.0, 50.0, 65.0), (0.0, 0.0, 0.0), 6.0, "y_motor_service_body")
    face = _box(bd, (60.0, 8.0, 65.0), (0.0, 42.0, 0.0), "y_motor_face")
    bearing_land = _box(bd, (48.0, 12.0, 36.0), (6.0, 8.0, 25.0), "y_fixed_bearing_land")
    result = _fuse_all([body, face, bearing_land])
    result = result.cut(_cylinder_axis(bd, 11.0, 54.0, (30.0, -2.0, 50.0), "y", "y_screw_passage"))
    result = result.cut(_cylinder_axis(bd, 13.0, 10.0, (30.0, 41.0, 50.0), "y", "y_motor_shaft_clearance"))
    for index, (x, z) in enumerate(((14.0, 13.0), (46.0, 13.0), (14.0, 52.0), (46.0, 52.0)), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 10.0, (x, 41.0, z), "y", f"y_motor_m4_{index}"))
    result.label = "y_motor_service_pocket"
    return result


def _build_bearing_cartridge(bd: Any, label: str, *, floating: bool = False, low_profile: bool = False) -> Any:
    if low_profile:
        body_height = 18.0 if not floating else 16.0
        flange_height = 14.0
        bore_z = 9.0 if not floating else 8.0
        rib_z = 12.0 if not floating else 10.0
        rib_height = 6.0
    else:
        body_height = 42.0 if not floating else 36.0
        flange_height = 34.0
        bore_z = 21.0 if not floating else 18.0
        rib_z = 34.0 if not floating else 28.0
        rib_height = 8.0
    body = _box(bd, (52.0, 34.0, body_height), (0.0, 0.0, 0.0), f"{label}_body")
    flange = _box(bd, (60.0, 10.0, flange_height), (-4.0, 0.0, 2.0), f"{label}_flange")
    rib = _box(bd, (44.0, 28.0, rib_height), (4.0, 6.0, rib_z), f"{label}_top_rib")
    result = _fuse_all([body, flange, rib])
    # A blind, retained pocket keeps the low Y cartridge one printable solid;
    # the final through-bore/retainer depth is still driven by the measured
    # bearing stack.
    bore_start = 7.0 if low_profile else -1.0
    bore_length = 20.0 if low_profile else 36.0
    result = result.cut(_cylinder_axis(bd, 11.0, bore_length, (26.0, bore_start, bore_z), "y", f"{label}_bearing_bore"))
    for index, x in enumerate((8.0, 44.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 12.0, (x, -1.0, 8.0), "y", f"{label}_mount_{index}"))
    result.label = label
    return result


def _build_y_rear_bearing_bridge(bd: Any) -> Any:
    bridge = _box(bd, (160.0, 40.0, 32.0), (0.0, 0.0, 0.0), "y_rear_bearing_bridge_body")
    # The bridge top is kept below the moving-bed bottom datum (-40 mm);
    # bearing support must not become a hidden Y-end collision.
    result = bridge
    for index, x in enumerate((12.0, 148.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 20.0, (x, 20.0, -1.0), "z", f"y_rear_bridge_m4_{index}"))
    result.label = "y_rear_bearing_bridge"
    return result


def _build_foot(bd: Any, label: str) -> Any:
    body = _box(bd, (50.0, 50.0, 20.0), (0.0, 0.0, 0.0), label)
    cap = _box(bd, (42.0, 42.0, 6.0), (4.0, 4.0, 20.0), f"{label}_cap")
    result = _fuse_all([body, cap]).cut(_cylinder_axis(bd, 2.25, 28.0, (25.0, 25.0, -1.0), "z", f"{label}_through_bolt"))
    result.label = label
    return result


def _build_electronics_mount(bd: Any) -> Any:
    rail = _box(bd, (260.0, 50.0, 14.0), (0.0, 0.0, 0.0), "electronics_rail_body")
    upper = _box(bd, (230.0, 38.0, 8.0), (15.0, 6.0, 14.0), "electronics_rail_upper")
    side_rib = _box(bd, (10.0, 50.0, 30.0), (0.0, 0.0, 0.0), "electronics_service_rib")
    # Rear standoffs land on the two side-base bodies.  The electronics deck
    # is deliberately above the Y floating-bearing envelope, while the
    # standoffs preserve a positive load path back into the base pair.
    standoffs = [
        _box(bd, (20.0, 10.0, 12.0), (x, 0.0, -12.0), f"electronics_rear_standoff_{index}")
        for index, x in enumerate((0.0, 240.0), start=1)
    ]
    result = _fuse_all([rail, upper, side_rib, *standoffs])
    for index, x in enumerate((20.0, 240.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 24.0, (x, 25.0, -1.0), "z", f"electronics_mount_m4_{index}"))
    result.label = "electronics_mount_rail"
    return result


def _build_gantry(bd: Any, side: str) -> Any:
    # Each half was sized after the 340 mm X rail span was placed.  The left
    # half carries a tongue and the right half carries its matching socket.
    # The X beam is behind the moving X/Z assembly in +Y.  Its local rear
    # datum is -65 mm so the placed beam occupies global Y=-95..-35 mm;
    # this leaves the spindle body and clamp service space in front of it.
    beam_y = -65.0
    tower = _box(bd, (55.0, 60.0, 250.0), ((0.0 if side == "left" else 150.0), beam_y, 0.0), f"gantry_{side}_tower")
    beam = _box(bd, (170.0, 60.0, 60.0), ((35.0 if side == "left" else 30.0), beam_y, 150.0), f"gantry_{side}_beam_half")
    gusset = _box(bd, (76.0, 60.0, 34.0), ((28.0 if side == "left" else 124.0), beam_y, 120.0), f"gantry_{side}_gusset")
    rail_seats = [
        _box(bd, (170.0, 14.0, 12.0), ((35.0 if side == "left" else 30.0), beam_y, z), f"gantry_{side}_x_rail_seat_{index}")
        for index, z in enumerate((150.0, 190.0), start=1)
    ]
    if side == "left":
        joint = _box(bd, (30.0, 32.0, 50.0), (175.0, beam_y + 14.0, 165.0), "gantry_left_beam_tongue")
        result = _fuse_all([tower, beam, gusset, *rail_seats, joint])
    else:
        socket = _box(bd, (30.0, 32.0, 50.0), (30.0, beam_y + 14.0, 165.0), "gantry_right_beam_socket")
        result = _fuse_all([tower, beam, gusset, *rail_seats]).cut(socket)
    # Tower-to-base clearance holes remain provisional M4 interfaces.
    for index, x in enumerate(((16.0 if side == "left" else 166.0), (42.0 if side == "left" else 192.0)), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 16.0, (x, 15.0, -1.0), "z", f"gantry_{side}_base_m4_{index}"))
    result.label = f"gantry_{side}_integrated"
    return result


def _build_x_bearing(bd: Any, label: str) -> Any:
    body = _box(bd, (55.0, 70.0, 58.0), (0.0, 0.0, 0.0), f"{label}_body")
    flange = _box(bd, (10.0, 82.0, 44.0), (0.0, -6.0, 7.0), f"{label}_flange")
    top = _box(bd, (45.0, 52.0, 8.0), (5.0, 9.0, 50.0), f"{label}_top_rib")
    result = _fuse_all([body, flange, top]).cut(_cylinder_axis(bd, 11.0, 57.0, (-1.0, 35.0, 29.0), "x", f"{label}_bearing_bore"))
    for index, y in enumerate((12.0, 58.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 12.0, (-1.0, y, 10.0), "x", f"{label}_mount_{index}"))
    result.label = label
    return result


def _build_x_z_backbone(bd: Any) -> Any:
    back = _box(bd, (115.0, 12.0, 125.0), (0.0, 0.0, 0.0), "x_z_backbone_backplate")
    upper = _box(bd, (115.0, 42.0, 12.0), (0.0, 12.0, 105.0), "x_z_backbone_upper_crossrib")
    lower = _box(bd, (115.0, 42.0, 12.0), (0.0, 12.0, 5.0), "x_z_backbone_lower_crossrib")
    side_ribs = [_box(bd, (12.0, 42.0, 125.0), (x, 12.0, 0.0), f"x_z_backbone_side_rib_{index}") for index, x in enumerate((0.0, 103.0), start=1)]
    z_seats = [_box(bd, (16.0, 12.0, 125.0), (x, -1.0, 0.0), f"x_z_backbone_z_rail_seat_{index}") for index, x in enumerate((17.0, 77.0), start=1)]
    # The Z screw/motor datum is on the front side of the moving backbone;
    # the fixed X beam remains behind the X guide plane and cannot sweep into
    # the motor body at either X travel extreme.
    motor_land = _box(bd, (52.0, 20.0, 52.0), (31.5, 42.0, 62.0), "x_z_backbone_z_motor_land")
    result = _fuse_all([back, upper, lower, *side_ribs, *z_seats, motor_land])
    for index, x in enumerate((12.0, 103.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 14.0, (x, -1.0, 20.0), "y", f"x_z_backbone_z_mount_{index}"))
    result.label = "x_z_backbone"
    return result


def _build_z_carriage(bd: Any) -> Any:
    back = _box(bd, (105.0, 12.0, 120.0), (0.0, 0.0, 0.0), "z_carriage_backplate")
    front = _box(bd, (105.0, 12.0, 120.0), (0.0, 53.0, 0.0), "z_carriage_front_plate")
    side_ribs = [_box(bd, (12.0, 41.0, 120.0), (x, 12.0, 0.0), f"z_carriage_side_rib_{index}") for index, x in enumerate((0.0, 93.0), start=1)]
    cross_ribs = [_box(bd, (105.0, 41.0, 10.0), (0.0, 12.0, z), f"z_carriage_cross_rib_{index}") for index, z in enumerate((12.0, 55.0, 98.0), start=1)]
    clamp_land = _box(bd, (105.0, 34.0, 16.0), (0.0, 12.0, 42.0), "z_carriage_clamp_land")
    result = _fuse_all([back, front, *side_ribs, *cross_ribs, clamp_land])
    for index, x in enumerate((14.0, 91.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 14.0, (x, -1.0, 20.0), "y", f"z_carriage_rail_mount_{index}"))
    result.label = "z_carriage_plate"
    return result


def _build_spindle_mount(bd: Any) -> Any:
    p = PHASE5_MASTER_PARAMETERS
    plate = _box(bd, (105.0, 12.0, 115.0), (0.0, 0.0, 0.0), "spindle_clamp_rear_plate")
    ring_outer = 31.0
    ring_inner = p.spindle_candidate_diameter_mm / 2.0 + 0.6
    rings: list[Any] = []
    for index, z in enumerate((22.0, 82.0), start=1):
        outer = _cylinder_axis(bd, ring_outer, 10.0, (52.5, 35.0, z), "z", f"spindle_clamp_ring_{index}")
        inner = _cylinder_axis(bd, ring_inner, 12.0, (52.5, 35.0, z - 1.0), "z", f"spindle_clamp_bore_{index}")
        rings.append(outer.cut(inner))
    bridge = _box(bd, (18.0, 35.0, 115.0), (43.5, 0.0, 0.0), "spindle_clamp_bridge")
    result = _fuse_all([plate, bridge, *rings])
    for index, z in enumerate((27.0, 87.0), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 14.0, (9.0, -1.0, z), "y", f"spindle_clamp_m4_{index}"))
    result.label = "spindle_mount_concept"
    return result


def _build_moving_bed(bd: Any) -> Any:
    width, depth = 240.0, 230.0
    front = _box(bd, (width, 16.0, 28.0), (0.0, 0.0, 0.0), "moving_bed_front_beam")
    rear = _box(bd, (width, 16.0, 28.0), (0.0, depth - 16.0, 0.0), "moving_bed_rear_beam")
    left = _box(bd, (16.0, depth - 32.0, 28.0), (0.0, 16.0, 0.0), "moving_bed_left_beam")
    right = _box(bd, (16.0, depth - 32.0, 28.0), (width - 16.0, 16.0, 0.0), "moving_bed_right_beam")
    skin = _box(bd, (width - 32.0, depth - 32.0, 6.0), (16.0, 16.0, 22.0), "moving_bed_datum_skin")
    ribs = [_box(bd, (width - 32.0, 10.0, 18.0), (16.0, y, 4.0), f"moving_bed_cross_rib_{index}") for index, y in enumerate((48.0, 94.0, 140.0, 186.0), start=1)]
    nut_boss = _box(bd, (52.0, 50.0, 18.0), (94.0, 90.0, 0.0), "moving_bed_y_nut_boss")
    pads = [_box(bd, (28.0, 34.0, 8.0), (x, y, 26.0), f"moving_bed_carriage_pad_{index}") for index, (x, y) in enumerate(((0.0, 32.0), (212.0, 32.0), (0.0, 164.0), (212.0, 164.0)), start=1)]
    result = _fuse_all([front, rear, left, right, skin, *ribs, nut_boss, *pads])
    for index, (x, y) in enumerate(((10.0, 48.0), (230.0, 48.0), (10.0, 182.0), (230.0, 182.0)), start=1):
        result = result.cut(_cylinder_axis(bd, 2.25, 36.0, (x, y, -1.0), "z", f"moving_bed_carriage_m4_{index}"))
    result.label = "moving_bed_frame"
    return result


def build_master_structural_parts() -> dict[str, Any]:
    """Build the derived local PETG solids from the master hardware layout."""

    bd = _build123d()
    parts = {
        "base_left_integrated": build_base_side("left"),
        "base_right_integrated": build_base_side("right"),
        "base_center_tie": _build_center_tie(bd),
        "y_motor_service_pocket": _build_y_motor_service_pocket(bd),
        "y_fixed_bearing_cartridge": _build_bearing_cartridge(bd, "y_fixed_bearing_cartridge", low_profile=True),
        "y_floating_bearing_cartridge": _build_bearing_cartridge(bd, "y_floating_bearing_cartridge", floating=True, low_profile=True),
        "y_rear_bearing_bridge": _build_y_rear_bearing_bridge(bd),
        "machine_foot_front_left": _build_foot(bd, "machine_foot_front_left"),
        "machine_foot_front_right": _build_foot(bd, "machine_foot_front_right"),
        "machine_foot_rear_left": _build_foot(bd, "machine_foot_rear_left"),
        "machine_foot_rear_right": _build_foot(bd, "machine_foot_rear_right"),
        "electronics_mount_rail": _build_electronics_mount(bd),
        "gantry_left_integrated": _build_gantry(bd, "left"),
        "gantry_right_integrated": _build_gantry(bd, "right"),
        "x_fixed_bearing_cartridge": _build_x_bearing(bd, "x_fixed_bearing_cartridge"),
        "x_floating_bearing_cartridge": _build_x_bearing(bd, "x_floating_bearing_cartridge"),
        "x_z_backbone": _build_x_z_backbone(bd),
        "z_carriage_plate": _build_z_carriage(bd),
        "spindle_mount_concept": _build_spindle_mount(bd),
        "moving_bed_frame": _build_moving_bed(bd),
    }
    if set(parts) != set(MASTER_PART_IDS):
        raise RuntimeError(f"Master structural inventory mismatch: {sorted(set(MASTER_PART_IDS) ^ set(parts))}")
    return {part_id: parts[part_id] for part_id in MASTER_PART_IDS}


__all__ = [
    "MASTER_PART_DEFINITIONS",
    "MASTER_PART_IDS",
    "MasterPartDefinition",
    "build_base_side",
    "build_master_structural_parts",
]
