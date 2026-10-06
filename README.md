# PCB CNC

Parametric design foundation for a small desktop CNC machine optimized for PCB
isolation routing, drilling, and outline cutting.

## Project status

This repository is in Phase 4A: preliminary structural optimization owner
review; Phase 4 and Phase 4A are not accepted.
Phase 1, the Architecture A baseline, the Phase 3 motion baseline, and the P2
Phase 3A packaging baseline are accepted by the project owner. The current
deliverable contains the Phase 2A structural comparison, motion component
trade, P1/P2/P3 packaging study, the 29-part Phase 4 baseline, the O1/O2/O3
Phase 4A comparison, the selected 19-part O2 review assembly, preliminary
calculations, owner-review views, and temporary STEP/STL exports generated
outside the repository. It contains no manufacturing-ready parts or production
release files.

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
and was exercised by the Phase 2 architecture-only spike. Phase 4 uses the
pinned build123d environment for review geometry only; Phase 5 has not begun.

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
- [Phase 3A PETG fastening strategy](requirements/phase-3a-fastening-strategy.md):
  M3/M4/M5 insert hierarchy, geometric load transfer, modularity, and
  measured-insert evidence boundary.
- [Phase 1 Z budget](requirements/phase-1-z-error-budget.md): compensatable
  versus non-compensatable height error.
- [Phase 1 envelope trade](requirements/phase-1-envelope-trade.md): A/B/C
  working-area comparison.
- [Phase 1 acceptance tests](requirements/phase-1-acceptance-tests.md):
  future physical test definitions.
- [Phase 3 motion system](requirements/phase-3-motion-system.md):
  owner-authorized motion-system screening requirements and evidence boundary.
- [Phase 3A packaging](requirements/phase-3a-packaging.md): compact packaging
  requirements, swept-travel rule, and gate boundary.
- [Phase 4 structural concept](requirements/phase-4-structural-concept.md):
  preliminary PETG force-loop, printability, serviceability, and review gate.
- [Phase 4A structural optimization](requirements/phase-4a-structural-optimization.md):
  O1/O2/O3 comparison, selected O2 consolidation, print boundary, and
  physical-evidence gate.
- [docs/engineering-workflow.md](docs/engineering-workflow.md): the mandatory
  ten-phase workflow and phase gates.
- [docs/architecture](docs/architecture): system-level architecture, Phase 2
  trade study, Phase 2A structural comparison and physical-validation plan,
  Phase 3 motion selection, Phase 3A compact packaging, Phase 4 structural
  concept, Phase 4A optimization, force loops, skeleton spike, and review
  views.
- [docs/decisions](docs/decisions): engineering decision records.
- [bom/phase-3-motion-bom.md](bom/phase-3-motion-bom.md): sample-only motion
  class BOM and purchase boundary.
- [bom/phase-3a-packaging-study.md](bom/phase-3a-packaging-study.md):
  sample-characterization boundary for compact packaging.
- [bom/phase-4a-preliminary-bom.md](bom/phase-4a-preliminary-bom.md):
  preliminary O2 printed-part and hardware measurement boundary.
- [.agents/skills](.agents/skills): project-specific engineering skills.
- [cad/parameters.py](cad/parameters.py): the central preliminary parameter
  set, including Phase 2, Phase 3, Phase 3A review-layout inputs, the Phase 4
  structural part/interface contracts, and the owner-directed PETG insert
  strategy.
- [cad/fastening.py](cad/fastening.py): dependency-light PETG interface checks
  for boss material, edge distance, access, geometric shear transfer, M5, and
  through-bolt justification.
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

Review proposed
[EDR-012](docs/decisions/012-phase-4a-structural-optimization.md) and the
selected O2 before/after package, inspect temporary Phase 4A STEP/STL exports,
measure the actual P2 hardware, and run the named PETG/joint/rail-seat/service
mock-ups. The unresolved spindle, controller, motor, exact rail/screw, insert,
probing, workholding, and physical-test questions remain visible. Phase 5 and
manufacturing release do not begin automatically.

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

The focused A/B study uses the same external environment and is run with:

    python -m tools.run_phase2a_study --output-dir <temporary-directory>

The Phase 3 motion study uses the same external environment and is run with:

    python -m tools.run_phase3_motion_study --output-dir <temporary-directory>

The Phase 3A packaging study uses the same external environment and is run
with:

    python -m tools.run_phase3a_packaging_study --output-dir <temporary-directory>

The Phase 4 preliminary structural study uses the pinned environment and
exports only to a temporary directory:

    python -m tools.run_phase4_preliminary_study --output-dir <temporary-directory>

The Phase 4A optimization comparison uses the same pinned environment and
exports only to a temporary directory:

    python -m tools.run_phase4a_optimization --output-dir <temporary-directory>
    python -m tools.generate_phase4a_owner_review
