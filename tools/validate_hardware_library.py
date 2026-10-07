"""Validate the persistent hardware CAD library manifest and stable IDs."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cad.library.registry import (
    HARDWARE_LIBRARY_MANIFEST_PATH,
    hardware_library_entries,
    hardware_library_manifest_dict,
    validate_hardware_library_manifest,
)


def main() -> int:
    manifest = hardware_library_manifest_dict()
    errors = validate_hardware_library_manifest(manifest)
    if errors:
        print(json.dumps({"manifest": str(HARDWARE_LIBRARY_MANIFEST_PATH), "errors": list(errors)}, indent=2))
        return 1
    summary = manifest["provenance_summary"]
    print(
        json.dumps(
            {
                "manifest": str(HARDWARE_LIBRARY_MANIFEST_PATH),
                "entry_count": len(hardware_library_entries()),
                "stable_ids": [entry["component_id"] for entry in hardware_library_entries()],
                "provenance_summary": summary,
                "status": "pass",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
