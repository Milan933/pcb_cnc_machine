"""Dependency-light Phase 2 architecture trade-study data and calculations.

The matrix is an ordinal engineering screen, not a finite-element result. It
keeps the criteria, weights, force-loop assumptions, and sensitivity method in
Python so the review tables can be checked without a CAD backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ArchitectureId(str, Enum):
    """Architecture candidates compared with the same Phase 1 baseline."""

    A = "A"
    B = "B"
    C = "C"


@dataclass(frozen=True)
class ArchitectureCandidate:
    """Candidate identity and the PCB-specific reason it is credible."""

    candidate_id: ArchitectureId
    name: str
    benefit: str
    primary_risk: str


ARCHITECTURE_CANDIDATES: tuple[ArchitectureCandidate, ...] = (
    ArchitectureCandidate(
        ArchitectureId.A,
        "fixed gantry / moving Y bed",
        "A fixed gantry can make the Z/X support reaction compact and stiff.",
        "The moving PCB/spoilboard bed adds mass, guide-span alignment, and map/workholding motion.",
    ),
    ArchitectureCandidate(
        ArchitectureId.B,
        "moving gantry / fixed bed",
        "A fixed PCB datum simplifies workholding, conductive probing, height mapping, and service.",
        "The moving gantry must close pitch/yaw/roll loads through two PETG side interfaces.",
    ),
    ArchitectureCandidate(
        ArchitectureId.C,
        "fixed gantry / fixed bed with moving XY head",
        "It keeps the PCB datum fixed while exploring a non-moving-bed alternative.",
        "The elevated XY head adds guide interfaces and a longer, more joint-sensitive tool loop.",
    ),
)


@dataclass(frozen=True)
class ScoringCriterion:
    """One weighted ordinal criterion; score 1 is poor and 5 is favorable."""

    criterion_id: str
    label: str
    weight_percent: float
    rationale: str


SCORING_CRITERIA: tuple[ScoringCriterion, ...] = (
    ScoringCriterion("tool_point_stiffness", "predicted tool-point stiffness", 15.0, "The 0.020 mm target is the primary process constraint."),
    ScoringCriterion("z_stiffness", "Z stiffness", 12.0, "Isolation depth and drilling datum depend on a short, stable Z loop."),
    ScoringCriterion("gantry_torsion", "gantry torsional stiffness", 8.0, "Pitch, yaw, and roll error remain load-direction dependent."),
    ScoringCriterion("force_loop", "force-loop length", 10.0, "Shorter direct paths reduce bending leverage and PETG joint count."),
    ScoringCriterion("structural_joints", "structural joints", 4.0, "Distributed one-piece or monocoque load paths are preferred."),
    ScoringCriterion("petg_creep", "PETG creep", 4.0, "Long-term preload and datum drift are architecture risks."),
    ScoringCriterion("rail_alignment", "rail alignment", 5.0, "Printed rail seats and separated guide datums need alignment access."),
    ScoringCriterion("assembly", "assembly", 4.0, "The architecture must be alignable without hidden preload steps."),
    ScoringCriterion("service", "service", 5.0, "FR4 dust, probe, spindle, and spoilboard maintenance need access."),
    ScoringCriterion("voron_printability", "Voron printability", 8.0, "The frame must exploit the available 350 mm printer without extrusion geometry."),
    ScoringCriterion("large_prints", "large-print risk", 3.0, "Long parts increase warp, conditioning, and inspection risk."),
    ScoringCriterion("material", "material efficiency", 2.0, "Geometry, not arbitrary infill, should close the force loop."),
    ScoringCriterion("moving_mass", "moving mass", 5.0, "Mass affects guide preload, acceleration, vibration, and cable load."),
    ScoringCriterion("spindle_compatibility", "spindle compatibility", 3.0, "The mount remains an envelope until the spindle is selected."),
    ScoringCriterion("workholding", "workholding accessibility", 5.0, "PCB support and replacement must not disturb the machine datum."),
    ScoringCriterion("probing", "probing accessibility", 3.0, "Conductive probing and map coverage are required process interfaces."),
    ScoringCriterion("travel", "achievable travel", 3.0, "Travel must include edge, clamp, probe, and homing margins."),
    ScoringCriterion("footprint", "footprint", 1.0, "Desktop size matters after stiffness and process access are protected."),
)


# Scores are deliberately integer, ordinal judgments documented in the Phase
# 2 trade study. They are not measurements or simulated displacement values.
ARCHITECTURE_SCORES: dict[ArchitectureId, tuple[int, ...]] = {
    ArchitectureId.A: (4, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 3, 4, 3, 3, 4, 3),
    ArchitectureId.B: (4, 4, 3, 4, 4, 3, 4, 3, 4, 4, 4, 3, 3, 4, 5, 5, 4, 4),
    ArchitectureId.C: (2, 3, 4, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 5, 4, 3, 2),
}


@dataclass(frozen=True)
class ForceLoopAssessment:
    """Comparable force-loop screening inputs, not a structural solver."""

    candidate_id: ArchitectureId
    path_description: str
    nominal_loop_length_mm: float
    dominant_compliance: str
    cantilever_or_torsion_risk: str
    printed_joint_risk: str
    datum_and_probe_risk: str


FORCE_LOOP_ASSESSMENTS: tuple[ForceLoopAssessment, ...] = (
    ForceLoopAssessment(
        ArchitectureId.A,
        "tool -> spindle -> Z carriage -> fixed X gantry -> fixed side supports -> base -> Y bed rails -> moving bed/spoilboard -> PCB -> tool",
        360.0,
        "moving-bed rail/bed support and the fixed gantry-to-base joints",
        "fixed gantry is favorable; bed pitch and board support remain load-sensitive",
        "moderate: fixed gantry can be monocoque, but the moving bed needs distributed rail and screw interfaces",
        "the board moves with the bed; probe cable and map validity must survive motion",
    ),
    ForceLoopAssessment(
        ArchitectureId.B,
        "tool -> spindle -> Z carriage -> X carriage -> deep gantry beam -> two side guide interfaces -> Y rails/base -> fixed bed/spoilboard -> PCB -> tool",
        330.0,
        "gantry beam torsion and the two moving-gantry side joints",
        "the beam must resist roll and pitch while translating; guide spacing closes the side moment",
        "moderate: one-piece deep ribbed monocoque beam and distributed side interfaces are required",
        "fixed bed is favorable; probe stowage and map coverage can remain stationary",
    ),
    ForceLoopAssessment(
        ArchitectureId.C,
        "tool -> spindle -> Z carriage -> moving XY head -> elevated Y cross-slide -> fixed gantry -> base -> fixed bed/spoilboard -> PCB -> tool",
        470.0,
        "elevated XY head joints, carriage overhang, and the moving-head guide seats",
        "longer head stack creates pitch/yaw leverage even though the gantry itself is fixed",
        "high: more separated printed interfaces and alignment steps are needed",
        "fixed bed is favorable, but head access and probe cable clearance are constrained",
    ),
)


@dataclass(frozen=True)
class ZGuideCandidate:
    """Architecture-stage comparison of the requested Z guide arrangements."""

    name: str
    guide_count: int
    rail_family: str
    center_spacing_mm: float
    relative_moment_behavior: str
    printability: str
    disposition: str


Z_GUIDE_CANDIDATES: tuple[ZGuideCandidate, ...] = (
    ZGuideCandidate(
        "single rail / carriage",
        1,
        "MGN12 candidate",
        0.0,
        "one reaction line does not form a separated couple for the 50 mm tool overhang",
        "lowest part count and mass",
        "reject as the primary Z architecture; retain only as a small-load comparison",
    ),
    ZGuideCandidate(
        "dual rails / two carriages",
        2,
        "MGN9 candidate",
        60.0,
        "separated rails react pitch/yaw through a guide couple",
        "lower mass and easier envelope, but tighter rail-seat/alignment sensitivity",
        "retain as a lower-mass candidate pending stiffness and rail-seat evidence",
    ),
    ZGuideCandidate(
        "dual rails / two carriages",
        2,
        "MGN12 candidate",
        60.0,
        "same separated couple with more rail/carriage section and mounting area",
        "higher mass and width, but credible for the 0.020 mm tool-point target",
        "preferred interface candidate; exact rail class remains a Phase 3 decision",
    ),
)


@dataclass(frozen=True)
class LeadScrewArrangement:
    """Axis screw-line arrangement kept independent of lead selection."""

    axis: str
    proposed_line: str
    racking_control: str
    lead_candidates: tuple[str, ...]
    disposition: str


LEAD_SCREW_ARRANGEMENTS: tuple[LeadScrewArrangement, ...] = (
    LeadScrewArrangement(
        "X",
        "one screw centered between the two X guide centerlines",
        "centered drive minimizes carriage yaw; guide spacing reacts spindle moment",
        ("T8x2", "T8x4"),
        "interface only; choose lead from speed, torque, backlash, and motor data",
    ),
    LeadScrewArrangement(
        "Y",
        "one central screw between the two separated Y guide lines",
        "central drive avoids asymmetric gantry/bed racking; dual screws remain a risk response",
        ("T8x2", "T8x4"),
        "one centered line is the preliminary architecture; do not freeze lead or dual-drive policy",
    ),
    LeadScrewArrangement(
        "Z",
        "one screw on the spindle centerline between the dual Z guide lines",
        "central axial load path avoids twisting the carriage; end supports react screw loads",
        ("T8x2", "T8x4"),
        "centerline interface only; anti-backlash and bearing arrangement remain open",
    ),
)


def _weights(weights: Iterable[float] | None = None) -> tuple[float, ...]:
    result = tuple(
        criterion.weight_percent for criterion in SCORING_CRITERIA
    ) if weights is None else tuple(weights)
    if len(result) != len(SCORING_CRITERIA):
        raise ValueError("Architecture weights must match the criterion count.")
    if any(weight < 0 for weight in result) or not sum(result):
        raise ValueError("Architecture weights must be non-negative and non-zero.")
    return result


def weighted_score(
    candidate_id: ArchitectureId,
    weights: Iterable[float] | None = None,
) -> float:
    """Return a normalized 0-100 score from the ordinal matrix."""

    selected_weights = _weights(weights)
    scores = ARCHITECTURE_SCORES[candidate_id]
    return 100.0 * sum(
        weight * score / 5.0
        for weight, score in zip(selected_weights, scores)
    ) / sum(selected_weights)


def ranked_scores(weights: Iterable[float] | None = None) -> tuple[tuple[ArchitectureId, float], ...]:
    """Return candidates from highest to lowest normalized score."""

    return tuple(sorted(
        ((candidate_id, weighted_score(candidate_id, weights)) for candidate_id in ArchitectureId),
        key=lambda item: (-item[1], item[0].value),
    ))


SENSITIVITY_SCENARIOS: dict[str, tuple[int, ...]] = {
    "stiffness-led": (0, 1, 2, 3),
    "datum-and-probing-led": (14, 15),
    "printability-led": (4, 5, 9, 10, 11),
    "service-and-access-led": (6, 7, 8, 13, 16, 17),
}


def sensitivity_scores(
    scenario: str,
    factor: float = 2.0,
) -> tuple[tuple[ArchitectureId, float], ...]:
    """Double a named criterion group and renormalize to compare sensitivity."""

    if scenario not in SENSITIVITY_SCENARIOS:
        raise KeyError(f"Unknown architecture sensitivity scenario: {scenario}")
    if factor <= 0:
        raise ValueError("Sensitivity factor must be positive.")
    weights = list(_weights())
    for index in SENSITIVITY_SCENARIOS[scenario]:
        weights[index] *= factor
    return ranked_scores(weights)


def matrix_is_well_formed() -> bool:
    """Check dimensions and the documented 100-point base weight total."""

    return (
        len(SCORING_CRITERIA) == 18
        and abs(sum(item.weight_percent for item in SCORING_CRITERIA) - 100.0) < 1e-9
        and all(len(scores) == len(SCORING_CRITERIA) for scores in ARCHITECTURE_SCORES.values())
        and all(1 <= score <= 5 for scores in ARCHITECTURE_SCORES.values() for score in scores)
    )
