"""Fail-closed validation for the proposed Phase 4A optimization study."""

from __future__ import annotations

from typing import Any

from cad.assembly.architecture_skeleton import find_interferences
from cad.parameters import (
    PHASE3A_PACKAGING_VARIANTS,
    PHASE4_STRUCTURAL_PARAMETERS,
    ParameterStatus,
)
from cad.phase4a_calculations import phase4a_structural_estimate
from cad.parts.phase4a_structural import (
    SELECTED_PHASE4A_VARIANT,
    VARIANT_ORDER,
    Phase4APartRecord,
    phase4a_part_records,
    phase4a_primary_loop_parts,
)
from cad.packaging_phase3a import phase3a_variant_by_id

from .model import IssueSeverity, ValidationIssue, ValidationReport, ValidationStatus
from .phase3a import check_phase3a_model_containment, check_phase3a_packaging_variant


_REQUIRED_REFERENCE_NAMES = {
    "phase3a_x_rail_1",
    "phase3a_x_rail_2",
    "phase3a_x_screw",
    "phase3a_x_fixed_bearing",
    "phase3a_x_floating_bearing",
    "phase3a_x_nut",
    "phase3a_x_coupler",
    "phase3a_x_nema17",
    "phase3a_y_rail_1",
    "phase3a_y_rail_2",
    "phase3a_y_screw",
    "phase3a_y_fixed_bearing",
    "phase3a_y_floating_bearing",
    "phase3a_y_nut",
    "phase3a_y_coupler",
    "phase3a_y_nema17",
    "phase3a_z_rail_1",
    "phase3a_z_rail_2",
    "phase3a_z_screw",
    "phase3a_z_fixed_bearing",
    "phase3a_z_floating_bearing",
    "phase3a_z_nut",
    "phase3a_z_coupler",
    "phase3a_z_nema17",
    "phase3a_spindle_mount",
    "phase3a_moving_bed_support",
    "phase3a_spoilboard",
    "phase3a_x_home_limit",
    "phase3a_y_home_limit",
    "phase3a_z_home_limit",
}

_REQUIRED_SERVICEABLE_PARTS = {
    "y_motor_service_pocket",
    "y_fixed_bearing_cartridge",
    "y_floating_bearing_cartridge",
    "z_carriage_plate",
    "spindle_mount_concept",
    "moving_bed_frame",
}


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


def _variant_exists(variant_id: str) -> bool:
    return variant_id in VARIANT_ORDER


def _p2_variant():
    return phase3a_variant_by_id("P2", PHASE3A_PACKAGING_VARIANTS)


def _records_for(
    variant_id: str,
    records: tuple[Phase4APartRecord, ...] | None,
) -> tuple[Phase4APartRecord, ...]:
    if records is not None:
        return records
    return phase4a_part_records(variant_id=variant_id)


