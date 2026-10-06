# Phase 5 complete-machine manufacturing CAD

**Status:** owner-authorized virtual-machine phase; candidate outputs only

This document extends the first base-pair requirements in
[phase-5-manufacturing-cad.md](phase-5-manufacturing-cad.md). The owner
explicitly opened complete Phase 5 from baseline
`afe2e14089467321b323d74f928a7ab4c5ffdc1f` and directed the project to finish
the coherent virtual machine before physical part review.

## Required outputs

1. A central coordinate, work-origin, travel, envelope, motor, spindle, and
   provisional-interface parameter contract.
2. All 19 accepted O2 structural identities as actual local fused solids with
   real walls, ribs, webs, gussets, rail seats, service openings, and fastening
   interfaces appropriate to each part.
3. A named complete assembly containing the fixed structure, moving bed,
   rails, carriages, screws, nuts, bearings, couplers, motors, spindle,
   workholding, PCB envelope, probe, limits, electronics, cable routes, feet,
   and service clearances.
4. A deterministic eight-corner full-travel check for X/Y/Z and an explicit
   expected-interference register. Critical bed/gantry checks must use exact
   solid intersections when the CAD backend is available, not only an AABB.
5. A stable PCNC-P001 through PCNC-P019 inventory with material, quantity,
   maturity, local print orientation, support strategy, bounding box, mass
   estimate, interfaces, and local STL/STEP paths.
6. Individual STL/STEP derivatives and a complete assembly STEP plus a
   visualization STL under ignored `generated/` development paths.
7. Twelve review images, a 30-step or more assembly guide, coordinate/datum
   instructions, alignment procedures, preliminary fastener schedule, wiring
   architecture, BOM categories, and a risk/open-item review package.

## Fixed architecture and hardware assumptions

- fixed gantry, moving Y bed, 200 x 150 mm PCB work area;
- dual MGN12-class X/Y guides, dual MGN9-class Z guides;
- T8x4 X/Y and T8x2 Z screening screw classes;
- owner-supplied NEMA17 stock, generic 42.3 mm frame, 5 mm shaft screening,
  40–48 mm body envelope and rear connector clearance;
- owner-supplied Arduino Mega + CNC Shield; exact shield revision and drivers
  remain unresolved and no replacement is assumed;
- spindle 10–30 krpm screening, practical 12–26 krpm, ER11 preferred,
  25/40/52 mm body classes and 0.30–0.80 kg screening mass.

## Maturity and release rules

Complete geometry may be test-printed and sliced while an interface is marked
`PROVISIONAL_HARDWARE_DIMENSION`. That status blocks `HARDWARE-VALIDATED` and
`RELEASED` maturity. Physical print inspection, measured hardware fit,
alignment, PETG process coupons, electrical identification, service mock-up,
and commissioning evidence are separate gates.

Development outputs remain outside `generated/*/release/`. A later release
must have a source revision, measured interface records, validation report,
owner review disposition, and explicit release authorization.
