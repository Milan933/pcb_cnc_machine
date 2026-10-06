"""Foundation-stage validation checks.

These checks intentionally cover contracts and planning values only. Detailed
solid collision, access, wall, and rail-seat checks will consume a CAD
backend adapter after the skeleton model exists.
"""

from __future__ import annotations

from cad.parameters import INITIAL_PARAMETERS, ProjectParameters

from .model import (
    AxisCapacity,
    IssueSeverity,
    PrintOrientationCandidate,
    PrintablePart,
    RuleDefinition,
    ValidationIssue,
    ValidationReport,
    ValidationStatus,
    WorkingEnvelopeRequirement,
)


RULE_CATALOG: tuple[RuleDefinition, ...] = (
    RuleDefinition("VAL-PARAMETERS", "Centralized parameter consistency", 1, False),
    RuleDefinition("VAL-FRAME-MATERIAL", "Predominantly printed frame constraint", 2, False),
    RuleDefinition("VAL-PRINT-PLANNING-X", "Planning X envelope vs printer volume", 1, False),
    RuleDefinition("VAL-PRINT-PLANNING-Y", "Planning Y envelope vs printer volume", 1, False),
    RuleDefinition("VAL-PRINT-PLANNING-Z", "Planning Z envelope vs printer volume", 1, False),
    RuleDefinition("VAL-PRINT-EVIDENCE", "Print-orientation manufacturing evidence", 6, True),
    RuleDefinition("VAL-TRAVEL-X", "Required X working travel", 5, False),
    RuleDefinition("VAL-TRAVEL-Y", "Required Y working travel", 5, False),
    RuleDefinition("VAL-TRAVEL-Z", "Required Z working travel", 5, False),
    RuleDefinition("VAL-RAIL-TRAVEL", "Rail-carriage usable travel", 8, True),
    RuleDefinition("VAL-SCREW-TRAVEL", "Lead-screw usable travel", 8, True),
    RuleDefinition("VAL-COLLISION", "Assembly solid and swept-volume collisions", 8, True),
    RuleDefinition("VAL-SPINDLE-CLEARANCE", "Spindle clearance", 8, True),
    RuleDefinition("VAL-SPINDLE-BED", "Spindle-to-bed clearance", 8, True),
    RuleDefinition("VAL-MOTOR-CLEARANCE", "Motor and connector clearance", 8, True),
    RuleDefinition("VAL-COUPLER-CLEARANCE", "Coupler and screw-support clearance", 8, True),
    RuleDefinition("VAL-SCREW-ACCESS", "Screw and tool accessibility", 8, True),
    RuleDefinition("VAL-ASSEMBLY-ACCESS", "Assembly and service accessibility", 8, True),
    RuleDefinition("VAL-WALL-THICKNESS", "Minimum printed wall thickness", 8, True),
    RuleDefinition("VAL-FASTENER-EDGE", "Minimum fastener edge distance", 8, True),
    RuleDefinition("VAL-FASTEN-SIZE-HIERARCHY", "Standard M3/M4/M5 insert hierarchy", 3, False),
    RuleDefinition("VAL-FASTEN-FAMILY-COMPLETENESS", "Central insert family completeness", 3, False),
    RuleDefinition("VAL-FASTEN-MEASURE-BEFORE-MANUFACTURE", "Measured insert dimensions before pilot release", 6, True),
    RuleDefinition("VAL-FASTEN-BOSS-WALL", "Heat-set insert boss material", 8, True),
    RuleDefinition("VAL-FASTEN-EDGE-DISTANCE", "Heat-set insert and fastener edge distance", 8, True),
    RuleDefinition("VAL-FASTEN-TOOL-ACCESS", "Insert installation and tightening access", 8, True),
    RuleDefinition("VAL-FASTEN-GEOMETRIC-TRANSFER", "Printed location and shear-transfer geometry", 8, True),
    RuleDefinition("VAL-FASTEN-THROUGH-BOLT", "Justified selective through-bolt use", 8, True),
    RuleDefinition("VAL-FASTEN-M5-JUSTIFICATION", "M5 structural-use justification", 8, True),
    RuleDefinition("VAL-RAIL-SEAT", "Linear-rail mounting surface", 8, True),
    RuleDefinition("VAL-PRINT-VOLUME", "Realistic print orientation in build volume", 6, True),
    RuleDefinition("VAL-PHASE2-TRAVEL-X", "Phase 2 skeleton X travel packaging", 2, False),
    RuleDefinition("VAL-PHASE2-TRAVEL-Y", "Phase 2 skeleton Y travel packaging", 2, False),
    RuleDefinition("VAL-PHASE2-TRAVEL-Z", "Phase 2 skeleton Z travel packaging", 2, False),
    RuleDefinition("VAL-PHASE2-BED-X", "Phase 2 bed envelope X packaging", 2, False),
    RuleDefinition("VAL-PHASE2-BED-Y", "Phase 2 bed envelope Y packaging", 2, False),
    RuleDefinition("VAL-PHASE2-GANTRY-SPAN", "Phase 2 gantry span packaging", 2, False),
    RuleDefinition("VAL-PHASE2-BASE-X", "Phase 2 base envelope X packaging", 2, False),
    RuleDefinition("VAL-PHASE2-BASE-Y", "Phase 2 base envelope Y packaging", 2, False),
    RuleDefinition("VAL-PHASE2-Z-GUIDE-SPACING", "Phase 2 dual Z guide interface", 2, False),
    RuleDefinition("VAL-PHASE2-Z-OVERHANG", "Phase 2 tool-point overhang", 2, False),
    RuleDefinition("VAL-PHASE2-PRINT-BOUND", "Phase 2 skeleton print bound", 2, False),
)


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


