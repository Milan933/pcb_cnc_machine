# PCB CNC

Parametric design foundation for a small desktop CNC machine optimized for PCB
isolation routing, drilling, and outline cutting.

## Project status

This repository is at the foundation stage. The current deliverable establishes
requirements, engineering rules, decision records, CAD conventions, and a
validation scaffold. It intentionally contains no detailed CNC geometry and no
production STEP or STL files.

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
and remains subject to the implementation spike required before Phase 5.

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
- [docs/engineering-workflow.md](docs/engineering-workflow.md): the mandatory
  ten-phase workflow and phase gates.
- [docs/architecture](docs/architecture): system-level architecture before
  detailed CAD.
- [docs/decisions](docs/decisions): engineering decision records.
- [.agents/skills](.agents/skills): project-specific engineering skills.
- [cad/parameters.py](cad/parameters.py): the central preliminary parameter
  set; it contains no detailed part geometry.
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

Review this foundation, resolve the open questions in
[requirements/open-questions.md](requirements/open-questions.md), then execute
the motion-system selection phase. Do not begin detailed structural CAD until
the architecture and motion candidates have an approved decision record.

## Development interface

The current foundation can be checked with:

    python -B -m unittest discover -s tests -v
    python -B tools/repository_audit.py

CAD generation and manufacturing export commands are intentionally not
available yet. They will be documented only after the CAD implementation
spike and validation gates exist.
