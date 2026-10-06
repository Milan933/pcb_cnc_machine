"""Run the proposed Phase 4A structural optimization comparison."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import asdict
import json
from pathlib import Path
import tempfile
from typing import Any, Iterable

from cad.assembly.architecture_skeleton import find_interferences
from cad.assembly.phase4_assembly import (
    build_gantry_joint_study,
    build_phase4_assembly,
    export_gantry_joint_study,
)
from cad.assembly.phase4a_assembly import (
    build_phase4a_assembly,
    export_phase4a_review_geometry,
)
from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS as P
from cad.phase4_calculations import estimated_petg_mass_kg, phase4_structural_estimate
from cad.phase4a_calculations import phase4a_structural_estimate
from cad.parts.phase4a_structural import (
    BASE_CLASSIFICATION,
    PHASE4A_VARIANTS,
    PRIMARY_LOOP_JOINT_COUNT_BY_VARIANT,
    SELECTED_PHASE4A_VARIANT,
    VARIANT_ORDER,
    build_phase4a_structural_parts,
    phase4a_part_records,
    phase4a_primary_loop_parts,
)
from cad.parts.phase4_structural import build_phase4_structural_parts
from cad.validation import (
    check_phase4a_assembly,
    check_phase4a_structural_parameters,
    phase4a_gate_report,
)


_BASELINE_PRIMARY_LOOP_PARTS = 17
_BASELINE_PRIMARY_LOOP_IDS = {
    "base_front_left",
    "base_front_right",
    "base_rear_left",
    "base_rear_right",
    "base_left_side_member",
    "base_right_side_member",
    "base_y_rail_carrier_left",
    "base_y_rail_carrier_right",
    "base_center_tie",
    "gantry_tower_left",
    "gantry_tower_right",
    "gantry_beam_left",
    "gantry_beam_right",
    "x_carriage_plate",
    "z_carriage_plate",
    "spindle_mount_concept",
    "moving_bed_frame",
}
_BASELINE_PHYSICAL_JOINT_GROUPS = 28
_BASELINE_AUTOMATED_OVERLAP_EVENTS = 34
_BUCKET_FACTORS = {
    "closed sections": (0.55, 0.75),
    "ribbed plates / bed / rail carriers": (0.50, 0.70),
    "local interfaces": (0.65, 0.85),
}


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


def _classification(part_id: str) -> str:
    if part_id in BASE_CLASSIFICATION:
        return BASE_CLASSIFICATION[part_id]
    if part_id in {
        "base_left_integrated",
        "base_right_integrated",
        "base_gantry_left",
        "base_gantry_right",
        "base_center_tie",
        "gantry_left_integrated",
        "gantry_right_integrated",
        "x_z_backbone",
        "z_carriage_plate",
        "moving_bed_frame",
    }:
        return "CRITICAL STRUCTURAL"
    if part_id == "spindle_mount_concept" or part_id.startswith("machine_foot"):
        return "MOUNT / INTERFACE"
    if part_id == "electronics_mount_rail":
        return "NON-STRUCTURAL"
    return "SECONDARY STRUCTURAL"


def _print_bucket(part_id: str) -> str:
    if part_id.startswith(("base_front", "base_rear", "base_side", "base_left_side", "base_right_side")):
        return "closed sections"
    if part_id in {
        "base_center_tie",
        "base_left_integrated",
        "base_right_integrated",
        "base_gantry_left",
        "base_gantry_right",
    }:
        return "closed sections"
    if part_id.startswith("gantry_") or part_id.startswith("gantry_tower") or part_id.startswith("gantry_beam"):
        return "closed sections"
    if part_id in {
        "base_y_rail_carrier_left",
        "base_y_rail_carrier_right",
        "x_carriage_plate",
        "x_z_backbone",
        "z_carriage_plate",
        "moving_bed_frame",
    }:
        return "ribbed plates / bed / rail carriers"
    return "local interfaces"


def _mass_buckets(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    volumes: dict[str, float] = defaultdict(float)
    for row in rows:
        volumes[_print_bucket(row["part_id"])] += row["volume_mm3"]
    result: dict[str, Any] = {}
    low_total = 0.0
    high_total = 0.0
    for bucket, (low_factor, high_factor) in _BUCKET_FACTORS.items():
        cad_mass = volumes[bucket] * P.petg_density_kg_per_mm3
        low_mass = cad_mass * low_factor
        high_mass = cad_mass * high_factor
        low_total += low_mass
        high_total += high_mass
        result[bucket] = {
            "cad_solid_equivalent_mass_kg": cad_mass,
            "planning_factor": f"{low_factor:.2f}-{high_factor:.2f}",
            "estimated_installed_petg_mass_kg": {
                "low": low_mass,
                "high": high_mass,
            },
        }
    result["total"] = {
        "cad_solid_equivalent_mass_kg": sum(
            item["cad_solid_equivalent_mass_kg"] for name, item in result.items() if name != "total"
        ),
        "estimated_installed_petg_mass_kg": {"low": low_total, "high": high_total},
        "basis": "Review-solid volume multiplied by PETG density and conceptual print-bucket factors; no slicer, hardware, support, or measured mass.",
    }
    return result


def _part_rows(
    components: tuple[Any, ...],
    records: tuple[Any, ...],
    *,
    baseline: bool = False,
) -> list[dict[str, Any]]:
    record_by_id = {record.part_id: record for record in records}
    rows: list[dict[str, Any]] = []
    for component in components:
        actual_bbox = _bbox(component.shape)
        record = record_by_id.get(component.name)
        if record is None and baseline:
            parameter = next(part for part in P.print_parts if part.part_id == component.name)
            row = {
                "part_id": component.name,
                "title": parameter.title,
                "role": parameter.role,
                "classification": _classification(component.name),
                "nominal_bbox_mm": list(parameter.nominal_bbox_mm),
                "actual_bbox_mm": actual_bbox,
                "print_orientation": parameter.print_orientation,
                "print_orientation_extents_mm": list(parameter.print_orientation_extents_mm),
                "support_requirement": parameter.support_requirement,
                "brim_requirement": parameter.brim_requirement,
                "warping_risk": parameter.warping_risk,
                "layer_load_concern": parameter.layer_load_concern,
                "direct_force_loop": component.name in _BASELINE_PRIMARY_LOOP_IDS,
            }
        elif record is not None:
            row = {
                "part_id": record.part_id,
                "title": record.title,
                "role": record.role,
                "classification": record.classification,
                "nominal_bbox_mm": list(record.nominal_bbox_mm),
                "actual_bbox_mm": actual_bbox,
                "print_orientation": record.print_orientation,
                "print_orientation_extents_mm": list(record.print_orientation_extents_mm),
                "support_requirement": record.support_requirement,
                "brim_requirement": record.brim_requirement,
                "warping_risk": record.warping_risk,
                "layer_load_concern": record.layer_load_concern,
                "direct_force_loop": record.direct_force_loop,
                "serviceable": record.serviceable,
                "status": record.status.value,
            }
        else:
            raise KeyError(f"No part record for {component.name}")
        row["volume_mm3"] = float(component.shape.volume)
        rows.append(row)
    return sorted(rows, key=lambda row: row["part_id"])


def _mass_and_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    class_mass: dict[str, float] = defaultdict(float)
    class_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        mass = row["volume_mm3"] * P.petg_density_kg_per_mm3
        class_mass[row["classification"]] += mass
        class_counts[row["classification"]] += 1
    return {
        "cad_solid_equivalent_mass_kg": sum(class_mass.values()),
        "class_mass_kg": dict(sorted(class_mass.items())),
        "class_counts": dict(sorted(class_counts.items())),
    }


def _largest_print(rows: list[dict[str, Any]]) -> dict[str, Any]:
    largest = max(rows, key=lambda row: max(row["actual_bbox_mm"]["size"][:2]))
    return {
        "part_id": largest["part_id"],
        "actual_bbox_mm": largest["actual_bbox_mm"],
        "print_orientation": largest["print_orientation"],
        "print_orientation_extents_mm": largest["print_orientation_extents_mm"],
    }


def _bed_mass(rows: list[dict[str, Any]]) -> dict[str, Any]:
    bed = next(row for row in rows if row["part_id"] == "moving_bed_frame")
    cad_mass = bed["volume_mm3"] * P.petg_density_kg_per_mm3
    return {
        "part_id": bed["part_id"],
        "cad_solid_equivalent_mass_kg": cad_mass,
        "estimated_installed_petg_mass_kg": {
            "low": cad_mass * 0.50,
            "high": cad_mass * 0.70,
        },
        "note": "Printed bed frame only; metal carriages, rails, screws, PCB support, spoilboard, and workholding are excluded.",
    }


def _calculation_report(estimate: Any) -> dict[str, Any]:
    total = estimate.total_tool_point_deflection_mm
    return {
        "test_load_n": estimate.test_load_n,
        "effective_petg_modulus_n_per_mm2": estimate.effective_petg_modulus_n_per_mm2,
        "beam_second_moment_mm4": estimate.beam_second_moment_mm4,
        "beam_torsion_constant_mm4": estimate.beam_torsion_constant_mm4,
        "direct_stack_mm": estimate.direct_stack_mm,
        "racking_mm": estimate.racking_mm,
        "total_tool_point_deflection_mm": total,
        "target_mm": estimate.target_mm,
        "preferred_target_mm": getattr(estimate, "preferred_target_mm", 0.015),
        "acceptance_mm": estimate.acceptance_mm,
        "target_passes": estimate.target_passes,
        "preferred_target_passes": getattr(estimate, "preferred_target_passes", False),
        "acceptance_passes": estimate.acceptance_passes,
        "dominant_contribution": estimate.dominant_contribution,
        "contributions": [asdict(item) for item in estimate.contributions],
        "contribution_percent_of_total": {
            item.name: item.displacement_mm / total * 100.0
            for item in estimate.contributions
            if total > 0
        },
        "evidence_status": estimate.evidence_status,
    }


def _baseline_snapshot() -> dict[str, Any]:
    model = build_phase4_assembly()
    components = tuple(model.structural_parts)
    records = tuple()
    rows = _part_rows(components, records, baseline=True)
    mass = _mass_and_counts(rows)
    overlaps = find_interferences(model)
    largest = _largest_print(rows)
    return {
        "variant_id": "Phase 4 baseline",
        "structural_part_count": len(rows),
        "critical_structural_part_count": mass["class_counts"].get("CRITICAL STRUCTURAL", 0),
        "primary_loop_part_count": _BASELINE_PRIMARY_LOOP_PARTS,
        "assembly_component_count": len(model.components),
        "assembly_bbox_mm": model.bounding_box_mm,
        "largest_printed_part": largest,
        "mass": mass,
        "printed_mass_estimate": _mass_buckets(rows),
        "bed_mass": _bed_mass(rows),
        "deflection": _calculation_report(phase4_structural_estimate()),
        "automated_expected_overlap_events": len(model.expected_interference_pairs),
        "actual_overlap_events": len(overlaps),
        "unexpected_interferences": [item for item in overlaps if not item["expected"]],
        "physical_joint_groups": _BASELINE_PHYSICAL_JOINT_GROUPS,
        "physical_joint_basis": "Phase 4 owner-review register; not a frozen hardware count.",
    }


def _variant_snapshot(variant_id: str) -> tuple[dict[str, Any], Any, tuple[Any, ...], tuple[Any, ...]]:
    components = build_phase4a_structural_parts(variant_id)
    records = phase4a_part_records(components, variant_id)
    model = build_phase4a_assembly(variant_id, components)
    rows = _part_rows(components, records)
    mass = _mass_and_counts(rows)
    overlaps = find_interferences(model)
    estimate = phase4a_structural_estimate(variant_id)
    largest = _largest_print(rows)
    parameter_report = check_phase4a_structural_parameters(variant_id, records)
    assembly_report = check_phase4a_assembly(model, variant_id, records, overlaps)
    snapshot = {
        "variant_id": variant_id,
        "title": next(item.title for item in PHASE4A_VARIANTS if item.variant_id == variant_id),
        "structural_part_count": len(rows),
        "critical_structural_part_count": mass["class_counts"].get("CRITICAL STRUCTURAL", 0),
        "primary_loop_part_count": len(phase4a_primary_loop_parts(variant_id)),
        "primary_loop_joint_count": PRIMARY_LOOP_JOINT_COUNT_BY_VARIANT[variant_id],
        "assembly_component_count": len(model.components),
        "assembly_bbox_mm": model.bounding_box_mm,
        "largest_printed_part": largest,
        "mass": mass,
        "printed_mass_estimate": _mass_buckets(rows),
        "bed_mass": _bed_mass(rows),
        "deflection": _calculation_report(estimate),
        "automated_expected_overlap_events": len(model.expected_interference_pairs),
        "actual_overlap_events": len(overlaps),
        "unexpected_interferences": [item for item in overlaps if not item["expected"]],
        "physical_joint_groups": None,
        "physical_joint_basis": "Not frozen; use the primary pair-level register and automated overlap graph until the integrated interfaces are physically reviewed.",
        "parameter_validation": _issue_report(parameter_report),
        "assembly_validation": _issue_report(assembly_report),
        "parts": rows,
    }
    return snapshot, model, records, components


def run(output_dir: Path) -> dict[str, Any]:
    """Generate the Phase 4A comparison, selected exports, and gate report."""

    output_dir.mkdir(parents=True, exist_ok=True)
    baseline = _baseline_snapshot()
    variants: dict[str, Any] = {}
    selected_model = None
    selected_records = None
    selected_snapshot = None
    for variant_id in VARIANT_ORDER:
        snapshot, model, records, _ = _variant_snapshot(variant_id)
        variants[variant_id] = snapshot
        if variant_id == SELECTED_PHASE4A_VARIANT:
            selected_model = model
            selected_records = records
            selected_snapshot = snapshot

    assert selected_model is not None
    assert selected_records is not None
    assert selected_snapshot is not None

    # OCCT intersection calls in build123d 0.12.0 can consume topology on a
    # compound child.  Rebuild the selected review model before export so the
    # tracked STEP/STL derivatives are generated from untouched topology.
    selected_model = build_phase4a_assembly(
        SELECTED_PHASE4A_VARIANT,
        build_phase4a_structural_parts(SELECTED_PHASE4A_VARIANT),
    )

    exports = export_phase4a_review_geometry(selected_model, output_dir)
    exports.update(export_gantry_joint_study(build_gantry_joint_study(), output_dir))
    export_sizes = {name: path.stat().st_size for name, path in sorted(exports.items())}

    selected_estimate = phase4a_structural_estimate(SELECTED_PHASE4A_VARIANT)
    gate = phase4a_gate_report()
    primary_joint_after = PRIMARY_LOOP_JOINT_COUNT_BY_VARIANT[SELECTED_PHASE4A_VARIANT]
    overlap_after = selected_snapshot["automated_expected_overlap_events"]
    return {
        "phase": "4A-structural-optimization",
        "status": "accepted-preliminary-architecture-hardware-freeze",
        "units": "mm, N, kg unless noted",
        "selected_variant": SELECTED_PHASE4A_VARIANT,
        "selection_reason": (
            "O2 is the balanced compromise: it removes the base perimeter and tower-to-beam PETG seams, retains replaceable motion and spindle hardware, "
            "keeps every print at or below the 300 mm preferred boundary, and passes the preferred 0.015 mm preliminary deflection target."
        ),
        "optimization_objective": {
            "primary_force_loop_simplification": True,
            "critical_petg_part_count_reduction": True,
            "critical_petg_joint_reduction": True,
            "stiffness_alignment_serviceability_printability_preserved_as_review_targets": True,
            "mass_is_secondary_to_load_path": True,
        },
        "owner_boundary": {
            "phase3_motion_baseline_accepted": True,
            "phase3a_p2_packaging_baseline_accepted": True,
            "phase4_preliminary_concept_authorized": True,
            "phase4_preliminary_architecture_baseline_accepted": True,
            "phase4a_preliminary_architecture_baseline_accepted": True,
            "phase4_manufacturing_ready": False,
            "phase5_started": False,
            "production_release": False,
        },
        "baseline": baseline,
        "variants": variants,
        "selected": selected_snapshot,
        "before_after": {
            "structural_part_count": {
                "before": baseline["structural_part_count"],
                "after": selected_snapshot["structural_part_count"],
                "removed": baseline["structural_part_count"] - selected_snapshot["structural_part_count"],
            },
            "critical_structural_part_count": {
                "before": baseline["critical_structural_part_count"],
                "after": selected_snapshot["critical_structural_part_count"],
                "removed": baseline["critical_structural_part_count"] - selected_snapshot["critical_structural_part_count"],
            },
            "primary_loop_part_count": {
                "before": baseline["primary_loop_part_count"],
                "after": selected_snapshot["primary_loop_part_count"],
                "removed": baseline["primary_loop_part_count"] - selected_snapshot["primary_loop_part_count"],
            },
            "primary_loop_joint_count": {
                "before": _BASELINE_PRIMARY_LOOP_PARTS,
                "after": primary_joint_after,
                "removed": _BASELINE_PRIMARY_LOOP_PARTS - primary_joint_after,
                "basis": "pair-level primary force-loop register; mirrored interfaces are separate",
            },
            "automated_expected_overlap_events": {
                "before": baseline["automated_expected_overlap_events"],
                "after": overlap_after,
                "removed": baseline["automated_expected_overlap_events"] - overlap_after,
                "basis": "build123d solid-overlap graph; not a frozen fastener or physical joint count",
            },
            "physical_joint_groups": {
                "before": baseline["physical_joint_groups"],
                "after": None,
                "basis": "The Phase 4A physical PETG-to-PETG register remains open until integrated-part access and hardware interfaces are reviewed; no invented purchase count is claimed.",
            },
            "cad_solid_equivalent_mass_kg": {
                "before": baseline["mass"]["cad_solid_equivalent_mass_kg"],
                "after": selected_snapshot["mass"]["cad_solid_equivalent_mass_kg"],
                "change": selected_snapshot["mass"]["cad_solid_equivalent_mass_kg"] - baseline["mass"]["cad_solid_equivalent_mass_kg"],
            },
            "estimated_installed_petg_mass_kg": {
                "before": baseline["printed_mass_estimate"]["total"]["estimated_installed_petg_mass_kg"],
                "after": selected_snapshot["printed_mass_estimate"]["total"]["estimated_installed_petg_mass_kg"],
            },
            "assembly_bbox_mm": {
                "before": baseline["assembly_bbox_mm"],
                "after": selected_snapshot["assembly_bbox_mm"],
                "no_regression": baseline["assembly_bbox_mm"] == selected_snapshot["assembly_bbox_mm"],
            },
            "bed_mass": {
                "before": baseline["bed_mass"],
                "after": selected_snapshot["bed_mass"],
            },
            "deflection": {
                "before_mm": baseline["deflection"]["total_tool_point_deflection_mm"],
                "after_mm": selected_estimate.total_tool_point_deflection_mm,
                "target_mm": selected_estimate.target_mm,
                "preferred_target_mm": selected_estimate.preferred_target_mm,
                "acceptance_mm": selected_estimate.acceptance_mm,
                "after_passes_preferred": selected_estimate.preferred_target_passes,
            },
        },
        "dominant_compliance": {
            "before": baseline["deflection"]["dominant_contribution"],
            "after": selected_estimate.dominant_contribution,
            "interpretation": "The selected estimate is still assumption-dominated by equivalent X/Z and interface allowances; it is not FEA or a measurement.",
        },
        "largest_print_and_voron_boundary": {
            "selected": selected_snapshot["largest_printed_part"],
            "preferred_xy_limit_mm": P.preferred_structural_xy_mm,
            "conservative_xy_limit_mm": P.conservative_structural_xy_mm,
            "proof_required": "Conditioning, warp, rail-seat datum, and full-size bed/gantry coupon evidence are required at the 300 mm boundary.",
        },
        "gantry_changes": {
            "before": "Four critical PETG pieces: two towers and two split beam halves; J1 remains the primary center interface.",
            "after": "Two integrated tower/beam side modules retain the split J1 center interface and rail pads; the tower-to-beam PETG joints are removed.",
            "serviceability": "X bearing cartridges and X/Z hardware remain removable; integrated side modules are not yet physically proven.",
        },
        "base_changes": {
            "before": "Seven critical base parts with separate front/rear/side/Y-carrier pieces and a center tie.",
            "after": "Two integrated 150 x 300 mm base/Y modules retain the center tie, feet, Y service cartridges, and inspectable rail datum strategy.",
            "serviceability": "Motors, bearings, rails, screws, feet, and center tie remain serviceable; long-axis conditioning and post-print datum work are open.",
        },
        "bed_changes": {
            "before": "Ribbed 230 x 180 x 30 mm printed bed frame; CAD-equivalent mass is reported separately from support/spoilboard.",
            "after": "Lighter ribbed perimeter/cross-rib bed with retained centered Y-nut boss and four carriage pads; hardware and spoilboard remain separate.",
        },
        "xz_changes": {
            "before": "X carriage plus separate Z fixed-bearing and Z motor service parts.",
            "after": "One coherent X/Z backbone retains removable bearing, motor, screw, rail, and coupler hardware while removing two PETG support seams.",
        },
        "hardware_changes": [
            "No vendor-specific component freeze or purchase order is authorized.",
            "Retain the accepted class baseline: MGN12 X/Y, MGN9 Z, T8 screws/nuts, NEMA17-class motors, flexible couplers, and serviceable fixed/floating supports.",
            "Reconcile actual rail-seat, bearing, motor, spindle, insert, fastener, and tool-access dimensions against the integrated modules before hardware-specific CAD.",
            "Use the existing M3 rail/accessory, M4 general structural/module, and conditional M5 escalation hierarchy; integrated parts do not waive insert and creep evidence.",
        ],
        "physical_validation": {
            "status": "not performed",
            "required": [
                "full-travel bed, spindle, rail, screw, bearing, limit, probe, cable, and tool-clearance mock-up",
                "conditioned 300 mm base/Y rail-carrier and integrated gantry print coupons",
                "5 N tool-point deflection test with contributions isolated where practical",
                "joint preload, creep, pull-out, and repeated-service evidence",
                "measured printed-part and moving-bed mass",
            ],
        },
        "gate_validation": _issue_report(gate),
        "exports": {name: str(path) for name, path in sorted(exports.items())},
        "export_sizes_bytes": export_sizes,
        "exports_non_empty": all(size > 0 for size in export_sizes.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="explicit temporary output directory; defaults to a system temp folder",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        help="optional JSON report path; export paths are reduced to file names when tracked",
    )
    args = parser.parse_args()
    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="pcbCNC-phase4a-optimization-"))
    result = run(output_dir)
    if args.report_path:
        tracked_result = dict(result)
        tracked_result["exports"] = {
            name: Path(path).name for name, path in result["exports"].items()
        }
        tracked_result["export_output_dir"] = "temporary output directory; STEP/STL derivatives are not tracked in Git"
        args.report_path.parent.mkdir(parents=True, exist_ok=True)
        args.report_path.write_text(
            json.dumps(tracked_result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    blocking = any(
        result["variants"][variant][key]["blocking"]
        for variant in result["variants"]
        for key in ("parameter_validation", "assembly_validation")
    )
    if blocking or result["selected"]["unexpected_interferences"] or not result["exports_non_empty"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
