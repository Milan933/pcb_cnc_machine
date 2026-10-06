# Phase 2A focused structural comparison: A versus B

**Status:** accepted Phase 2A baseline amendment; physical evidence remains open
**Date:** 2026-10-06
**Scope:** focused Phase 2A comparison only; Phase 3 is now owner-authorized,
but production CAD remains out of scope
**Units:** millimetres, newtons, kilograms, and seconds unless stated
otherwise

## Decision boundary

The opening comparison below is the historical pre-owner-review proposal.
The owner disposition is recorded in EDR-007: A is the accepted system
baseline, B is the documented rejected alternative, and physical evidence
remains open.

The original Phase 2 matrix was close: A scored 73.6 and B scored 77.0. That
result was a screening judgment, not proof that B is the better
predominantly-PETG structure. Phase 2A reopens only A versus B with the same
200 x 150 mm PCB baseline, 220 x 170 x 40 mm preliminary tool travel,
spindle envelope, guide-reference layout, PETG-first constraints, and 5 N
load philosophy. C is deliberately not part of this study.

The result below is a calculated structural screen. It is not an FEA result or
a measured stiffness value. The owner accepted A as the mechanical baseline;
the physical coupons and force-loop tests remain open. EDR-007 records the
boundary and does not accept Phase 3 or production CAD.

## Executive result

The independently optimized equivalent-section model gives:

| Result | A: fixed gantry / moving Y bed | B: moving Y gantry / fixed bed |
| --- | ---: | ---: |
| Total 5 N tool-point displacement | **0.0111 mm** | **0.0269 mm** |
| Direct additive stack, before asymmetric racking | 0.0086 mm | 0.0219 mm |
| Target <=0.020 mm | pass | miss |
| First-prototype acceptance <=0.030 mm | pass | pass |
| Estimated moving mass | **1.24 kg** | **3.95 kg** |
| Structural recommendation | provisional lead | process/usability alternative |

A is the current provisional structural baseline for PETG because it passes the
target with margin in this transparent model and has the lower moving mass.
B remains credible and attractive for a fixed PCB datum, probing, workholding,
and service. The difference is not yet trustworthy enough to freeze because
the largest inputs are equivalent joint, rail-seat, and PETG-process
assumptions rather than measured properties.

## Common baseline and controlled assumptions

| Input | Phase 2A value | Classification |
| --- | ---: | --- |
| PCB working area | 200 x 150 | accepted Phase 1 baseline |
| Tool travel screen | 220 x 170 x 40 | preliminary packaging assumption |
| Static tool load | 5 N at the tool point | accepted screening philosophy |
| Tool-point overhang | 50 | Phase 1 preferred screening value |
| Spindle screening envelope | 52 diameter x 120 length, 15 tool stickout | generic Phase 1 envelope; no spindle selected |
| Rail references | X separation 50, Y separation 220, Z separation 60 | architecture skeleton interfaces; no rail class selected |
| Effective PETG modulus | 2,000 N/mm2 | conservative equivalent-section assumption |
| Effective Poisson ratio | 0.35 | calculation assumption |
| PETG section constraint | 4 mm equivalent wall screen; closed/deep-ribbed/gusseted load path | geometry constraint, not detailed part CAD |
| Torsion half-span | 140 | equivalent load-path assumption |
| Racking force offset and tool arm | 100 and 100 | deliberately visible worst-edge screen |
| Y guide spacing | 220 | existing skeleton reference |
| Nominal Y acceleration | 0.20 m/s2 | low-speed process assumption; speed is secondary |
| Guide friction coefficient | 0.15 | conservative screening assumption |
| Screw efficiency | 0.35 | generic lead-screw assumption |
| Screw leads screened | T8x2 and T8x4 | not a selection |

The 2,000 N/mm2 modulus is not a claim about a particular filament or print
orientation. It is an effective value used consistently for both candidates.
The equivalent section and joint stiffness values are deliberately separated
from bulk material modulus so that rail seats, layer orientation, interfaces,
and fastener bearing are not hidden inside a falsely precise beam result.

## Independently optimized structural concepts

### A: fixed gantry, moving Y bed

A exploits the stationary gantry force path:

- integrated left/right supports and a deep closed U/monocoque review volume;
- 280 mm clear span, 320 mm outer width, and a 90 x 100 mm equivalent deep
  section for the structural calculation;
- wide base interfaces, short joints, neutral rail paths, and gusset/rib space;
- a one-piece U candidate within the Voron 350 envelope, with a multi-piece
  beam-plus-support fallback if warping or inspection requires it;
