"""Fail-closed validation for the preliminary Phase 4 structural concept."""

from __future__ import annotations

from typing import Any

from cad.parameters import (
    PHASE4_STRUCTURAL_PARAMETERS,
    PHASE3A_PACKAGING_VARIANTS,
    ParameterStatus,
    Phase4StructuralParameters,
)
from cad.phase4_calculations import phase4_structural_estimate

from .model import IssueSeverity, ValidationIssue, ValidationReport, ValidationStatus
from .phase3a import check_phase3a_model_containment, check_phase3a_packaging_variant


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


def _phase4_variant():
    for variant in PHASE3A_PACKAGING_VARIANTS:
        if variant.variant_id == PHASE4_STRUCTURAL_PARAMETERS.reference_variant_id:
            return variant
    raise KeyError(PHASE4_STRUCTURAL_PARAMETERS.reference_variant_id)


def check_phase4_structural_parameters(
    parameters: Phase4StructuralParameters = PHASE4_STRUCTURAL_PARAMETERS,
) -> ValidationReport:
    """Validate the dependency-light Phase 4 part, interface, and calculation contracts."""

    report = ValidationReport()
    part_ids = [part.part_id for part in parameters.print_parts]
    if len(part_ids) != len(set(part_ids)):
        report.add(
            _issue(
                "VAL-PHASE4-PART-IDS",
                ValidationStatus.FAIL,
                "Phase 4 structural part IDs must be unique.",
            )
        )
    if not part_ids:
        report.add(
            _issue(
                "VAL-PHASE4-PART-COUNT",
                ValidationStatus.FAIL,
                "The Phase 4 concept must declare structural parts before assembly review.",
            )
        )

    oversized: list[str] = []
    conditional: list[str] = []
    missing_manufacturing_fields: list[str] = []
    non_preliminary: list[str] = []
    for part in parameters.print_parts:
        if any(value <= 0 for value in part.nominal_bbox_mm + part.print_orientation_extents_mm):
            report.add(
                _issue(
                    "VAL-PHASE4-PART-DIMENSIONS",
                    ValidationStatus.FAIL,
                    "Structural part nominal and orientation extents must be positive.",
                    component=part.part_id,
                )
            )
        if max(part.print_orientation_extents_mm[:2]) > parameters.conservative_structural_xy_mm:
            oversized.append(part.part_id)
        elif max(part.print_orientation_extents_mm[:2]) > parameters.preferred_structural_xy_mm:
            conditional.append(part.part_id)
        if any(
            not value.strip()
            for value in (
                part.print_orientation,
                part.support_requirement,
                part.brim_requirement,
                part.warping_risk,
                part.layer_load_concern,
                part.notes,
            )
        ):
            missing_manufacturing_fields.append(part.part_id)
        if part.status != ParameterStatus.PRELIMINARY:
            non_preliminary.append(part.part_id)

    if oversized:
        report.add(
            _issue(
                "VAL-PHASE4-PRINT-BOUND",
                ValidationStatus.FAIL,
                "Mandatory Phase 4 structural parts exceed the conservative 320 mm XY build bound.",
                evidence=", ".join(oversized),
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-PRINT-BOUND",
                ValidationStatus.PASS,
                "All declared mandatory structural parts fit within the conservative 320 mm XY bound.",
                severity=IssueSeverity.INFO,
            )
        )
    if conditional:
        report.add(
            _issue(
                "VAL-PHASE4-PRINTABILITY-REVIEW",
                ValidationStatus.PASS,
                "Parts at the 300 mm preferred boundary are flagged for printer-specific conditioning and coupon review.",
                severity=IssueSeverity.WARNING,
                evidence=", ".join(conditional),
            )
        )
    if missing_manufacturing_fields:
        report.add(
            _issue(
                "VAL-PHASE4-PRINT-EVIDENCE",
                ValidationStatus.NOT_READY,
                "Every structural part needs orientation, support, brim/warping, and layer-load notes.",
                evidence=", ".join(missing_manufacturing_fields),
            )
        )
    if non_preliminary:
        report.add(
            _issue(
                "VAL-PHASE4-STATUS-BOUNDARY",
                ValidationStatus.FAIL,
                "Phase 4 review geometry must not be marked manufacturing-ready.",
                evidence=", ".join(non_preliminary),
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-STATUS-BOUNDARY",
                ValidationStatus.PASS,
                "All structural part records remain PRELIMINARY; no production release is implied.",
                severity=IssueSeverity.INFO,
            )
        )

    for seat in parameters.rail_seats:
        if (
            seat.axis not in {"X", "Y", "Z"}
            or seat.rail_reference_length_mm <= 0
            or seat.supported_length_mm <= 0
            or seat.supported_length_mm > seat.rail_reference_length_mm
            or seat.seat_width_mm <= 0
            or seat.seat_height_mm <= 0
            or not seat.datum_strategy.strip()
            or not seat.alignment_method.strip()
            or not seat.post_process.strip()
        ):
            report.add(
                _issue(
                    "VAL-PHASE4-RAIL-SEAT",
                    ValidationStatus.FAIL,
                    "Every rail seat needs ordered dimensions, a datum, an alignment method, and post-processing strategy.",
                    component=seat.seat_id,
                )
            )
    if parameters.rail_seats and not any(
        seat.supported_length_mm < seat.rail_reference_length_mm for seat in parameters.rail_seats
    ):
        report.add(
            _issue(
                "VAL-PHASE4-RAIL-SEAT",
                ValidationStatus.NOT_READY,
                "At least one rail seat should document the supported-length versus hardware-length distinction.",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-RAIL-SEAT",
                ValidationStatus.PASS,
                "Rail seats document printed datum strategy, alignment, and post-processing; raw PETG precision is not assumed.",
                severity=IssueSeverity.INFO,
            )
        )

    concept_ids = [concept.concept_id for concept in parameters.joint_concepts]
    selected = [concept for concept in parameters.joint_concepts if concept.selected]
    if set(concept_ids) != {"J1", "J2", "J3"} or len(selected) != 1:
        report.add(
            _issue(
                "VAL-PHASE4-JOINT-STUDY",
                ValidationStatus.FAIL,
                "The gantry study must compare exactly J1, J2, and J3 and select one provisional concept.",
            )
        )
    elif selected[0].concept_id != "J1":
        report.add(
            _issue(
                "VAL-PHASE4-JOINT-STUDY",
                ValidationStatus.NOT_READY,
                "The current provisional joint selection is not the required J1 baseline.",
                evidence=selected[0].concept_id,
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-JOINT-STUDY",
                ValidationStatus.PASS,
                "J1/J2/J3 are compared and J1 is selected provisionally; coupon and repeated-service evidence remain open.",
                severity=IssueSeverity.INFO,
            )
        )

    if not parameters.serviceable_components or not parameters.assembly_sequence:
        report.add(
            _issue(
                "VAL-PHASE4-SERVICEABILITY",
                ValidationStatus.FAIL,
                "Phase 4 must list serviceable motion components and an assembly sequence.",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-SERVICEABILITY",
                ValidationStatus.PASS,
                "Motors, fixed/floating supports, couplers, screws/nuts, guides, spindle, limits, wiring, and spoilboard are listed as serviceable.",
                severity=IssueSeverity.INFO,
            )
        )

    estimate = phase4_structural_estimate(parameters)
    if not estimate.acceptance_passes:
        report.add(
            _issue(
                "VAL-PHASE4-CALCULATION",
                ValidationStatus.FAIL,
                "The preliminary 5 N structural screen exceeds the 0.030 mm acceptance limit.",
                evidence=f"{estimate.total_tool_point_deflection_mm:.6f} mm; dominant {estimate.dominant_contribution}",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-CALCULATION",
                ValidationStatus.PASS,
                "The equivalent-section 5 N screen passes the 0.030 mm acceptance limit.",
                severity=IssueSeverity.INFO,
                evidence=(
                    f"total {estimate.total_tool_point_deflection_mm:.6f} mm; target "
                    f"{estimate.target_mm:.3f} mm={'pass' if estimate.target_passes else 'not met'}; "
                    f"dominant {estimate.dominant_contribution}"
                ),
            )
        )
    report.add(
        _issue(
            "VAL-PHASE4-CALCULATION-EVIDENCE",
            ValidationStatus.NOT_READY,
            "The structural result is a preliminary equivalent-section screen, not FEA or measured PETG evidence.",
            severity=IssueSeverity.WARNING,
            evidence=estimate.evidence_status,
        )
    )
    return report


