"""Fail-closed checks for the first Phase 5 manufacturing-CAD batch."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cad.parts.phase5_structural import (
    PHASE5_BASE_PAIR_PARAMETERS,
    PHASE5_BASE_PART_IDS,
    Phase5BasePairParameters,
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


def _vector_tuple(vector: Any) -> tuple[float, float, float]:
    return tuple(float(getattr(vector, axis)) for axis in ("X", "Y", "Z"))


def _shape_is_valid(shape: Any) -> bool:
    value = getattr(shape, "is_valid", False)
    return bool(value() if callable(value) else value)


def _solid_count(shape: Any) -> int:
    value = getattr(shape, "solids", ())
    solids = value() if callable(value) else value
    return len(solids)


def check_phase5_base_pair_geometry(
    parts: Mapping[str, Any],
    parameters: Phase5BasePairParameters = PHASE5_BASE_PAIR_PARAMETERS,
) -> ValidationReport:
    """Validate actual fused candidate solids without granting release status."""

    report = ValidationReport()
    expected_size = (
        parameters.part_width_mm,
        parameters.part_length_mm,
        parameters.overall_height_mm,
    )
    for part_id in PHASE5_BASE_PART_IDS:
        shape = parts.get(part_id)
        if shape is None:
            report.add(
                _issue(
                    "VAL-PHASE5-PART-PRESENT",
                    ValidationStatus.FAIL,
                    "The first Phase 5 batch must contain both integrated base parts.",
                    component=part_id,
                )
            )
            continue

        if not _shape_is_valid(shape):
            report.add(
                _issue(
                    "VAL-PHASE5-SOLID-VALID",
                    ValidationStatus.FAIL,
                    "The generated base candidate is not a valid CAD shape.",
                    component=part_id,
                )
            )
        else:
            report.add(
                _issue(
                    "VAL-PHASE5-SOLID-VALID",
                    ValidationStatus.PASS,
                    "The generated base candidate reports a valid CAD shape.",
                    severity=IssueSeverity.INFO,
                    component=part_id,
                )
            )

        solid_count = _solid_count(shape)
        if solid_count != 1:
            report.add(
                _issue(
                    "VAL-PHASE5-SINGLE-SOLID",
                    ValidationStatus.FAIL,
                    "Each integrated base candidate must be one fused printable solid, not a review compound.",
                    component=part_id,
                    evidence=f"solid_count={solid_count}",
                )
            )
        else:
            report.add(
                _issue(
                    "VAL-PHASE5-SINGLE-SOLID",
                    ValidationStatus.PASS,
                    "The integrated base candidate is one fused solid.",
                    severity=IssueSeverity.INFO,
                    component=part_id,
                )
            )

        size = _vector_tuple(shape.bounding_box().size)
        if any(abs(actual - expected) > 0.01 for actual, expected in zip(size, expected_size)):
            report.add(
                _issue(
                    "VAL-PHASE5-EXTENTS",
                    ValidationStatus.FAIL,
                    "The candidate bounding box does not match the parametric print contract.",
                    component=part_id,
                    evidence=f"actual={size}; expected={expected_size}",
                )
            )
        else:
            report.add(
                _issue(
                    "VAL-PHASE5-EXTENTS",
                    ValidationStatus.PASS,
                    "The candidate fits the declared 150 x 300 mm print footprint and height.",
                    severity=IssueSeverity.INFO,
                    component=part_id,
                    evidence=f"bbox={size}",
                )
            )
        if max(size[:2]) > 320.0 + 1e-6:
            report.add(
                _issue(
                    "VAL-PHASE5-PRINT-BOUND",
                    ValidationStatus.FAIL,
                    "The candidate exceeds the conservative 320 mm XY printer bound.",
                    component=part_id,
                    evidence=f"bbox={size}",
                )
            )

    report.add(
        _issue(
            "VAL-PHASE5-PROVISIONAL-INTERFACES",
            ValidationStatus.NOT_READY,
            "Rail fastener openings, foot openings, and center-tie openings use explicitly provisional hardware dimensions.",
            severity=IssueSeverity.WARNING,
            evidence=(
                "Measure representative rails, fasteners, inserts, feet, and the center tie before fit or production claims; "
                "owner-supplied NEMA17 and Arduino Mega + CNC Shield remain outside this base-pair fit contract."
            ),
        )
    )
    report.add(
        _issue(
            "VAL-PHASE5-MATURITY",
            ValidationStatus.NOT_READY,
            "The first base pair is PROTOTYPE-STL: suitable for owner slicing and fit review, not RELEASED or HARDWARE-VALIDATED.",
            severity=IssueSeverity.WARNING,
        )
    )
    return report


def check_phase5_export_files(paths: Mapping[str, Any]) -> ValidationReport:
    """Check that requested local STEP/STL derivatives exist and are non-empty."""

    report = ValidationReport()
    for key, path in sorted(paths.items()):
        path_obj = path
        if not path_obj.exists() or path_obj.stat().st_size <= 0:
            report.add(
                _issue(
                    "VAL-PHASE5-EXPORT-FILE",
                    ValidationStatus.FAIL,
                    "A requested local manufacturing derivative is missing or empty.",
                    component=key,
                    evidence=str(path_obj),
                )
            )
        else:
            report.add(
                _issue(
                    "VAL-PHASE5-EXPORT-FILE",
                    ValidationStatus.PASS,
                    "The local manufacturing derivative exists and is non-empty.",
                    severity=IssueSeverity.INFO,
                    component=key,
                    evidence=f"{path_obj} ({path_obj.stat().st_size} bytes)",
                )
            )
    return report


def phase5_gate_report() -> ValidationReport:
    """Report the owner-authorized Phase 5 boundary and the release stop."""

    report = ValidationReport()
    report.add(
        _issue(
            "VAL-PHASE5-AUTHORIZATION",
            ValidationStatus.PASS,
            "Phase 5 manufacturing CAD is owner-authorized for the first base-pair batch.",
            severity=IssueSeverity.INFO,
            evidence="Owner authorization references baseline afe2e14089467321b323d74f928a7ab4c5ffdc1f.",
        )
    )
    report.add(
        _issue(
            "VAL-PHASE5-BATCH-SCOPE",
            ValidationStatus.PASS,
            "This batch is limited to base_left_integrated and base_right_integrated; remaining structural parts are not started.",
            severity=IssueSeverity.INFO,
        )
    )
    report.add(
        _issue(
            "VAL-PHASE5-RELEASE-BOUNDARY",
            ValidationStatus.NOT_READY,
            "Physical first-print, measured-hardware fit, PETG process, and review evidence are still required before manufacturing release.",
            severity=IssueSeverity.WARNING,
        )
    )
    return report


__all__ = [
    "check_phase5_base_pair_geometry",
    "check_phase5_export_files",
    "phase5_gate_report",
]
