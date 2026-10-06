"""Preliminary Phase 4 structural calculations for the accepted P2 concept.

This is an auditable equivalent-section screen tied to the Phase 4 central
geometry parameters. It is not FEA, a strength calculation, or measured PETG
performance. Physical force-loop and coupon evidence remain required.
"""

from __future__ import annotations

from dataclasses import dataclass

from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS, Phase4StructuralParameters

from .phase2a import (
    cantilever_deflection_mm,
    closed_section_torsion_constant,
    closed_section_torsion_deflection_mm,
    simply_supported_center_deflection_mm,
)


@dataclass(frozen=True)
class Phase4DeflectionContribution:
    """One preliminary tool-point deflection contribution in millimetres."""

    name: str
    displacement_mm: float
    method: str


@dataclass(frozen=True)
class Phase4StructuralEstimate:
    """Calculated Phase 4 force-loop screen and target comparison."""

    test_load_n: float
    effective_petg_modulus_n_per_mm2: float
    beam_second_moment_mm4: float
    beam_torsion_constant_mm4: float
    direct_stack_mm: float
    racking_mm: float
    total_tool_point_deflection_mm: float
    target_mm: float
    acceptance_mm: float
    target_passes: bool
    acceptance_passes: bool
    dominant_contribution: str
    contributions: tuple[Phase4DeflectionContribution, ...]
    evidence_status: str


def hollow_section_second_moment_mm4(
    width_mm: float,
    height_mm: float,
    wall_mm: float,
) -> float:
    """Return the strong-axis second moment of a rectangular closed section."""

    if min(width_mm, height_mm, wall_mm) <= 0 or 2.0 * wall_mm >= min(width_mm, height_mm):
        raise ValueError("Closed-section dimensions are not physically ordered.")
    return (
        width_mm * height_mm**3
        - (width_mm - 2.0 * wall_mm) * (height_mm - 2.0 * wall_mm) ** 3
    ) / 12.0


def phase4_structural_estimate(
    parameters: Phase4StructuralParameters = PHASE4_STRUCTURAL_PARAMETERS,
) -> Phase4StructuralEstimate:
    """Calculate the preliminary 5 N screen from the actual concept inputs."""

    width, height, wall = parameters.gantry_beam_section_mm
    beam_i = hollow_section_second_moment_mm4(width, height, wall)
    beam_j = closed_section_torsion_constant(width, height, wall)
    modulus = parameters.effective_petg_modulus_n_per_mm2
    shear_modulus = modulus / (2.0 * (1.0 + parameters.effective_petg_poisson_ratio))
    force = parameters.test_load_n
    tool_arm = parameters.tool_point_overhang_mm
    tool_torque = force * tool_arm

    contributions = (
        Phase4DeflectionContribution(
            "gantry beam bending",
            simply_supported_center_deflection_mm(
                force,
                parameters.gantry_clear_span_mm,
                modulus,
                beam_i,
            ),
            "Closed-section equivalent over the 280 mm P2 clear span.",
        ),
        Phase4DeflectionContribution(
            "gantry beam torsion",
            closed_section_torsion_deflection_mm(
                tool_torque,
                parameters.gantry_clear_span_mm / 2.0,
                shear_modulus,
                beam_j,
                tool_arm,
            ),
            "Thin-wall closed-section twist over the half-span; no FEA claim.",
        ),
        Phase4DeflectionContribution(
            "gantry tower bending",
            cantilever_deflection_mm(
                force / 2.0,
                parameters.tower_support_length_mm,
                modulus,
                parameters.tower_effective_second_moment_mm4,
            ),
            "Two tower reactions using the preliminary closed-tower effective I.",
        ),
        Phase4DeflectionContribution(
            "gantry joint",
            force / parameters.gantry_joint_stiffness_n_per_mm,
            "Equivalent J1 tongue/socket interface stiffness; coupon required.",
        ),
        Phase4DeflectionContribution(
            "X/Z structure",
            force / parameters.xz_structure_stiffness_n_per_mm,
            "Equivalent moving X carriage, Z plate, guide, and spindle interface stiffness.",
        ),
        Phase4DeflectionContribution(
            "base",
            force / parameters.base_stiffness_n_per_mm,
            "Equivalent closed base and tower-foot stiffness; rail datum excluded here.",
        ),
        Phase4DeflectionContribution(
            "rail-seat/interface allowance",
            force / parameters.rail_seat_stiffness_n_per_mm,
            "Equivalent PETG rail-seat, shim, fastener, and datum compliance allowance.",
        ),
        Phase4DeflectionContribution(
            "moving-bed support",
            force / parameters.moving_bed_stiffness_n_per_mm,
            "Equivalent ribbed bed/support compliance at the PCB datum.",
        ),
    )
    direct_stack = sum(item.displacement_mm for item in contributions)
    racking = (
        force
        * 100.0
        / parameters.racking_rotational_stiffness_nmm_per_rad
        * tool_arm
    )
    total = direct_stack + racking
    dominant = max(contributions, key=lambda item: item.displacement_mm).name
    return Phase4StructuralEstimate(
        test_load_n=force,
        effective_petg_modulus_n_per_mm2=modulus,
        beam_second_moment_mm4=beam_i,
        beam_torsion_constant_mm4=beam_j,
        direct_stack_mm=direct_stack,
        racking_mm=racking,
        total_tool_point_deflection_mm=total,
        target_mm=0.020,
        acceptance_mm=0.030,
        target_passes=total <= 0.020,
        acceptance_passes=total <= 0.030,
        dominant_contribution=dominant,
        contributions=contributions
        + (
            Phase4DeflectionContribution(
                "asymmetric-force racking",
                racking,
                "5 N force at a 100 mm lateral offset with preliminary rotational stiffness.",
            ),
        ),
        evidence_status="calculated preliminary screen; not experimentally verified",
    )


def estimated_petg_mass_kg(component_volumes_mm3: tuple[float, ...], density_kg_per_mm3: float = PHASE4_STRUCTURAL_PARAMETERS.petg_density_kg_per_mm3) -> float:
    """Convert measured review-solid volumes to a nominal PETG mass estimate."""

    if density_kg_per_mm3 <= 0 or any(volume < 0 for volume in component_volumes_mm3):
        raise ValueError("Component volumes and PETG density must be non-negative/positive.")
    return sum(component_volumes_mm3) * density_kg_per_mm3
