# Phase 1 motion and structural requirements

These targets are screening requirements for architecture and motion-system
trade studies. They are not component selections and have not been verified
on the machine.

## Travel and working-area relationship

The project distinguishes usable PCB area from tool-point travel. The machine
must provide at least the selected usable PCB area plus the access needed for
registration, clamps, probing, and safe tool paths. The final relationship is
an architecture decision.

The three working-area options are:

- A: 160 x 100 mm;
- B: 200 x 150 mm;
- C: 250 x 180 mm.

The Phase 1 recommendation is option B as the process envelope, while
retaining approximately 200 x 150 mm as the minimum tool-point travel
planning target until the architecture allocates edge and datum margins.

## XY motion targets

| Property | Target | Provisional acceptance | Meaning |
| --- | ---: | ---: | --- |
| Commanded linear increment | <=0.010 mm | N/A | Controller command granularity only; not accuracy. |
| Calibrated absolute XY error | <=0.050 mm over 200 mm | <=0.100 mm over 200 mm | Scale and geometric error after calibration. |
| Bidirectional repeatability | <=0.030 mm | <=0.050 mm | Return spread from repeated approaches. |
| Backlash | <=0.030 mm | <=0.050 mm | Reversal offset measured separately from repeatability. |
| Axis straightness | <=0.050 mm over the long axis | <=0.100 mm | Tool-point path deviation under a defined measurement setup. |
| Squareness | <=0.050 mm over 100 mm | <=0.100 mm over 100 mm | Orthogonality error measured with a calibrated artifact. |

These values are deliberately separate from the 0.15-0.25 mm initial
trace/space capability target. A calibrated coordinate error can sometimes be
corrected; backlash, deflection, and runout cannot be removed by software
calibration.

## Controller and motor implications

For a 200-step/rev motor and 16 commanded microsteps:

- T8x2 nominal increment = 2 / (200 x 16) = 0.000625 mm;
- T8x4 nominal increment = 4 / (200 x 16) = 0.00125 mm.

These are command increments only. Motor torque at speed, driver current,
mechanical compliance, screw pitch error, backlash, and microstep nonlinearity
determine practical motion. The exact NEMA17 motor identity and installed
controller modules are unresolved, but the owner-supplied platform is known:
Arduino Mega + CNC Shield. Preliminary structural CAD uses the generic NEMA17
interface; these values do not select a final motor or authorize controller
replacement.

The controller shall support independently configured rapid, cutting,
probing, and homing rates, and shall expose usable limit and probe inputs.
The final step rate and driver voltage/current budget belongs to Phase 3.

## Tool-point deflection and stiffness

The proposed screening target is:

- tool-point deflection <=0.020 mm under a 5 N static load applied at the
  process tool point in the measured load direction;
- provisional acceptance maximum <=0.030 mm under the same defined test;
- corresponding minimum screening stiffness is 5 N / 0.020 mm = 250 N/mm.

The 5 N load is a conservative test load assumption, not a measured PCB
cutting force. The physical machine shall also be tested with a representative
tool and process, because static stiffness does not capture vibration,
cutting-force direction, spindle imbalance, or PETG creep.

The design shall report Z-axis, X/Y-axis, and gantry torsion separately. A
single bulk frame displacement number is insufficient.

## Z-axis geometry targets

Until a spindle envelope is selected, use these as packaging limits:

- spindle nose / tool-point support overhang from the nearest effective Z
  guide reaction plane: preferred 25-50 mm, conditional maximum 60 mm;
- total cutting tool stickout: preferred 5-15 mm for isolation, with a
  longer allowance for drilling and outline tooling only when required;
- Z carriage overhang beyond the guide reaction plane: preferred <=50 mm,
  conditional maximum 75 mm.

These values are architecture screening constraints. They must be recalculated
when spindle diameter, mass, collet, tool stickout, guide spacing, and
workholding clearance are known.

## Guide, screw, and homing requirements

The architecture shall compare MGN9, MGN12, and alternatives by carriage
moment capacity, guide spacing, mounting-surface stiffness, contamination,
preload, and serviceability. T8x2 and T8x4 shall be compared by speed,
resolution, torque, critical speed, backlash, and anti-backlash behavior.
None is selected by this document.

Each axis shall provide:

- usable travel after subtracting carriage, support, hard-stop, and homing
  margins;
- a screw/guide arrangement with defined axial support and no motor-bearing
  abuse;
- accessible limit/homing switches with a repeatability target of <=0.020 mm
  and provisional acceptance <=0.050 mm;
- a safe homing sequence, soft limits after homing, and a switch-fault
  response;
- cable routing that does not add an unmeasured process load.

## Requirement IDs

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-MOT-001 | The selected machine shall preserve the Phase 1 working-area/travel distinction and meet the approved tool-point travel budget. | Preliminary |
| REQ-MOT-002 | Commanded XY/Z increments shall be <=0.010 mm where the chosen screw, motor, driver, and controller can support that command rate. | Preliminary |
| REQ-MOT-003 | Calibrated absolute error, repeatability, backlash, straightness, and squareness shall be measured and reported separately. | Known process rule |
| REQ-MOT-004 | Tool-point deflection shall meet the 0.020 mm target under a defined 5 N static test load; 0.030 mm is the provisional acceptance limit. | Preliminary |
| REQ-MOT-005 | The Z guide reaction plane and tool-point overhang shall be recorded and remain within the screening limits above unless an EDR justifies a change. | Preliminary |
| REQ-MOT-006 | Homing and limit switches shall be stiff, accessible, independently validated, and compatible with the controller fault behavior. | Preliminary |
