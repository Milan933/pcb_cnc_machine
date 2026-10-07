# Phase 5 master-assembly BOM and procurement boundary

Status: virtual-machine review BOM; not a production purchasing release.

The active master contains 20 derived PETG structural parts. The inventory
and local dimensions are generated in
[`phase5-complete-machine-manifest.json`](../docs/manufacturing/phase5-complete-machine-manifest.json).
Source/confidence/reuse status for reference hardware is in the
[hardware model register](../docs/manufacturing/hardware-model-register.md).

## Printed PETG candidate inventory

| Qty | Part | Role | Maturity |
| ---: | --- | --- | --- |
| 1 | PCNC-P001 `base_left_integrated` | left base/Y rail/tower load path | PROTOTYPE-STL |
| 1 | PCNC-P002 `base_right_integrated` | right base/Y rail/tower load path | PROTOTYPE-STL |
| 1 | PCNC-P003 `base_center_tie` | indexed base shear tie | PROTOTYPE-STL |
| 1 | PCNC-P004 `y_motor_service_pocket` | low Y motor/coupler service mount | PROTOTYPE-STL |
| 1 | PCNC-P005 `y_fixed_bearing_cartridge` | low fixed Y bearing housing | PROTOTYPE-STL |
| 1 | PCNC-P006 `y_floating_bearing_cartridge` | low floating Y bearing housing | PROTOTYPE-STL |
| 1 | PCNC-P007 `y_rear_bearing_bridge` | rear floating-bearing support bridge | PROTOTYPE-STL |
| 4 | PCNC-P008..P011 machine feet | leveling/support interfaces | PROTOTYPE-STL |
| 1 | PCNC-P012 `electronics_mount_rail` | controller/cable service rail | PROTOTYPE-STL |
| 1 | PCNC-P013 `gantry_left_integrated` | left tower/X beam segment | PROTOTYPE-STL |
| 1 | PCNC-P014 `gantry_right_integrated` | right tower/X beam socket segment | PROTOTYPE-STL |
| 2 | PCNC-P015/P016 X bearing cartridges | X screw supports | PROTOTYPE-STL |
| 1 | PCNC-P017 `x_z_backbone` | X carriage and Z guide backbone | PROTOTYPE-STL |
| 1 | PCNC-P018 `z_carriage_plate` | moving Z/spindle interface | PROTOTYPE-STL |
| 1 | PCNC-P019 `spindle_mount_concept` | modular spindle clamp | PROTOTYPE-STL |
| 1 | PCNC-P020 `moving_bed_frame` | moving Y bed, carriages, and nut frame | PROTOTYPE-STL |

All parts are local parametric solids with
`PROVISIONAL_HARDWARE_DIMENSION` interfaces. Their generated STEP/STL files
are candidate review artifacts, not manufacturing release files.

## Owner-supplied hardware - do not buy

| Item | Status and use |
| --- | --- |
| Existing NEMA17 motor stock | **OWNER-SUPPLIED - DO NOT BUY.** Use the generic 42.3 mm frame, approximately 31 mm mounting pitch, screening 5 mm shaft, 40-48 mm body, and rear connector/wiring envelope. Characterize stock before X/Y/Z assignment. |
| Arduino Mega + CNC Shield | **OWNER-SUPPLIED - DO NOT REPLACE** absent a validated technical limitation. Exact Shield revision and installed drivers remain unresolved. Verify microsteps, current/voltage capability, cooling, limits, probe, spindle PWM/control, and GRBL-compatible firmware mapping. |
| Voron 2.4 350 printer | Owner print capability; verify actual usable volume and long-axis process limits. |

Final motor strategy: normal suitable owner-stock motors for X/Y, and the
strongest electrically compatible owner-stock motor for Z. Do not infer
holding torque from physical size.

## Reference hardware to identify/measure

| Qty/class | Master representation | Current reference geometry | Measurement gate |
| --- | --- | --- | --- |
| 2 | MGN12 X rails and 4 MGN12H blocks | 330 mm X guide span | section, hole stations, preload/play, straightness, carriage fit |
| 2 | MGN12 Y rails and 4 MGN12H blocks | 310 mm Y rail length | same, including bed parallelism and printed seat/shim plan |
| 2 | MGN9 Z rails and 4 MGN9H blocks | 130 mm Z rail length | height, spacing, preload/play, carriage fit |
| 1 | T8x4 X screw/nut | 310 mm non-helical envelope | lead/pitch/starts, journals, runout, nut/backlash |
| 1 | T8x4 Y screw/nut | 340 mm non-helical envelope | same plus low drive datum and axial stack |
| 1 | T8x2 Z screw/nut | 155 mm non-helical envelope | gravity hold, drag, backlash, fixed/floating support |
| 3 axis sets | 608 fixed/floating bearing arrangements | 8 x 22 x 7 mm class | actual bearing stack, retainers, axial float |
| 3 | 5-to-8 mm couplers | 20 x 30 mm reference envelope | bore, length, set-screw access, axial parasitic force |
| samples | M3/M4 inserts and fasteners | provisional bosses/through interfaces | OD, length, pilot, pull-out, creep, torque, tool access |
| 1 candidate | ER11 spindle | local 45 x 140 mm SycoTec candidate | diameter, mass, length, cable/heat, runout, clamp fit |
| samples | limits, probe, clamps, spoilboard | local service/process envelopes | actuation, repeatability, cable, flatness, distortion, replacement |

No unmeasured row authorizes a production purchase. The exact CNC Shield and
driver modules are identification items, not a recommendation to replace the
owner controller. New stepper motors are not a procurement item.

## Process and safety items after identification

- conditioned PETG for rail-seat, joint, insert, and bed coupons;
- M3/M4 hardware, measured inserts, washers, captive nuts, and strain relief;
- replaceable spoilboard and low-profile PCB registration/workholding;
- shielded motor/limit/probe/spindle-control cable, fusing, emergency-stop,
  spindle inhibit, and protective-earth hardware as required by electrical
  review;
- guards/chip shielding and final enclosure details after thermal and service
  review.

The next action is hardware identification and controlled coupon testing, not
motor purchase, controller replacement, or release of the candidate CAD.
