# Phase 4 preliminary structural BOM boundary

**Status:** review and measurement list; not a production purchasing release

This BOM follows the owner-accepted P2 packaging and Phase 4 structural
concept. It deliberately separates low-risk items that can be bought for
measurement/coupon work from items that must wait for exact dimensions,
physical evidence, or owner acceptance. Reference envelopes are not vendor
specifications.

## Safe to purchase now for measurement, coupons, or controlled review

| Quantity | Item / class | Status | Why it is safe now | Notes |
| ---: | --- | --- | --- | --- |
| 1 spool or existing stock | PETG filament matching the printer process | Safe for coupons | Required to condition printed beam, rail-seat, insert, bearing-pocket, and bed coupons. | Record brand, color, lot, drying/conditioning, nozzle, layer height, and perimeter policy. |
| 1 sample set | MGN12-class rail and long blocks, nominal X/Y class | Sample/measure | The motion class is owner-accepted and needed to measure rail, block, hole, and seat interfaces. | Do not order production lengths or assume clone tolerances. Measure X 340 mm and Y 310 mm candidates. |
| 1 sample set | MGN9-class rail and long blocks, nominal Z class | Sample/measure | The short-Z class is owner-accepted for the review baseline. | Measure 130 mm candidate, play, preload, mounting faces, and fallback MGN12 need. |
| 1 sample each | T8x4 and T8x2 screw/nut samples | Sample/measure | Lead classes are owner-accepted and samples are needed for straightness, nut fit, and backlash screening. | Production cut lengths remain 360/330/145 mm nominal until measurement. |
| 1 set each | 8 mm fixed and floating bearing samples | Sample/measure | Fixed/floating topology is owner-accepted and cartridges require actual envelope data. | Exact BK/BF/angular-contact supplier and fit remain open. |
| 1 each | 5-to-8 mm flexible coupler samples | Sample/measure | Direct torque-only coupling is the accepted interface rule. | Confirm bore, length, set-screw access, and axial clearance. |
| 1 sample set | M3 and M4 heat-set inserts, representative lengths | Coupon/measure | M3/M4 are the default interface classes. | Measure OD, length, pilot, insertion depth, tool access, pull-out, torque, creep, and repeated assembly. |
| as needed | Fastener samples M3/M4, washers, and selective through-bolt samples | Coupon/measure | Needed to validate clamp access and geometric shear interfaces. | M5 is not a default purchase; justify only after load-path evidence. |
| existing set | Owned NEMA17 motors | Existing/measure | The owner already has motors and must identify/measure them before final pockets. | Record model, shaft, length, current, torque, and condition. Do not buy replacements yet. |
| existing set | Owned controller / Arduino CNC Shield / GRBL hardware | Existing/measure | Needed for interface and service review. | Record shield revision, driver carriers, firmware, supply, limit/probe/PWM behavior. |
| 1 sample | Generic low-profile workholding and spoilboard material | Process sample | Needed to review the 230 x 180 bed datum and replacement workflow. | Do not freeze vacuum perimeter or final clamp pattern. |

## Wait for measurement, owner review, or physical evidence

| Item / class | Wait condition | Reason |
| --- | --- | --- |
| Production MGN12/MGN9 rail and carriage quantities | Sample measurement and Phase 4 owner review | Exact supplier, preload, straightness, hole pattern, and rail-seat fit are unresolved. |
| Production T8x4/T8x2 screw lengths, end machining, and nuts | Straightness, critical-speed, backlash, drag, and service review | Nominal 360/330/145 mm values are packaging screens, not purchase dimensions. |
| Fixed-end paired axial/angular-contact supports | Bearing sample fit and axial-load review | The fixed end must carry screw thrust; supplier envelopes and preload are open. |
| Floating radial bearing supports | Sample fit and axial-float review | Both screw ends must not be axially constrained. |
| Production NEMA17 motors or replacement motors | Identification of the owned motors and torque/current test | The mechanical envelope alone does not prove torque or connector compatibility. |
| Spindle and ER11/tooling | Spindle diameter, mass, runout, cable exit, cooling, and thermal measurement | The 52 mm mount is a maximum screening envelope, not a selected spindle. |
| Limit switches, probe hardware, and cable chains | Electrical/interface and full-travel service mock-up | Switch type, probe datum, cable drag, and fault response remain open. |
| M5 inserts or through-bolts | Load, creep, preload, moment, and failure-consequence justification | M5 and through-bolts are selective escalations, not defaults. |
| Printed production parts | EDR-011 acceptance, measured hardware, coupons, and manufacturing review | Current 29 parts are PRELIMINARY review geometry only. |
| Final spoilboard, clamp, or vacuum hardware | Workholding distortion and PCB process trial | P2 has a replaceable spoilboard concept but no final workholding release. |
| Controller/driver production wiring and enclosure | Bench I/O, cooling, noise, homing, probe, and spindle-control tests | Existing hardware is not yet identified or electrically accepted. |

## Printed concept inventory

The current review assembly contains 29 structural concept parts: 17 base/
service parts, 6 gantry/X parts, 5 X/Z/spindle parts, and 1 moving-bed frame.
Their exact IDs, nominal and actual review bounding boxes, print orientations,
and process notes are generated by `tools/run_phase4_preliminary_study.py`.
No part is manufacturing-ready, and no STEP/STL file from the review runner is
placed under `generated/*/release/`.

## Purchase gate

Before a production BOM is issued, record supplier identities, quantities,
actual dimensions, price/availability, tolerances, acceptance measurements,
and the decision record that justifies each dependency. The production BOM is
blocked by unresolved spindle/motor/controller/rail/screw/bearing/insert data,
PETG coupon evidence, service mock-up, and owner acceptance of EDR-011.
