"""Run the Phase 2 build123d implementation spike.

The output directory is an explicit development-artifact location. It must
not be a generated release directory: this command creates review-only
skeleton STEP/STL derivatives, not manufacturing exports.
"""

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
from cad.validation import check_phase2_skeleton_parameters


def run(output_dir: Path) -> dict[str, object]:
    """Build, validate, bound, and export all three architecture skeletons."""

    import build123d

    parameter_report = check_phase2_skeleton_parameters()
    candidates: list[dict[str, object]] = []
    for candidate_id in ArchitectureId:
        model = build_skeleton(candidate_id)
        exports = export_skeleton(model, output_dir)
        interferences = find_interferences(model)
        unexpected = unexpected_interferences(model)
        candidates.append(
            {
                "candidate": candidate_id.value,
                "component_count": len(model.components),
                "bbox_mm": model.bounding_box_mm,
                "expected_interferences": len([item for item in interferences if item["expected"]]),
                "unexpected_interferences": unexpected,
                "exports": {name: str(path) for name, path in exports.items()},
                "export_sizes_bytes": {name: path.stat().st_size for name, path in exports.items()},
            }
        )

    return {
        "build123d_version": getattr(build123d, "__version__", "unknown"),
        "units": "mm",
        "parameter_validation_status": parameter_report.status.value,
        "parameter_validation_blocking": len(parameter_report.blocking_issues),
        "output_dir": str(output_dir),
        "candidates": candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="explicit temporary output directory; defaults to a system temp folder",
    )
    args = parser.parse_args()
    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="pcbCNC-phase2-cad-spike-"))
    result = run(output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["parameter_validation_blocking"]:
        return 1
    if any(candidate["unexpected_interferences"] for candidate in result["candidates"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
