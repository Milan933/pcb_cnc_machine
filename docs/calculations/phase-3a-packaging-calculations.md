# Phase 3A packaging calculations

These are dimensional screening calculations for the review-only packaging
variants. They do not establish rail preload, screw straightness, PETG
stiffness, motor torque at speed, spindle clearance under vibration, or
manufacturing tolerances.

## Why the current skeleton reaches 384.3 x 384.3 x 300.65 mm

The Phase 3 skeleton bounding box is the union of nominal reference envelopes,
not a detailed frame. Its extrema are approximately:

| Direction | Lower/upper cause | Extent |
| --- | --- | ---: |
| X | fixed-gantry/body reference to the recessed-side X motor/support; opposite side ends at the gantry bound | -214.3 to +170.0 = 384.3 mm |
| Y | front Y motor/support to the rear structural/guide reference | -214.3 to +170.0 = 384.3 mm |
| Z | underside of the Y motor envelope to the upper Z motor envelope | -50.65 to +250.0 = 300.65 mm |

The rounded machine envelope was therefore set to 400 x 400 x 310 mm. The
dominant packaging causes are the exposed X/Y motor and bearing support
envelopes, long reference rails with no explicit swept-carriage proof, the
240 x 190 mm bed, and the upper Z motor stack. The 220 mm Y rail spacing is a
transverse dimension; it is not itself a 220 mm front-to-rear requirement.

## Swept rail-length equation

For two carriages on one rail, the minimum rail length screen is:

```text
L_rail,min = tool travel
             + (carriage-center spacing + block length)
             + 2 * declared end margin
```

The HIWIN reference block lengths used by the Phase 3 screen are 47.6 mm for
MGN12H and 39.9 mm for MGN9H. The group span is measured between the outer
faces of the two blocks, not between their centers alone.

### P1 / P2 / P3 rail stacks

| Variant/axis | Travel | Block group | End margin each end | Calculated minimum | Selected rail | Free margin each end |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 X / MGN12H | 220.0 | 127.6 (centers +/-40) | 10.0 | 367.6 | 370 | 11.2 |
| P1 Y / MGN12H | 170.0 | 147.6 (centers +/-50) | 10.0 | 337.6 | 340 | 11.2 |
| P1 Z / MGN9H | 40.0 | 89.9 (centers +/-25) | 5.0 | 139.9 | 145 | 7.55 |
| P2 X / MGN12H | 220.0 | 107.6 (centers +/-30) | 6.0 | 339.6 | 340 | 6.2 |
| P2 Y / MGN12H | 170.0 | 127.6 (centers +/-40) | 6.0 | 309.6 | 310 | 6.2 |
| P2 Z / MGN9H | 40.0 | 79.9 (centers +/-20) | 5.0 | 129.9 | 130 | 5.05 |
| P3 X / MGN12H | 210.0 | 95.6 (centers +/-24) | 5.0 | 315.6 | 320 | 7.2 |
| P3 Y / MGN12H | 160.0 | 107.6 (centers +/-30) | 4.0 | 275.6 | 280 | 6.2 |
| P3 Z / MGN9H | 40.0 | 79.9 (centers +/-20) | 2.0 | 123.9 | 125 | 2.55 |

This exposes why the earlier 300/280/100 mm references were not sufficient
evidence for 220/170/40 mm full swept travel with two carriages per rail.

## Screw and speed screen

The nominal screw cut envelope adds approximately 20 mm beyond the screened
unsupported span for end engagement/support packaging. The critical-speed
screen uses the existing pinned-pinned equation and the existing 70% margin.

| Variant | X screw / unsupported; 70% feed screen | Y screw / unsupported; 70% feed screen | Z screw / unsupported; 70% feed screen |
| --- | --- | --- | --- |
| P1 | 390 / 370 mm; 477 mm/min; commission 450 | 360 / 340 mm; 565 mm/min; commission 550 | 160 / 145 mm; 1,553 mm/min; commission 1,200 |
| P2 | 360 / 340 mm; 565 mm/min; commission 520 | 330 / 310 mm; 679 mm/min; commission 650 | 145 / 130 mm; 1,932 mm/min; commission 1,100 |
| P3 | 340 / 320 mm; 638 mm/min; commission 580 | 300 / 280 mm; 833 mm/min; commission 700 | 140 / 125 mm; 2,089 mm/min; commission 1,100 |

These are commissioning caps, not performance claims. P2 deliberately lowers
the Phase 3 preliminary X/Y commissioning feeds because packaging-corrected
screw spans reduce the conservative whip-screen feed margin.

## P2 X/Y dimensional chains

The recommended P2 retains the full Phase 3 tool travel:

```text
X: 200 PCB width + 2*10 tool access = 220 tool travel
   + 107.6 two-block group + 2*6 end margin = 339.6 -> 340 mm rail
   + fixed/floating support and direct motor pocket = 360 mm nominal screw
   + 12 mm side/end structural allowance = 364 mm body width

Y: 150 PCB depth + 2*10 tool access = 170 tool travel
   + 127.6 two-block group + 2*6 end margin = 309.6 -> 310 mm rail
   + fixed/floating support and direct front motor pocket = 330 mm nominal screw
   + 180 bed depth + 170 full sweep + 2*3 body clearance = 356 mm body depth
```

The guide spacing remains 220 mm across X. The 230 mm P2 bed therefore has
5 mm transverse overhang per side; it does not need to cover the full width of
the two carriage rows.

## Bed study

| Variant | Bed support | PCB perimeter | Bed over guide spacing | Longitudinal bed overhang beyond carriage group | Full-sweep body clearance/end | Y motor vertical gap |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| P1 | 240 x 190 x 8 | 20 / 20 | 10 | 21.2 | 12.5 | 4.85 |
| P2 | 230 x 180 x 8 | 15 / 15 | 5 | 26.2 | 3.0 | 4.85 |
| P3 | 220 x 170 x 8 | 10 / 10 | 0 | 31.2 | 2.0 | 2.85 |

The full-sweep clearance is checked with a union envelope of bed depth plus Y
tool travel. Workholding defaults to tape and low-profile edge clamps. P1/P2
leave a plausible future vacuum perimeter; P3 remains conditional and should
not assume a vacuum seal.

## P2 Z stack

The Z values overlap in space; they must not be added as if every envelope were
serial. With the workholding reference plane at Z=0:

```text
bed support underside                 -8.0 mm
spoilboard reference underside       -12.0 mm (overlapping layer)
maximum PCB thickness                  2.0 mm (screening value)
tool stickout                         15.0 mm
spindle envelope length              120.0 mm
tool + spindle upper reference       135.0 mm
Z carriage group                     44.05 to 123.95 mm
Z rail envelope                       19.0 to 149.0 mm
fixed Z support top                  168.5 mm
upper Z motor top                    218.5 mm
Y motor underside                   -55.15 mm
fixed gantry upper reference         110.0 mm
declared package                    -56.0 to 220.0 mm = 276.0 mm
```

The package height is driven by the lower Y motor/base bound and upper Z motor
bound, not by tall workpieces. The actual spindle diameter, tool-change
clearance, outline/surfacing reach, and guarding remain open until the spindle
is measured.
