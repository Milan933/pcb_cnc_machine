"""Build123d architecture-only skeleton for the Phase 2 trade study.

The module deliberately contains bounding volumes and reference tubes only:
working/travel envelopes, guide and screw centerlines, carriage boxes,
spindle envelope, bed envelope, and structural bounds. It is not a detailed
printable-part model and must not be used as a manufacturing export.

The build123d import is lazy so the dependency-light validation and unit tests
remain runnable without a CAD installation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cad.architecture import ArchitectureId
from cad.parameters import (
    PHASE2A_PARAMETERS,
    PHASE2_SKELETON_PARAMETERS,
    Phase2AParameters,
    Phase2SkeletonParameters,
)


@dataclass(frozen=True)
class SkeletonComponent:
    """Named, placed skeleton shape with a review-only semantic category."""

    name: str
    category: str
    shape: Any
    notes: str


@dataclass(frozen=True)
class SkeletonModel:
    """A deterministic compound-backed architecture assembly."""

    candidate_id: ArchitectureId
    components: tuple[SkeletonComponent, ...]
    expected_interference_pairs: tuple[frozenset[str], ...]
    variant: str = "phase2"

    @property
    def compound(self) -> Any:
        """Return an unfused build123d compound preserving component boundaries."""

        from build123d import Compound

        return Compound(children=[component.shape for component in self.components])

    @property
    def bounding_box_mm(self) -> dict[str, tuple[float, float, float]]:
        """Return the compound bounding-box extents in millimetres."""

        bounding_box = self.compound.bounding_box()
        return {
            "min": _vector_tuple(bounding_box.min),
            "max": _vector_tuple(bounding_box.max),
            "size": _vector_tuple(bounding_box.size),
        }


def _build123d() -> Any:
    try:
        import build123d
    except ImportError as exc:  # pragma: no cover - exercised by the spike runner
        raise RuntimeError(
            "The architecture skeleton requires build123d. Install the pinned "
            "dependency from requirements/cad-phase-2.txt."
        ) from exc
    return build123d


def _vector_tuple(vector: Any) -> tuple[float, float, float]:
    return tuple(float(getattr(vector, axis)) for axis in ("X", "Y", "Z"))


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


def _reference_tube(
    build123d: Any,
    name: str,
    axis: str,
    length: float,
    center: tuple[float, float, float],
    diameter: float,
) -> Any:
    """Create a thin rectangular reference tube along one global axis."""

    x, y, z = center
    half = diameter / 2.0
    if axis == "x":
        size = (length, diameter, diameter)
        minimum = (x - length / 2.0, y - half, z - half)
    elif axis == "y":
        size = (diameter, length, diameter)
        minimum = (x - half, y - length / 2.0, z - half)
    elif axis == "z":
        size = (diameter, diameter, length)
        minimum = (x - half, y - half, z - length / 2.0)
    else:
        raise ValueError(f"Unsupported reference-tube axis: {axis}")
    return _box(build123d, name, size, minimum)


def _component(
    build123d: Any,
    name: str,
    category: str,
    shape: Any,
    notes: str,
) -> SkeletonComponent:
    shape.label = name
    return SkeletonComponent(name=name, category=category, shape=shape, notes=notes)


def _common_components(
    build123d: Any,
    parameters: Phase2SkeletonParameters,
) -> list[SkeletonComponent]:
    px, py, pz = parameters.bed_envelope_mm
    bx, by, bz = parameters.base_envelope_mm
    wx, wy = parameters.working_area_mm
    tx, ty, tz = parameters.tool_travel_mm

    components = [
        _component(
            build123d,
            "base_envelope",
            "structural",
            _box(build123d, "base_envelope", (bx, by, bz), (-bx / 2.0, -by / 2.0, -bz)),
            "Architecture-only base bounding volume; no wall or rib geometry.",
        ),
        _component(
            build123d,
            "pcb_bed_envelope",
            "datum-envelope",
            _box(build123d, "pcb_bed_envelope", (px, py, pz), (-px / 2.0, -py / 2.0, -pz)),
            "Replaceable spoilboard and PCB support envelope; workholding details are open.",
        ),
        _component(
            build123d,
            "pcb_working_area",
            "process-envelope",
            _box(build123d, "pcb_working_area", (wx, wy, 2.0), (-wx / 2.0, -wy / 2.0, 0.0)),
            "Accepted 200 x 150 mm process baseline, not final tool travel.",
        ),
        _component(
            build123d,
            "tool_point_travel_envelope",
            "process-envelope",
            _box(build123d, "tool_point_travel_envelope", (tx, ty, tz), (-tx / 2.0, -ty / 2.0, -tz)),
            "Preliminary skeleton sweep showing tool-point travel budget only.",
        ),
    ]

    spindle_x = 0.0
    spindle_y = -20.0
    spindle_bottom = parameters.tool_stickout_mm
    components.extend(
        (
            _component(
                build123d,
                "z_carriage_envelope",
                "carriage-envelope",
                _box(
                    build123d,
                    "z_carriage_envelope",
                    parameters.z_carriage_envelope_mm,
                    (
                        -parameters.z_carriage_envelope_mm[0] / 2.0,
                        spindle_y - parameters.z_carriage_envelope_mm[1] / 2.0,
                        parameters.gantry_crossbeam_bottom_z_mm,
                    ),
                ),
                "Z carriage bounding box; spindle mount and rail-seat geometry are intentionally absent.",
            ),
            _component(
                build123d,
                "spindle_envelope",
                "hardware-envelope",
                _cylinder(
                    build123d,
                    "spindle_envelope",
                    parameters.spindle_envelope_diameter_mm / 2.0,
                    parameters.spindle_envelope_length_mm,
                    (spindle_x, spindle_y, spindle_bottom),
                ),
                "Maximum screening spindle envelope; no spindle is selected.",
            ),
            _component(
                build123d,
                "tool_envelope",
                "hardware-envelope",
                _cylinder(
                    build123d,
                    "tool_envelope",
                    3.0,
                    parameters.tool_stickout_mm,
                    (spindle_x, spindle_y, 0.0),
                ),
                "Tool stickout envelope for clearance review; cutter geometry is not selected.",
            ),
        )
    )
    return components


def _fixed_gantry_components(
    build123d: Any,
    parameters: Phase2SkeletonParameters,
    prefix: str,
) -> list[SkeletonComponent]:
    outer = parameters.gantry_outer_width_mm
    clear = parameters.gantry_clear_span_mm
    side_width = (outer - clear) / 2.0
    side_y = parameters.gantry_section_depth_mm
    beam_z = parameters.gantry_crossbeam_bottom_z_mm
    beam_h = parameters.gantry_section_height_mm
    components = [
        _component(
            build123d,
            f"{prefix}_gantry_left",
            "structural",
            _box(build123d, f"{prefix}_gantry_left", (side_width, side_y, beam_z + parameters.bed_envelope_mm[2]), (-outer / 2.0, -side_y / 2.0, -parameters.bed_envelope_mm[2])),
            "Fixed-ganty side structural bound; printed monocoque/ribs are future geometry.",
        ),
        _component(
            build123d,
            f"{prefix}_gantry_right",
            "structural",
            _box(build123d, f"{prefix}_gantry_right", (side_width, side_y, beam_z + parameters.bed_envelope_mm[2]), (outer / 2.0 - side_width, -side_y / 2.0, -parameters.bed_envelope_mm[2])),
            "Fixed-gantry side structural bound; printed monocoque/ribs are future geometry.",
        ),
        _component(
            build123d,
            f"{prefix}_gantry_crossbeam",
            "structural",
            _box(build123d, f"{prefix}_gantry_crossbeam", (clear, side_y, beam_h), (-clear / 2.0, -side_y / 2.0, beam_z)),
            "Crossbeam bound for deep closed/ribbed/torsion-box comparison; no detailed section.",
        ),
    ]
    return components


def _moving_gantry_components(
    build123d: Any,
    parameters: Phase2SkeletonParameters,
) -> list[SkeletonComponent]:
    outer = parameters.gantry_outer_width_mm
    clear = parameters.gantry_clear_span_mm
    side_width = (outer - clear) / 2.0
    side_y = parameters.gantry_section_depth_mm
    beam_z = parameters.gantry_crossbeam_bottom_z_mm
    beam_h = parameters.gantry_section_height_mm
    return [
        _component(
            build123d,
            "moving_gantry_left",
            "structural",
            _box(build123d, "moving_gantry_left", (side_width, side_y, beam_z + parameters.bed_envelope_mm[2]), (-outer / 2.0, -side_y / 2.0, -parameters.bed_envelope_mm[2])),
            "Moving-gantry side interface bound; Y rail and bearing seats are future geometry.",
        ),
        _component(
            build123d,
            "moving_gantry_right",
            "structural",
            _box(build123d, "moving_gantry_right", (side_width, side_y, beam_z + parameters.bed_envelope_mm[2]), (outer / 2.0 - side_width, -side_y / 2.0, -parameters.bed_envelope_mm[2])),
            "Moving-gantry side interface bound; Y rail and bearing seats are future geometry.",
        ),
        _component(
            build123d,
            "moving_gantry_crossbeam",
            "structural",
            _box(build123d, "moving_gantry_crossbeam", (clear, side_y, beam_h), (-clear / 2.0, -side_y / 2.0, beam_z)),
            "Moving crossbeam bound for the deep ribbed closed monocoque candidate.",
        ),
    ]


def _phase2a_fixed_gantry_components(
    build123d: Any,
    parameters: Phase2SkeletonParameters,
    phase2a: Phase2AParameters,
) -> list[SkeletonComponent]:
    """Optimized A bound: one integrated deep stationary gantry concept."""

    outer = parameters.gantry_outer_width_mm
    clear = parameters.gantry_clear_span_mm
    side_width = (outer - clear) / 2.0
    beam_depth = phase2a.a_section_width_mm
    beam_height = phase2a.a_section_depth_mm
    beam_bottom = phase2a.a_beam_bottom_z_mm
    base_top = -parameters.bed_envelope_mm[2]
    left = _box(
        build123d,
        "a_fixed_gantry_left_support",
        (side_width, beam_depth, beam_bottom - base_top),
        (-outer / 2.0, -beam_depth / 2.0, base_top),
    )
    right = _box(
        build123d,
        "a_fixed_gantry_right_support",
        (side_width, beam_depth, beam_bottom - base_top),
        (outer / 2.0 - side_width, -beam_depth / 2.0, base_top),
    )
    beam = _box(
        build123d,
        "a_fixed_gantry_deep_torsion_box",
        (clear, beam_depth, beam_height),
        (-clear / 2.0, -beam_depth / 2.0, beam_bottom),
    )
    integrated = build123d.Compound(children=[left, right, beam])
    integrated.label = "a_integrated_fixed_gantry_envelope"
    return [
        _component(
            build123d,
            "a_integrated_fixed_gantry_envelope",
            "structural",
            integrated,
            "Optimized A one-piece U/monocoque bound: deep torsion box, large side supports, wide base interfaces. A multi-piece beam-plus-two-support variant remains the print-risk fallback.",
        ),
        _component(
            build123d,
            "a_moving_bed_structure",
            "structural",
            _box(
                build123d,
                "a_moving_bed_structure",
                (
                    parameters.bed_envelope_mm[0],
                    parameters.bed_envelope_mm[1],
                    phase2a.a_moving_bed_support_thickness_mm,
                ),
                (
                    -parameters.bed_envelope_mm[0] / 2.0,
                    -parameters.bed_envelope_mm[1] / 2.0,
                    -phase2a.a_moving_bed_support_thickness_mm,
                ),
            ),
            "Low-mass moving PCB/spoilboard support; thin support is optimized because the bed carries only the PCB process datum.",
        ),
    ]


def _phase2a_moving_gantry_components(
    build123d: Any,
    parameters: Phase2SkeletonParameters,
    phase2a: Phase2AParameters,
) -> list[SkeletonComponent]:
    """Optimized B bound: lighter deep beam with explicit side interfaces."""

    outer = parameters.gantry_outer_width_mm
    clear = parameters.gantry_clear_span_mm
    side_width = (outer - clear) / 2.0
    beam_depth = phase2a.b_section_width_mm
    beam_height = phase2a.b_section_depth_mm
    beam_bottom = parameters.gantry_crossbeam_bottom_z_mm
    base_top = -parameters.bed_envelope_mm[2]
    side_height = beam_bottom - base_top
    return [
        _component(
            build123d,
            "moving_gantry_left",
            "structural",
            _box(
                build123d,
                "moving_gantry_left",
                (side_width, phase2a.b_support_bending_length_mm, side_height),
                (-outer / 2.0, -phase2a.b_support_bending_length_mm / 2.0, base_top),
            ),
            "Optimized B left side interface with integrated gusset envelope; Y rail seat and through-bolt load spreader remain future geometry.",
        ),
        _component(
            build123d,
            "moving_gantry_right",
            "structural",
            _box(
                build123d,
                "moving_gantry_right",
                (side_width, phase2a.b_support_bending_length_mm, side_height),
                (outer / 2.0 - side_width, -phase2a.b_support_bending_length_mm / 2.0, base_top),
            ),
            "Optimized B right side interface with integrated gusset envelope; Y rail seat and through-bolt load spreader remain future geometry.",
        ),
        _component(
            build123d,
            "moving_gantry_crossbeam",
            "structural",
            _box(
                build123d,
                "moving_gantry_crossbeam",
                (clear, beam_depth, beam_height),
                (-clear / 2.0, -beam_depth / 2.0, beam_bottom),
            ),
            "Optimized B deep ribbed closed beam bound; side interfaces remain separate to expose moving-joint compliance.",
        ),
    ]


def _guide_and_screw_references(
    build123d: Any,
    parameters: Phase2SkeletonParameters,
    candidate_id: ArchitectureId,
    *,
    beam_bottom_z_mm: float | None = None,
    beam_height_mm: float | None = None,
    beam_depth_mm: float | None = None,
) -> list[SkeletonComponent]:
    d = parameters.reference_axis_diameter_mm
    screw_d = parameters.reference_screw_diameter_mm
    x_span = parameters.gantry_clear_span_mm
    y_span = parameters.tool_travel_mm[1] + 2.0 * parameters.rail_end_margin_mm
    z_span = parameters.tool_travel_mm[2] + 2.0 * parameters.rail_end_margin_mm
    beam_bottom = (
        parameters.gantry_crossbeam_bottom_z_mm
        if beam_bottom_z_mm is None
        else beam_bottom_z_mm
    )
    beam_height = (
        parameters.gantry_section_height_mm
        if beam_height_mm is None
        else beam_height_mm
    )
    beam_depth = (
        parameters.gantry_section_depth_mm
        if beam_depth_mm is None
        else beam_depth_mm
    )
    z_center = beam_bottom + beam_height / 2.0
    z_axis_center = beam_bottom
    x_rail_y = -beam_depth / 2.0 - d
    spindle_y = -20.0
    refs: list[SkeletonComponent] = []

    for index, z in enumerate((z_center - parameters.x_rail_vertical_spacing_mm / 2.0, z_center + parameters.x_rail_vertical_spacing_mm / 2.0), start=1):
        name = f"x_rail_centerline_{index}"
        refs.append(_component(build123d, name, "reference", _reference_tube(build123d, name, "x", x_span, (0.0, x_rail_y, z), d), "X rail centerline reference."))
    name = "x_screw_centerline"
    refs.append(_component(build123d, name, "reference", _reference_tube(build123d, name, "x", x_span + 2.0 * parameters.screw_end_margin_mm, (0.0, x_rail_y - d, z_center), screw_d), "Centered X screw reference; T8x2/T8x4 remain candidates."))

    y_x_positions = (-parameters.y_rail_center_spacing_mm / 2.0, parameters.y_rail_center_spacing_mm / 2.0)
    for index, x in enumerate(y_x_positions, start=1):
        name = f"y_rail_centerline_{index}"
        refs.append(_component(build123d, name, "reference", _reference_tube(build123d, name, "y", y_span, (x, 0.0, -parameters.bed_envelope_mm[2] - d), d), "Separated Y rail centerline reference."))
    name = "y_screw_centerline"
    refs.append(_component(build123d, name, "reference", _reference_tube(build123d, name, "y", y_span + 2.0 * parameters.screw_end_margin_mm, (0.0, 0.0, -parameters.bed_envelope_mm[2] - 2.0 * d), screw_d), "Centered Y screw reference; dual screw remains a racking contingency."))

    for index, x in enumerate((-parameters.z_rail_center_spacing_mm / 2.0, parameters.z_rail_center_spacing_mm / 2.0), start=1):
        name = f"z_rail_centerline_{index}"
        refs.append(_component(build123d, name, "reference", _reference_tube(build123d, name, "z", z_span, (x, spindle_y, z_axis_center), d), "Dual Z guide centerline; MGN9/MGN12 class remains open."))
    name = "z_screw_centerline"
    refs.append(_component(build123d, name, "reference", _reference_tube(build123d, name, "z", z_span, (0.0, spindle_y, z_axis_center), screw_d), "Centered Z screw reference; T8x2/T8x4 remain candidates."))

    if candidate_id == ArchitectureId.C:
        # C uses the same guide/screw count for a fair comparison, but the
        # references sit in the elevated moving-head subassembly.
        refs.append(_component(build123d, "c_xy_head_reference", "reference", _box(build123d, "c_xy_head_reference", (100.0, 80.0, 40.0), (-50.0, -60.0, 70.0)), "Moving XY head bounding box; the extra head stack is the reason C is retained only as a credible alternative."))
    return refs


def build_skeleton(
    candidate_id: ArchitectureId | str,
    parameters: Phase2SkeletonParameters = PHASE2_SKELETON_PARAMETERS,
    *,
    structural_variant: str = "phase2",
    phase2a_parameters: Phase2AParameters = PHASE2A_PARAMETERS,
) -> SkeletonModel:
    """Build one deterministic architecture-only skeleton.

    ``structural_variant='phase2a'`` is restricted to A and B and exposes the
    independently optimized preliminary structural bounds used by the focused
    comparison. Neither variant is a detailed manufacturing model.
    """

    build123d = _build123d()
    candidate = ArchitectureId(candidate_id)
    if structural_variant not in {"phase2", "phase2a"}:
        raise ValueError(f"Unknown skeleton structural variant: {structural_variant}")
    if structural_variant == "phase2a" and candidate not in (ArchitectureId.A, ArchitectureId.B):
        raise ValueError("The Phase 2A optimized skeleton compares only A and B.")
    components = _common_components(build123d, parameters)

    if structural_variant == "phase2a" and candidate == ArchitectureId.A:
        components.extend(_phase2a_fixed_gantry_components(build123d, parameters, phase2a_parameters))
        beam_bottom = phase2a_parameters.a_beam_bottom_z_mm
        beam_height = phase2a_parameters.a_section_depth_mm
        beam_depth = phase2a_parameters.a_section_width_mm
    elif structural_variant == "phase2a" and candidate == ArchitectureId.B:
        components.extend(_phase2a_moving_gantry_components(build123d, parameters, phase2a_parameters))
        beam_bottom = parameters.gantry_crossbeam_bottom_z_mm
        beam_height = phase2a_parameters.b_section_depth_mm
        beam_depth = phase2a_parameters.b_section_width_mm
    elif candidate in (ArchitectureId.A, ArchitectureId.C):
        components.extend(_fixed_gantry_components(build123d, parameters, candidate.value.lower()))
        beam_bottom = parameters.gantry_crossbeam_bottom_z_mm
        beam_height = parameters.gantry_section_height_mm
        beam_depth = parameters.gantry_section_depth_mm
    else:
        components.extend(_moving_gantry_components(build123d, parameters))
        beam_bottom = parameters.gantry_crossbeam_bottom_z_mm
        beam_height = parameters.gantry_section_height_mm
        beam_depth = parameters.gantry_section_depth_mm
    components.extend(
        _guide_and_screw_references(
            build123d,
            parameters,
            candidate,
            beam_bottom_z_mm=beam_bottom,
            beam_height_mm=beam_height,
            beam_depth_mm=beam_depth,
        )
    )

    expected_pairs_list = [
        frozenset(("base_envelope", "pcb_bed_envelope")),
        frozenset(("z_carriage_envelope", "spindle_envelope")),
    ]
    if structural_variant == "phase2a" and candidate == ArchitectureId.A:
        expected_pairs_list.extend(
            (
                frozenset(("base_envelope", "a_integrated_fixed_gantry_envelope")),
                frozenset(("pcb_bed_envelope", "a_moving_bed_structure")),
                frozenset(("base_envelope", "a_moving_bed_structure")),
                frozenset(("z_carriage_envelope", "a_integrated_fixed_gantry_envelope")),
                frozenset(("spindle_envelope", "a_integrated_fixed_gantry_envelope")),
            )
        )
    else:
        gantry_prefix = "moving_gantry" if candidate == ArchitectureId.B else f"{candidate.value.lower()}_gantry"
        expected_pairs_list.extend(
            (
                frozenset(("z_carriage_envelope", f"{gantry_prefix}_crossbeam")),
                frozenset(("spindle_envelope", f"{gantry_prefix}_crossbeam")),
                frozenset(("base_envelope", f"{gantry_prefix}_left")),
                frozenset(("base_envelope", f"{gantry_prefix}_right")),
            )
        )
    return SkeletonModel(
        candidate_id=candidate,
        components=tuple(components),
        expected_interference_pairs=tuple(expected_pairs_list),
        variant=structural_variant,
    )


def _intersection_volume(first: Any, second: Any) -> float:
    intersection = first.intersect(second)
    if intersection is None:
        return 0.0
    return sum(float(shape.volume) for shape in intersection if hasattr(shape, "volume"))


def find_interferences(model: SkeletonModel, tolerance_mm3: float = 1e-6) -> tuple[dict[str, Any], ...]:
    """Report solid overlaps, excluding documented interface/process overlaps."""

    findings: list[dict[str, Any]] = []
    for index, first in enumerate(model.components):
        if first.category in {"reference", "motion-reference", "process-envelope"}:
            continue
        for second in model.components[index + 1 :]:
            if second.category in {"reference", "motion-reference", "process-envelope"}:
                continue
            pair = frozenset((first.name, second.name))
            volume = _intersection_volume(first.shape, second.shape)
            if volume <= tolerance_mm3:
                continue
            findings.append(
                {
                    "first": first.name,
                    "second": second.name,
                    "volume_mm3": volume,
                    "expected": pair in model.expected_interference_pairs,
                }
            )
    return tuple(findings)


def unexpected_interferences(model: SkeletonModel) -> tuple[dict[str, Any], ...]:
    """Return only overlaps not documented as process or interface contact."""

    return tuple(item for item in find_interferences(model) if not item["expected"])


def export_skeleton(model: SkeletonModel, output_dir: Path) -> dict[str, Path]:
    """Export review-only STEP and STL derivatives to an explicit temp folder."""

    build123d = _build123d()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{model.variant}-{model.candidate_id.value.lower()}-architecture-skeleton"
    step_path = output_dir / f"{stem}.step"
    stl_path = output_dir / f"{stem}.stl"
    build123d.export_step(model.compound, step_path)
    build123d.export_stl(
        model.compound,
        stl_path,
        tolerance=0.01,
        angular_tolerance=0.2,
    )
    return {"step": step_path, "stl": stl_path}