def check_phase4_assembly(model: Any) -> ValidationReport:
    """Validate the build123d assembly, containment, references, and overlaps."""

    report = ValidationReport()
    variant = _phase4_variant()
    report.extend(check_phase3a_packaging_variant(variant))
    report.extend(check_phase3a_model_containment(model, variant))

    names = [component.name for component in model.components]
    if len(names) != len(set(names)):
        report.add(
            _issue(
                "VAL-PHASE4-ASSEMBLY",
                ValidationStatus.FAIL,
                "Phase 4 assembly component names must be unique.",
            )
        )

    parts = tuple(getattr(model, "structural_parts", ()))
    expected_ids = {part.part_id for part in PHASE4_STRUCTURAL_PARAMETERS.print_parts}
    parameter_by_id = {part.part_id: part for part in PHASE4_STRUCTURAL_PARAMETERS.print_parts}
    actual_ids = {part.name for part in parts}
    if actual_ids != expected_ids:
        report.add(
            _issue(
                "VAL-PHASE4-ASSEMBLY",
                ValidationStatus.FAIL,
                "The assembly must contain one built structural component for every Phase 4 part record.",
                evidence=f"missing={sorted(expected_ids - actual_ids)} extra={sorted(actual_ids - expected_ids)}",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-ASSEMBLY",
                ValidationStatus.PASS,
                f"Assembly contains all {len(expected_ids)} preliminary structural parts plus the P2 motion/process references.",
                severity=IssueSeverity.INFO,
            )
        )

    for component in parts:
        bounding_box = component.shape.bounding_box()
        size = tuple(float(getattr(bounding_box.size, axis)) for axis in ("X", "Y", "Z"))
        if any(value <= 0 for value in size):
            report.add(
                _issue(
                    "VAL-PHASE4-ASSEMBLY",
                    ValidationStatus.FAIL,
                    "Every built structural part must have a non-zero review-solid bounding box.",
                    component=component.name,
                )
            )
        if max(size[:2]) > PHASE4_STRUCTURAL_PARAMETERS.conservative_structural_xy_mm + 1e-6:
            report.add(
                _issue(
                    "VAL-PHASE4-PRINT-BOUND",
                    ValidationStatus.FAIL,
                    "Built structural geometry exceeds the conservative 320 mm XY bound.",
                    component=component.name,
                    evidence=f"built bbox {size}",
                )
            )
        declared = parameter_by_id.get(component.name)
        if declared is not None and any(
            abs(actual - expected) > 1e-6
            for actual, expected in zip(size, declared.nominal_bbox_mm)
        ):
            report.add(
                _issue(
                    "VAL-PHASE4-ASSEMBLY",
                    ValidationStatus.FAIL,
                    "Built structural bounding box does not match its centralized preliminary part contract.",
                    component=component.name,
                    evidence=f"built {size}; declared {declared.nominal_bbox_mm}",
                )
            )

    required_reference_names = {
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
    missing_refs = sorted(required_reference_names - set(names))
    if missing_refs:
        report.add(
            _issue(
                "VAL-PHASE4-MOTION-REFERENCE",
                ValidationStatus.FAIL,
                "The assembly is missing one or more accepted P2 rail, screw, bearing, motor, bed, spindle, or limit references.",
                evidence=", ".join(missing_refs),
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-MOTION-REFERENCE",
                ValidationStatus.PASS,
                "Accepted P2 X/Y/Z motion, motor, bearing, bed, spindle, and limit references are present.",
                severity=IssueSeverity.INFO,
            )
        )

    from cad.assembly.phase4_assembly import phase4_model_interferences

    unexpected = phase4_model_interferences(model)
    if unexpected:
        for item in unexpected:
            report.add(
                _issue(
                    "VAL-PHASE4-INTERFERENCE",
                    ValidationStatus.FAIL,
                    "Unexpected overlap exists between independent Phase 4 solids.",
                    component=f"{item['first']} / {item['second']}",
                    evidence=f"{item['volume_mm3']:.6f} mm^3",
                )
            )
    else:
        report.add(
            _issue(
                "VAL-PHASE4-INTERFERENCE",
                ValidationStatus.PASS,
                "No unexpected solid overlaps were found between separate structural concept parts.",
                severity=IssueSeverity.INFO,
            )
        )

    report.add(
        _issue(
            "VAL-PHASE4-SERVICEABILITY-EVIDENCE",
            ValidationStatus.NOT_READY,
            "Service access, removable cartridges, cable routing, and full assembly sequence still require physical/mock-up evidence.",
            severity=IssueSeverity.WARNING,
        )
    )
    return report


def phase4_gate_report() -> ValidationReport:
    """List evidence required before manufacturing release or later batches."""

    report = ValidationReport()
    for evidence in (
        "physical evidence must confirm the owner-accepted preliminary structural CAD, part decomposition, and provisional J1 selection",
        "printer-specific PETG conditioning, warp, bridge, layer-load, and 300 mm rail-carrier coupons",
        "actual MGN12/MGN9, T8 screw/nut, bearing, coupler, motor, spindle, insert, and fastener dimensions",
        "rail-seat datum, skim/shim, parallelism, and carriage-preload evidence",
        "full-travel assembly mock-up proving bed, spindle, motor, screw, coupler, bearing, fastener, limit, probe, and cable access",
        "5 N tool-point load test separated by gantry beam, towers/joint, X/Z, base, rail seats, and moving-bed contributions",
        "joint coupon and repeated-disassembly evidence for J1 before the joint is frozen",
        "measured printed-part mass, creep/thermal conditioning, and spoilboard/workholding implementation",
    ):
        report.add(
            _issue(
                "VAL-PHASE4-GATE-EVIDENCE",
                ValidationStatus.NOT_READY,
                f"Required before manufacturing release or later Phase 5 batches: {evidence}.",
                evidence="Review geometry and calculations do not replace physical evidence.",
            )
        )
    report.add(
        _issue(
            "VAL-PHASE4-PHASE5-RELEASE-GATE",
            ValidationStatus.PASS,
            "Phase 4 preliminary architecture is owner-accepted; the owner-authorized Phase 5 base-pair candidate is open, while production release and later parts remain closed.",
            severity=IssueSeverity.INFO,
        )
    )
    return report


__all__ = [
    "check_phase4_assembly",
    "check_phase4_structural_parameters",
    "phase4_gate_report",
]
