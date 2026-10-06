# Phase 3 motion-system selection

**Status:** owner-accepted component-class baseline; physical evidence open
**Date:** 2026-10-06
**Architecture:** A — fixed PETG gantry with moving Y PCB bed
**Decision record:** [EDR-008](../decisions/008-phase-3-motion-system.md)

## Boundary and recommendation

The owner has accepted Architecture A as the mechanical architecture baseline.
The B moving-gantry/fixed-bed architecture remains documented as the primary
rejected alternative and is not being physically built. This phase selects a
complete preliminary motion layout before detailed structural CAD; it does not
freeze detailed geometry or authorize production parts.

The owner accepted this component-class baseline on 2026-10-06. The P2
packaging record later corrected the review lengths to 340/310/130 mm rails and
360/330/145 mm nominal screws; the motion classes and topology below are
unchanged. The reference layout is:

| Axis | Guide arrangement | Reference rail class | Screw lead class | Travel / reference length |
| --- | --- | --- | --- | --- |
| X | two rails, two long blocks per rail | MGN12H | T8x4 | 220 / 340 mm rail, 360 mm screw |
| Y | two rails, two long blocks per rail | MGN12H | T8x4 | 170 / 310 mm rail, 330 mm screw |
| Z | two rails, two long blocks per rail | MGN9H | T8x2 | 40 / 130 mm rail, 145 mm screw |

The H blocks are long-block reference envelopes. The actual supplier, preload,
rail straightness, end preparation, and fastener interface remain open until
sample hardware is measured. MGN12 is the conservative PETG-seat choice for
the long X/Y spans; MGN9H is retained for the short Z axis because the
separated 60 mm guide plane has a large moment margin and the smaller blocks
reduce Z mass. If the Z coupon or tool-point test misses its stiffness target,
the controlled fallback is dual MGN12H, not a single rail.

## Guideway comparison

The following are official HIWIN MGN-C/MGN-H reference values, used to make the
class comparison quantitative. They are not a claim that a future marketplace
rail has the same preload, straightness, material, or capacity. See the
[HIWIN MGN/MGW dimension and rating catalog](https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E-2.pdf).

| Reference block | Assembly W x H (mm) | Block L (mm) | C / C0 (kN) | Static moments Mr / Mp / My (N-m) | Block mass |
| --- | ---: | ---: | ---: | ---: | ---: |
| MGN9C | 20 x 10 | 30.0 | 2.01 / 2.84 | 13.05 / 8.97 / 8.97 | 0.012 kg |
| MGN9H | 20 x 10 | 39.9 | 2.50 / 3.93 | 19.71 / 21.47 / 21.47 | 0.020 kg |
| MGN12C | 27 x 13 | 35.0 | 2.84 / 3.92 | 25.48 / 13.72 / 13.72 | 0.025 kg |
| MGN12H | 27 x 13 | 47.6 | 4.27 / 5.90 | 38.40 / 37.49 / 37.49 | 0.047 kg |

Both families use an M3 rail fastener in this reference catalog and are
available in common small-CNC channels. MGN9 is lower mass and typically lower
cost; MGN12 has a wider rail, more mounting area, higher long-block moment
ratings, and a better PETG rail-seat margin. Availability and clone quality
are a risk for both, so the purchase rule is sample-first and measure-first.

| Trade property | MGN9 class | MGN12 class | Phase 3 consequence |
| --- | --- | --- | --- |
| Capacity / moment | lower absolute load and moment rating; adequate only with the separated short-Z plane | higher long-block capacity and moment rating | MGN12 is the X/Y baseline; MGN9 is conditional Z only |
| Carriage / preload | C is shorter/lighter; H is the long-block reference; preload code and drag must be measured | same C/H choice, with longer/wider H block | Use H reference blocks, then verify the actual preload and carriage drag |
| Guide stiffness | lower section and rail-seat margin; more sensitive to PETG distortion | wider rail and higher section/seat margin | MGN12 better for long spans and printed rail seats |
| Mounting sensitivity | M3 fasteners and narrow 20 mm assembly width demand a flat, supported seat and edge-distance check | still M3, but 27 mm assembly width gives more distributed PETG support | Both need a post-processed datum or metal-backed/through-bolted interface |
| PETG suitability | acceptable for short Z if the rail seat is conditioned and the plate is stiff | preferred where rail-seat creep/alignment dominates | Do not rely on infill to compensate for a warped seat |
| Mass / packaging | 0.020 kg MGN9H block and 0.38 kg/m rail reference | 0.047 kg MGN12H block and 0.65 kg/m rail reference | MGN9 saves moving Z mass; MGN12 mass is acceptable on fixed X/Y and bed-supported Y |
| Cost / availability class | low-cost / widely available marketplace class | medium-cost / widely available marketplace class | No production quantity until supplier/sample inspection |

