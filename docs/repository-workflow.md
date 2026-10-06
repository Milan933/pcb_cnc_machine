# Repository and publication workflow

This project is intentionally public.

- Local working repository: D:\pcbCNC
- Canonical public remote:
  https://github.com/Milan933/pcb_cnc_machine.git

The repository is experimental until physical validation is complete. Public
documentation must distinguish source code and design intent from measured
machine performance.

## What belongs in the public repository

The public repository may contain:

- parametric CAD source;
- requirements, calculations, architecture, and engineering decision records;
- validation code and tests;
- BOM data;
- reviewed STEP/STL files and drawings;
- assembly instructions and slicer recommendations;
- photos and diagrams explicitly approved for publication.

It must not contain secrets, private keys, credentials, authentication
cookies, machine-specific secrets, local environment files containing secrets,
virtual environments, build caches, sensitive IDE metadata, temporary files,
or unrelated personal files.

## Artifact publication classes

| Class | Default location / state | Publication rule |
| --- | --- | --- |
| Source of truth | CAD source, docs, requirements, validation, tests | Normally tracked. |
| Development artifact | Local cache or temporary generated export | Normally ignored and never published automatically. |
| Validated manufacturing artifact | Reviewed STEP/STL/drawing | Publish only after relevant validation and review. |
| Release artifact | generated/step/release, generated/stl/release, generated/drawings/release | Requires source revision, manifest, validation result, and review. |

The default generated directories remain ignored so an exploratory export
cannot become a public file by accident. The release subdirectories are
explicit publication locations, but placing a file there is not a substitute
for review.

## Pre-commit and pre-push sequence

1. Verify the repository root, branch, status, and recent history.
2. Verify origin is exactly the canonical public URL.
3. Inspect the candidate or staged file list and the staged diff.
4. Run the non-leaking audit:

       python -B tools/repository_audit.py

   It reports only paths and finding categories, never matched credential
   values. Use --tracked-only when auditing the committed file set.
5. Run tests and applicable validation.
6. Commit a small logical change with a descriptive message.
7. Push only when explicitly authorized for the current task.
8. Compare the local commit SHA with the remote branch SHA after pushing.

If a suspicious credential is found, stop immediately. Do not commit or push;
remove or quarantine the file through an authorized, separately reviewed
action, and report only the path and category.

## Reproducibility

A fresh clone should eventually be able to install CAD dependencies, run
validation, generate the complete assembly, export STEP/STL, and run tests.
Commands and supported versions must be documented in the repository. No
undocumented file outside the clone may be required to reconstruct the
mechanical design.

Future release tags are planned as:

- v0.1.0-prototype
- v0.2.0-motion-test
- v0.3.0-pcb-test
- v1.0.0

These tags are placeholders for future reviewed releases and are not created
by the foundation workflow.
