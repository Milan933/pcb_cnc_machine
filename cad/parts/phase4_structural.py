"""Parametric preliminary PETG structural parts for the accepted P2 baseline.

The builders intentionally create review geometry rather than manufacturing
parts. They expose load-path concepts, indexed joints, rail-seat pads, service
cartridges, and print-size boundaries while keeping supplier-dependent holes
and insert pockets unresolved.
"""

from __future__ import annotations

from typing import Any

from cad.assembly.architecture_skeleton import SkeletonComponent
from cad.parameters import (
    PHASE4_STRUCTURAL_PARAMETERS,
    Phase4PrintPartParameter,
)


def _build123d() -> Any:
    try:
        import build123d
    except ImportError as exc:  # pragma: no cover - exercised by CAD runner
        raise RuntimeError(
            "Phase 4 structural review geometry requires build123d. Install "
            "the pinned dependency from requirements/cad-phase-2.txt."
        ) from exc
    return build123d


def _box(build123d: Any, name: str, size: tuple[float, float, float], minimum: tuple[float, float, float]) -> Any:
    shape = build123d.Box(
        *size,
        align=(build123d.Align.MIN, build123d.Align.MIN, build123d.Align.MIN),
    ).located(build123d.Location(minimum))
    shape.label = name
    return shape


def _cylinder(
    build123d: Any,
    name: str,
    radius: float,
    height: float,
    minimum: tuple[float, float, float],
) -> Any:
    shape = build123d.Cylinder(
        radius,
        height,
        align=(build123d.Align.CENTER, build123d.Align.CENTER, build123d.Align.MIN),
    ).located(build123d.Location(minimum))
    shape.label = name
    return shape


def _closed_box(
    build123d: Any,
    name: str,
    size: tuple[float, float, float],
    minimum: tuple[float, float, float],
    wall_mm: float = 6.0,
) -> Any:
    """Create a closed printed box section with a preliminary wall screen."""

    if min(size) <= 2.0 * wall_mm:
        raise ValueError(f"{name} is too small for a {wall_mm} mm closed-section wall.")
    outer = _box(build123d, f"{name}_outer", size, minimum)
    inner_size = tuple(value - 2.0 * wall_mm for value in size)
    inner_minimum = tuple(value + wall_mm for value in minimum)
    inner = _box(build123d, f"{name}_inner", inner_size, inner_minimum)
    result = outer.cut(inner)
    result.label = name
    return result


def _compound(build123d: Any, name: str, shapes: list[Any]) -> Any:
    result = build123d.Compound(children=shapes)
    result.label = name
    return result


def _part(
    build123d: Any,
    parameter: Phase4PrintPartParameter,
    shape: Any,
    extra_notes: str = "",
) -> SkeletonComponent:
    shape.label = parameter.part_id
    notes = (
        f"PRELIMINARY Phase 4 structural PETG concept; {parameter.role}. "
        f"Print orientation: {parameter.print_orientation}. "
        f"Support: {parameter.support_requirement} Brim: {parameter.brim_requirement}. "
        f"Warping: {parameter.warping_risk}. Layer/load concern: {parameter.layer_load_concern}. "
        f"{parameter.notes} {extra_notes}"
    )
    return SkeletonComponent(
        name=parameter.part_id,
        category="structural",
        shape=shape,
        notes=notes,
    )


def _parameter(part_id: str) -> Phase4PrintPartParameter:
    for parameter in PHASE4_STRUCTURAL_PARAMETERS.print_parts:
        if parameter.part_id == part_id:
            return parameter
    raise KeyError(f"Unknown Phase 4 structural part: {part_id}")


