# Working-tree cleanup audit

Date: 2026-10-07

## Scope and rule

The current working tree was classified by purpose and architectural origin,
not by filename. The previous PCB-CNC repository and the generic-looking
infrastructure built primarily to support it are removed from the working tree.
Git history is retained and is not rewritten.

## Classification before cleanup

### KEEP — essential generic repository infrastructure

- Git metadata and history under `.git/`.
- A minimal root `README.md`, rewritten to describe the clean research
  baseline.
- A minimal root `.gitignore`, rewritten for generic Python, local-environment,
  credential, and editor hygiene.

### KEEP — precision-mechanical-cad

- `.agents/skills/precision-mechanical-cad/SKILL.md`
- `.agents/skills/precision-mechanical-cad/references/engineering-references.md`
- `.agents/skills/precision-mechanical-cad/references/anti-patterns.md`
- `.agents/skills/precision-mechanical-cad/references/examples-and-exercises.md`

This is the only project skill intentionally preserved. It is product-neutral
and does not depend on the former repository modules.

### DELETE — PCB-CNC project

- `AGENTS.md` — PCB-CNC-specific operating boundary and phase policy.
- `bom/` — machine BOMs, procurement, and hardware measurement records.
- `cad/` — PCB-CNC parametric parts, assemblies, hardware models, parameters,
  exports, and validation.
- `docs/` — PCB-CNC requirements, architecture, calculations, decisions,
  manufacturing, assembly, and review artifacts.
- `generated/` — PCB-CNC STL, STEP, render, and review outputs.
- `requirements/` — PCB-CNC process, motion, structure, and phase requirements.
- `tests/` — PCB-CNC-specific tests and validation fixtures.

### DELETE — CNC-derived infrastructure

- `.agents/skills/cad-conventions/`
- `.agents/skills/cad-design-review/`
- `.agents/skills/cad-hardware-integration/`
- `.agents/skills/cad-rendering-visualization/`
- `.agents/skills/design-for-3d-printing/`
- `.agents/skills/design-validation/`
- `.agents/skills/mechanical-assembly-design/`
- `.agents/skills/mechanical-cad-design/`
- `.agents/skills/mechanical-joints-fasteners/`
- `.agents/skills/motion-mechanism-design/`
- `.agents/skills/motion-system-design/`
- `.agents/skills/pcb-cnc-architecture/`
- `.agents/skills/printed-structural-design/`
- `.agents/skills/repository-workflow/`
- `tools/` — phase generators, renderers, validators, hardware checks, and the
  publication audit created for the former public PCB-CNC project.

The generic-looking CAD and repository abstractions were not retained merely
because they might be reusable later. Their interfaces, terminology, checks,
and workflow assumptions were created inside the former project and could bias
the clean-slate investigation.

### REVIEW — resolution

- `README.md`: retained only as a rewritten generic baseline; all product
  claims, phase references, and old workflow links were removed.
- `.gitignore`: retained only as a rewritten generic hygiene file; all
  generated-CAD allowlists and machine-specific paths were removed.
- `tools/repository_audit.py`: removed. Its publication policy and scanner
  were coupled to the former public PCB-CNC repository, and a replacement
  should be designed only if first-principles research demonstrates a need.
- All other root content was unambiguously product-specific or derived from
  the former CNC effort and was removed.

## Post-cleanup baseline

The intended tree contains only the Git metadata, generic root hygiene and
orientation files, this audit record, and the preserved
`precision-mechanical-cad` skill. No replacement CAD framework is part of this
cleanup.

## Corrective inventory

After the cleanup commit, a hidden-file inventory found four regular files at
`.agents/skills/` that were not shown by the initial directory-only listing:

- `mechanical-cad-framework.md`
- `mechanical-cad-anti-patterns.md`
- `mechanical-cad-references.md`
- `mechanical-cad-validation-exercises.md`

They were introduced by the earlier generic-CAD framework commit and their
framework graph explicitly depended on the deleted skills. They were therefore
classified as CNC-derived infrastructure rather than as supporting material
for `precision-mechanical-cad`, and removed in the follow-up cleanup commit.
The preserved skill directory remains unchanged.
