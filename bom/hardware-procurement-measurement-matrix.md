# Hardware procurement / measurement BOM matrix

**Status:** active characterization BOM; not a production purchasing release
**Baseline:** owner-accepted preliminary Phase 4/4A O2 architecture
**Detail:** [hardware procurement / measurement freeze](../requirements/hardware-procurement-measurement-freeze.md)

This is the short purchase-order view. The linked requirement document is the
controlling record for dimensions, tolerances, drawing sufficiency, physical
measurement methods, coupons, and release gates.

## Immediate action matrix

| Action | Quantity | Item | Purchase/measurement boundary |
| --- | ---: | --- | --- |
| **A - BUY NOW** | 1 spool or qualified stock | Process-matched PETG | For conditioned print, rail-seat, joint, insert, and bed coupons only. |
| **A - BUY NOW if absent** | 1 set | Caliper, square, straightedge, feeler/thread gauges, multimeter | Basic inspection; record resolution and zero check. |
| **A - BUY NOW if absent** | 1 set | <=0.005 mm readable dial indicator and rigid/magnetic base | Rail parallelism, screw runout, backlash, and simple 5 N deflection test. |
| **A - BUY NOW if absent** | 1 set | 0.510 kg known mass or verified 5 N spring scale plus rigid fixture | Simple static load; no specialized force metrology assumed. |
| **B - BUY SAMPLE NOW** | 2 rails + 4 blocks | X MGN12/MGN12H, 340 mm reference | Complete X characterization set; use exact length only with a valid drawing, otherwise nearest longer standard length retained uncut. |
| **B - BUY SAMPLE NOW** | 2 rails + 4 blocks | Y MGN12/MGN12H, 310 mm reference | Complete Y characterization set; retain longer rail if exact length is unavailable. |
| **B - BUY SAMPLE NOW** | 2 rails + 4 blocks | Z MGN9/MGN9H, 130 mm reference | Complete Z characterization set; retain longer rail if exact length is unavailable. |
| **B - BUY SAMPLE NOW** | 1 | X T8x4 screw, 360 mm finished/reference; blank >=400 mm if machining | Measure lead/pitch/starts, runout, journals, nut fit; do not cut before datum review. |
| **B - BUY SAMPLE NOW** | 1 | Y T8x4 screw, 330 mm finished/reference; blank >=370 mm if machining | Same measurement and post-processing boundary as X. |
| **B - BUY SAMPLE NOW** | 1 | Z T8x2 screw, 145 mm finished/reference; blank >=180 mm if machining | Add gravity-hold and power-off descent test. |
| **B - BUY SAMPLE NOW** | 2 minimum + candidates | X/Y adjustable split-brass or dual-brass nuts | Target <=0.030 mm backlash; test polymer and standard-brass controls only. |
| **B - BUY SAMPLE NOW** | 1 minimum + candidate | Z adjustable/spring anti-backlash nut | Test drag, gravity hold, preload retention, and cycling. |
| **B - BUY SAMPLE NOW** | 3 axis sets | Fixed 8 mm supports: paired angular-contact sample or documented BK08-class sample | Fixed end constrains screw axially both directions in a replaceable cartridge. |
| **B - BUY SAMPLE NOW** | 3 | Floating 8 mm radial supports: BF08-class-style sample | Radial support only; axial thermal float required. |
| **B - BUY SAMPLE NOW** | 3 + alternatives | 5 mm motor to measured screw-journal couplers | Helical first; Oldham comparison; jaw only if measured. Coupler is torque-only. |
| **B - BUY SAMPLE NOW** | 20 per candidate family/size | M3 heat-set inserts | Measure OD/length/taper/thread depth; coupon before pocket geometry. |
| **B - BUY SAMPLE NOW** | 20 per candidate family/size | M4 heat-set inserts | Default structural/module sample; coupon before pocket geometry. |
| **B - BUY SAMPLE NOW** | 10 per candidate family/size | M5 heat-set inserts | Conditional sample only; no default M5 interface. |
| **B - BUY SAMPLE NOW** | 100 / 50 / 10 mixed | M3 / M4 / M5 socket-head sample screws | No final lengths; M5 is conditional. Add washers/nuts only for justified joints. |
| **B - BUY SAMPLE NOW** | 3 + 1 | Limit switches and conductive probe sample | Measure actuation, repeatability, connector/cable envelope, and fault response. |
| **B - BUY SAMPLE NOW** | 1 each | 230 x 180 x 12 MDF and comparison surfaced board if needed | Process samples; measure flatness after skim and workholding load. |
| **D - MEASURE EXISTING** | At least 3 candidates plus spares | **OWNER-SUPPLIED NEMA17 motor stock — DO NOT BUY** | Use a generic 42.3 mm mounting interface, screening 5 mm shaft, and 40-48 mm body envelope with rear connector/wiring access. Identify and assign by measured evidence. |
| **D - MEASURE EXISTING** | 1 assembly | **OWNER-SUPPLIED Arduino Mega + CNC Shield — DO NOT REPLACE absent a validated limitation** | Identify exact Shield revision, installed driver modules, microsteps, motor-current/supply capability, cooling, limits, probe, spindle PWM/control, and GRBL-compatible firmware/configuration. |
| **C - WAIT** | 1 eventual | Final spindle, collets, and PCB tools | Select against 10-30 krpm, <=0.010 mm TIR target, 50-150 W, 0.30-0.80 kg, and diameter classes; 52 mm is only a screen. |
| **C - WAIT** | 1 eventual + spare | Final workholding, vacuum/tape/registration, production spoilboard | Requires board datum, flatness, clamp distortion, probing, and outline-cut validation. |
| **C - WAIT** | 19 parts | Production O2 PETG structural parts | No production print until measured hardware, coupons, service mock-up, and 5 N test pass. |
| **C - WAIT** | As required | Conditional replacement hardware, final feet, cable routing, enclosure, guards | No motor/controller replacement is recommended now; consider replacement only if later electrical or motion validation identifies an actual limitation. |

