"""Backend-independent PETG fastening strategy checks.

The checks cover reusable interface contracts before production structural CAD
exists.  Supplier-dependent insert dimensions intentionally produce an
explicit not-ready warning until an actual insert is selected and measured.
"""

from __future__ import annotations

from cad.parameters import (
    FastenerInterfaceParameter,
    FastenerStrategyParameters,
    InsertFamilyParameters,
    PHASE3A_FASTENER_INTERFACE_SCREENS,
    PHASE3A_FASTENER_STRATEGY,
)

from .validation.model import (
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


def _family_by_size(parameters: FastenerStrategyParameters) -> dict[str, InsertFamilyParameters]:
    return {family.nominal_size: family for family in parameters.insert_families}


def check_fastening_strategy(
    parameters: FastenerStrategyParameters = PHASE3A_FASTENER_STRATEGY,
) -> ValidationReport:
    """Validate the standard hierarchy and its evidence boundary."""

    report = ValidationReport()
    allowed = parameters.allowed_insert_sizes
    if allowed != ("M3", "M4", "M5") or len(set(allowed)) != len(allowed):
        report.add(
            _issue(
                "VAL-FASTEN-SIZE-HIERARCHY",
                ValidationStatus.FAIL,
                "The PETG insert hierarchy must be exactly M3, M4, and M5 with no duplicate or extra default sizes.",
            )
        )

    families = _family_by_size(parameters)
    if set(families) != set(allowed):
        report.add(
            _issue(
                "VAL-FASTEN-FAMILY-COMPLETENESS",
                ValidationStatus.FAIL,
                "Every standardized insert size must have one central family definition.",
                evidence=f"allowed={allowed}; defined={tuple(families)}",
            )
        )

    for use, size in parameters.default_size_by_use:
        if size not in allowed:
            report.add(
                _issue(
                    "VAL-FASTEN-SIZE-HIERARCHY",
                    ValidationStatus.FAIL,
                    f"Default fastening use '{use}' refers to non-standard size {size}.",
                )
            )
    if not parameters.core_principle:
        report.add(
            _issue(
                "VAL-FASTEN-CORE-PRINCIPLE",
                ValidationStatus.FAIL,
                "The fastening strategy must state the preload versus geometric load-transfer principle.",
            )
        )

    for family in parameters.insert_families:
        if family.minimum_surrounding_wall_mm <= 0 or family.minimum_edge_distance_mm <= 0:
            report.add(
                _issue(
                    "VAL-FASTEN-BOSS-WALL",
                    ValidationStatus.FAIL,
                    "Preliminary insert-boss wall and edge screens must be positive.",
                    component=family.nominal_size,
                )
            )
        if any(value <= 0 for value in family.installation_tool_access_mm):
            report.add(
                _issue(
                    "VAL-FASTEN-TOOL-ACCESS",
                    ValidationStatus.FAIL,
                    "Insert installation-tool access screens must be positive in all directions.",
                    component=family.nominal_size,
                )
            )
        if not family.exact_dimensions_resolved:
            report.add(
                _issue(
                    "VAL-FASTEN-MEASURE-BEFORE-MANUFACTURE",
                    ValidationStatus.NOT_READY,
                    f"{family.nominal_size} insert OD, length, pilot, insertion depth, and screw-clearance dimensions are not selected and measured.",
                    severity=IssueSeverity.WARNING,
                    component=family.nominal_size,
                    evidence=family.notes,
                )
            )

    if not report.issues:
        report.add(
            _issue(
                "VAL-FASTEN-SIZE-HIERARCHY",
                ValidationStatus.PASS,
                "PETG fastening hierarchy and family definitions are internally consistent.",
                severity=IssueSeverity.INFO,
            )
        )
    return report


def check_fastener_interface(
    interface: FastenerInterfaceParameter,
    parameters: FastenerStrategyParameters = PHASE3A_FASTENER_STRATEGY,
) -> ValidationReport:
    """Check boss material, edge distance, access, and geometric load transfer."""

    report = ValidationReport()
    families = _family_by_size(parameters)
    mode = interface.fastening_mode
    if mode not in {"insert", "through_bolt"}:
        report.add(
            _issue(
                "VAL-FASTEN-MODE",
                ValidationStatus.FAIL,
                f"Unsupported fastening mode '{mode}'.",
                component=interface.interface_id,
            )
        )
        return report

    if interface.boss_wall_mm <= 0:
        report.add(
            _issue(
                "VAL-FASTEN-BOSS-WALL",
                ValidationStatus.FAIL,
                "The interface must declare positive surrounding boss material.",
                component=interface.interface_id,
            )
        )
    if interface.edge_distance_mm <= 0:
        report.add(
            _issue(
                "VAL-FASTEN-EDGE-DISTANCE",
                ValidationStatus.FAIL,
                "The interface must declare positive edge distance.",
                component=interface.interface_id,
            )
        )
    if any(value <= 0 for value in interface.installation_tool_access_mm):
        report.add(
            _issue(
                "VAL-FASTEN-TOOL-ACCESS",
                ValidationStatus.FAIL,
                "The interface must provide positive insertion and tightening-tool access.",
                component=interface.interface_id,
            )
        )
    if not interface.load_transfer_features:
        report.add(
            _issue(
                "VAL-FASTEN-GEOMETRIC-TRANSFER",
                ValidationStatus.FAIL,
                "Fasteners cannot be the only location or shear-transfer feature; declare a mating shoulder, key, pocket, rib, or equivalent.",
                component=interface.interface_id,
            )
        )

    if mode == "insert":
        if interface.insert_size not in parameters.allowed_insert_sizes:
            report.add(
                _issue(
                    "VAL-FASTEN-SIZE-HIERARCHY",
                    ValidationStatus.FAIL,
                    f"Insert size {interface.insert_size!r} is outside the M3/M4/M5 hierarchy.",
                    component=interface.interface_id,
                )
            )
        else:
            family = families.get(interface.insert_size)
            if family is None:
                report.add(
                    _issue(
                        "VAL-FASTEN-FAMILY-COMPLETENESS",
                        ValidationStatus.FAIL,
                        f"No central insert family exists for {interface.insert_size}.",
                        component=interface.interface_id,
                    )
                )
            else:
                if interface.boss_wall_mm < family.minimum_surrounding_wall_mm:
                    report.add(
                        _issue(
                            "VAL-FASTEN-BOSS-WALL",
                            ValidationStatus.FAIL,
                            f"Declared boss wall {interface.boss_wall_mm:.2f} mm is below the {family.nominal_size} preliminary screen of {family.minimum_surrounding_wall_mm:.2f} mm.",
                            component=interface.interface_id,
                        )
                    )
                if interface.edge_distance_mm < family.minimum_edge_distance_mm:
                    report.add(
                        _issue(
                            "VAL-FASTEN-EDGE-DISTANCE",
                            ValidationStatus.FAIL,
                            f"Declared edge distance {interface.edge_distance_mm:.2f} mm is below the {family.nominal_size} preliminary screen of {family.minimum_edge_distance_mm:.2f} mm.",
                            component=interface.interface_id,
                        )
                    )
                if any(
                    actual < required
                    for actual, required in zip(
                        interface.installation_tool_access_mm,
                        family.installation_tool_access_mm,
                    )
                ):
                    report.add(
                        _issue(
                            "VAL-FASTEN-TOOL-ACCESS",
                            ValidationStatus.FAIL,
                            f"The interface does not meet the {family.nominal_size} installation-tool access screen.",
                            component=interface.interface_id,
                        )
                    )
                if interface.insert_size == "M5" and not interface.size_justification:
                    report.add(
                        _issue(
                            "VAL-FASTEN-M5-JUSTIFICATION",
                            ValidationStatus.FAIL,
                            "M5 requires an explicit load-path and capacity justification; it is not a default structural size.",
                            component=interface.interface_id,
                        )
                    )
                if interface.requires_selected_insert and not family.exact_dimensions_resolved:
                    report.add(
                        _issue(
                            "VAL-FASTEN-MEASURE-BEFORE-MANUFACTURE",
                            ValidationStatus.NOT_READY,
                            f"Do not freeze the {family.nominal_size} pilot or pocket from this review screen until the actual insert is measured and coupon-tested.",
                            severity=IssueSeverity.WARNING,
                            component=interface.interface_id,
                            evidence=family.notes,
                        )
                    )

    if mode == "through_bolt":
        if interface.insert_size is not None:
            report.add(
                _issue(
                    "VAL-FASTEN-MODE",
                    ValidationStatus.FAIL,
                    "A through-bolt interface must not be represented as an insert interface.",
                    component=interface.interface_id,
                )
            )
        if not interface.through_bolt_justification:
            report.add(
                _issue(
                    "VAL-FASTEN-THROUGH-BOLT",
                    ValidationStatus.FAIL,
                    "Through-bolts require a documented pull-out, creep, preload, moment, cyclic-load, or failure-consequence justification.",
                    component=interface.interface_id,
                )
            )

    if not report.issues:
        report.add(
            _issue(
                "VAL-FASTEN-INTERFACE",
                ValidationStatus.PASS,
                "Fastener preload, geometry-based location/shear transfer, material, edge, and access screens pass.",
                severity=IssueSeverity.INFO,
                component=interface.interface_id,
            )
        )
    return report


def check_phase3a_fastener_interfaces(
    interfaces: tuple[FastenerInterfaceParameter, ...] = PHASE3A_FASTENER_INTERFACE_SCREENS,
    parameters: FastenerStrategyParameters = PHASE3A_FASTENER_STRATEGY,
) -> ValidationReport:
    """Validate the review-only interfaces attached to Phase 3A packaging."""

    report = check_fastening_strategy(parameters)
    interface_ids = [interface.interface_id for interface in interfaces]
    if len(interface_ids) != len(set(interface_ids)):
        report.add(
            _issue(
                "VAL-FASTEN-INTERFACE-ID",
                ValidationStatus.FAIL,
                "Fastener interface IDs must be unique.",
            )
        )
    for interface in interfaces:
        report.extend(check_fastener_interface(interface, parameters))
    return report
