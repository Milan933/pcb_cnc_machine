"""Reproducible analytical Phase 2A comparison of architectures A and B.

This module intentionally uses equivalent-section beam and joint models rather
than an opaque FEA dependency. The values are screening assumptions and the
results are engineering estimates, not measured machine performance.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

from cad.architecture import ArchitectureId
from cad.parameters import PHASE2A_PARAMETERS, PHASE2_SKELETON_PARAMETERS, Phase2AParameters


@dataclass(frozen=True)
class DeflectionContribution:
    """One additive tool-point displacement contribution in millimetres."""

    name: str
    displacement_mm: float
    method: str


@dataclass(frozen=True)
class StructuralEstimate:
    """Analytical structural estimate for one optimized architecture."""

    candidate_id: ArchitectureId
    section_second_moment_mm4: float
    torsion_constant_mm4: float
    direct_stack_mm: float
    total_tool_point_displacement_mm: float
    contributions: tuple[DeflectionContribution, ...]

    @property
    def contribution_percentages(self) -> tuple[tuple[str, float], ...]:
        if self.total_tool_point_displacement_mm <= 0:
            return tuple((item.name, 0.0) for item in self.contributions)
        return tuple(
            (
                item.name,
                100.0 * item.displacement_mm / self.total_tool_point_displacement_mm,
            )
            for item in self.contributions
        )


@dataclass(frozen=True)
class MassBreakdown:
    candidate_id: ArchitectureId
    items_kg: tuple[tuple[str, float], ...]

    @property
    def total_kg(self) -> float:
        return sum(value for _, value in self.items_kg)


@dataclass(frozen=True)
class DynamicEstimate:
    candidate_id: ArchitectureId
    moving_mass_kg: float
    static_equivalent_stiffness_n_per_mm: float
    relative_resonance_index: float
    acceleration_force_n: float
    equivalent_friction_force_n: float
    cable_drag_force_n: float
    y_screw_design_force_n: float
    screw_torque_nm_by_lead: tuple[tuple[float, float], ...]
    qualitative_resonance_risk: str


@dataclass(frozen=True)
class RackingEstimate:
    candidate_id: ArchitectureId
    asymmetric_force_moment_nmm: float
    differential_guide_force_n: float
    estimated_edge_displacement_mm: float
    centered_screw_credible: bool
    assessment: str


@dataclass(frozen=True)
class ManufacturingEstimate:
    candidate_id: ArchitectureId
    printed_mass_kg: float
    print_hours_range: tuple[float, float]
    structural_print_count: int
    largest_print_mm: tuple[float, float, float]
    structural_joint_count: int
    heat_set_insert_count: int
    through_bolt_count: int
    rail_seat_count: int
    rail_seat_post_process: str


@dataclass(frozen=True)
class Phase2ACriterion:
    criterion_id: str
    label: str
    weight_percent: float
    rationale: str


PHASE2A_CRITERIA: tuple[Phase2ACriterion, ...] = (
    Phase2ACriterion("static_stiffness", "static tool-point stiffness", 18.0, "Uses the total analytical displacement, with target/acceptance distinction."),
    Phase2ACriterion("torsional_stiffness", "torsional stiffness", 10.0, "Scores the isolated closed-section torsion contribution only."),
    Phase2ACriterion("racking", "racking susceptibility", 8.0, "Scores asymmetric-force rotation and guide-couple sensitivity."),
    Phase2ACriterion("calibration_retention", "calibration retention", 18.0, "Separates stationary/moving PCB datum and preload drift."),
    Phase2ACriterion("moving_mass", "moving mass", 10.0, "Includes inertia and cyclic guide/screw loading; speed is secondary."),
    Phase2ACriterion("joint_count", "structural joint count", 8.0, "Counts major printed interfaces rather than every fastener."),
    Phase2ACriterion("petg_creep", "PETG creep sensitivity", 8.0, "Scores sustained preload and cyclic-load exposure."),
    Phase2ACriterion("manufacturing", "manufacturing complexity", 8.0, "Includes print count, large-part risk, inserts, bolts, and rail-seat work."),
    Phase2ACriterion("probing_workholding", "probing/workholding", 6.0, "Scores fixed datum, map validity, loading, and probe access."),
    Phase2ACriterion("serviceability", "serviceability", 4.0, "Scores cleaning, cable, spindle, rail, and spoilboard access."),
    Phase2ACriterion("footprint", "footprint", 2.0, "Small influence after stiffness and process access."),
)


# These scores use the revised Phase 2A evidence, not the original three-way
# screen. They are ordinal (1 poor, 5 favorable), with no separate bending
# criterion that would double-count the total static result.
PHASE2A_SCORES: dict[ArchitectureId, tuple[int, ...]] = {
    ArchitectureId.A: (5, 5, 4, 3, 5, 4, 4, 3, 2, 2, 3),
    ArchitectureId.B: (4, 4, 3, 5, 2, 3, 2, 4, 5, 5, 4),
}


PHASE2A_SENSITIVITY_GROUPS: dict[str, tuple[int, ...]] = {
    "structural-evidence-heavy": (0, 1, 2, 4, 5, 6),
    "calibration-and-usability-heavy": (3, 8, 9),
    "manufacturing-heavy": (4, 5, 6, 7),
    "moving-mass-heavy": (4,),
}


def second_moment_rectangle(width_mm: float, depth_mm: float) -> float:
    """Return the strong-axis second moment for an equivalent rectangle."""

    return width_mm * depth_mm**3 / 12.0


def closed_section_torsion_constant(
    width_mm: float,
    depth_mm: float,
    wall_mm: float,
) -> float:
    """Return a thin-wall closed-section torsion constant approximation."""

    if min(width_mm, depth_mm, wall_mm) <= 0 or 2.0 * wall_mm >= min(width_mm, depth_mm):
        raise ValueError("Closed-section dimensions are not physically ordered.")
    midline_width = width_mm - wall_mm
    midline_depth = depth_mm - wall_mm
    area = midline_width * midline_depth
    perimeter = 2.0 * (midline_width + midline_depth)
    return 4.0 * area**2 / (perimeter / wall_mm)


def simply_supported_center_deflection_mm(
    force_n: float,
    span_mm: float,
    modulus_n_per_mm2: float,
    second_moment_mm4: float,
) -> float:
    """Ideal central-load beam deflection."""

    return force_n * span_mm**3 / (48.0 * modulus_n_per_mm2 * second_moment_mm4)


def cantilever_deflection_mm(
    force_n: float,
    length_mm: float,
    modulus_n_per_mm2: float,
    second_moment_mm4: float,
) -> float:
    """Ideal cantilever tip deflection."""

    return force_n * length_mm**3 / (3.0 * modulus_n_per_mm2 * second_moment_mm4)


def closed_section_torsion_deflection_mm(
    torque_nmm: float,
    torsion_length_mm: float,
    shear_modulus_n_per_mm2: float,
    torsion_constant_mm4: float,
    tool_arm_mm: float,
) -> float:
    """Convert equivalent-section twist into tool-point displacement."""

    angle_rad = torque_nmm * torsion_length_mm / (
        shear_modulus_n_per_mm2 * torsion_constant_mm4
    )
    return angle_rad * tool_arm_mm


def joint_deflection_mm(force_n: float, effective_stiffness_n_per_mm: float) -> float:
    """Return force over equivalent joint stiffness."""

    return force_n / effective_stiffness_n_per_mm


def _parameters_for(candidate_id: ArchitectureId, parameters: Phase2AParameters) -> tuple[float, ...]:
    if candidate_id == ArchitectureId.A:
        return (
            parameters.a_section_width_mm,
            parameters.a_section_depth_mm,
            parameters.a_section_wall_mm,
            parameters.a_support_bending_length_mm,
            parameters.a_support_effective_second_moment_mm4,
            parameters.a_z_effective_stiffness_n_per_mm,
            parameters.a_joint_effective_stiffness_n_per_mm,
            parameters.a_racking_rotational_stiffness_nmm_per_rad,
        )
    if candidate_id == ArchitectureId.B:
        return (
            parameters.b_section_width_mm,
            parameters.b_section_depth_mm,
            parameters.b_section_wall_mm,
            parameters.b_support_bending_length_mm,
            parameters.b_support_effective_second_moment_mm4,
            parameters.b_z_effective_stiffness_n_per_mm,
            parameters.b_joint_effective_stiffness_n_per_mm,
            parameters.b_racking_rotational_stiffness_nmm_per_rad,
        )
    raise ValueError("Phase 2A only compares architecture A and B.")


def structural_estimate(
    candidate_id: ArchitectureId,
    parameters: Phase2AParameters = PHASE2A_PARAMETERS,
) -> StructuralEstimate:
    """Calculate additive direct and asymmetric-racking tool-point estimates."""

    (
        section_width,
        section_depth,
        wall,
        support_length,
        support_second_moment,
        z_stiffness,
        joint_stiffness,
        racking_stiffness,
    ) = _parameters_for(candidate_id, parameters)
    force = parameters.test_load_n
    modulus = parameters.effective_petg_modulus_n_per_mm2
    shear_modulus = modulus / (2.0 * (1.0 + parameters.effective_petg_poisson_ratio))
    second_moment = second_moment_rectangle(section_width, section_depth)
    torsion_constant = closed_section_torsion_constant(section_width, section_depth, wall)
    tool_torque = force * parameters.tool_point_overhang_mm

    contributions = (
        DeflectionContribution(
            "gantry bending",
            simply_supported_center_deflection_mm(
                force,
                PHASE2_SKELETON_PARAMETERS.gantry_clear_span_mm,
                modulus,
                second_moment,
            ),
            "5 N central-load simply-supported equivalent beam over 280 mm.",
        ),
        DeflectionContribution(
            "gantry torsion",
            closed_section_torsion_deflection_mm(
                tool_torque,
                parameters.torsion_half_span_mm,
                shear_modulus,
                torsion_constant,
                parameters.tool_point_overhang_mm,
            ),
            "Closed thin-wall equivalent section; not a shell/FEA result.",
        ),
        DeflectionContribution(
            "side/support bending",
            cantilever_deflection_mm(
                force / 2.0,
                support_length,
                modulus,
                support_second_moment,
            ),
            "Half-load cantilever equivalent for the support/interface pair.",
        ),
        DeflectionContribution(
            "Z carriage compliance",
            joint_deflection_mm(force, z_stiffness),
            "Equivalent dual-guide carriage stiffness assumption.",
        ),
        DeflectionContribution(
            "structural joints",
            joint_deflection_mm(force, joint_stiffness),
            "Equivalent PETG joint/rail-seat stiffness assumption.",
        ),
        DeflectionContribution(
            "asymmetric-force racking",
            parameters.test_load_n
            * parameters.racking_force_offset_mm
            / racking_stiffness
            * parameters.racking_tool_arm_mm,
            "Worst-edge 5 N moment; conservative addition to the direct stack.",
        ),
    )
    direct_stack = sum(item.displacement_mm for item in contributions[:-1])
    total = direct_stack + contributions[-1].displacement_mm
    return StructuralEstimate(
        candidate_id=candidate_id,
        section_second_moment_mm4=second_moment,
        torsion_constant_mm4=torsion_constant,
        direct_stack_mm=direct_stack,
        total_tool_point_displacement_mm=total,
        contributions=contributions,
    )


def mass_breakdown(
    candidate_id: ArchitectureId,
    parameters: Phase2AParameters = PHASE2A_PARAMETERS,
) -> MassBreakdown:
    """Return the nominal moving mass estimate for A or B."""

    if candidate_id == ArchitectureId.A:
        items = parameters.a_moving_mass_items_kg
    elif candidate_id == ArchitectureId.B:
        items = parameters.b_moving_mass_items_kg
    else:
        raise ValueError("Phase 2A only compares architecture A and B.")
    return MassBreakdown(candidate_id, items)


def printed_mass_breakdown(
    candidate_id: ArchitectureId,
    parameters: Phase2AParameters = PHASE2A_PARAMETERS,
) -> ManufacturingEstimate:
    """Return the nominal printed-mass and manufacturing screen."""

    if candidate_id == ArchitectureId.A:
        return ManufacturingEstimate(
            candidate_id,
            sum(value for _, value in parameters.a_printed_mass_items_kg),
            parameters.a_print_hours_range,
            parameters.a_structural_print_count,
            parameters.a_largest_print_mm,
            parameters.a_structural_joint_count,
            parameters.a_heat_set_insert_count,
            parameters.a_through_bolt_count,
            parameters.a_rail_seat_count,
            "Four continuous rail-seat datums; post-print skim/shim or replaceable metal seat required.",
        )
    if candidate_id == ArchitectureId.B:
        return ManufacturingEstimate(
            candidate_id,
            sum(value for _, value in parameters.b_printed_mass_items_kg),
            parameters.b_print_hours_range,
            parameters.b_structural_print_count,
            parameters.b_largest_print_mm,
            parameters.b_structural_joint_count,
            parameters.b_heat_set_insert_count,
            parameters.b_through_bolt_count,
            parameters.b_rail_seat_count,
            "Six separated rail/interface datums; each side requires post-print skim/shim or a metal load spreader.",
        )
    raise ValueError("Phase 2A only compares architecture A and B.")


def dynamic_estimate(
    candidate_id: ArchitectureId,
    parameters: Phase2AParameters = PHASE2A_PARAMETERS,
) -> DynamicEstimate:
    """Estimate low-acceleration Y force and screw torque implications."""

    mass = mass_breakdown(candidate_id, parameters).total_kg
    structural = structural_estimate(candidate_id, parameters)
    static_stiffness = parameters.test_load_n / structural.total_tool_point_displacement_mm
    resonance_index = math.sqrt(static_stiffness / mass)
    acceleration_force = mass * parameters.nominal_y_acceleration_m_per_s2
    friction_force = parameters.guide_friction_coefficient * parameters.test_load_n
    cable_drag = parameters.a_cable_drag_n if candidate_id == ArchitectureId.A else parameters.b_cable_drag_n
    design_force = acceleration_force + friction_force + cable_drag
    torque_by_lead = tuple(
        (
            lead,
            design_force * lead / (2.0 * math.pi * parameters.screw_efficiency) / 1000.0,
        )
        for lead in parameters.screw_leads_mm
    )
    resonance = (
        "Lower moving mass reduces inertial excitation; bed/PCB datum motion remains the process risk."
        if candidate_id == ArchitectureId.A
        else "Higher moving mass lowers the first-mode margin for equal stiffness and increases cyclic side-joint loading."
    )
    return DynamicEstimate(
        candidate_id,
        mass,
        static_stiffness,
        resonance_index,
        acceleration_force,
        friction_force,
        cable_drag,
        design_force,
        torque_by_lead,
        resonance,
    )


def racking_estimate(
    candidate_id: ArchitectureId,
    parameters: Phase2AParameters = PHASE2A_PARAMETERS,
) -> RackingEstimate:
    """Estimate asymmetric guide reaction and edge rotation."""

    if candidate_id == ArchitectureId.A:
        stiffness = parameters.a_racking_rotational_stiffness_nmm_per_rad
    elif candidate_id == ArchitectureId.B:
        stiffness = parameters.b_racking_rotational_stiffness_nmm_per_rad
    else:
        raise ValueError("Phase 2A only compares architecture A and B.")
    moment = parameters.test_load_n * parameters.racking_force_offset_mm
    differential_force = moment / parameters.y_guide_spacing_mm
    displacement = moment / stiffness * parameters.racking_tool_arm_mm
    return RackingEstimate(
        candidate_id,
        moment,
        differential_force,
        displacement,
        True,
        "A centered Y screw is credible at the low PCB acceleration target only with symmetric, preloaded guides; B additionally needs stiff side interfaces and a racking test.",
    )


def _weights(weights: Iterable[float] | None = None) -> tuple[float, ...]:
    result = tuple(item.weight_percent for item in PHASE2A_CRITERIA) if weights is None else tuple(weights)
    if len(result) != len(PHASE2A_CRITERIA) or any(value < 0 for value in result) or not sum(result):
        raise ValueError("Phase 2A weights must be non-negative and match the criteria.")
    return result


def phase2a_score(
    candidate_id: ArchitectureId,
    weights: Iterable[float] | None = None,
) -> float:
    """Return normalized 0-100 A/B score."""

    if candidate_id not in PHASE2A_SCORES:
        raise ValueError("Phase 2A scoring contains only A and B.")
    selected = _weights(weights)
    return 100.0 * sum(
        weight * score / 5.0
        for weight, score in zip(selected, PHASE2A_SCORES[candidate_id])
    ) / sum(selected)


def phase2a_ranking(weights: Iterable[float] | None = None) -> tuple[tuple[ArchitectureId, float], ...]:
    return tuple(sorted(
        ((candidate, phase2a_score(candidate, weights)) for candidate in (ArchitectureId.A, ArchitectureId.B)),
        key=lambda item: (-item[1], item[0].value),
    ))


def phase2a_sensitivity(
    scenario: str,
    factor: float = 2.0,
) -> tuple[tuple[ArchitectureId, float], ...]:
    """Double one criterion group and renormalize the revised matrix."""

    if scenario not in PHASE2A_SENSITIVITY_GROUPS:
        raise KeyError(f"Unknown Phase 2A sensitivity scenario: {scenario}")
    if factor <= 0:
        raise ValueError("Sensitivity factor must be positive.")
    weights = list(_weights())
    for index in PHASE2A_SENSITIVITY_GROUPS[scenario]:
        weights[index] *= factor
    return phase2a_ranking(weights)


def phase2a_is_well_formed() -> bool:
    return (
        len(PHASE2A_CRITERIA) == 11
        and abs(sum(item.weight_percent for item in PHASE2A_CRITERIA) - 100.0) < 1e-9
        and all(len(scores) == len(PHASE2A_CRITERIA) for scores in PHASE2A_SCORES.values())
        and all(1 <= score <= 5 for scores in PHASE2A_SCORES.values() for score in scores)
    )
