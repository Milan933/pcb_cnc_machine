# Engineering decision record: hardware procurement / measurement freeze

- **Record ID:** EDR-013
- **Phase:** hardware procurement and measurement freeze after preliminary Phase 4/4A architecture
- **Status:** proposed / owner review required
- **Date:** 2026-10-06
- **Owner:** project owner / project team
- **Inputs:** owner acceptance of EDR-011 and EDR-012, EDR-008, EDR-009,
  EDR-010, and the Phase 4A O2 review metrics
- **Affected requirements:** REQ-HW-001 through REQ-HW-008,
  REQ-MOT3-004 through REQ-MOT3-010, REQ-FAST-001 through REQ-FAST-008,
  REQ-P4-001 through REQ-P4-015, REQ-VAL-001 through REQ-VAL-003

## Decision proposed for owner review

Enter a hardware procurement / measurement freeze before manufacturing-ready
structural CAD. The owner-accepted O2 architecture is the reference for
sample quantities and measurement locations, but no vendor-independent
assumption becomes a final CAD interface until the physical sample or owned
hardware is identified and measured.

The controlling implementation is:

- [hardware procurement / measurement requirements](../../requirements/hardware-procurement-measurement-freeze.md);
- [owned hardware identification sheets](../../requirements/hardware-identification-sheets.md);
- [short procurement BOM matrix](../../bom/hardware-procurement-measurement-matrix.md).

## Procurement disposition

| Category | Disposition |
| --- | --- |
| A - safe to buy now / architecture defining | Process-matched PETG, basic inspection tools, a readable dial indicator/rigid base if absent, and a simple known 5 N loading set. A 230 x 180 x 12 mm MDF board is a low-regret process sample only. |
| B - buy sample / measure before final CAD | Complete X/Y/Z rail and carriage characterization set; T8x4/T8x2 screw and nut candidates; fixed/floating 8 mm bearing candidates; 5 mm-to-measured-journal couplers; M3/M4/M5 inserts; standard fastener samples; limit/probe samples; spoilboard material samples. |
| C - wait until later design phase | Final spindle/collets/tools, final workholding or vacuum, production spoilboard batch, production O2 parts, final insert pockets, final fastener lengths, guards, and enclosure. Replacement motor/controller hardware is conditional only if later validation demonstrates an actual limitation; no replacement is recommended now. |
| D - already owned / identify and measure | Owner-supplied NEMA17 stock and the intended Arduino Mega + CNC Shield platform, including installed driver carriers and wiring. **Do not buy motors. Do not replace the controller unless later validation identifies an actual limitation.** |

## Motion procurement baseline

| Axis | Rail and carriage quantity | Rail reference | Screw quantity and class | Screw reference |
| --- | --- | ---: | --- | ---: |
| X | 2 MGN12 rails + 4 MGN12H carriages | 340 mm | 1 T8x4 | 360 mm |
| Y | 2 MGN12 rails + 4 MGN12H carriages | 310 mm | 1 T8x4 | 330 mm |
| Z | 2 MGN9 rails + 4 MGN9H carriages | 130 mm | 1 T8x2 | 145 mm |

Exact rail length is preferred when the selected vendor provides a valid
drawing and physical sample. If not, buy the nearest standard rail longer than
the reference and retain it uncut until the measured stop, carriage, and seat
stack is reviewed. Rail cutting is not the default. If a screw must be cut,
face/square, finish journals, chamfer/deburr, clean the thread, and remeasure
runout, journals, shoulders, and usable thread.

T8x4 and T8x2 identify lead. Supplier and physical records must separately
state pitch and number of starts. The sample record must also include major
diameter, straightness, machined ends, and nut behavior.

## Preliminary motion interface choices

- X/Y use adjustable split-brass or dual-brass anti-backlash candidates;
  Z uses an adjustable/spring-preloaded candidate subject to drag and
  power-off gravity-hold testing. The reversal target is <=0.030 mm.
- Each screw has one fixed end with a matched pair of 8 mm-bore
  708/8, 718/8, or 719/8 angular-contact candidates, or a documented BK08-class
  equivalent, in a DB/O arrangement with light controlled preload, an axial
  shoulder/retainer, and a replaceable cartridge. The opposite end uses one
  floating 8 mm radial support with axial freedom. The motor bearing and
  coupler are not axial supports.
- The first coupler sample is compact helical 5 mm to the measured screw
  journal; Oldham is the comparison/fallback; jaw/spider is not the default.

