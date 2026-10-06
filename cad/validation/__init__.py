"""Backend-independent validation primitives and foundation checks."""

from .checks import (
    RULE_CATALOG,
    check_printable_part,
    check_project_parameters,
    check_target_envelope_within_build_volume,
    check_working_envelope,
    run_foundation_checks,
)
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

__all__ = [
    "AxisCapacity",
    "IssueSeverity",
    "PrintOrientationCandidate",
    "PrintablePart",
    "RuleDefinition",
    "ValidationIssue",
    "ValidationReport",
    "ValidationStatus",
    "WorkingEnvelopeRequirement",
    "RULE_CATALOG",
    "check_printable_part",
    "check_project_parameters",
    "check_target_envelope_within_build_volume",
    "check_working_envelope",
    "run_foundation_checks",
]
