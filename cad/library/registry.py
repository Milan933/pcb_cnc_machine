"""Authoritative registry and stable-ID mapping for persistent hardware CAD."""

from __future__ import annotations

import ast
from copy import deepcopy
from fnmatch import fnmatchcase
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable


HARDWARE_LIBRARY_MANIFEST_PATH = Path(__file__).with_name("hardware-model-manifest.json")
_COMPONENT_ID_PATTERN = re.compile(r"^HW-[A-Z0-9-]+$")
_REQUIRED_ENTRY_FIELDS = {
    "component_id",
    "category",
    "description",
    "manufacturer",
    "part_number",
    "source_url",
    "source_type",
    "original_filename",
    "local_model_path",
    "model_format",
    "license",
    "redistribution_allowed",
    "sha256",
    "retrieved_date",
    "verification_status",
    "critical_dimensions",
    "confidence_classification",
    "master_component_patterns",
    "notes",
}


def _model_symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def _validate_model_path(value: str, errors: list[str]) -> None:
    for reference in (part.strip() for part in value.split(";") if part.strip()):
        if "::" not in reference:
            errors.append(f"local_model_path must use path::symbol syntax: {reference}")
            continue
        relative, symbol = reference.split("::", 1)
        path = HARDWARE_LIBRARY_MANIFEST_PATH.parent.parent.parent / relative
        if not path.exists():
            errors.append(f"local model path does not exist: {relative}")
            continue
        try:
            symbols = _model_symbols(path)
        except (OSError, SyntaxError) as exc:
            errors.append(f"cannot parse local model path {relative}: {exc}")
            continue
        if symbol not in symbols:
            errors.append(f"local model symbol is not defined: {relative}::{symbol}")


def validate_hardware_library_manifest(manifest: dict[str, Any] | None = None) -> tuple[str, ...]:
    """Return fail-closed schema/provenance errors for the authoritative manifest."""

    value = manifest if manifest is not None else json.loads(HARDWARE_LIBRARY_MANIFEST_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    if value.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if value.get("manifest_type") != "persistent-hardware-cad-library":
        errors.append("manifest_type is not the persistent hardware CAD library type")
    entries = value.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries must be a non-empty list")
        return tuple(errors)

    seen_ids: set[str] = set()
    seen_patterns: dict[str, str] = {}
    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(_REQUIRED_ENTRY_FIELDS - set(entry))
        errors.extend(f"{prefix} missing {field}" for field in missing)
        component_id = entry.get("component_id")
        if not isinstance(component_id, str) or not _COMPONENT_ID_PATTERN.fullmatch(component_id):
            errors.append(f"{prefix}.component_id is not a stable HW-* ID")
        elif component_id in seen_ids:
            errors.append(f"duplicate component_id: {component_id}")
        else:
            seen_ids.add(component_id)
        if entry.get("redistribution_allowed") not in (True, False, None):
            errors.append(f"{prefix}.redistribution_allowed must be true, false, or null")
        checksum = entry.get("sha256")
        if checksum is not None and (not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", checksum)):
            errors.append(f"{prefix}.sha256 must be null or a 64-character hexadecimal checksum")
        local_model_path = entry.get("local_model_path")
        if isinstance(local_model_path, str):
            _validate_model_path(local_model_path, errors)
        else:
            errors.append(f"{prefix}.local_model_path must be a string")
        patterns = entry.get("master_component_patterns")
        if not isinstance(patterns, list) or not all(isinstance(pattern, str) for pattern in patterns):
            errors.append(f"{prefix}.master_component_patterns must be a list of strings")
        else:
            for pattern in patterns:
                previous = seen_patterns.get(pattern)
                if previous is not None:
                    errors.append(f"duplicate assembly pattern {pattern!r} used by {previous} and {component_id}")
                else:
                    seen_patterns[pattern] = str(component_id)
    return tuple(errors)


def hardware_library_manifest_dict() -> dict[str, Any]:
    """Load and return a detached copy of the authoritative JSON manifest."""

    manifest = json.loads(HARDWARE_LIBRARY_MANIFEST_PATH.read_text(encoding="utf-8"))
    errors = validate_hardware_library_manifest(manifest)
    if errors:
        raise ValueError("Invalid hardware CAD library manifest: " + "; ".join(errors))
    return deepcopy(manifest)


def hardware_library_entries() -> tuple[dict[str, Any], ...]:
    return tuple(hardware_library_manifest_dict()["entries"])


def hardware_model_id_for_instance(instance_name: str) -> str | None:
    """Resolve one master-assembly instance to its stable library model ID."""

    matches = [
        entry["component_id"]
        for entry in hardware_library_entries()
        for pattern in entry["master_component_patterns"]
        if fnmatchcase(instance_name, pattern)
    ]
    if len(matches) > 1:
        raise ValueError(f"Assembly instance {instance_name!r} maps to multiple hardware models: {matches}")
    return matches[0] if matches else None


def hardware_model_ids_for_instances(instance_names: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({model_id for name in instance_names if (model_id := hardware_model_id_for_instance(name))}))


def hardware_library_sha256(path: Path) -> str:
    """Return a checksum helper for future vendored source files."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


__all__ = [
    "HARDWARE_LIBRARY_MANIFEST_PATH",
    "hardware_library_entries",
    "hardware_library_manifest_dict",
    "hardware_library_sha256",
    "hardware_model_id_for_instance",
    "hardware_model_ids_for_instances",
    "validate_hardware_library_manifest",
]