def _base_part_shapes(build123d: Any) -> dict[str, Any]:
    shapes: dict[str, Any] = {}
    for part_id, minimum in (
        ("base_front_left", (-174.0, -150.0, -56.0)),
        ("base_front_right", (24.0, -150.0, -56.0)),
        ("base_rear_left", (-174.0, 118.0, -56.0)),
        ("base_rear_right", (24.0, 118.0, -56.0)),
    ):
        shapes[part_id] = _closed_box(build123d, part_id, (150.0, 32.0, 36.0), minimum)
    shapes["base_left_side_member"] = _closed_box(
        build123d, "base_left_side_member", (48.0, 236.0, 36.0), (-174.0, -118.0, -56.0)
    )
    shapes["base_right_side_member"] = _closed_box(
        build123d, "base_right_side_member", (48.0, 236.0, 36.0), (126.0, -118.0, -56.0)
    )
    for part_id, x in (("base_y_rail_carrier_left", -124.0), ("base_y_rail_carrier_right", 96.0)):
        # The carrier top is aligned to the P2 MGN12 rail screen
        # (centre -14 mm, rail envelope height 2.5 mm).  The extra height
        # below the datum is a printed load-spreading web, not a raw-PETG
        # precision surface.
        pad = _box(build123d, f"{part_id}_pad", (28.0, 300.0, 16.0), (x, -150.0, -31.25))
        rib_a = _box(build123d, f"{part_id}_rib_front", (28.0, 18.0, 22.0), (x, -150.0, -37.25))
        rib_b = _box(build123d, f"{part_id}_rib_rear", (28.0, 18.0, 22.0), (x, 132.0, -37.25))
        shapes[part_id] = _compound(build123d, part_id, [pad, rib_a, rib_b])
    center_tie = _closed_box(
        build123d, "base_center_tie", (252.0, 24.0, 30.0), (-126.0, -12.0, -50.0)
    )
    # Leave a documented service relief around the centered Y nut and screw.
    # The lower wall remains a transverse base tie while the moving nut boss
    # cannot collide with the fixed member during the full Y sweep.
    center_relief = _box(build123d, "base_center_tie_nut_relief", (60.0, 40.0, 20.0), (-30.0, -20.0, -35.0))
    shapes["base_center_tie"] = center_tie.cut(center_relief)
    shapes["base_center_tie"].label = "base_center_tie"
    shapes["y_motor_service_pocket"] = _closed_box(
        build123d, "y_motor_service_pocket", (70.0, 38.0, 40.0), (-35.0, -178.0, -52.0), 5.0
    )
    shapes["y_fixed_bearing_cartridge"] = _closed_box(
        build123d, "y_fixed_bearing_cartridge", (52.0, 40.0, 38.0), (-26.0, -174.0, -48.0), 5.0
    )
    shapes["y_floating_bearing_cartridge"] = _closed_box(
        build123d, "y_floating_bearing_cartridge", (52.0, 40.0, 34.0), (-26.0, 134.0, -46.0), 5.0
    )
    for part_id, minimum in (
        ("machine_foot_front_left", (-174.0, -150.0, -56.0)),
        ("machine_foot_front_right", (134.0, -150.0, -56.0)),
        ("machine_foot_rear_left", (-174.0, 110.0, -56.0)),
        ("machine_foot_rear_right", (134.0, 110.0, -56.0)),
    ):
        shapes[part_id] = _box(build123d, part_id, (40.0, 40.0, 15.0), minimum)
    shapes["electronics_mount_rail"] = _closed_box(
        build123d, "electronics_mount_rail", (180.0, 20.0, 20.0), (-90.0, 150.0, -10.0), 4.0
    )
    return shapes


def _gantry_part_shapes(build123d: Any) -> dict[str, Any]:
    shapes: dict[str, Any] = {}
    tower_width = PHASE4_STRUCTURAL_PARAMETERS.gantry_tower_width_mm
    for part_id, center_x in zip(
        ("gantry_tower_left", "gantry_tower_right"),
        PHASE4_STRUCTURAL_PARAMETERS.gantry_tower_x_centers_mm,
    ):
        x = center_x - tower_width / 2.0
        outer = _box(build123d, f"{part_id}_outer", (tower_width, 90.0, 62.0), (x, -10.0, -20.0))
        cavity = _box(build123d, f"{part_id}_cavity", (tower_width - 24.0, 66.0, 50.0), (x + 12.0, 2.0, -14.0))
        shoulder = _box(build123d, f"{part_id}_shoulder", (tower_width, 90.0, 8.0), (x, -10.0, 34.0))
        shapes[part_id] = _compound(build123d, part_id, [outer.cut(cavity), shoulder])

    left_main = _closed_box(build123d, "gantry_beam_left_main", (172.0, 90.0, 90.0), (-172.0, -10.0, 42.0))
    left_tongue = _box(build123d, "gantry_beam_left_tongue", (8.0, 40.0, 60.0), (0.0, 15.0, 57.0))
    right_main = _closed_box(build123d, "gantry_beam_right_main", (172.0, 90.0, 90.0), (0.0, -10.0, 42.0))
    right_groove = _box(build123d, "gantry_beam_right_groove", (8.0, 40.0, 60.0), (0.0, 15.0, 57.0))
    left_pads = [
        _box(build123d, "gantry_beam_left_lower_rail_pad", (172.0, 32.0, 14.0), (-172.0, -42.0, 47.0)),
        _box(build123d, "gantry_beam_left_upper_rail_pad", (172.0, 32.0, 14.0), (-172.0, -42.0, 107.0)),
    ]
    right_pads = [
        _box(build123d, "gantry_beam_right_lower_rail_pad", (172.0, 32.0, 14.0), (0.0, -42.0, 47.0)),
        _box(build123d, "gantry_beam_right_upper_rail_pad", (172.0, 32.0, 14.0), (0.0, -42.0, 107.0)),
    ]
    shapes["gantry_beam_left"] = _compound(build123d, "gantry_beam_left", [left_main, left_tongue, *left_pads])
    shapes["gantry_beam_right"] = _compound(
        build123d, "gantry_beam_right", [right_main.cut(right_groove), *right_pads]
    )
    shapes["x_fixed_bearing_cartridge"] = _closed_box(
        build123d, "x_fixed_bearing_cartridge", (38.0, 70.0, 48.0), (-181.0, -5.0, 60.0), 5.0
    )
    shapes["x_floating_bearing_cartridge"] = _closed_box(
        build123d, "x_floating_bearing_cartridge", (38.0, 70.0, 48.0), (143.0, -5.0, 60.0), 5.0
    )
    return shapes


