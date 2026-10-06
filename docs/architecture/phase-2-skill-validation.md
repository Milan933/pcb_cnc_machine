# Phase 2 project-skill validation

The six project skills were read in full and applied to this phase package.
Their evidence boundary is recorded here so the architecture result is not
mistaken for detailed part or motion selection.

| Skill | Phase 2 evidence | Deliberate boundary |
| --- | --- | --- |
| `pcb-cnc-architecture` | A/B/C force loops, fixed-bed workholding, conductive probing, map validity, PCB process priorities | no final controller/toolpath implementation |
| `motion-system-design` | X/Y/Z travel budgets, guide spacing and moment comparison, centered screw lines, MGN9/MGN12 and T8x2/T8x4 candidates, homing/service questions | no rail, screw, motor, bearing, coupler, or controller freeze |
| `printed-structural-design` | closed/deep-ribbed/monocoque PETG section trade, distributed interfaces, creep/anisotropy/printability risks, Voron 350 bound | no wall, rib, insert, fastener, slicer, or printable-part geometry |
| `cad-conventions` | millimetre coordinate convention, centralized skeleton parameters, deterministic named placements, compound-backed assembly, explicit review exports | no manufacturing STEP/STL release |
| `design-validation` | fail-closed parameter checks, skeleton bounds, exact-solid interference scan with documented expected contacts, explicit not-ready future evidence | detailed rail seats, wall thickness, clearances, swept cable/motor access remain future geometry rules |
| `repository-workflow` | public-boundary audit, external temporary spike outputs, pinned dependency, tracked source only, staged diff/test/push gate | no temporary CAD binaries or unreviewed release artifacts in Git |

The architecture package is therefore complete for owner review but is not an
authorization to start Phase 3 or detailed structural CAD.

## Phase 2A supplement evidence

The same six skills were applied to the focused A/B study:

| Skill | Phase 2A application | Boundary retained |
| --- | --- | --- |
| `pcb-cnc-architecture` | A moving-bed datum risk and B fixed-bed probing/workholding benefit are quantified alongside the tool loop | no process acceptance claim from a static model |
| `motion-system-design` | Y moving mass, acceleration force, centered screw, guide couple, and lead/torque implications are screened | no motor, screw, rail, or controller selection |
| `printed-structural-design` | A deep integrated U and B deep ribbed beam are compared with PETG joint/creep risks | equivalent sections are not FEA or printable geometry |
| `cad-conventions` | Phase 2A inputs are centralized; A/B optimized bounds use named review components and the existing coordinate convention | no production CAD or manufacturing export |
| `design-validation` | input checks, bounded review skeletons, non-empty exports, and zero unexpected overlaps are required | physical stiffness, creep, alignment, and fit remain not-ready |
| `repository-workflow` | study outputs are external temporary derivatives; tests, candidate audit, tracked audit, and diff review are required before publication | no temp binaries, caches, or secrets in Git |

The Phase 2A implementation deliberately uses a transparent standard-library
analytical model. No opaque or non-reproducible FEA result was substituted for
the mandatory equations.

## Phase 3A fastening-strategy supplement

The owner-directed PETG fastening strategy was reviewed against the three
affected project skills and the repository workflow:

| Skill | Phase 3A application | Boundary retained |
| --- | --- | --- |
| `printed-structural-design` | Heat-set inserts are the default reusable PETG thread; M3/M4/M5 hierarchy, rib-connected bosses, geometric shear transfer, selective through-bolts, insert orientation, and <=300/<=320 mm print-size rules are explicit. | Exact insert dimensions, PETG pull-out/creep/repeated-assembly data, and production joint geometry remain open. |
| `cad-conventions` | `cad/parameters.py` centralizes insert families and review interfaces; reusable interfaces declare wall, edge, direction, clearance, and tool-access fields without scattered pilot literals. | No production structural CAD or frozen supplier pocket dimensions. |
| `design-validation` | `cad/fastening.py` checks hierarchy, family completeness, boss material, edge distance, tool access, geometric load transfer, M5 justification, and through-bolt justification; unresolved supplier dimensions return explicit `not-ready`. | Review-level screens do not replace measured inserts, coupons, load-path evidence, or service mock-up. |
| `repository-workflow` | New source, tests, requirements, decision record, and documentation are audited before commit; temporary CAD environments and exports remain outside Git. | No generated manufacturing artifacts or final hardware BOM. |

Verification for this supplement is `python -B -m unittest discover -s tests -v`
(42 tests passing), the pinned build123d Phase 3A runner (P1/P2/P3 exports,
containment, and zero unexpected interferences), `python -B
tools/repository_audit.py`, and a staged-diff review. The fastening report is
intentionally `not-ready` with zero blocking issues until actual inserts and
PETG coupons exist; Phase 4 remains blocked.