- a low-mass moving PCB/spoilboard bed, rather than carrying the spindle/Z/X
  stack on Y.

The moving bed is not free: PCB, spoilboard, registration, cable/probe loop,
and Y hardware move together. The board must remain registered and the height
map must be repeated or validity-checked after any bed movement.

### B: moving Y gantry, fixed bed

B exploits the stationary PCB datum:

- fixed PCB/spoilboard and fixed probing/workholding reference;
- a deep ribbed/closed crossbeam with a 60 x 70 mm equivalent section;
- separate side interfaces with an 80 mm support-bending screen length;
- distributed Y rail seats and a centered Y screw, with symmetric preload
  required to make one screw credible;
- explicit allowance for side-interface bending, racking, cyclic preload, and
  PETG creep.

B's moving assembly includes the printed gantry, side interfaces, Y hardware,
X rails/carriage/screw, Z guides/carriage/screw/mount, spindle allowance, and
cables/probe. Its fixed bed is a real process advantage, but it makes more
PETG structure participate in every Y acceleration cycle.

The Phase 2A review skeleton represents these concepts as named structural
bounding volumes only. It does not imply wall thickness, rib pitch, insert
geometry, rail selection, print orientation, or release-ready parts.

## Analytical structural model

The reproducible model is implemented in `cad/phase2a.py` and is intentionally
small enough to audit by inspection. It uses:

```text
I = b*h^3/12
delta_beam = F*L^3/(48*E*I)                 (central simply-supported beam)
delta_support = (F/2)*L^3/(3*E*I_support)  (support-pair screen)
J = 4*A_m^2 / sum(s/t)                     (thin-wall closed section)
delta_torsion = (T*L/(G*J))*tool_arm
delta_joint = F/k_joint
delta_racking = (F*offset/k_theta)*tool_arm
```

The total reported value is the sum of five direct contributions plus the
conservative asymmetric-racking term:

```text
delta_total = gantry bending + gantry torsion + support bending
              + Z carriage compliance + structural joints
              + asymmetric-force racking
```

The racking term is shown separately and added conservatively; it is not also
hidden in the beam or joint terms. The matrix has no separate generic
"bending" criterion in addition to the total static criterion, avoiding a
second score for the same result.

### Contribution results

| Contribution | A mm | A % | B mm | B % |
| --- | ---: | ---: | ---: | ---: |
| Gantry bending | 0.000152 | 1.38 | 0.000667 | 2.48 |
| Gantry torsion | 0.000789 | 7.12 | 0.002637 | 9.80 |
| Side/support bending | 0.002133 | 19.26 | 0.007111 | 26.42 |
| Z carriage compliance | 0.002500 | 22.57 | 0.003500 | 13.00 |
| Structural joints | 0.003000 | 27.09 | 0.008000 | 29.72 |
| Asymmetric-force racking | 0.002500 | 22.57 | 0.005000 | 18.58 |
| **Total** | **0.011074** | **100.00** | **0.026915** | **100.00** |

The largest A contributors are equivalent structural joints, Z carriage
compliance, and the deliberately conservative racking term. The largest B
contributors are equivalent structural joints and side/support bending,
followed by racking and Z carriage compliance. This identifies where coupons
and representative interfaces should improve the model.

## Dynamic and screw implications

The dynamic screen is deliberately low-acceleration because PCB process speed
is secondary to tool stability and repeatability. It includes acceleration,
guide friction, cable/probe drag, and screw efficiency:

| Quantity | A | B |
| --- | ---: | ---: |
| Moving mass | 1.24 kg | 3.95 kg |
| Inertial force at 0.20 m/s2 | 0.248 N | 0.790 N |
| Guide-friction equivalent | 0.750 N | 0.750 N |
| Cable/probe drag allowance | 0.500 N | 1.000 N |
| Y screw design force | **1.498 N** | **2.540 N** |
| T8x2 torque at 0.35 efficiency | 0.00136 Nm | 0.00231 Nm |
| T8x4 torque at 0.35 efficiency | 0.00272 Nm | 0.00462 Nm |
| Static equivalent stiffness | 451.5 N/mm | 185.8 N/mm |
| Relative sqrt(stiffness/mass) index | 19.08 | 6.86 |

These torques are only the stated low-speed screening forces. They omit
acceleration transients, screw/bearing friction variation, preload, critical
speed, motor torque-speed roll-off, and cutting forces. They do not select a
screw, motor, driver, or controller.

