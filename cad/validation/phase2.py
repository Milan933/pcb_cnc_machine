"""Backend-independent validation for the Phase 2 architecture skeleton."""

from __future__ import annotations

from cad.parameters import (
    INITIAL_PARAMETERS,
    PHASE2_SKELETON_PARAMETERS,
    Phase2SkeletonParameters,
)

from .model import IssueSeverity, ValidationIssue, ValidationReport, ValidationStatus


def _issue(
    rule_id: str,
    status: ValidationStatus,
    message: str,
    *,
    severity: IssueSeverity = IssueSeverity.ERROR,
    evidence: str | None = None,
) -> ValidationIssue:
    return ValidationIssue(
        rule_id=rule_id,
        status=status,
        severity=severity,
        message=message,
        evidence=evidence,
    )


def check_phase2_skeleton_parameters(
    parameters: Phase2SkeletonParameters = PHASE2_SKELETON_PARAMETERS,
) -> ValidationReport:
    """Check travel, packaging, and interface relationships before solids."""

    report = ValidationReport()
    working_x, working_y = parameters.working_area_mm
    travel_x, travel_y, travel_z = parameters.tool_travel_mm
    bed_x, bed_y, _ = parameters.bed_envelope_mm
    base_x, base_y, _ = parameters.base_envelope_mm

    comparisons = (
        ("VAL-PHASE2-TRAVEL-X", "X tool travel", travel_x, working_x + 2.0 * parameters.travel_margin_each_end_mm),
        ("VAL-PHASE2-TRAVEL-Y", "Y tool travel", travel_y, working_y + 2.0 * parameters.travel_margin_each_end_mm),
        ("VAL-PHASE2-BED-X", "bed envelope X", bed_x, working_x + 2.0 * parameters.travel_margin_each_end_mm),
        ("VAL-PHASE2-BED-Y", "bed envelope Y", bed_y, working_y + 2.0 * parameters.travel_margin_each_end_mm),
        ("VAL-PHASE2-GANTRY-SPAN", "gantry clear span", parameters.gantry_clear_span_mm, travel_x),
        ("VAL-PHASE2-BASE-X", "base envelope X", base_x, parameters.gantry_outer_width_mm),
        ("VAL-PHASE2-BASE-Y", "base envelope Y", base_y, travel_y + 2.0 * parameters.rail_end_margin_mm),
    )
    for rule_id, label, available, required in comparisons:
        if available < required:
            report.add(
                _issue(
                    rule_id,
                    ValidationStatus.FAIL,
                    f"{label} {available:g} mm is below the screening requirement {required:g} mm.",
                )
            )
        else:
            report.add(
                _issue(
                    rule_id,
                    ValidationStatus.PASS,
                    f"{label} {available:g} mm meets the screening requirement {required:g} mm.",
                    severity=IssueSeverity.INFO,
                )
            )

    z_range = INITIAL_PARAMETERS.target_z_travel_mm
    if not z_range.minimum <= travel_z <= z_range.maximum:
        report.add(
            _issue(
                "VAL-PHASE2-TRAVEL-Z",
                ValidationStatus.FAIL,
                f"Skeleton Z travel {travel_z:g} mm is outside the accepted Phase 1 range {z_range.minimum:g}-{z_range.maximum:g} mm.",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE2-TRAVEL-Z",
                ValidationStatus.PASS,
                f"Skeleton Z travel {travel_z:g} mm is inside the Phase 1 range {z_range.minimum:g}-{z_range.maximum:g} mm.",
                severity=IssueSeverity.INFO,
            )
        )

    if parameters.z_rail_center_spacing_mm <= 0:
        report.add(_issue("VAL-PHASE2-Z-GUIDE-SPACING", ValidationStatus.FAIL, "Dual Z guide spacing must be positive."))
    else:
        report.add(_issue("VAL-PHASE2-Z-GUIDE-SPACING", ValidationStatus.PASS, "Dual Z guide center spacing is defined.", severity=IssueSeverity.INFO))

    if parameters.tool_point_overhang_mm > 60.0:
        report.add(
            _issue(
                "VAL-PHASE2-Z-OVERHANG",
                ValidationStatus.FAIL,
                "Tool-point overhang exceeds the Phase 1 conditional 60 mm screening maximum.",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE2-Z-OVERHANG",
                ValidationStatus.PASS,
                f"Tool-point overhang {parameters.tool_point_overhang_mm:g} mm is inside the Phase 1 screening maximum.",
                severity=IssueSeverity.INFO,
            )
        )

    printable_structural_bounds = (
        parameters.gantry_outer_width_mm,
        parameters.gantry_section_depth_mm,
        parameters.gantry_section_height_mm,
        parameters.bed_envelope_mm[0],
        parameters.base_envelope_mm[0],
    )
    if any(value > parameters.conditional_printed_dimension_mm for value in printable_structural_bounds):
        report.add(
            _issue(
                "VAL-PHASE2-PRINT-BOUND",
                ValidationStatus.FAIL,
                "A primary structural bound exceeds the conditional one-piece print bound.",
                evidence=f"structural bounds={printable_structural_bounds!r}",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE2-PRINT-BOUND",
                ValidationStatus.PASS,
                "Primary structural bounds stay within the conditional one-piece print bound; orientation and warping evidence remain future work.",
                severity=IssueSeverity.INFO,
            )
        )

    return report
