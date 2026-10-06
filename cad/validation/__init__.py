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
from .phase3a import (
    check_phase3a_all_variants,
    check_phase3a_model_containment,
    check_phase3a_packaging_variant,
    phase3a_gate_report,
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
    "check_phase1_requirements",
    "v_bit_isolation_width_mm",
    "v_bit_width_sensitivity",
    "check_phase2_skeleton_parameters",
    "check_phase2a_parameters",
    "check_phase3_motion_parameters",
    "phase3_gate_report",
    "check_phase3a_all_variants",
    "check_phase3a_model_containment",
    "check_phase3a_packaging_variant",
    "phase3a_gate_report",
    "check_fastener_interface",
    "check_fastening_strategy",
    "check_phase3a_fastener_interfaces",
    "RULE_CATALOG",
    "check_printable_part",
    "check_project_parameters",
    "check_target_envelope_within_build_volume",
    "check_working_envelope",
    "run_foundation_checks",
]


def __getattr__(name: str):
    """Load fastening checks lazily to keep the validation package acyclic."""

    if name in {
        "check_fastener_interface",
        "check_fastening_strategy",
        "check_phase3a_fastener_interfaces",
    }:
        from cad.fastening import (
            check_fastener_interface,
            check_fastening_strategy,
            check_phase3a_fastener_interfaces,
        )

        return {
            "check_fastener_interface": check_fastener_interface,
            "check_fastening_strategy": check_fastening_strategy,
            "check_phase3a_fastener_interfaces": check_phase3a_fastener_interfaces,
        }[name]
    raise AttributeError(name)
