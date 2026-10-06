"""Fail-closed checks for the Phase 3 motion-system review layout."""

from __future__ import annotations

from cad.motion_phase3 import phase3_motion_screen, rail_class_lookup
from cad.parameters import PHASE3_MOTION_PARAMETERS, Phase3MotionParameters

from .model import (
    IssueSeverity,
    ValidationIssue,
    ValidationReport,
    ValidationStatus,
)


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


def check_phase3_motion_parameters(
    parameters: Phase3MotionParameters = PHASE3_MOTION_PARAMETERS,
) -> ValidationReport:
    """Check internal consistency of the preliminary motion layout."""

    report = ValidationReport()
    if len(parameters.axes) != 3 or {axis.axis for axis in parameters.axes} != {"X", "Y", "Z"}:
        report.add(
            _issue(
                "VAL-PHASE3-AXES",
                ValidationStatus.FAIL,
                "Phase 3 must define exactly one X, Y, and Z axis.",
            )
        )

    if parameters.working_area_mm[0] <= 0 or parameters.working_area_mm[1] <= 0:
        report.add(_issue("VAL-PHASE3-WORKING-AREA", ValidationStatus.FAIL, "Working area must be positive."))
    if any(value <= 0 for value in parameters.screened_travel_mm):
        report.add(_issue("VAL-PHASE3-TRAVEL", ValidationStatus.FAIL, "All screened travels must be positive."))
    if parameters.nominal_moving_bed_mass_kg <= 0:
        report.add(_issue("VAL-PHASE3-MASS", ValidationStatus.FAIL, "Moving-bed mass estimate must be positive."))

    try:
        screen = phase3_motion_screen(parameters)
    except (KeyError, ValueError, StopIteration) as exc:
        report.add(
            _issue(
                "VAL-PHASE3-CALCULATION-INPUT",
                ValidationStatus.FAIL,
                f"Motion screening could not be evaluated: {exc}",
            )
        )
        return report

    if not screen.bed_area_margin_ok:
        report.add(
            _issue(
                "VAL-PHASE3-BED-MARGIN",
                ValidationStatus.FAIL,
                "Moving bed does not preserve the required PCB edge/clamp margin.",
            )
        )
    if parameters.backlash_target_mm <= 0 or parameters.backlash_target_mm > 0.050:
        report.add(
            _issue(
                "VAL-PHASE3-BACKLASH-TARGET",
                ValidationStatus.FAIL,
                "The provisional backlash target must be positive and no looser than the Phase 1 acceptance limit.",
            )
        )
    if not 0 < parameters.critical_speed_margin < 1:
        report.add(
            _issue(
                "VAL-PHASE3-CRITICAL-SPEED-MARGIN",
                ValidationStatus.FAIL,
                "Critical-speed margin must be between zero and one.",
            )
        )
    if parameters.recommended_microsteps <= 0:
        report.add(_issue("VAL-PHASE3-MICROSTEPS", ValidationStatus.FAIL, "Recommended microstepping must be positive."))
    if parameters.minimum_xy_holding_torque_nm <= 0 or parameters.minimum_z_holding_torque_nm <= 0:
        report.add(_issue("VAL-PHASE3-MOTOR-TORQUE", ValidationStatus.FAIL, "Motor torque envelope must be positive."))

    for axis in parameters.axes:
        try:
            rail = rail_class_lookup(axis.rail_class, parameters.rail_classes)
        except (KeyError, ValueError) as exc:
            report.add(
                _issue(
                    "VAL-PHASE3-RAIL-CLASS",
                    ValidationStatus.FAIL,
                    f"{axis.axis} rail class is unresolved: {exc}",
                )
            )
            continue
        if axis.rail_count < 2 or axis.carriages_per_rail < 2:
            report.add(
                _issue(
                    "VAL-PHASE3-GUIDE-COUNT",
                    ValidationStatus.FAIL,
                    f"{axis.axis} requires separated rails and two carriages per rail for the selected moment path.",
                )
            )
        if axis.rail_center_spacing_mm <= 0 or axis.rail_length_mm <= axis.travel_mm:
            report.add(
                _issue(
                    "VAL-PHASE3-RAIL-TRAVEL",
                    ValidationStatus.FAIL,
                    f"{axis.axis} rail spacing/length does not provide a positive travel margin.",
                )
            )
        if axis.screw_lead_mm not in parameters.screw_candidate_leads_mm:
            report.add(
                _issue(
                    "VAL-PHASE3-SCREW-LEAD",
                    ValidationStatus.FAIL,
                    f"{axis.axis} screw lead is outside the Phase 3 candidate set.",
                )
            )
        if axis.screw_length_mm < axis.screw_unsupported_length_mm:
            report.add(
                _issue(
                    "VAL-PHASE3-SCREW-LENGTH",
                    ValidationStatus.FAIL,
                    f"{axis.axis} screw length cannot cover its unsupported span.",
                )
            )
        axis_screen = next(item for item in screen.axes if item.axis == axis.axis)
        if axis.commissioning_feed_mm_min > axis_screen.screw.screened_max_feed_mm_min:
            report.add(
                _issue(
                    "VAL-PHASE3-FEED-WHIP",
                    ValidationStatus.FAIL,
                    f"{axis.axis} commissioning feed exceeds the 70% screw critical-speed screen.",
                )
            )
        if rail.dynamic_load_kn <= 0 or rail.static_load_kn <= 0:
            report.add(
                _issue(
                    "VAL-PHASE3-RAIL-DATA",
                    ValidationStatus.FAIL,
                    f"{axis.axis} rail class has no positive capacity reference.",
                )
            )

    if parameters.bearing_bore_mm != 8.0:
        report.add(
            _issue(
                "VAL-PHASE3-BEARING-INTERFACE",
                ValidationStatus.WARNING,
                "The current generic bearing interface is not the planned 8 mm T8 screw envelope.",
                severity=IssueSeverity.WARNING,
            )
        )
    return report

def phase3_gate_report(
    parameters: Phase3MotionParameters = PHASE3_MOTION_PARAMETERS,
) -> ValidationReport:
    """Report evidence that is intentionally still missing at the Phase 3 gate."""

    report = ValidationReport()
    for evidence in (
        "exact owned motor identity and torque-speed/current data",
        "exact CNC Shield revision, driver carrier, supply, and GRBL pin map",
        "measured spindle diameter, mass, runout, cable exit, and tool retention",
        "measured rail preload/play and PETG rail-seat coupon result",
        "backlash, axial-play, repeatability, missed-step, and homing test records",
        "physical motion evidence and owner confirmation of any changes to the accepted EDR-008 baseline",
    ):
        report.add(
            _issue(
                "VAL-PHASE3-EVIDENCE",
                ValidationStatus.NOT_READY,
                f"Required before motion freeze and physical evidence closure: {evidence}.",
            )
        )
    if not parameters.physical_motion_tests:
        report.add(
            _issue(
                "VAL-PHASE3-TEST-PLAN",
                ValidationStatus.NOT_READY,
                "No physical motion test plan is recorded.",
            )
        )
    return report
