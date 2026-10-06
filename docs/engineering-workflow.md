# Mandatory engineering workflow

The project advances through the following phases. A phase is not complete
when its files exist; it is complete when the exit evidence and a decision
record have been reviewed.

| Phase | Purpose | Required outputs | Gate |
| --- | --- | --- | --- |
| 1. Requirements | Convert the project brief into traceable requirements and acceptance measures. | Requirements baseline, open questions, initial calculations plan, EDR. | No conflicting or hidden requirements. |
| 2. Architecture | Choose the force loops, axis arrangement candidates, workholding, probing concept, and service boundaries. | Architecture options, trade study, risk register, EDR. | One architecture is selected or the blocker is explicit. |
| 3. Motion-system selection | Select guides, screws or transmissions, bearings, motors, couplers, switches, and controller interfaces. | Component trade study, motor data, travel budgets, preliminary motion BOM, EDR. | Components satisfy travel, load, speed, and packaging budgets. |
| 4. Preliminary BOM | Identify purchased and printed items with quantity, source, status, and dependencies. | Preliminary BOM and cost/availability risks, EDR. | No geometry relies on an untracked component assumption. |
| 5. Parametric skeleton model | Establish the coordinate system, datums, parameter schema, interfaces, and export smoke tests. | Central parameters, skeleton assembly, naming map, CAD spike, EDR. | Deterministic generation works without detailed geometry. |
| 6. Structural components | Design and analyze the printed PETG frame and interfaces. | Individual parametric parts, print orientations, calculations, coupons, EDR. | Parts fit the printer and load paths are reviewable. |
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
primary rejected alternative. The repository is now in Phase 3A compact
packaging review under proposed EDR-009, with EDR-008's motion classes serving
as the current technical baseline.

Phase 3/3A may select and dimension component classes, document interfaces and
calculations, compare compact packaging variants, and build review-only
motion/packaging skeletons. Exact hardware identity, supplier/preload,
spindle, PETG rail-seat/bearing-pocket evidence, full-travel service access,
and physical motion tests remain open. Phase 4 BOM finalization, detailed
structural CAD, and manufacturing exports do not begin from the proposed
Phase 3/3A records alone.
