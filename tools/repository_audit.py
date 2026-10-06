"""Audit candidate repository files for publication-boundary violations.

The scanner is intentionally conservative and non-leaking: findings report
only a relative path and rule name, never the matched value. It is a
lightweight safeguard, not a replacement for credential rotation or a
dedicated secret-scanning service.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable


SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "env",
    "ENV",
}

SUSPICIOUS_NAMES = (
    ".env",
    "credentials",
    "secrets",
    "password",
    "token",
    "id_rsa",
)

SENSITIVE_SUFFIXES = (".key", ".pem", ".p12", ".pfx", ".secret", ".token")

CONTENT_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private-key-header",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ),
    (
        "credential-assignment",
        re.compile(
            r"(?i)\b(?:api[_ -]?key|access[_ -]?token|github[_ -]?token|"
            r"password|passwd|secret|private[_ -]?key)\b\s*[:=]\s*"
            r"[\"']?[A-Za-z0-9+/_.-]{12,}"
        ),
    ),
    (
        "credential-bearing-url",
        re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@"),
    ),
    (
        "aws-access-key",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ),
    (
        "github-token-shape",
        re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    ),
)

BINARY_SUFFIXES = {
    ".3mf",
    ".gif",
    ".jpg",
    ".jpeg",
    ".png",
    ".stl",
    ".step",
    ".stp",
    ".zip",
}


def git_candidate_paths(root: Path, tracked_only: bool) -> list[Path]:
    """Return tracked or non-ignored candidate paths without exposing content."""

    command = ["git", "ls-files", "-z"]
    if not tracked_only:
        command.extend(["-co", "--exclude-standard"])
    try:
        result = subprocess.run(
            command,
            cwd=root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return list(walk_candidate_paths(root))

    relative_paths = [Path(item) for item in result.stdout.decode().split("\0") if item]
    return [root / relative_path for relative_path in relative_paths]


def walk_candidate_paths(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def suspicious_name(path: Path) -> str | None:
    name = path.name.lower()
    if name == ".env.example":
        return None
    if name == ".env" or name.startswith(".env."):
        return "sensitive-environment-file"
    if name.endswith(SENSITIVE_SUFFIXES):
        return "sensitive-file-extension"
    if any(token in name for token in SUSPICIOUS_NAMES):
        return "sensitive-file-name"
    return None


def content_findings(path: Path) -> list[str]:
    if path.suffix.lower() in BINARY_SUFFIXES:
        return []
    try:
        data = path.read_bytes()
    except OSError:
        return ["unreadable-candidate-file"]
    if b"\0" in data[:4096]:
        return []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return []
    findings = []
    for rule_name, pattern in CONTENT_RULES:
        if pattern.search(text):
            findings.append(rule_name)
    return findings


def audit(paths: Iterable[Path], root: Path) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for path in paths:
        name_rule = suspicious_name(path)
        if name_rule:
            findings.append((path.relative_to(root).as_posix(), name_rule))
        for content_rule in content_findings(path):
            findings.append((path.relative_to(root).as_posix(), content_rule))
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tracked-only",
        action="store_true",
        help="audit only files already tracked by Git",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root; defaults to the current directory",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    paths = git_candidate_paths(root, args.tracked_only)
    findings = audit(paths, root)
    if findings:
        print("Repository audit stopped: suspicious publication material found.")
        for relative_path, rule in findings:
            print(f"- {relative_path}: {rule}")
        print("Values are intentionally not printed.")
        return 1
    mode = "tracked" if args.tracked_only else "candidate"
    print(f"Repository audit passed: {mode} files scanned; no suspicious credential material found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
