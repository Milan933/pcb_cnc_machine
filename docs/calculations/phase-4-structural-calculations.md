# Phase 4 preliminary structural calculations

## Boundary

This is an auditable equivalent-section screen for the P2 preliminary
structural concept. It is not FEA, a strength calculation, a fatigue/creep
prediction, or measured PETG performance. The effective modulus, section
properties, interface stiffnesses, and rotational stiffness are preliminary
inputs and must be replaced or bounded by coupons and force-loop tests.

The implementation is `cad/phase4_calculations.py`; the centralized inputs
are in `PHASE4_STRUCTURAL_PARAMETERS`.

## Inputs

| Input | Value | Status |
| --- | ---: | --- |
| Tool-point test load | 5.0 N | Phase 1 accepted screening load |
| Effective PETG modulus | 2000 N/mm² | Preliminary effective screen |
| Effective Poisson ratio | 0.35 | Preliminary screen |
| Closed beam section | 90 x 90 x 6 mm | Preliminary concept section |
| Clear beam span | 280 mm | Accepted P2 architecture reference |
| Tower support length | 62 mm | Preliminary concept geometry |
| Tool-point arm | 50 mm | Accepted process/motion screen |
| Racking offset | 100 mm | Phase 2A screening convention |
| Equivalent J1 stiffness | 1800 N/mm | Preliminary interface allowance |
| Equivalent X/Z stiffness | 1800 N/mm | Preliminary interface allowance |
| Equivalent base stiffness | 3000 N/mm | Preliminary interface allowance |
| Equivalent rail-seat stiffness | 2500 N/mm | Preliminary PETG/datum allowance |
| Equivalent moving-bed stiffness | 4000 N/mm | Preliminary ribbed-bed allowance |
| Racking rotational stiffness | 30,000,000 N-mm/rad | Preliminary interface allowance |

## Equations

For the rectangular closed section, the strong-axis second moment is screened
as:

```text
I = [b h^3 - (b - 2t)(h - 2t)^3] / 12
```

For the beam center load, the existing simply-supported equivalent is used:

```text
delta_beam = F L^3 / (48 E I)
```

The thin-wall closed-section torsion screen uses the documented torsion
constant from `cad/phase2a.py`, with the 250 N-mm tool torque and half-span
load path. Tower bending uses the two equal tower reactions. Joint, X/Z,
base, rail-seat, and bed compliance are added as force/stiffness terms:

```text
delta_i = F / k_i
```

The asymmetric racking allowance is:

```text
theta = F * offset / K_theta
delta_racking = theta * tool_arm
```

The final screen is additive:

```text
delta_tool = sum(delta_beam, delta_torsion, delta_towers,
                 delta_joint, delta_XZ, delta_base,
                 delta_rail_seat, delta_bed) + delta_racking
```

## Result

| Contribution | Displacement (mm) | Method |
| --- | ---: | --- |
| Gantry beam bending | 0.000479805 | 90 x 90 x 6 mm closed-section equivalent |
| Gantry beam torsion | 0.000664328 | Thin-wall closed-section screen |
| Gantry tower bending | 0.000198607 | Two tower reactions, effective tower I |
| Gantry joint | 0.002777778 | 5 N / 1800 N/mm |
| X/Z structure | 0.002777778 | 5 N / 1800 N/mm |
| Base | 0.001666667 | 5 N / 3000 N/mm |
| Rail-seat/interface allowance | 0.002000000 | 5 N / 2500 N/mm |
| Moving-bed support | 0.001250000 | 5 N / 4000 N/mm |
| Direct stack | 0.011814962 | Sum before racking |
| Asymmetric-force racking | 0.000833333 | 5 N at 100 mm / 30,000,000 N-mm/rad, multiplied by 50 mm arm |
| **Total tool-point screen** | **0.012648296** | **Preliminary calculated value** |

The current screen is below the Phase 1 target of 0.020 mm and the
0.030 mm acceptance limit. The largest direct contribution is tied between
the provisional J1 gantry joint and the X/Z structure at 0.002777778 mm; the
rail-seat/interface allowance is the next largest. This ranking is a design
priority, not a measured failure-mode ranking.

## Required evidence and limits

The result must not be promoted to a verified value until:

1. the actual rail, spindle, carriage, and fastener dimensions are measured;
2. representative beam, tower, J1, rail-seat, bearing-pocket, insert, and bed
   coupons are printed in the proposed orientations and conditioned;
3. tool-point displacement is measured at 5 N with the contributions separated
   into gantry beam, tower/joint, X/Z, base, rail-seat, and bed effects;
4. creep and repeated-disassembly effects are bounded; and
5. the 230 x 180 mm bed retains its PCB datum under workholding and cable
   loads.

The Phase 4 validator fails if the calculated screen exceeds 0.030 mm. A
target miss would remain an explicit engineering result, not be converted to a
pass. The current code also reports the evidence status as calculated and not
experimentally verified.
