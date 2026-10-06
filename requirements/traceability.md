# Initial requirement traceability

This is a starting traceability map, not a claim that every requirement is
already validated.

| Requirement family | Primary implementation / guidance | Validation evidence |
| --- | --- | --- |
| REQ-FN, REQ-ENV | pcb-cnc-architecture skill; docs/architecture/initial-architecture.md | Architecture review, then measured travel and process tests. |
| REQ-STR | printed-structural-design skill | Print-orientation evidence, structural calculations, coupons, and inspection. |
| REQ-HW | motion-system-design skill; open-questions.md | Motor and component data sheets plus motion decision record. |
| REQ-CAD | cad-conventions skill; cad/parameters.py | Deterministic generation and STEP/STL export tests. |
| REQ-VAL | design-validation skill; cad/validation | Automated report plus reviewed geometry evidence. |

## Evidence rule

A requirement is not complete merely because a module exists. The phase gate
must identify the evidence type: documentation, calculation, automated check,
dimensional inspection, test coupon, or machine experiment.
