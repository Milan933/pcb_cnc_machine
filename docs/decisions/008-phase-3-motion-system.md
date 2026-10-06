# Engineering decision record: Phase 3 motion system

- **Record ID:** EDR-008
- **Phase:** 3 - Motion-system selection
- **Status:** proposed / owner review required
- **Date:** 2026-10-06
- **Owner:** project owner / project team
- **Architecture input:** EDR-006 and EDR-007 owner disposition — Architecture A accepted as the mechanical baseline
- **Affected requirements:** REQ-MOT-001 through REQ-MOT-006, REQ-MOT3-001 through REQ-MOT3-015, REQ-VAL-001 through REQ-VAL-003, REQ-HW-001 through REQ-HW-005

## Decision proposed for owner review

Use the following component classes for the Phase 3 review layout of the
fixed-gantry/moving-Y-bed machine:

- X: dual MGN12H-class rails, two long blocks per rail, approximately 60 mm
  vertical separation, centered T8x4 screw;
- Y: dual MGN12H-class rails, two long blocks per rail, approximately 220 mm
  separation, centered T8x4 screw and moving 240 x 190 mm bed support;
- Z: dual MGN9H-class rails, two long blocks per rail, approximately 60 mm
  separation, centered T8x2 screw and approximately 40 mm usable travel;
- fixed/floating screw supports on every axis, with paired axial support at
  one end, radial-only float at the other, and an 8 mm generic T8 end envelope;
- adjustable preloaded anti-backlash nuts as the X/Y default and a tested
  preloaded Z nut; flexible 5-to-8 mm couplers transmit torque only;
- typical 40-48 mm NEMA17 packaging envelope, subject to measured motor
  torque/current/shaft data;
- GRBL 1.1-compatible STEP/DIR controller, starting at 8 microsteps, with the
  exact CNC Shield and driver carrier still unresolved;
- X/Y/Z homing at left/negative, front/negative, and up/positive, with G54
  established from the registered PCB datum and probe.

These are preliminary component-class choices. They do not freeze an exact
supplier, preload, rail length, screw end machining, bearing fit, nut geometry,
motor, driver, spindle, shield, printed rail seat, or production part.

## Alternatives considered

### MGN9 versus MGN12

MGN9 is lower mass and lower packaging burden. MGN12 provides a wider seat,
higher long-block moment capacity, more PETG mounting margin, and a better
long-span X/Y stiffness risk posture. The selected arrangement is MGN12H for
X/Y and MGN9H for short Z. MGN12H remains the controlled Z fallback if the
short-Z coupon or tool-point test misses the stiffness target. A single rail
or a single carriage line is rejected as the baseline because it weakens the
separated moment reaction path.

### T8x2 versus T8x4

T8x4 is selected for X/Y to keep screw rpm within a conservative whip screen
while preserving sufficient command resolution. T8x2 is selected for Z for
greater mechanical advantage, gravity-hold margin, and short-axis packaging.
Both are low-cost, widely available classes, but supplier straightness, root
diameter, nut fit, and backlash vary and require sample measurement.

### Bearing arrangements

A fixed/floating arrangement is selected over two axially constrained ends.
Paired angular-contact or compact BK08-class supports react screw thrust; an
8 mm radial BF08-class support permits axial growth. A coupler cannot replace
the fixed bearing. Exact block vendor and fit remain open.

### Nut arrangements

Standard brass nuts are retained only as inexpensive comparison samples.
Spring-preloaded split brass or dual-brass nuts are the X/Y default because
the project has a <=0.030 mm provisional backlash target and needs serviceable
adjustment. Polymer anti-backlash nuts remain a wear/creep alternative. Z
preload is conditional on drag and power-off tests.

### Motor/controller

The owner already has NEMA17 motors and Arduino CNC Shield/GRBL-compatible
hardware, but no exact models are yet identified. The design uses an acceptance
envelope rather than forcing those items into the mechanism. A4988 and DRV8825
are driver candidates; 8 microsteps is the starting setting, not a claim that
either installed carrier is suitable.

## Evidence and reasoning

The Phase 3 equations are implemented in `cad/motion_phase3.py` and reproduced
in [phase-3-motion-calculations.md](../calculations/phase-3-motion-calculations.md).
The nominal build123d layout is in `cad/assembly/motion_skeleton.py` and
contains only reference envelopes. The calculated screens are:

