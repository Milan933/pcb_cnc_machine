"""Run the reproducible Phase 2A A-versus-B structural study."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from cad.architecture import ArchitectureId
from cad.assembly.architecture_skeleton import (
    build_skeleton,
    export_skeleton,
    find_interferences,
    unexpected_interferences,
)
from cad.parameters import PHASE2A_PARAMETERS
from cad.phase2a import (
    dynamic_estimate,
    mass_breakdown,
    phase2a_ranking,
    phase2a_sensitivity,
    printed_mass_breakdown,
    racking_estimate,
    structural_estimate,
)
from cad.validation import check_phase2_skeleton_parameters, check_phase2a_parameters


def _structural_result(candidate_id: ArchitectureId) -> dict[str, object]:
    result = structural_estimate(candidate_id)
    return {
        "direct_stack_mm": result.direct_stack_mm,
        "total_tool_point_displacement_mm": result.total_tool_point_displacement_mm,
        "target_status": "pass" if result.total_tool_point_displacement_mm <= PHASE2A_PARAMETERS.tool_point_deflection_target_mm else "fail",
        "prototype_acceptance_status": "pass" if result.total_tool_point_displacement_mm <= PHASE2A_PARAMETERS.tool_point_deflection_acceptance_mm else "fail",
        "section_second_moment_mm4": result.section_second_moment_mm4,
        "torsion_constant_mm4": result.torsion_constant_mm4,
        "contributions": [
            {
                "name": item.name,
                "displacement_mm": item.displacement_mm,
                "percentage": percentage,
                "method": item.method,
            }
            for item, (_, percentage) in zip(result.contributions, result.contribution_percentages)
        ],
    }


def _dynamic_result(candidate_id: ArchitectureId) -> dict[str, object]:
    result = dynamic_estimate(candidate_id)
    return {
        "moving_mass_kg": result.moving_mass_kg,
        "static_equivalent_stiffness_n_per_mm": result.static_equivalent_stiffness_n_per_mm,
        "relative_resonance_index": result.relative_resonance_index,
        "acceleration_force_n": result.acceleration_force_n,
        "equivalent_friction_force_n": result.equivalent_friction_force_n,
        "cable_drag_force_n": result.cable_drag_force_n,
        "y_screw_design_force_n": result.y_screw_design_force_n,
        "screw_torque_nm_by_lead": [list(item) for item in result.screw_torque_nm_by_lead],
        "qualitative_resonance_risk": result.qualitative_resonance_risk,
    }


def _manufacturing_result(candidate_id: ArchitectureId) -> dict[str, object]:
    result = printed_mass_breakdown(candidate_id)
    return {
        "printed_mass_kg": result.printed_mass_kg,
        "print_hours_range": list(result.print_hours_range),
        "structural_print_count": result.structural_print_count,
        "largest_print_mm": list(result.largest_print_mm),
        "structural_joint_count": result.structural_joint_count,
        "heat_set_insert_count": result.heat_set_insert_count,
        "through_bolt_count": result.through_bolt_count,
        "rail_seat_count": result.rail_seat_count,
        "rail_seat_post_process": result.rail_seat_post_process,
    }


def run(output_dir: Path) -> dict[str, object]:
    """Build optimized A/B skeletons and return all Phase 2A evidence."""

    import build123d

    parameter_report = check_phase2_skeleton_parameters()
    phase2a_parameter_report = check_phase2a_parameters()
    candidates: dict[str, object] = {}
    expected_bbox = {
        "min": (-170.0, -145.0, -40.0),
        "max": (170.0, 145.0, 180.0),
        "size": (340.0, 290.0, 220.0),
    }
    for candidate_id in (ArchitectureId.A, ArchitectureId.B):
        model = build_skeleton(candidate_id, structural_variant="phase2a")
        exports = export_skeleton(model, output_dir)
        interferences = find_interferences(model)
        bbox = model.bounding_box_mm
        candidates[candidate_id.value] = {
            "component_count": len(model.components),
            "bbox_mm": bbox,
            "bbox_screen_pass": bbox == expected_bbox,
            "expected_interferences": len([item for item in interferences if item["expected"]]),
            "unexpected_interferences": unexpected_interferences(model),
            "exports": {name: str(path) for name, path in exports.items()},
            "export_sizes_bytes": {name: path.stat().st_size for name, path in exports.items()},
            "exports_non_empty": all(path.stat().st_size > 0 for path in exports.values()),
            "structural": _structural_result(candidate_id),
            "mass": {
                "items_kg": [list(item) for item in mass_breakdown(candidate_id).items_kg],
                "total_kg": mass_breakdown(candidate_id).total_kg,
            },
            "dynamic": _dynamic_result(candidate_id),
            "racking": {
                "asymmetric_force_moment_nmm": racking_estimate(candidate_id).asymmetric_force_moment_nmm,
                "differential_guide_force_n": racking_estimate(candidate_id).differential_guide_force_n,
                "estimated_edge_displacement_mm": racking_estimate(candidate_id).estimated_edge_displacement_mm,
                "centered_screw_credible": racking_estimate(candidate_id).centered_screw_credible,
                "assessment": racking_estimate(candidate_id).assessment,
            },
            "manufacturing": _manufacturing_result(candidate_id),
        }

    return {
        "build123d_version": getattr(build123d, "__version__", "unknown"),
        "units": "mm",
        "parameter_validation_status": parameter_report.status.value,
        "parameter_validation_blocking": len(parameter_report.blocking_issues),
        "phase2a_parameter_validation_status": phase2a_parameter_report.status.value,
        "phase2a_parameter_validation_blocking": len(phase2a_parameter_report.blocking_issues),
        "output_dir": str(output_dir),
        "candidates": candidates,
        "revised_scores": {candidate.value: score for candidate, score in phase2a_ranking()},
        "sensitivity": {
            scenario: {candidate.value: score for candidate, score in phase2a_sensitivity(scenario)}
            for scenario in ("structural-evidence-heavy", "calibration-and-usability-heavy", "manufacturing-heavy", "moving-mass-heavy")
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="explicit temporary output directory; defaults to a system temp folder",
    )
    args = parser.parse_args()
    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="pcbCNC-phase2a-study-"))
    result = run(output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["parameter_validation_blocking"] or result["phase2a_parameter_validation_blocking"]:
        return 1
    if any(
        candidate["unexpected_interferences"]
        or not candidate["bbox_screen_pass"]
        or not candidate["exports_non_empty"]
        for candidate in result["candidates"].values()
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
