# Engineering decision record: Phase 2 architecture

- **Record ID:** EDR-006
- **Phase:** 2 - Architecture
- **Status:** accepted by owner with Phase 2A amendment; historical proposal retained

The original decision proposal below is retained as historical evidence. The
owner disposition at the end of this record is the current Phase 2 decision.
- **Date:** 2026-10-06
- **Owner:** project team
- **Affected requirements:** REQ-ARCH-001 through REQ-ARCH-005, REQ-FN-003,
  REQ-FN-004, REQ-ENV-001 through REQ-ENV-005, REQ-MOT-001, REQ-MOT-004,
  REQ-MOT-005, REQ-Z-001 through REQ-Z-004, REQ-PETG-001 through
  REQ-PETG-006

## Decision proposed for owner review

Use **B: moving gantry with fixed bed** as the preliminary PCB CNC
architecture. Keep **A: fixed gantry with moving Y bed** as the explicit
runner-up and fallback. Do not carry C, a fixed-gantry/fixed-bed moving-XY
head, into detailed design unless new evidence shows a specific PCB benefit.

The B interface proposal is:

- fixed, replaceable-spoilboard bed around 240 x 190 mm with a nominal
  200 x 150 mm PCB working area;
- preliminary tool-point travel of 220 x 170 x 40 mm, subject to packaging;
- two separated Y guide centerlines around 220 mm apart and one centered Y
  screw line;
- two X guide centerlines across a deep gantry beam and one centered X screw
  line;
- two Z guide centerlines around 60 mm apart and one centered Z screw line;
- dual-guide Z interface preferred. Dual MGN12 is the stronger candidate and
  dual MGN9 remains a lower-mass candidate; a single MGN12 carriage is not the
  primary moment-reaction layout;
- T8x2 and T8x4 remain lead candidates. No rail class, screw lead, spindle,
  motor, controller, or probing hardware is frozen;
- deep closed/deep-ribbed PETG monocoque gantry with distributed interfaces,
  not copied aluminium-extrusion geometry.

## Alternatives considered

### A — fixed gantry / moving bed

Strengths are a stationary gantry and potentially short Z/X force loop. Risks
are moving PCB datum, moving spoilboard mass, bed support pitch, cable/probe
motion, and long rail-seat alignment. It scores 73.6/100 and remains the
fallback if B's gantry test fails.

### B — moving gantry / fixed bed

Strengths are fixed workholding, stationary conductive probing and height-map
datum, better loading/service access, and a short direct loop when the gantry
is a deep closed section. The key risk is PETG torsion and creep in the two
moving side interfaces. It scores 77.0/100 and wins all tested weight
sensitivities, with a narrow margin in the stiffness-led scenario.

### C — fixed gantry / fixed bed / moving XY head

The fixed bed is a credible PCB-specific benefit, but the elevated XY head
adds guide interfaces, carriage overhang, alignment steps, and cable/probe
constraints. It scores 53.2/100 and is not advanced.

## Evidence and reasoning

The common 5 N load and 50 mm tool overhang produce a 250 Nmm moment. A
60 mm dual-guide spacing gives an idealized 4.17 N reaction couple. The
architecture calculation uses only relative loop length, section-depth, and
joint-risk screens; it does not present fake FEA precision.

The weighted matrix gives 45% of the weight to tool-point stiffness, Z
stiffness, gantry torsion, and force-loop length. The fixed bed and stationary
probe/workholding account for B's margin over A. PETG structural geometry is
specified as a deep closed/ribbed monocoque with large section depth, fillets,
gussets, distributed rail loads, and metal load spreaders where preload or
datum stability requires them.

The architecture-only build123d spike passed with version 0.12.0. It built all
three deterministic skeletons, exported non-empty STEP and review STL
derivatives outside the repository, reported 340 x 290 x 220 mm skeleton
bounding boxes, and found zero unexpected solid overlaps after documenting
intentional interfaces. No manufacturing STL or release export was created.

