"""Run the Phase 3 motion screening and review-only CAD skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from cad.assembly.motion_skeleton import export_motion_skeleton, build_motion_skeleton
from cad.motion_phase3 import phase3_motion_screen, rail_class_lookup
from cad.parameters import PHASE3_MOTION_PARAMETERS
from cad.validation import check_phase3_motion_parameters, phase3_gate_report
from cad.assembly.architecture_skeleton import unexpected_interferences


def run(output_dir: Path) -> dict[str, object]:
    """Generate the report and temporary review exports."""

    parameter_report = check_phase3_motion_parameters()
    gate_report = phase3_gate_report()
    screen = phase3_motion_screen()
    model = build_motion_skeleton()
    exports = export_motion_skeleton(model, output_dir)
    unexpected = unexpected_interferences(model)
    axes: dict[str, object] = {}
    for item in screen.axes:
        axis = next(axis for axis in PHASE3_MOTION_PARAMETERS.axes if axis.axis == item.axis)
        rail = rail_class_lookup(axis.rail_class)
        axes[item.axis] = {
            "travel_mm": item.travel_mm,
            "rail_class": item.rail_class,
            "rail_class_data": {
                "block_type": rail.block_type,
                "assembly_width_mm": rail.assembly_width_mm,
                "assembly_height_mm": rail.assembly_height_mm,
                "block_length_mm": rail.block_length_mm,
                "dynamic_load_kn": rail.dynamic_load_kn,
                "static_load_kn": rail.static_load_kn,
                "rated_moments_nm": [
                    rail.rated_moment_mr_nm,
                    rail.rated_moment_mp_nm,
                    rail.rated_moment_my_nm,
                ],
                "block_mass_kg": rail.block_mass_kg,
                "rail_mass_kg_per_m": rail.rail_mass_kg_per_m,
            },
            "rail_count": item.rail_count,
            "carriages_per_rail": item.carriages_per_rail,
            "rail_center_spacing_mm": item.rail_center_spacing_mm,
            "guide_moment_reaction_n": item.guide_moment_reaction_n,
            "racking_moment_reaction_n": item.racking_moment_reaction_n,
            "screw": {
                "lead_mm": item.screw.lead_mm,
                "full_step_increment_mm": item.screw.full_step_increment_mm,
                "microstep_increment_mm": item.screw.microstep_increment_mm,
                "steps_per_mm": item.screw.steps_per_mm,
                "design_force_n": item.screw.design_force_n,
                "estimated_input_torque_nm": item.screw.estimated_input_torque_nm,
                "unsupported_length_mm": item.screw.unsupported_length_mm,
                "estimated_critical_speed_rpm": item.screw.estimated_critical_speed_rpm,
                "screened_max_speed_rpm": item.screw.screened_max_speed_rpm,
                "screened_max_feed_mm_min": item.screw.screened_max_feed_mm_min,
                "commissioning_feed_mm_min": item.screw.commissioning_feed_mm_min,
            },
            "fixed_bearing_location": axis.fixed_bearing_location,
            "floating_bearing_location": axis.floating_bearing_location,
            "home_direction": axis.home_direction,
        }
    return {
        "phase": "3-motion-system-selection",
        "status": "proposed-owner-review",
        "units": "mm, N, N-mm, N-m, rpm, mm/min unless noted",
        "parameter_validation_status": parameter_report.status.value,
        "parameter_validation_blocking": len(parameter_report.blocking_issues),
        "gate_status": gate_report.status.value,
        "gate_blocking_evidence_items": len(gate_report.blocking_issues),
        "screen": {
            "axes": axes,
            "pcb_edge_margin_mm": list(screen.pcb_edge_margin_mm),
            "moving_bed_mass_kg": screen.moving_bed_mass_kg,
            "motor_torque_margin_xy_screen": screen.motor_torque_margin_xy,
            "motor_torque_margin_z_screen": screen.motor_torque_margin_z,
            "recommended_microsteps": screen.recommended_microsteps,
        },
        "layout": {
            "component_count": len(model.components),
            "component_names": [component.name for component in model.components],
            "bbox_mm": model.bounding_box_mm,
            "unexpected_interferences": unexpected,
            "machine_envelope_mm": PHASE3_MOTION_PARAMETERS.machine_envelope_mm,
            "service_footprint_mm": PHASE3_MOTION_PARAMETERS.service_footprint_mm,
        },
        "exports": {name: str(path) for name, path in exports.items()},
        "export_sizes_bytes": {name: path.stat().st_size for name, path in exports.items()},
        "exports_non_empty": all(path.stat().st_size > 0 for path in exports.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="explicit temporary output directory; defaults to a system temp folder",
    )
    args = parser.parse_args()
    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="pcbCNC-phase3-motion-"))
    result = run(output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["parameter_validation_blocking"]:
        return 1
    if result["layout"]["unexpected_interferences"] or not result["exports_non_empty"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
