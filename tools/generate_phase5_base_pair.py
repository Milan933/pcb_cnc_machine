"""Generate and validate the first Phase 5 integrated base-pair candidates."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import subprocess
from typing import Any

import build123d

from cad.parts.phase5_structural import (
    PHASE5_BASE_PAIR_PARAMETERS,
    PHASE5_BASE_PART_IDS,
    build_phase5_base_pair,
)
from cad.validation import check_phase5_base_pair_geometry, check_phase5_export_files


def _bbox(shape: Any) -> dict[str, tuple[float, float, float]]:
    bounding_box = shape.bounding_box()

    def vector_tuple(vector: Any) -> tuple[float, float, float]:
        return tuple(float(getattr(vector, axis)) for axis in ("X", "Y", "Z"))

    return {
        "min": vector_tuple(bounding_box.min),
        "max": vector_tuple(bounding_box.max),
        "size": vector_tuple(bounding_box.size),
    }


def _shape_is_valid(shape: Any) -> bool:
    value = getattr(shape, "is_valid", False)
    return bool(value() if callable(value) else value)


def _solid_count(shape: Any) -> int:
    value = getattr(shape, "solids", ())
    solids = value() if callable(value) else value
    return len(solids)


def _display_path(path: Path) -> str:
    """Keep manifests reproducible and free of machine-specific absolutes."""

    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _git_state() -> dict[str, Any]:
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        dirty = bool(
            subprocess.check_output(
                ["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL
            ).strip()
        )
    except (OSError, subprocess.CalledProcessError):
        revision = "unknown"
        dirty = True
    return {"revision": revision, "working_tree_dirty_at_generation": dirty}


def _issue_dict(issue: Any) -> dict[str, Any]:
    evidence = issue.evidence
    if evidence:
        repo_root = str(Path.cwd().resolve())
        evidence = evidence.replace(repo_root, ".").replace(repo_root.replace("\\", "/"), ".")
    return {
        "rule_id": issue.rule_id,
        "status": issue.status.value,
        "severity": issue.severity.value,
        "message": issue.message,
        "component": issue.component,
        "evidence": evidence,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("generated"),
        help="Generated-output root; STEP/STL candidates remain in ignored subdirectories.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("docs/manufacturing/phase5-base-pair-manifest.json"),
        help="Tracked or review-local JSON manifest path.",
    )
    return parser


def generate(output_root: Path, manifest_path: Path) -> dict[str, Any]:
    """Build, export, validate, and describe the first base-pair batch."""

    output_root = output_root.resolve()
    stl_dir = output_root / "stl" / "phase5-base-pair"
    step_dir = output_root / "step" / "phase5-base-pair"
    stl_dir.mkdir(parents=True, exist_ok=True)
    step_dir.mkdir(parents=True, exist_ok=True)

    parts = build_phase5_base_pair()
    geometry_report = check_phase5_base_pair_geometry(parts)
    if not geometry_report.passed:
        raise RuntimeError(
            "Phase 5 base-pair geometry validation failed: "
            + "; ".join(issue.rule_id for issue in geometry_report.blocking_issues)
        )

    export_paths: dict[str, Path] = {}
    part_records: list[dict[str, Any]] = []
    for part_id in PHASE5_BASE_PART_IDS:
        shape = parts[part_id]
        stl_path = stl_dir / f"{part_id}.stl"
        step_path = step_dir / f"{part_id}.step"
        build123d.export_stl(shape, stl_path, tolerance=0.01, angular_tolerance=0.2)
        build123d.export_step(shape, step_path)
        export_paths[f"{part_id}_stl"] = stl_path
        export_paths[f"{part_id}_step"] = step_path
        part_records.append(
            {
                "part_id": part_id,
                "maturity": PHASE5_BASE_PAIR_PARAMETERS.maturity,
                "interface_status": PHASE5_BASE_PAIR_PARAMETERS.interface_status,
                "coordinate_frame": "local print frame; X width, Y length, Z print-up",
                "print_orientation": "flat on the XY base face; no support; brim/skirt is slicer-review dependent",
                "shape_valid": _shape_is_valid(shape),
                "solid_count": _solid_count(shape),
                "bbox_mm": _bbox(shape),
                "stl": _display_path(stl_path),
                "step": _display_path(step_path),
            }
        )

    export_report = check_phase5_export_files(export_paths)
    if not export_report.passed:
        raise RuntimeError(
            "Phase 5 export validation failed: "
            + "; ".join(issue.rule_id for issue in export_report.blocking_issues)
        )

    parameters = asdict(PHASE5_BASE_PAIR_PARAMETERS)
    parameters["overall_height_mm"] = PHASE5_BASE_PAIR_PARAMETERS.overall_height_mm
    parameters["side_member_depth_mm"] = PHASE5_BASE_PAIR_PARAMETERS.side_member_depth_mm
    parameters["rail_hole_y_positions_mm"] = PHASE5_BASE_PAIR_PARAMETERS.rail_hole_y_positions_mm
    manifest = {
        "phase": "5-manufacturing-cad",
        "batch": "phase5-base-pair",
        "status": "candidate-generated-owner-review",
        "maturity": PHASE5_BASE_PAIR_PARAMETERS.maturity,
        "units": "mm",
        "owner_authorization": {
            "authorized": True,
            "baseline_commit": "afe2e14089467321b323d74f928a7ab4c5ffdc1f",
            "scope": "first real printable structural STL/STEP batch only",
        },
        "source": {
            "module": "cad/parts/phase5_structural.py",
            **_git_state(),
        },
        "parts": part_records,
        "parameters": parameters,
        "hardware_boundary": {
            "controller": "OWNER-SUPPLIED — ARDUINO MEGA + CNC SHIELD",
            "motors": "OWNER-SUPPLIED — DO NOT BUY; generic NEMA17 interface",
            "unresolved_identification": [
                "exact CNC Shield model/revision",
                "installed stepper-driver modules",
                "driver microstep/current/voltage/cooling capability",
                "representative final NEMA17 assignment",
                "measured rail, fastener, foot, and center-tie interfaces",
            ],
        },
        "validation": {
            "geometry_status": geometry_report.status.value,
            "geometry_passed": geometry_report.passed,
            "geometry_issues": [_issue_dict(issue) for issue in geometry_report.issues],
            "export_status": export_report.status.value,
            "export_passed": export_report.passed,
            "export_issues": [_issue_dict(issue) for issue in export_report.issues],
        },
        "open_items_before_release": [
            "owner opens both STL files in OrcaSlicer and reviews orientation, supports, brim, walls, ribs, holes, and estimated print behavior",
            "first physical PETG print and dimensional inspection",
            "measure representative Y rails and fasteners before fit claim",
            "inspect rail datum and post-process/shim strategy",
            "review base/center-tie and foot interfaces against the remaining O2 assembly",
        ],
        "stop_boundary": "Do not generate the remaining 17 O2 structural parts until owner review of this batch.",
    }
    manifest_path = manifest_path.resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    args = _parser().parse_args()
    manifest = generate(args.output_root, args.manifest)
    print(
        json.dumps(
            {
                "status": manifest["status"],
                "maturity": manifest["maturity"],
                "parts": [part["part_id"] for part in manifest["parts"]],
                "manifest": _display_path(args.manifest),
                "outputs": [
                    path
                    for part in manifest["parts"]
                    for path in (part["stl"], part["step"])
                ],
                "stop_boundary": manifest["stop_boundary"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