def _moving_head_part_shapes(build123d: Any) -> dict[str, Any]:
    shapes: dict[str, Any] = {}
    backplate = _closed_box(build123d, "x_carriage_plate", (90.0, 34.0, 130.0), (-45.0, -52.0, 18.0), 5.0)
    rail_ribs = [
        _box(build123d, "x_carriage_left_z_rail_rib", (14.0, 14.0, 120.0), (-42.0, -52.0, 23.0)),
        _box(build123d, "x_carriage_right_z_rail_rib", (14.0, 14.0, 120.0), (28.0, -52.0, 23.0)),
    ]
    shapes["x_carriage_plate"] = _compound(build123d, "x_carriage_plate", [backplate, *rail_ribs])

    z_plate = _box(build123d, "z_carriage_plate_body", (90.0, 44.0, 100.0), (-45.0, -62.0, 30.0))
    z_ribs = [
        _box(build123d, "z_carriage_left_rib", (12.0, 44.0, 100.0), (-45.0, -62.0, 30.0)),
        _box(build123d, "z_carriage_right_rib", (12.0, 44.0, 100.0), (33.0, -62.0, 30.0)),
    ]
    shapes["z_carriage_plate"] = _compound(build123d, "z_carriage_plate", [z_plate, *z_ribs])
    shapes["z_fixed_bearing_support"] = _closed_box(
        build123d, "z_fixed_bearing_support", (70.0, 50.0, 32.0), (-35.0, -48.0, 142.0), 5.0
    )
    shapes["z_motor_service_cartridge"] = _closed_box(
        build123d, "z_motor_service_cartridge", (70.0, 50.0, 45.0), (-35.0, -48.0, 174.0), 5.0
    )
    ring_outer = _cylinder(build123d, "spindle_mount_outer", 38.0, 20.0, (0.0, -58.0, 72.0))
    ring_inner = _cylinder(build123d, "spindle_mount_bore_screen", 26.0, 20.0, (0.0, -58.0, 72.0))
    saddle = _box(build123d, "spindle_mount_saddle", (80.0, 18.0, 40.0), (-40.0, -62.0, 72.0))
    clamp_rib = _box(build123d, "spindle_mount_clamp_rib", (80.0, 12.0, 12.0), (-40.0, -44.0, 80.0))
    shapes["spindle_mount_concept"] = _compound(
        build123d, "spindle_mount_concept", [ring_outer.cut(ring_inner), saddle, clamp_rib]
    )
    return shapes


def _moving_bed_shape(build123d: Any) -> Any:
    bed_z = -8.0
    pieces = [
        _box(build123d, "moving_bed_front_beam", (230.0, 18.0, 12.0), (-115.0, -90.0, bed_z)),
        _box(build123d, "moving_bed_rear_beam", (230.0, 18.0, 12.0), (-115.0, 72.0, bed_z)),
        _box(build123d, "moving_bed_left_beam", (18.0, 144.0, 12.0), (-115.0, -72.0, bed_z)),
        _box(build123d, "moving_bed_right_beam", (18.0, 144.0, 12.0), (97.0, -72.0, bed_z)),
    ]
    for index, x in enumerate((-55.0, 0.0, 55.0), start=1):
        pieces.append(_box(build123d, f"moving_bed_cross_rib_{index}", (14.0, 126.0, 12.0), (x - 7.0, -63.0, bed_z)))
    # The boss drops around the T8x4 nut envelope; its lower extent is why
    # this review part is declared as a 30 mm concept height in the parameter
    # table, while the 8 mm PCB bed support remains a separate datum.
    pieces.append(_box(build123d, "moving_bed_y_nut_boss", (40.0, 32.0, 30.0), (-20.0, -16.0, -26.0)))
    for index, (x, y) in enumerate(((-110.0, -40.0), (110.0, -40.0), (-110.0, 40.0), (110.0, 40.0)), start=1):
        pieces.append(_box(build123d, f"moving_bed_carriage_pad_{index}", (10.0, 32.0, 12.0), (x - 5.0, y - 16.0, bed_z)))
    return _compound(build123d, "moving_bed_frame", pieces)


def build_phase4_structural_parts() -> tuple[SkeletonComponent, ...]:
    """Build all preliminary structural PETG parts in machine coordinates."""

    build123d = _build123d()
    shapes = _base_part_shapes(build123d)
    shapes.update(_gantry_part_shapes(build123d))
    shapes.update(_moving_head_part_shapes(build123d))
    shapes["moving_bed_frame"] = _moving_bed_shape(build123d)
    components: list[SkeletonComponent] = []
    for parameter in PHASE4_STRUCTURAL_PARAMETERS.print_parts:
        if parameter.part_id not in shapes:
            raise KeyError(f"No Phase 4 shape builder exists for {parameter.part_id}")
        components.append(_part(build123d, parameter, shapes[parameter.part_id]))
    return tuple(components)