def check_project_parameters(parameters: ProjectParameters) -> ValidationReport:
    """Check basic ordering and positivity of centralized planning inputs."""

    report = ValidationReport()
    positive_values = (
        ("target_x_travel_mm", parameters.target_x_travel_mm),
        ("target_y_travel_mm", parameters.target_y_travel_mm),
        ("target_z_min_mm", parameters.target_z_travel_mm.minimum),
        ("target_z_max_mm", parameters.target_z_travel_mm.maximum),
        *(
            (f"voron_build_volume_{axis}", value)
            for axis, value in zip("xyz", parameters.voron_build_volume_mm)
        ),
    )
    for name, value in positive_values:
        if value <= 0:
            report.add(
                _issue(
                    "VAL-PARAMETERS",
                    ValidationStatus.FAIL,
                    f"{name} must be greater than zero; got {value}.",
                )
            )

    if not parameters.target_z_travel_mm.is_ordered():
        report.add(
            _issue(
                "VAL-PARAMETERS",
                ValidationStatus.FAIL,
                "The target Z travel range is reversed.",
            )
        )

    if not parameters.frame_is_predominantly_printed:
        report.add(
            _issue(
                "VAL-FRAME-MATERIAL",
                ValidationStatus.FAIL,
                "The foundation parameter set does not mark the frame as predominantly printed.",
            )
        )

    if not report.issues:
        report.add(
            _issue(
                "VAL-PARAMETERS",
                ValidationStatus.PASS,
                "Centralized foundation parameters are ordered and positive.",
                severity=IssueSeverity.INFO,
            )
        )
    return report


def check_working_envelope(
    requirement: WorkingEnvelopeRequirement,
    capacity: AxisCapacity,
) -> ValidationReport:
    """Compare required tool-point travel with usable axis capacity."""

    report = ValidationReport()
    comparisons = (
        ("VAL-TRAVEL-X", "X", requirement.x_travel_mm, capacity.x_travel_mm),
        ("VAL-TRAVEL-Y", "Y", requirement.y_travel_mm, capacity.y_travel_mm),
        (
            "VAL-TRAVEL-Z",
            "Z",
            requirement.z_travel_mm.maximum,
            capacity.z_travel_mm,
        ),
    )
    for rule_id, axis, required, available in comparisons:
        if available < required:
            report.add(
                _issue(
                    rule_id,
                    ValidationStatus.FAIL,
                    f"{axis} usable travel {available:g} mm is below the "
                    f"planning target {required:g} mm.",
                )
            )
        else:
            report.add(
                _issue(
                    rule_id,
                    ValidationStatus.PASS,
                    f"{axis} usable travel {available:g} mm meets the "
                    f"planning target {required:g} mm.",
                    severity=IssueSeverity.INFO,
                )
            )
    return report


