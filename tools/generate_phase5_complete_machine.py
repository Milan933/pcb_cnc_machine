"""Build, validate, export, and describe the complete Phase 5 machine."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any

import build123d

from cad.assembly.phase5_complete_assembly import build_phase5_complete_assembly
from cad.parameters import PHASE5_COMPLETE_PARAMETERS
from cad.parts.phase5_complete_structural import (
    PHASE5_COMPLETE_PART_DEFINITIONS,
    PHASE5_COMPLETE_PART_IDS,
    build_phase5_complete_structural_parts,
)
from cad.validation.phase5_complete import (
    check_phase5_complete_assembly,
    check_phase5_complete_export_files,
    check_phase5_complete_structural_interference,
    check_phase5_complete_structural_parts,
    check_phase5_complete_travel_extremes,
    phase5_complete_gate_report,
)


def _bbox(shape: Any) -> dict[str, tuple[float, float, float]]:
    box = shape.bounding_box()
    return {
        "min": tuple(float(value) for value in box.min),
        "max": tuple(float(value) for value in box.max),
        "size": tuple(float(value) for value in box.size),
    }


def _shape_is_valid(shape: Any) -> bool:
    value = getattr(shape, "is_valid", False)
    return bool(value() if callable(value) else value)


def _solid_count(shape: Any) -> int:
    value = getattr(shape, "solids", ())
    solids = value() if callable(value) else value
    return len(solids)


def _display_path(path: Path) -> str:
    root = Path.cwd().resolve()
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _git_state() -> dict[str, Any]:
    try:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip())
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = "unknown", True
    return {"revision": revision, "working_tree_dirty_at_generation": dirty}


def _issue_dict(issue: Any) -> dict[str, Any]:
    return {
        "rule_id": issue.rule_id,
        "status": issue.status.value,
        "severity": issue.severity.value,
        "message": issue.message,
        "component": issue.component,
        "evidence": issue.evidence,
    }


def _report_dict(report: Any) -> dict[str, Any]:
    return {
        "status": report.status.value,
        "passed": report.passed,
        "issues": [_issue_dict(issue) for issue in report.issues],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=Path("generated"))
    parser.add_argument("--manifest", type=Path, default=Path("docs/manufacturing/phase5-complete-machine-manifest.json"))
    parser.add_argument("--skip-images", action="store_true", help="Skip local PNG rendering; CAD exports and manifest are still generated.")
    return parser


def _render_images(manifest_path: Path, drawing_dir: Path) -> list[Path]:
    launcher = shutil.which("py")
    if not launcher:
        raise RuntimeError("The local system Python launcher 'py' is required for the dependency-light PNG renderer.")
    subprocess.run(
        [launcher, "tools/render_phase5_complete_review.py", "--manifest", str(manifest_path), "--output-dir", str(drawing_dir)],
        check=True,
    )
    return sorted(drawing_dir.glob("*.png"))


def generate(output_root: Path, manifest_path: Path, *, skip_images: bool = False) -> dict[str, Any]:
    output_root = output_root.resolve()
    stl_dir = output_root / "stl" / "phase5-complete-machine"
    step_dir = output_root / "step" / "phase5-complete-machine"
    drawing_dir = output_root / "drawings" / "phase5-complete-machine"
    scene_dir = drawing_dir / "scene-stl"
    for directory in (stl_dir, step_dir, drawing_dir, scene_dir):
        directory.mkdir(parents=True, exist_ok=True)

    parts = build_phase5_complete_structural_parts()
    assembly = build_phase5_complete_assembly()
    reports = {
        "structural_parts": check_phase5_complete_structural_parts(parts),
        "assembly": check_phase5_complete_assembly(assembly),
        "structural_interference": check_phase5_complete_structural_interference(assembly),
        "travel_extremes": check_phase5_complete_travel_extremes(),
        "phase_gate": phase5_complete_gate_report(),
    }
    blocking = [name for name, report in reports.items() if not report.passed]
    if blocking:
        raise RuntimeError(f"Complete Phase 5 validation failed: {blocking}")

    part_records: list[dict[str, Any]] = []
    export_records: dict[str, str] = {}
    for definition in PHASE5_COMPLETE_PART_DEFINITIONS:
        shape = parts[definition.part_id]
        stl_path = stl_dir / f"{definition.part_id}.stl"
        step_path = step_dir / f"{definition.part_id}.step"
        build123d.export_stl(shape, stl_path, tolerance=0.01, angular_tolerance=0.2)
        build123d.export_step(shape, step_path)
        export_records[f"{definition.part_id}_stl"] = _display_path(stl_path)
        export_records[f"{definition.part_id}_step"] = _display_path(step_path)
        volume_mm3 = float(shape.volume)
        part_records.append(
            {
                "part_number": definition.part_number,
                "part_id": definition.part_id,
                "description": definition.description,
                "quantity": definition.quantity,
                "material": definition.material,
                "maturity": definition.maturity,
                "interface_status": definition.interface_status,
                "critical_force_loop_part": definition.critical,
                "print_orientation": definition.print_orientation,
                "support_strategy": definition.support_strategy,
                "bbox_mm": _bbox(shape),
                "volume_mm3": volume_mm3,
                "estimated_mass_kg": volume_mm3 * PHASE5_COMPLETE_PARAMETERS.petg_density_kg_per_mm3,
                "shape_valid": _shape_is_valid(shape),
                "solid_count": _solid_count(shape),
                "stl": _display_path(stl_path),
                "step": _display_path(step_path),
                "notes": definition.notes,
            }
        )

    assembly_step = step_dir / "pcb_cnc_complete_assembly.step"
    assembly_stl = stl_dir / "pcb_cnc_complete_assembly.stl"
    build123d.export_step(assembly.master_shape, assembly_step)
    build123d.export_stl(assembly.master_shape, assembly_stl, tolerance=0.02, angular_tolerance=0.3)
    export_records["complete_assembly_step"] = _display_path(assembly_step)
    export_records["complete_assembly_stl_visualization"] = _display_path(assembly_stl)

    export_paths = {
        name: Path(path)
        for name, path in (
            (key, output_root.parent / value if not Path(value).is_absolute() else Path(value))
            for key, value in export_records.items()
        )
    }
    export_report = check_phase5_complete_export_files(export_paths)
    if not export_report.passed:
        raise RuntimeError("Complete Phase 5 export validation failed")
    reports["exports"] = export_report

    scene_records: list[dict[str, Any]] = []
    for component in assembly.components:
        scene_path = scene_dir / f"{component.name}.stl"
        build123d.export_stl(component.shape, scene_path, tolerance=0.03, angular_tolerance=0.4)
        scene_records.append(
            {
                "name": component.name,
                "category": component.category,
                "stl": _display_path(scene_path),
                "provisional": component.provisional,
            }
        )

    manifest_path = manifest_path.resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "phase": "5-manufacturing-cad",
        "phase_state": "phase-5-complete-virtual-machine",
        "batch": "phase5-complete-machine",
        "status": "complete-virtual-machine-candidate-owner-review",
        "maturity": "PROTOTYPE-STL",
        "units": "mm",
        "owner_authorization": {
            "authorized": True,
            "baseline_commit": "afe2e14089467321b323d74f928a7ab4c5ffdc1f",
            "scope": "complete virtual machine, all printable structural candidates, local derivatives, and owner review package",
        },
        "source": {
            "module_structural": "cad/parts/phase5_complete_structural.py",
            "module_assembly": "cad/assembly/phase5_complete_assembly.py",
            **_git_state(),
        },
        "coordinate_system": {
            "convention": PHASE5_COMPLETE_PARAMETERS.coordinate_convention,
            "machine_origin": PHASE5_COMPLETE_PARAMETERS.machine_origin,
            "work_origin": PHASE5_COMPLETE_PARAMETERS.work_origin,
            "work_area_mm": PHASE5_COMPLETE_PARAMETERS.work_area_mm,
            "usable_travel_mm": PHASE5_COMPLETE_PARAMETERS.usable_travel_mm,
            "travel_min_tool_point_mm": PHASE5_COMPLETE_PARAMETERS.travel_min_mm,
            "travel_max_tool_point_mm": PHASE5_COMPLETE_PARAMETERS.travel_max_mm,
        },
        "parameters": asdict(PHASE5_COMPLETE_PARAMETERS),
        "part_count": len(part_records),
        "part_ids": list(PHASE5_COMPLETE_PART_IDS),
        "parts": part_records,
        "complete_assembly": {
            "component_count": len(assembly.components),
            "printed_structural_count": len(assembly.structural_components),
            "hardware_envelope_count": len(assembly.hardware_components),
            "bbox_mm": _bbox(assembly.master_shape),
            "nominal_travel_state": assembly.travel_state,
            "master_step": _display_path(assembly_step),
            "master_stl_visualization": _display_path(assembly_stl),
            "expected_interference_pairs": [sorted(pair) for pair in assembly.expected_interference_pairs],
            "component_names": [component.name for component in assembly.components],
        },
        "exports": export_records,
        "scene_components": scene_records,
        "review_images": [],
        "hardware_boundary": {
            "controller": "OWNER-SUPPLIED — ARDUINO MEGA + CNC SHIELD",
            "motors": "OWNER-SUPPLIED — DO NOT BUY; standardized generic NEMA17 interface",
            "motor_screening": {
                "frame_mm": PHASE5_COMPLETE_PARAMETERS.nema17_frame_mm,
                "shaft_diameter_mm": PHASE5_COMPLETE_PARAMETERS.nema17_shaft_diameter_mm,
                "body_length_range_mm": PHASE5_COMPLETE_PARAMETERS.nema17_body_length_range_mm,
                "final_assignment": "X/Y suitable owner-stock motors; strongest electrically compatible owner-stock motor for Z after characterization",
            },
            "unresolved_identification": [
                "exact CNC Shield model/revision",
                "installed stepper-driver type and microstep/current/voltage/cooling capability",
                "limit, probe, and spindle PWM/control pin mapping after shield identification",
                "representative final NEMA17 labels, body lengths, shafts, current, resistance, pinout, and condition",
                "measured MGN rail, T8 screw/nut/bearing/coupler, fastener, insert, foot, and spindle interfaces",
            ],
        },
        "validation": {name: _report_dict(report) for name, report in reports.items()},
        "review_package": {
            "assembly_guide": "docs/assembly/assembly-guide.md",
            "coordinate_system": "docs/assembly/coordinate-system.md",
            "wiring_control": "docs/assembly/wiring-control-integration.md",
            "fastener_schedule": "docs/assembly/fastener-schedule.md",
            "bom": "bom/phase5-complete-machine-bom.md",
            "review_report": "docs/manufacturing/phase5-complete-machine-review.md",
        },
        "open_items_before_hardware_validation": [
            "owner reviews all STL files in OrcaSlicer and selects print profiles/orientations",
            "physical first prints and dimensional inspection of critical force-loop parts",
            "measure representative rails, screws, bearings, inserts, feet, spindle, and controller hardware",
            "perform rail alignment, gantry squareness, bed leveling, spindle tram, and full service mock-up",
            "identify exact CNC Shield revision and driver modules before final wiring/pin configuration",
            "characterize representative owner-stock NEMA17 motors before final axis assignment",
            "do not label any part HARDWARE-VALIDATED or RELEASED from this virtual pass",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if not skip_images:
        image_paths = _render_images(manifest_path, drawing_dir)
        manifest["review_images"] = [_display_path(path) for path in image_paths]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    return manifest


def main() -> int:
    args = _parser().parse_args()
    manifest = generate(args.output_root, args.manifest, skip_images=args.skip_images)
    print(
        json.dumps(
            {
                "status": manifest["status"],
                "maturity": manifest["maturity"],
                "part_count": manifest["part_count"],
                "assembly_component_count": manifest["complete_assembly"]["component_count"],
                "assembly_bbox_mm": manifest["complete_assembly"]["bbox_mm"],
                "manifest": _display_path(Path(args.manifest)),
                "review_images": manifest["review_images"],
                "validation_status": {name: value["status"] for name, value in manifest["validation"].items()},
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