These are preliminary choices for sample purchasing, not manufacturing locks.

## Owned hardware gate

The owner’s motors are the only motor source for the current design stage;
motor purchases are not authorized. Preliminary structural CAD uses a generic
NEMA17 interface: approximately 42.3 mm mounting square, screening 5 mm shaft,
40-48 mm body class, and rear connector/wiring access for multiple common
3D-printer motor lengths. Final axis assignment is made only after
manufacturer/model where available, body, current, torque evidence, phase
resistance, shaft, connector, step angle, mounting pattern, condition, and
torque-at-speed behavior are recorded. The screen is >=0.45 N-m holding torque
for X/Y and >=0.55 N-m for Z; holding torque alone is insufficient.

Normal suitable stock is preferred for X/Y. The strongest suitable owner motor
is preferred for Z only when electrically compatible with the identified
driver and supply. The unselected final motor does not block preliminary
structural CAD, but it blocks manufacturing-ready interfaces and commissioning.

The owner-supplied controller platform is **Arduino Mega + CNC Shield** and is
intended for this machine. It must not be replaced by assumption. Identify the
exact CNC Shield model/revision, installed stepper-driver modules, supported
microstep configuration, motor-current capability, supply-voltage capability,
cooling, spindle PWM/control outputs, probe input, limit inputs,
GRBL-compatible firmware/configuration strategy, pinout, and fault/homing
behavior. A4988 and DRV8825 are only possible module markings until physically
identified.

## Fastening, spindle, and process gates

M3/M4/M5 insert samples are required, but no generic pocket dimension is
accepted. Each selected family needs OD, length, flange/taper, thread depth,
pilot range, insertion depth, tool access, pull-out, torque, deformation,
repeated-assembly, and preload-creep evidence. M3 is the accessory/rail class,
M4 is the general structural/module class, and M5 is conditional.

The final spindle remains open. A candidate must support isolation routing,
drilling, and outline cutting and be measured against 10,000-30,000 rpm,
<=0.010 mm TIR target / <=0.020 mm provisional maximum, 50-150 W, 0.30-0.80
kg, ER11-class tooling, electrical/controller compatibility, noise, bearing
quality, thermal behavior, cable exit, and clamp envelope. The 52 mm body is a
screen, not a reason to buy an inferior spindle.

## Required evidence before production CAD

1. Physical rail/block, screw/nut, bearing, coupler, insert, fastener, and
   owned hardware measurements are recorded with instruments and sample IDs.
2. Rail-seat, MGN9, PETG process, J1/structural joint, bearing-pocket, and
   spoilboard/workholding coupons are inspected and passed or explicitly
   dispositioned.
3. Full X/Y/Z travel and service mock-up includes the measured motors,
   spindle envelope, switches, probe, cables, screws, bearings, couplers,
   workholding, and spoilboard.
4. A simple physical 5 N tool-point test is completed and labeled as measured;
   the 0.009410 mm analytical estimate is not substituted for it.
5. Spindle TIR/mass/centerline/thermal data and controller compatibility are
   recorded before the spindle mount is frozen.

## Risks and mitigations

| Risk | Consequence | Mitigation |
| --- | --- | --- |
| Clone rail dimensions differ from the HIWIN class name. | Rail seats, carriage height, and travel are invalid. | Sample-first measurement; drawing plus actual min/max record; retain longer rails. |
| Screw end machining or nut preload differs from the envelope. | Bearing cartridges, couplers, and backlash fail. | Buy sample blanks, measure/finish ends, and test nuts before CAD. |
| Bearing/coupler arrangement carries axial load incorrectly. | Motor damage, Z creep, or lost position. | Fixed/floating axial test and explicit torque-only coupler rule. |
| PETG inserts or long rail seats creep. | Datum drift, pull-out, or binding. | Size-specific coupons, conditioning, preload retention, shim/skim strategy. |
| Owned motor/controller cannot meet current, torque, or I/O needs. | Missed steps or unsafe electrical interface. | Identify and bench-test first; consider replacement only if the actual limitation is demonstrated. |
| Spindle exceeds the 52 mm screen or has poor TIR. | Inferior process performance or mount redesign. | Keep mount replaceable and select by PCB process data, not envelope alone. |

## Gate disposition

EDR-013 remains **proposed / owner review required**. It authorizes the
characterization purchase and measurement plan described above, not production
quantities, manufacturing-ready interfaces, final production CAD, or Phase 5.
