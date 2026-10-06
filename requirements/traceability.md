# Initial requirement traceability

This is a starting traceability map, not a claim that every requirement is
already validated.

| Requirement family | Primary implementation / guidance | Validation evidence |
| --- | --- | --- |
| REQ-FN, REQ-ENV | pcb-cnc-architecture skill; docs/architecture/initial-architecture.md | Architecture review, then measured travel and process tests. |
| REQ-STR | printed-structural-design skill | Print-orientation evidence, structural calculations, coupons, and inspection. |
| REQ-HW | motion-system-design skill; requirements/phase-3-motion-system.md; open-questions.md | Motor and component data sheets plus motion decision record. |
| REQ-CAD | cad-conventions skill; cad/parameters.py | Deterministic generation and STEP/STL export tests. |
| REQ-VAL | design-validation skill; cad/validation | Automated report plus reviewed geometry evidence. |
| REQ-PCB | requirements/phase-1-process-requirements.md; pcb-cnc-architecture skill | Tool/depth/feed coupon, drilling coupon, outline coupon, and process records. |
| REQ-SPN | requirements/phase-1-process-requirements.md; motion-system-design skill | Spindle speed, runout, mass, diameter, and collet measurements. |
| REQ-WHL, REQ-PROBE | requirements/phase-1-process-requirements.md; pcb-cnc-architecture skill | Workholding distortion, conductive probe, map residual, and datum tests. |
| REQ-MOT | requirements/phase-1-motion-structure.md; motion-system-design skill | Axis calibration, repeatability, backlash, straightness, squareness, homing, and deflection tests. |
| REQ-Z | requirements/phase-1-z-error-budget.md; design-validation skill | Separate mechanical, probing, map, thermal, and board-surface evidence. |
| REQ-ENV-006 through REQ-ENV-008 | requirements/phase-1-envelope-trade.md | Reviewed A/B/C trade study and Phase 2 architecture EDR. |
| REQ-ARCH-* | requirements/phase-1-architecture-comparison.md | Phase 2 objective architecture comparison and architecture EDR. |
| REQ-PETG-* | requirements/phase-1-petg-manufacturing.md; printed-structural-design skill | Printer calibration coupons, print orientation, joint tests, and rail-seat inspection. |
| AT-* | requirements/phase-1-acceptance-tests.md | Physical test records; not satisfied by code alone. |
| REQ-ARCH-* | docs/architecture/phase-2-architecture.md; docs/architecture/phase-2-force-loop.md; docs/decisions/006-phase-2-architecture.md | Owner review of the A/B/C comparison, force-loop tests, workholding/probing mock-up, and the 5 N stiffness/creep evidence plan. |
| Phase 2 skeleton interfaces | cad/parameters.py; cad/assembly/architecture_skeleton.py | Dependency-light parameter checks plus the pinned build123d spike, deterministic placement, STEP/STL review export, bounding box, and interference report. |
| REQ-CAD-001 through REQ-CAD-004 | docs/architecture/phase-2-build123d-spike.md; requirements/cad-phase-2.txt | Pinned build123d smoke test now passes for the architecture skeleton; detailed parts and manufacturing export gates remain future work. |
| Phase 2A A/B structural evidence | cad/phase2a.py; cad/parameters.py; docs/architecture/phase-2a-structural-comparison.md; docs/calculations/phase-2a-structural-calculations.md; docs/architecture/phase-2a-physical-validation.md; EDR-007 | Reproducible analytical model, 22 automated tests, optimized review skeleton, and coupon/test plan; physical stiffness and creep remain not-ready. |
| Phase 3 motion classes | requirements/phase-3-motion-system.md; cad/parameters.py; cad/motion_phase3.py; docs/architecture/phase-3-motion-system.md; docs/calculations/phase-3-motion-calculations.md; EDR-008 | Centralized component-class inputs, dependency-light calculations, parameter checks, review-only motion skeleton, and proposed physical tests; exact hardware and motion evidence remain not-ready. |
| Phase 3 review BOM | bom/phase-3-motion-bom.md; EDR-008 | Quantity/class/sample boundary and safe-purchase guidance; production BOM remains a Phase 4 gate. |

## Evidence rule

A requirement is not complete merely because a module exists. The phase gate
must identify the evidence type: documentation, calculation, automated check,
dimensional inspection, test coupon, or machine experiment.