## Risks and mitigations

| Risk | Consequence | Mitigation / gate evidence | Owner |
| --- | --- | --- | --- |
| B gantry torsion exceeds the 0.020 mm target. | PCB isolation depth and drilling datum shift with load direction. | Representative printed beam/side-joint 5 N X/Y/Z test; reopen A if it fails. | project team |
| PETG creep relaxes rail or screw preload. | Alignment and map datum drift over time. | Preload/creep coupon and post-conditioning rail-seat inspection. | project team |
| Fixed bed is too shallow or inaccessible for clamps/probe. | Board cannot be registered or mapped safely. | Workholding/probe mock-up and swept-volume review before motion selection. | project team |
| MGN9/MGN12 or T8x2/T8x4 choice is made from availability. | Hidden torque, stiffness, speed, or service failure. | Phase 3 component trade using actual motor/controller/spindle data. | project team |
| Spindle envelope is wrong. | Mount, tool overhang, cable, and thermal assumptions break. | Select and measure a spindle before detailed mount geometry. | project team |

## Unresolved questions carried forward

- exact spindle, tool retention, mass, diameter, runout, cable exit, and
  thermal behavior;
- actual owned motor models and torque-speed data;
- controller/GRBL variant, driver current, probe input, limits, and spindle
  control;
- exact conductive probe and height-map acquisition/storage/toolpath policy;
- rail preload/class and screw lead/anti-backlash/bearing arrangement;
- workholding clamp/tape/adhesive method and board thickness range;
- PETG filament, print orientation, wall/perimeter process, conditioning, and
  rail-seat post-processing;
- physical B-vs-A stiffness, creep, and datum test results.

## Validation and review

- [x] Phase 1 owner acceptance recorded in EDR-005.
- [x] A, B, and credible C compared with the same baseline.
- [x] Complete force-loop paths, interfaces, and dominant compliance risks documented.
- [x] Gantry section, Z guide, Y bed, screw-line, workholding, and probing trades documented.
- [x] Weighted matrix and sensitivity check implemented and tested.
- [x] Architecture-only build123d skeleton, exports, bounds, and interference policy tested.
- [x] No production STL/STEP/detailed printable part generated or published.
- [x] Owner reviewed the original proposal together with EDR-007 and recorded the A baseline disposition below.

## Phase gate (historical pre-disposition state)

The preceding proposal required owner review. That review and the Phase 2A
disposition are now recorded below; the accepted baseline still does not
authorize detailed structural CAD or manufacturing exports.

## Phase 2A addendum (2026-10-06; historical pre-disposition text)

The close original A/B result triggered a focused structural follow-up. The
original B recommendation is therefore reopened for comparison with an
independently optimized A fixed-gantry/moving-bed concept. The follow-up is
recorded in [EDR-007](007-phase-2a-structural-comparison.md) and
[the Phase 2A package](../architecture/phase-2a-structural-comparison.md).
At the time this addendum was written, EDR-006 remained proposed and Phase 3
was not authorized. The owner disposition below supersedes that temporary
pre-review boundary.

## Owner disposition (2026-10-06)

The owner reviewed the original Phase 2 proposal together with EDR-007 and
accepted **A: fixed gantry with moving Y bed** as the mechanical architecture
baseline. **B: moving gantry with fixed bed** remains the documented primary
rejected alternative and is not to be physically built unless the owner
reopens the architecture.

The architecture is frozen only at the system-mechanical level. Detailed
geometry, guide class, screw lead, bearing arrangement, spindle, dimensions,
interfaces, motor/controller identity, and production parts remain open for
Phase 3 and later evidence. The Phase 2A values remain calculated screening
results, not measured machine results. PETG coupons, joint/rail-seat tests,
and representative 5 N force-loop evidence remain required.

This disposition authorizes Phase 3 motion-system selection and its
review-only parameter/skeleton work. It does not accept the Phase 3 decision
record, authorize detailed structural CAD, or authorize production STEP/STL.
