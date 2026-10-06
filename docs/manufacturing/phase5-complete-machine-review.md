# Phase 5 complete virtual-machine owner review package

Status: generated review candidate; overall maturity `PROTOTYPE-STL`.

This package converts the accepted Phase 4A O2 architecture into a coherent
virtual fixed-gantry PCB CNC machine. It is intentionally complete before the
physical first-part review, but it is not a hardware-validated or released
machine.

## What is being reviewed

- fixed gantry with a moving Y bed;
- 19 actual fused PETG structural solids, inventoried as PCNC-P001 through
  PCNC-P019;
- dual MGN12-class X/Y guide envelopes, dual MGN9-class Z guide envelopes,
  T8x4 X/Y and T8x2 Z screw envelopes;
- nominal 200 x 150 mm PCB area, 220 x 170 x 40 mm tool-point screening travel;
- parametric NEMA17 motor envelope and owner-stock motor strategy;
- owner Arduino Mega + CNC Shield controller envelope, without inventing its
  shield revision or driver pinout;
- replaceable spoilboard, workholding, conductive probe, limits, service loops,
  and electronics mounting space;
- ordered assembly guide, coordinate system, preliminary fastener schedule,
  wiring architecture, BOM, and local export manifest.

## Dimensions and inventory

| Item | Current virtual-CAD value | Status |
| --- | ---: | --- |
| Master service-envelope X/Y/Z | 479 x 475 x 273 mm | calculated from virtual envelopes |
| PCB work area | 200 x 150 mm | accepted screening requirement |
| Tool-point travel | 220 x 170 x 40 mm | preliminary packaging target |
| Spoilboard | 230 x 180 x 12 mm | provisional purchased interface |
| Printable structural parts | 19 | controlled inventory |
| Master components | 70 | 19 printed + 51 hardware/process envelopes |
| PETG solid-equivalent estimate | approximately 5.72 kg | calculated; not slicer mass |
| Motor interface | 42.3 mm NEMA17 class, 5 mm shaft screen, 40–48 mm body | owner-stock screening assumption |
| Spindle screen | 25/40/52 mm body classes, 0.30–0.80 kg | provisional envelope |

The solid-equivalent PETG estimate is higher than the earlier Phase 4A
analytical printed-mass range because this pass measures the CAD solids at a
nominal material density. It must not be read as expected slicer mass or as a
structural-performance result.

## Files and review views

The generator command is:

```text
C:\Users\milan\pcbCNC-cad-env\Scripts\python.exe -m tools.generate_phase5_complete_machine
```

The generated files are local development artifacts under
`generated/stl/phase5-complete-machine/`,
`generated/step/phase5-complete-machine/`, and
`generated/drawings/phase5-complete-machine/`. The tracked manifest is
[phase5-complete-machine-manifest.json](phase5-complete-machine-manifest.json).

Review the 19 individual STL files in OrcaSlicer, then inspect these views:

1. [complete front isometric](../../generated/drawings/phase5-complete-machine/01-complete-front-isometric.png)
2. [complete rear isometric](../../generated/drawings/phase5-complete-machine/02-complete-rear-isometric.png)
3. [top](../../generated/drawings/phase5-complete-machine/03-top.png)
4. [front](../../generated/drawings/phase5-complete-machine/04-front.png)
5. [side](../../generated/drawings/phase5-complete-machine/05-side.png)
6. [exploded machine](../../generated/drawings/phase5-complete-machine/06-exploded-machine.png)
7. [exploded base/Y](../../generated/drawings/phase5-complete-machine/07-exploded-base-y.png)
8. [exploded gantry/X](../../generated/drawings/phase5-complete-machine/08-exploded-gantry-x.png)
9. [exploded Z/spindle](../../generated/drawings/phase5-complete-machine/09-exploded-z-spindle.png)
10. [electronics and cable service](../../generated/drawings/phase5-complete-machine/10-electronics-cable.png)
11. [PCB and workholding](../../generated/drawings/phase5-complete-machine/11-pcb-workholding.png)
12. [motion envelope](../../generated/drawings/phase5-complete-machine/12-motion-envelope.png)

## Validation result

The complete batch passed the blocking automated checks:

- exact 19-part inventory;
- valid single-solid structural candidates;
- conservative 320 mm print-envelope check;
- complete named assembly with master STEP/STL derivatives;
- classified nominal structural overlap screen;
- eight-corner X/Y/Z travel screen, including exact BRep checks for the
  critical bed/gantry cases;
- local file generation and non-empty export checks.

The overall report remains `not-ready` because the following are intentionally
open:

- physical printability, dimensional inspection, PETG creep and joint tests;
- measured rail, screw, bearing, coupler, insert, foot, and spindle interfaces;
- exact CNC Shield revision, installed drivers, microsteps, current, voltage,
  cooling, limits, probe, spindle output, and GRBL-compatible mapping;
- representative owner NEMA17 characterization and final axis assignment;
- exact cable bend radius, connector placement, and electrical safety review;
- rail alignment, gantry squareness, bed leveling, spindle tram, and first
  PCB process validation.

## Owner decision prompt

**Do I want to build this?**

If yes, the next controlled action is to review the complete STL/STEP package,
identify and measure the owner hardware, and choose the first physical PETG
coupons/parts. A “yes” to this virtual package does not make the interfaces
released. A “no” should identify the architecture or service issue to revise
before printing.

No part in this package is `HARDWARE-VALIDATED` or `RELEASED`.
