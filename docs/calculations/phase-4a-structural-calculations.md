# Phase 4A structural optimization calculations

## Boundary

This is a preliminary before/after equivalent-section screen. It is not FEA,
not a strength or fatigue calculation, and not measured PETG performance.
Beam geometry terms are separated from assumed tower, joint, X/Z, base,
rail-seat, bed, and racking allowances. All assumed terms require coupons or
a separated physical force-loop test.

The implementation is [cad/phase4a_calculations.py](../../cad/phase4a_calculations.py).
The controlled runner is [run_phase4a_optimization.py](../../tools/run_phase4a_optimization.py).

## Controlled comparison

| Variant | Beam wall screen | Equivalent joint stiffness N/mm | X/Z stiffness N/mm | Base stiffness N/mm | Rail/interface stiffness N/mm | Bed stiffness N/mm | Racking stiffness N-mm/rad | Total mm |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Phase 4 baseline | 6.0 mm | 1,800 | 1,800 | 3,000 | 2,500 | 4,000 | 30,000,000 | 0.012648 |
| O1 | 6.0 mm | 2,300 | 2,100 | 3,300 | 2,800 | 4,200 | 32,000,000 | 0.011170 |
| **O2** | **5.0 mm** | **3,200** | **2,700** | **4,400** | **3,200** | **4,500** | **36,000,000** | **0.009410** |
| O3 | 5.0 mm | 4,200 | 3,000 | 5,200 | 3,500 | 4,600 | 40,000,000 | 0.008427 |

The O1/O2/O3 stiffness values are controlled architecture screens, not
measurements. O2 is not selected because the assumptions are optimistic; it
is selected because its geometry and service boundary are more reviewable than
O3 while its screen is comfortably below the preferred target.

## O2 contribution breakdown

| Contribution | Displacement mm | Classification | Basis |
| --- | ---: | --- | --- |
| Gantry beam bending | 0.000556592 | Geometry-derived estimate | 90 x 90 mm closed-section screen, 5 mm equivalent wall, 280 mm clear span |
| Gantry beam torsion | 0.000769387 | Geometry-derived estimate | Thin-wall closed-section torsion screen and 50 mm tool arm |
| Tower compliance | 0.000165506 | Assumed allowance | Equivalent tower I = 600,000 mm4; integrated shoulder not measured |
| Gantry joints | 0.001562500 | Assumed allowance | Equivalent remaining J1/interface stiffness = 3,200 N/mm |
| X/Z structure | 0.001851852 | Assumed allowance | Equivalent coherent backbone stiffness = 2,700 N/mm |
| Base | 0.001136364 | Assumed allowance | Equivalent integrated base/member stiffness = 4,400 N/mm |
| Rail/interface allowance | 0.001562500 | Assumed allowance | Equivalent rail-seat, shim, and fastener allowance = 3,200 N/mm |
| Y bed | 0.001111111 | Assumed allowance | Equivalent ribbed bed stiffness = 4,500 N/mm |
| Asymmetric-force racking | 0.000694444 | Assumed allowance | 5 N, 100 mm lateral offset, 36,000,000 N-mm/rad |
| **Total tool-point screen** | **0.009410256** | **Preliminary** | Direct stack 0.008715812 mm plus racking |

The dominant O2 contribution is the assumed X/Z structure allowance
(approximately 19.7% of total), followed by gantry joint and rail/interface
allowances (approximately 16.6% each). The ranking is a design priority, not
a measured failure-mode ranking.

## Method

For the rectangular closed-section screen:

    I = [b h^3 - (b - 2t)(h - 2t)^3] / 12

Beam bending, beam torsion, and tower compliance are written as geometry or
equivalent-section terms. Interface terms use:

    delta_i = F / k_i

Asymmetric racking uses:

    theta = F * offset / K_theta
    delta_racking = theta * tool_arm

The total is the additive direct stack plus the racking allowance. The
calculation uses the 5 N Phase 4/P2 screening load, 2,000 N/mm2 effective PETG
modulus, 0.35 Poisson ratio, and 50 mm tool-point arm.

## Required evidence

Before any calculated value can be treated as a design acceptance result:

1. measure the actual rail, carriage, screw, nut, bearing, motor, coupler,
   spindle, insert, and fastener interfaces;
2. print and condition beam, tower, J1, rail-seat, bearing-pocket, insert,
   base/Y, and bed coupons in the proposed orientations;
3. measure 5 N tool-point displacement with beam, tower/joint, X/Z, base,
   rail-seat, and bed contributions separated where practical;
4. bound PETG creep, thermal conditioning, preload retention, and repeated
   disassembly; and
5. measure the moving-bed datum under PCB workholding and cable loads.

The reported O2 result is therefore **preliminary and not experimentally
verified**.
