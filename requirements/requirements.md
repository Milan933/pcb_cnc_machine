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

## Owned hardware and future purchase boundary

| ID | Item | Status | Design consequence |
| --- | --- | --- | --- |
| REQ-HW-001 | Multiple NEMA 17 stepper motors are already owned. | Known requirement | Record motor model, torque curve, shaft, current, and condition before final motion selection. |
| REQ-HW-002 | An Arduino CNC Shield / GRBL-compatible controller is already owned. | Known requirement | Confirm supported stepper current, number of axes, limit inputs, probing input, spindle control, and firmware limits. |
| REQ-HW-003 | A Voron 2.4 350 printer is available for PETG structural parts. | Known requirement | Measure usable build margins and establish a print-orientation validation method. |
| REQ-HW-004 | Rails, screws, bearings, spindle, fasteners, inserts, couplers, and similar mechanical components may be purchased later. | Known requirement | Choose mechanically appropriate parts first; create the BOM afterward. |
| REQ-HW-005 | MGN9, MGN12, T8x2, and T8x4 are candidates to evaluate, not selections. | Known requirement | Compare against load, stiffness, speed, packaging, contamination, and availability requirements. |

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

The following requirement groups are proposed by the Phase 1 review and remain
preliminary until EDR-005 is accepted:

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
that need a physical coupon or machine test. They do not select a spindle,
rail, screw, motor, controller, or axis architecture.

## Scope exclusions for this iteration

- No detailed CNC part geometry.
- No production STEP, STL, or drawing export.
- No final rail, screw, spindle, motor, controller, workholding, or probing selection.
- No unverified accuracy, repeatability, deflection, feed-rate, or runout claims.
