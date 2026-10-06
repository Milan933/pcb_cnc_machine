# Phase 1 acceptance-test plan

These are proposed measurable tests for the future physical machine. Values
marked provisional are not yet experimentally verified. A test result shall
include instrument, setup, temperature, tool, datum, number of trials, raw
data, and uncertainty.

## Motion and structure

| Test ID | Test | Target | Provisional acceptance |
| --- | --- | ---: | ---: |
| AT-MOT-001 | Calibrated absolute XY error over 200 mm | <=0.050 mm | <=0.100 mm |
| AT-MOT-002 | Bidirectional XY repeatability at home, center, and near travel limits | <=0.030 mm | <=0.050 mm |
| AT-MOT-003 | Reversal backlash at three positions per axis | <=0.030 mm | <=0.050 mm |
| AT-MOT-004 | Axis straightness over the long travel | <=0.050 mm | <=0.100 mm |
| AT-MOT-005 | Squareness error over a 100 mm test length | <=0.050 mm | <=0.100 mm |
| AT-STR-001 | Tool-point static displacement under a 5 N defined load | <=0.020 mm | <=0.030 mm |
| AT-STR-002 | Z machine contribution excluding board variation | <=0.040 mm allocation | <=0.050 mm |
| AT-MOT-006 | Homing repeatability under repeated cold and warm cycles | <=0.020 mm | <=0.050 mm |

## Spindle, probing, and Z

| Test ID | Test | Target | Provisional acceptance |
| --- | --- | ---: | ---: |
| AT-SPN-001 | Radial tool-shank TIR at the selected collet/tool | <=0.010 mm | <=0.020 mm |
| AT-SPN-002 | Tool re-installation axial seating variation | <=0.005 mm allocation | <=0.010 mm |
| AT-PRO-001 | Conductive probe repeatability | <=0.010 mm | <=0.020 mm |
| AT-PRO-002 | Height-map residual at independent points | <=0.020 mm | <=0.030 mm |
| AT-PRO-003 | Open-circuit probe response | Stop before cutting | No unsafe plunge |

Map tests shall compare the 25 mm baseline grid with 12.5 mm refinement on
the same board and clamping state. The map must not be reused after the board,
fixture, tool, or datum changes without an explicit validity rule.

## PCB process coupons

### Isolation coupon

Use measured 1 oz and, if available, 2 oz copper coupons. Include:

- 0.25 mm trace/space as the robust baseline;
- 0.20 mm trace/space as an intermediate target;
- 0.15 mm trace/space as a stretch target;
- isolated pads, long traces, corners, and a copper-clearance ladder;
- V-bit angle, tip class, depth, feed, RPM, and map grid in the record.

Pass criteria include electrical isolation, no unintended opens, trace-width
measurement, visible burrs, and repeatability across at least three locations.
The project shall not claim sub-0.15 mm capability from a single coupon.

### Drilling coupon

Use representative 0.30-1.00 mm drills where available. Record center
registration, hole diameter, breakout, burrs, board support, retract/peck
settings, spindle speed, and tool wear separately.

### Outline coupon

Cut a measured outline with at least one internal corner and one long edge.
Record dimensional error, corner radius, burrs, board movement, final-pass
retention, and spoilboard penetration. The initial dimensional target is
<=0.10 mm over a 100 mm feature with a provisional acceptance of <=0.15 mm.

## Evidence rule

These tests are not passed by code existence. A physical result is required.
Before physical validation, the requirements remain preliminary and the
project remains experimental.