def check_phase4a_structural_parameters(
    variant_id: str = SELECTED_PHASE4A_VARIANT,
    records: tuple[Phase4APartRecord, ...] | None = None,
) -> ValidationReport:
    """Validate one O1/O2/O3 part contract and preliminary stiffness screen."""

    report = ValidationReport()
    if not _variant_exists(variant_id):
        report.add(
            _issue(
                "VAL-PHASE4A-VARIANT",
                ValidationStatus.FAIL,
                "Phase 4A variant must be one of O1, O2, or O3.",
                evidence=variant_id,
            )
        )
        return report

    records = _records_for(variant_id, records)
    part_ids = [record.part_id for record in records]
    if len(part_ids) != len(set(part_ids)):
        report.add(
            _issue(
                "VAL-PHASE4A-PART-IDS",
                ValidationStatus.FAIL,
                "Phase 4A part IDs must be unique within a candidate.",
            )
        )
    if not records:
        report.add(
            _issue(
                "VAL-PHASE4A-PART-COUNT",
                ValidationStatus.FAIL,
                "A Phase 4A candidate must declare printable structural parts.",
            )
        )

    oversized: list[str] = []
    preferred_boundary: list[str] = []
    missing_fields: list[str] = []
    non_preliminary: list[str] = []
    for record in records:
        if any(value <= 0 for value in record.nominal_bbox_mm + record.print_orientation_extents_mm):
            report.add(
                _issue(
                    "VAL-PHASE4A-PART-DIMENSIONS",
                    ValidationStatus.FAIL,
                    "Nominal and print-orientation extents must be positive.",
                    component=record.part_id,
                )
            )
        xy = max(record.print_orientation_extents_mm[:2])
        if xy > PHASE4_STRUCTURAL_PARAMETERS.conservative_structural_xy_mm + 1e-6:
            oversized.append(record.part_id)
        elif xy >= PHASE4_STRUCTURAL_PARAMETERS.preferred_structural_xy_mm - 1e-6:
            preferred_boundary.append(record.part_id)
        if any(
            not value.strip()
            for value in (
                record.print_orientation,
                record.support_requirement,
                record.brim_requirement,
                record.warping_risk,
                record.layer_load_concern,
                record.notes,
            )
        ):
            missing_fields.append(record.part_id)
        if record.status != ParameterStatus.PRELIMINARY:
            non_preliminary.append(record.part_id)

    if oversized:
        report.add(
            _issue(
                "VAL-PHASE4A-PRINT-BOUND",
                ValidationStatus.FAIL,
                "A mandatory Phase 4A print exceeds the conservative 320 mm XY build bound.",
                evidence=", ".join(oversized),
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-PRINT-BOUND",
                ValidationStatus.PASS,
                "All Phase 4A review parts fit the conservative 320 mm XY build bound.",
                severity=IssueSeverity.INFO,
            )
        )
    if preferred_boundary:
        report.add(
            _issue(
                "VAL-PHASE4A-PRINTABILITY-BOUNDARY",
                ValidationStatus.NOT_READY,
                "Parts at the 300 mm preferred boundary require printer-specific conditioning, warp, and datum evidence.",
                severity=IssueSeverity.WARNING,
                evidence=", ".join(preferred_boundary),
            )
        )
    if missing_fields:
        report.add(
            _issue(
                "VAL-PHASE4A-PRINT-EVIDENCE",
                ValidationStatus.NOT_READY,
                "Every Phase 4A part needs orientation, support, brim/warping, layer-load, and review notes.",
                severity=IssueSeverity.WARNING,
                evidence=", ".join(missing_fields),
            )
        )
    if non_preliminary:
        report.add(
            _issue(
                "VAL-PHASE4A-STATUS-BOUNDARY",
                ValidationStatus.FAIL,
                "Phase 4A geometry must remain PRELIMINARY until owner and physical gates are closed.",
                evidence=", ".join(non_preliminary),
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-STATUS-BOUNDARY",
                ValidationStatus.PASS,
                "All Phase 4A part records remain PRELIMINARY; no manufacturing release is implied.",
                severity=IssueSeverity.INFO,
            )
        )

    primary = phase4a_primary_loop_parts(variant_id)
    actual_primary = {record.part_id for record in records if record.direct_force_loop}
    if actual_primary != set(primary):
        report.add(
            _issue(
                "VAL-PHASE4A-FORCE-LOOP",
                ValidationStatus.FAIL,
                "Direct-force-loop flags must match the controlled variant force-loop register.",
                evidence=f"missing={sorted(primary - actual_primary)} extra={sorted(actual_primary - primary)}",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-FORCE-LOOP",
                ValidationStatus.PASS,
                f"The {variant_id} primary force loop is explicitly named and contains {len(primary)} PETG parts.",
                severity=IssueSeverity.INFO,
            )
        )

    estimate = phase4a_structural_estimate(variant_id)
    if not estimate.acceptance_passes:
        report.add(
            _issue(
                "VAL-PHASE4A-CALCULATION",
                ValidationStatus.FAIL,
                "The preliminary 5 N Phase 4A screen exceeds the 0.030 mm acceptance limit.",
                evidence=f"{estimate.total_tool_point_deflection_mm:.6f} mm; dominant {estimate.dominant_contribution}",
            )
        )
    elif not estimate.target_passes:
        report.add(
            _issue(
                "VAL-PHASE4A-CALCULATION",
                ValidationStatus.NOT_READY,
                "The candidate exceeds the 0.020 mm target and cannot proceed without architectural justification.",
                severity=IssueSeverity.WARNING,
                evidence=f"{estimate.total_tool_point_deflection_mm:.6f} mm",
            )
        )
    elif not estimate.preferred_target_passes:
        report.add(
            _issue(
                "VAL-PHASE4A-CALCULATION",
                ValidationStatus.NOT_READY,
                "The candidate meets the 0.020 mm target but not the preferred 0.015 mm target; owner justification is required.",
                severity=IssueSeverity.WARNING,
                evidence=f"{estimate.total_tool_point_deflection_mm:.6f} mm",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-CALCULATION",
                ValidationStatus.PASS,
                "The preliminary 5 N Phase 4A screen passes both the 0.020 mm target and 0.015 mm preferred target.",
                severity=IssueSeverity.INFO,
                evidence=f"{estimate.total_tool_point_deflection_mm:.6f} mm; dominant {estimate.dominant_contribution}",
            )
        )
    report.add(
        _issue(
            "VAL-PHASE4A-CALCULATION-EVIDENCE",
            ValidationStatus.NOT_READY,
            "The structural result is an equivalent-section screen, not FEA, a measured deflection, or a PETG coupon result.",
            severity=IssueSeverity.WARNING,
            evidence=estimate.evidence_status,
        )
    )
    return report


