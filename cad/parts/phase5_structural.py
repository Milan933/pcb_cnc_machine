"""First Phase 5 manufacturing-CAD batch for the integrated base pair.

This module is deliberately separate from the Phase 4A review builder.  The
Phase 4A O2 model showed the load path with compounds; this builder creates
one fused, printable solid for each base side, including real walls, ribs,
rail-seat material, provisional fastener holes, and a center-tie shear land.

The rail, fastener, and center-tie dimensions are explicitly provisional
until representative hardware is measured.  The geometry is therefore a
test-printable ``PROTOTYPE-STL`` candidate, not a released or
hardware-validated part.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class Phase5BasePairParameters:
    """Parametric contract for both mirrored integrated base components."""

    part_width_mm: float = 150.0
    part_length_mm: float = 300.0
    perimeter_height_mm: float = 36.0
    perimeter_wall_mm: float = 5.0
    front_rear_depth_mm: float = 32.0
    side_member_width_mm: float = 48.0
    side_member_inner_wall_mm: float = 5.0

    rail_carrier_x_mm: float = 50.0
    rail_carrier_width_mm: float = 28.0
    rail_carrier_bottom_z_mm: float = 24.75
    rail_carrier_height_mm: float = 16.0
    rail_carrier_wall_mm: float = 4.0
    rail_carrier_end_margin_mm: float = 10.0
    rail_pad_x_mm: float = 54.0
    rail_pad_width_mm: float = 20.0
    rail_pad_height_mm: float = 3.0
    rail_datum_shoulder_x_mm: float = 51.0
    rail_datum_shoulder_width_mm: float = 3.0
    rail_hole_x_mm: float = 64.0
    rail_hole_diameter_mm: float = 4.0
    rail_hole_pitch_mm: float = 30.0
    rail_hole_first_y_mm: float = 15.0
    rail_hole_count: int = 10

    shear_web_x_mm: float = 44.0
    shear_web_width_mm: float = 14.0
    shear_web_y_margin_mm: float = 32.0
    shear_web_bottom_z_mm: float = 18.75
    shear_web_height_mm: float = 16.0
    cross_rib_width_mm: float = 34.0
    cross_rib_depth_mm: float = 10.0
    cross_rib_y_positions_mm: tuple[float, ...] = (52.0, 112.0, 172.0, 232.0)

    center_tie_land_x_mm: float = 44.0
    center_tie_land_width_mm: float = 34.0
    center_tie_land_y_mm: float = 130.0
    center_tie_land_length_mm: float = 40.0
    center_tie_land_z_mm: float = 12.0
    center_tie_land_height_mm: float = 16.0
    center_tie_hole_x_mm: float = 64.0
    center_tie_hole_y_positions_mm: tuple[float, ...] = (140.0, 160.0)

    foot_hole_x_mm: float = 24.0
    foot_hole_y_positions_mm: tuple[float, ...] = (16.0, 284.0)
    provisional_m4_clearance_diameter_mm: float = 4.5
    provisional_m4_counterbore_diameter_mm: float = 9.0
    provisional_m4_counterbore_depth_mm: float = 2.5

    @property
    def overall_height_mm(self) -> float:
        return self.rail_carrier_bottom_z_mm + self.rail_carrier_height_mm + self.rail_pad_height_mm

    @property
    def side_member_depth_mm(self) -> float:
        return self.part_length_mm - 2.0 * self.front_rear_depth_mm

    @property
    def rail_hole_y_positions_mm(self) -> tuple[float, ...]:
        return tuple(
            self.rail_hole_first_y_mm + index * self.rail_hole_pitch_mm
            for index in range(self.rail_hole_count)
        )

    @property
    def maturity(self) -> str:
        return "PROTOTYPE-STL"

    @property
    def interface_status(self) -> str:
        return "PROVISIONAL_HARDWARE_DIMENSION"


PHASE5_BASE_PAIR_PARAMETERS = Phase5BasePairParameters()
PHASE5_BASE_PART_IDS = ("base_left_integrated", "base_right_integrated")


def _build123d() -> Any:
    try:
        import build123d
    except ImportError as exc:  # pragma: no cover - exercised by CAD runner
        raise RuntimeError(
            "Phase 5 manufacturing geometry requires build123d. Install the "
            "pinned dependency from requirements/cad-phase-2.txt."
        ) from exc
    return build123d


def _box(build123d: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], label: str) -> Any:
    shape = build123d.Box(
        *size,
        align=(build123d.Align.MIN, build123d.Align.MIN, build123d.Align.MIN),
    ).located(build123d.Location(minimum))
    shape.label = label
    return shape


def _cylinder(
    build123d: Any,
    radius_mm: float,
    height_mm: float,
    minimum: tuple[float, float, float],
    label: str,
) -> Any:
    shape = build123d.Cylinder(
        radius_mm,
        height_mm,
        align=(build123d.Align.CENTER, build123d.Align.CENTER, build123d.Align.MIN),
    ).located(build123d.Location(minimum))
    shape.label = label
    return shape


def _closed_box(
    build123d: Any,
    size: tuple[float, float, float],
    minimum: tuple[float, float, float],
    wall_mm: float,
    label: str,
) -> Any:
    if min(size) <= 2.0 * wall_mm:
        raise ValueError(f"{label} is too small for a {wall_mm} mm closed section.")
    outer = _box(build123d, size, minimum, f"{label}_outer")
    inner_size = tuple(value - 2.0 * wall_mm for value in size)
    inner_minimum = tuple(value + wall_mm for value in minimum)
    inner = _box(build123d, inner_size, inner_minimum, f"{label}_cavity")
    result = outer.cut(inner)
    result.label = label
    return result


def _fuse_all(shapes: list[Any]) -> Any:
    if not shapes:
        raise ValueError("At least one solid is required.")
    result = shapes[0]
    for shape in shapes[1:]:
        result = result.fuse(shape)
    return result


def _build_left_base(parameters: Phase5BasePairParameters, build123d: Any) -> Any:
    """Build the left-hand local part before the mirrored right-hand copy."""

    p = parameters
    front_rear_size = (p.part_width_mm, p.front_rear_depth_mm, p.perimeter_height_mm)
    front = _closed_box(
        build123d,
        front_rear_size,
        (0.0, 0.0, 0.0),
        p.perimeter_wall_mm,
        "phase5_front_perimeter",
    )
    rear = _closed_box(
        build123d,
        front_rear_size,
        (0.0, p.part_length_mm - p.front_rear_depth_mm, 0.0),
        p.perimeter_wall_mm,
        "phase5_rear_perimeter",
    )
    side = _closed_box(
        build123d,
        (p.side_member_width_mm, p.side_member_depth_mm, p.perimeter_height_mm),
        (0.0, p.front_rear_depth_mm, 0.0),
        p.perimeter_wall_mm,
        "phase5_outer_side_perimeter",
    )

    carrier_outer = _box(
        build123d,
        (p.rail_carrier_width_mm, p.part_length_mm, p.rail_carrier_height_mm),
        (p.rail_carrier_x_mm, 0.0, p.rail_carrier_bottom_z_mm),
        "phase5_rail_carrier_outer",
    )
    carrier_cavity = _box(
        build123d,
        (
            p.rail_carrier_width_mm - 2.0 * p.rail_carrier_wall_mm,
            p.part_length_mm - 2.0 * p.rail_carrier_end_margin_mm,
            p.rail_carrier_height_mm - 6.0,
        ),
        (
            p.rail_carrier_x_mm + p.rail_carrier_wall_mm,
            p.rail_carrier_end_margin_mm,
            p.rail_carrier_bottom_z_mm - 0.25,
        ),
        "phase5_rail_carrier_cavity",
    )
    carrier = carrier_outer.cut(carrier_cavity)
    carrier.label = "phase5_rail_carrier_ribbed"

    rail_pad = _box(
        build123d,
        (p.rail_pad_width_mm, p.part_length_mm, p.rail_pad_height_mm),
        (p.rail_pad_x_mm, 0.0, p.rail_carrier_bottom_z_mm + p.rail_carrier_height_mm),
        "phase5_rail_datum_pad",
    )
    rail_shoulder = _box(
        build123d,
        (p.rail_datum_shoulder_width_mm, p.part_length_mm, p.rail_pad_height_mm),
        (p.rail_datum_shoulder_x_mm, 0.0, p.rail_carrier_bottom_z_mm + p.rail_carrier_height_mm),
        "phase5_rail_datum_shoulder",
    )

    shear_web = _box(
        build123d,
        (p.shear_web_width_mm, p.side_member_depth_mm, p.shear_web_height_mm),
        (p.shear_web_x_mm, p.front_rear_depth_mm, p.shear_web_bottom_z_mm),
        "phase5_continuous_shear_web",
    )
    cross_ribs = [
        _box(
            build123d,
            (p.cross_rib_width_mm, p.cross_rib_depth_mm, p.shear_web_height_mm),
            (p.shear_web_x_mm, y_mm, p.shear_web_bottom_z_mm),
            f"phase5_cross_rib_{index}",
        )
        for index, y_mm in enumerate(p.cross_rib_y_positions_mm, start=1)
    ]

    tie_land = _box(
        build123d,
        (p.center_tie_land_width_mm, p.center_tie_land_length_mm, p.center_tie_land_height_mm),
        (p.center_tie_land_x_mm, p.center_tie_land_y_mm, p.center_tie_land_z_mm),
        "phase5_center_tie_shear_land",
    )

    result = _fuse_all([front, rear, side, carrier, rail_pad, rail_shoulder, shear_web, *cross_ribs, tie_land])

    # The following openings are intentionally screening dimensions.  They
    # make the part usable for fit checks without claiming measured rail or
    # fastener geometry.
    rail_hole_radius = p.rail_hole_diameter_mm / 2.0
    for index, y_mm in enumerate(p.rail_hole_y_positions_mm, start=1):
        result = result.cut(
            _cylinder(
                build123d,
                rail_hole_radius,
                p.overall_height_mm + 2.0,
                (p.rail_hole_x_mm, y_mm, p.rail_carrier_bottom_z_mm - 1.0),
                f"phase5_rail_hole_{index}",
            )
        )

    foot_hole_radius = p.provisional_m4_clearance_diameter_mm / 2.0
    counterbore_radius = p.provisional_m4_counterbore_diameter_mm / 2.0
    for index, y_mm in enumerate(p.foot_hole_y_positions_mm, start=1):
        result = result.cut(
            _cylinder(
                build123d,
                foot_hole_radius,
                p.perimeter_height_mm + 2.0,
                (p.foot_hole_x_mm, y_mm, -1.0),
                f"phase5_foot_clearance_{index}",
            )
        )
        result = result.cut(
            _cylinder(
                build123d,
                counterbore_radius,
                p.provisional_m4_counterbore_depth_mm + 0.1,
                (p.foot_hole_x_mm, y_mm, -0.1),
                f"phase5_foot_counterbore_{index}",
            )
        )

    tie_hole_radius = p.provisional_m4_clearance_diameter_mm / 2.0
    for index, y_mm in enumerate(p.center_tie_hole_y_positions_mm, start=1):
        result = result.cut(
            _cylinder(
                build123d,
                tie_hole_radius,
                p.center_tie_land_height_mm + 2.0,
                (p.center_tie_hole_x_mm, y_mm, p.center_tie_land_z_mm - 1.0),
                f"phase5_center_tie_hole_{index}",
            )
        )

    result.label = "base_left_integrated"
    return result


def build_phase5_base_part(
    side: Literal["left", "right"],
    parameters: Phase5BasePairParameters = PHASE5_BASE_PAIR_PARAMETERS,
) -> Any:
    """Build one local, slicer-ready integrated base part."""

    build123d = _build123d()
    left = _build_left_base(parameters, build123d)
    if side == "left":
        result = left
    elif side == "right":
        mirror_plane = build123d.Plane(
            origin=(parameters.part_width_mm / 2.0, 0.0, 0.0),
            z_dir=(1.0, 0.0, 0.0),
        )
        result = build123d.mirror(left, about=mirror_plane)
    else:
        raise ValueError(f"Unknown base side: {side}")
    result.label = f"base_{side}_integrated"
    return result


def build_phase5_base_pair(
    parameters: Phase5BasePairParameters = PHASE5_BASE_PAIR_PARAMETERS,
) -> dict[str, Any]:
    """Build exactly the first two Phase 5 manufacturing parts."""

    return {
        "base_left_integrated": build_phase5_base_part("left", parameters),
        "base_right_integrated": build_phase5_base_part("right", parameters),
    }


__all__ = [
    "PHASE5_BASE_PAIR_PARAMETERS",
    "PHASE5_BASE_PART_IDS",
    "Phase5BasePairParameters",
    "build_phase5_base_pair",
    "build_phase5_base_part",
]
