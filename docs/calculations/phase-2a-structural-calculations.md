# Phase 2A structural calculation record

**Status:** calculated screening evidence; not experimentally verified
**Source:** `cad/phase2a.py` and `cad/parameters.py`
**Date:** 2026-10-06

## Purpose and method

This record makes the focused A/B calculation auditable without FEA. It uses
equivalent PETG sections, explicit support and joint stiffness assumptions,
and a conservative additive racking term. It is intentionally not a shell
model, a finite-element solution, or a measured machine deflection result.

All lengths are millimetres and all forces are newtons. The common load is
`F = 5 N`, the tool-point overhang is `e = 50 mm`, and the resulting tool
moment is:

```text
T_tool = F*e = 5*50 = 250 Nmm
```

The material screen uses `E_eff = 2000 N/mm2` and `nu_eff = 0.35`, giving:

```text
G_eff = E_eff/(2*(1+nu_eff)) = 740.7407 N/mm2
```

These are controlled assumptions, not supplier or test data.

## Section properties

For each candidate, the equivalent rectangular strong-axis property is:

```text
I = b*h^3/12
```

The thin-wall closed-section approximation uses midline dimensions and:

```text
J = 4*A_m^2 / (perimeter_m/wall)
```

The resulting values are:

| Candidate | Equivalent section | `I` mm4 | `J` mm4 |
| --- | --- | ---: | ---: |
| A | 90 x 100, 4 wall | 7,500,000 | 2,996,111 |
| B | 60 x 70, 4 wall | 1,715,000 | 895,765 |

The A and B sections are optimized independently for their architecture
concepts. They are not forced to have equal mass, depth, or print shape.

## Deflection terms

The code evaluates:

```text
delta_gantry = F*280^3/(48*E_eff*I)
delta_torsion = (T_tool*140/(G_eff*J))*50
delta_support = (F/2)*L_support^3/(3*E_eff*I_support)
delta_Z = F/k_Z
delta_joint = F/k_joint
delta_racking = (F*100/k_theta)*100
```

Controlled candidate inputs:

| Input | A | B |
| --- | ---: | ---: |
| Support equivalent length `L_support` | 160 | 80 |
| Support equivalent `I_support` mm4 | 800,000 | 30,000 |
| Z equivalent stiffness `k_Z` N/mm | 2,000 | 1,428.5714 |
| Joint equivalent stiffness `k_joint` N/mm | 1,666.6667 | 625 |
| Racking rotational stiffness `k_theta` Nmm/rad | 20,000,000 | 10,000,000 |

Calculated outputs:

| Term | A mm | B mm |
| --- | ---: | ---: |
| Gantry bending | 0.00015244 | 0.00066667 |
| Gantry torsion | 0.00078852 | 0.00263741 |
| Side/support bending | 0.00213333 | 0.00711111 |
| Z carriage compliance | 0.00250000 | 0.00350000 |
| Structural joints | 0.00300000 | 0.00800000 |
| Direct stack | 0.00857430 | 0.02191519 |
| Asymmetric-force racking | 0.00250000 | 0.00500000 |
| **Total** | **0.01107430** | **0.02691519** |

Percentages of each candidate total are:

| Term | A | B |
| --- | ---: | ---: |
| Gantry bending | 1.3766% | 2.4769% |
| Gantry torsion | 7.1203% | 9.7990% |
| Side/support bending | 19.2638% | 26.4204% |
| Z carriage compliance | 22.5748% | 13.0038% |
| Structural joints | 27.0897% | 29.7230% |
| Asymmetric-force racking | 22.5748% | 18.5769% |

The direct stack deliberately excludes the racking term, then total adds it
once. This avoids double-counting the same rotational mechanism in the
structural matrix.

## Dynamic equations

For nominal Y acceleration `a = 0.20 m/s2`:

```text
F_accel = m*a
F_design = F_accel + mu*5 + F_cable
T_screw = F_design*lead/(2*pi*eta)/1000
```

The `/1000` converts Nmm to Nm. Results:

| Quantity | A | B |
| --- | ---: | ---: |
| Moving mass | 1.24 kg | 3.95 kg |
| Acceleration force | 0.248 N | 0.790 N |
| Friction equivalent | 0.750 N | 0.750 N |
| Cable/probe drag | 0.500 N | 1.000 N |
| Design force | 1.498 N | 2.540 N |
| T8x2 screw torque | 0.001362 Nm | 0.002310 Nm |
| T8x4 screw torque | 0.002725 Nm | 0.004620 Nm |

The dynamic output is a load implication only. It does not include motor
torque-speed curves, screw critical speed, bearing friction, preload, driver
current, or cutting force and therefore cannot select hardware.

For a relative resonance screen only, the study calculates `k_static =
F/delta_total` and `sqrt(k_static/m)`. The values are 19.08 for A and 6.86 for
B, ratio 2.78. These are proportional modal indices, not natural frequencies
in hertz; no frequency claim is made without measured modal stiffness and
mass participation.

## Racking equations

The asymmetric tool load is screened as:

```text
M = F*offset = 5*100 = 500 Nmm
Delta guide force = M/220 = 2.2727 N
Delta edge = M/k_theta*100
```

The centered screw is considered credible at the nominal acceleration only
with symmetric, preloaded guide lines. B's lower `k_theta` makes it the more
sensitive candidate to side-interface fit, creep, and friction mismatch.

## Matrix and sensitivity calculation

The 11 weights sum to 100 percent. Scores are ordinal 1-5 and are stored in
`PHASE2A_SCORES`; normalized score is:

```text
score = 100 * sum(weight_i*score_i/5) / sum(weight_i)
```

The base result is A 78.0 and B 75.2. Sensitivity doubles each listed group
and renormalizes:

| Scenario | A | B |
| --- | ---: | ---: |
| Structural evidence heavy | 83.4568 | 70.6173 |
| Calibration/usability heavy | 72.5000 | 80.6250 |
| Manufacturing heavy | 78.8060 | 69.8507 |
| Moving mass heavy | 80.0000 | 72.0000 |

These are decision-support numbers, not probabilities or confidence bounds.

## Limitations and model update path

The model cannot predict anisotropic print behavior, layer separation,
local wall buckling, rail/carriage catalogue compliance, insert pull-out,
through-bolt bearing, spindle runout, backlash, thermal drift, or a natural
frequency. It uses equivalent inputs so that those unknowns are visible and
replaceable. Coupon measurements shall replace `E_eff`, section properties,
`k_Z`, `k_joint`, `k_theta`, mass, friction, drag, and thermal/conditioning
allowances before the architecture is frozen.