def check_phase4a_assembly(
    model: Any,
    variant_id: str = SELECTED_PHASE4A_VARIANT,
    records: tuple[Phase4APartRecord, ...] | None = None,
    interference_findings: tuple[dict[str, Any], ...] | None = None,
) -> ValidationReport:
    """Validate P2 travel/containment, optimized parts, access contracts, and overlaps."""

    report = ValidationReport()
    if not _variant_exists(variant_id):
        report.add(
            _issue(
                "VAL-PHASE4A-VARIANT",
                ValidationStatus.FAIL,
                "Cannot validate an unknown Phase 4A assembly variant.",
                evidence=variant_id,
            )
        )
        return report

    p2 = _p2_variant()
    # This carries the accepted P2 full-travel, swept-clearance, rail/screw,
    # motor, bed, spindle, and service-footprint checks into Phase 4A.
    report.extend(check_phase3a_packaging_variant(p2))
    report.extend(check_phase3a_model_containment(model, p2))

    names = [component.name for component in model.components]
    if len(names) != len(set(names)):
        report.add(
            _issue(
                "VAL-PHASE4A-ASSEMBLY-NAMES",
                ValidationStatus.FAIL,
                "Phase 4A assembly component names must be unique.",
            )
        )

    structural_parts = tuple(getattr(model, "structural_parts", ()))
    records = _records_for(variant_id, records)
    expected_ids = {record.part_id for record in records}
    actual_ids = {part.name for part in structural_parts}
    if actual_ids != expected_ids:
        report.add(
            _issue(
                "VAL-PHASE4A-ASSEMBLY-PARTS",
                ValidationStatus.FAIL,
                "The built assembly must contain one structural component for every Phase 4A part record.",
                evidence=f"missing={sorted(expected_ids - actual_ids)} extra={sorted(actual_ids - expected_ids)}",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-ASSEMBLY-PARTS",
                ValidationStatus.PASS,
                f"Assembly contains all {len(expected_ids)} selected {variant_id} structural parts.",
                severity=IssueSeverity.INFO,
            )
        )

    record_by_id = {record.part_id: record for record in records}
    for component in structural_parts:
        box = component.shape.bounding_box()
        size = tuple(float(getattr(box.size, axis)) for axis in ("X", "Y", "Z"))
        if any(value <= 0 for value in size):
            report.add(
                _issue(
                    "VAL-PHASE4A-ASSEMBLY-DIMENSIONS",
                    ValidationStatus.FAIL,
                    "Every built Phase 4A structural part must have a positive review-solid bounding box.",
                    component=component.name,
                )
            )
        if max(size[:2]) > PHASE4_STRUCTURAL_PARAMETERS.conservative_structural_xy_mm + 1e-6:
            report.add(
                _issue(
                    "VAL-PHASE4A-PRINT-BOUND",
                    ValidationStatus.FAIL,
                    "Built Phase 4A geometry exceeds the conservative 320 mm XY build bound.",
                    component=component.name,
                    evidence=f"built bbox {size}",
                )
            )
        declared = record_by_id.get(component.name)
        if declared is not None and any(
            abs(actual - expected) > 1e-6
            for actual, expected in zip(size, declared.nominal_bbox_mm)
        ):
            report.add(
                _issue(
                    "VAL-PHASE4A-ASSEMBLY-CONTRACT",
                    ValidationStatus.FAIL,
                    "Built geometry must match the actual preliminary part-record bounding box.",
                    component=component.name,
                    evidence=f"built={size}; record={declared.nominal_bbox_mm}",
                )
            )

    missing_refs = sorted(_REQUIRED_REFERENCE_NAMES - set(names))
    if missing_refs:
        report.add(
            _issue(
                "VAL-PHASE4A-MOTION-REFERENCE",
                ValidationStatus.FAIL,
                "The optimized assembly is missing an accepted P2 motion, bed, spindle, or limit reference.",
                evidence=", ".join(missing_refs),
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-MOTION-REFERENCE",
                ValidationStatus.PASS,
                "Accepted P2 rails, screws, bearings, motors, bed, spindle, and homing references remain present.",
                severity=IssueSeverity.INFO,
            )
        )

    missing_service = sorted(_REQUIRED_SERVICEABLE_PARTS - actual_ids)
    if missing_service:
        report.add(
            _issue(
                "VAL-PHASE4A-SERVICEABILITY",
                ValidationStatus.FAIL,
                "The optimization removed a required serviceable motion or process module.",
                evidence=", ".join(missing_service),
            )
        )
    elif PHASE4_STRUCTURAL_PARAMETERS.assembly_sequence and PHASE4_STRUCTURAL_PARAMETERS.serviceable_components:
        report.add(
            _issue(
                "VAL-PHASE4A-SERVICEABILITY",
                ValidationStatus.PASS,
                "The P2 serviceable hardware register and assembly sequence remain defined; optimized structural modules still require mock-up evidence.",
                severity=IssueSeverity.INFO,
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-SERVICEABILITY",
                ValidationStatus.NOT_READY,
                "Serviceable components and the assembly sequence are incomplete.",
                severity=IssueSeverity.WARNING,
            )
        )

    all_interferences = (
        tuple(interference_findings)
        if interference_findings is not None
        else find_interferences(model)
    )
    unexpected = tuple(item for item in all_interferences if not item["expected"])
    if unexpected:
        for item in unexpected:
            report.add(
                _issue(
                    "VAL-PHASE4A-INTERFERENCE",
                    ValidationStatus.FAIL,
                    "Unexpected overlap exists between independent Phase 4A structural parts.",
                    component=f"{item['first']} / {item['second']}",
                    evidence=f"{item['volume_mm3']:.6f} mm^3",
                )
            )
    else:
        report.add(
            _issue(
                "VAL-PHASE4A-INTERFERENCE",
                ValidationStatus.PASS,
                "No unexpected structural overlaps were found; documented interfaces are the only solid-overlap events.",
                severity=IssueSeverity.INFO,
                evidence=f"{len(all_interferences)} documented overlap events",
            )
        )
    return report


