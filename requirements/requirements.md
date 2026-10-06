# Initial requirements

This document is the initial requirements baseline. It is intentionally
conservative: a preliminary target is not an acceptance limit until it is
reviewed and promoted by an engineering decision record.

## Requirement status vocabulary

| Status | Meaning |
| --- | --- |
| Known requirement | Explicitly supplied by the user or directly observed. |
| Assumption | Temporary value adopted to make analysis possible. |
| Preliminary choice | Candidate selected for the next phase, not yet frozen. |
| Calculated value | Derived from documented inputs and an equation. |
| Experimentally verified value | Measured on a test article or the machine. |

## Functional requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-FN-001 | The primary use is PCB manufacturing: FR4 isolation routing, PCB drilling, and PCB outline cutting. | Known requirement | User project brief. |
| REQ-FN-002 | The machine is not intended to be a general-purpose metal milling machine. | Known requirement | User project brief. |
| REQ-FN-003 | Accuracy, repeatability, low Z deflection, low spindle runout, rigidity around the tool, and PCB height mapping have priority over large cutting forces and high material removal rate. | Known requirement | User project brief; quantify acceptance values during Phase 1. |
| REQ-FN-004 | The design must support repeatable PCB workholding, a replaceable or serviceable spoilboard, probing, and a height-mapping workflow. | Known requirement | User project brief; implementation details remain open. |

## Envelope and interface requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-ENV-001 | Initial target X working travel is approximately 200 mm. | Preliminary choice | User target; confirm usable tool-point travel after architecture layout. |
| REQ-ENV-002 | Initial target Y working travel is approximately 150 mm. | Preliminary choice | User target; confirm usable tool-point travel after architecture layout. |
| REQ-ENV-003 | Initial target Z working travel is approximately 30-50 mm. | Preliminary choice | User target range; select a design point after tool, workholding, and clearance analysis. |
| REQ-ENV-004 | Every printable structural component must have a realistic print orientation within the usable build volume of a Voron 2.4 350, approximately 350 mm x 350 mm x 350 mm. | Known requirement | User printer capability; confirm usable margins and orientation in Phase 6. |
| REQ-ENV-005 | The target envelope is a planning target, not an immutable dimension. Changes require a recorded reason and impact review. | Known requirement | User project brief. |

## Structural requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-STR-001 | The structural frame shall be predominantly 3D-printed PETG. | Known requirement | User project brief. |
| REQ-STR-002 | The printed frame shall use additive-manufacturing-appropriate geometry: monocoques, closed sections, ribs, gussets, triangulation, large radii, short load paths, distributed interfaces, and appropriate print orientation. | Known requirement | User project brief; detail in printed-structural-design skill. |
| REQ-STR-003 | Metal components are allowed where mechanically appropriate, including rails, lead screws, bearings, fasteners, shafts, spindle, threaded inserts, and couplers. | Known requirement | User project brief. |
| REQ-STR-004 | Aluminum extrusion, aluminum plate, or welded steel shall not be substituted for the printed frame without an explicit load-path decision record. | Known requirement | User project brief. |
| REQ-STR-005 | Stiffness shall be obtained primarily through geometry and load-path design rather than an assumed high infill percentage. | Known requirement | User project brief; verify through calculation and test coupons. |

## PETG fastening and modularity requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-FAST-001 | Fasteners shall provide preload while printed geometry provides location and shear transfer. | Known owner direction | Central strategy in `cad/parameters.py`; interface validation and joint review. |
| REQ-FAST-002 | Heat-set inserts shall be the default reusable threaded interface in PETG. | Known owner direction | PETG skill, Phase 3A strategy, and measured insert/coupon evidence before release. |
| REQ-FAST-003 | The default insert hierarchy shall be M3 for small/accessory hardware, M4 for general structural/module joints, and M5 only when technically justified. | Known owner direction | `PHASE3A_FASTENER_STRATEGY`; no extra sizes without an EDR. |
| REQ-FAST-004 | Important joints shall use geometric shoulders, steps, keys, pockets, registrations, shear keys, mating faces, or interlocking ribs in addition to clamp fasteners. | Known owner direction | Review-only interface screens; future structural CAD and joint inspection. |
| REQ-FAST-005 | Through-bolts shall be selective, justified by insert pull-out, creep, preload, moment, cyclic loading, or failure consequence, and shall still use geometric shear transfer. | Known owner direction | Fail-closed interface validator and joint load-path review. |
| REQ-FAST-006 | Reusable insert interfaces shall parameterize OD, length, pilot range, insertion depth, wall, edge distance, direction, screw clearance, and soldering-iron/tool access. | Preliminary owner direction | Supplier dimensions remain unresolved until actual inserts are measured and coupon-tested. |
| REQ-FAST-007 | Structural parts shall prefer <=300 mm XY dimensions, use <=320 mm as the conservative maximum, and receive explicit review at or above 300 mm. | Preliminary owner direction | PETG manufacturing requirements, printability review, and modular interface study. |
| REQ-FAST-008 | Motors, rails, carriages, lead screws/nuts, bearings, spindle, limits, probe wiring, and moving-bed wiring shall remain replaceable. | Preliminary owner direction | Service-access mock-up before Phase 3A acceptance. |

