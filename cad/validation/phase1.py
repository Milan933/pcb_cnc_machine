"""Executable checks and calculations for the Phase 1 requirements baseline."""

from __future__ import annotations

import math

from cad.parameters import (
    INITIAL_PARAMETERS,
    PHASE1_REQUIREMENTS,
    Phase1Requirements,
    non_compensatable_z_budget_mm,
)

from .model import (
    IssueSeverity,
    ValidationIssue,
    ValidationReport,
    ValidationStatus,
)


def v_bit_isolation_width_mm(
    depth_mm: float,
    included_angle_deg: float,
    tip_diameter_mm: float = 0.0,
) -> float:
    """Ideal geometric V-bit width at a depth below the tip.

    Tip radius, runout, tool deflection, burrs, and material behavior are not
    represented by this ideal geometry and must be tested separately.
    """

    if depth_mm < 0:
        raise ValueError("depth_mm must not be negative")
    if not 0 < included_angle_deg < 180:
        raise ValueError("included_angle_deg must be between 0 and 180")
    if tip_diameter_mm < 0:
        raise ValueError("tip_diameter_mm must not be negative")
    return tip_diameter_mm + 2.0 * depth_mm * math.tan(
        math.radians(included_angle_deg / 2.0)
    )


def v_bit_width_sensitivity(included_angle_deg: float) -> float:
    """Ideal change in width per millimetre of depth change."""

    if not 0 < included_angle_deg < 180:
        raise ValueError("included_angle_deg must be between 0 and 180")
    return 2.0 * math.tan(math.radians(included_angle_deg / 2.0))


def _issue(
    rule_id: str,
    status: ValidationStatus,
    message: str,
    *,
    severity: IssueSeverity = IssueSeverity.ERROR,
) -> ValidationIssue:
    return ValidationIssue(
        rule_id=rule_id,
        status=status,
        severity=severity,
        message=message,
    )


