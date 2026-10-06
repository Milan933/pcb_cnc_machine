"""Preliminary before/after structural screens for Phase 4A.

The model intentionally keeps geometry-derived beam terms separate from
assumed interface stiffness allowances.  It is not FEA and does not claim
measured PETG behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS as P
from cad.phase2a import (
    cantilever_deflection_mm,
    closed_section_torsion_constant,
    closed_section_torsion_deflection_mm,
    simply_supported_center_deflection_mm,
)
from cad.phase4_calculations import hollow_section_second_moment_mm4


@dataclass(frozen=True)
class Phase4AContribution:
    name: str
    displacement_mm: float
    method: str
    category: str


@dataclass(frozen=True)
class Phase4AStructuralEstimate:
    variant_id: str
    test_load_n: float
    effective_petg_modulus_n_per_mm2: float
    beam_second_moment_mm4: float
    beam_torsion_constant_mm4: float
    direct_stack_mm: float
    racking_mm: float
    total_tool_point_deflection_mm: float
    target_mm: float
    preferred_target_mm: float
    acceptance_mm: float
    target_passes: bool
    preferred_target_passes: bool
    acceptance_passes: bool
    dominant_contribution: str
    contributions: tuple[Phase4AContribution, ...]
    evidence_status: str


# These are controlled optimization screens.  The beam terms use the changed
# equivalent wall and the remaining values are explicit joint/interface
# allowances to be replaced by coupons and physical tests.
_VARIANT_INPUTS = {
    "O1": {
        "beam_wall_mm": 6.0,
        "tower_i_mm4": 500_000.0,
        "joint_stiffness_n_per_mm": 2_300.0,
        "xz_stiffness_n_per_mm": 2_100.0,
        "base_stiffness_n_per_mm": 3_300.0,
        "rail_stiffness_n_per_mm": 2_800.0,
        "bed_stiffness_n_per_mm": 4_200.0,
        "racking_stiffness_nmm_per_rad": 32_000_000.0,
    },
    "O2": {
        "beam_wall_mm": 5.0,
        "tower_i_mm4": 600_000.0,
        "joint_stiffness_n_per_mm": 3_200.0,
        "xz_stiffness_n_per_mm": 2_700.0,
        "base_stiffness_n_per_mm": 4_400.0,
        "rail_stiffness_n_per_mm": 3_200.0,
        "bed_stiffness_n_per_mm": 4_500.0,
        "racking_stiffness_nmm_per_rad": 36_000_000.0,
    },
    "O3": {
        "beam_wall_mm": 5.0,
        "tower_i_mm4": 700_000.0,
        "joint_stiffness_n_per_mm": 4_200.0,
        "xz_stiffness_n_per_mm": 3_000.0,
        "base_stiffness_n_per_mm": 5_200.0,
        "rail_stiffness_n_per_mm": 3_500.0,
        "bed_stiffness_n_per_mm": 4_600.0,
        "racking_stiffness_nmm_per_rad": 40_000_000.0,
    },
}


def phase4a_structural_estimate(variant_id: str = "O2") -> Phase4AStructuralEstimate:
    """Calculate the preliminary 5 N screen for one optimization level."""

    if variant_id not in _VARIANT_INPUTS:
        raise ValueError(f"Unknown Phase 4A variant: {variant_id}")
    inputs = _VARIANT_INPUTS[variant_id]
    width, height, _ = P.gantry_beam_section_mm
    wall = inputs["beam_wall_mm"]
    beam_i = hollow_section_second_moment_mm4(width, height, wall)
    beam_j = closed_section_torsion_constant(width, height, wall)
    modulus = P.effective_petg_modulus_n_per_mm2
    shear_modulus = modulus / (2.0 * (1.0 + P.effective_petg_poisson_ratio))
    force = P.test_load_n
    tool_arm = P.tool_point_overhang_mm
    tool_torque = force * tool_arm

    contributions = (
        Phase4AContribution(
            "gantry beam bending",
            simply_supported_center_deflection_mm(force, P.gantry_clear_span_mm, modulus, beam_i),
            f"Geometry-derived equivalent closed section over {P.gantry_clear_span_mm:g} mm; wall screen {wall:g} mm.",
            "geometry-derived estimate",
        ),
        Phase4AContribution(
            "gantry beam torsion",
            closed_section_torsion_deflection_mm(
                tool_torque,
                P.gantry_clear_span_mm / 2.0,
                shear_modulus,
                beam_j,
                tool_arm,
            ),
            f"Geometry-derived thin-wall twist screen; wall screen {wall:g} mm.",
            "geometry-derived estimate",
        ),
        Phase4AContribution(
            "tower compliance",
            cantilever_deflection_mm(force / 2.0, P.tower_support_length_mm, modulus, inputs["tower_i_mm4"]),
            f"Equivalent tower second moment {inputs['tower_i_mm4']:g} mm4; integrated shoulder is not measured.",
            "assumed allowance",
        ),
        Phase4AContribution(
            "gantry joints",
            force / inputs["joint_stiffness_n_per_mm"],
            f"Equivalent remaining J1/interface stiffness {inputs['joint_stiffness_n_per_mm']:g} N/mm; coupon required.",
            "assumed allowance",
        ),
        Phase4AContribution(
            "X/Z structure",
            force / inputs["xz_stiffness_n_per_mm"],
            f"Equivalent coherent X/Z backbone stiffness {inputs['xz_stiffness_n_per_mm']:g} N/mm; no physical measurement.",
            "assumed allowance",
        ),
        Phase4AContribution(
            "base",
            force / inputs["base_stiffness_n_per_mm"],
            f"Equivalent integrated base/member stiffness {inputs['base_stiffness_n_per_mm']:g} N/mm; rail datum excluded here.",
            "assumed allowance",
        ),
        Phase4AContribution(
            "rail/interface allowance",
            force / inputs["rail_stiffness_n_per_mm"],
            f"Equivalent measured-by-future rail-seat/shim/fastener allowance {inputs['rail_stiffness_n_per_mm']:g} N/mm.",
            "assumed allowance",
        ),
        Phase4AContribution(
            "Y bed",
            force / inputs["bed_stiffness_n_per_mm"],
            f"Equivalent ribbed bed stiffness {inputs['bed_stiffness_n_per_mm']:g} N/mm; support plate remains material-dependent.",
            "assumed allowance",
        ),
    )
    direct_stack = sum(item.displacement_mm for item in contributions)
    racking = force * 100.0 / inputs["racking_stiffness_nmm_per_rad"] * tool_arm
    racking_item = Phase4AContribution(
        "other: asymmetric-force racking",
        racking,
        f"5 N at 100 mm lateral offset and assumed rotational stiffness {inputs['racking_stiffness_nmm_per_rad']:g} Nmm/rad.",
        "assumed allowance",
    )
    all_contributions = contributions + (racking_item,)
    total = direct_stack + racking
    dominant = max(all_contributions, key=lambda item: item.displacement_mm).name
    return Phase4AStructuralEstimate(
        variant_id=variant_id,
        test_load_n=force,
        effective_petg_modulus_n_per_mm2=modulus,
        beam_second_moment_mm4=beam_i,
        beam_torsion_constant_mm4=beam_j,
        direct_stack_mm=direct_stack,
        racking_mm=racking,
        total_tool_point_deflection_mm=total,
        target_mm=0.020,
        preferred_target_mm=0.015,
        acceptance_mm=0.030,
        target_passes=total <= 0.020,
        preferred_target_passes=total <= 0.015,
        acceptance_passes=total <= 0.030,
        dominant_contribution=dominant,
        contributions=all_contributions,
        evidence_status="preliminary equivalent-section screen; not FEA and not experimentally verified",
    )


def phase4a_variant_inputs() -> dict[str, dict[str, float]]:
    """Return a copy-safe view of the controlled optimization screen inputs."""

    return {variant: dict(values) for variant, values in _VARIANT_INPUTS.items()}


__all__ = [
    "Phase4AContribution",
    "Phase4AStructuralEstimate",
    "phase4a_structural_estimate",
    "phase4a_variant_inputs",
]