## Owned hardware and future purchase boundary

| ID | Item | Status | Design consequence |
| --- | --- | --- | --- |
| REQ-HW-001 | A large selection of NEMA17 stepper motors originally acquired for 3D-printer use is already owned. | Known requirement | Do not purchase motors. Characterize representative stock and assign axes from measured evidence. |
| REQ-HW-002 | An Arduino Mega + CNC Shield controller platform is already owned and intended for this machine. | Known requirement | Do not replace the controller unless later validation identifies an actual limitation; identify the exact Shield revision and installed drivers. |
| REQ-HW-003 | A Voron 2.4 350 printer is available for PETG structural parts. | Known requirement | Measure usable build margins and establish a print-orientation validation method. |
| REQ-HW-004 | Rails, screws, bearings, spindle, fasteners, inserts, couplers, and similar mechanical components may be purchased later. | Known requirement | Use the hardware procurement / measurement freeze before any production interface is released. |
| REQ-HW-005 | The preliminary motion class is dual MGN12H X/Y, dual MGN9H Z, T8x4 X/Y, T8x2 Z, serviceable fixed/floating screw supports, and torque-only flexible couplers. | Owner-accepted preliminary baseline | EDR-008, EDR-009, EDR-013; exact supplier, preload, end machining, and measured dimensions remain open. |
| REQ-HW-006 | Existing NEMA17 motors and the Arduino Mega + CNC Shield platform shall be identified and measured before final electrical/mechanical interfaces or commissioning. | Owner direction | Hardware identification sheets in `requirements/hardware-procurement-measurement-freeze.md`; this does not block the generic preliminary structural CAD envelope. |
| REQ-HW-007 | Preliminary structural CAD shall use a standardized common NEMA17 mechanical interface rather than one exact owner motor: approximately 42.3 mm mounting square, screening 5 mm shaft, common 40-48 mm body class, and rear connector/wiring access. | Owner direction | Central Phase 3 parameters and review envelopes; exact pilot, shaft engagement, body, connector, and rear-clearance values remain measured before manufacturing release. |
| REQ-HW-008 | Final motor assignment shall come from owner stock: normal suitable characterized motors for X/Y and the strongest electrically compatible characterized motor for Z. | Owner direction | Motor identification sheet, driver/supply compatibility, torque-at-speed, temperature, and missed-step evidence. |

## CAD and deliverable requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-CAD-001 | The authoritative source shall be parametric CAD, not a mesh-first model. | Known requirement | User project brief. |
| REQ-CAD-002 | The CAD source shall produce STEP and STL files, a complete assembly, and individual printable parts. | Known requirement | User project brief; export tests are a Phase 10 gate. |
| REQ-CAD-003 | Important dimensions shall come from a centralized parameter file. | Known requirement | User project brief; enforced by cad-conventions skill and review. |
| REQ-CAD-004 | Part names, placements, mounting-hole patterns, standard hardware representations, and coordinate conventions shall be deterministic and reusable. | Known requirement | User project brief. |

## Validation requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-VAL-001 | Validation shall cover target XY and Z travel, rail-carriage travel, lead-screw travel, collisions, spindle clearance, spindle-to-bed clearance, motor and coupler clearance, screw accessibility, assembly accessibility, wall thickness, fastener edge distance, rail mounting surfaces, and build-volume compatibility. | Known requirement | Validation rule catalog in design-validation skill; geometry adapters are future work. |
| REQ-VAL-002 | Build-volume validation shall consider at least one realistic print orientation, not only the default bounding box. | Known requirement | Implemented as an explicit candidate-orientation interface in cad/validation. |
| REQ-VAL-003 | Missing geometry or evidence shall produce an explicit not-ready or error result rather than a silent pass. | Preliminary choice | Adopt as validation policy; review during Phase 8. |

## Phase 1 quantitative baseline

The following requirement groups were accepted as the Phase 1 screening
baseline through EDR-005. They remain preliminary or assumed where marked in
their source documents and are not physically verified:

