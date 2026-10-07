# Phase 5 master-assembly-first owner review

Status: generated virtual-machine candidate; `PROTOTYPE-STL`.

The complete assembled CNC is the primary design object. The printable PETG
parts are derived from its hardware relationships and load paths. The previous
envelope-only STL set is superseded and must not be printed or released.

## Review scope

- fixed gantry with moving Y bed and 200 x 150 mm PCB work area;
- 20 derived PETG structural solids, including a dedicated rear Y floating-
  bearing bridge;
- local derived models for MGN12/MGN9 guide classes, T8 screws/nuts, 608
  bearings, couplers, generic owner-stock NEMA17 motors, Arduino Mega,
  provisional CNC Shield, ER11 spindle candidate, switches, probe, and
  representative fastener;
- persistent hardware library with stable IDs, source provenance, reuse
  status, and deterministic project-generated builder paths;
- complete named master assembly with 68 components, support/fastening
  records, service loops, workholding, controller access, and cable volumes;
- actual individual STL/STEP candidates, complete master STEP, and a master
  visualization STL suitable for opening in OrcaSlicer;
- 16 review views covering assembled, subsystem, exploded, printed-only,
  hardware-only, and motion-extreme states.

## Current virtual dimensions

| Item | Current value | Evidence status |
| --- | ---: | --- |
| Master envelope X/Y/Z | 370 x 406 x 320 mm | calculated virtual envelope |
| PCB work area | 200 x 150 mm | accepted screening requirement |
| Tool-point screening travel | 220 x 170 x 40 mm | preliminary packaging target |
| Printed-part screening bound | 320 mm maximum | automated candidate check |
| Structural candidates | 20 | local fused PETG solids |
| Master components | 68 | 20 structural plus hardware/process models |
| Motor interface | 42.3 mm NEMA17 class; 5 mm shaft screen; 40-48 mm body | generic owner-stock interface |
| Spindle representation | SycoTec 5045 AC-ER11 local 45 x 140 mm envelope | reference candidate only |

The 320 mm master Z extent is an assembly envelope, not a claim that the
owner's printer can produce it as one part. The longest structural parts are
the conditional 320 mm base sides; all individual candidate solids are
screened against the conservative 320 mm bound. Verify usable Voron 350
volume and long-axis process distortion before any print.

## Reproducible package

Run the pinned CAD environment:

```text
C:\Users\milan\pcbCNC-cad-env\Scripts\python.exe -m tools.generate_phase5_complete_machine
```

The package is written to:

- [`generated/stl/phase5-complete-machine/`](../../generated/stl/phase5-complete-machine/)
  for individual candidates and `pcb_cnc_master_assembly.stl`;
- [`generated/step/phase5-complete-machine/`](../../generated/step/phase5-complete-machine/)
  for individual candidates and `pcb_cnc_master_assembly.step`;
- [`generated/drawings/phase5-complete-machine/`](../../generated/drawings/phase5-complete-machine/)
  for 16 review views;
- [`phase5-complete-machine-manifest.json`](phase5-complete-machine-manifest.json)
  for inventory, source, hardware library/register, support audit, exports,
  and validation;
- [`../../cad/library/hardware-model-manifest.json`](../../cad/library/hardware-model-manifest.json)
  for the authoritative reusable hardware registry.

No `release/` output is created.

## Review views

1. [master front isometric](../../generated/drawings/phase5-complete-machine/01-master-front-isometric.png)
2. [master rear isometric](../../generated/drawings/phase5-complete-machine/02-master-rear-isometric.png)
3. [left side](../../generated/drawings/phase5-complete-machine/03-left-side.png)
4. [right side](../../generated/drawings/phase5-complete-machine/04-right-side.png)
5. [top](../../generated/drawings/phase5-complete-machine/05-top.png)
6. [front](../../generated/drawings/phase5-complete-machine/06-front.png)
7. [rear](../../generated/drawings/phase5-complete-machine/07-rear.png)
8. [base and Y detail](../../generated/drawings/phase5-complete-machine/08-base-y-detail.png)
9. [gantry and X detail](../../generated/drawings/phase5-complete-machine/09-gantry-x-detail.png)
10. [X/Z/spindle detail](../../generated/drawings/phase5-complete-machine/10-xz-spindle-detail.png)
11. [electronics and service](../../generated/drawings/phase5-complete-machine/11-electronics-detail.png)
12. [PCB and workholding](../../generated/drawings/phase5-complete-machine/12-workholding-detail.png)
13. [exploded assembly](../../generated/drawings/phase5-complete-machine/13-exploded-assembly.png)
14. [printed parts only](../../generated/drawings/phase5-complete-machine/14-printed-parts-only.png)
15. [hardware only](../../generated/drawings/phase5-complete-machine/15-hardware-only.png)
16. [motion extremes](../../generated/drawings/phase5-complete-machine/16-motion-extremes.png)

Exploded and subsystem views intentionally offset or filter components. Use
the master isometric/front/rear/top views and the support-audit table when
judging whether a component is physically supported.

## Automated result

The blocking checks pass for the current virtual batch:

- declared structural inventory and single-solid/320 mm checks;
- complete assembly names, uniqueness, support/fastening records, and master
  shape validity;
- exact BRep structural overlap classification;
- eight X/Y/Z travel corners, including spindle/gantry, bed/gantry,
  Y-end-support, Z-motor registration, and Z-motor/gantry screens;
- non-empty STL/STEP derivatives.

The report remains `not-ready` by design. Physical printability, measured
hardware fit, PETG creep/joint evidence, rail alignment, controller/driver
identification, spindle runout, cable bend radius, homing, and commissioning
are still open. No part is `HARDWARE-VALIDATED` or `RELEASED`.

## Owner review decision

This package is ready for owner structural review of the complete virtual
machine and its derived printable candidates. It is not authorization to
print the superseded STL set or to manufacture/release the current candidates
without the measurement and physical-evidence gates.

See the [hardware model register](hardware-model-register.md),
[persistent hardware library](../../cad/library/README.md),
[support audit](master-assembly-support-audit.md),
[assembly guide](../../docs/assembly/assembly-guide.md), and
[EDR-016](../decisions/016-phase-5-master-assembly-first-redesign.md).
