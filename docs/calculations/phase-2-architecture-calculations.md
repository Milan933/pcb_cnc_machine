# Phase 2 architecture calculations

These calculations are deliberately low-order screening tools. They bound
interfaces and expose dominant terms; they are not FEA, supplier data, or
physical validation.

## Controlled inputs

| Input | Value | Status / source |
| --- | ---: | --- |
| PCB working area | 200 x 150 mm | owner-accepted Phase 1 baseline |
| tool-point travel skeleton | 220 x 170 x 40 mm | preliminary packaging assumption |
| 5 N tool-point load | 5 N | owner-accepted Phase 1 test load |
| tool-point overhang | 50 mm | Phase 1 preferred screening value |
| Z guide center spacing | 60 mm | Phase 2 preliminary interface |
| gantry clear span | 280 mm | Phase 2 preliminary skeleton |
| gantry section depth | 60 mm | Phase 2 geometry-only screening bound |
| effective PETG modulus for comparison | 2,000 N/mm² | conservative modeling assumption; must be replaced/validated |
| nominal print preferred XY dimension | 300 mm | Owner-directed PETG modularity constraint |
| nominal print conservative maximum | 320 mm | Owner-directed PETG modularity constraint |

## Tool moment and guide couple

```text
M_tool = F * e = 5 N * 50 mm = 250 Nmm
F_guide_couple = M_tool / s = 250 Nmm / 60 mm = 4.17 N
```

This couple is only available when the Z guides are separated. The single
MGN12 candidate has one reaction line, so it is not treated as equivalent to
two rails. Dual MGN9 and dual MGN12 share the same 60 mm interface in this
phase; the larger rail class is preferred provisionally for seat and moment
margin, not frozen.

## Idealized gantry bending comparison

For a simply supported beam with a central transverse load:

```text
delta = F*L^3 / (48*E*I)
I = b*h^3 / 12
```

Using an intentionally idealized 40 x 60 mm section, 280 mm span, 5 N load,
and 2,000 N/mm² effective modulus:

```text
I = 40*60^3/12 = 720,000 mm^4
delta_ideal = 5*280^3 / (48*2,000*720,000) ~= 0.0016 mm
```

This value is not a machine claim. It omits the PETG layer direction, local
wall buckling, fastener bearing, rail-seat compliance, side joints, spindle
mass, and creep. It only shows why a deeper closed path is more valuable than
an extrusion-like thin profile.

## Force-loop path index

The skeleton bookkeeping path lengths are approximately:

| Candidate | Path-length screen | Normalized to B |
| --- | ---: | ---: |
| A moving bed | 360 mm | 1.09 |
| B moving gantry | 330 mm | 1.00 |
| C moving XY head | 470 mm | 1.42 |

The path index is used only to expose leverage and joint count. The actual
dominant compliance must be measured on a representative printed structure.

## Travel and packaging references

The skeleton uses a 10 mm nominal access margin at each edge of the accepted
working area:

```text
X travel = 200 + 2*10 = 220 mm
Y travel = 150 + 2*10 = 170 mm
```

The reference lines add 30 mm end margins for rail/screw supports:

| Axis | Tool travel | Rail centerline length | Screw reference length |
| --- | ---: | ---: | ---: |
| X | 220 mm | 280 mm clear-span reference | 340 mm including two 30 mm end margins |
| Y | 170 mm | 230 mm including two 30 mm end margins | 290 mm including two additional screw margins |
| Z | 40 mm | 100 mm including two 30 mm end margins | 100 mm reference |

These are not purchased rail or screw lengths. Carriage length, bearing
supports, coupler access, hard stops, homing, and service clearance remain
Phase 3 packaging inputs.

## Screw command-resolution comparison

For a 200-step/rev motor and 16 commanded microsteps:

```text
T8x2: 2 / (200*16) = 0.000625 mm/commanded microstep
T8x4: 4 / (200*16) = 0.00125  mm/commanded microstep
```

These are command increments only. They do not select T8x2 or T8x4 and do not
prove accuracy, repeatability, backlash, speed, or torque margin. The lead
choice moves to Phase 3 with the actual motor, driver voltage/current,
acceleration, screw critical speed, bearing arrangement, nut preload, and
contamination requirements.

## Z error budget carried forward

The Phase 2 architecture must preserve the owner-accepted Phase 1 values:

- non-compensatable allocation: 0.040 mm;
- post-map residual target: <=0.020 mm;
- first-prototype post-map acceptance: <=0.030 mm.

The fixed B bed improves map validity and workholding repeatability, but it
does not reduce the structural allocation until a 5 N test, probing test,
workholding test, and thermal/creep evidence exist.
