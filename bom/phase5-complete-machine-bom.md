# Phase 5 complete-machine BOM and procurement boundary

Status: virtual-machine review BOM; not a production purchasing release.

The complete model contains 19 printed PETG structural parts. Exact rail,
screw, bearing, insert, spindle, shield, and driver interfaces remain
provisional. The owner’s motors and controller are explicitly not purchase
items.

## PRINTED — PETG

| Qty | Part number | Part ID | Role | Maturity |
| ---: | --- | --- | --- | --- |
| 1 | PCNC-P001 | `base_left_integrated` | left base/Y rail/tower load path | PROTOTYPE-STL |
| 1 | PCNC-P002 | `base_right_integrated` | right base/Y rail/tower load path | PROTOTYPE-STL |
| 1 | PCNC-P003 | `base_center_tie` | transverse base shear tie | PROTOTYPE-STL |
| 1 | PCNC-P004 | `y_motor_service_pocket` | Y motor/coupler service mount | PROTOTYPE-STL |
| 1 | PCNC-P005 | `y_fixed_bearing_cartridge` | Y fixed bearing support | PROTOTYPE-STL |
| 1 | PCNC-P006 | `y_floating_bearing_cartridge` | Y floating bearing support | PROTOTYPE-STL |
| 4 | PCNC-P007..P010 | machine feet | leveling/support interfaces | PROTOTYPE-STL |
| 1 | PCNC-P011 | `electronics_mount_rail` | controller/cable service rail | PROTOTYPE-STL |
| 1 | PCNC-P012 | `gantry_left_integrated` | left tower/X beam segment | PROTOTYPE-STL |
| 1 | PCNC-P013 | `gantry_right_integrated` | right tower/X beam socket segment | PROTOTYPE-STL |
| 2 | PCNC-P014/P015 | X bearing cartridges | X screw supports | PROTOTYPE-STL |
| 1 | PCNC-P016 | `x_z_backbone` | X carriage and Z guide backbone | PROTOTYPE-STL |
| 1 | PCNC-P017 | `z_carriage_plate` | moving Z/spindle interface | PROTOTYPE-STL |
| 1 | PCNC-P018 | `spindle_mount_concept` | modular spindle clamp | PROTOTYPE-STL |
| 1 | PCNC-P019 | `moving_bed_frame` | moving Y bed and nut/carriage frame | PROTOTYPE-STL |

The current solid-equivalent estimate from the CAD volumes is approximately
5.72 kg at the documented PETG density. This is not a printed mass claim:
slicer infill, shells, modifiers, supports, process waste, and inserts will
change the actual result.

## OWNER-SUPPLIED — DO NOT BUY

| Qty | Item | Use / identification status |
| ---: | --- | --- |
| stock selection | NEMA17 stepper motors | Use existing stock. Screen generic 42.3 mm frame, 5 mm shaft, 40–48 mm body envelope; characterize candidates before final X/Y/Z assignment. |
| 1 | Arduino Mega + CNC Shield | Intended controller platform. Identify exact shield revision, installed drivers, microsteps, current/voltage/cooling, inputs/outputs, and firmware mapping. Do not replace absent a validated limitation. |
| 1 | Voron 2.4 350 printer | Owner print capability; confirm usable volume and process settings. |

## BUY AFTER MEASUREMENT — motion and interfaces

| Qty / class | Item | Measurement gate |
| --- | --- | --- |
| 2 | MGN12-class X rails, approximately 340 mm | width, hole pitch, height, preload, straightness, end margin |
| 2 | MGN12-class Y rails, approximately 310 mm | same; full parallelism and printed seat/shim plan |
| 4 | MGN12H X carriage blocks | measured body and mounting pattern |
| 4 | MGN12H Y carriage blocks | measured body and mounting pattern |
| 2 | MGN9-class Z rails, approximately 130 mm | rail/block height and spacing |
| 4 | MGN9H Z carriage blocks | measured body and mounting pattern |
| 1 | T8x4 X screw and nut | straightness, nut envelope, backlash, service stack |
| 1 | T8x4 Y screw and nut | same |
| 1 | T8x2 Z screw and nut | same; axial load and nut alignment |
| 3 | fixed/floating bearing sets | bore, flange, axial-float arrangement |
| 3 | flexible 5-to-8 mm couplers | bores, length, set-screw access, axial clearance |
| sample set | M3/M4 inserts and screws | OD, length, pilot, insertion depth, pull-out, creep, torque, tool access |
| sample set | feet, washers, leveling/support hardware | grip, table interface, adjustment and access |
| 1 representative | spindle / controller | diameter, mass, length, ER11/tooling, cable exit, heat, runout and clamp interface |

## BUY AFTER MEASUREMENT — process and safety

- replaceable 230 x 180 x 12 mm spoilboard stock and mounting hardware;
- PCB registration, low-profile clamps, or vacuum/workholding hardware;
- normally-closed limit switches, probe hardware, cable, strain relief, and
  drag/service-loop components;
- suitable motor/spindle power supplies, fusing, emergency stop, and guarded
  spindle control components after electrical review;
- hardware-specific printed inserts/standoffs only after the actual insert and
  controller board geometry is measured.

## OPTIONAL

- removable rail shim/reference strips;
- sacrificial bed skins and calibration coupons;
- spindle guard or chip shield after thermal and visibility review;
- additional probe fixture or removable PCB registration frame;
- cable-chain hardware if the free-loop design is not sufficient.

No category above authorizes a production order for unmeasured hardware. The
next procurement action is identification and measurement, not motor purchase
or controller replacement.