def phase4a_gate_report() -> ValidationReport:
    """List evidence required before manufacturing release or later batches."""

    report = ValidationReport()
    for evidence in (
        "physical evidence must confirm the owner-accepted O2 before/after package and hardware-freeze disposition",
        "measured MGN12/MGN9, T8 screw/nut, bearing, coupler, motor, spindle, insert, and fastener interfaces",
        "Voron 2.4 350 mm conditioning, warp, bridge, layer-load, and 300 mm Y rail-carrier coupons",
        "rail-seat datum, skim/shim, parallelism, and carriage-preload evidence after conditioning",
        "full-travel assembly mock-up proving bed, spindle, motor, screw, coupler, bearing, fastener, limit, probe, cable, and tool access",
        "5 N tool-point test separated by gantry, base, X/Z, rail/interface, bed, and joint contributions",
        "J1/service-joint pull-out, creep, preload-retention, and repeated-disassembly evidence",
        "measured printed-part mass, moving-bed mass, thermal/creep conditioning, spoilboard, and workholding implementation",
    ):
        report.add(
            _issue(
                "VAL-PHASE4A-GATE-EVIDENCE",
                ValidationStatus.NOT_READY,
                f"Required before manufacturing release or later Phase 5 batches: {evidence}.",
                severity=IssueSeverity.WARNING,
                evidence="Preliminary CAD and calculations do not replace physical evidence.",
            )
        )
    report.add(
        _issue(
            "VAL-PHASE4A-PHASE5-RELEASE-GATE",
            ValidationStatus.PASS,
            "Phase 4 and Phase 4A preliminary architecture is owner-accepted; the owner-authorized Phase 5 base-pair candidate is open, while production release and later parts remain closed.",
            severity=IssueSeverity.INFO,
        )
    )
    return report


__all__ = [
    "check_phase4a_assembly",
    "check_phase4a_structural_parameters",
    "phase4a_gate_report",
]
