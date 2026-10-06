# Phase 4A structural optimization - owner-review package

**Status:** owner-accepted preliminary O2 structural architecture baseline
(2026-10-06); physical validation and manufacturing interface evidence remain
open. The 5 N deflection value is calculated, not measured.
**Selected preliminary candidate:** O2 balanced optimization
**Phase 4 preliminary architecture accepted:** yes
**Phase 4A preliminary architecture accepted:** yes
**Phase 5 started:** no
**Production release:** no

This package uses the completed Phase 4 owner-review package as its baseline.
It implements and compares O1, O2, and O3 in the parametric build123d source,
then validates the selected O2 review assembly against the accepted P2 motion
and packaging references. It does not freeze supplier hardware or convert
review geometry into release geometry.

The source implementation is [phase4a_structural.py](../../cad/parts/phase4a_structural.py),
the assembly and overlap graph are in
[phase4a_assembly.py](../../cad/assembly/phase4a_assembly.py), the calculation
screen is in [phase4a_calculations.py](../../cad/phase4a_calculations.py), and
the reproducible runner is
[run_phase4a_optimization.py](../../tools/run_phase4a_optimization.py).

## Executive comparison

| Candidate | Total PETG parts | Critical PETG parts | Primary-loop parts | Primary pair-level joints | CAD mass kg | Estimated installed PETG kg | Bed CAD mass kg | 5 N deflection mm | Largest print |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Phase 4 baseline | 29 | 16 | 17 | 17 | 5.808293 | 3.195-4.357 | 0.354117 | 0.012648 | 28 x 300 x 22 |
| O1 conservative | 27 | 16 | 17 | 17 | 5.822517 | 3.177-4.342 | 0.354117 | 0.011170 | 28 x 300 x 22 |
| **O2 balanced** | **19** | **8** | **9** | **7** | **4.720329** | **2.595-3.539** | **0.267970** | **0.009410** | **150 x 300 x 40.75** |
| O3 aggressive | 10 | 6 | 7 | 5 | 3.033261 | 1.633-2.240 | 0.267970 | 0.008427 | 189 x 300 x 188 |

The CAD mass is a sum of build123d review-solid volumes multiplied by the
central PETG density. The installed-PETG range is a transparent print-bucket
planning estimate, not a slicer result, measured mass, or purchase quantity.
The bed values are the printed frame only; rails, carriages, screws, PCB
support, spoilboard, workholding, and hardware are excluded.

O2 is selected because it removes the most important redundant PETG seams
while retaining replaceable rails, carriages, screws, nuts, bearing
cartridges, motors, spindle mount, feet, electronics rail, and center tie.
It also passes the preferred 0.015 mm preliminary screen and keeps the
largest XY print exactly at the 300 mm preferred boundary. O3 is lighter but
embeds too many alignment and bearing interfaces in two large side modules.
O1 preserves too much of the original joint complexity and does not reduce
the critical-part count.

## 1. The 16 baseline critical structural parts

The Phase 4 baseline critical register is:

1. base_front_left
2. base_front_right
3. base_rear_left
4. base_rear_right
5. base_left_side_member
6. base_right_side_member
7. base_y_rail_carrier_left
8. base_y_rail_carrier_right
9. base_center_tie
10. gantry_tower_left
11. gantry_tower_right
12. gantry_beam_left
13. gantry_beam_right
14. x_carriage_plate
15. z_carriage_plate
16. moving_bed_frame

In O2 these become eight critical printed parts:
base_left_integrated, base_right_integrated, base_center_tie,
gantry_left_integrated, gantry_right_integrated, x_z_backbone,
z_carriage_plate, and moving_bed_frame.

## 2. Primary force loop and joint reduction

The baseline primary printed force loop contains 17 parts:

spindle_mount_concept -> z_carriage_plate -> x_carriage_plate ->
gantry_beam_left/right -> gantry_tower_left/right ->
base_y_rail_carrier_left/right -> base side and front/rear members ->
base_center_tie -> moving_bed_frame.

The O2 force loop contains nine named parts:

spindle_mount_concept, z_carriage_plate, x_z_backbone,
gantry_left_integrated, gantry_right_integrated,
base_left_integrated, base_right_integrated, base_center_tie, and
moving_bed_frame.

The controlled primary pair-level joint screen falls from 17 to 7. It counts
mirrored structural interfaces separately and excludes metal rail, screw,
bearing, and hardware-to-PETG service interfaces. The seven O2 consolidation
interfaces are the two base-module/center-tie contacts, two
base-module/integrated-gantry contacts, two integrated-gantry/XZ-backbone
contacts, and the XZ-backbone/Z-carriage interface. The spindle mount remains
replaceable and is treated as an interface module rather than hidden inside
the X/Z backbone.

The automated expected-overlap register falls from 34 baseline entries to 24
O2 entries. The current baseline geometry produces 33 actual overlap events
because one documented pair has no positive solid overlap; O2 produces 24
actual events, all documented. Neither count is a final fastener or physical
joint count. The Phase 4 baseline physical register contains 28 planned
groups; the Phase 4A physical group count remains open rather than being
invented from the optimized CAD.

