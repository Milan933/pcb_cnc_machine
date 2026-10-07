"""Complete hardware-first master assembly for the PCB CNC.

This module is the primary design object for the redesign.  Hardware is
placed first from the controlled master parameters; derived PETG structure is
then placed around it.  The component records carry an explicit support and
fastening answer so a visually plausible but physically floating component
cannot silently pass review.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from cad.hardware.master_hardware import (
    build_608_bearing,
    build_arduino_mega,
    build_conductive_probe,
    build_cnc_shield,
    build_d2f_limit_switch,
    build_fastener_envelope,
    build_flexible_coupler,
    build_mgn_carriage,
    build_mgn_rail,
    build_nema17,
    build_spindle_candidate,
    build_t8_nut,
    build_t8_screw,
)
from cad.parameters import PHASE5_MASTER_PARAMETERS, Phase5MasterMachineParameters
from cad.parts.master_structural import MASTER_PART_IDS, build_master_structural_parts


@dataclass(frozen=True)
class MasterAssemblyComponent:
    name: str
    category: str
    shape: Any
    source: str
    supporting_part: str
    fastening_method: str
    confidence: str
    serviceable: bool = True
    provisional: bool = True
    expected_overlap_with: tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class MasterMachineAssembly:
    parameters: Phase5MasterMachineParameters
    components: tuple[MasterAssemblyComponent, ...]
    expected_interference_pairs: tuple[frozenset[str], ...]
    travel_state: tuple[float, float, float]
    master_shape: Any

    @property
    def component_map(self) -> dict[str, MasterAssemblyComponent]:
        return {component.name: component for component in self.components}

    @property
    def structural_components(self) -> tuple[MasterAssemblyComponent, ...]:
        return tuple(component for component in self.components if component.category == "printed-structural")

    @property
    def hardware_components(self) -> tuple[MasterAssemblyComponent, ...]:
        return tuple(component for component in self.components if component.category != "printed-structural")

    @property
    def support_audit(self) -> tuple[dict[str, str], ...]:
        return tuple(
            {
                "component": component.name,
                "supporting_part": component.supporting_part,
                "fastening_method": component.fastening_method,
                "confidence": component.confidence,
            }
            for component in self.components
        )


def _build123d() -> Any:
    import build123d

    return build123d


def _placed(shape: Any, position: tuple[float, float, float], label: str | None = None, rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Any:
    bd = _build123d()
    # ``moved`` preserves the local orientation and axis datum of a derived
    # hardware model.  ``located`` would replace the shape location and can
    # silently turn an oriented NEMA17 or screw into an unrotated envelope.
    result = shape.moved(bd.Location(position, rotation))
    if label:
        result.label = label
    return result


def _box(bd: Any, size: tuple[float, float, float], minimum: tuple[float, float, float], label: str) -> Any:
    shape = bd.Box(*size, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)).located(bd.Location(minimum))
    shape.label = label
    return shape


def _cylinder_axis(bd: Any, radius: float, length: float, start: tuple[float, float, float], axis: str, label: str) -> Any:
    rotations = {"x": (0.0, 90.0, 0.0), "y": (-90.0, 0.0, 0.0), "z": (0.0, 0.0, 0.0)}
    shape = bd.Cylinder(radius, length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).located(bd.Location(start, rotations[axis]))
    shape.label = label
    return shape


def _component(
    name: str,
    category: str,
    shape: Any,
    *,
    supporting_part: str,
    fastening_method: str,
    source: str,
    confidence: str = "reference",
    serviceable: bool = True,
    provisional: bool = True,
    expected_overlap_with: Iterable[str] = (),
    notes: str = "",
) -> MasterAssemblyComponent:
    shape.label = name
    return MasterAssemblyComponent(
        name=name,
        category=category,
        shape=shape,
        source=source,
        supporting_part=supporting_part,
        fastening_method=fastening_method,
        confidence=confidence,
        serviceable=serviceable,
        provisional=provisional,
        expected_overlap_with=tuple(expected_overlap_with),
        notes=notes,
    )


def _structural_components(parts: dict[str, Any], p: Phase5MasterMachineParameters, *, x_position: float, y_position: float, z_offset: float) -> list[MasterAssemblyComponent]:
    placements = {
        "base_left_integrated": p.base_left_placement_mm,
        "base_right_integrated": p.base_right_placement_mm,
        "base_center_tie": (-130.0, -160.0, -48.0),
        "y_motor_service_pocket": (-30.0, -195.0, -115.0),
        "y_fixed_bearing_cartridge": (-26.0, -180.0, -79.0),
        "y_floating_bearing_cartridge": (-26.0, 145.0, -79.0),
        "y_rear_bearing_bridge": (-130.0, 145.0, -90.0),
        "machine_foot_front_left": (-170.0, -155.0, -70.0),
        "machine_foot_front_right": (120.0, -155.0, -70.0),
        "machine_foot_rear_left": (-170.0, 105.0, -70.0),
        "machine_foot_rear_right": (120.0, 105.0, -70.0),
        "electronics_mount_rail": (-130.0, 150.0, 5.0),
        "gantry_left_integrated": (-180.0, -30.0, -60.0),
        "gantry_right_integrated": (-25.0, -30.0, -60.0),
        "x_fixed_bearing_cartridge": (-185.0, -65.0, 82.0),
        "x_floating_bearing_cartridge": (115.0, -65.0, 82.0),
        "x_z_backbone": (-57.5 + x_position, -62.0, 50.0),
        "z_carriage_plate": (-52.5 + x_position, -60.0, 30.0 + z_offset),
        "spindle_mount_concept": (-52.5 + x_position, -28.0, 35.0 + z_offset),
        "moving_bed_frame": (-125.0, -115.0 + y_position, -40.0),
    }
    supports = {
        "base_left_integrated": "machine_foot_front_left + machine_foot_rear_left",
        "base_right_integrated": "machine_foot_front_right + machine_foot_rear_right",
        "base_center_tie": "base_left_integrated + base_right_integrated",
        "y_motor_service_pocket": "base_center_tie + front base datums",
        "y_fixed_bearing_cartridge": "base_center_tie + base rail-end datum",
        "y_floating_bearing_cartridge": "y_rear_bearing_bridge + left-base rear datum",
        "y_rear_bearing_bridge": "base_left_integrated rear datum",
        "machine_foot_front_left": "support surface",
        "machine_foot_front_right": "support surface",
        "machine_foot_rear_left": "support surface",
        "machine_foot_rear_right": "support surface",
        "electronics_mount_rail": "base_left_integrated + base_right_integrated rear datum",
        "gantry_left_integrated": "base_left_integrated",
        "gantry_right_integrated": "base_right_integrated",
        "x_fixed_bearing_cartridge": "gantry_left_integrated",
        "x_floating_bearing_cartridge": "gantry_right_integrated",
        "x_z_backbone": "x_carriages and X guide plane",
        "z_carriage_plate": "z carriages on x_z_backbone",
        "spindle_mount_concept": "z_carriage_plate replaceable clamp land",
        "moving_bed_frame": "Y carriages on y rails",
    }
    fasteners = {
        "base_left_integrated": "M4 heat-set/through interface at feet; printed base shoulder carries shear",
        "base_right_integrated": "M4 heat-set/through interface at feet; printed base shoulder carries shear",
        "base_center_tie": "M4 inserts/through-bolts; end keys carry location and shear",
        "y_motor_service_pocket": "M4 structural joint; face shoulder carries motor reaction",
        "y_fixed_bearing_cartridge": "M4 retainers around 608 bearing pair; housing carries radial load",
        "y_floating_bearing_cartridge": "M4 retainer around 608 bearing; housing permits axial float",
        "y_rear_bearing_bridge": "M4 through-bolts into the left base side; bridge carries radial reaction",
        "machine_foot_front_left": "M4 through-bolt and washer to base",
        "machine_foot_front_right": "M4 through-bolt and washer to base",
        "machine_foot_rear_left": "M4 through-bolt and washer to base",
        "machine_foot_rear_right": "M4 through-bolt and washer to base",
        "electronics_mount_rail": "M4 base joint plus M3 controller slots",
        "gantry_left_integrated": "M4 base preload; keyed beam tongue carries beam shear",
        "gantry_right_integrated": "M4 base preload; keyed beam socket carries beam shear",
        "x_fixed_bearing_cartridge": "M4 bearing housing fasteners; gantry seat carries reaction",
        "x_floating_bearing_cartridge": "M4 bearing housing fasteners; radial seat preserves float",
        "x_z_backbone": "M3 carriage fasteners; rail shoulders carry alignment",
        "z_carriage_plate": "M3 carriage fasteners; Z backplate carries moment",
        "spindle_mount_concept": "M4 removable clamp bolts; ring and rear plate carry shear",
        "moving_bed_frame": "M3/M4 carriage and nut fasteners; bed ribs carry load",
    }
    result: list[MasterAssemblyComponent] = []
    for part_id in MASTER_PART_IDS:
        result.append(
            _component(
                part_id,
                "printed-structural",
                _placed(parts[part_id], placements[part_id], part_id),
                supporting_part=supports[part_id],
                fastening_method=fasteners[part_id],
                source="cad/parts/master_structural.py",
                confidence="local parametric source",
                serviceable=part_id not in {"base_left_integrated", "base_right_integrated", "gantry_left_integrated", "gantry_right_integrated"},
                notes="Derived from master hardware layout; supplier-dependent fit remains provisional.",
            )
        )
    return result


def _motion_components(bd: Any, p: Phase5MasterMachineParameters, *, x_position: float, y_position: float, z_offset: float) -> list[MasterAssemblyComponent]:
    result: list[MasterAssemblyComponent] = []

    def add(name: str, category: str, shape: Any, **kwargs: Any) -> None:
        result.append(_component(name, category, shape, source="cad/hardware/master_hardware.py", **kwargs))

    # Hardware is placed from the master datum before derived printed parts.
    for name, z in (("x_rail_lower", p.x_rail_z_mm[0]), ("x_rail_upper", p.x_rail_z_mm[1])):
        add(name, "linear-guide", _placed(build_mgn_rail("x", p.x_rail_length_mm, size=12, label=name), (-p.x_rail_length_mm / 2.0, p.x_rail_y_mm, z), name), supporting_part="gantry_left_integrated + gantry_right_integrated", fastening_method="M3 rail fasteners through rail holes; printed shoulders carry alignment", confidence="HIWIN reference dimensions", expected_overlap_with=("gantry_left_integrated", "gantry_right_integrated"), notes="MGN12 rail reference section and 25 mm hole pitch; actual rail/preload must be measured.")
        for index, x in enumerate((x_position - 35.0, x_position + 10.0), start=1):
            carriage_name = f"{name.replace('rail', 'carriage')}_{index}"
            add(carriage_name, "linear-guide", _placed(build_mgn_carriage("x", size=12, label=carriage_name), (x, p.x_rail_y_mm - 7.5, z + 8.0), carriage_name), supporting_part="x_z_backbone", fastening_method="M3 carriage screws into backbone inserts", confidence="HIWIN reference dimensions", expected_overlap_with=("x_z_backbone",), notes="MGN12H carriage envelope.")

    add("x_lead_screw", "transmission", _placed(build_t8_screw("x", p.x_screw_length_mm, p.x_y_screw_lead_mm, label="x_lead_screw"), (-p.x_screw_length_mm / 2.0, p.x_screw_y_mm, p.x_screw_z_mm), "x_lead_screw"), supporting_part="x_fixed_bearing_cartridge + x_floating_bearing_cartridge", fastening_method="Fixed/floating 608 bearing stack; coupler carries torque only", confidence="T8 envelope", expected_overlap_with=("x_fixed_bearing_cartridge", "x_floating_bearing_cartridge", "x_lead_nut"), notes="Non-helical T8x4 representation; journal dimensions remain provisional.")
    add("x_lead_nut", "transmission", _placed(build_t8_nut(label="x_lead_nut"), (x_position - 12.0, p.x_screw_y_mm - 12.0, p.x_screw_z_mm - 12.0), "x_lead_nut", rotation=(0.0, 90.0, 0.0)), supporting_part="x_z_backbone", fastening_method="M4 nut-flange fasteners; printed pocket carries reaction", confidence="nut envelope", expected_overlap_with=("x_z_backbone", "x_lead_screw"), notes="Anti-backlash architecture candidate; actual nut flange must be measured.")
    add("x_motor_nema17", "motor", _placed(build_nema17("x", label="x_motor_nema17"), (-190.0, p.x_screw_y_mm, p.x_screw_z_mm), "x_motor_nema17"), supporting_part="x_fixed_bearing_cartridge", fastening_method="NEMA17 M3/M4 face fasteners; face pilot locates motor", confidence="generic NEMA17 interface", expected_overlap_with=("x_fixed_bearing_cartridge", "x_coupler"), notes="Owner-stock motor; 40-48 mm body and connector clearance are modeled.")
    add("x_coupler", "transmission", _placed(build_flexible_coupler("x", label="x_coupler"), (-180.0, p.x_screw_y_mm, p.x_screw_z_mm), "x_coupler"), supporting_part="x_fixed_bearing_cartridge + x_motor_nema17", fastening_method="Two-bore clamp screws; no axial support", confidence="MISUMI reference envelope", expected_overlap_with=("x_lead_screw", "x_motor_nema17"), notes="Representative 5/8 mm coupler envelope.")

    for name, x in (("y_rail_left", p.y_rail_center_x_mm[0]), ("y_rail_right", p.y_rail_center_x_mm[1])):
        add(name, "linear-guide", _placed(build_mgn_rail("y", p.y_rail_length_mm, size=12, label=name), (x - 6.0, p.y_rail_start_y_mm, p.y_rail_z_mm), name), supporting_part="base_left_integrated + base_right_integrated", fastening_method="M3 rail fasteners through reference holes; continuous PETG shoulder carries alignment", confidence="HIWIN reference dimensions", expected_overlap_with=("base_left_integrated", "base_right_integrated"), notes="MGN12 rail reference section; rail datum and preload are not owner-measured.")
        side = "left" if x < 0 else "right"
        for index, y in enumerate((-60.0 + y_position, 35.0 + y_position), start=1):
            carriage_name = f"y_carriage_{side}_{index}"
            add(carriage_name, "linear-guide", _placed(build_mgn_carriage("y", size=12, label=carriage_name), (x - 7.5, y, p.y_rail_z_mm + 8.0), carriage_name), supporting_part="moving_bed_frame", fastening_method="M3 carriage screws into bed inserts", confidence="HIWIN reference dimensions", expected_overlap_with=("moving_bed_frame",), notes="MGN12H moving-bed carriage envelope.")

    add("y_lead_screw", "transmission", _placed(build_t8_screw("y", p.y_screw_length_mm, p.x_y_screw_lead_mm, label="y_lead_screw"), (p.y_screw_x_mm, -155.0, p.y_screw_z_mm), "y_lead_screw"), supporting_part="y_fixed_bearing_cartridge + y_floating_bearing_cartridge", fastening_method="Fixed/floating 608 bearing stack; coupler carries torque only", confidence="T8 envelope", expected_overlap_with=("y_fixed_bearing_cartridge", "y_floating_bearing_cartridge", "y_lead_nut"), notes="Non-helical T8x4 representation.")
    add("y_lead_nut", "transmission", _placed(build_t8_nut(label="y_lead_nut"), (-12.0, y_position - 12.0, p.y_screw_z_mm - 12.0), "y_lead_nut", rotation=(-90.0, 0.0, 0.0)), supporting_part="moving_bed_frame", fastening_method="M4 nut-flange fasteners; bed boss carries reaction", confidence="nut envelope", expected_overlap_with=("moving_bed_frame", "y_lead_screw"), notes="Anti-backlash architecture candidate.")
    add("y_motor_nema17", "motor", _placed(build_nema17("y", label="y_motor_nema17"), (0.0, -195.0, p.y_screw_z_mm), "y_motor_nema17"), supporting_part="y_motor_service_pocket", fastening_method="NEMA17 M3/M4 face fasteners; face pilot locates motor", confidence="generic NEMA17 interface", expected_overlap_with=("y_motor_service_pocket", "y_coupler"), notes="Owner-stock motor with rear connector/wiring clearance.")
    add("y_coupler", "transmission", _placed(build_flexible_coupler("y", label="y_coupler"), (0.0, -195.0, p.y_screw_z_mm), "y_coupler"), supporting_part="y_motor_service_pocket + y_fixed_bearing_cartridge", fastening_method="Two-bore clamp screws; no axial support", confidence="MISUMI reference envelope", expected_overlap_with=("y_lead_screw", "y_motor_nema17"), notes="Representative 5/8 mm coupler envelope.")

    for name, x in (("z_rail_left", -p.z_rail_center_spacing_mm / 2.0 + x_position), ("z_rail_right", p.z_rail_center_spacing_mm / 2.0 + x_position)):
        add(name, "linear-guide", _placed(build_mgn_rail("z", p.z_rail_length_mm, size=9, label=name), (x - 4.5, p.z_rail_y_mm, p.z_rail_start_z_mm), name), supporting_part="x_z_backbone", fastening_method="M2/M3 rail fasteners; printed vertical shoulder carries alignment", confidence="HIWIN reference dimensions", expected_overlap_with=("x_z_backbone",), notes="MGN9 reference rail and H carriage envelope.")
        for index, z in enumerate((p.z_rail_start_z_mm + 18.0 + z_offset, p.z_rail_start_z_mm + 80.0 + z_offset), start=1):
            carriage_name = f"{name.replace('rail', 'carriage')}_{index}"
            add(carriage_name, "linear-guide", _placed(build_mgn_carriage("z", size=9, label=carriage_name), (x - 10.0, p.z_rail_y_mm - 1.0, z), carriage_name), supporting_part="z_carriage_plate", fastening_method="M2/M3 carriage screws into Z plate inserts", confidence="HIWIN reference dimensions", expected_overlap_with=("z_carriage_plate",), notes="MGN9H carriage envelope.")

    add("z_lead_screw", "transmission", _placed(build_t8_screw("z", p.z_screw_length_mm, p.z_screw_lead_mm, label="z_lead_screw"), (p.z_screw_x_mm + x_position, p.z_screw_y_mm, 35.0), "z_lead_screw"), supporting_part="x_z_backbone fixed drive support", fastening_method="Fixed upper bearing and floating lower support; coupler carries torque only", confidence="T8 envelope", expected_overlap_with=("z_carriage_plate", "z_lead_nut", "z_coupler"), notes="Non-helical T8x2 representation.")
    add("z_lead_nut", "transmission", _placed(build_t8_nut(label="z_lead_nut"), (x_position - 12.0, p.z_screw_y_mm - 12.0, 55.0 + z_offset), "z_lead_nut"), supporting_part="z_carriage_plate", fastening_method="M4 nut-flange fasteners; Z plate boss carries reaction", confidence="nut envelope", expected_overlap_with=("z_carriage_plate", "z_lead_screw"), notes="Anti-backlash architecture candidate.")
    add("z_motor_nema17", "motor", _placed(build_nema17("z", label="z_motor_nema17"), (x_position, p.z_screw_y_mm, 190.0), "z_motor_nema17", rotation=(180.0, 0.0, 0.0)), supporting_part="x_z_backbone upper motor land", fastening_method="NEMA17 face fasteners; pilot locates motor", confidence="generic NEMA17 interface", expected_overlap_with=("z_coupler", "x_z_backbone"), notes="Strongest electrically compatible owner-stock motor is selected after characterization.")
    add("z_coupler", "transmission", _placed(build_flexible_coupler("z", label="z_coupler"), (x_position, p.z_screw_y_mm, 175.0), "z_coupler"), supporting_part="x_z_backbone + z_motor_nema17", fastening_method="Two-bore clamp screws; no axial support", confidence="MISUMI reference envelope", expected_overlap_with=("z_lead_screw", "z_motor_nema17"), notes="Representative 5/8 mm coupler envelope.")

    spindle = _placed(build_spindle_candidate(label="spindle_5045_ac_er11"), (x_position, 7.0, 45.0 + z_offset), "spindle_5045_ac_er11")
    add("spindle_5045_ac_er11", "spindle", spindle, supporting_part="spindle_mount_concept", fastening_method="Two removable M4 clamp rings; clamp geometry carries radial/shear load", confidence="SycoTec official reference", expected_overlap_with=("spindle_mount_concept", "tool_envelope"), notes="45 mm ER11 candidate; official CAD remains external because redistribution rights are unclear.")
    add("tool_envelope", "spindle", _cylinder_axis(bd, 2.0, 36.0, (x_position, 7.0, -25.0 + z_offset), "z", "tool_envelope"), supporting_part="spindle and ER11 tool interface", fastening_method="ER11 collet; actual tool selection remains open", confidence="process envelope", expected_overlap_with=("spindle_5045_ac_er11", "pcb_envelope", "spoilboard"), notes="Tool point covers the -25 to +11 mm Z screening range; cutter remains unselected.")
    return result


def _bed_and_process_components(bd: Any, p: Phase5MasterMachineParameters, *, y_position: float) -> list[MasterAssemblyComponent]:
    result: list[MasterAssemblyComponent] = []

    def add(name: str, category: str, shape: Any, **kwargs: Any) -> None:
        result.append(_component(name, category, shape, source="cad/assembly/master_machine.py", **kwargs))

    add("spoilboard", "workholding", _box(bd, (230.0, 180.0, 12.0), (-115.0, -90.0 + y_position, -12.0), "spoilboard"), supporting_part="moving_bed_frame", fastening_method="M4 countersunk/through fasteners into bed inserts; edge shoulders locate it", confidence="project envelope", expected_overlap_with=("moving_bed_frame", "pcb_envelope", "workholding_clamp_front", "workholding_clamp_rear"), notes="Replaceable spoilboard envelope.")
    add("pcb_envelope", "workholding", _box(bd, (200.0, 150.0, p.pcb_nominal_thickness_mm), (-100.0, -75.0 + y_position, 0.0), "pcb_envelope"), supporting_part="spoilboard", fastening_method="Low-profile edge clamps and registration datums", confidence="process requirement", expected_overlap_with=("spoilboard", "workholding_clamp_front", "workholding_clamp_rear", "workholding_clamp_right", "tool_envelope"), notes="Nominal PCB work area.")
    for name, x, y in (("workholding_clamp_front", -92.0, -82.0 + y_position), ("workholding_clamp_rear", -92.0, 74.0 + y_position), ("workholding_clamp_right", 92.0, -4.0 + y_position)):
        add(name, "workholding", _box(bd, (16.0, 8.0, 8.0), (x, y, 1.6), name), supporting_part="spoilboard", fastening_method="M3/M4 clamp screw into replaceable insert or nut; clamp toe retains PCB edge", confidence="process envelope", expected_overlap_with=("pcb_envelope", "spoilboard"), notes="Low-profile workholding reference.")
    probe = _placed(build_conductive_probe(label="conductive_probe"), (72.0, 38.0 + y_position, 0.0), "conductive_probe")
    probe = probe.fuse(_box(bd, (25.0, 25.0, 2.0), (72.0, 38.0 + y_position, -1.0), "conductive_probe_bracket"))
    add("conductive_probe", "probe", probe, supporting_part="spoilboard", fastening_method="M3 bracket/clip and removable probe cable", confidence="process concept", expected_overlap_with=("spoilboard", "pcb_envelope"), notes="Conductive touch plate and cable-entry concept.")
    return result


def _control_and_service_components(bd: Any, p: Phase5MasterMachineParameters) -> list[MasterAssemblyComponent]:
    result: list[MasterAssemblyComponent] = []

    def add(name: str, category: str, shape: Any, **kwargs: Any) -> None:
        result.append(_component(name, category, shape, source="cad/assembly/master_machine.py", **kwargs))

    add("arduino_mega_owner_hardware", "controller", _placed(build_arduino_mega(label="arduino_mega_owner_hardware"), (-50.0, 150.0, 12.0), "arduino_mega_owner_hardware"), supporting_part="electronics_mount_rail", fastening_method="M3 slotted mounting holes; board standoffs are replaceable", confidence="Arduino official reference", expected_overlap_with=("electronics_mount_rail", "cnc_shield_owner_hardware"), notes="Owner-supplied Arduino Mega representation; connector access is modeled.")
    add("cnc_shield_owner_hardware", "controller", _placed(build_cnc_shield(label="cnc_shield_owner_hardware"), (-49.0, 151.0, 15.0), "cnc_shield_owner_hardware"), supporting_part="arduino_mega_owner_hardware + electronics_mount_rail", fastening_method="Mega header stack plus flexible M3 support slots", confidence="provisional owner hardware", expected_overlap_with=("arduino_mega_owner_hardware", "electronics_mount_rail", "driver_cooling_clearance"), notes="OWNER HARDWARE MUST BE IDENTIFIED: exact shield revision and driver modules are unknown.")
    add("driver_cooling_clearance", "controller", _box(bd, (100.0, 60.0, 28.0), (-50.0, 151.0, 33.0), "driver_cooling_clearance"), supporting_part="electronics_mount_rail", fastening_method="Open airflow volume; final fan/vent provision follows driver identification", confidence="provisional owner hardware", expected_overlap_with=("cnc_shield_owner_hardware",), notes="Clearance volume, not a physical part.")
    add("controller_service_loop", "cable-management", _box(bd, (28.0, 60.0, 18.0), (85.0, 145.0, -5.0), "controller_service_loop"), supporting_part="electronics_mount_rail", fastening_method="M3 printed anchor clips and strain relief", confidence="layout provision", notes="USB, power, motor, limit, probe, and spindle-control service corridor.")

    x_switch = _placed(build_d2f_limit_switch(label="x_home_limit"), (-179.0, -42.0, 82.0), "x_home_limit", rotation=(0.0, 0.0, 90.0))
    x_switch = x_switch.fuse(_box(bd, (8.0, 21.0, 6.0), (-185.0, -42.0, 80.0), "x_home_limit_bracket"))
    add("x_home_limit", "limit", x_switch, supporting_part="gantry_left_integrated", fastening_method="M3 switch bracket; lever is actuated by X carriage stop", confidence="Omron family reference", expected_overlap_with=("x_carriage_lower_1",), notes="Known actuation direction remains to be commissioned.")
    y_switch = _placed(build_d2f_limit_switch(label="y_home_limit"), (-135.0, -158.0, -6.0), "y_home_limit", rotation=(90.0, 0.0, 0.0))
    y_switch = y_switch.fuse(_box(bd, (32.0, 8.0, 8.0), (-140.0, -165.0, -10.0), "y_home_limit_bracket"))
    add("y_home_limit", "limit", y_switch, supporting_part="base_left_integrated + base_center_tie", fastening_method="M3 switch bracket; bed flag actuates lever", confidence="Omron family reference", expected_overlap_with=("moving_bed_frame",), notes="Known actuation direction remains to be commissioned.")
    z_switch = _placed(build_d2f_limit_switch(label="z_home_limit"), (48.0, -64.0, 164.0), "z_home_limit", rotation=(0.0, 90.0, 0.0))
    z_switch = z_switch.fuse(_box(bd, (14.0, 12.0, 10.0), (44.0, -66.0, 140.0), "z_home_limit_bracket"))
    add("z_home_limit", "limit", z_switch, supporting_part="x_z_backbone", fastening_method="M3 switch bracket; Z carriage flag actuates lever", confidence="Omron family reference", expected_overlap_with=("z_carriage_left_2",), notes="Known actuation direction remains to be commissioned.")

    add("x_moving_cable_loop", "cable-management", _box(bd, (18.0, 100.0, 20.0), (-75.0, -10.0, 150.0), "x_moving_cable_loop"), supporting_part="gantry_left_integrated + x_z_backbone", fastening_method="M3 anchor clips; bend-radius volume kept clear", confidence="layout provision", notes="Moving X/Z harness corridor, not a decorative line.")
    add("y_moving_cable_loop", "cable-management", _box(bd, (20.0, 110.0, 24.0), (135.0, -55.0, -2.0), "y_moving_cable_loop"), supporting_part="moving_bed_frame + electronics_mount_rail", fastening_method="M3 anchor clips and strain relief", confidence="layout provision", notes="Moving-bed motor, limit, and probe harness corridor.")

    add("representative_m4_fastener", "fastener", _placed(build_fastener_envelope(label="representative_m4_fastener"), (-145.0, -145.0, -48.0), "representative_m4_fastener"), supporting_part="base_left_integrated", fastening_method="Representative M4 through-bolt/washer envelope", confidence="standard fastener envelope", notes="Visible reference only; exact length and washer stack remain provisional." )
    return result


def _expected_interference_pairs() -> tuple[frozenset[str], ...]:
    pairs = {
        frozenset(pair)
        for pair in (
            ("base_left_integrated", "base_center_tie"),
            ("base_right_integrated", "base_center_tie"),
            ("base_left_integrated", "moving_bed_frame"),
            ("base_right_integrated", "moving_bed_frame"),
            ("base_center_tie", "machine_foot_front_left"),
            ("base_center_tie", "machine_foot_front_right"),
            ("y_rear_bearing_bridge", "machine_foot_rear_left"),
            ("y_motor_service_pocket", "y_fixed_bearing_cartridge"),
            ("base_left_integrated", "gantry_left_integrated"),
            ("base_right_integrated", "gantry_right_integrated"),
            ("gantry_left_integrated", "gantry_right_integrated"),
            ("gantry_left_integrated", "x_z_backbone"),
            ("gantry_right_integrated", "x_z_backbone"),
            ("gantry_left_integrated", "z_carriage_plate"),
            ("gantry_right_integrated", "z_carriage_plate"),
            ("gantry_left_integrated", "spindle_mount_concept"),
            ("gantry_right_integrated", "spindle_mount_concept"),
            ("gantry_left_integrated", "x_fixed_bearing_cartridge"),
            ("gantry_right_integrated", "x_floating_bearing_cartridge"),
            ("x_z_backbone", "z_carriage_plate"),
            ("x_z_backbone", "spindle_mount_concept"),
            ("z_carriage_plate", "spindle_mount_concept"),
            ("z_carriage_plate", "moving_bed_frame"),
            ("moving_bed_frame", "spoilboard"),
            ("spoilboard", "pcb_envelope"),
            ("arduino_mega_owner_hardware", "cnc_shield_owner_hardware"),
        )
    }
    return tuple(sorted(pairs, key=lambda pair: tuple(sorted(pair))))


def build_master_machine(
    parameters: Phase5MasterMachineParameters = PHASE5_MASTER_PARAMETERS,
    *,
    x_position: float = 0.0,
    y_position: float = 0.0,
    z_offset: float = 0.0,
    include_hardware: bool = True,
) -> MasterMachineAssembly:
    """Build the complete machine at a deterministic X/Y/Z state."""

    bd = _build123d()
    parts = build_master_structural_parts()
    components = _structural_components(parts, parameters, x_position=x_position, y_position=y_position, z_offset=z_offset)
    if include_hardware:
        components.extend(_motion_components(bd, parameters, x_position=x_position, y_position=y_position, z_offset=z_offset))
        components.extend(_bed_and_process_components(bd, parameters, y_position=y_position))
        components.extend(_control_and_service_components(bd, parameters))
    master = bd.Compound(children=[component.shape for component in components])
    master.label = "pcb_cnc_master_machine"
    return MasterMachineAssembly(
        parameters=parameters,
        components=tuple(components),
        expected_interference_pairs=_expected_interference_pairs(),
        travel_state=(x_position, y_position, z_offset),
        master_shape=master,
    )


def build_master_travel_state(
    x_position: float,
    y_position: float,
    z_offset: float,
    *,
    parameters: Phase5MasterMachineParameters = PHASE5_MASTER_PARAMETERS,
) -> MasterMachineAssembly:
    return build_master_machine(parameters, x_position=x_position, y_position=y_position, z_offset=z_offset, include_hardware=True)


__all__ = ["MasterAssemblyComponent", "MasterMachineAssembly", "build_master_machine", "build_master_travel_state"]
