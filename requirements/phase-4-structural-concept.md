# Phase 4 - preliminary structural CAD concept

**Status:** authorized for preliminary owner review; not accepted for
manufacturing or Phase 5

The owner accepted the Phase 3 motion baseline and the P2 Phase 3A packaging
baseline on 2026-10-06. This document defines the controlled Phase 4 scope. It
authorizes a coherent, printable, serviceable structural concept and review
exports; it does not freeze supplier-dependent dimensions or release parts for
manufacture.

## Requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-P4-001 | Use the accepted P2 reference: approximately 364 x 356 x 276 mm machine envelope, 444 x 428 x 322 mm service footprint, 200 x 150 mm PCB area, 230 x 180 x 8 mm bed support, and 230 x 180 x 12 mm spoilboard. | Owner baseline / preliminary | Central parameters and assembly containment; verify with measured hardware. |
| REQ-P4-002 | Preserve the fixed gantry with moving Y bed force loop, dual MGN12 X/Y guides, dual MGN9 Z guides, 60 mm X/Z spacing, 220 mm Y spacing, T8x4 X/Y, T8x2 Z, and 40 mm Z travel. | Owner baseline / preliminary | P2 references in the review assembly; motion and physical tests remain open. |
| REQ-P4-003 | Build PETG stiffness through closed sections, torsion boxes, ribs, gussets, monocoque load paths, broad interfaces, and short force loops rather than a visually solid high-infill block. | Known design rule | Structural review geometry and printed coupons. |
| REQ-P4-004 | Keep every mandatory structural print at or below 320 mm in both build-plate axes and prefer at or below 300 mm. A larger mandatory part requires a new owner decision and printer-specific proof. | Owner direction | 29-part decomposition and fail-closed print-bound validation. |
| REQ-P4-005 | Split the fixed gantry beam only as needed; compare J1 deep tongue/socket, J2 stepped keyed shoulder, and J3 interlocking rib/shear-key concepts. | Preliminary choice | J1 selected provisionally; joint coupons and service cycling required. |
| REQ-P4-006 | Use M3 for small/accessory hardware, M4 for general structural/module joints, and M5 only with a technical justification. Fasteners provide preload; printed geometry provides location and shear transfer. | Owner direction | Central fastening strategy, part notes, and future insert measurements. |
| REQ-P4-007 | Keep insert OD, length, pilot, insertion depth, boss wall, edge distance, clearance, direction, and tool access unresolved until actual inserts are measured and PETG coupons pass. | Known evidence boundary | Preliminary pockets/interfaces only; no production insert geometry. |
| REQ-P4-008 | Tie dual X rail seats into the fixed torsion structure and dual Z rail seats into the X/Z backplate; tie dual Y rail seats into the base load path. Do not assume raw PETG is a precision datum. | Preliminary interface rule | Printed shoulders/pads, shim/skimming strategy, and parallelism checks. |
| REQ-P4-009 | Provide a low-mass ribbed moving bed with replaceable spoilboard/workholding and a centered Y nut/screw service path. | Preliminary concept | Moving-bed frame geometry and full-travel mock-up. |
| REQ-P4-010 | Make motors, fixed/floating bearing cartridges, couplers, screws/nuts, rails/carriages, spindle, limits, probe, moving-bed wiring, and spoilboard replaceable. | Owner direction | Assembly sequence, service notes, and physical access review. |
| REQ-P4-011 | Update the Phase 2A 5 N deflection screen by separating gantry beam, tower/joint, X/Z, base, rail-seat, and moving-bed contributions. Target is <=0.020 mm and acceptance is <=0.030 mm. | Calculated preliminary | `cad/phase4_calculations.py`; no FEA or measured-property claim. |
| REQ-P4-012 | Document every structural part's status, orientation, print extents, support, brim/warping, and layer/load concerns. | Preliminary process contract | Central part parameter records and print-planning report. |
| REQ-P4-013 | Validate full XYZ travel, bed/spindle/motor/screw/coupler/bearing/fastener/rail/limit/probe clearances, assembly sequence, component containment, and unexpected solid interference. | Automated plus physical evidence | Pinned build123d runner passes review geometry; physical mock-up remains open. |
| REQ-P4-014 | Split the BOM into safe-to-purchase measurement/coupon items and wait-for-measurement or owner-review items. Do not treat reference envelopes as vendor dimensions. | Preliminary purchasing boundary | `bom/phase-4-preliminary-structural-bom.md`. |
| REQ-P4-015 | Keep Phase 4 geometry PRELIMINARY. Do not generate production release files, mark parts manufacturing-ready, accept Phase 4, or begin Phase 5. | Owner gate | EDR-011, repository audit, and explicit owner review. |

## Scope boundary

Phase 4 includes preliminary parametric geometry and temporary review exports.
It excludes final rail/screw/bearing/motor/spindle/controller/switch/probe/
workholding dimensions, production insert pockets, manufacturing tolerances,
final fastener patterns, physical structural validation, release drawings,
release STEP/STL, and Phase 5 work.

The next gate is owner review of EDR-011 with the generated report, temporary
STEP/STL artifacts, print decomposition, joint study, rail-seat strategy,
calculation screen, and preliminary BOM. The gate remains not-ready until the
named physical and measurement evidence is collected.
