"""Fail-closed validation for the Phase 5 master-assembly redesign."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from cad.library.registry import hardware_library_entries
from cad.parameters import PHASE5_MASTER_PARAMETERS, Phase5MasterMachineParameters
from cad.parts.master_structural import MASTER_PART_DEFINITIONS, MASTER_PART_IDS

from .model import IssueSeverity, ValidationIssue, ValidationReport, ValidationStatus


def _issue(
    rule_id: str,
    status: ValidationStatus,
    message: str,
    *,
    severity: IssueSeverity = IssueSeverity.ERROR,
    component: str | None = None,
    evidence: str | None = None,
) -> ValidationIssue:
    return ValidationIssue(rule_id, status, severity, message, component, evidence)


def _shape_is_valid(shape: Any) -> bool:
    value = getattr(shape, "is_valid", False)
    return bool(value() if callable(value) else value)


def _solid_count(shape: Any) -> int:
    value = getattr(shape, "solids", ())
    solids = value() if callable(value) else value
    return len(solids)


def _vector_tuple(vector: Any) -> tuple[float, float, float]:
    return tuple(float(value) for value in vector)


def _aabb(shape: Any) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    box = shape.bounding_box()
    return _vector_tuple(box.min), _vector_tuple(box.max)


def _aabb_overlap(first: Any, second: Any, *, tolerance_mm: float = 1e-6) -> bool:
    first_min, first_max = _aabb(first)
    second_min, second_max = _aabb(second)
    return all(
        first_max[index] > second_min[index] + tolerance_mm
        and second_max[index] > first_min[index] + tolerance_mm
        for index in range(3)
    )


def _exact_volume_overlap(first: Any, second: Any, *, tolerance_mm3: float = 1e-6) -> bool:
    try:
        intersection = first.intersect(second)
    except (AttributeError, RuntimeError, TypeError):
        return _aabb_overlap(first, second)
    if intersection is None:
        return False
    shapes = [intersection] if hasattr(intersection, "volume") else list(intersection)
    return sum(float(getattr(shape, "volume", 0.0)) for shape in shapes) > tolerance_mm3


def check_phase5_complete_structural_parts(
    parts: Mapping[str, Any],
    parameters: Phase5MasterMachineParameters = PHASE5_MASTER_PARAMETERS,
) -> ValidationReport:
    """Check derived solids and the printer-boundary contract."""

    report = ValidationReport()
    expected = set(MASTER_PART_IDS)
    actual = set(parts)
    if actual != expected:
        report.add(_issue("VAL-PHASE5-COMPLETE-PART-IDS", ValidationStatus.FAIL, "Master-derived structural inventory does not match its declared part IDs.", evidence=f"missing={sorted(expected - actual)}; extra={sorted(actual - expected)}"))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-PART-IDS", ValidationStatus.PASS, "All declared master-derived PETG part IDs are present exactly once.", severity=IssueSeverity.INFO, evidence="; ".join(MASTER_PART_IDS)))

    for definition in MASTER_PART_DEFINITIONS:
        shape = parts.get(definition.part_id)
        if shape is None:
            continue
        valid = _shape_is_valid(shape)
        solids = _solid_count(shape)
        report.add(_issue("VAL-PHASE5-COMPLETE-SOLID-VALID", ValidationStatus.PASS if valid else ValidationStatus.FAIL, "Derived PETG part is a valid CAD shape." if valid else "Derived PETG part is not a valid CAD shape.", severity=IssueSeverity.INFO if valid else IssueSeverity.ERROR, component=definition.part_id))
        report.add(_issue("VAL-PHASE5-COMPLETE-SINGLE-SOLID", ValidationStatus.PASS if solids == 1 else ValidationStatus.FAIL, "Derived part is one fused solid." if solids == 1 else "Derived part is not one fused solid.", severity=IssueSeverity.INFO if solids == 1 else IssueSeverity.ERROR, component=definition.part_id, evidence=f"solid_count={solids}"))
        size = _vector_tuple(shape.bounding_box().size)
        fits = max(size) <= parameters.conservative_printed_dimension_mm + 1e-6
        report.add(_issue("VAL-PHASE5-COMPLETE-PRINT-BOUND", ValidationStatus.PASS if fits else ValidationStatus.FAIL, "Derived part fits the conservative 320 mm screening envelope." if fits else "Derived part exceeds the conservative 320 mm screening envelope.", severity=IssueSeverity.INFO if fits else IssueSeverity.ERROR, component=definition.part_id, evidence=f"bbox_mm={size}; preferred={parameters.preferred_printed_dimension_mm}; conservative={parameters.conservative_printed_dimension_mm}"))

    report.add(_issue("VAL-PHASE5-COMPLETE-PROVISIONAL", ValidationStatus.NOT_READY, "Supplier-dependent hardware interfaces and PETG process evidence remain provisional.", severity=IssueSeverity.WARNING, evidence="Measure rails, screws, nuts, bearings, couplers, motors, spindle, controller, switches, probe, inserts, and print coupons before hardware validation or release."))
    return report


REQUIRED_COMPLETE_COMPONENTS = frozenset(
    {
        *MASTER_PART_IDS,
        "x_rail_lower", "x_rail_upper", "x_carriage_lower_1", "x_carriage_lower_2", "x_carriage_upper_1", "x_carriage_upper_2",
        "x_lead_screw", "x_lead_nut", "x_motor_nema17", "x_coupler",
        "y_rail_left", "y_rail_right", "y_carriage_left_1", "y_carriage_left_2", "y_carriage_right_1", "y_carriage_right_2",
        "y_lead_screw", "y_lead_nut", "y_motor_nema17", "y_coupler",
        "z_rail_left", "z_rail_right", "z_carriage_left_1", "z_carriage_left_2", "z_carriage_right_1", "z_carriage_right_2",
        "z_lead_screw", "z_lead_nut", "z_motor_nema17", "z_coupler",
        "spindle_5045_ac_er11", "tool_envelope", "spoilboard", "pcb_envelope",
        "workholding_clamp_front", "workholding_clamp_rear", "workholding_clamp_right", "conductive_probe",
        "arduino_mega_owner_hardware", "cnc_shield_owner_hardware", "driver_cooling_clearance",
        "x_home_limit", "y_home_limit", "z_home_limit",
    }
)


def check_phase5_complete_assembly(assembly: Any) -> ValidationReport:
    """Check completeness, support/fastening records, and master validity."""

    report = ValidationReport()
    names = {component.name for component in assembly.components}
    missing = sorted(REQUIRED_COMPLETE_COMPONENTS - names)
    if missing:
        report.add(_issue("VAL-PHASE5-COMPLETE-ASSEMBLY", ValidationStatus.FAIL, "Master assembly is missing required structural or hardware components.", evidence=f"missing={missing}"))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-ASSEMBLY", ValidationStatus.PASS, "Master assembly contains the derived structure and major real-hardware representations.", severity=IssueSeverity.INFO, evidence=f"component_count={len(names)}"))
    structural = [component for component in assembly.components if component.category == "printed-structural"]
    if len(structural) != len(MASTER_PART_IDS):
        report.add(_issue("VAL-PHASE5-COMPLETE-STRUCTURAL-COUNT", ValidationStatus.FAIL, "Master assembly structural component count does not match the derived inventory.", evidence=f"count={len(structural)}"))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-STRUCTURAL-COUNT", ValidationStatus.PASS, "Master assembly includes all derived structural parts.", severity=IssueSeverity.INFO))
    if len(names) != len(assembly.components):
        report.add(_issue("VAL-PHASE5-COMPLETE-UNIQUE-NAMES", ValidationStatus.FAIL, "Master assembly component names are not unique."))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-UNIQUE-NAMES", ValidationStatus.PASS, "Master assembly component names are unique.", severity=IssueSeverity.INFO))
    unsupported = [component.name for component in assembly.components if not component.supporting_part.strip() or not component.fastening_method.strip()]
    if unsupported:
        report.add(_issue("VAL-PHASE5-MASTER-SUPPORT-FASTENING", ValidationStatus.FAIL, "Every major component must answer what supports it and what fastens it.", evidence="; ".join(unsupported)))
    else:
        report.add(_issue("VAL-PHASE5-MASTER-SUPPORT-FASTENING", ValidationStatus.PASS, "Every master component has an explicit support and fastening record.", severity=IssueSeverity.INFO, evidence=f"audited_components={len(assembly.components)}"))
    master_valid = _shape_is_valid(assembly.master_shape)
    report.add(_issue("VAL-PHASE5-COMPLETE-MASTER", ValidationStatus.PASS if master_valid else ValidationStatus.FAIL, "Master assembly compound is valid." if master_valid else "Master assembly compound is invalid.", severity=IssueSeverity.INFO if master_valid else IssueSeverity.ERROR))
    known_model_ids = {entry["component_id"] for entry in hardware_library_entries()}
    unknown_model_ids = sorted({component.hardware_model_id for component in assembly.components if component.hardware_model_id and component.hardware_model_id not in known_model_ids})
    if unknown_model_ids:
        report.add(_issue("VAL-PHASE5-HARDWARE-LIBRARY-ID", ValidationStatus.FAIL, "Master assembly references an unknown persistent hardware model ID.", evidence="; ".join(unknown_model_ids)))
    else:
        report.add(_issue("VAL-PHASE5-HARDWARE-LIBRARY-ID", ValidationStatus.PASS, "All assigned master hardware model IDs resolve in the persistent library manifest.", severity=IssueSeverity.INFO, evidence=f"model_ids={len({component.hardware_model_id for component in assembly.components if component.hardware_model_id})}"))
    library_source_without_id = sorted(component.name for component in assembly.components if component.source == "cad/library/parametric_models.py" and not component.hardware_model_id)
    if library_source_without_id:
        report.add(_issue("VAL-PHASE5-HARDWARE-LIBRARY-COVERAGE", ValidationStatus.FAIL, "A library-sourced assembly component has no stable hardware model ID.", evidence="; ".join(library_source_without_id)))
    else:
        report.add(_issue("VAL-PHASE5-HARDWARE-LIBRARY-COVERAGE", ValidationStatus.PASS, "Every library-sourced assembly component carries a stable hardware model ID.", severity=IssueSeverity.INFO))
    return report


def _declared_interface(first: Any, second: Any, expected: set[frozenset[str]]) -> bool:
    pair = frozenset((first.name, second.name))
    if pair in expected:
        return True
    if second.name in first.expected_overlap_with or first.name in second.expected_overlap_with:
        return True
    return second.name in first.supporting_part or first.name in second.supporting_part


def check_phase5_complete_structural_interference(assembly: Any) -> ValidationReport:
    """Audit derived structural overlaps and reject undeclared intersections."""

    report = ValidationReport()
    components = [component for component in assembly.components if component.category == "printed-structural"]
    expected = set(assembly.expected_interference_pairs)
    observed: list[str] = []
    unexpected: list[str] = []
    for index, first in enumerate(components):
        for second in components[index + 1 :]:
            # Use exact BRep overlap when the CAD kernel is available.  AABB
            # is reserved for the explicit fallback inside
            # _exact_volume_overlap so clearance sweeps do not become false
            # positives merely because two bounding boxes are broad.
            if not _exact_volume_overlap(first.shape, second.shape):
                continue
            text = f"{first.name} / {second.name}"
            observed.append(text)
            if not _declared_interface(first, second, expected):
                unexpected.append(text)
    if unexpected:
        report.add(_issue("VAL-PHASE5-COMPLETE-INTERFERENCE", ValidationStatus.FAIL, "Undeclared derived-structure overlap detected.", evidence="; ".join(unexpected)))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-INTERFERENCE", ValidationStatus.PASS, "All derived-structure overlaps are declared structural joints, supports, or service interfaces.", severity=IssueSeverity.INFO, evidence=f"observed_overlap_count={len(observed)}"))
    return report


def check_phase5_complete_travel_extremes(parameters: Phase5MasterMachineParameters = PHASE5_MASTER_PARAMETERS) -> ValidationReport:
    """Check all X/Y/Z travel corners against the hardware-first master."""

    from cad.assembly.master_machine import build_master_travel_state

    report = ValidationReport()
    failures: list[str] = []
    state_count = 0
    x_values = (-parameters.usable_travel_mm[0] / 2.0, parameters.usable_travel_mm[0] / 2.0)
    y_values = (-parameters.usable_travel_mm[1] / 2.0, parameters.usable_travel_mm[1] / 2.0)
    z_values = (parameters.travel_min_mm[2], parameters.travel_max_mm[2])
    for x_position in x_values:
        for y_position in y_values:
            for z_offset in z_values:
                state_count += 1
                assembly = build_master_travel_state(x_position, y_position, z_offset, parameters=parameters)
                by_name = assembly.component_map
                spindle = by_name["spindle_5045_ac_er11"].shape
                bed = by_name["moving_bed_frame"].shape
                towers = (by_name["gantry_left_integrated"].shape, by_name["gantry_right_integrated"].shape)
                if any(_aabb_overlap(spindle, tower) for tower in towers):
                    failures.append(f"spindle/gantry x={x_position}, y={y_position}, z={z_offset}")
                if any(_exact_volume_overlap(bed, tower) for tower in towers):
                    failures.append(f"bed/gantry x={x_position}, y={y_position}, z={z_offset}")
                for support_name in ("y_fixed_bearing_cartridge", "y_floating_bearing_cartridge", "y_motor_service_pocket", "y_motor_nema17", "y_rear_bearing_bridge"):
                    if _exact_volume_overlap(bed, by_name[support_name].shape):
                        failures.append(f"bed/{support_name} x={x_position}, y={y_position}, z={z_offset}")
                # The Z motor is deliberately mounted to the moving X/Z
                # backbone, so overlap with that mounting land is expected.
                # The fail-closed screen instead requires the motor to remain
                # registered to the backbone and clear of the fixed gantry.
                if not _aabb_overlap(by_name["x_z_backbone"].shape, by_name["z_motor_nema17"].shape):
                    failures.append(f"Z motor lost backbone registration x={x_position}, y={y_position}, z={z_offset}")
                if any(_exact_volume_overlap(by_name["z_motor_nema17"].shape, tower) for tower in towers):
                    failures.append(f"Z motor/gantry x={x_position}, y={y_position}, z={z_offset}")
    if failures:
        report.add(_issue("VAL-PHASE5-COMPLETE-TRAVEL", ValidationStatus.FAIL, "Master travel clearance failed at one or more corners.", evidence="; ".join(failures)))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-TRAVEL", ValidationStatus.PASS, "All eight X/Y/Z travel corners pass spindle/tower, bed/tower, and Z motor/gantry clearance screens; the motor remains registered to its moving backbone mount.", severity=IssueSeverity.INFO, evidence=f"states={state_count}; travel_mm={parameters.usable_travel_mm}"))
    report.add(_issue("VAL-PHASE5-COMPLETE-SWEPT-INTERFACES", ValidationStatus.NOT_READY, "Exact swept BRep, cable bend-radius, homing repeatability, and measured hardware fit remain open.", severity=IssueSeverity.WARNING, evidence="Corner screening passed; physical measurements and process evidence are still required."))
    return report


def check_phase5_complete_export_files(paths: Mapping[str, Path]) -> ValidationReport:
    report = ValidationReport()
    for name, path in sorted(paths.items()):
        path = Path(path)
        if not path.exists() or path.stat().st_size <= 0:
            report.add(_issue("VAL-PHASE5-COMPLETE-EXPORT-FILE", ValidationStatus.FAIL, "Master-machine export is missing or empty.", component=name, evidence=str(path)))
            continue
        if path.suffix.lower() == ".stl" and path.stat().st_size < 84:
            report.add(_issue("VAL-PHASE5-COMPLETE-EXPORT-FILE", ValidationStatus.FAIL, "STL candidate is too short to contain a mesh header and triangle data.", component=name, evidence=f"{path.stat().st_size} bytes"))
            continue
        report.add(_issue("VAL-PHASE5-COMPLETE-EXPORT-FILE", ValidationStatus.PASS, "Master-machine derivative exists and is non-empty.", severity=IssueSeverity.INFO, component=name, evidence=f"{path} ({path.stat().st_size} bytes)"))
    return report


def phase5_complete_gate_report() -> ValidationReport:
    report = ValidationReport()
    report.add(_issue("VAL-PHASE5-COMPLETE-AUTHORIZATION", ValidationStatus.PASS, "Owner direction opens the master-assembly-first Phase 5 redesign from the published Phase 5 baseline.", severity=IssueSeverity.INFO))
    report.add(_issue("VAL-PHASE5-COMPLETE-METHODOLOGY", ValidationStatus.PASS, "The complete assembled CNC is the primary design object; PETG splits are derived from its hardware relationships.", severity=IssueSeverity.INFO))
    report.add(_issue("VAL-PHASE5-COMPLETE-MATURITY", ValidationStatus.NOT_READY, "The complete virtual machine and regenerated parts are PROTOTYPE-STL review artifacts, not HARDWARE-VALIDATED or RELEASED.", severity=IssueSeverity.WARNING))
    report.add(_issue("VAL-PHASE5-COMPLETE-PHYSICAL-EVIDENCE", ValidationStatus.NOT_READY, "Physical first prints, supplier measurements, motor/controller identification, alignment, runout, and commissioning evidence remain open.", severity=IssueSeverity.WARNING))
    return report


__all__ = [
    "REQUIRED_COMPLETE_COMPONENTS",
    "check_phase5_complete_assembly",
    "check_phase5_complete_structural_interference",
    "check_phase5_complete_structural_parts",
    "check_phase5_complete_travel_extremes",
    "check_phase5_complete_export_files",
    "phase5_complete_gate_report",
]
