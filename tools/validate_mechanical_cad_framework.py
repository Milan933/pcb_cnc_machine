"""Validate the repository's generic mechanical CAD skill framework."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills"

GENERIC_SKILLS = (
    "mechanical-cad-design",
    "mechanical-assembly-design",
    "design-for-3d-printing",
    "mechanical-joints-fasteners",
    "motion-mechanism-design",
    "cad-hardware-integration",
    "cad-design-review",
    "cad-rendering-visualization",
)

EXISTING_OVERLAY_SCOPES = (
    "cad-conventions",
    "design-validation",
    "motion-system-design",
    "pcb-cnc-architecture",
    "printed-structural-design",
)

ANTI_PATTERNS = (
    "FLOATING COMPONENT",
    "MAGIC BOX",
    "DECORATIVE RIB",
    "BOLTS-AS-DOWELS",
    "IMPOSSIBLE FASTENER",
    "TRAPPED HARDWARE",
    "UNSUPPORTED RAIL",
    "COUPLER-AS-BEARING",
    "VISUAL-ONLY ASSEMBLY",
    "TEST-PASSES-SO-DESIGN-IS-GOOD",
    "ARBITRARY SPLIT PLANE",
    "INFILL-AS-STRUCTURE",
    "UNVERIFIED-VENDOR-MODEL",
    "OVERCONSTRAINED MOTION",
    "UNDERCONSTRAINED MOTION",
    "DATUM DRIFT",
    "TOLERANCE HOPE",
)


def validate_framework(root: Path = ROOT) -> list[str]:
    """Return validation errors; an empty list means the framework is valid."""

    skill_root = root / ".agents" / "skills"
    errors: list[str] = []

    for skill_name in GENERIC_SKILLS:
        path = skill_root / skill_name / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing generic skill: {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
            errors.append(f"invalid frontmatter: {path.relative_to(root)}")
        if "TODO" in text or "<placeholder>" in text:
            errors.append(f"unfinished scaffold marker: {path.relative_to(root)}")
        if "**Good:**" not in text or "**Bad:**" not in text:
            errors.append(f"missing good/bad example: {path.relative_to(root)}")

    architecture = skill_root / "mechanical-cad-framework.md"
    anti_patterns = skill_root / "mechanical-cad-anti-patterns.md"
    references = skill_root / "mechanical-cad-references.md"
    exercises = skill_root / "mechanical-cad-validation-exercises.md"
    for path in (architecture, anti_patterns, references, exercises):
        if not path.is_file():
            errors.append(f"missing framework document: {path.relative_to(root)}")

    if architecture.is_file():
        text = architecture.read_text(encoding="utf-8")
        for skill_name in GENERIC_SKILLS:
            if skill_name not in text:
                errors.append(f"architecture does not name {skill_name}")
        for overlay in EXISTING_OVERLAY_SCOPES:
            if overlay not in text:
                errors.append(f"architecture does not classify {overlay}")
        for token in ("REFACTOR", "KEEP", "CNC-SPECIFIC OVERLAY", "Cross-skill workflow"):
            if token not in text:
                errors.append(f"architecture missing classification/workflow token: {token}")

    if anti_patterns.is_file():
        text = anti_patterns.read_text(encoding="utf-8")
        for pattern in ANTI_PATTERNS:
            if pattern not in text:
                errors.append(f"anti-pattern missing: {pattern}")
        if text.count("**Symptom:**") != len(ANTI_PATTERNS):
            errors.append("anti-pattern entries do not all contain symptom fields")
        if text.count("**Correction:**") != len(ANTI_PATTERNS):
            errors.append("anti-pattern entries do not all contain correction fields")

    if references.is_file():
        text = references.read_text(encoding="utf-8")
        if len(re.findall(r"https?://", text)) < 10:
            errors.append("research references contain fewer than ten source URLs")
        if "Retrieved 2026-10-07" not in text:
            errors.append("research retrieval date is missing")

    if exercises.is_file():
        text = exercises.read_text(encoding="utf-8")
        for example in (
            "NEMA17 motor bracket",
            "Supported linear rail",
            "Leadscrew bearing arrangement",
            "Two-piece printable structural beam",
            "Electronics mounting plate",
        ):
            if example not in text:
                errors.append(f"validation exercise missing: {example}")
        if "CNC geometry" not in text:
            errors.append("validation exercises do not state the CNC geometry boundary")

    for overlay in EXISTING_OVERLAY_SCOPES:
        path = skill_root / overlay / "SKILL.md"
        if path.is_file() and "Scope and dependency boundary" not in path.read_text(encoding="utf-8"):
            errors.append(f"existing skill lacks generic/overlay boundary: {path.relative_to(root)}")

    return errors


def main() -> int:
    errors = validate_framework()
    if errors:
        print("Generic mechanical CAD framework validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Generic mechanical CAD framework validation passed: "
        f"{len(GENERIC_SKILLS)} generic skills, {len(ANTI_PATTERNS)} anti-patterns, "
        "five validation exercises, and research/dependency documents present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