- MGN12H reference ratings provide more load/moment and mounting width for the
  long X/Y rails; MGN9H is adequate as a class screen for the short, separated
  Z plane but remains conditional on PETG evidence;
- 60 mm guide separation gives a 4.17 N ideal reaction for the 250 N-mm tool
  moment; 220 mm Y separation gives 1.14 N;
- X/Y T8x4 and Z T8x2 give full-step command increments of 0.020 and 0.010
  mm, respectively, and 8-microstep increments of 0.0025 and 0.00125 mm;
- the 70% pinned-screw critical-speed screen gives approximately 725 mm/min
  for X, 833 mm/min for Y, and 2267 mm/min for Z, before practical caps of
  600, 700, and 1200 mm/min;
- the 1.24 kg moving-bed estimate is inherited from Phase 2A and remains
  unweighed.

The quantity and sample boundary is recorded in the
[Phase 3 review BOM](../../bom/phase-3-motion-bom.md); it is not a Phase 4
production purchase list.

These are calculated screening values, not measured accuracy, stiffness,
backlash, feed, torque, or resonance claims.

## Risks and mitigations

| Risk | Consequence | Mitigation / gate evidence |
| --- | --- | --- |
| Actual owned motor has lower torque or incompatible shaft/current. | Missed steps, bad coupler fit, or overheating. | Identify and measure motors; obtain torque-speed/current data before purchase. |
| CNC Shield or GRBL fork lacks the assumed probe/PWM/limit behavior. | Unsafe homing, no height map, or no spindle control. | Record board revision/pin map; bench-test every I/O and alarm path. |
| Clone rail preload/play or PETG seat compliance exceeds the screen. | Tool-point deflection, chatter, or datum drift. | Measure samples; print rail-seat and joint coupons; repeat 5 N force-loop tests. |
| T8 screw straightness/end fit lowers usable speed. | Whip, vibration, and lost steps. | Measure runout/straightness, use fixed/floating supports, commission below 70% screen. |
| Anti-backlash preload relaxes or creates excess drag. | Backlash, heat, and missed steps. | Measure reversal, preload, drag, and wear after a cycling test. |
| Moving bed is heavier than 1.24 kg or cable drag is high. | Acceleration margin and squareness loss. | Weigh the assembly, measure cable drag, and tune acceleration conservatively. |
| Spindle diameter/mass/overhang differs from envelope. | Z moment and mount interfaces become invalid. | Measure the actual spindle before detailed Z mount design. |

## Purchase and CAD boundary

One sample of each candidate class may be purchased for measurement and
coupons. Production rail/screw quantities and detailed PETG mounts are not
approved by this record. The reference skeleton is review geometry only and
must not be exported to `generated/*/release/` or used as a manufacturing STL.

## Unresolved questions

- Which exact owned NEMA17 motors, drivers, supply voltage, and current limits
  are available?
- Which exact CNC Shield revision and GRBL fork are installed?
- Which spindle will define diameter, mass, runout, cable exit, cooling, and
  ER11/tool retention?
- Which rail/screw supplier, preload, straightness, and end machining pass
  measurement?
- Which anti-backlash nut survives the target cycle count without excessive
  drag or creep?
- What switch type, probe plate, cable routing, and noise protection will be
  used?
- Does the moving-bed structure retain the workholding datum under loading and
  after thermal/creep conditioning?

## Validation and review

- [x] Owner Architecture A decision recorded; B remains the rejected documented alternative.
- [x] X/Y/Z guide, spacing, screw, bearing, nut, motor, controller, and homing classes documented.
- [x] Central Phase 3 parameters and dependency-light calculations added.
- [x] Review-only build123d motion skeleton added; no production structural geometry created.
- [x] Backlash, preload, axial-play, homing, missed-step, and repeatability tests added to the plan.
- [x] Sample-characterization BOM and safe-purchase boundary added.
- [x] Candidate and tracked repository audit paths remain part of the commit gate.
- [ ] Exact owned hardware identified and measured.
- [ ] Representative motion hardware and PETG interface coupons tested.
- [ ] Phase 3 owner review completed.

## Gate

This record remains **proposed**. The repository may proceed to owner review of
the motion-class baseline and the separate Phase 2A physical validation plan.
It must not begin Phase 4 BOM finalization, detailed structural CAD, or
manufacturing export from this record alone.
