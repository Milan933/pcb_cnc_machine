# PCB CNC

Parametric design foundation for a small desktop CNC machine optimized for PCB
isolation routing, drilling, and outline cutting.

## Project status

This repository is in Phase 2: Architecture review. Phase 1 is accepted by
the project owner; the current deliverable compares moving-bed, moving-gantry,
and one credible fixed-bed moving-head alternative, documents force loops and
preliminary calculations, and adds an architecture-only parametric skeleton
spike. It still contains no detailed printable CNC parts or production STEP
or STL files.

The project is experimental until physical validation is complete. Existing
documentation and checks must not be read as claims of measured accuracy,
repeatability, stiffness, runout, or manufacturing success.

## Canonical repository

The local working repository is D:\pcbCNC. The canonical public GitHub
repository is:

https://github.com/Milan933/pcb_cnc_machine.git

Publication rules, secret scanning, commit discipline, and release artifact
boundaries are documented in
[docs/repository-workflow.md](docs/repository-workflow.md) and
[the repository-workflow skill](.agents/skills/repository-workflow/SKILL.md).

The preliminary CAD recommendation is build123d. That recommendation is
recorded in [the CAD technology decision](docs/decisions/002-cad-technology.md)
and was exercised by the Phase 2 architecture-only spike; Phase 5 approval is
still required.

## Design intent

The machine is a PCB process tool, not a general-purpose metal milling
machine. The design therefore prioritizes:

- low tool-point deflection and spindle runout;
- a short, stiff Z force loop;
- repeatable PCB workholding and a replaceable spoilboard;
- probing and PCB height mapping;
- adequate travel for the preliminary 200 mm x 150 mm x 30-50 mm target;
- a predominantly 3D-printed PETG structural frame using geometry for
  stiffness.

Owned hardware is treated as an input, not as a reason to force an unsuitable
mechanical layout. The current known items are multiple NEMA 17 motors, an
Arduino CNC Shield / GRBL-compatible controller, and a Voron 2.4 350 mm
printer.

## Repository map

- [requirements](requirements/requirements.md): tagged requirements,
  constraints, and traceability.
- [Phase 1 process requirements](requirements/phase-1-process-requirements.md):
  PCB tools, isolation, drilling, outline, spindle, workholding, and probing.
- [Phase 1 motion and structure](requirements/phase-1-motion-structure.md):
  XY targets, tool-point deflection, and overhang screening limits.
- [Phase 1 architecture comparison](requirements/phase-1-architecture-comparison.md):
  objective moving-bed versus moving-gantry criteria for Phase 2.
- [Phase 1 PETG manufacturing](requirements/phase-1-petg-manufacturing.md):
  print-volume, orientation, tolerance, joint, and rail-seat constraints.
- [Phase 1 Z budget](requirements/phase-1-z-error-budget.md): compensatable
  versus non-compensatable height error.
- [Phase 1 envelope trade](requirements/phase-1-envelope-trade.md): A/B/C
  working-area comparison.
- [Phase 1 acceptance tests](requirements/phase-1-acceptance-tests.md):
  future physical test definitions.
- [docs/engineering-workflow.md](docs/engineering-workflow.md): the mandatory
  ten-phase workflow and phase gates.
- [docs/architecture](docs/architecture): system-level architecture, Phase 2
  trade study, force loops, skeleton spike, and review views.
- [docs/decisions](docs/decisions): engineering decision records.
- [.agents/skills](.agents/skills): project-specific engineering skills.
- [cad/parameters.py](cad/parameters.py): the central preliminary parameter
  set, including Phase 2 skeleton envelopes; it contains no detailed part
  geometry.
- [cad/validation](cad/validation): dependency-light validation interfaces and
  foundation checks.
- [generated](generated): reserved for reviewed manufacturing outputs.
- [tools/repository_audit.py](tools/repository_audit.py): non-leaking
  publication-boundary audit.

Read [AGENTS.md](AGENTS.md) before making project changes.

## Status vocabulary

Every important value or decision must be marked as one of:

- **Known requirement**: supplied by the user or directly observed.
- **Assumption**: adopted temporarily to permit analysis; must be revisited.
- **Preliminary choice**: a selected candidate that still needs engineering
  confirmation.
- **Calculated value**: derived from documented inputs and equations.
- **Experimentally verified value**: measured on hardware or a representative
  printed test article.

## Near-term next step

Review and accept or rework proposed
[EDR-006](docs/decisions/006-phase-2-architecture.md). The unresolved spindle,
controller, motor, exact rail/screw, probing, workholding, and physical-test
questions remain visible and move into the later evidence plan. Phase 3 motion
selection and detailed structural CAD do not begin automatically.

## Development interface

The current foundation can be checked with:

    python -B -m unittest discover -s tests -v
    python -B tools/repository_audit.py

The architecture-only build123d spike is run in an external virtual
environment using the pinned dependency in
[requirements/cad-phase-2.txt](requirements/cad-phase-2.txt):

    python -m tools.run_phase2_cad_spike --output-dir <temporary-directory>

The spike outputs review-only temporary STEP/STL files; it does not create
manufacturing release files.
