# Phase 2 weighted architecture decision matrix

The matrix is an ordinal screening tool. Each candidate receives 1 (poor) to
5 (favorable) for the same 200 x 150 mm PCB baseline, 5 N test load, 40 mm
screening Z travel, predominantly PETG frame, and Voron 350 print constraint.
The normalized score is `100 * sum(weight * score / 5) / sum(weight)`.

The first four criteria carry 45% of the weight because tool-point stiffness,
Z stiffness, torsion, and force-loop length directly control PCB isolation and
drilling. Structural/PETG/printability criteria carry 26%, datum and probing
carry 8%, assembly/service/mass/spindle compatibility carry 17%, and
travel/footprint carry 4%.
This intentionally puts process stability ahead of cost or maximum envelope.

The matrix below is the original Phase 2 three-way baseline. Its close B
result was a screening judgment, not structural proof and not an accepted
architecture decision. The higher-resolution A/B replacement is in
[phase-2a-structural-comparison.md](phase-2a-structural-comparison.md).

## Base matrix

| Criterion | Weight | A moving bed | B moving gantry | C moving XY head |
| --- | ---: | ---: | ---: | ---: |
| predicted tool-point stiffness | 15 | 4 | 4 | 2 |
| Z stiffness | 12 | 4 | 4 | 3 |
| gantry torsional stiffness | 8 | 4 | 3 | 4 |
| force-loop length | 10 | 4 | 4 | 2 |
| structural joints | 4 | 4 | 4 | 2 |
| PETG creep | 4 | 3 | 3 | 2 |
| rail alignment | 5 | 3 | 4 | 2 |
| assembly | 4 | 3 | 3 | 2 |
| service | 5 | 3 | 4 | 2 |
| Voron printability | 8 | 4 | 4 | 3 |
| large-print risk | 3 | 4 | 4 | 3 |
| material efficiency | 2 | 4 | 3 | 2 |
| moving mass | 5 | 3 | 3 | 2 |
| spindle compatibility | 3 | 4 | 4 | 3 |
| workholding accessibility | 5 | 3 | 5 | 5 |
| probing accessibility | 3 | 3 | 5 | 4 |
| achievable travel | 3 | 4 | 4 | 3 |
| footprint | 1 | 3 | 4 | 2 |
| **normalized result** | **100** | **73.6** | **77.0** | **53.2** |

## Interpretation of the original baseline

B wins by 3.4 points over A. The margin comes from its fixed PCB datum,
stationary workholding and probe, service access, and better alignment
opportunity at the base. A scores well on fixed-gantry stiffness and
printability but gives those advantages back through a moving bed, moving
datum, and longer rail/bed support problem. C is not retained just to create a
third row: its fixed-bed benefit is real, but the extra moving-head stack
creates a longer force loop and more PETG alignment interfaces.

## Sensitivity check

Each scenario doubles the listed criterion-group weights and renormalizes the
total to 100. It is a deliberate weight perturbation, not a statistical
confidence interval.

| Weight emphasis | A | B | C | Result |
| --- | ---: | ---: | ---: | --- |
| base | 73.6 | 77.0 | 53.2 | B |
| stiffness-led: tool point, Z, torsion, loop | 75.6 | 76.8 | 53.0 | B, narrow margin |
| datum/probing-led | 72.6 | 78.7 | 56.1 | B |
| printability-led: joints, creep, print size/material | 74.0 | 76.5 | 52.7 | B |
| service/access-led | 72.2 | 76.9 | 51.9 | B |

B remains the screening winner under the tested perturbations, but the
stiffness-led margin is narrow. That is why the Phase 2 gate requires a
representative B gantry load/creep test and keeps A as the explicit fallback.
If B fails the 5 N tool-point target or the 0.040 mm non-compensatable Z
allocation, the architecture review reopens rather than hiding the result in
height mapping.

The matrix is generated and tested by `cad/architecture.py`; the integer
scores remain review judgments, not measured performance.

## Current Phase 2A disposition

Phase 2A removes C from the focused structural comparison, independently
optimizes A and B for predominantly PETG geometry, and uses a revised matrix
without a second bending criterion that would double-count the total
deflection result. The current result is A 78.0 and B 75.2, but this is still
proposed evidence pending representative printed coupons and owner review.
