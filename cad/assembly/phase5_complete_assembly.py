"""Complete virtual Phase 5 assembly and hardware-envelope model.

Structural parts are inserted from local manufacturing geometry.  Hardware is
represented by named, conservative envelopes until the owner identifies and
measures the exact rails, screws, drivers, spindle, switches, and controller
revision.  The assembly is a compound by design: it preserves serviceable
part boundaries and records intentional interfaces instead of hiding them in
one boolean solid.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from cad.parameters import PHASE5_COMPLETE_PARAMETERS, Phase5CompleteMachineParameters
from cad.parts.phase5_complete_structural import (
    PHASE5_COMPLETE_PART_IDS,
    build_phase5_complete_structural_parts,
)


@dataclass(frozen=True)
class CompleteAssemblyComponent:
    """One named component in the complete machine assembly."""

    name: str
    category: str
    shape: Any
    source: str
    serviceable: bool
    provisional: bool
    expected_overlap_with: tuple[str, ...] = ()
    notes: str = ""


@dataclass
class CompleteMachineAssembly:
    """Assembly result with stable component names and validation metadata."""

    parameters: Phase5CompleteMachineParameters
    components: tuple[CompleteAssemblyComponent, ...]
    expected_interference_pairs: tuple[frozenset[str], ...]
    travel_state: tuple[float, float, float]
    master_shape: Any

    @property
    def component_map(self) -> dict[str, CompleteAssemblyComponent]:
        return {component.name: component for component in self.components}

    @property
    def structural_components(self) -> tuple[CompleteAssemblyComponent, ...]:
        return tuple(component for component in self.components if component.category == "printed-structural")

    @property
    def hardware_components(self) -> tuple[CompleteAssemblyComponent, ...]:
        return tuple(component for component in self.components if component.category != "printed-structural")


def _build123d() -> Any:
    try:
        import build123d
    except ImportError as exc:  # pragma: no cover - CAD runner only
        raise RuntimeError("Complete assembly requires build123d") from exc
    return build123d


def _box(bd: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], label: str) -> Any:
    shape = bd.Box(*size, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)).located(bd.Location(minimum))
    shape.label = label
    return shape


def _cylinder_axis(bd: Any, radius: float, length: float, start: tuple[float, float, float], axis: str, label: str) -> Any:
    rotations = {"x": (0.0, 90.0, 0.0), "y": (-90.0, 0.0, 0.0), "z": (0.0, 0.0, 0.0)}
    shape = bd.Cylinder(
        radius,
        length,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    ).located(bd.Location(start, rotations[axis]))
    shape.label = label
    return shape


def _placed(shape: Any, position: tuple[float, float, float], label: str | None = None) -> Any:
    result = shape.located(_build123d().Location(position))
    if label:
        result.label = label
    return result


def _component(
    name: str,
    category: str,
    shape: Any,
    *,
    source: str,
    serviceable: bool = True,
    provisional: bool = True,
    expected_overlap_with: Iterable[str] = (),
    notes: str = "",
) -> CompleteAssemblyComponent:
    shape.label = name
    return CompleteAssemblyComponent(
        name=name,
        category=category,
        shape=shape,
        source=source,
        serviceable=serviceable,
        provisional=provisional,
        expected_overlap_with=tuple(expected_overlap_with),
        notes=notes,
    )


def _structural_components(
    parts: dict[str, Any],
    parameters: Phase5CompleteMachineParameters,
    *,
    x_position: float,
    y_position: float,
    z_offset: float,
) -> list[CompleteAssemblyComponent]:
    positions: dict[str, tuple[float, float, float]] = {
        **dict(parameters.base_pair_placements_mm),
        "base_center_tie": parameters.center_tie_placement_mm,
        **dict(parameters.gantry_placements_mm),
        "x_z_backbone": parameters.x_z_backbone_placement_mm,
        "z_carriage_plate": tuple(a + b for a, b in zip(parameters.z_carriage_placement_mm, (x_position, 0.0, z_offset))),
        "spindle_mount_concept": tuple(a + b for a, b in zip(parameters.spindle_mount_placement_mm, (x_position, 0.0, z_offset))),
        "moving_bed_frame": tuple(a + b for a, b in zip(parameters.moving_bed_placement_mm, (0.0, y_position, 0.0))),
        **dict(parameters.x_bearing_placements_mm),
        **dict(parameters.y_service_placements_mm),
        **dict(parameters.foot_placements_mm),
        "electronics_mount_rail": parameters.electronics_rail_placement_mm,
    }
    overlap_map = {
        "base_left_integrated": ("base_center_tie", "gantry_left_integrated", "machine_foot_front_left", "machine_foot_rear_left"),
        "base_right_integrated": ("base_center_tie", "gantry_right_integrated", "machine_foot_front_right", "machine_foot_rear_right"),
        "gantry_left_integrated": ("base_left_integrated", "gantry_right_integrated", "x_z_backbone"),
        "gantry_right_integrated": ("base_right_integrated", "gantry_left_integrated", "x_z_backbone"),
        "x_z_backbone": ("gantry_left_integrated", "gantry_right_integrated", "z_carriage_plate"),
        "z_carriage_plate": ("x_z_backbone", "spindle_mount_concept"),
        "spindle_mount_concept": ("z_carriage_plate",),
        "moving_bed_frame": ("base_left_integrated", "base_right_integrated"),
    }
    result: list[CompleteAssemblyComponent] = []
    for part_id in PHASE5_COMPLETE_PART_IDS:
        result.append(
            _component(
                part_id,
                "printed-structural",
                _placed(parts[part_id], positions[part_id], part_id),
                source="cad/parts/phase5_complete_structural.py",
                serviceable=part_id not in {"base_left_integrated", "base_right_integrated", "gantry_left_integrated", "gantry_right_integrated"},
                expected_overlap_with=overlap_map.get(part_id, ()),
                notes="Local single-solid PETG candidate; all unmeasured interfaces remain provisional.",
            )
        )
    return result


def _motion_components(
    bd: Any,
    parameters: Phase5CompleteMachineParameters,
    *,
    x_position: float,
    y_position: float,
    z_offset: float,
) -> list[CompleteAssemblyComponent]:
    components: list[CompleteAssemblyComponent] = []

    def add(name: str, category: str, shape: Any, **kwargs: Any) -> None:
        components.append(_component(name, category, shape, source="cad/assembly/phase5_complete_assembly.py", **kwargs))

    # X fixed rails and their four carriage envelopes.
    for name, z in (("x_rail_lower", 73.0), ("x_rail_upper", 133.0)):
        add(name, "linear-guide", _box(bd, (340.0, 12.0, 8.0), (-170.0, -104.0, z), name), serviceable=False, expected_overlap_with=("gantry_left_integrated", "gantry_right_integrated"), notes="MGN12 screening envelope; hole pattern and rail height are provisional.")
    for rail_name, z in (("lower", 70.0), ("upper", 130.0)):
        for index, x in enumerate((-42.0, 16.0), start=1):
            add(f"x_carriage_{rail_name}_{index}", "linear-guide", _box(bd, (26.0, 24.0, 20.0), (x + x_position, -110.0, z), f"x_carriage_{rail_name}_{index}"), serviceable=True, expected_overlap_with=("x_z_backbone",), notes="MGN12H carriage screening envelope.")

    # X screw, nut, drive and bearing envelopes.
    add("x_lead_screw", "transmission", _cylinder_axis(bd, 4.0, parameters.x_screw_length_mm, (-180.0, -65.0, 98.0), "x", "x_lead_screw"), serviceable=True, expected_overlap_with=("x_fixed_bearing_cartridge", "x_floating_bearing_cartridge", "x_z_backbone"), notes="T8x4 screening axis; exact screw and nut remain provisional.")
    add("x_lead_nut", "transmission", _box(bd, (24.0, 24.0, 20.0), (-12.0 + x_position, -77.0, 88.0), "x_lead_nut"), serviceable=True, expected_overlap_with=("x_z_backbone",), notes="Anti-backlash nut envelope; exact nut length and flange unmeasured.")
    add("x_motor_nema17", "motor", _box(bd, (48.0, 52.0, 52.0), (-274.0, -91.0, 72.0), "x_motor_nema17"), serviceable=True, expected_overlap_with=("x_fixed_bearing_cartridge",), notes="Owner-stock NEMA17 envelope; body length and connector position are not selected.")
    add("x_motor_connector_clearance", "cable", _box(bd, (20.0, 34.0, 24.0), (-226.0, -82.0, 86.0), "x_motor_connector_clearance"), serviceable=True, expected_overlap_with=("x_motor_nema17",), notes="Rear/side wiring clearance allowance.")
    add("x_coupler", "transmission", _cylinder_axis(bd, 8.0, 24.0, (-204.0, -65.0, 98.0), "x", "x_coupler"), serviceable=True, expected_overlap_with=("x_lead_screw", "x_fixed_bearing_cartridge"), notes="Flexible-coupler envelope; vendor dimensions provisional.")

    # Y moving bed guides, screw, service interfaces, and motor.
    for name, x in (("y_rail_left", -116.0), ("y_rail_right", 104.0)):
        add(name, "linear-guide", _box(bd, (12.0, 310.0, 8.0), (x, -155.0, -12.0), name), serviceable=False, expected_overlap_with=("base_left_integrated", "base_right_integrated", "moving_bed_frame"), notes="MGN12 screening envelope; PETG seat/shim and hole pattern are provisional.")
    for x_name, x in (("left", -122.0), ("right", 98.0)):
        for index, y in enumerate((-67.5, 32.5), start=1):
            add(f"y_carriage_{x_name}_{index}", "linear-guide", _box(bd, (24.0, 28.0, 20.0), (x, y + y_position, -12.0), f"y_carriage_{x_name}_{index}"), serviceable=True, expected_overlap_with=("moving_bed_frame",), notes="MGN12H moving-bed carriage envelope.")
    add("y_lead_screw", "transmission", _cylinder_axis(bd, 4.0, parameters.y_screw_length_mm, (0.0, -165.0, -35.0), "y", "y_lead_screw"), serviceable=True, expected_overlap_with=("y_motor_service_pocket", "y_fixed_bearing_cartridge", "y_floating_bearing_cartridge", "moving_bed_frame"), notes="T8x4 screening axis; exact screw, nut, and bearing stack remain provisional.")
    add("y_lead_nut", "transmission", _box(bd, (40.0, 34.0, 16.0), (-20.0, -17.0 + y_position, -43.0), "y_lead_nut"), serviceable=True, expected_overlap_with=("moving_bed_frame",), notes="Moving anti-backlash nut envelope.")
    add("y_motor_nema17", "motor", _box(bd, (52.0, 48.0, 52.0), (-26.0, -220.0, -61.0), "y_motor_nema17"), serviceable=True, expected_overlap_with=("y_motor_service_pocket",), notes="Owner-stock NEMA17 envelope with body-length clearance strategy.")
    add("y_motor_connector_clearance", "cable", _box(bd, (28.0, 20.0, 28.0), (-14.0, -172.0, -49.0), "y_motor_connector_clearance"), serviceable=True, expected_overlap_with=("y_motor_nema17", "y_coupler"), notes="Front/rear connector access allowance.")
    add("y_coupler", "transmission", _cylinder_axis(bd, 8.0, 24.0, (0.0, -172.0, -35.0), "y", "y_coupler"), serviceable=True, expected_overlap_with=("y_lead_screw", "y_motor_nema17"), notes="Flexible-coupler envelope.")

    # Z guides, transmission, motor, and spindle/tool envelopes.
    for name, x in (("z_rail_left", -34.0), ("z_rail_right", 26.0)):
        add(name, "linear-guide", _box(bd, (8.0, 8.0, 130.0), (x, -111.0, 16.0), name), serviceable=False, expected_overlap_with=("x_z_backbone",), notes="MGN9 screening envelope; exact rail and block interfaces are provisional.")
    for rail_name, x in (("left", -38.0), ("right", 22.0)):
        for index, z in enumerate((30.0, 92.0), start=1):
            add(f"z_carriage_{rail_name}_{index}", "linear-guide", _box(bd, (16.0, 30.0, 26.0), (x, -116.0, z + z_offset), f"z_carriage_{rail_name}_{index}"), serviceable=True, expected_overlap_with=("z_carriage_plate",), notes="MGN9H carriage envelope.")
    add("z_lead_screw", "transmission", _cylinder_axis(bd, 4.0, parameters.z_screw_length_mm, (0.0, -65.0, 10.0), "z", "z_lead_screw"), serviceable=True, expected_overlap_with=("x_z_backbone", "z_carriage_plate", "z_motor_nema17"), notes="T8x2 screening axis; exact nut and bearing stack remain provisional.")
    add("z_lead_nut", "transmission", _box(bd, (22.0, 22.0, 20.0), (-11.0, -76.0, 55.0 + z_offset), "z_lead_nut"), serviceable=True, expected_overlap_with=("z_carriage_plate",), notes="Moving anti-backlash nut envelope.")
    add("z_motor_nema17", "motor", _box(bd, (52.0, 52.0, 48.0), (-26.0, -91.0, 145.0), "z_motor_nema17"), serviceable=True, expected_overlap_with=("x_z_backbone", "z_coupler"), notes="Owner-stock NEMA17 envelope; strongest suitable stock motor is selected only after characterization.")
    add("z_coupler", "transmission", _cylinder_axis(bd, 8.0, 24.0, (0.0, -65.0, 145.0), "z", "z_coupler"), serviceable=True, expected_overlap_with=("z_lead_screw", "z_motor_nema17"), notes="Flexible-coupler envelope.")
    add("spindle_envelope", "spindle", _cylinder_axis(bd, 26.0, 100.0, (0.0 + x_position, 10.0, 20.0 + z_offset), "z", "spindle_envelope"), serviceable=True, expected_overlap_with=("spindle_mount_concept", "z_carriage_plate", "tool_envelope"), notes="Parametric 52 mm maximum screening body; ER11/diameter/mass remain provisional.")
    add("tool_envelope", "spindle", _cylinder_axis(bd, 2.0, 45.0, (0.0 + x_position, 10.0, -25.0 + z_offset), "z", "tool_envelope"), serviceable=True, expected_overlap_with=("spindle_envelope", "pcb_envelope", "spoilboard"), notes="Tool and collet clearance envelope, not a cutter selection.")

    return components


def _bed_and_process_components(
    bd: Any,
    parameters: Phase5CompleteMachineParameters,
    *,
    y_position: float,
    x_position: float,
    z_offset: float,
) -> list[CompleteAssemblyComponent]:
    components: list[CompleteAssemblyComponent] = []

    def add(name: str, category: str, shape: Any, **kwargs: Any) -> None:
        components.append(_component(name, category, shape, source="cad/assembly/phase5_complete_assembly.py", **kwargs))

    add("spoilboard", "workholding", _box(bd, parameters.spoilboard_size_mm, (-115.0, -90.0 + y_position, -12.0), "spoilboard"), serviceable=True, provisional=True, expected_overlap_with=("moving_bed_frame", "pcb_envelope", "tool_envelope"), notes="Replaceable 230 x 180 x 12 screening envelope.")
    add("pcb_envelope", "workholding", _box(bd, (200.0, 150.0, parameters.pcb_nominal_thickness_mm), (-100.0, -75.0 + y_position, 0.0), "pcb_envelope"), serviceable=True, provisional=True, expected_overlap_with=("spoilboard", "workholding_clamp_front", "workholding_clamp_rear", "tool_envelope"), notes="Nominal 200 x 150 usable work area; board thickness is a process assumption.")
    for name, x, y in (("workholding_clamp_front", -92.0, -82.0), ("workholding_clamp_rear", -92.0, 74.0), ("workholding_clamp_right", 92.0, -4.0)):
        add(name, "workholding", _box(bd, (16.0, 8.0, 8.0), (x, y + y_position, 1.6), name), serviceable=True, provisional=True, expected_overlap_with=("pcb_envelope", "spoilboard"), notes="Generic low-profile clamp envelope; exact workholding remains open.")
    add("conductive_probe", "probe", _box(bd, (18.0, 18.0, 12.0), (80.0, 50.0 + y_position, 2.0), "conductive_probe"), serviceable=True, provisional=True, expected_overlap_with=("pcb_envelope", "spoilboard"), notes="Probe parking/measurement envelope; exact sensor and bracket remain open.")
    add("probe_cable_route", "cable", _box(bd, (8.0, 90.0, 8.0), (85.0, 45.0 + y_position, 8.0), "probe_cable_route"), serviceable=True, provisional=True, expected_overlap_with=("conductive_probe", "moving_bed_frame"), notes="Service-loop clearance allowance.")
    return components


def _control_and_service_components(bd: Any) -> list[CompleteAssemblyComponent]:
    components: list[CompleteAssemblyComponent] = []

    def add(name: str, category: str, shape: Any, **kwargs: Any) -> None:
        components.append(_component(name, category, shape, source="cad/assembly/phase5_complete_assembly.py", **kwargs))

    # The board envelope is intentionally generic: it records owner hardware
    # without inventing a shield revision or driver pinout.
    add("arduino_mega_owner_hardware", "controller", _box(bd, (102.0, 54.0, 15.0), (-100.0, 150.0, 7.0), "arduino_mega_owner_hardware"), serviceable=True, expected_overlap_with=("electronics_mount_rail", "cnc_shield_owner_hardware"), notes="OWNER-SUPPLIED Arduino Mega envelope; board revision and connector clearance to be measured.")
    add("cnc_shield_owner_hardware", "controller", _box(bd, (80.0, 60.0, 15.0), (-88.0, 147.0, 22.0), "cnc_shield_owner_hardware"), serviceable=True, expected_overlap_with=("arduino_mega_owner_hardware", "electronics_mount_rail"), notes="OWNER-SUPPLIED Arduino Mega + CNC Shield platform; exact shield revision and drivers unresolved.")
    add("driver_cooling_clearance", "controller", _box(bd, (86.0, 68.0, 28.0), (-91.0, 143.0, 37.0), "driver_cooling_clearance"), serviceable=True, provisional=True, expected_overlap_with=("cnc_shield_owner_hardware",), notes="Clearance placeholder; driver type, current, voltage, and cooling are identification items.")
    add("controller_cable_service_loop", "cable", _box(bd, (24.0, 110.0, 18.0), (5.0, 145.0, 8.0), "controller_cable_service_loop"), serviceable=True, provisional=True, expected_overlap_with=("arduino_mega_owner_hardware", "cnc_shield_owner_hardware"), notes="Cable-route envelope only; do not infer pin assignments.")
    add("x_home_limit", "limit", _box(bd, (18.0, 18.0, 18.0), (-176.0, -120.0, 56.0), "x_home_limit"), serviceable=True, provisional=True, expected_overlap_with=("x_rail_lower",), notes="Switch mounting envelope; exact switch body and actuation direction open.")
    add("y_home_limit", "limit", _box(bd, (18.0, 18.0, 18.0), (-132.0, -164.0, -25.0), "y_home_limit"), serviceable=True, provisional=True, expected_overlap_with=("y_rail_left",), notes="Switch mounting envelope.")
    add("z_home_limit", "limit", _box(bd, (18.0, 18.0, 18.0), (50.0, -90.0, 142.0), "z_home_limit"), serviceable=True, provisional=True, expected_overlap_with=("z_rail_right", "z_motor_nema17"), notes="Switch mounting envelope.")
    add("motor_cable_route", "cable", _box(bd, (18.0, 260.0, 14.0), (150.0, -130.0, 150.0), "motor_cable_route"), serviceable=True, provisional=True, expected_overlap_with=("x_motor_nema17", "z_motor_nema17"), notes="High-level service route; preserve bend radius and moving slack in detailed harness design.")
    add("moving_bed_cable_loop", "cable", _box(bd, (16.0, 80.0, 30.0), (125.0, -40.0, -5.0), "moving_bed_cable_loop"), serviceable=True, provisional=True, expected_overlap_with=("moving_bed_frame", "probe_cable_route"), notes="Moving Y cable loop clearance placeholder.")
    add("machine_feet_hardware", "support", _box(bd, (300.0, 260.0, 4.0), (-150.0, -130.0, -80.0), "machine_feet_hardware"), serviceable=True, provisional=True, expected_overlap_with=("machine_foot_front_left", "machine_foot_front_right", "machine_foot_rear_left", "machine_foot_rear_right"), notes="Support surface / foot contact envelope, not a purchased component.")
    return components


def _expected_interference_pairs() -> tuple[frozenset[str], ...]:
    pairs = {
        frozenset(pair)
        for component in (
            *_structural_expected_pairs(),
        )
        for pair in component
    }
    return tuple(sorted(pairs, key=lambda pair: tuple(sorted(pair))))


def _structural_expected_pairs() -> list[tuple[tuple[str, str], ...]]:
    return [
        (("base_left_integrated", "base_center_tie"), ("base_right_integrated", "base_center_tie")),
        (("base_left_integrated", "gantry_left_integrated"), ("base_right_integrated", "gantry_right_integrated")),
        (("gantry_left_integrated", "gantry_right_integrated"),),
        (("x_z_backbone", "z_carriage_plate"), ("z_carriage_plate", "spindle_mount_concept")),
        (("moving_bed_frame", "spoilboard"), ("spoilboard", "pcb_envelope")),
    ]


def build_phase5_complete_assembly(
    parameters: Phase5CompleteMachineParameters = PHASE5_COMPLETE_PARAMETERS,
    *,
    x_position: float = 0.0,
    y_position: float = 0.0,
    z_offset: float = 0.0,
    include_hardware: bool = True,
) -> CompleteMachineAssembly:
    """Build the complete assembly at one valid X/Y/Z travel state."""

    bd = _build123d()
    parts = build_phase5_complete_structural_parts()
    components = _structural_components(
        parts,
        parameters,
        x_position=x_position,
        y_position=y_position,
        z_offset=z_offset,
    )
    if include_hardware:
        components.extend(_motion_components(bd, parameters, x_position=x_position, y_position=y_position, z_offset=z_offset))
        components.extend(_bed_and_process_components(bd, parameters, y_position=y_position, x_position=x_position, z_offset=z_offset))
        components.extend(_control_and_service_components(bd))
    master = bd.Compound(children=[component.shape for component in components])
    master.label = "pcb_cnc_complete_assembly"
    return CompleteMachineAssembly(
        parameters=parameters,
        components=tuple(components),
        expected_interference_pairs=_expected_interference_pairs(),
        travel_state=(x_position, y_position, z_offset),
        master_shape=master,
    )


def build_phase5_travel_state(
    x_position: float,
    y_position: float,
    z_offset: float,
    *,
    parameters: Phase5CompleteMachineParameters = PHASE5_COMPLETE_PARAMETERS,
) -> CompleteMachineAssembly:
    """Convenience wrapper used by motion-extreme validation."""

    return build_phase5_complete_assembly(
        parameters,
        x_position=x_position,
        y_position=y_position,
        z_offset=z_offset,
        include_hardware=True,
    )


__all__ = [
    "CompleteAssemblyComponent",
    "CompleteMachineAssembly",
    "build_phase5_complete_assembly",
    "build_phase5_travel_state",
]
