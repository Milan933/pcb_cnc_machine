# PCB CNC

Parametric design foundation for a small desktop CNC machine optimized for PCB
isolation routing, drilling, and outline cutting.

## Project status

The owner accepted Phase 4 and Phase 4A as the preliminary structural
architecture baseline on 2026-10-06, selecting the balanced 19-part O2 review
architecture. The owner has now authorized complete Phase 5 virtual-machine
manufacturing CAD: all 19 O2 structural part identities have real source
geometry, a named complete assembly, and local candidate STEP/STL derivatives.
Phase 1, the Architecture A
baseline, the Phase 3 motion baseline, and the P2 Phase 3A packaging baseline
are also accepted. The complete candidate is `PROTOTYPE-STL` only; it contains
no released or hardware-validated parts. Physical review follows the coherent
virtual-machine review rather than an isolated base-pair stop.

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
and was exercised by the Phase 2 architecture-only spike. Phase 5 uses the
pinned build123d environment for the controlled complete-machine manufacturing
pass; the exact hardware-dependent interfaces remain provisional.

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
mechanical layout. The current known items are a large selection of
owner-supplied NEMA17 motors (**do not buy**), an owner-supplied **Arduino
Mega + CNC Shield** controller platform (**do not replace absent a validated
limitation**), and a Voron 2.4 350 mm printer. The exact Shield revision and
installed driver modules remain identification items.

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
- [Phase 5 manufacturing CAD](requirements/phase-5-manufacturing-cad.md):
  first real integrated-base pair, candidate export boundary, and owner-review
  stop gate.
- [Phase 5 complete-machine manufacturing CAD](requirements/phase-5-complete-machine.md):
  complete 19-part virtual machine, travel/interference checks, export and
  review-package contract.
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
- [cad/parts/phase5_structural.py](cad/parts/phase5_structural.py): the first
  fused, parametric integrated-base pair with explicitly provisional hardware
  openings.
- [cad/parts/phase5_complete_structural.py](cad/parts/phase5_complete_structural.py):
  all 19 local fused PETG candidate solids.
- [cad/assembly/phase5_complete_assembly.py](cad/assembly/phase5_complete_assembly.py):
  complete named structural, motion, process, control, and service assembly.
- [cad/fastening.py](cad/fastening.py): dependency-light PETG interface checks
  for boss material, edge distance, access, geometric shear transfer, M5, and
  through-bolt justification.
- [cad/validation](cad/validation): dependency-light validation interfaces and
  foundation checks.
- [generated](generated): useful versioned Phase 5 engineering artifacts and
  separately controlled disposable/release output paths.
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

Review the [complete Phase 5 virtual-machine package](requirements/phase-5-complete-machine.md),
the [owner review report](docs/manufacturing/phase5-complete-machine-review.md),
and the local STL files in OrcaSlicer. Then identify/measure the owner
controller, drivers, motors, motion hardware, spindle, fasteners, and inserts
before controlled first prints and coupons. Continue hardware identification
under [EDR-013](requirements/hardware-procurement-measurement-freeze.md); do
not publish release artifacts from this candidate pass.

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

The authorized complete Phase 5 pass uses the pinned environment and writes
useful current derivatives under the allowlisted
`generated/stl/phase5-complete-machine/` and
`generated/step/phase5-complete-machine/` directories, with review PNGs under
`generated/drawings/phase5-complete-machine/`:

    python -m tools.generate_phase5_complete_machine

The generated candidates are `PROTOTYPE-STL` review artifacts, not release
files. Temporary scene meshes and caches remain ignored.

The Phase 4A optimization comparison uses the same pinned environment and
exports only to a temporary directory:

    python -m tools.run_phase4a_optimization --output-dir <temporary-directory>
    python -m tools.generate_phase4a_owner_review
