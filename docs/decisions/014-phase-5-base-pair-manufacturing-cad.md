# Engineering decision record: Phase 5 first base-pair manufacturing CAD

- **Record ID:** EDR-014
- **Phase:** Phase 5 manufacturing CAD, first controlled batch
- **Status:** owner-authorized / implementation batch
- **Date:** 2026-10-07
- **Owner:** project owner / project team
- **Baseline:** `afe2e14089467321b323d74f928a7ab4c5ffdc1f`
- **Inputs:** accepted Phase 4/4A O2 architecture, hardware clarification,
  EDR-013 measurement boundary, and owner authorization to open Phase 5
- **Affected requirements:** REQ-P4-003, REQ-P4-004, REQ-P4-008,
  REQ-P4-010, REQ-P4-012, REQ-P4-013, REQ-P4-015, REQ-HW-007,
  REQ-HW-008, REQ-CAD, and REQ-VAL

## Decision

Open Phase 5 for exactly two first-batch manufacturing-CAD parts:
`base_left_integrated` and `base_right_integrated`. Convert the accepted O2
review concepts into deterministic, fused, locally printable PETG solids with
real perimeter walls, carrier webs, ribs, rail-seat material, and provisional
fastener openings. Generate local STEP and STL derivatives and stop for owner
review.

This decision establishes the manufacturing-CAD conventions. It does not open
the remaining 17 structural parts, authorize a production BOM, or authorize
release artifacts.

## Alternatives considered

| Alternative | Disposition | Reason |
| --- | --- | --- |
| Keep all O2 geometry as review compounds | Rejected for this batch | Does not meet the owner's request for real printable structural STL files. |
| Convert all 19 O2 parts in one batch | Rejected | Too much uncontrolled interface and print-risk surface before the conventions are reviewed. |
| Wait for final NEMA17, Shield, rail, and insert identification | Rejected for preliminary candidate geometry | Owner explicitly authorized provisional interfaces and confirmed that motor selection does not block structural STL development. |
| Build only the integrated base pair | Selected | Exercises walls, ribs, rail seats, print orientation, provisional interfaces, export, and validation at a reviewable scope. |

## Controlled geometry choice

The first pair uses a 150 x 300 mm local print footprint and 43.75 mm
parametric height. Each part is a mirrored local variant. The source creates:

- 5 mm screened closed perimeter walls;
- a 28 mm carrier with a relieved cavity, top rail pad, and 3 mm printed
  shoulder;
- a continuous carrier-to-side shear web and four transverse ribs;
- a center-tie shear land;
- provisional rail clearance openings, foot clearance/counterbore openings,
  and center-tie clearance openings.

The rail, foot, and tie openings are not measured interfaces. They are labeled
`PROVISIONAL_HARDWARE_DIMENSION` in the source and manifest. The rail shoulder
is a printed alignment aid, not a claim that unconditioned PETG is a precision
datum.

## Hardware disposition

The design continues to use the owner-supplied Arduino Mega + CNC Shield and
the owner's NEMA17 stock. It does not recommend replacement controller or new
motors. Shield revision, driver modules, electrical capability, and final motor
assignment remain commissioning/identification items. The generic NEMA17
interface is not embedded in this base pair and therefore does not block the
batch.

## Validation and maturity

The Phase 5 validator must fail closed for a missing part, invalid shape,
multiple disconnected solids, a footprint over 320 mm, or a missing/empty
STEP/STL file. It may report warning-level `NOT_READY` states for provisional
hardware dimensions and missing physical evidence so that a test-printable
candidate can be inspected without being mislabeled as released.

The target maturity is `PROTOTYPE-STL`. The output is neither
`HARDWARE-VALIDATED` nor `RELEASED`.

## Evidence and stop boundary

The owner must inspect both files in OrcaSlicer, perform the first PETG print,
measure the printed datums and hardware interfaces, and review the manifest
before the next manufacturing-CAD batch. The repository must retain the
parametric source, tests, validation, manifest, and decision record. Candidate
STEP/STL files remain in ignored development directories; release directories
remain empty.

**Disposition:** Phase 5 first batch open; stop after the base pair for owner
review. Remaining O2 parts and manufacturing release remain not-ready.