## 3. Three best simplification candidates

### Candidate 1 - integrate each base/Y rail side

The four front/rear perimeter members, one side member, and one Y rail
carrier on each side become base_left_integrated and
base_right_integrated. The 150 x 300 mm modules retain the rail datum,
front/rear load loop, service cartridges, feet, and removable center tie.
This is the highest-value simplification because it removes multiple
load-path seams without embedding replaceable hardware.

### Candidate 2 - integrate each tower with its beam half

Each tower and its X torsion-box beam half become gantry_left_integrated or
gantry_right_integrated. The J1 center beam split remains visible and
serviceable. This removes the tower-to-beam PETG joint while retaining the
beam rail pads and the central service interface.

### Candidate 3 - create one coherent X/Z backbone

The X carriage, Z fixed-bearing support, and Z motor service envelope become
x_z_backbone. The Z carriage, spindle mount, rails, screws, bearings,
coupler, and motor remain service targets. This shortens the cutting-force
path and removes two small printed support seams.

The lighter O2 moving bed is a secondary mass refinement: its perimeter,
cross ribs, centered Y-nut boss, and four carriage pads remain explicit, but
unnecessary solid volume is removed.

## 4. Three highest-risk remaining joints/interfaces

1. **J1 center beam split:** the deep tongue/socket still carries the highest
   remaining service-cycle and preload risk. M4 inserts supply clamp preload;
   the printed shoulder and tongue must carry shear and torsion.
2. **300 mm integrated Y rail datum:** the base/Y module is printable on paper
   but conditioning, long-axis curl, shim/skim allowance, parallelism, and
   rail preload are not proven.
3. **XZ backbone to Z carriage/rail datums:** the integrated backbone removes
   seams but concentrates alignment, bearing-support, motor, rail-seat, and
   tool-point moment requirements in one tall printed part.

Dominant uncertainties are not bulk beam bending. The selected screen is
dominated by the assumed equivalent X/Z structure allowance, followed by
interface/rail-seat allowances. The other major uncertainties are PETG
anisotropy and creep, conditioned 300 mm datum stability, actual spindle
centerline and mass, actual rail/bearing/motor dimensions, insert geometry,
and service-tool access after assembly.

## 5. Before-to-after structural result

| Metric | Phase 4 baseline | Selected O2 | Change / interpretation |
| --- | ---: | ---: | --- |
| Named PETG structural parts | 29 | 19 | 10 fewer review parts |
| Critical structural PETG parts | 16 | 8 | 8 fewer; integrated parts carry more responsibility |
| Primary-loop PETG parts | 17 | 9 | 8 fewer |
| Primary pair-level joints | 17 | 7 | 10 fewer in the controlled screen |
| Automated expected overlap entries | 34 | 24 | 10 fewer documented overlap interfaces |
| CAD solid-equivalent mass | 5.808293 kg | 4.720329 kg | -1.087963 kg; mass is secondary |
| Estimated installed PETG | 3.195-4.357 kg | 2.595-3.539 kg | Planning range only |
| Printed bed frame CAD mass | 0.354117 kg | 0.267970 kg | Lighter ribbed frame; complete moving mass remains open |
| 5 N deflection screen | 0.012648 mm | 0.009410 mm | Passes target and preferred target |
| Assembly bounds | 363 x 353 x 275 mm | 363 x 353 x 275 mm | No packaging regression |
| Unexpected structural interferences | 0 | 0 | Automated result |

The O2 preliminary compliance screen is 0.009410 mm at 5 N against a
0.020 mm target, 0.015 mm preferred target, and 0.030 mm acceptance limit.
The result remains preliminary equivalent-section arithmetic, not FEA or
measured deflection.

## 6. Gantry, base, bed, and X/Z changes

### Gantry

The two tower/beam pairs become two integrated side modules. The J1 center
split, beam rail pads, serviceable X bearing cartridges, and P2 X rail
references remain. O2 does not use the O3 one-piece side modules that absorb
the X bearing pockets.

### Base

The eight perimeter/Y-carrier pieces become two 150 x 300 mm integrated
base/Y modules. The center tie, Y motor pocket, fixed/floating Y cartridges,
four feet, and electronics rail remain separate and serviceable. The
integrated modules use a closed-section perimeter plus a continuous rail web;
they do not become a visually solid printed slab.

### Moving bed

The 230 x 180 mm frame remains separate from the P2 bed support and
spoilboard. O2 uses a lighter perimeter and cross-rib arrangement, a
centered 40 x 32 mm Y-nut boss, and four carriage pads. Its CAD
solid-equivalent mass is 0.267970 kg; the complete moving assembly still
requires metal-carriage, screw, support, spoilboard, PCB, and workholding
measurement.

### X/Z

The X carriage, Z fixed support, and Z motor service cartridge become the
90 x 58 x 201 mm x_z_backbone review part. Bearing, motor, coupler, screw,
rail, and spindle hardware remain removable. The z_carriage_plate and
spindle_mount_concept remain separate so the spindle diameter, centerline,
thermal behavior, and clamp access are not frozen prematurely.

## 7. Printability and alignment