## Accepted axis quantities and target references

| Axis | Rail/carriage quantity | Target rail | Screw quantity/specification | Target screw reference |
| --- | --- | --- | --- | --- |
| X | 2 x MGN12 rail, 4 x MGN12H carriage | 340 mm | 1 x T8x4 | 360 mm finished/reference |
| Y | 2 x MGN12 rail, 4 x MGN12H carriage | 310 mm | 1 x T8x4 | 330 mm finished/reference |
| Z | 2 x MGN9 rail, 4 x MGN9H carriage | 130 mm | 1 x T8x2 | 145 mm finished/reference |

`T8x4` and `T8x2` specify lead, not pitch or starts. Record all three from
the supplier and from the sample. The screw interface is not manufacturing-
ready until the selected journal/end machining is measured.

## Owner-supplied hardware boundary

The owner has a large selection of 3D-printer NEMA17 motors and an intended
**Arduino Mega + CNC Shield** controller platform. This matrix does not
authorize a motor purchase or controller replacement. The preliminary CAD
interface remains standardized around the common 42.3 mm NEMA17 mounting
square, a screening 5 mm shaft, and a 40-48 mm body envelope. Motor pockets
must preserve rear connector, wiring bend, strain-relief, and service access
for multiple body lengths; the exact clearance is measured from representative
stock before manufacturing release.

Final motor assignment is evidence-based: normal suitable owner stock for X/Y
and the strongest electrically compatible stock for Z. The exact Shield
revision and installed driver carriers are the only controller platform
identity items still unresolved; microstep support, current/voltage capacity,
cooling, I/O, and GRBL-compatible firmware behavior remain verification items.

## Preliminary interface strategy

- X/Y nuts: adjustable split brass or dual-brass preload, selected by measured
  backlash/drag/cycle results; Z adds a gravity-hold test.
- Fixed screw end: paired 8 mm angular-contact bearings or a documented
  BK08-class pair in a replaceable cartridge. Floating end: 8 mm radial
  bearing with axial float, BF08-class envelope.
- Couplers: compact 5 mm-to-measured-journal helical sample first, Oldham
  comparison; no jaw default. No coupler or motor bearing carries screw thrust.
- Fasteners: M3 rail/accessory, M4 general structural/module, M5 only with a
  written load/creep/preload justification and an independent geometric shear
  path. Final lengths remain open.

## Stop conditions

Do not convert this matrix into a production BOM or release structural CAD if
any of these are missing:

- actual rail/block dimensions, preload/play, hole stations, and rail-seat
  alignment evidence;
- screw lead/pitch/starts, runout, journals, nut backlash and drag evidence;
- fixed/floating bearing axial behavior and coupler axial-parasitic-force
  evidence;
- owned-motor and controller identification sheets;
- measured insert families and passed PETG coupons;
- measured spindle/tool TIR, mass, centerline, thermal/cable envelope, and
  controller compatibility;
- full-travel/service mock-up, spoilboard/workholding datum evidence, and the
  separated 5 N physical force-loop result.

No row above marks an interface manufacturing-ready. The owner-authorized
Phase 5 base-pair candidate does not close this measurement matrix; production
CAD and hardware-dependent fit remain not-ready.
