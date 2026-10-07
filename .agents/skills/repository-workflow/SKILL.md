---
name: repository-workflow
description: Safely audit, commit, publish, and release the public PCB CNC repository while keeping secrets, temporary artifacts, and machine-specific files out of Git.
---

# Repository workflow

Use this skill for Git status, repository initialization, commit, push,
publication, release-artifact, or public-repository hygiene tasks in this
project. It governs the local repository at D:\pcbCNC and the canonical public
remote:

    https://github.com/Milan933/pcb_cnc_machine.git

## Public-repository boundary

This is an open engineering project. The CNC machine design is not
confidential. Normal parametric CAD, STL/STEP exports, complete assembly
exports, PNG/JPG/WebP renders, drawings, BOMs, wiring/assembly documents,
manifests, validation reports, and test results are intended to be
publishable when useful to build, inspect, reproduce, or document the machine.

Assume every committed file is visible to the public. Allowed content
includes source-of-truth parametric CAD, engineering documentation,
requirements, decision records, validation code, tests, BOM data, reviewed
manufacturing files, drawings, assembly instructions, slicer guidance, and
explicitly approved photos or diagrams.

Never publish:

- API keys, access tokens, GitHub tokens, passwords, credentials, cookies, or
  private URLs containing credentials;
- SSH private keys, private-key certificates, or local authentication files;
- machine-specific secrets, environment files containing secrets, local
  virtual environments, build caches, IDE state with sensitive content, local
  temporary files, or unrelated personal files.

Do not print a discovered secret in a command result, commit message, report,
or error summary. Report only the path and the finding category.

## Before a commit intended for push

1. Confirm the repository root and inspect status, branch, recent history, and
   configured remotes.
2. Confirm origin exactly matches the canonical URL before pushing.
3. Review the staged and candidate file list. Check that changes belong to the
   requested project phase.
4. Run the repository audit:

       python -B tools/repository_audit.py

   For a post-commit or tracked-file-only check, use its tracked-only mode.
5. Run the relevant tests and validation. A failed test or suspicious
   credential finding is a stop condition.
6. Inspect the staged diff, including file modes and unexpectedly large or
   binary files. Do not add disposable generated development artifacts merely
   because they exist locally; useful engineering artifacts are allowed when
   the current project policy allowlists or intentionally stages them.

If a suspicious value is found: stop, do not commit, do not push, and report
only the file and reason.

The audit must detect genuine secrets, credentials, private keys, and private
personal information. It must not treat STL, STEP, PNG/JPG/WebP, machine
dimensions, BOM entries, public vendor/product references, or engineering
measurements as suspicious merely because they are binary or public project
content.

## Git initialization and commits

If the authorized local repository is not initialized, initialize it at the
specified project root and add only the canonical origin. Do not infer or add
other remotes.

Prefer small, logically scoped commits with descriptive messages, for example:

    foundation: add public repository workflow

Where practical, connect engineering, CAD, validation, and generated-artifact
commits to the relevant phase or engineering decision record.

Do not rewrite published history, force-push, delete remote branches or tags,
or change a user's Git identity without explicit instruction.

## Publication classes

Keep these classes distinct:

1. **Source of truth**: parametric CAD, requirements, decisions, validation,
   tests, and documentation. Normally version controlled.
2. **Useful versioned engineering artifacts**: current printable STL/STEP,
   assembly exports, renders, drawings, manifests, and related files useful to
   build, inspect, reproduce, or document the machine. Normally tracked when
   intentionally selected.
3. **Disposable development artifacts**: temporary exports, scene meshes,
   caches, viewer state, and local logs. Normally ignored.
4. **Validated manufacturing artifacts**: reviewed STEP/STL/drawings with
   validation evidence and a known source revision.
5. **Release artifacts**: validated files intentionally published under
   generated/step/release/, generated/stl/release/, or
   generated/drawings/release/, with a manifest and review record.

The default generated paths remain protected, while useful current artifacts
may be targeted by narrow `.gitignore` allowlists. For the current Phase 5
pass, the versioned paths are `generated/stl/phase5-complete-machine/`,
`generated/step/phase5-complete-machine/`, and direct PNG/JPG/WebP files in
`generated/drawings/phase5-complete-machine/`. Its `scene-stl/` render inputs
remain disposable. Release subdirectories are a separate maturity boundary;
tracking a candidate does not make it released or hardware-validated. Never
force-add temporary exports.

Future normal CNC engineering artifacts do not require repeated owner
permission. They still require relevant validation and the genuine-sensitive-
data audit.

## Push and remote verification

A push requires explicit user authorization for the current task. Before
pushing, verify origin with a command equivalent to:

    git remote get-url origin

After pushing, verify the remote branch points to the exact local commit:

    git rev-parse HEAD
    git ls-remote origin refs/heads/<branch>

Compare the two full SHA values. If authentication, branch protection, or
network state prevents verification, stop and report the exact non-secret
blocker; do not retry by changing remotes or force-pushing.

## Reproducibility

A fresh clone must eventually be sufficient to install CAD dependencies, run
validation, generate the assembly, export STEP/STL, and run tests. Record
supported tool versions and commands in the repository. Machine-specific
configuration may remain local only when it is not needed to reconstruct the
mechanical design.

Future release tags may use:

    v0.1.0-prototype
    v0.2.0-motion-test
    v0.3.0-pcb-test
    v1.0.0

Do not create a release tag merely because a commit was pushed. A tag requires
the corresponding engineering review and release evidence.
