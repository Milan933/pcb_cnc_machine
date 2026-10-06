"""Fail-closed checks for the complete Phase 5 virtual machine."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from cad.parameters import PHASE5_COMPLETE_PARAMETERS, Phase5CompleteMachineParameters
from cad.parts.phase5_complete_structural import (
    PHASE5_COMPLETE_PART_DEFINITIONS,
    PHASE5_COMPLETE_PART_IDS,
)

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
    return ValidationIssue(
        rule_id=rule_id,
        status=status,
        severity=severity,
        message=message,
        component=component,
        evidence=evidence,
    )


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
    """Return a conservative BRep overlap result when the CAD backend exists."""

    try:
        intersection = first.intersect(second)
    except (AttributeError, RuntimeError, TypeError):
        return _aabb_overlap(first, second)
    if intersection is None:
        return False
    if hasattr(intersection, "volume"):
        shapes = [intersection]
    else:
        shapes = list(intersection)
    volume = sum(float(getattr(shape, "volume", 0.0)) for shape in shapes)
    return volume > tolerance_mm3


def check_phase5_complete_structural_parts(
    parts: Mapping[str, Any],
    parameters: Phase5CompleteMachineParameters = PHASE5_COMPLETE_PARAMETERS,
) -> ValidationReport:
    """Check all 19 local candidates without granting hardware validation."""

    report = ValidationReport()
    expected = set(PHASE5_COMPLETE_PART_IDS)
    actual = set(parts)
    if actual != expected:
        report.add(
            _issue(
                "VAL-PHASE5-COMPLETE-PART-IDS",
                ValidationStatus.FAIL,
                "The complete manufacturing batch must contain exactly the 19 stable structural part IDs.",
                evidence=f"missing={sorted(expected - actual)}; extra={sorted(actual - expected)}",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE5-COMPLETE-PART-IDS",
                ValidationStatus.PASS,
                "All 19 stable PCNC structural part IDs are present exactly once.",
                severity=IssueSeverity.INFO,
                evidence="; ".join(PHASE5_COMPLETE_PART_IDS),
            )
        )

    for definition in PHASE5_COMPLETE_PART_DEFINITIONS:
        shape = parts.get(definition.part_id)
        if shape is None:
            continue
        valid = _shape_is_valid(shape)
        solids = _solid_count(shape)
        if not valid:
            report.add(_issue("VAL-PHASE5-COMPLETE-SOLID-VALID", ValidationStatus.FAIL, "Printable candidate is not a valid CAD shape.", component=definition.part_id))
        else:
            report.add(_issue("VAL-PHASE5-COMPLETE-SOLID-VALID", ValidationStatus.PASS, "Printable candidate reports a valid CAD shape.", severity=IssueSeverity.INFO, component=definition.part_id))
        if solids != 1:
            report.add(_issue("VAL-PHASE5-COMPLETE-SINGLE-SOLID", ValidationStatus.FAIL, "Each printable candidate must be a single fused solid, not a review compound.", component=definition.part_id, evidence=f"solid_count={solids}"))
        else:
            report.add(_issue("VAL-PHASE5-COMPLETE-SINGLE-SOLID", ValidationStatus.PASS, "Candidate is one fused solid.", severity=IssueSeverity.INFO, component=definition.part_id))
        size = _vector_tuple(shape.bounding_box().size)
        if max(size) > parameters.conservative_printed_dimension_mm + 1e-6:
            report.add(_issue("VAL-PHASE5-COMPLETE-PRINT-BOUND", ValidationStatus.FAIL, "Candidate exceeds the conservative 320 mm printable envelope in at least one axis.", component=definition.part_id, evidence=f"bbox_mm={size}"))
        else:
            report.add(_issue("VAL-PHASE5-COMPLETE-PRINT-BOUND", ValidationStatus.PASS, "Candidate remains within the conservative 320 mm envelope.", severity=IssueSeverity.INFO, component=definition.part_id, evidence=f"bbox_mm={size}"))

    report.add(
        _issue(
            "VAL-PHASE5-COMPLETE-PROVISIONAL",
            ValidationStatus.NOT_READY,
            "The complete batch deliberately contains provisional hardware interfaces.",
            severity=IssueSeverity.WARNING,
            evidence="Rail, screw, bearing, insert, spindle, and exact controller interfaces require measured hardware before fit/release claims.",
        )
    )
    return report


REQUIRED_COMPLETE_COMPONENTS = frozenset(
    {
        *PHASE5_COMPLETE_PART_IDS,
        "x_rail_lower",
        "x_rail_upper",
        "y_rail_left",
        "y_rail_right",
        "z_rail_left",
        "z_rail_right",
        "x_lead_screw",
        "y_lead_screw",
        "z_lead_screw",
        "x_motor_nema17",
        "y_motor_nema17",
        "z_motor_nema17",
        "spindle_envelope",
        "tool_envelope",
        "spoilboard",
        "pcb_envelope",
        "conductive_probe",
        "arduino_mega_owner_hardware",
        "cnc_shield_owner_hardware",
        "x_home_limit",
        "y_home_limit",
        "z_home_limit",
    }
)


def check_phase5_complete_assembly(assembly: Any) -> ValidationReport:
    """Check assembly completeness and named service boundaries."""

    report = ValidationReport()
    names = {component.name for component in assembly.components}
    missing = sorted(REQUIRED_COMPLETE_COMPONENTS - names)
    if missing:
        report.add(_issue("VAL-PHASE5-COMPLETE-ASSEMBLY", ValidationStatus.FAIL, "Complete assembly is missing required structural or hardware-envelope components.", evidence=f"missing={missing}"))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-ASSEMBLY", ValidationStatus.PASS, "Complete assembly contains the 19 structural parts and required motion, process, control, limit, and probe envelopes.", severity=IssueSeverity.INFO, evidence=f"component_count={len(names)}"))
    structural = [component for component in assembly.components if component.category == "printed-structural"]
    if len(structural) != len(PHASE5_COMPLETE_PART_IDS):
        report.add(_issue("VAL-PHASE5-COMPLETE-STRUCTURAL-COUNT", ValidationStatus.FAIL, "Assembly structural component count does not match the 19-part inventory.", evidence=f"count={len(structural)}"))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-STRUCTURAL-COUNT", ValidationStatus.PASS, "Assembly includes exactly 19 printed structural components.", severity=IssueSeverity.INFO))
    if len(names) != len(assembly.components):
        report.add(_issue("VAL-PHASE5-COMPLETE-UNIQUE-NAMES", ValidationStatus.FAIL, "Assembly component names are not unique."))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-UNIQUE-NAMES", ValidationStatus.PASS, "Assembly component names are unique and reviewable.", severity=IssueSeverity.INFO))
    master_valid = _shape_is_valid(assembly.master_shape)
    report.add(_issue("VAL-PHASE5-COMPLETE-MASTER", ValidationStatus.PASS if master_valid else ValidationStatus.FAIL, "Master assembly compound is valid." if master_valid else "Master assembly compound is invalid.", severity=IssueSeverity.INFO if master_valid else IssueSeverity.ERROR))
    return report


def check_phase5_complete_structural_interference(assembly: Any) -> ValidationReport:
    """Classify nominal structural AABB overlaps as interfaces or errors.

    This is a conservative envelope screen.  It does not pretend that an
    AABB result is a measured fit or a BRep contact proof; the report records
    the explicit expected interfaces so unclassified overlaps cannot be
    silently ignored.
    """

    report = ValidationReport()
    components = [component for component in assembly.components if component.category == "printed-structural"]
    by_name = {component.name: component for component in components}
    expected = {
        frozenset(pair)
        for pair in (
            ("base_left_integrated", "base_center_tie"),
            ("base_right_integrated", "base_center_tie"),
            ("base_left_integrated", "y_motor_service_pocket"),
            ("base_left_integrated", "y_fixed_bearing_cartridge"),
            ("base_left_integrated", "y_floating_bearing_cartridge"),
            ("base_right_integrated", "y_motor_service_pocket"),
            ("base_right_integrated", "y_fixed_bearing_cartridge"),
            ("base_right_integrated", "y_floating_bearing_cartridge"),
            ("y_motor_service_pocket", "y_fixed_bearing_cartridge"),
            ("base_left_integrated", "moving_bed_frame"),
            ("base_right_integrated", "moving_bed_frame"),
            ("base_center_tie", "moving_bed_frame"),
            ("gantry_left_integrated", "gantry_right_integrated"),
            ("gantry_left_integrated", "x_fixed_bearing_cartridge"),
            ("gantry_right_integrated", "x_floating_bearing_cartridge"),
            ("gantry_left_integrated", "x_z_backbone"),
            ("gantry_right_integrated", "x_z_backbone"),
            ("gantry_left_integrated", "z_carriage_plate"),
            ("gantry_right_integrated", "z_carriage_plate"),
            ("gantry_left_integrated", "moving_bed_frame"),
            ("gantry_right_integrated", "moving_bed_frame"),
            ("x_z_backbone", "z_carriage_plate"),
            ("z_carriage_plate", "spindle_mount_concept"),
            ("machine_foot_front_left", "base_left_integrated"),
            ("machine_foot_rear_left", "base_left_integrated"),
            ("machine_foot_front_right", "base_right_integrated"),
            ("machine_foot_rear_right", "base_right_integrated"),
        )
    }
    observed: list[str] = []
    unexpected: list[str] = []
    for index, first in enumerate(components):
        for second in components[index + 1 :]:
            if not _aabb_overlap(first.shape, second.shape):
                continue
            pair = frozenset((first.name, second.name))
            text = f"{first.name} / {second.name}"
            observed.append(text)
            if pair not in expected:
                unexpected.append(text)
    if unexpected:
        report.add(_issue("VAL-PHASE5-COMPLETE-INTERFERENCE", ValidationStatus.FAIL, "Unclassified nominal structural AABB overlap detected.", evidence="; ".join(unexpected)))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-INTERFERENCE", ValidationStatus.PASS, "All nominal structural AABB overlaps are explicit force-loop or service interfaces.", severity=IssueSeverity.INFO, evidence=f"expected_overlap_count={len(observed)}"))
    return report


def check_phase5_complete_travel_extremes(
    parameters: Phase5CompleteMachineParameters = PHASE5_COMPLETE_PARAMETERS,
) -> ValidationReport:
    """Build all eight X/Y/Z travel corners and check critical clearances."""

    from cad.assembly.phase5_complete_assembly import build_phase5_travel_state

    report = ValidationReport()
    x_values = (-parameters.usable_travel_mm[0] / 2.0, parameters.usable_travel_mm[0] / 2.0)
    y_values = (-parameters.usable_travel_mm[1] / 2.0, parameters.usable_travel_mm[1] / 2.0)
    z_deltas = (
        parameters.travel_min_mm[2] - (-5.0),
        parameters.travel_max_mm[2] - (-5.0),
    )
    state_count = 0
    failures: list[str] = []
    for x_position in x_values:
        for y_position in y_values:
            for z_delta in z_deltas:
                state_count += 1
                assembly = build_phase5_travel_state(x_position, y_position, z_delta, parameters=parameters)
                by_name = assembly.component_map
                spindle = by_name["spindle_envelope"].shape
                spoilboard = by_name["spoilboard"].shape
                bed = by_name["moving_bed_frame"].shape
                gantry = (by_name["gantry_left_integrated"].shape, by_name["gantry_right_integrated"].shape)
                if any(_aabb_overlap(spindle, tower) for tower in gantry):
                    failures.append(f"spindle/gantry at x={x_position},y={y_position},z_delta={z_delta}")
                if _aabb_overlap(spindle, spoilboard):
                    failures.append(f"spindle/spoilboard at x={x_position},y={y_position},z_delta={z_delta}")
                if any(_exact_volume_overlap(bed, tower) for tower in gantry):
                    failures.append(f"bed/gantry at x={x_position},y={y_position},z_delta={z_delta}")
    if failures:
        report.add(_issue("VAL-PHASE5-COMPLETE-TRAVEL", ValidationStatus.FAIL, "Critical complete-machine travel clearance failed at one or more corners.", evidence="; ".join(failures)))
    else:
        report.add(_issue("VAL-PHASE5-COMPLETE-TRAVEL", ValidationStatus.PASS, "All eight X/Y/Z usable-travel corners pass the critical spindle, spoilboard, and bed-to-gantry envelope screen.", severity=IssueSeverity.INFO, evidence=f"states={state_count}; travel_mm={parameters.usable_travel_mm}"))
    report.add(_issue("VAL-PHASE5-COMPLETE-SWEPT-INTERFACES", ValidationStatus.NOT_READY, "Exact swept BRep collision and cable bend-radius validation remain provisional until measured hardware and final harness geometry exist.", severity=IssueSeverity.WARNING, evidence="AABB corner screening passed; exact rail/screw/spindle/controller interfaces are not hardware-validated."))
    return report


def check_phase5_complete_export_files(paths: Mapping[str, Path]) -> ValidationReport:
    """Check that local candidate derivatives exist and contain geometry bytes."""

    report = ValidationReport()
    for name, path in sorted(paths.items()):
        path = Path(path)
        if not path.exists() or path.stat().st_size <= 0:
            report.add(_issue("VAL-PHASE5-COMPLETE-EXPORT-FILE", ValidationStatus.FAIL, "Complete-machine export is missing or empty.", component=name, evidence=str(path)))
            continue
        if path.suffix.lower() == ".stl" and path.stat().st_size < 84:
            report.add(_issue("VAL-PHASE5-COMPLETE-EXPORT-FILE", ValidationStatus.FAIL, "STL candidate is too short to contain a mesh header and triangle data.", component=name, evidence=f"{path.stat().st_size} bytes"))
            continue
        report.add(_issue("VAL-PHASE5-COMPLETE-EXPORT-FILE", ValidationStatus.PASS, "Local STEP/STL derivative exists and is non-empty.", severity=IssueSeverity.INFO, component=name, evidence=f"{path} ({path.stat().st_size} bytes)"))
    return report


def phase5_complete_gate_report() -> ValidationReport:
    """Record the open Phase 5 gate and its explicit non-release boundary."""

    report = ValidationReport()
    report.add(_issue("VAL-PHASE5-COMPLETE-AUTHORIZATION", ValidationStatus.PASS, "Owner authorization explicitly opens complete Phase 5 manufacturing CAD from baseline afe2e14089467321b323d74f928a7ab4c5ffdc1f.", severity=IssueSeverity.INFO))
    report.add(_issue("VAL-PHASE5-COMPLETE-SCOPE", ValidationStatus.PASS, "Scope is the complete virtual machine, all 19 printable structural candidates, local STL/STEP derivatives, BOM, assembly guide, and review evidence.", severity=IssueSeverity.INFO))
    report.add(_issue("VAL-PHASE5-COMPLETE-MATURITY", ValidationStatus.NOT_READY, "The machine and parts are PROTOTYPE-STL / MANUFACTURING-CANDIDATE review artifacts, not HARDWARE-VALIDATED or RELEASED.", severity=IssueSeverity.WARNING))
    report.add(_issue("VAL-PHASE5-COMPLETE-PHYSICAL-EVIDENCE", ValidationStatus.NOT_READY, "Physical first-print, measured hardware fit, alignment, electrical identification, and commissioning evidence remain open owner actions.", severity=IssueSeverity.WARNING))
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
