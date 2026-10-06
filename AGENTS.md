# Agent instructions for PCB CNC

## Current boundary

The repository is in Phase 1: Requirements. Work in this phase may improve
quantitative requirements, calculations, acceptance-test definitions, decision
records, parameter schemas, and validation infrastructure. It must not
silently turn an unresolved choice into an engineering fact.

Do not begin Phase 2 architecture selection, detailed CAD, structural CNC
parts, component selection, or production STL/STEP/drawing generation until
the Phase 1 decision record has been reviewed and the workflow gate is passed.

## Canonical public repository

This is an intentionally public repository. The canonical remote is:

    https://github.com/Milan933/pcb_cnc_machine.git

The local working repository is D:\pcbCNC. For any Git, commit, branch,
publication, or release task, read
[.agents/skills/repository-workflow/SKILL.md](.agents/skills/repository-workflow/SKILL.md).
Verify the configured remote before pushing. Do not force-push, rewrite
published history, delete remote branches or tags, or publish secrets.

The public repository may contain reviewed source, documentation, requirements,
decision records, validation, tests, BOM data, and explicitly approved
manufacturing artifacts. It must not contain credentials, private keys,
machine-specific secrets, local caches, virtual environments, or unrelated
personal files. Use the repository audit before a commit intended for push.

## Source of truth

Use the following order when resolving project intent:

1. explicit user requirements in requirements/requirements.md;
2. the quantitative Phase 1 requirements in requirements/phase-1-*.md;
3. approved engineering decision records in docs/decisions;
4. centralized values in cad/parameters.py;
5. the project skills in .agents/skills;
6. implementation details in part and assembly modules.

If two sources disagree, stop and record the conflict in a decision record.
Never repair a contradiction by changing a lower-level file silently.

## Engineering rules

- This is a PCB-specific machine. Optimize for tool-point stiffness, runout,
  repeatability, probing, and controlled shallow cuts rather than metal-cutting
  force or material-removal rate.
- The structural frame is predominantly printed PETG. Do not replace it with
  aluminum extrusion or plate by default. If a metal component is proposed,
  document the mechanical reason and its load path.
- Prefer monocoques, box sections, ribs, gussets, triangulation, distributed
  interfaces, and short force loops over simply increasing infill.
- Treat PETG creep, anisotropy, print orientation, fastener bearing, and
  long-term preload loss as design inputs.
- All dimensions belong in the centralized parameter model or in a documented
  calculation. Do not scatter unexplained literals through CAD code.
- The authoritative model is parametric. Meshes are manufacturing derivatives,
  never the source of truth.
- A printable part must have a documented realistic print orientation within
  the usable Voron 2.4 350 build volume. A bounding-box-only check is
  insufficient.
- Every major phase requires an engineering decision record covering the
  decision, alternatives, reasoning, risks, and unresolved questions.
- Validation should fail closed when required evidence is absent.

## Coordinate convention

The project convention is:

- X: left to right, positive to the right when facing the machine;
- Y: front to back, positive toward the rear of the machine;
- Z: down to up, positive upward from the workholding reference plane.

The physical location of the machine origin and the final bed datum remain
controlled design decisions. Part code must not invent an origin placement.

## Working style

Before changing geometry or selecting hardware:

1. identify whether a value is known, assumed, preliminary, calculated, or
   verified;
2. update the relevant requirement or decision record;
3. use the relevant project skill;
4. run the applicable validation and tests;
5. summarize new risks and unresolved decisions.

Keep generated artifacts out of source control unless they are explicitly
reviewed manufacturing deliverables. Prefer small, inspectable modules over
large scripts with hidden placement or export behavior.

- Source-of-truth parametric CAD is normally tracked. Temporary exports remain
  ignored. Reviewed release exports may be committed only under the designated
  generated/*/release/ directories after validation and review.
- A fresh clone must eventually be able to install dependencies, run
  validation, generate the assembly, export STEP/STL, and run tests without
  undocumented files outside the repository.