The chosen rail count is dual rail with two carriages per rail on X, Y, and Z.
A single MGN12 rail with two carriages remains a packaging fallback for a
non-load-bearing guide experiment only; it is not the motion baseline because
it does not establish a separated moment-reaction plane.

A single rail with two carriages gives a good in-line load path but cannot
create the same separated reaction plane for pitch/roll or racking. The
baseline therefore uses two rails and two blocks on each rail for every axis.
This is four blocks per axis, not a claim that every block sees equal load.

### Spacing derivation

The Phase 1 static screen uses 5 N at a 50 mm tool overhang, giving 250 N-mm.
The ideal differential guide reaction is `M / spacing`:

| Axis | Spacing | 250 N-mm tool moment reaction | 500 N-mm asymmetric/racking screen |
| --- | ---: | ---: | ---: |
| X | 60 mm vertical rail separation | 4.17 N | 8.33 N |
| Y | 220 mm rail separation | 1.14 N | 2.27 N |
| Z | 60 mm rail separation | 4.17 N | 8.33 N |

These reactions are far below the catalog load and moment ratings before
mounting-surface and joint effects are included. The dominant uncertainty is
therefore PETG rail-seat flatness, preload retention, carriage play, plate
compliance, and the actual load direction—not catalog load capacity alone.

## Screw and transmission comparison

