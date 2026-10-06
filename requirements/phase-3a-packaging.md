# Phase 3A - compact packaging optimization

**Status:** owner-accepted P2 baseline; physical evidence and Phase 4 review gate remain open

Phase 3A is a packaging review around the owner-accepted Phase 3 motion
classes. P2 is the accepted packaging baseline for Phase 4 preliminary
structural concept work. It does not authorize manufacturing-ready PETG parts,
production STEP/STL, exact hardware purchase, or motion-system class changes.

## Requirements

| ID | Requirement | Evidence status |
| --- | --- | --- |
| REQ-PKG-001 | Preserve Architecture A: fixed gantry with moving Y bed, 200 x 150 mm PCB area, dual rails, two carriages per rail, 60 mm X/Z guide spacing, 220 mm Y guide spacing, T8x4 X/Y, T8x2 Z, and nominal 40 mm Z travel. | Known baseline; calculated packaging variants |
| REQ-PKG-002 | Cover the required working area with a documented tool-point travel allowance. P1/P2 retain 220 x 170 x 40 mm; P3 is conditional at 210 x 160 x 40 mm. | Calculated; P3 needs owner confirmation |
| REQ-PKG-003 | Size every rail from tool travel, the two-block swept group, and both end margins. | Automated calculation and review skeleton |
| REQ-PKG-004 | Keep X/Y/Z screw leads and fixed/floating bearing topology unchanged. Nominal screw lengths may grow to cover the corrected rail/support stack. | Preliminary choice; physical fit remains open |
| REQ-PKG-005 | Keep direct screw drive. X/Y/Z motor pockets may be recessed or inverted only when shaft alignment, cooling, fastener access, and service removal remain possible. No belt drive is introduced. | Review envelope; assembly mock-up required |
| REQ-PKG-006 | Provide a bed study for 240 x 190, 230 x 180, and 220 x 170 mm supports, including PCB margin, guide overhang, full Y sweep, workholding, and future vacuum implications. | Calculated review |
| REQ-PKG-007 | Review compact fixed/floating 8 mm bearing cartridges. The fixed end must react axial screw load; the remote end must float axially. | Packaging study; bearing and PETG coupons required |
| REQ-PKG-008 | Minimize Z height without tall-workpiece capability. Include the bed, spoilboard, PCB, tool/spindle envelope, mount, Z guide/screw supports, motor, Y motor, and gantry references. | Calculated Z stack |
| REQ-PKG-009 | Keep future major PETG packaging prints within the nominal 350 mm Voron volume on paper and document orientation/access risks. | Dimensional screen; print evidence not ready |
| REQ-PKG-010 | Validate all variants for rail sweep, full bed sweep, motor/bearing/bed/spindle/tool/limit containment, unexpected reference collisions, and non-empty review exports. | Automated checks and build123d runner |
| REQ-PKG-011 | Record the current envelope cause, P1/P2/P3 trade, recommendation, forced motion corrections, risks, and open owner decisions in EDR-009. | Proposed decision record |
| REQ-PKG-012 | Apply the owner-directed PETG fastening strategy: heat-set inserts by default, M3/M4/M5 hierarchy, fastener preload separated from printed geometric location/shear transfer, and selective justified through-bolts. | Central parameters, skill rules, and `cad/fastening.py` review checks |
| REQ-PKG-013 | Seat the gantry crossmember mechanically with a tongue-and-groove, stepped socket, keyed pocket, shoulder, or interlocking rib; screws clamp the seat and do not provide sole location. | Review-only interface screen; production geometry and joint evidence remain open |
| REQ-PKG-014 | Keep insert OD, length, pilot, insertion depth, screw clearance, boss wall, edge distance, direction, and soldering-iron/tool access explicit; do not freeze supplier-dependent pilot dimensions before measurement and coupons. | `PHASE3A_FASTENER_STRATEGY`; report remains not-ready |
| REQ-PKG-015 | Prefer structural-part XY dimensions <=300 mm, use <=320 mm as the conservative maximum, and preserve replacement access for motion, spindle, limit, probe, and moving-bed hardware. | Phase 4 preliminary decomposition and service mock-up required |

## Frozen versus variable inputs

The frozen Phase 3 class baseline is MGN12H dual X/Y, MGN9H dual Z,
two carriages per rail, approximately 60/220/60 mm guide spacing,
T8x4/T8x4/T8x2 screws, direct drive, and fixed/floating supports. Phase 3A
varies rail length, carriage pitch, bearing envelope, motor recess, bed
support, end margin, service access, and package bounds only.

The exact motor identity, installed driver modules, spindle, controller
revision, rail supplier/preload, screw straightness, nut, switch, workholding,
and PETG interface remain unresolved. The owner-supplied controller platform is
known as Arduino Mega + CNC Shield, and the preliminary motor interface is the
generic 42.3 mm / 5 mm / 40-48 mm NEMA17 screen with rear connector/wiring
access. All dimensions in the Phase 3A model are review envelopes or
calculated packaging choices, not measured manufacturing facts.

## Gate boundary

The owner selected and accepted P2 on 2026-10-06. Phase 3A physical evidence
remains open, and Phase 4 is limited to preliminary structural concept CAD,
review calculations, print planning, and a preliminary safe-to-buy/wait BOM.
Manufacturing-ready geometry, production exports, final insert dimensions, and
later Phase 5 batches remain outside this Phase 3A scope. The separately
authorized Phase 5 base-pair candidate does not change the Phase 3A hardware
measurement boundary.
