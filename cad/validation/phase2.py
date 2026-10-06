"""Backend-independent validation for the Phase 2 architecture skeleton."""

from __future__ import annotations

from cad.parameters import (
    INITIAL_PARAMETERS,
    PHASE2A_PARAMETERS,
    PHASE2_SKELETON_PARAMETERS,
    Phase2AParameters,
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


def check_phase2a_parameters(
    parameters: Phase2AParameters = PHASE2A_PARAMETERS,
) -> ValidationReport:
    """Check the controlled assumptions used by the A-versus-B study.

    This validates input ordering and completeness only. It does not turn the
    analytical estimates into measured structural evidence.
    """

    report = ValidationReport()

    positive_values = (
        ("test load", parameters.test_load_n),
        ("tool-point target", parameters.tool_point_deflection_target_mm),
        ("tool-point acceptance", parameters.tool_point_deflection_acceptance_mm),
        ("tool-point overhang", parameters.tool_point_overhang_mm),
        ("effective PETG modulus", parameters.effective_petg_modulus_n_per_mm2),
        ("torsion half-span", parameters.torsion_half_span_mm),
        ("racking force offset", parameters.racking_force_offset_mm),
        ("racking tool arm", parameters.racking_tool_arm_mm),
        ("Y guide spacing", parameters.y_guide_spacing_mm),
        ("Y acceleration", parameters.nominal_y_acceleration_m_per_s2),
        ("screw efficiency", parameters.screw_efficiency),
        ("A beam bottom", parameters.a_beam_bottom_z_mm),
        ("A moving-bed support thickness", parameters.a_moving_bed_support_thickness_mm),
    )
    for label, value in positive_values:
        if value <= 0:
            report.add(
                _issue(
                    "VAL-PHASE2A-POSITIVE",
                    ValidationStatus.FAIL,
                    f"Phase 2A {label} must be positive; received {value:g}.",
                )
            )

    if not 0.0 < parameters.effective_petg_poisson_ratio < 0.5:
        report.add(
            _issue(
                "VAL-PHASE2A-POISSON",
                ValidationStatus.FAIL,
                "The effective Poisson ratio must be between zero and one half.",
            )
        )
    if not parameters.screw_leads_mm or any(lead <= 0 for lead in parameters.screw_leads_mm):
        report.add(
            _issue(
                "VAL-PHASE2A-SCREW-LEAD",
                ValidationStatus.FAIL,
                "At least one positive screw lead is required for the dynamic screen.",
            )
        )
    if parameters.tool_point_deflection_target_mm > parameters.tool_point_deflection_acceptance_mm:
        report.add(
            _issue(
                "VAL-PHASE2A-DEFLECTION-LIMITS",
                ValidationStatus.FAIL,
                "The Phase 2A deflection target must not exceed its prototype acceptance limit.",
            )
        )

    sections = (
        ("A", parameters.a_section_width_mm, parameters.a_section_depth_mm, parameters.a_section_wall_mm),
        ("B", parameters.b_section_width_mm, parameters.b_section_depth_mm, parameters.b_section_wall_mm),
    )
    for candidate, width, depth, wall in sections:
        if min(width, depth, wall) <= 0 or 2.0 * wall >= min(width, depth):
            report.add(
                _issue(
                    "VAL-PHASE2A-SECTION",
                    ValidationStatus.FAIL,
                    f"{candidate} equivalent closed section has invalid width/depth/wall ordering.",
                )
            )

    mass_sets = (
        ("A moving mass", parameters.a_moving_mass_items_kg),
        ("B moving mass", parameters.b_moving_mass_items_kg),
        ("A printed mass", parameters.a_printed_mass_items_kg),
        ("B printed mass", parameters.b_printed_mass_items_kg),
    )
    for label, items in mass_sets:
        if not items or any(value < 0 for _, value in items) or not sum(value for _, value in items):
            report.add(
                _issue(
                    "VAL-PHASE2A-MASS",
                    ValidationStatus.FAIL,
                    f"{label} must contain non-negative, non-zero mass items.",
                )
            )

    largest_prints = (parameters.a_largest_print_mm, parameters.b_largest_print_mm)
    if any(min(extents) <= 0 or max(extents) > 330.0 for extents in largest_prints):
        report.add(
            _issue(
                "VAL-PHASE2A-PRINT-BOUND",
                ValidationStatus.FAIL,
                "A Phase 2A largest-print estimate is outside the 330 mm conditional Voron 350 bound.",
            )
        )

    if not report.issues:
        report.add(
            _issue(
                "VAL-PHASE2A-INPUTS",
                ValidationStatus.PASS,
                "Phase 2A analytical inputs are ordered, positive, and bounded for screening.",
                severity=IssueSeverity.INFO,
            )
        )
    return report
