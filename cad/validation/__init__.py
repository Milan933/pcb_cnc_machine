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
from .phase1 import (
    check_phase1_requirements,
    v_bit_isolation_width_mm,
    v_bit_width_sensitivity,
)
from .phase2 import check_phase2_skeleton_parameters, check_phase2a_parameters
from .phase3 import check_phase3_motion_parameters, phase3_gate_report

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
    "check_phase1_requirements",
    "v_bit_isolation_width_mm",
    "v_bit_width_sensitivity",
    "check_phase2_skeleton_parameters",
    "check_phase2a_parameters",
    "check_phase3_motion_parameters",
    "phase3_gate_report",
    "RULE_CATALOG",
    "check_printable_part",
    "check_project_parameters",
    "check_target_envelope_within_build_volume",
    "check_working_envelope",
    "run_foundation_checks",
]
