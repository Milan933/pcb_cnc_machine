# Mandatory engineering workflow

The project advances through the following phases. A phase is not complete
when its files exist; it is complete when the exit evidence and a decision
record have been reviewed.

| Phase | Purpose | Required outputs | Gate |
| --- | --- | --- | --- |
| 1. Requirements | Convert the project brief into traceable requirements and acceptance measures. | Requirements baseline, open questions, initial calculations plan, EDR. | No conflicting or hidden requirements. |
| 2. Architecture | Choose the force loops, axis arrangement candidates, workholding, probing concept, and service boundaries. | Architecture options, trade study, risk register, EDR. | One architecture is selected or the blocker is explicit. |
| 3. Motion-system selection | Select guides, screws or transmissions, bearings, motors, couplers, switches, and controller interfaces. | Component trade study, motor data, travel budgets, preliminary motion BOM, EDR. | Components satisfy travel, load, speed, and packaging budgets. |
| 3A. Compact packaging | Fit the accepted motion classes, full travel, bed, spindle, motors, supports, and service envelopes. | P1/P2/P3 packaging study, P2 baseline, EDR. | A packaging baseline is selected or the blocker is explicit. |
| 4. Preliminary structural CAD concept | Develop the printed PETG force-loop parts, split joints, rail seats, moving bed, service interfaces, print plans, calculations, and preliminary BOM. | Parametric review geometry, assembly, joint study, printability evidence plan, calculations, preliminary BOM, EDR. | Owner review accepts the concept or records rework; no production release is implied. |
| 4B. Hardware procurement / measurement freeze | Convert the accepted vendor-independent motion and fastening classes into measured sample interfaces and procurement gates. | A-D procurement matrix, hardware identification sheets, measurement plan, coupons, EDR. | Measured interfaces and physical evidence are complete enough for a new owner decision; manufacturing-ready CAD is still a later gate. |
| 5. Manufacturing CAD first batch | Convert the accepted O2 base pair into real fused, parametric, printable PETG parts and reproducible local STEP/STL candidates. | Base-pair source, print orientation/process contract, candidate export manifest, geometry/export validation, EDR. | Owner can inspect/slice the two candidates; no release or hardware-validation claim. |
| 6. Remaining structural components | Extend the manufacturing-CAD conventions to the remaining O2 parts after the base-pair review. | Individual parametric parts, print orientations, calculations, coupons, EDR. | Parts fit the printer and load paths are reviewable. |
| 7. Complete assembly | Integrate motion, spindle, workholding, probing, guards, cables, and service access. | Complete parametric assembly, interference report, assembly EDR. | Required clearances and access pass. |
| 8. Automated validation | Run the rule catalog against the assembly and exports. | Validation report, test results, exceptions, EDR. | No unreviewed errors; warnings have owners. |
| 9. Design review | Review requirements, risks, calculations, printability, maintainability, and safety. | Review checklist, disposition of actions, release decision, EDR. | Explicit approval or rework list. |
| 10. Manufacturing exports | Generate reviewed STEP, STL, drawings, and release metadata. | Versioned exports, export manifest, print notes, final BOM, EDR. | Exports are reproducible from the tagged source. |

## Rules for every phase

Each phase creates an engineering decision record containing:

- decision;
- alternatives considered;
- reasoning and evidence;
- risks and mitigations;
- unresolved questions;
- affected requirements;
- owner and review status.

Changing an approved decision reopens its downstream gates. An unresolved
question may remain open only if the risk is bounded and the next evidence
collection step is named.

## Current phase

The repository has completed the foundation pass and Phase 1. The owner has
reviewed EDR-006 with EDR-007 and accepted **A: fixed gantry with moving Y
bed** as the mechanical architecture baseline; B remains the documented
primary rejected alternative. The owner accepted the Phase 3 motion baseline,
the P2 Phase 3A packaging baseline, and the Phase 4/4A preliminary structural
architecture baseline on 2026-10-06. The repository is now in the hardware
procurement / measurement freeze under proposed EDR-013.

The O2 structure is accepted as preliminary architecture only. The owner has
now authorized the first Phase 5 manufacturing-CAD batch for
`base_left_integrated` and `base_right_integrated`. Exact hardware identity,
supplier/preload, spindle, insert dimensions, PETG rail-seat/bearing-pocket
evidence, full-travel service access, and physical force-loop tests remain
open. The first batch is `PROTOTYPE-STL`; release exports, hardware validation,
and the remaining structural parts remain blocked pending owner review.
