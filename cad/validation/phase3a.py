"""Fail-closed checks for the Phase 3A compact packaging review."""

from __future__ import annotations

from typing import Any

from cad.packaging_phase3a import phase3a_packaging_study
from cad.parameters import (
    INITIAL_PARAMETERS,
    PHASE3A_PACKAGING_VARIANTS,
    PHASE3_MOTION_PARAMETERS,
    Phase3APackagingVariant,
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


def check_phase3a_packaging_variant(
    variant: Phase3APackagingVariant,
) -> ValidationReport:
    """Validate one variant's dimensional and screening contracts."""

    report = ValidationReport()
    try:
        study = phase3a_packaging_study(variant)
    except (KeyError, ValueError, StopIteration) as exc:
        report.add(
            _issue(
                "VAL-PHASE3A-CALCULATION-INPUT",
                ValidationStatus.FAIL,
                f"Packaging calculations could not be evaluated: {exc}",
            )
        )
        return report

    if variant.body_max_z_mm - variant.body_min_z_mm != variant.body_envelope_mm[2]:
        report.add(
            _issue(
                "VAL-PHASE3A-BODY-HEIGHT",
                ValidationStatus.FAIL,
                "Body envelope height must equal the declared top-minus-bottom stack.",
            )
        )
    if any(value <= 0 for value in variant.body_envelope_mm + variant.service_footprint_mm):
        report.add(
            _issue(
                "VAL-PHASE3A-ENVELOPE-POSITIVE",
                ValidationStatus.FAIL,
                "Body and service envelopes must be positive.",
            )
        )
    if variant.body_min_z_mm >= variant.body_max_z_mm:
        report.add(
            _issue(
                "VAL-PHASE3A-Z-ORDER",
                ValidationStatus.FAIL,
                "Body Z limits must be ordered.",
            )
        )

    pcb_x, pcb_y = variant.working_area_mm
    tx, ty, tz = variant.tool_travel_mm
    if tx < pcb_x or ty < pcb_y or tz <= 0:
        report.add(
            _issue(
                "VAL-PHASE3A-TRAVEL",
                ValidationStatus.FAIL,
                "Tool travel must cover the required 200 x 150 mm PCB area and have positive Z travel.",
            )
        )
    if variant.variant_id == "P3":
        report.add(
            _issue(
                "VAL-PHASE3A-P3-TRAVEL-MARGIN",
                ValidationStatus.PASS,
                "P3 deliberately reduces the XY tool-point access margin to 5 mm per side; owner confirmation is required.",
                severity=IssueSeverity.WARNING,
                evidence="P3 tool travel is 210 x 160 mm for a 200 x 150 mm PCB working area.",
            )
        )

    bed_x, bed_y, bed_t = variant.bed_support_mm
    margin_x, margin_y = study.bed.pcb_edge_margin_mm
    if bed_x < pcb_x or bed_y < pcb_y or bed_t <= 0:
        report.add(
            _issue(
                "VAL-PHASE3A-BED-SUPPORT",
                ValidationStatus.FAIL,
                "Bed support must cover the PCB working area with positive thickness.",
            )
        )
    if margin_x < variant.pcb_edge_margin_mm[0] or margin_y < variant.pcb_edge_margin_mm[1]:
        report.add(
            _issue(
                "VAL-PHASE3A-BED-MARGIN",
                ValidationStatus.FAIL,
                "Calculated PCB edge margins are below the declared variant margins.",
            )
        )
    if study.bed.transverse_bed_overhang_mm < 0 or study.bed.longitudinal_bed_overhang_mm < 0:
        report.add(
            _issue(
                "VAL-PHASE3A-BED-GUIDE-SUPPORT",
                ValidationStatus.FAIL,
                "The bed must not be narrower than the 220 mm guide spacing or the two-block longitudinal group.",
            )
        )
    if study.bed.swept_bed_end_clearance_mm < variant.bed_sweep_end_clearance_mm - 1e-6:
        report.add(
            _issue(
                "VAL-PHASE3A-BED-SWEEP",
                ValidationStatus.FAIL,
                "Full Y bed sweep does not retain the declared front/rear body clearance.",
                evidence=(
                    f"calculated {study.bed.swept_bed_end_clearance_mm:g} mm per end; "
                    f"declared {variant.bed_sweep_end_clearance_mm:g} mm"
                ),
            )
        )
    if study.bed.bed_to_y_motor_clearance_mm <= 0:
        report.add(
            _issue(
                "VAL-PHASE3A-Y-MOTOR-COLLISION",
                ValidationStatus.FAIL,
                "The moving-bed underside intersects the Y motor envelope at full travel.",
                evidence=f"vertical gap {study.bed.bed_to_y_motor_clearance_mm:g} mm",
            )
        )
    elif study.bed.bed_to_y_motor_clearance_mm < 5.0:
        report.add(
            _issue(
                "VAL-PHASE3A-Y-MOTOR-CLEARANCE",
                ValidationStatus.PASS,
                "Y motor is vertically separated from the swept moving bed, but the clearance is tight and must be mocked up.",
                severity=IssueSeverity.WARNING,
                evidence=f"vertical gap {study.bed.bed_to_y_motor_clearance_mm:g} mm",
            )
        )
    if any(clearance < 0 for clearance in study.bed.tool_to_bed_clearance_mm):
        report.add(
            _issue(
                "VAL-PHASE3A-TOOL-BED-COLLISION",
                ValidationStatus.FAIL,
                "Screened tool travel extends beyond the proposed bed support envelope.",
                evidence=f"tool-to-bed clearances {study.bed.tool_to_bed_clearance_mm}",
            )
        )
    if any(clearance < 0 for clearance in study.bed.spindle_swept_body_clearance_mm):
        report.add(
            _issue(
                "VAL-PHASE3A-SPINDLE-BODY-COLLISION",
                ValidationStatus.FAIL,
                "The swept generic spindle envelope extends outside the body package.",
                evidence=f"spindle-to-body clearances {study.bed.spindle_swept_body_clearance_mm}",
            )
        )
    bearing_sizes = variant.bearing_fixed_envelopes_mm + variant.bearing_floating_envelopes_mm
    if any(any(value <= 0 for value in size) for _, size in bearing_sizes):
        report.add(
            _issue(
                "VAL-PHASE3A-BEARING-ENVELOPE",
                ValidationStatus.FAIL,
                "All fixed and floating bearing review envelopes must be positive.",
            )
        )

    for axis in study.axes:
        if not axis.rail_travel_passes:
            report.add(
                _issue(
                    "VAL-PHASE3A-RAIL-SWEEP",
                    ValidationStatus.FAIL,
                    f"{axis.axis} rail is {axis.rail_length_mm:g} mm but requires at least "
                    f"{axis.minimum_rail_length_mm:g} mm for full swept travel.",
                    component=axis.axis,
                    evidence=(
                        f"travel {axis.travel_mm:g} + carriage group {axis.carriage_group_span_mm:g} "
                        f"+ two end margins {2.0 * axis.declared_end_margin_mm:g}"
                    ),
                )
            )
        if axis.screw_length_mm < axis.screw_unsupported_length_mm:
            report.add(
                _issue(
                    "VAL-PHASE3A-SCREW-LENGTH",
                    ValidationStatus.FAIL,
                    f"{axis.axis} nominal screw length must cover its unsupported screening length.",
                    component=axis.axis,
                )
            )
        if not axis.feed_screen_passes:
            report.add(
                _issue(
                    "VAL-PHASE3A-FEED-WHIP",
                    ValidationStatus.FAIL,
                    f"{axis.axis} commissioning feed exceeds the 70% critical-speed screen for the compact package.",
                    component=axis.axis,
                    evidence=(
                        f"screened maximum {axis.screened_max_feed_mm_min:.1f} mm/min; "
                        f"commissioning {axis.commissioning_feed_mm_min:.1f} mm/min"
                    ),
                )
            )
        if axis.actual_end_margin_mm < 0:
            report.add(
                _issue(
                    "VAL-PHASE3A-RAIL-END-MARGIN",
                    ValidationStatus.FAIL,
                    f"{axis.axis} swept carriage group extends past the rail end.",
                    component=axis.axis,
                )
            )

    z = study.z_stack
    if z.y_motor_bottom_mm < variant.body_min_z_mm - 1e-6:
        report.add(
            _issue(
                "VAL-PHASE3A-Y-MOTOR-BOUND",
                ValidationStatus.FAIL,
                "The recessed Y motor extends below the declared body envelope.",
            )
        )
    if z.z_motor_top_mm > variant.body_max_z_mm + 1e-6:
        report.add(
            _issue(
                "VAL-PHASE3A-Z-MOTOR-BOUND",
                ValidationStatus.FAIL,
                "The Z motor/support stack extends above the declared body envelope.",
            )
        )
    if z.gantry_top_mm > variant.body_max_z_mm + 1e-6:
        report.add(
            _issue(
                "VAL-PHASE3A-GANTRY-BOUND",
                ValidationStatus.FAIL,
                "The fixed-gantry packaging bound extends above the declared body envelope.",
            )
        )
    if variant.home_limit_clearance_mm <= 0:
        report.add(
            _issue(
                "VAL-PHASE3A-HOME-CLEARANCE",
                ValidationStatus.FAIL,
                "Home/limit clearance must be positive.",
            )
        )

    build_volume = INITIAL_PARAMETERS.voron_build_volume_mm
    if any(extent > limit for extent, limit in zip(variant.largest_future_petg_print_mm, build_volume)):
        report.add(
            _issue(
                "VAL-PHASE3A-PRINT-VOLUME",
                ValidationStatus.FAIL,
                "The declared largest future PETG packaging print exceeds the nominal Voron build volume.",
                evidence=f"candidate {variant.largest_future_petg_print_mm}; build volume {build_volume}",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PHASE3A-PRINT-VOLUME",
                ValidationStatus.PASS,
                "Largest future PETG packaging print fits the nominal build-volume dimensions on paper.",
                severity=IssueSeverity.INFO,
                evidence=variant.largest_future_petg_print_notes,
            )
        )

    if variant.service_footprint_mm[0] < variant.body_envelope_mm[0] or variant.service_footprint_mm[1] < variant.body_envelope_mm[1]:
        report.add(
            _issue(
                "VAL-PHASE3A-SERVICE-FOOTPRINT",
                ValidationStatus.FAIL,
                "Service footprint must not be smaller than the machine body footprint.",
            )
        )
    report.add(
        _issue(
            "VAL-PHASE3A-PACKAGING-SCREEN",
            ValidationStatus.PASS,
            f"{variant.variant_id} passes the dependency-light packaging screen; this is not owner acceptance.",
            severity=IssueSeverity.INFO,
            evidence=(
                f"body {variant.body_envelope_mm}; rails {variant.rail_lengths_mm}; "
                f"screws {variant.screw_lengths_mm}"
            ),
        )
    )
    return report


def check_phase3a_all_variants(
    variants: tuple[Phase3APackagingVariant, ...] = PHASE3A_PACKAGING_VARIANTS,
) -> ValidationReport:
    """Validate every declared packaging variant."""

    report = ValidationReport()
    ids = [variant.variant_id for variant in variants]
    if len(ids) != len(set(ids)):
        report.add(
            _issue(
                "VAL-PHASE3A-VARIANT-IDS",
                ValidationStatus.FAIL,
                "Phase 3A variant IDs must be unique.",
            )
        )
    for variant in variants:
        report.extend(check_phase3a_packaging_variant(variant))
    return report


def check_phase3a_model_containment(
    model: Any,
    variant: Phase3APackagingVariant,
    tolerance_mm: float = 1e-6,
) -> ValidationReport:
    """Check every review shape against the declared body envelope."""

    report = ValidationReport()
    body_x, body_y, _ = variant.body_envelope_mm
    minimum = (-body_x / 2.0, -body_y / 2.0, variant.body_min_z_mm)
    maximum = (body_x / 2.0, body_y / 2.0, variant.body_max_z_mm)
    for component in model.components:
        bounding_box = component.shape.bounding_box()
        component_min = tuple(float(getattr(bounding_box.min, axis)) for axis in ("X", "Y", "Z"))
        component_max = tuple(float(getattr(bounding_box.max, axis)) for axis in ("X", "Y", "Z"))
        if any(value < limit - tolerance_mm for value, limit in zip(component_min, minimum)) or any(
            value > limit + tolerance_mm for value, limit in zip(component_max, maximum)
        ):
            report.add(
                _issue(
                    "VAL-PHASE3A-MODEL-CONTAINMENT",
                    ValidationStatus.FAIL,
                    "Review component extends outside the declared body envelope.",
                    component=component.name,
                    evidence=f"min {component_min}; max {component_max}; body min {minimum}; max {maximum}",
                )
            )
    if not report.issues:
        report.add(
            _issue(
                "VAL-PHASE3A-MODEL-CONTAINMENT",
                ValidationStatus.PASS,
                "All review envelopes are contained by the declared body package.",
                severity=IssueSeverity.INFO,
            )
        )
    return report


def phase3a_gate_report() -> ValidationReport:
    """List evidence still required before a compact package is accepted."""

    report = ValidationReport()
    for evidence in (
        "owner selection of P1, P2, or P3 and confirmation that P3 travel margin is acceptable",
        "full-travel assembly mock-up proving rail, carriage, screw, motor, homing, and tool clearances",
        "service-access review proving every fixed bearing, nut, coupler, motor, and limit fastener is removable",
        "PETG rail-seat, bearing-pocket, motor-pocket, and fastener/joint coupon evidence",
        "measured spindle envelope and workholding implementation before structural dimensions are frozen",
    ):
        report.add(
            _issue(
                "VAL-PHASE3A-GATE-EVIDENCE",
                ValidationStatus.NOT_READY,
                f"Required before Phase 3A acceptance: {evidence}.",
                evidence="Review-only packaging results do not replace physical evidence.",
            )
        )
    report.add(
        _issue(
            "VAL-PHASE3A-NO-PHASE4",
            ValidationStatus.PASS,
            "Phase 4 remains blocked by the requested owner-review boundary.",
            severity=IssueSeverity.INFO,
        )
    )
    return report