B has approximately 3.2 times A's moving mass. Using the calculated total
static stiffness only as a proportional modal screen, `sqrt(k/m)` is 19.08
for A and 6.86 for B, a ratio of about 2.78. This is not a natural frequency
in hertz; it indicates that B has less first-mode and servo/stepper
disturbance margin for equal participation. The cyclic PETG risks are
correspondingly higher at the two moving side interfaces. A reduces gantry
excitation but moves the board datum and its workholding/cable loop; its bed
rail seats and board support therefore remain the dynamic process risk. A
measured modal test is still required.

## Racking and centered-screw credibility

For a 5 N force offset by 100 mm:

```text
M_racking = 5 N * 100 mm = 500 Nmm
Delta guide reaction = 500 Nmm / 220 mm = 2.273 N
```

The direct 50 mm tool overhang alone produces a 250 Nmm couple. If the two
Y guide lines share that moment ideally, the corresponding reaction couple is
`250/220 = 1.136 N` per differential reaction. The 2.273 N value above is the
deliberately harsher 100 mm asymmetric-force screen, not an additional load
to add to the 5 N force.

The equivalent rotational stiffness assumptions produce an edge displacement
of 0.0025 mm for A and 0.0050 mm for B. A centered Y screw is credible for
both at the nominal 0.20 m/s2 acceleration only if the two guide lines are
parallel, preloaded, and similarly stiff. B needs the stricter side-interface
and racking test because its moving gantry joints carry the differential
guide reactions. A still needs a bed pitch/racking test; its lighter bed does
not make a loose rail seat acceptable.

## Thermal, creep, and alignment comparison

| Risk | A | B |
| --- | --- | --- |
| Stationary structural loop | Fixed gantry keeps spindle/Z/X reactions out of moving Y mass | Spindle/Z/X structure travels through side joints and Y interfaces |
| PETG cyclic preload | Main gantry joints are not cycled by Y acceleration; bed rail seats and datum still cycle | Side interfaces, rail seats, inserts, and through-bolts cycle every move |
| Thermal exposure | Spindle heat is separated from the stationary gantry only by the mount/Z path; bed map can still drift thermally | Spindle heat and moving mass are on the gantry; thermal gradients can change side alignment |
| Calibration retention | Structural reference can be stable, but the PCB map is vulnerable if the bed moves or settles after probing | PCB datum is stationary and easier to re-probe/map, but gantry preload and side-joint creep can move the tool datum |
| Alignment service | Fewer major structural joints, but long moving-bed rail seats must remain parallel | More side/rail datums and joint preload checks; fixed bed is easier to inspect and load |

Neither candidate may use height mapping to hide load-dependent machine
deflection, backlash, spindle seating error, or board movement. Temperature,
conditioning, and map validity must be recorded with physical results.

## Manufacturing and service screen

| Estimate | A | B |
| --- | ---: | ---: |
| Printed structural mass | 4.12 kg | 3.70 kg |
| Estimated print time | 32-42 h | 28-38 h |
| Structural print count | 5 | 6 |
| Largest estimated print | 320 x 100 x 220 | 300 x 80 x 160 |
| Major structural joints | 4 | 6 |
| Heat-set inserts | 16 | 24 |
| Through-bolts | 12 | 20 |
| Rail-seat datums | 4 continuous paths | 6 separated paths |

A's integrated U minimizes joints and should improve force-loop continuity,
but the large one-piece concept has more warp, bed-contact, and inspection
risk. The multi-piece A fallback increases joint evidence requirements. B's
individual prints are easier to fit within the printer and replace, but its
additional inserts, bolts, and rail datums increase assembly and creep
inspection. Both require post-print rail-seat measurement and either skim,
shim, or a replaceable metal load-spreading datum; neither treats as-printed
PETG as a precision rail surface.

For usability, B is better for fixed-board loading, conductive probing,
height-map reuse under an unchanged clamp state, chip clearing, and spindle
service. A is better for a stationary spindle/gantry force path and lower Y
mass, but the board, spoilboard, registration, probe/cable allowance, and
workholding move together. A therefore needs a movement-state check between
probing and cutting and a positive registration strategy.

## Revised Phase 2A matrix

Scores are still ordinal judgments from 1 (poor) to 5 (favorable). The
normalized result is `100 * sum(weight * score / 5) / sum(weight)`. Structural
stiffness is represented by the total analytical result and a separate
torsion/racking view; there is no duplicate generic-bending score.

