"""Run the Phase 3A compact packaging study and review-only skeletons."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from cad.assembly.packaging_skeleton import (
    build_packaging_skeleton,
    export_packaging_skeleton,
    packaging_model_interferences,
)
from cad.packaging_phase3a import phase3a_packaging_study
from cad.parameters import PHASE3A_PACKAGING_VARIANTS
from cad.validation import (
    check_phase3a_all_variants,
    check_phase3a_fastener_interfaces,
    check_phase3a_model_containment,
    phase3a_gate_report,
)


def _axis_report(axis: object) -> dict[str, object]:
    return {
        "axis": axis.axis,
        "travel_mm": axis.travel_mm,
        "rail_class": axis.rail_class,
        "block_length_mm": axis.block_length_mm,
        "carriage_center_offsets_mm": list(axis.carriage_center_offsets_mm),
        "carriage_group_span_mm": axis.carriage_group_span_mm,
        "declared_end_margin_mm": axis.declared_end_margin_mm,
        "minimum_rail_length_mm": axis.minimum_rail_length_mm,
        "rail_length_mm": axis.rail_length_mm,
        "actual_end_margin_mm": axis.actual_end_margin_mm,
        "screw_lead_mm": axis.screw_lead_mm,
        "screw_length_mm": axis.screw_length_mm,
        "screw_unsupported_length_mm": axis.screw_unsupported_length_mm,
        "critical_speed_rpm": axis.critical_speed_rpm,
        "screened_max_feed_mm_min": axis.screened_max_feed_mm_min,
        "commissioning_feed_mm_min": axis.commissioning_feed_mm_min,
        "feed_margin_mm_min": axis.feed_margin_mm_min,
        "rail_travel_passes": axis.rail_travel_passes,
        "feed_screen_passes": axis.feed_screen_passes,
    }


def run(output_dir: Path) -> dict[str, object]:
    """Generate calculations and temporary STEP/STL review exports."""

    parameter_report = check_phase3a_all_variants()
    fastening_report = check_phase3a_fastener_interfaces()
    gate_report = phase3a_gate_report()
    variants: dict[str, object] = {}
    for variant in PHASE3A_PACKAGING_VARIANTS:
        study = phase3a_packaging_study(variant)
        model = build_packaging_skeleton(variant)
        containment = check_phase3a_model_containment(model, variant)
        unexpected = packaging_model_interferences(model)
        exports = export_packaging_skeleton(model, output_dir)
        variants[variant.variant_id] = {
            "title": variant.title,
            "design_intent": variant.design_intent,
            "working_area_mm": list(variant.working_area_mm),
            "tool_travel_mm": list(variant.tool_travel_mm),
            "bed_support_mm": list(variant.bed_support_mm),
            "spoilboard_mm": list(variant.spoilboard_mm),
            "pcb_edge_margin_mm": list(study.bed.pcb_edge_margin_mm),
            "bed_transverse_overhang_mm": study.bed.transverse_bed_overhang_mm,
            "bed_longitudinal_overhang_mm": study.bed.longitudinal_bed_overhang_mm,
            "swept_bed_end_clearance_mm": study.bed.swept_bed_end_clearance_mm,
            "bed_to_y_motor_clearance_mm": study.bed.bed_to_y_motor_clearance_mm,
            "tool_to_bed_clearance_mm": list(study.bed.tool_to_bed_clearance_mm),
            "spindle_swept_body_clearance_mm": list(study.bed.spindle_swept_body_clearance_mm),
            "vacuum_perimeter_status": study.bed.vacuum_perimeter_status,
            "axes": [_axis_report(axis) for axis in study.axes],
            "body_envelope_mm": list(study.body_envelope_mm),
            "service_footprint_mm": list(study.service_footprint_mm),
            "z_stack": {
                "bed_support_drop_mm": study.z_stack.bed_support_drop_mm,
                "spoilboard_drop_mm": study.z_stack.spoilboard_drop_mm,
                "pcb_max_thickness_mm": study.z_stack.pcb_max_thickness_mm,
                "tool_stickout_mm": study.z_stack.tool_stickout_mm,
                "spindle_envelope_length_mm": study.z_stack.spindle_envelope_length_mm,
                "tool_and_spindle_top_mm": study.z_stack.tool_and_spindle_top_mm,
                "z_carriage_group_min_mm": study.z_stack.z_carriage_group_min_mm,
                "z_carriage_group_max_mm": study.z_stack.z_carriage_group_max_mm,
                "z_rail_min_mm": study.z_stack.z_rail_min_mm,
                "z_rail_max_mm": study.z_stack.z_rail_max_mm,
                "z_fixed_support_top_mm": study.z_stack.z_fixed_support_top_mm,
                "z_motor_top_mm": study.z_stack.z_motor_top_mm,
                "y_motor_bottom_mm": study.z_stack.y_motor_bottom_mm,
                "gantry_top_mm": study.z_stack.gantry_top_mm,
                "package_min_z_mm": study.z_stack.package_min_z_mm,
                "package_max_z_mm": study.z_stack.package_max_z_mm,
                "package_height_mm": study.z_stack.package_height_mm,
            },
            "bearing_strategy": variant.bearing_strategy,
            "motor_strategies": {axis: strategy for axis, strategy in variant.motor_strategies},
            "largest_future_petg_print_mm": list(variant.largest_future_petg_print_mm),
            "largest_future_petg_print_notes": variant.largest_future_petg_print_notes,
            "parameter_validation_status": check_phase3a_all_variants((variant,)).status.value,
            "fastening_interface_status": fastening_report.status.value,
            "fastening_interface_blocking": len(fastening_report.blocking_issues),
            "model_containment_status": containment.status.value,
            "model_containment_blocking": len(containment.blocking_issues),
            "layout": {
                "component_count": len(model.components),
                "bbox_mm": model.bounding_box_mm,
                "unexpected_interferences": unexpected,
            },
            "exports": {name: str(path) for name, path in exports.items()},
            "export_sizes_bytes": {name: path.stat().st_size for name, path in exports.items()},
            "exports_non_empty": all(path.stat().st_size > 0 for path in exports.values()),
        }
    return {
        "phase": "3A-compact-packaging-optimization",
        "status": "owner-accepted-p2-baseline",
        "units": "mm, mm/min, rpm unless noted",
        "parameter_validation_status": parameter_report.status.value,
        "parameter_validation_blocking": len(parameter_report.blocking_issues),
        "fastening_interface_status": fastening_report.status.value,
        "fastening_interface_blocking": len(fastening_report.blocking_issues),
        "gate_status": gate_report.status.value,
        "gate_blocking_evidence_items": len(gate_report.blocking_issues),
        "variants": variants,
        "phase4_started": True,
        "phase4_status": "preliminary-structural-concept-owner-review",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="explicit temporary output directory; defaults to a system temp folder",
    )
    args = parser.parse_args()
    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="pcbCNC-phase3a-packaging-"))
    result = run(output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["parameter_validation_blocking"] or result["fastening_interface_blocking"]:
        return 1
    for variant in result["variants"].values():
        if variant["model_containment_blocking"] or variant["layout"]["unexpected_interferences"] or not variant["exports_non_empty"]:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
