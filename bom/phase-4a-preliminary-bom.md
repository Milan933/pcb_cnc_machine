# Phase 4A preliminary BOM and hardware boundary

**Status:** owner-accepted preliminary O2 architecture; procurement and
measurement list; not a production purchasing release

Phase 4A selects O2 as a preliminary printed-structure candidate. The BOM
change is a part-decomposition change, not a supplier or hardware freeze.
Reference envelopes remain screening geometry.

## Printed O2 concept inventory

| Quantity | Printed part / group | Role | Service boundary |
| ---: | --- | --- | --- |
| 2 | base_left_integrated, base_right_integrated | Integrated base, front/rear perimeter, and Y rail carrier | Structural module; rail datum inspected and shimmed; hardware remains removable |
| 1 | base_center_tie | Transverse base closure and Y-nut relief | Removable center module |
| 3 | y_motor_service_pocket, y_fixed_bearing_cartridge, y_floating_bearing_cartridge | Y motor and fixed/floating screw supports | Replaceable |
| 4 | machine_foot_front_left/right, machine_foot_rear_left/right | Leveling/table interface | Replaceable |
| 1 | electronics_mount_rail | Optional electronics attachment | Optional and serviceable |
| 2 | gantry_left_integrated, gantry_right_integrated | Integrated tower/beam side modules | Structural module; J1 center interface remains |
| 2 | x_fixed_bearing_cartridge, x_floating_bearing_cartridge | X screw support | Replaceable |
| 1 | x_z_backbone | Integrated X carriage/Z support | Printed module; bearings, rails, motor, screw, and coupler remain removable |
| 1 | z_carriage_plate | Moving spindle carriage | Replaceable interface module |
| 1 | spindle_mount_concept | Parametric spindle interface | Replaceable; spindle bore and centerline remain open |
| 1 | moving_bed_frame | Ribbed moving Y bed | Removable from metal carriages; support and spoilboard remain separate |
| **19** | **Total preliminary PETG parts** |  | **All remain PRELIMINARY** |

## Printed before/after boundary

| Baseline group | O2 change | Quantity impact |
| --- | --- | ---: |
| Four front/rear base members, two side members, two Y carriers | Two integrated base/Y modules | 8 -> 2 |
| Two towers and two split beam halves | Two integrated tower/beam modules | 4 -> 2 |
| X carriage, Z fixed support, Z motor service cartridge | One X/Z backbone | 3 -> 1 |
| Moving bed frame | Lighter rib/perimeter geometry | 1 -> 1 |
| Service cartridges, feet, electronics rail, Z carriage, spindle mount, center tie | Retained as modular interfaces | unchanged |

The 29-part Phase 4 baseline therefore becomes 19 O2 review parts. This
does not mean that ten hardware interfaces disappear: rails, carriages,
screws, nuts, bearings, couplers, motors, spindle, limits, probe, cables,
feet, and spoilboard still need access and fit evidence.

## Superseded by the hardware freeze

The detailed A-D matrix, per-component dimensions, identification sheets,
measurement methods, and physical-test gates are now controlled by
[hardware-procurement-measurement-matrix.md](hardware-procurement-measurement-matrix.md)
and the linked [requirements freeze](../requirements/hardware-procurement-measurement-freeze.md).
The earlier sample guidance below is retained as the Phase 4A audit trail.

## Safe to purchase or sample for measurement/coupons

| Quantity | Item/class | Reason |
| ---: | --- | --- |
| 1 spool or existing stock | Process-matched PETG | Condition base/Y, gantry, rail-seat, insert, J1, and bed coupons |
| 1 sample set | MGN12-class X/Y rails and blocks | Measure rail width, hole pitch, block height, preload, and seat fit |
| 1 sample set | MGN9-class Z rails and blocks | Measure the compact Z interface and block access |
| 1 sample each | T8x4 and T8x2 screw/nut samples | Measure straightness, nut envelope, backlash, drag, and service access |
| 1 set each | Fixed and floating 8 mm bearing samples | Validate cartridge envelopes and axial-float strategy |
| 1 each | Flexible 5-to-8 mm coupler samples | Validate bore, length, set-screw access, and axial clearance |
| 1 sample set | M3 and M4 inserts and fasteners | Measure OD, length, pilot, insertion depth, pull-out, torque, creep, and repeated service |
| Existing stock/platform | **OWNER-SUPPLIED NEMA17 motors — DO NOT BUY; OWNER-SUPPLIED Arduino Mega + CNC Shield — DO NOT REPLACE absent a validated limitation** | Use generic NEMA17 preliminary CAD interfaces; identify motor stock, exact Shield revision, installed drivers, microsteps, current/voltage capability, cooling, limits, probe, spindle PWM/control, and GRBL-compatible firmware/configuration |
| 1 sample | Spindle or representative mount envelope | Measure diameter, mass, centerline, cable exit, heat, and clamp requirements |

## Wait for measurement, owner review, or physical evidence

| Item/class | Wait condition |
| --- | --- |
| Production rails, blocks, screws, nuts, bearings, couplers | Sample measurement and full-travel service mock-up |
| Production motor purchases or replacement motors | No motor purchase; consider replacement only if later validation identifies an actual limitation |
| Spindle and final clamp | Actual diameter, mass, runout, cable/thermal envelope, and centerline |
| Insert-specific bosses and pockets | Actual insert data plus PETG pull-out, creep, preload, and service coupons |
| M5 inserts or through-bolts | Documented load, moment, creep, and failure-consequence justification |
| Final printed parts | Owner acceptance, measured hardware, coupons, datum inspection, and manufacturing review |
| Spoilboard, clamps, vacuum, probe, limits, cable routing | Process and full-travel/workholding validation |

## Interface rules carried forward

- M3 is the default rail and accessory class.
- M4 is the default general structural/module class.
- M5 is conditional and is not a default purchase.
- Fasteners supply clamp preload; printed shoulders, keys, pockets, tongues,
  and mating faces supply location and shear.
- Actual insert OD, length, pilot, wall, edge distance, tool access, and
  installation direction remain unresolved.

No row in this document authorizes a production purchase order or a
manufacturing release. Phase 4 and Phase 4A are accepted only as preliminary
architecture; physical evidence, manufacturing interfaces, and Phase 5 remain
closed.