| Criterion | Weight | A score | B score | Basis |
| --- | ---: | ---: | ---: | --- |
| Static tool-point stiffness | 18 | 5 | 4 | total 5 N estimate and target/acceptance distinction |
| Torsional stiffness | 10 | 5 | 4 | isolated closed-section torsion contribution |
| Racking susceptibility | 8 | 4 | 3 | rotational stiffness and guide-couple screen |
| Calibration retention | 18 | 3 | 5 | moving datum risk versus fixed PCB datum |
| Moving mass | 10 | 5 | 2 | 1.24 versus 3.95 kg nominal moving mass |
| Structural joint count | 8 | 4 | 3 | 4 versus 6 major joints |
| PETG creep sensitivity | 8 | 4 | 2 | cyclic side-interface/preload exposure |
| Manufacturing complexity | 8 | 3 | 4 | large A U versus smaller B parts, with more B interfaces |
| Probing/workholding | 6 | 2 | 5 | fixed bed and map validity |
| Serviceability | 4 | 2 | 5 | access, loading, cleaning, and datum inspection |
| Footprint | 2 | 3 | 4 | same machine envelope, B lighter packaging burden |
| **Normalized result** | **100** | **78.0** | **75.2** | **A by 2.8 points** |

### Sensitivity

Each scenario doubles the listed group weights and renormalizes the total. It
is a deliberate weight perturbation, not a confidence interval.

| Weight emphasis | A | B | Winner |
| --- | ---: | ---: | --- |
| Base | 78.000 | 75.200 | A |
| Structural-evidence-heavy | 83.457 | 70.617 | A |
| Calibration-and-usability-heavy | 72.500 | 80.625 | B |
| Manufacturing-heavy | 78.806 | 69.851 | A |
| Moving-mass-heavy | 80.000 | 72.000 | A |

The result is therefore close in the real decision sense even though the
revised base score favors A: B wins when fixed-datum calibration and process
access are emphasized. The owner decision should be driven by representative
stiffness, creep, and map-retention evidence rather than by a small matrix
margin.

## Physical validation coupons and model feedback

The following coupons are required before an architecture freeze. Each result
must record filament, print orientation, perimeter/wall process, layer height,
conditioning, fastener torque, temperature, load direction, measurement
instrument, and uncertainty.

1. **Representative beam bending.** Print A and B beam sections with the
   proposed span and interfaces. Apply known 5 N and 10 N loads at the tool
   point, measure displacement with a dial indicator or LVDT, record loading
   and unloading, and fit effective `EI` and interface compliance.
2. **Torsion-box twist.** Clamp the representative support pair, apply a
   known torque or separated force couple, measure angle across the section,
   and fit effective `GJ`. Repeat before and after conditioning.
3. **Rail-seat deformation.** Print a representative rail-seat coupon with
   the actual insert/through-bolt/load-spreader arrangement. Torque in the
   intended sequence, apply a 5 N lateral and moment load, and measure rail
   datum movement and permanent set.
4. **Heat-set insert creep.** Use the actual insert, PETG process, washer,
   screw, preload, and temperature. Record torque, bolt projection, insert
   pull/rotation indicators, and rail datum at 0, 1, 7, and 30 days.
5. **Through-bolt creep.** Build a representative clamped joint with the
   intended washer/load spreader. Measure clamp length, slip, and rail datum
   after preload, thermal cycling, and representative repeated Y motion.

Feed the measurements back by replacing the effective modulus, section
properties, `k_joint`, `k_theta`, friction/drag, and mass values in
`cad/parameters.py`, rerun `tools.run_phase2a_study`, update the calculation
record and matrix, and preserve the previous result as an audit trail. A
target miss or creep drift reopens the architecture rather than being
absorbed by a height map.

## Reproducibility and gate status

Dependency-light analytical tests run with:

```text
python -B -m unittest discover -s tests -v
```

The optimized review skeleton and calculations run in the pinned external
build123d environment:

```text
<temp>\pcbCNC-phase2-build123d-venv\Scripts\python.exe -m tools.run_phase2a_study --output-dir <temp>\pcbCNC-phase2a-study-output
```

The command must pass Phase 2 and Phase 2A input validation, create non-empty
review exports for A and B, and report zero unexpected solid overlaps. It does
not create production geometry or publish temporary artifacts.

The architecture baseline is frozen only at the system level. Confidence is
**low-to-moderate** for the comparative direction and **low** for the absolute
millimetre values. The assumptions most likely to change the result are PETG
print orientation and conditioning, actual rail-seat and joint stiffness,
insert/through-bolt creep, spindle mass and tool overhang, real Y friction and
cable drag, and the actual load direction. The next decision gate is physical
coupon and representative 5 N A/B evidence under the same workholding and
thermal state.