def check_phase1_requirements(
    requirements: Phase1Requirements = PHASE1_REQUIREMENTS,
) -> ValidationReport:
    """Check internal consistency of the quantitative Phase 1 baseline."""

    report = ValidationReport()
    ranges = (
        ("copper_thickness_mm", requirements.copper_thickness_mm),
        ("pcb_thickness_mm", requirements.pcb_thickness_mm),
        ("isolation_depth_mm", requirements.isolation_depth_mm),
        ("v_bit_tip_diameter_mm", requirements.v_bit_tip_diameter_mm),
        ("fine_end_mill_diameter_mm", requirements.fine_end_mill_diameter_mm),
        ("drill_diameter_mm", requirements.drill_diameter_mm),
        ("isolation_feed_mm_min", requirements.isolation_feed_mm_min),
        ("drilling_feed_mm_min", requirements.drilling_feed_mm_min),
        ("outline_feed_mm_min", requirements.outline_feed_mm_min),
        ("spindle_speed_rpm", requirements.spindle_speed_rpm),
        ("spindle_power_w", requirements.spindle_power_w),
        ("spindle_mass_kg", requirements.spindle_mass_kg),
        ("xy_packaging_allowance_total_mm", requirements.xy_packaging_allowance_total_mm),
    )
    for name, value_range in ranges:
        if not value_range.is_ordered() or value_range.minimum <= 0:
            report.add(
                _issue(
                    "VAL-PHASE1-RANGES",
                    ValidationStatus.FAIL,
                    f"{name} must be positive and ordered.",
                )
            )

    if not (
        requirements.isolation_depth_mm.minimum
        <= requirements.initial_isolation_depth_mm
        <= requirements.isolation_depth_mm.maximum
    ):
        report.add(
            _issue(
                "VAL-PHASE1-ISOLATION-DEPTH",
                ValidationStatus.FAIL,
                "Initial isolation depth must lie inside the proposed process window.",
            )
        )

    if not (
        requirements.spindle_speed_rpm.minimum
        <= requirements.initial_spindle_speed_rpm
        <= requirements.spindle_speed_rpm.maximum
    ):
        report.add(
            _issue(
                "VAL-PHASE1-SPINDLE-SPEED",
                ValidationStatus.FAIL,
                "Initial spindle speed must lie inside the screening range.",
            )
        )

    if requirements.spindle_runout_target_mm > requirements.spindle_runout_acceptance_max_mm:
        report.add(
            _issue(
                "VAL-PHASE1-RUNOUT",
                ValidationStatus.FAIL,
                "Spindle runout target must not exceed its acceptance limit.",
            )
        )

    paired_limits = (
        (
            "XY absolute error",
            requirements.xy_absolute_error_target_mm,
            requirements.xy_absolute_error_acceptance_mm,
        ),
        (
            "XY repeatability",
            requirements.xy_repeatability_target_mm,
            requirements.xy_repeatability_acceptance_mm,
        ),
        (
            "XY backlash",
            requirements.xy_backlash_target_mm,
            requirements.xy_backlash_acceptance_mm,
        ),
        (
            "XY straightness",
            requirements.xy_straightness_target_mm,
            requirements.xy_straightness_acceptance_mm,
        ),
        (
            "XY squareness",
            requirements.xy_squareness_target_mm_per_100mm,
            requirements.xy_squareness_acceptance_mm_per_100mm,
        ),
        (
            "Z map residual",
            requirements.z_map_residual_target_mm,
            requirements.z_map_residual_acceptance_mm,
        ),
    )
    for name, target, acceptance in paired_limits:
        if target <= 0 or acceptance <= 0 or target > acceptance:
            report.add(
                _issue(
                    "VAL-PHASE1-TARGETS",
                    ValidationStatus.FAIL,
                    f"{name} target and acceptance limit are inconsistent.",
                )
            )

    if non_compensatable_z_budget_mm(requirements) > requirements.z_machine_error_budget_mm:
        report.add(
            _issue(
                "VAL-PHASE1-Z-BUDGET",
                ValidationStatus.FAIL,
                "Non-compensatable Z allocations exceed the machine Z budget.",
            )
        )

    if (
        requirements.tool_point_deflection_target_mm <= 0
        or requirements.tool_point_deflection_test_load_n <= 0
    ):
        report.add(
            _issue(
                "VAL-PHASE1-DEFLECTION",
                ValidationStatus.FAIL,
                "Tool-point deflection target and test load must be positive.",
            )
        )

    if not (
        requirements.height_map_grid_max_spacing_mm > 0
        and requirements.height_map_refinement_spacing_mm > 0
        and requirements.height_map_refinement_spacing_mm
        < requirements.height_map_grid_max_spacing_mm
    ):
        report.add(
            _issue(
                "VAL-PHASE1-MAP-GRID",
                ValidationStatus.FAIL,
                "Height-map refinement spacing must be positive and finer than the baseline grid.",
            )
        )

    option_ids = {option.option_id for option in requirements.working_area_options}
    if requirements.recommended_working_area_option_id not in option_ids:
        report.add(
            _issue(
                "VAL-PHASE1-ENVELOPE",
                ValidationStatus.FAIL,
                "Recommended working-area option is not present in the option set.",
            )
        )
    for option in requirements.working_area_options:
        if option.pcb_x_mm <= 0 or option.pcb_y_mm <= 0:
            report.add(
                _issue(
                    "VAL-PHASE1-ENVELOPE",
                    ValidationStatus.FAIL,
                    f"Working-area option {option.option_id} is not positive.",
                )
            )

    nominal_printer_dimension_mm = max(INITIAL_PARAMETERS.voron_build_volume_mm)
    if not (
        0 < requirements.preferred_printed_dimension_mm
        <= requirements.conditional_printed_dimension_mm
        <= nominal_printer_dimension_mm
    ):
        report.add(
            _issue(
                "VAL-PHASE1-PRINT-VOLUME",
                ValidationStatus.FAIL,
                "Printed-component screening dimensions are inconsistent with the nominal printer volume.",
            )
        )

    if not report.issues:
        report.add(
            _issue(
                "VAL-PHASE1-BASELINE",
                ValidationStatus.PASS,
                "Phase 1 quantitative requirement parameters are internally consistent.",
                severity=IssueSeverity.INFO,
            )
        )
    return report