| Requirement group | Detail |
| --- | --- |
| REQ-PCB-* | [PCB process requirements](phase-1-process-requirements.md) for copper, tool families, isolation depth, drilling, outline cutting, spindle envelope, workholding, probing, and mapping. |
| REQ-MOT-* | [Motion and structure requirements](phase-1-motion-structure.md) for travel, command increments, accuracy, repeatability, backlash, straightness, squareness, deflection, overhang, and homing. |
| REQ-Z-* | [Z error budget](phase-1-z-error-budget.md), with separate mechanical and map residual limits. |
| REQ-ENV-006 through REQ-ENV-008 | [Envelope trade study](phase-1-envelope-trade.md) for 160 x 100, 200 x 150, and 250 x 180 mm PCB areas. |
| REQ-ARCH-* | [Architecture-comparison requirements](phase-1-architecture-comparison.md) for moving-bed and moving-gantry studies; no architecture is selected here. |
| REQ-PETG-* | [PETG manufacturing constraints](phase-1-petg-manufacturing.md) for printing, joints, tolerances, and rail seats. |
| AT-* | [Acceptance-test plan](phase-1-acceptance-tests.md) for future physical validation. |

These documents distinguish calculated screening values from requirements
that need a physical coupon or machine test. They do not claim measured
performance.

## Phase 3 motion-system baseline

The owner-authorized Phase 3 screening requirements and evidence boundary are
recorded in [phase-3-motion-system.md](phase-3-motion-system.md). The current
review layout uses Architecture A, dual MGN12H-class X/Y guides, dual MGN9H
class Z guides, T8x4 X/Y screws, T8x2 Z screw, fixed/floating screw supports,
preloaded anti-backlash nut classes, an identified NEMA17 acceptance envelope,
and a GRBL-compatible 8-microstep starting configuration. These are
preliminary component classes, not final purchased parts or measured
performance.

Phase 2A PETG coupons and representative 5 N force-loop evidence remain
required. Phase 3 adds rail-seat/play, backlash/preload, screw axial play,
homing repeatability, missed-step, straightness/squareness, and controller
interface tests. The owner accepted the Phase 3 motion baseline on 2026-10-06
in [EDR-008](../docs/decisions/008-phase-3-motion-system.md). Exact supplier
hardware, measured dimensions, and physical motion evidence remain open.

The owner-directed PETG fastening strategy is recorded in
[phase-3a-fastening-strategy.md](phase-3a-fastening-strategy.md) and
[EDR-010](../docs/decisions/010-petg-fastening-strategy.md). It applies to
Phase 3A review interfaces and later structural CAD. The owner accepted P2 as
the Phase 3A baseline on 2026-10-06; it authorizes the preliminary Phase 4
concept but not production geometry or release.

## Phase 4 preliminary structural concept baseline

The owner-accepted preliminary Phase 4 scope is recorded in
[phase-4-structural-concept.md](phase-4-structural-concept.md) and
[EDR-011](../docs/decisions/011-phase-4-preliminary-structural-concept.md).
The accepted P2 reference is approximately 364 x 356 x 276 mm with a 444 x
428 x 322 mm service footprint, a 230 x 180 x 8 mm bed support, a 230 x 180 x
12 mm spoilboard, fixed gantry, moving Y bed, dual MGN12 X/Y guides, dual
MGN9 Z guides, T8x4 X/Y screws, T8x2 Z screw, and 40 mm Z travel.

Phase 4 may build preliminary PETG force-loop geometry, a split fixed-gantry
beam with a provisional J1 tongue/socket, rail-seat datum concepts, a ribbed
moving bed, service cartridges, a full review assembly, temporary STEP/STL
exports, preliminary calculations, and a split BOM. Every mandatory printed
part must be at or below 320 mm in both build-plate axes, preferably at or
below 300 mm, with explicit orientation and process notes. Fasteners provide
preload; printed geometry provides location and shear transfer.

Phase 4 geometry remains PRELIMINARY. Actual rail, screw, bearing, motor,
spindle, insert, switch, controller, probe, workholding, and PETG coupon
dimensions remain unresolved. The preliminary architecture is accepted, but
manufacturing release and Phase 5 are not authorized.

## Hardware procurement / measurement freeze

The active A-D procurement, identification, measurement, coupon, and physical
test requirements are recorded in
[hardware-procurement-measurement-freeze.md](hardware-procurement-measurement-freeze.md)
and [EDR-013](../docs/decisions/013-hardware-procurement-measurement-freeze.md).
The document is the controlling pre-production interface list; it does not
make any hardware interface manufacturing-ready.

## Scope exclusions for this iteration

- No manufacturing-ready CNC part geometry; Phase 4 review geometry is
  explicitly preliminary.
- No production STEP, STL, or drawing export.
- No final vendor rail, screw, spindle, motor, controller, workholding, or
  probing selection; only preliminary motion component classes, reference
  envelopes, and concept interfaces are recorded.
- No final insert pilot/OD/length dimensions, production fastener pattern, or
  Phase 5 work.
- No unverified accuracy, repeatability, deflection, feed-rate, or runout claims.