The screening motor is a typical 200-step/rev, 1.8-degree NEMA17. The
controller resolution is `steps/mm = (steps/rev x microsteps) / lead`. It is
command granularity only; it is not absolute accuracy, repeatability, or
backlash. GRBL documents the same relationship and warns that unnecessarily
high microstepping can reduce available stepper torque in its
[settings documentation](https://github.com/gnea/grbl/blob/master/doc/markdown/settings.md?plain=1).

| Axis | Lead | Full step increment | 8 microsteps | 16 microsteps | 32 microsteps | 50 N screw torque screen |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| X/Y | T8x4 | 0.020 mm | 0.0025 mm / 400 steps-mm | 0.00125 mm / 800 | 0.000625 mm / 1600 | 0.09095 N-m |
| Z | T8x2 | 0.010 mm | 0.00125 mm / 800 steps-mm | 0.000625 mm / 1600 | 0.0003125 mm / 3200 | 0.04547 N-m |

T8x4 is recommended for X/Y because the 4 mm lead reduces screw rpm and makes
the 220/170 mm travel practical without giving up the Phase 1 command target
at full step. T8x2 is recommended for Z because it gives more axial mechanical
advantage, better gravity-hold behavior, and a higher command density at the
same microstep setting. T8x2 is not automatically self-locking with every
nut, lubricant, and load condition; the Z axis still requires a holding and
power-off test.

The 50 N axial force is a conservative motion-screening load, not a measured
cutting force. The Phase 2A analytical Y forces were only 1.498 N for A and
2.540 N for B; those values are also calculated, not measured. The torque
screen omits starting friction, anti-backlash preload, misalignment,
acceleration, and the motor torque-speed curve. It cannot select a motor by
itself.

### Whip and feed screen

Using a 6.2 mm root-diameter approximation, steel `E = 200 GPa`, density
`7.85e-6 kg/mm^3`, and a pinned-pinned screening equation gives:

| Axis | Unsupported screw length | Estimated critical speed | 70% screen | 70% feed at selected lead | Commissioning cap |
| --- | ---: | ---: | ---: | ---: | ---: |
| X / T8x4 | 300 mm | 259 rpm | 181 rpm | 725 mm/min | 600 mm/min |
| Y / T8x4 | 280 mm | 297 rpm | 208 rpm | 833 mm/min | 700 mm/min |
| Z / T8x2 | 120 mm | 1,619 rpm | 1,133 rpm | 2,267 mm/min | 1,200 mm/min |

The end condition, straightness, nut position, bearing runout, and coupler
alignment can reduce these values. The commissioning caps are practical
starting limits, not guaranteed maximum feeds. Motor torque at speed and
missed-step margin must be tested before increasing them.

## Bearing, nut, and coupler philosophy

Each screw has one axial fixed end and one radially supported floating end:

| Axis | Fixed end | Floating end | Motor/coupler position |
| --- | --- | --- | --- |
| X | left motor end, paired angular-contact or compact BK08-class support | right radial BF08-class support | motor outside fixed support; flexible 5-to-8 mm coupler |
| Y | front motor end, paired axial support | rear radial support | motor outside front support; flexible coupler |
| Z | upper motor end, paired axial support | lower radial-only support | motor above fixed support; flexible coupler |

The 8 mm bore is a generic T8 end-envelope, not a bearing vendor selection.
The coupler is torque-only: it must not be used as an axial bearing or as a
way to absorb screw thrust. The fixed support, bearing fit, shoulder, and nut
preload must form the axial load loop.

| Nut class | Advantage | Risk | Phase 3 disposition |
| --- | --- | --- | --- |
| Standard brass | cheap and common | uncontrolled reversal clearance and wear | sample only; not the X/Y default |
| Spring-preloaded split brass / dual brass | adjustable, serviceable, low-cost | drag, spring relaxation, inconsistent clone geometry | recommended X/Y class |
| POM or other polymer anti-backlash | quiet and low friction | creep, temperature sensitivity, wear, uncertain preload | controlled alternative after cycling test |
| Ball screw or precision rolled screw | lower friction and potentially lower backlash | cost, packaging, contamination, nut preload and size | not justified before the T8 screen and physical evidence |

The provisional X/Y backlash target is <=0.030 mm. Software compensation is
not a substitute for mechanical preload, a measured reversal offset, or a
replaceable worn nut. Z preload must be checked for drag, gravity creep, and
power-off descent.

## Motor and controller acceptance envelope

No exact owner motor is selected until its label, shaft, current, holding
torque, condition, and torque-speed behavior are recorded. Motors are
owner-supplied and must not be purchased at this stage. Preliminary structural
CAD uses a standardized common NEMA17 interface; the acceptance envelope is:

- 42.3 mm NEMA17 mounting square;
- 40-48 mm body length for the initial packaging envelope;
- 5 mm shaft with approximately 20 mm usable engagement, pending measurement;
- rear connector, wiring bend, strain-relief, and service access for common
  40-48 mm 3D-printer motor bodies, pending representative measurement;
- at least 0.45 N-m holding torque for X/Y and 0.55 N-m for Z as screening
  minima, with torque at operating speed still to be verified;
- a rated phase current that can be set safely on the identified driver with
  thermal margin; the present 0.8-1.5 A range is a test window, not a motor
  specification.

The controller platform is owner-supplied Arduino Mega + CNC Shield with a
GRBL-compatible STEP/DIR configuration strategy. A4988 carriers are commonly
limited to 1/16 microstep by the [Allegro A4988 product
documentation](https://www.allegromicro.com/en/products/motor-drivers/brush-dc-motor-drivers/a4988);
the TI DRV8825 supports up to 1/32 microstep and documents an 8.2-45 V supply
range in its [official datasheet](https://www.ti.com/lit/ds/symlink/drv8825.pdf).
Those IC limits do not identify the actual plug-in carrier's thermal or
current capability.

The recommended starting setting is 8 microsteps on all three axes. 16 is a
calibration/quietness experiment only after missed-step and driver-temperature
tests; 32 is not the baseline. GRBL exposes independent steps/mm `$100-$102`,
maximum rates `$110-$112`, acceleration `$120-$122`, maximum travel
`$130-$132`, homing `$22-$27`, and spindle `$30-$31` settings in its
[official interface table](https://github.com/gnea/grbl/blob/master/doc/markdown/interface.md).
The exact CNC Shield revision and installed driver modules must be identified
before wiring because board pinouts, probe routing, driver cooling, current
capability, and spindle PWM implementation vary. Do not replace the platform
unless these checks demonstrate an actual limitation.

## Moving Y bed and workholding layout

The nominal moving support envelope is 240 x 190 x 8 mm, carrying a replaceable
spoilboard/PCB support envelope of 240 x 190 x 12 mm. A 200 x 150 mm board
therefore retains 20 mm nominal edge margin in X and Y for registration,
clamps, probing access, and cable clearance. The centered single Y screw is
the baseline; a second screw is a racking contingency only if the measured
bed/seat assembly cannot hold squareness.

The nominal Phase 2A moving-bed mass is 1.24 kg, including PCB, spoilboard,
printed support, workholding, Y hardware, and cable/probe allowance. It is a
planning estimate, not a weighed assembly. The motion layout uses the bed as
the moving Y datum; the fixed gantry carries X and Z, keeping the cutting
force loop independent of Y bed acceleration except at the tool/board
interface.

The motion layout envelope is approximately 400 x 400 x 310 mm before service
clearance. The current service footprint allowance is 520 x 520 x 370 mm,
including front loading, rear cable/bearing access, and top spindle/motor
clearance. These are packaging envelopes, not printable-part dimensions.

## Homing, limits, and coordinates

The project coordinates remain X right, Y rear, Z up. The proposed switches
are X negative/left, Y negative/front, and Z positive/up. For the moving bed,
positive machine Y means the bed and PCB move toward the rear; the cutter is
stationary in Y relative to the gantry. G54 is set on the registered PCB
datum: front-left board corner in X/Y and the probed board/copper surface in Z.
Cutting moves are negative Z from that work surface.

GRBL normally assumes positive-direction homing but permits inversion through
the homing direction mask; its homing routine records the machine position from
the configured travel and pull-off values. The recommended numeric convention
therefore leaves negative-home X/Y at approximately `-$27` after pull-off and
leaves positive-home Z at approximately `$132+$27`, rather than pretending the
switch closures are automatically numeric zero. See the [official homing settings
documentation](https://github.com/gnea/grbl/blob/master/doc/markdown/settings.md?plain=1)
and [limit/homing implementation](https://github.com/gnea/grbl/blob/master/grbl/limits.c).
G54 then hides that machine-coordinate convention by setting work zero on the
registered PCB datum. The final installation shall use normally closed,
fault-detectable switches if
the identified controller supports them, place hard limits near both ends,
enable soft limits only after measured travel is entered, and require homing
before a work coordinate is trusted. The conductive probe input must be
electrically verified, protected from spindle noise, and tested for an open or
broken probe before a height map is accepted.

## Sourcing and purchase boundary

Safe now for characterization, not final production:

- one measured MGN12 rail/block sample and one MGN9H rail/block sample;
- one T8x4 screw/nut sample and one T8x2 screw/nut sample at non-final length;
- one 8 mm fixed-support/floating-support and 5-to-8 mm coupler sample;
- a compatible motor-driver carrier only for bench identification/testing;
- one representative anti-backlash nut of each candidate class.

Do not yet buy production quantities or finalize geometry around:

- exact rail lengths, preload, or clone supplier;
- final screw straightness/end machining, bearing blocks, or nut preload;
- a spindle, motor set, or controller shield before their identifying data is
  recorded;
- printed rail seats, gantry plates, motor mounts, spindle mounts, or any
  production PETG structural part;
- a final workholding or probe installation that has not passed the datum and
  electrical checks.

The motion skeleton in `cad/assembly/motion_skeleton.py` uses only nominal
reference envelopes and is intentionally safe to change when the samples are
measured.

## Physical evidence carried forward

The Phase 2A beam, torsion, rail-seat, insert-creep, through-bolt-creep, and
A force-loop coupons remain mandatory. Phase 3 adds rail play/preload,
backlash/reversal, nut drag/wear, screw axial play, homing repeatability,
missed-step margin, axis straightness/squareness, and spindle-envelope
tool-point deflection tests. None is satisfied by the calculated values or the
review-only CAD skeleton.
