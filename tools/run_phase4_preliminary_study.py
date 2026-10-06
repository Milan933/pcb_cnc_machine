"""Run the Phase 4 preliminary structural CAD and validation study."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import tempfile
from typing import Any

from cad.assembly.phase4_assembly import (
    build_gantry_joint_study,
    build_phase4_assembly,
    export_gantry_joint_study,
    export_phase4_review_geometry,
    phase4_model_interferences,
)
from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS
from cad.phase4_calculations import estimated_petg_mass_kg, phase4_structural_estimate
from cad.validation import (
    check_phase4_assembly,
    check_phase4_structural_parameters,
    phase4_gate_report,
)
from cad.assembly.architecture_skeleton import find_interferences


def _issue_report(report: Any) -> dict[str, Any]:
    return {
        "status": report.status.value,
        "blocking": len(report.blocking_issues),
        "issues": [
            {
                "rule_id": issue.rule_id,
                "status": issue.status.value,
                "severity": issue.severity.value,
                "message": issue.message,
                "component": issue.component,
                "evidence": issue.evidence,
            }
            for issue in report.issues
        ],
    }


def _bbox(shape: Any) -> dict[str, tuple[float, float, float]]:
    bounding_box = shape.bounding_box()

    def vector_tuple(vector: Any) -> tuple[float, float, float]:
        return tuple(float(getattr(vector, axis)) for axis in ("X", "Y", "Z"))

    return {
        "min": vector_tuple(bounding_box.min),
        "max": vector_tuple(bounding_box.max),
        "size": vector_tuple(bounding_box.size),
    }


def _actual_part_report(model: Any) -> tuple[list[dict[str, Any]], float]:
    parameter_by_id = {part.part_id: part for part in PHASE4_STRUCTURAL_PARAMETERS.print_parts}
    rows: list[dict[str, Any]] = []
    volumes: list[float] = []
    for component in model.structural_parts:
        bbox = _bbox(component.shape)
        volume = float(component.shape.volume)
        volumes.append(volume)
        parameter = parameter_by_id[component.name]
        rows.append(
            {
                "part_id": component.name,
                "title": parameter.title,
                "role": parameter.role,
                "status": parameter.status.value,
                "mandatory": parameter.mandatory,
                "nominal_bbox_mm": list(parameter.nominal_bbox_mm),
                "actual_bbox_mm": bbox,
                "print_orientation": parameter.print_orientation,
                "print_orientation_extents_mm": list(parameter.print_orientation_extents_mm),
                "support_requirement": parameter.support_requirement,
                "brim_requirement": parameter.brim_requirement,
                "warping_risk": parameter.warping_risk,
                "layer_load_concern": parameter.layer_load_concern,
                "volume_mm3": volume,
            }
        )
    rows.sort(key=lambda row: row["part_id"])
    return rows, estimated_petg_mass_kg(tuple(volumes))


def run(output_dir: Path) -> dict[str, Any]:
    """Generate preliminary review exports and a machine-readable gate report."""

    output_dir.mkdir(parents=True, exist_ok=True)
    parameter_report = check_phase4_structural_parameters()
    model = build_phase4_assembly()
    assembly_report = check_phase4_assembly(model)
    gate_report = phase4_gate_report()
    joint_model = build_gantry_joint_study()

    exports = export_phase4_review_geometry(model, output_dir)
    exports.update(export_gantry_joint_study(joint_model, output_dir))
    part_rows, mass_kg = _actual_part_report(model)
    estimate = phase4_structural_estimate()
    all_interferences = find_interferences(model)
    unexpected = phase4_model_interferences(model)
    largest = max(
        part_rows,
        key=lambda row: max(row["actual_bbox_mm"]["size"][:2]),
    )

    exports_report = {
        name: str(path)
        for name, path in sorted(exports.items())
    }
    exports_sizes = {
        name: path.stat().st_size
        for name, path in sorted(exports.items())
    }
    exports_non_empty = all(size > 0 for size in exports_sizes.values())
    joint_non_empty = all(
        path.stat().st_size > 0
        for name, path in exports.items()
        if "joint_study" in name
    )

    return {
        "phase": "4-preliminary-structural-concept",
        "status": "proposed-owner-review",
        "units": "mm, N, kg unless noted",
        "reference_variant_id": PHASE4_STRUCTURAL_PARAMETERS.reference_variant_id,
        "owner_boundary": {
            "phase3_motion_baseline_accepted": True,
            "phase3a_p2_packaging_baseline_accepted": True,
            "phase4_preliminary_structural_concept_authorized": True,
            "phase4_accepted": False,
            "phase5_started": False,
            "production_release": False,
        },
        "parameter_validation": _issue_report(parameter_report),
        "assembly_validation": _issue_report(assembly_report),
        "gate_validation": _issue_report(gate_report),
        "structural_part_count": len(part_rows),
        "assembly_component_count": len(model.components),
        "assembly_bbox_mm": model.bounding_box_mm,
        "largest_printed_part": {
            "part_id": largest["part_id"],
            "actual_bbox_mm": largest["actual_bbox_mm"],
            "print_orientation": largest["print_orientation"],
            "print_orientation_extents_mm": largest["print_orientation_extents_mm"],
        },
        "printed_part_mass_estimate_kg": mass_kg,
        "printed_part_mass_basis": "nominal build123d review-solid volumes multiplied by the centralized PETG density; not a measured mass",
        "structural_calculation": {
            "test_load_n": estimate.test_load_n,
            "effective_petg_modulus_n_per_mm2": estimate.effective_petg_modulus_n_per_mm2,
            "beam_second_moment_mm4": estimate.beam_second_moment_mm4,
            "beam_torsion_constant_mm4": estimate.beam_torsion_constant_mm4,
            "direct_stack_mm": estimate.direct_stack_mm,
            "racking_mm": estimate.racking_mm,
            "total_tool_point_deflection_mm": estimate.total_tool_point_deflection_mm,
            "target_mm": estimate.target_mm,
            "acceptance_mm": estimate.acceptance_mm,
            "target_passes": estimate.target_passes,
            "acceptance_passes": estimate.acceptance_passes,
            "dominant_contribution": estimate.dominant_contribution,
            "evidence_status": estimate.evidence_status,
            "contributions": [asdict(item) for item in estimate.contributions],
        },
        "joint_concepts": [asdict(concept) for concept in PHASE4_STRUCTURAL_PARAMETERS.joint_concepts],
        "rail_seats": [asdict(seat) for seat in PHASE4_STRUCTURAL_PARAMETERS.rail_seats],
        "serviceable_components": list(PHASE4_STRUCTURAL_PARAMETERS.serviceable_components),
        "assembly_sequence": list(PHASE4_STRUCTURAL_PARAMETERS.assembly_sequence),
        "interferences": {
            "all": list(all_interferences),
            "unexpected": list(unexpected),
            "expected_count": sum(1 for item in all_interferences if item["expected"]),
        },
        "parts": part_rows,
        "exports": exports_report,
        "export_sizes_bytes": exports_sizes,
        "exports_non_empty": exports_non_empty,
        "joint_exports_non_empty": joint_non_empty,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="explicit temporary output directory; defaults to a system temp folder",
    )
    args = parser.parse_args()
    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="pcbCNC-phase4-structural-"))
    result = run(output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    if (
        result["parameter_validation"]["blocking"]
        or result["assembly_validation"]["blocking"]
        or result["interferences"]["unexpected"]
        or not result["exports_non_empty"]
        or not result["joint_exports_non_empty"]
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
