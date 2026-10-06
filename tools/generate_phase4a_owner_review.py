"""Generate tracked Phase 4A O2 engineering views and review metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
from typing import Any

from PIL import Image, ImageDraw

from cad.assembly.phase4_assembly import build_phase4_assembly
from cad.assembly.phase4a_assembly import build_phase4a_assembly
from cad.parameters import PHASE4_STRUCTURAL_PARAMETERS as P
from cad.phase4a_calculations import phase4a_structural_estimate
from cad.parts.phase4a_structural import (
    SELECTED_PHASE4A_VARIANT,
    build_phase4a_structural_parts,
    phase4a_classification,
    phase4a_part_records,
    phase4a_primary_loop_parts,
)

from tools import generate_phase4_owner_review as renderer


_BASELINE_CLASSIFICATION = dict(renderer.CLASSIFICATION)
_BASELINE_PRIMARY_LOOP = set(renderer.PRIMARY_LOOP)
_BASELINE_JOINT_HIGHLIGHTS = set(renderer.JOINT_HIGHLIGHT_NAMES)
_BASELINE_REVIEW_BANNER = renderer.REVIEW_BANNER


def _configure_phase4a_renderer() -> None:
    renderer.CLASSIFICATION = {
        component.name: phase4a_classification(component.name, SELECTED_PHASE4A_VARIANT)
        for component in build_phase4a_structural_parts(SELECTED_PHASE4A_VARIANT)
    }
    renderer.PRIMARY_LOOP = set(phase4a_primary_loop_parts(SELECTED_PHASE4A_VARIANT))
    renderer.JOINT_HIGHLIGHT_NAMES = {
        "gantry_left_integrated",
        "gantry_right_integrated",
        "base_left_integrated",
        "base_right_integrated",
    }
    renderer.REVIEW_BANNER = "PHASE 4A PROPOSED / REVIEW ONLY"


def _phase4a_views(model: Any, output_dir: Path) -> list[str]:
    structural_names = set(renderer.CLASSIFICATION)
    visible_names = {component.name for component in renderer._visible_components(model)}
    hardware_names = visible_names - structural_names
    all_names = structural_names | hardware_names
    gantry_names = {
        name
        for name in all_names
        if "gantry" in name
        or name
        in {
            "phase3a_x_rail_1",
            "phase3a_x_rail_2",
            "phase3a_x_screw",
            "x_fixed_bearing_cartridge",
            "x_floating_bearing_cartridge",
        }
    }
    base_names = {
        name
        for name in all_names
        if name.startswith(("base_", "y_", "machine_foot", "gantry_"))
        or name.startswith(
            (
                "phase3a_y_rail",
                "phase3a_y_carriage",
                "phase3a_y_screw",
                "phase3a_y_nut",
                "phase3a_y_fixed",
                "phase3a_y_floating",
                "phase3a_y_coupler",
                "phase3a_y_nema",
            )
        )
    }
    bed_names = {
        name
        for name in all_names
        if name
        in {
            "moving_bed_frame",
            "phase3a_moving_bed_support",
            "phase3a_spoilboard",
            "phase3a_y_rail_1",
            "phase3a_y_rail_2",
            "phase3a_y_screw",
            "phase3a_y_nut",
            "phase3a_y_carriage_1",
            "phase3a_y_carriage_2",
            "phase3a_y_carriage_3",
            "phase3a_y_carriage_4",
        }
    }
    xz_names = {
        name
        for name in all_names
        if (
            (
                name in renderer.CLASSIFICATION
                and (
                    name
                    in {
                        "x_z_backbone",
                        "z_carriage_plate",
                        "spindle_mount_concept",
                        "gantry_left_integrated",
                        "gantry_right_integrated",
                    }
                    or name.startswith(("x_", "z_"))
                )
            )
            or name.startswith(
                (
                    "phase3a_x_rail",
                    "phase3a_x_carriage",
                    "phase3a_x_screw",
                    "phase3a_z_rail",
                    "phase3a_z_carriage",
                    "phase3a_z_screw",
                    "phase3a_z_nut",
                    "phase3a_z_fixed",
                    "phase3a_z_floating",
                    "phase3a_z_coupler",
                    "phase3a_z_nema",
                    "phase3a_spindle_mount",
                )
            )
        )
    }
    views = [
        (
            "A",
            "01-complete-isometric.png",
            "A - Complete Phase 4A O2/P2 review assembly - isometric",
            38.0,
            25.0,
            renderer._items_for_names(model, all_names),
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE", "hardware/reference"),
        ),
        (
            "B",
            "02-front.png",
            "B - Front elevation - integrated gantry and moving bed",
            -90.0,
            5.0,
            renderer._items_for_names(model, all_names),
            ("CRITICAL STRUCTURAL", "hardware/reference"),
        ),
        (
            "C",
            "03-side.png",
            "C - Side elevation - integrated base, Y service, tower and Z stack",
            0.0,
            5.0,
            renderer._items_for_names(model, all_names),
            ("CRITICAL STRUCTURAL", "hardware/reference"),
        ),
        (
            "D",
            "04-top.png",
            "D - Top view - PCB/bed, rail spacing and 300 mm base modules",
            0.0,
            88.0,
            renderer._items_for_names(model, all_names),
            ("CRITICAL STRUCTURAL", "bed-support", "hardware/reference"),
        ),
        (
            "E",
            "05-exploded-structural.png",
            "E - Exploded Phase 4A structural concept - consolidation review",
            38.0,
            25.0,
            renderer._items_for_names(
                model,
                structural_names,
                offsets={
                    **{
                        name: (0.0, 0.0, -42.0)
                        for name in structural_names
                        if name.startswith(("base_", "machine_foot"))
                    },
                    **{
                        name: (0.0, 0.0, 44.0)
                        for name in structural_names
                        if name.startswith("gantry_")
                    },
                    **{
                        name: (0.0, 48.0, 0.0)
                        for name in structural_names
                        if name.startswith(("x_", "z_", "spindle_"))
                    },
                    "moving_bed_frame": (0.0, -45.0, 0.0),
                    "electronics_mount_rail": (0.0, 0.0, -65.0),
                },
            ),
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE"),
        ),
        (
            "F",
            "06-highlighted-force-loop.png",
            "F - Phase 4A O2 primary force-loop PETG highlighted",
            38.0,
            25.0,
            renderer._items_for_names(model, all_names, "force"),
            ("force-loop PETG", "hardware/reference"),
        ),
        (
            "G",
            "07-gantry-joint-close-up.png",
            "G - Integrated gantry close-up - tower/beam and J1 center interface",
            -38.0,
            25.0,
            renderer._items_for_names(model, gantry_names, "joint"),
            ("highlighted interface", "CRITICAL STRUCTURAL", "hardware/reference"),
        ),
        (
            "H",
            "08-y-rail-base-close-up.png",
            "H - Integrated Y rail/base close-up - carrier datum and service modules",
            -74.0,
            16.0,
            renderer._items_for_names(model, base_names),
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "hardware/reference"),
        ),
        (
            "I",
            "09-bed-underside.png",
            "I - Moving-bed underside - lighter ribs, centered nut boss and carriages",
            35.0,
            -48.0,
            renderer._items_for_names(model, bed_names),
            ("CRITICAL STRUCTURAL", "bed-support", "hardware/reference"),
        ),
        (
            "J",
            "10-z-x-close-up.png",
            "J - X/Z close-up - coherent backbone, rail seats and spindle mount",
            -42.0,
            22.0,
            renderer._items_for_names(model, xz_names),
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE", "hardware/reference"),
        ),
    ]
    generated: list[str] = []
    for _, filename, title, azimuth, elevation, items, legend in views:
        renderer.render_view(items, output_dir / filename, title, azimuth, elevation, legend)
        generated.append(filename)
    return generated


def _before_after_view(before_model: Any, after_model: Any, output_dir: Path) -> str:
    with tempfile.TemporaryDirectory(prefix="pcbCNC-phase4a-before-after-") as temp:
        temp_dir = Path(temp)
        original_classification = renderer.CLASSIFICATION
        original_primary = renderer.PRIMARY_LOOP
        original_joint = renderer.JOINT_HIGHLIGHT_NAMES
        original_banner = renderer.REVIEW_BANNER

        # Restore the baseline configuration explicitly because main() already
        # configured the module for the selected Phase 4A candidate.
        renderer.CLASSIFICATION = dict(_BASELINE_CLASSIFICATION)
        renderer.PRIMARY_LOOP = set(_BASELINE_PRIMARY_LOOP)
        renderer.JOINT_HIGHLIGHT_NAMES = set(_BASELINE_JOINT_HIGHLIGHTS)
        renderer.REVIEW_BANNER = _BASELINE_REVIEW_BANNER
        renderer.REVIEW_BANNER = "PHASE 4 BASELINE / REVIEW ONLY"
        before_names = {component.name for component in renderer._visible_components(before_model)}
        before_path = temp_dir / "before.png"
        renderer.render_view(
            renderer._items_for_names(before_model, before_names),
            before_path,
            "Before - Phase 4 P2 preliminary structural concept",
            38.0,
            25.0,
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE", "hardware/reference"),
        )

        renderer.CLASSIFICATION = original_classification
        renderer.PRIMARY_LOOP = original_primary
        renderer.JOINT_HIGHLIGHT_NAMES = original_joint
        _configure_phase4a_renderer()
        after_names = {component.name for component in renderer._visible_components(after_model)}
        after_path = temp_dir / "after.png"
        renderer.render_view(
            renderer._items_for_names(after_model, after_names),
            after_path,
            "After - Phase 4A O2 proposed optimization",
            38.0,
            25.0,
            ("CRITICAL STRUCTURAL", "SECONDARY STRUCTURAL", "MOUNT / INTERFACE", "hardware/reference"),
        )

        before = Image.open(before_path).convert("RGB")
        after = Image.open(after_path).convert("RGB")
        combined = Image.new("RGB", (before.width * 2, before.height + 54), (246, 248, 249))
        combined.paste(before, (0, 54))
        combined.paste(after, (before.width, 54))
        draw = ImageDraw.Draw(combined)
        draw.text(
            (24, 18),
            "Before \u2192 after structural optimization; both views are review geometry, not release drawings",
            fill=(39, 51, 59),
        )
        output = output_dir / "11-before-after-isometric.png"
        combined.save(output, format="PNG", optimize=True)

        renderer.CLASSIFICATION = original_classification
        renderer.PRIMARY_LOOP = original_primary
        renderer.JOINT_HIGHLIGHT_NAMES = original_joint
        renderer.REVIEW_BANNER = original_banner
    return output.name


def _metrics(model: Any, view_names: list[str]) -> dict[str, Any]:
    records = phase4a_part_records(model.structural_parts, SELECTED_PHASE4A_VARIANT)
    record_by_id = {record.part_id: record for record in records}
    rows: list[dict[str, Any]] = []
    for component in model.structural_parts:
        bbox = component.shape.bounding_box()
        size = tuple(round(float(getattr(bbox.size, axis)), 3) for axis in ("X", "Y", "Z"))
        record = record_by_id[component.name]
        volume = float(component.shape.volume)
        rows.append(
            {
                "part_id": component.name,
                "classification": record.classification,
                "direct_force_loop": record.direct_force_loop,
                "serviceable": record.serviceable,
                "volume_mm3": volume,
                "cad_mass_kg": volume * P.petg_density_kg_per_mm3,
                "actual_bbox_mm": size,
                "print_orientation": record.print_orientation,
                "support_requirement": record.support_requirement,
                "brim_requirement": record.brim_requirement,
                "warping_risk": record.warping_risk,
                "layer_load_concern": record.layer_load_concern,
            }
        )
    estimate = phase4a_structural_estimate(SELECTED_PHASE4A_VARIANT)
    largest = max(rows, key=lambda row: max(row["actual_bbox_mm"][:2]))
    return {
        "phase": "4A-structural-architecture-hardware-freeze",
        "source_variant": "phase4a-o2-p2",
        "owner_boundary": {
            "phase4_preliminary_architecture_baseline_accepted": True,
            "phase4a_preliminary_architecture_baseline_accepted": True,
            "phase4_manufacturing_ready": False,
            "phase5_started": False,
            "production_release": False,
        },
        "review_views": view_names,
        "structural_part_count": len(rows),
        "critical_structural_part_count": sum(row["classification"] == "CRITICAL STRUCTURAL" for row in rows),
        "primary_loop_part_count": sum(row["direct_force_loop"] for row in rows),
        "assembly_component_count": len(model.components),
        "assembly_bbox_mm": {
            key: tuple(float(value) for value in values)
            for key, values in model.bounding_box_mm.items()
        },
        "largest_printed_part": {
            "part_id": largest["part_id"],
            "actual_bbox_mm": largest["actual_bbox_mm"],
            "print_orientation": largest["print_orientation"],
        },
        "cad_solid_equivalent_mass_kg": sum(row["cad_mass_kg"] for row in rows),
        "density_kg_per_mm3": P.petg_density_kg_per_mm3,
        "deflection": {
            "test_load_n": estimate.test_load_n,
            "total_mm": estimate.total_tool_point_deflection_mm,
            "target_mm": estimate.target_mm,
            "preferred_target_mm": estimate.preferred_target_mm,
            "acceptance_mm": estimate.acceptance_mm,
            "target_passes": estimate.target_passes,
            "preferred_target_passes": estimate.preferred_target_passes,
            "acceptance_passes": estimate.acceptance_passes,
            "dominant_contribution": estimate.dominant_contribution,
            "evidence_status": estimate.evidence_status,
        },
        "parts": sorted(rows, key=lambda row: row["part_id"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "docs" / "architecture" / "phase-4a-review",
        help="tracked Phase 4A review-view output directory",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    before_model = build_phase4_assembly()
    after_model = build_phase4a_assembly(
        SELECTED_PHASE4A_VARIANT,
        build_phase4a_structural_parts(SELECTED_PHASE4A_VARIANT),
    )
    _configure_phase4a_renderer()
    views = _phase4a_views(after_model, args.output_dir)
    views.append(_before_after_view(before_model, after_model, args.output_dir))
    metrics = _metrics(after_model, views)
    (args.output_dir / "phase4a-review-metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_dir": str(args.output_dir),
                "views": views,
                "mass_kg": metrics["cad_solid_equivalent_mass_kg"],
                "deflection_mm": metrics["deflection"]["total_mm"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
