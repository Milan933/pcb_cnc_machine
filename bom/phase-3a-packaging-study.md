# Phase 3A packaging study material boundary

This is not a Phase 4 production BOM. It lists only sample-characterization
items needed to decide whether the compact packaging envelopes are serviceable.

| Item | Study quantity | Purpose | Status |
| --- | ---: | --- | --- |
| MGN12H-class rail/block sample | 1 representative set per supplier candidate | Verify block length, preload/play, mounting access, and rail-seat envelope | Sample only |
| MGN9H-class rail/block sample | 1 representative set per supplier candidate | Verify short-Z carriage fit and stiffness fallback | Sample only |
| T8x4 screw samples | 1 X/Y length sample per candidate | Measure straightness, root diameter, end machining, nut drag, and whip behavior | Sample only |
| T8x2 screw sample | 1 Z length sample per candidate | Measure gravity-hold, preload, straightness, and end fit | Sample only |
| 8 mm fixed-end bearing options | 1 pair per candidate | Compare paired axial/angular-contact concepts and preload adjustment | Sample only |
| 8 mm floating radial bearing options | 3 | Verify replaceable radial pocket and axial float | Sample only |
| Flexible 5-to-8 mm couplers | 3 | Check coaxial fit and torque-only behavior | Sample only |
| M3/M4 heat-set insert candidate families | Representative coupon set per candidate family | Measure OD, length, pilot, insertion depth, soldering-iron access, pull-out, torque, cracking, creep, and repeated assembly | Characterization only; exact family not selected |
| Conditional M5 insert candidate | Only if a load-path review identifies a justified high-load joint | Compare against M4 insert capacity and selective through-bolt alternative | Do not purchase as a default size |
| Through-bolt/load-spreader samples | Only for documented escalation candidates | Compare insert pull-out/creep/preload/moment/cyclic-load evidence with a geometric shear path | Conditional study only |
| Owner-supplied NEMA17 motors | All available | **Do not buy.** Measure body, shaft, current, torque-at-speed envelope, connector/wiring access, and service fit; use the generic 42.3 mm / 40-48 mm preliminary interface | Identify before manufacturing freeze; exact final motor does not block preliminary structural CAD |
| Owner-supplied Arduino Mega + CNC Shield | 1 platform | **Do not replace absent a validated limitation.** Identify exact Shield revision, installed drivers, microsteps, current/voltage, cooling, limits, probe, spindle PWM/control, and GRBL-compatible configuration | Identify before commissioning and final electrical interfaces |
| Limit/probe switch samples | Representative set | Mock up home/limit access and fault-safe wiring | Open |
| PETG rail-seat/bearing-pocket/motor-pocket/insert-joint coupons | Test set | Measure creep, insert pull-out, preload retention, edge damage, tool access, and service replacement | Required evidence |

No item above authorizes production quantities, final supplier selection, or
detailed printed structural parts. The Phase 4 preliminary BOM now separates
sample/coupon purchases from wait-for-measurement items; production
procurement remains a later release decision.