def check_target_envelope_within_build_volume(
    parameters: ProjectParameters,
) -> ValidationReport:
    """Check planning-envelope fit against the printer, not machine travel."""

    report = ValidationReport()
    required = (
        ("X", parameters.target_x_travel_mm, parameters.voron_build_volume_mm[0]),
        ("Y", parameters.target_y_travel_mm, parameters.voron_build_volume_mm[1]),
        ("Z", parameters.target_z_travel_mm.maximum, parameters.voron_build_volume_mm[2]),
    )
    for axis, target, build_limit in required:
        rule_id = f"VAL-PRINT-PLANNING-{axis}"
        if target <= build_limit:
            report.add(
                _issue(
                    rule_id,
                    ValidationStatus.PASS,
                    f"Preliminary {axis} envelope target {target:g} mm fits the "
                    f"nominal printer dimension {build_limit:g} mm.",
                    severity=IssueSeverity.INFO,
                    evidence="This is a planning comparison only; usable print margins are not yet measured.",
                )
            )
        else:
            report.add(
                _issue(
                    rule_id,
                    ValidationStatus.FAIL,
                    f"Preliminary {axis} envelope target {target:g} mm exceeds "
                    f"the nominal printer dimension {build_limit:g} mm.",
                    evidence="Re-evaluate architecture or document a different print strategy.",
                )
            )
    return report


def _fits(
    extents: tuple[float, float, float],
    build_volume: tuple[float, float, float],
) -> bool:
    return all(extent > 0 and extent <= limit for extent, limit in zip(extents, build_volume))


def check_printable_part(
    part: PrintablePart,
    build_volume_mm: tuple[float, float, float],
) -> ValidationReport:
    """Require at least one documented, realistic print orientation."""

    report = ValidationReport()
    if not part.orientations:
        report.add(
            _issue(
                "VAL-PRINT-VOLUME",
                ValidationStatus.NOT_READY,
                "No realistic print orientation has been documented.",
                component=part.name,
            )
        )
        return report

    candidates_without_notes = [
        candidate.name
        for candidate in part.orientations
        if not candidate.manufacturing_notes.strip()
    ]
    if candidates_without_notes:
        report.add(
            _issue(
                "VAL-PRINT-EVIDENCE",
                ValidationStatus.NOT_READY,
                "Each print orientation must include manufacturing notes covering "
                "support, bed contact, critical faces, and post-processing.",
                component=part.name,
                evidence=", ".join(candidates_without_notes),
            )
        )

    documented_candidates = [
        candidate
        for candidate in part.orientations
        if candidate.manufacturing_notes.strip()
    ]
    if not documented_candidates:
        return report

    fitting_candidates: list[PrintOrientationCandidate] = []
    for candidate in documented_candidates:
        if _fits(candidate.extents_mm, build_volume_mm):
            fitting_candidates.append(candidate)

    if fitting_candidates:
        names = ", ".join(candidate.name for candidate in fitting_candidates)
        report.add(
            _issue(
                "VAL-PRINT-VOLUME",
                ValidationStatus.PASS,
                f"At least one documented orientation fits the configured build volume: {names}.",
                severity=IssueSeverity.INFO,
                component=part.name,
                evidence="Orientation extents and manufacturing notes supplied by the part module.",
            )
        )
    else:
        report.add(
            _issue(
                "VAL-PRINT-VOLUME",
                ValidationStatus.FAIL,
                "No documented orientation fits the configured build volume.",
                component=part.name,
                evidence="Compare each candidate's extents with the usable volume and print notes.",
            )
        )
    return report


def run_foundation_checks(
    parameters: ProjectParameters = INITIAL_PARAMETERS,
) -> ValidationReport:
    """Run checks that are meaningful before detailed geometry exists."""

    report = ValidationReport()
    report.extend(check_project_parameters(parameters))
    report.extend(
        check_target_envelope_within_build_volume(parameters)
    )
    return report