The selected largest print is base_left_integrated, with an actual review
bbox of 150 x 300 x 40.75 mm. Its 300 mm Y extent is exactly the preferred
boundary, not a claim that a raw conditioned PETG datum will be accurate.
Required evidence includes diagonal/edge warp inspection, a conditioned
full-size print, supported rail datum strips, skim/shim allowance, parallelism
measurement, and carriage-preload checks.

Every O1/O2/O3 part is <=320 mm in both XY axes. O3's largest module is
189 x 300 x 188 mm; its 300 mm part is why O3 carries a substantially higher
alignment and repair risk even though its analytical deflection is lower.

Review views are generated from the selected O2 assembly:

- [A - complete isometric](phase-4a-review/01-complete-isometric.png)
- [B - front](phase-4a-review/02-front.png)
- [C - side](phase-4a-review/03-side.png)
- [D - top](phase-4a-review/04-top.png)
- [E - exploded structural](phase-4a-review/05-exploded-structural.png)
- [F - force loop](phase-4a-review/06-highlighted-force-loop.png)
- [G - gantry/J1](phase-4a-review/07-gantry-joint-close-up.png)
- [H - Y rail/base](phase-4a-review/08-y-rail-base-close-up.png)
- [I - bed underside](phase-4a-review/09-bed-underside.png)
- [J - X/Z](phase-4a-review/10-z-x-close-up.png)
- [before/after isometric](phase-4a-review/11-before-after-isometric.png)

The tracked view metrics are in
[phase4a-review-metrics.json](phase-4a-review/phase4a-review-metrics.json).

## 8. Serviceability and assembly

O2 preserves the Phase 4/P2 service boundary for motors, fixed and floating
bearing cartridges, T8 screws/nuts, flexible couplers, MGN rails and
carriages, spindle mount, limit switches, probe/wiring, feet, electronics
rail, and replaceable spoilboard. The optimized printed modules themselves
are not yet proven serviceable; the integrated seams are a reason to inspect
and condition the parts before hardware-specific CAD.

The reviewed assembly sequence remains: condition and inspect the base
modules; install feet; fit Y rails, cartridges, screw, motor, and bed;
install the integrated gantry sides and J1 center interface; align X rails
and cartridges; install the X/Z backbone, Z rails, screw supports, motor and
coupler; install the spindle, limits, probe, wiring, electronics, and
spoilboard; then verify full travel, datum, clearance, and service access.

The P2 packaging validator covers the accepted full-travel, rail-length,
screw-length, bed sweep, spindle envelope, motor, limit, and service-footprint
screens. This CAD review does not replace the physical sequence mock-up.

## 9. Hardware and BOM impact

No vendor-specific hardware is frozen. The class baseline remains:

- dual MGN12 X and Y guides, dual MGN9 Z guides and their carriages;
- T8x4 X/Y and T8x2 Z screws with replaceable anti-backlash nuts;
- NEMA17-class motors and flexible 5-to-8 mm couplers;
- fixed and floating bearing topology;
- M3 rail/accessory hardware, M4 general structural/module interfaces, and
  conditional M5 escalation only after load evidence.

The main printed-BOM change is 29 -> 19:

- 8 base perimeter/Y-carrier parts -> 2 integrated base/Y modules;
- 4 tower/beam parts -> 2 integrated gantry modules;
- 3 X/Z support parts -> 1 X/Z backbone;
- 1 bed frame remains, with lighter rib geometry;
- service cartridges, feet, electronics rail, Z carriage, and spindle mount
  remain separate.

Actual rail holes, bearing bores, motor pockets, spindle bore/centerline,
insert OD/length/pilot, fastener access, and supplier dimensions remain open.
See [the preliminary Phase 4A BOM](../../bom/phase-4a-preliminary-bom.md).

## 10. Validation and physical evidence boundary

The selected O2 CAD assembly has:

- P2 full-travel and clearance screen retained;
- model containment retained;
- 19 unique structural parts and the accepted P2 motion/process references;
- all parts within the 320 mm conservative XY print bound;
- 24 documented overlap events and zero unexpected structural interferences;
- non-empty temporary STEP/STL exports for each selected part, the assembly,
  and the J1/J2/J3 study;
- preliminary calculation passing target, preferred target, and acceptance.

Physical validation has **not** been performed. Required next evidence is:
conditioned 300 mm base/Y and integrated gantry coupons, rail-seat datum
inspection, insert and joint creep/pull-out/repeat-service tests, full-travel
service mock-up, measured hardware fit, measured printed and moving-bed mass,
and a separated 5 N tool-point test.

## 11. Gate disposition

**ACCEPT O2 AS THE PRELIMINARY STRUCTURAL ARCHITECTURE BASELINE; DO NOT
AUTHORIZE PRODUCTION CAD OR PHASE 5.**

O2 is the owner-selected baseline because it has the best current combination
of force-loop simplification, critical part/joint reduction, calculated
stiffness screen, serviceability, alignment inspectability, and Voron print
boundary. This acceptance does not turn the calculated deflection into a
measurement, freeze hardware interfaces, or authorize further optimization.
EDR-013 now controls the procurement and measurement transition.
