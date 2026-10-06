# Phase 3 motion calculations

**Evidence status:** calculated screening values only; no measured machine
performance is implied.

## Inputs

The controlled inputs are in
[`cad/parameters.py`](../../cad/parameters.py), under
`PHASE3_MOTION_PARAMETERS`:

- 200 x 150 mm usable PCB area;
- 220 x 170 x 40 mm screened tool travel;
- 5 N tool-point test load and 50 mm overhang;
- 60 mm X/Z guide spacing and 220 mm Y guide spacing;
- 200 full steps/rev, 0.35 screw efficiency screen;
- 6.2 mm T8 root-diameter approximation;
- steel screw `E = 200000 N/mm²`, density `7.85e-6 kg/mm³`;
- 70% of the calculated critical speed as a commissioning screen.

The 50 N screw design force is deliberately separate from the 5 N tool-point
deflection load. It is a conservative axial transmission screen, not a
measured cutting force.

## Resolution and torque

For motor full steps `S`, microsteps `m`, and screw lead `L`:

```text
steps/mm = S × m / L
command increment = L / (S × m)
```

For axial force `F`, lead `L`, and efficiency `η`:

```text
T = F × L / (2π η)
```

The lead is in millimetres in the source parameter model, so the calculation
converts the result to N-m. With `S = 200`, `F = 50 N`, and `η = 0.35`:

| Lead | Full-step increment | 8 microsteps | 16 microsteps | 32 microsteps | Input torque |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 mm | 0.010000 mm | 0.001250 mm / 800 steps-mm | 0.000625 mm / 1600 | 0.0003125 mm / 3200 | 0.045473 N-m |
| 4 mm | 0.020000 mm | 0.002500 mm / 400 steps-mm | 0.001250 mm / 800 | 0.000625 mm / 1600 | 0.090946 N-m |

The torque margin against the preliminary 0.45 N-m X/Y and 0.55 N-m Z holding
torque minima is a zero-speed screening ratio only. It does not account for
the torque-speed curve, acceleration, driver voltage/current, nut preload,
guide friction, or a stalled axis.

## Guide reaction screen

The ideal differential force from a moment couple is:

```text
ΔF = M / b
```

where `b` is the separated guide spacing. The 5 N load at 50 mm creates
`M = 250 N-mm`; an asymmetric 5 N force at a 100 mm arm creates
`M = 500 N-mm`.

| Guide plane | Spacing | 250 N-mm reaction | 500 N-mm reaction |
| --- | ---: | ---: | ---: |
| X | 60 mm | 4.1667 N | 8.3333 N |
| Y | 220 mm | 1.1364 N | 2.2727 N |
| Z | 60 mm | 4.1667 N | 8.3333 N |

This is a load-distribution screen. It does not convert catalog carriage
ratings into a printed-structure stiffness claim; rail-seat compliance,
fastener bearing, PETG creep, block preload, and carriage spacing must be
measured.

## Lead-screw critical speed

The review model treats the screw as a uniform round shaft with an approximate
root diameter `d`. For a round shaft, `I/A = d²/16`. The pinned-pinned natural
frequency screen is:

```text
f₁ = π / (2 L²) × sqrt(E × (I/A) / ρ)
critical rpm = 60 × f₁
```

Applying the 70% commissioning margin:

| Axis | Lead | Unsupported length | Critical rpm | 70% rpm | 70% feed |
| --- | ---: | ---: | ---: | ---: | ---: |
| X | 4 mm | 300 mm | 259.084 | 181.359 | 725.435 mm/min |
| Y | 4 mm | 280 mm | 297.418 | 208.192 | 832.770 mm/min |
| Z | 2 mm | 120 mm | 1,619.275 | 1,133.492 | 2,266.984 mm/min |

The model is intentionally conservative but incomplete. End-bearing condition,
screw straightness, rotating nut/motor parts, coupler alignment, and the
actual screw supplier can reduce usable speed. The selected commissioning
limits are 600, 700, and 1200 mm/min for X, Y, and Z, respectively.

## Moving-bed packaging

The moving support is 240 x 190 x 8 mm. The 200 x 150 mm PCB area leaves:

```text
X margin = (240 - 200) / 2 = 20 mm
Y margin = (190 - 150) / 2 = 20 mm
```

The 1.24 kg moving-bed mass is inherited from Phase 2A's nominal breakdown;
it must be replaced with a measured mass before acceleration and missed-step
limits are promoted.

## Reproducibility

The calculations are executable without build123d:

```text
python -B -m unittest discover -s tests -v
```

`cad/motion_phase3.py` is the calculation source. The Phase 3 runner adds the
nominal build123d reference layout and exports only to an explicit temporary
directory. A parameter-integrity pass does not close the Phase 3 engineering
gate; `phase3_gate_report()` remains not-ready until measured hardware and
physical motion evidence exist.
