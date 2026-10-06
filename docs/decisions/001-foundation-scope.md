# Engineering decision record: foundation before geometry

- **Record ID:** EDR-001
- **Phase:** Foundation / preparation for Phase 1
- **Status:** accepted for review
- **Date:** 2026-10-06
- **Owner:** project team
- **Affected requirements:** REQ-FN-001 through REQ-VAL-003

## Decision

The first implementation iteration establishes the requirements baseline,
project engineering skills, CAD conventions, decision workflow, and
dependency-light validation interfaces. It does not create detailed CNC
geometry or manufacturing exports.

## Alternatives considered

1. Start with a detailed gantry and select components while modeling.
2. Build a requirements and validation foundation before detailed CAD.
3. Use a mesh or manually edited CAD file as the initial source.

## Reasoning and evidence

The machine has a constrained PCB process goal but several unresolved inputs:
spindle, motor data, controller capability, motion components, workholding,
probing, and acceptance values. Starting detailed geometry would make those
unknowns invisible and would risk fitting the design to an unsuitable
component. A parametric source and validation architecture are therefore
required before the first structural part.

## Risks and mitigations

| Risk | Consequence | Mitigation / evidence needed | Owner |
| --- | --- | --- | --- |
| Foundation becomes documentation without executable checks. | Errors appear only after detailed CAD. | Keep a small standard-library validation scaffold and tests now; extend it at each phase. | project team |
| Preliminary target travel is treated as final. | Architecture is over-constrained or misses the process. | Keep status labels and require acceptance values before Phase 2 closes. | project team |
| Owned hardware is assumed compatible. | Motor or controller cannot support the selected axes. | Record exact hardware and verify interfaces in Phase 3. | project team |

## Unresolved questions

See requirements/open-questions.md. In particular, spindle, motor,
controller, process acceptance, and motion-system choices remain open.

## Validation and review

- [x] Requirements and status vocabulary created.
- [x] Initial skill set created.
- [x] Validation interface and foundation tests created.
- [ ] Foundation reviewed by the project owner.
- [ ] Phase 1 acceptance values added.

## Follow-up

Review the foundation, then execute Phase 1 and Phase 2. Do not create
production exports until the workflow gates are accepted.
