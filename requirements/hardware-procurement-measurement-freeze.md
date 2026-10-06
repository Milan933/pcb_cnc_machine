# Hardware procurement / measurement freeze

**Date:** 2026-10-06
**Status:** active transition after owner acceptance of the preliminary Phase
4/4A architecture; hardware interfaces are not manufacturing-ready
**Controlling decision:** proposed [EDR-013](../docs/decisions/013-hardware-procurement-measurement-freeze.md)

## 1. Freeze boundary

The owner accepted the Phase 4 and Phase 4A preliminary structural
architecture baseline and the balanced O2 option. The baseline is now stable
enough to purchase low-regret characterization material and representative
hardware. It is not permission to draw final pockets, drill patterns, spindle
mounts, bearing cartridges, or production fastener lengths.

The O2 values remain:

| Metric | Owner-accepted preliminary value | Evidence status |
| --- | ---: | --- |
| PETG structural parts | 19 | CAD review count |
| Critical structural PETG parts | 8 | CAD classification |
| Primary force-loop PETG parts | 9 | CAD classification |
| Primary force-loop PETG joints | 7 | Pair-level review register |
| CAD solid-equivalent PETG mass | 4.720329 kg | Calculated from review solids |
| Estimated installed PETG | 2.595-3.539 kg | Conceptual print-factor range |
| Tool-point deflection at 5 N | 0.009410 mm | Preliminary analytical estimate, not measured |
| Largest structural print | 150 x 300 x 40.75 mm | CAD bounding box and orientation record |

The 0.009410 mm value is not machine accuracy or validated physical
stiffness. The dominant compliance term is still based on assumed X/Z
structure/interface stiffness. Physical validation remains mandatory. No
further optimization for mass or part count is authorized during this freeze.

## 2. Procurement categories

| Category | Meaning | Current action |
| --- | --- | --- |
| **A - SAFE TO BUY NOW / ARCHITECTURE DEFINING** | Low-regret process material or measurement equipment that does not define a final supplier interface. | Buy now if absent. |
| **B - BUY SAMPLE / MEASURE BEFORE FINAL CAD** | Representative motion, fastening, bearing, or process hardware needed to measure the accepted class. | Buy characterization samples only; retain all evidence. |
| **C - WAIT UNTIL LATER DESIGN PHASE** | Hardware whose exact envelope, electrical behavior, workholding role, or supplier choice can invalidate the interface. | Do not place a production order. |
| **D - ALREADY OWNED / MUST IDENTIFY AND MEASURE** | Hardware supplied by the owner and explicitly excluded from new purchase recommendations. | Inventory, identify, and bench-test. |

The phrase “buy now” below means a sample or validation purchase unless a
line is explicitly marked as low-regret material. A vendor drawing is never a
substitute for measuring a clone or an unverified marketplace part.

## 3. A-D component matrix

The CAD column defines the information needed to freeze an interface. A
dimension marked “measured” must be recorded as actual min/nominal/max values,
with the instrument and sample ID; a generic family name is not evidence.
No blanket tolerance is accepted for an unidentified clone: the selected
vendor tolerance, sample min/nominal/max, and the project-level screening
limit must all be recorded. A missing vendor tolerance or an out-of-family
sample is **not-ready**, not an assumed fit.

| Cat. | Component and quantity | Nominal specification | Critical dimensions and variation screen | Dimensions CAD will need | Vendor drawing sufficient? | Physical measurement | Recommended method |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Process PETG, 1 spool or qualified existing stock | Same filament/process intended for structural parts and coupons | Lot, color, moisture condition, nozzle, layer height, perimeter policy, conditioning history | Density only as a calculation input; print process record | No | Yes, material/process record | Dry/condition per printer procedure; print and weigh a reference coupon |
| A | Basic inspection set, 1 set if absent | Caliper, steel rule, square, straightedge, feeler gauges, thread pitch gauge, multimeter | Resolution and calibration status; caliper resolution at least 0.01 mm; indicator resolution at least 0.005 mm for the 0.030 mm backlash screen | No machine interface; tool capability is recorded in test evidence | Not applicable | Yes, verify zero and repeatability | Compare against a known gauge/block or repeated measurement of a reference feature |
| A | Simple 5 N loading set, 1 set | 0.510 kg known mass, hook/rigid load fixture, or a verified 5 N spring scale | Actual mass/force and attachment offset; load must not swing into the machine | Tool-point load application location and 50 mm model arm | Not applicable | Yes | Weigh the mass or verify the scale; apply at the tool-point fixture and repeat three times |
| B | X rails, 2; X carriages, 4 | MGN12 rail, MGN12H long block; reference rail length 340 mm | Rail width/height, hole pitch, end-hole offset, straightness, hole diameter/counterbore, block W/H/L, mounting pattern, assembled height, preload/play | Actual rail seat length, rail section, hole stations, carriage envelope, block spacing, datum height | Drawing required for ordering, not sufficient for a clone | Mandatory | Measure rail with caliper/straightedge, inspect every hole station, measure block envelope and play before and after loading |
| B | Y rails, 2; Y carriages, 4 | MGN12 rail, MGN12H long block; reference rail length 310 mm | Same as X; also measure paired rail parallelism and carriage pitch/racking under the moving-bed load | Actual 300 mm supported seat, rail hole stations, carriage center offsets, assembled bed height | Drawing required, physical sample still required | Mandatory | Measure both rails on a flat reference, fit two blocks per rail, sweep a dial indicator across the pair |
| B | Z rails, 2; Z carriages, 4 | MGN9 rail, MGN9H long block; reference rail length 130 mm | Rail width/height, hole pitch/end offset, block W/H/L, mounting pattern, assembled height, preload/play, side clearance | Actual 60 mm guide spacing, rail section, hole stations, block envelope, tool-side datum height | Drawing required, clone sample must be measured | Mandatory | Caliper plus square/indicator on a temporary backplate; record any MGN12 fallback need |
| B | X screw, 1 | T8x4 lead class; finished/reference length about 360 mm | Major diameter, lead 4 mm/rev, pitch, starts, straightness/runout, threaded length, fixed/floating journal, motor-end diameter/length | Centerline, finished end-to-end length, journal diameters/shoulders, nut envelope, usable travel margins | Only if the drawing specifies the actual end machining and straightness | Mandatory | Thread pitch gauge and one-revolution lead check; V-block/indicator runout; caliper journals; inspect after machining |
| B | Y screw, 1 | T8x4 lead class; finished/reference length about 330 mm | Same as X; include front fixed-end and rear floating-end datum relationship | Centerline, finished length, journal/shoulder stack, nut envelope, bed clearance | Same as X | Mandatory | Same as X; verify the measured screw does not bind through the full Y sweep |
| B | Z screw, 1 | T8x2 lead class; finished/reference length about 145 mm | Major diameter, lead 2 mm/rev, pitch, starts, straightness, journal dimensions, motor end, power-off gravity behavior | Centerline, finished length, fixed upper journal, floating lower support, nut preload position | Only after end geometry and gravity behavior are documented | Mandatory | Lead/pitch/start check, runout indicator, caliper, vertical power-off descent test with guarded load |
| B | X/Y lead nuts, 2 minimum plus candidate spares | Adjustable split brass or dual-brass preload; polymer candidate for comparison only | Thread fit, outer envelope, mounting pattern, preload adjustment, drag, reversal backlash, spring relaxation | Nut envelope, mounting holes, adjustment access, preload direction, service clearance | No; marketplace “anti-backlash” claims are not evidence | Mandatory | Install on the measured screw; indicator reversal test in both directions, drag-torque check, cycling and preload-retention check |
| B | Z lead nut, 1 minimum plus candidate spare | Spring-preloaded/adjustable anti-backlash nut; brass fallback | Same as X/Y plus gravity hold, power-off descent, axial drag, and wear | Nut envelope, adjustment access, gravity-safe stack, service path | No | Mandatory | Vertical reversal test, controlled power-off hold test, repeated-cycle drag and backlash measurement |
| B | Fixed screw supports, 3 axis sets | Preferred: paired 8 mm-bore angular-contact bearings in a compact replaceable cartridge; alternative BK08-class support only if its internal pair is documented | Bore, OD, width, contact angle/series, arrangement (DB/O), preload method, axial retention shoulders, fit, axial displacement under 50 N, drag | Cartridge envelope, shaft shoulder/journal, bearing seat, clamp/retainer access, motor-side clearance | Drawing can define the bearing; housing drawing is not enough | Mandatory | Measure bore/OD/width; assemble on an 8 mm gauge shaft; apply axial load both directions and measure displacement/drag |
| B | Floating screw supports, 3 | 8 mm-bore radial deep-groove bearing in an axially floating BF08-class-style cartridge | Bore/OD/width, radial play, axial float travel, housing clearance, retainer friction | Radial seat, axial float allowance, retainer access, thermal/service direction | Drawing can define bearing, not the printed cartridge | Mandatory | Measure bearing and shaft fit; verify radial support and free axial movement while warm/cold cycling |
| B | Motor/screw couplers, 3 | 5 mm motor bore to measured screw journal, compact zero-backlash flexible type | Both bores, clamp screw size/access, body OD/length, angular/parallel misalignment, axial spring force, torsional backlash | Motor shaft engagement, screw journal, coupler length/guard clearance, service access | Drawing is sufficient only after shaft interfaces are measured | Mandatory | Caliper bores and length; mount between aligned shafts; indicator axial force and torsional reversal test |
| B | M3 heat-set inserts, minimum 20 per candidate family | M3 reusable PETG insert sample; no generic pocket geometry | Maximum knurl OD, minimum body OD, length, flange/taper, thread depth, installation tool access | Actual OD/length/pilot range/insertion depth, boss wall, edge distance, screw clearance | No; drawing is a candidate input | Mandatory | Caliper/micrometer, thread gauge, visual taper/knurl record, installation temperature/process coupon |
| B | M4 heat-set inserts, minimum 20 per candidate family | M4 structural/module insert sample | Same as M3 | Same as M3; M4 is the default structural/module class | No | Mandatory | Same as M3 plus pull-out, torque, preload-creep, and repeated-service coupons |
| B | M5 heat-set inserts, minimum 10 per candidate family | Conditional M5 sample only; not a default purchase | Same as M3; record flange and through-bolt alternatives | Only if a named load/moment/creep review justifies M5 | No | Mandatory if M5 remains in the design | Same as M3; reject unless geometric shear path and technical justification exist |
| B | Fastener sample assortment, M3/M4/M5, 1 assortment | Socket-head screws, washers, nuts where useful; mixed short/medium/long samples, not final lengths | Thread quality, head OD/height, under-head bearing, washer OD/thickness, nut width/height, grade/material | Diameter, head clearance, engagement, access, washer/spreader, final length after measured stack | Standard fastener drawing is sufficient for nominal hardware; not for final stack | Measure representative samples | Caliper/thread gauge; assemble into coupons; record stripped threads and tool access |
| B | Limit switch and probe samples, 3 limits plus 1 probe method | Accessible, fault-detectable switches; conductive probe compatible with controller candidate | Actuator height/travel, repeatability, body/lever envelope, connector exit, probe tip, cable bend radius | Switch datum, hard-stop relationship, wiring path, probe datum/stow position | Drawing is sufficient for envelope only | Mandatory before final mounts | Repeated actuation with indicator; continuity/open-circuit fault test; sweep cable and tool volume |
| B | Spoilboard sample, 1 of each candidate | Default sample: 230 x 180 x 12 mm MDF; compare surfaced machinable board/phenolic if needed | Actual thickness, density, flatness after skim, moisture/edge damage, screw/adhesive response | 230 x 180 x 12 nominal process surface, replacement datum, skim allowance, fastener pattern | Material data is not sufficient for flatness | Mandatory for chosen material | Measure thickness/grid flatness, skim a sample, remeasure relative to machine datum, test PCB support |
| B | Machine feet/table interface, 4 sample interfaces | Rubber/metal leveling or isolation feet compatible with the O2 base concept | Height range, contact area, load, thread/washer stack, slip, vibration response | Contact plane, fastener access, leveling range, table clearance | Drawing is sufficient for envelope only | Mandatory before final base feet | Caliper and simple load/rocking check on a flat table |
| C | Final spindle, 1 | PCB spindle selected against the specification in Section 9; do not auto-purchase | Speed, radial/axial TIR, power, mass, diameter, length, ER collet system, cable exit, cooling, bearing noise/quality, voltage | Actual clamp diameter/shape, nose/tool centerline, mass center, cable/thermal clearance, mount fasteners | Vendor drawing and test report required, then physical inspection | Mandatory before mount CAD | Indicator TIR with actual collet/tool; weigh; caliper; temperature/noise/cable test |
| C | Final ER collets and PCB tool set | ER11-class or better match to selected spindle; 3.175 mm and small-tool coverage | Collet runout, tool range, nut envelope, tool stickout, tool retention | Collet/nut/body clearances, tool length and process datum | Drawing/test report required; actual runout still required | Mandatory for process release | Measure with indicator and actual V-bit/drill/end mill; document tool seating |
| C | Final workholding, clamps, tape, vacuum, or registration hardware | Support 200 x 150 PCB without bowing and leave probing/tool access | Clamp force, board contact, flatness, thickness, registration repeatability, cable/probe access | PCB datum, clamp envelope/swept volume, replacement workflow, final-pass support | No | Mandatory | Indicator/grid height map under clamp load; repeat load/unload and inspect board movement |
| C | Production spoilboard and replacement stock | Chosen surfaced material, initial reference 230 x 180 x 12 mm | Batch thickness/flatness, resurfacing allowance, attachment and datum repeatability | Final mounting holes/slots, datum face, skim depth, replaceability | Material drawing insufficient | Mandatory | Grid measurement before/after skim and after workholding load |
| C | Production O2 PETG parts, 19 parts | O2 structural architecture only; no final supplier-specific pockets yet | Printer conditioning, warp, layer orientation, mass, rail datum, joint creep, insert fit | Measured hardware-driven dimensions, datums, tolerances, print orientation, release metadata | No | Mandatory | Print representative coupons first; no production release before evidence gate |
| D | Owned NEMA17 motors, at least 3 candidates plus spares | **OWNER-SUPPLIED — DO NOT BUY**; final axis assignment comes from stock characterization | Model/label, body length, rated current, holding torque, resistance, shaft diameter/length/flat, connector, step angle, 42.3 mm mounting interface, bearing play, temperature | Generic 42.3 mm square, screening 5 mm shaft, 40-48 mm body envelope, plus rear connector/wiring access; exact values remain measured | Label/datasheet helpful, not sufficient for unidentified motors | Mandatory for final assignment/manufacturing interfaces; not required to start preliminary structural CAD | Use the identification sheet; caliper, ohmmeter, visual wiring trace, guarded low-speed bench test |
| D | **Owner-supplied Arduino Mega + CNC Shield**, 1 intended controller platform | **OWNER-SUPPLIED — DO NOT REPLACE absent a validated limitation**; exact Shield revision and installed drivers unresolved | Shield revision, Arduino Mega board revision, driver carriers/models, jumpers, supported microsteps, supply-voltage/current capability, current setting, cooling, spindle PWM/control, probe/limits, pinout, GRBL-compatible firmware/configuration | Board envelope, connector exits, driver heatsink clearance, electrical interfaces, enclosure/service access | Board drawing/manual helpful, physical revision identification mandatory | Mandatory | Photograph/mark revision, trace pins with continuity meter, read firmware/settings, bench-test limits/probe/spindle output |
| D | Installed driver carriers and wiring, existing set | Owner-supplied with the controller; do not buy replacement modules unless a validated limitation is found | Carrier model/marking, current-limit method, microstep jumpers, heatsink, motor supply, wiring gauge/connectors | Driver cooling/enclosure, wire bend radius, connector access, current setting | Datasheet not enough for clone carriers | Mandatory | Read markings, continuity/pinout, measure supply/current setting, temperature test under load |

### 3.1 Category decision summary

| Action visible to owner | Items |
| --- | --- |
| **BUY NOW** | Process-matched PETG; basic caliper/square/straightedge/feeler/thread-gauge set if absent; an indicator and simple 5 N loading set if absent. A 230 x 180 x 12 mm MDF sample is a low-regret process sample, not a final workholding release. |
| **BUY SAMPLE NOW** | Complete accepted motion-class sample set in Section 4; T8 screw/nut candidates; fixed/floating 8 mm bearing candidates; 5-to-measured-journal couplers; M3/M4/M5 insert candidates; M3/M4/M5 fastener assortment; limit/probe and spoilboard samples. |
| **MEASURE EXISTING HARDWARE** | Owner-supplied NEMA17 stock, the Arduino Mega + CNC Shield platform, installed driver carriers, and existing wiring. |
| **WAIT** | Final spindle, final collets/tools, final clamps/vacuum/workholding, production spoilboard batch, production PETG parts, final insert pockets, final fastener lengths, and any replacement hardware that later validation might justify. No motor or controller replacement is recommended now. |

## 4. Linear-rail purchase decision

The owner-accepted architecture requires the following exact axis quantities;
these are characterization quantities and reference lengths, not a supplier
release:

| Axis | Rails | Carriages | Reference rail length | Target travel | Purchase decision |
| --- | ---: | ---: | ---: | ---: | --- |
| X | 2 x MGN12 | 4 x MGN12H | 340 mm | 220 mm | Buy a complete sample set at 340 mm if the selected vendor supplies that length and drawing. Otherwise buy the nearest standard length **longer than 340 mm** and retain it uncut. |
| Y | 2 x MGN12 | 4 x MGN12H | 310 mm | 170 mm | Buy 310 mm if documented; otherwise buy the nearest standard length longer than 310 mm and retain it uncut. |
| Z | 2 x MGN9 | 4 x MGN9H | 130 mm | 40 mm | Buy 130 mm if documented; otherwise buy the nearest standard length longer than 130 mm and retain it uncut. |

Do not cut a rail merely to match the nominal number. Rail end-hole offset,
end squareness, hardening, and burrs can make a cut rail unusable. Retain a
longer rail until the measured carriage/stop stack and final rail datum are
reviewed. If cutting is unavoidable, cut only after a datum is chosen, face
and deburr the end, preserve or re-establish the end-hole offset, and verify
straightness, hole position, and carriage travel after cutting.

### Rail interface record

The selected HIWIN catalog classes give these reference carriage envelopes;
clone marketplace products must not be treated as identical:

| Class | Candidate rail width | Candidate mounting pitch/end offset | H carriage assembly W x H | H carriage L | Release condition |
| --- | ---: | --- | ---: | ---: | --- |
| MGN9H | approximately 9 x 6 mm rail body class | 20 mm pitch / 10 mm end offset are catalog screening values only | 20 x 10 mm | 39.9 mm | Verify rail body height, pitch, offset, hole form, block pattern, preload, and play on the selected sample. |
| MGN12H | approximately 12 x 8 mm rail body class | 25 mm pitch / 10 mm end offset are catalog screening values only | 27 x 13 mm | 47.6 mm | Verify rail body height, pitch, offset, hole form, block pattern, preload, and play on the selected sample. |

For every rail/block set record: rail width and body height; mounting-hole
pitch and end-hole offset; hole diameter/counterbore; carriage width, height,
length, and mounting-hole pattern; assembled rail/block height; preload code;
drag; radial play; and the variation across all blocks. The drawing is
sufficient to plan a sample order, but physical measurement is mandatory for
manufacturing CAD. Use the actual measured worst-case envelope plus documented
clearance; do not invent a universal clone tolerance.

As an axis screening check, record straightness and installed parallelism
against the existing project targets of <=0.050 mm/100 mm target and
<=0.100 mm/100 mm provisional acceptance. These are machine screening limits,
not a claim about the raw rail.

## 5. Lead-screw purchase decision

For a multi-start screw:

- **lead** is axial travel per revolution;
- **pitch** is axial spacing between adjacent thread crests;
- **starts** is the number of independent thread starts;
- `lead = pitch x starts`.

The requested classes therefore mean T8 nominal major diameter with 4 mm or
2 mm lead. A T8x4 sample may be a 2-start, 2 mm-pitch screw and a T8x2 sample
may be a 1-start, 2 mm-pitch screw, but the supplier declaration and a physical
lead/pitch/start check are required.

| Axis | Qty | Lead class | Finished/reference length | Recommended unmachined purchase minimum | End strategy |
| --- | ---: | --- | ---: | ---: | --- |
| X | 1 | T8x4 | about 360 mm | nearest standard blank >=400 mm when end machining is needed | Keep full length until fixed/floating journal and motor-end stack are measured. |
| Y | 1 | T8x4 | about 330 mm | nearest standard blank >=370 mm when end machining is needed | Keep full length until front fixed-end and rear floating-end stacks are measured. |
| Z | 1 | T8x2 | about 145 mm | nearest standard blank >=180 mm when end machining is needed | Keep full length until upper fixed journal, lower float, and gravity-safe nut stack are measured. |

The 400/370/180 mm values are practical blank-length recommendations with
post-processing allowance, not CAD finished lengths or claims about available
catalog sizes. If a vendor supplies drawing-controlled machined ends, buy the
nearest documented finished length instead. If a blank is cut, the required
post-processing is: square/face the cut, turn or otherwise finish the bearing
journals, chamfer and deburr the motor end, remove thread damage, clean the
nut path, and remeasure major diameter, straightness/runout, journal diameter,
shoulders, and usable threaded length.

## 6. Nut, bearing, and coupler decisions

### Lead nuts

The preliminary preferred strategy is an adjustable split-brass or dual-brass
preload nut on X and Y, with a spring-preloaded/adjustable nut on Z. Polymer
anti-backlash nuts are a comparison sample, not the default, because PETG-like
creep, temperature, and wear can relax preload. Standard loose brass is a
control sample only.

Accept a candidate only after measuring reversal backlash at the installed
preload, drag torque/force through the full screw, axial hysteresis, preload
retention after cycling, and wear/temperature behavior. The target is
**<=0.030 mm** reversal backlash; the existing **<=0.050 mm** value remains a
provisional acceptance limit and is not an automatic release. Test Z for
gravity creep and power-off descent with the actual moving load.

### Fixed/floating bearings

The preferred topology is one fixed end per screw using either:

1. a matched pair from an 8 mm-bore angular-contact series such as 708/8,
   718/8, or 719/8 in a DB/O arrangement, with light controlled preload, an
   axial shoulder/retainer, and a replaceable cartridge;
2. a compact BK08-class support only if the supplier identifies the internal
   paired bearing arrangement and axial rating; or
3. a simpler deep-groove arrangement only as a measured low-force comparison
   sample, not by convention.

The opposite end is one 8 mm-bore radial bearing in a replaceable BF08-style
cartridge that supports radial runout while allowing axial thermal freedom.
The exact angular-contact series, seal/open form, matched preload, spacer, and
retainer are supplier/sample choices; do not substitute a nominal 8 mm bearing
without checking its axial capacity and fit. The screw interface is an 8 mm
nominal journal only until the actual end machining is measured.
The fixed bearing must carry the screw thrust in both directions. Neither the
motor bearing nor the coupler is an axial bearing. Compare the candidates
quantitatively using axial displacement under the existing 50 N screw design
screen, drag torque, runout, temperature after cycling, and free axial float
at the floating end.

### Couplers

The motor interface is expected to be 5 mm. The screw interface is **not
frozen at 8 mm** until the machined journal is selected and measured. Buy
5-to-8 mm samples only when the screw-end sample uses that journal, and keep a
5-to-measured-journal alternative available.

| Type | Strength | Risk | Preliminary disposition |
| --- | --- | --- | --- |
| Helical/beam | Compact, zero nominal backlash, simple service | Can transmit axial parasitic force when misaligned; limited misalignment | First sample for compactness; measure axial spring force and runout. |
| Oldham | Good parallel/angular misalignment tolerance and low axial coupling force | More parts, insert wear, possible lost motion if worn | Preferred comparison/fallback if helical axial force is excessive. |
| Jaw/spider | Common and easy to replace | Spider compliance and backlash can enter a low-force axis | Do not default; accept only with measured reversal and axial-force evidence. |

All types transmit torque only. The test must cover bore/clamp access,
torsional reversal, angular/parallel misalignment, axial parasitic force,
guard clearance, and service replacement.

## 7. Owned motor and controller identification

The owner already has a large selection of NEMA17 motors and an intended
**Arduino Mega + CNC Shield** controller platform. NEMA17 motors are
**OWNER-SUPPLIED — DO NOT BUY**. The controller is **OWNER-SUPPLIED — DO NOT
REPLACE** unless later electrical or motion validation identifies an actual
limitation. Fill the separate [identification sheets](hardware-identification-sheets.md)
for every representative motor and the controller assembly.

Preliminary structural CAD uses a standardized common NEMA17 mechanical
interface rather than one exact motor model: approximately 42.3 mm mounting
square, screening 5 mm shaft, and a 40-48 mm body envelope. Motor mounts must
retain rear clearance for connector exit, wiring bend radius, strain relief,
and service access across multiple common 3D-printer motor body lengths. The
exact rear-access dimension is not frozen until representative owner motors
are measured. This unresolved final motor assignment does **not** block the
preliminary structural CAD envelope; it blocks manufacturing-ready interfaces
and commissioning only.

Assign normal suitable owner motors to X/Y after characterization. Assign the
strongest suitable owner motor to Z only if it remains electrically compatible
with the identified driver and supply.

Motor screening minimums are **>=0.45 N-m holding torque for X/Y** and
**>=0.55 N-m for Z**. Holding torque alone is not acceptance: rated current,
torque at operating speed, driver current, acceleration, screw efficiency,
preload, and temperature must be checked.

The controller checklist must establish exact CNC Shield model/revision,
Arduino Mega board revision, installed stepper-driver modules, supported
microstep configuration, motor-current capability, supply-voltage capability,
cooling, spindle PWM/control outputs, probe input, limit inputs, pinout,
GRBL-compatible firmware/configuration strategy, homing direction, pull-off,
debounce, soft limits, and alarm behavior. A4988 and DRV8825 are only marking
examples until the installed carriers are identified; a printed or marketplace
carrier must be identified by its actual marking and thermal/current behavior.

## 8. Heat-set inserts and fastener schedule

Purchase M3, M4, and conditional M5 samples as described in the matrix. For
each selected insert family record maximum knurl OD, minimum body diameter,
total length, flange diameter, taper, thread depth, pilot-hole range,
insertion depth, tool access, and installation temperature/process. Generic
internet dimensions must not become pocket geometry.

Print at least three PETG coupon types for each selected size/family:

1. a pilot-hole ladder covering the supplier range and one installation
   procedure;
2. pull-out and torque coupons with at least three installed inserts per load
   mode;
3. repeated-assembly and preload-creep coupons with at least two inserts,
   conditioned and rechecked after the planned service cycle.

Record boss-wall deformation, edge cracking, insertion depth, pull-out,
torque, preload retention, and failure mode. The coupon does not freeze a
production boss until the selected insert and installation process are
accepted.

Use this preliminary fastener hierarchy:

| Size | Intended use | Sample quantity | Final length/quantity |
| --- | --- | ---: | --- |
| M3 socket-head | Rail screws, limits, probe, cable, small accessories | 100 mixed samples | Derive from measured rail pitch, stack, and access; no length frozen |
| M4 socket-head | General structural/module joints, cartridges, motor/spindle modules | 50 mixed samples | Derive from measured insert depth, shoulder, washer, and engagement |
| M5 socket-head | Only a named high-preload/moment/creep escalation | 10 conditional samples | Zero default; requires EDR-013 follow-on justification and geometric shear path |
| Washers | Bearing/load spread and selected through-bolt interfaces | 25 per used size | Select OD/thickness after joint load-path review |
| Nuts | Only where a through-bolt is justified or a metal subassembly needs one | 25 per used size | Do not treat nuts as precision locators |

## 9. Spindle procurement specification

Do not purchase the final spindle automatically. Screen a candidate for all
three processes: PCB isolation routing, drilling, and outline cutting.

| Property | Screening specification |
| --- | --- |
| Speed | 10,000-30,000 rpm usable; initial process trials 12,000-26,000 rpm |
| Runout | Target <=0.010 mm TIR; provisional maximum <=0.020 mm TIR at the actual tool shank, measured |
| Power | 50-150 W continuous/equivalent screening class; more power is not automatically better |
| Mass | 0.30-0.80 kg screening class, with tool-point stiffness check if heavier |
| Diameter | Compare approximately 25, 40, and 52 mm body classes; 52 mm is a maximum reference screen, not a selection mandate |
| Tooling | ER11-class or better compatibility for 3.175 mm / 1/8 in shanks and matched small-tool collets |
| Mechanical | Nose length, centerline, clamp length, cable exit, cooling/heat, bearing quality, replacement collets, and service access recorded |
| Electrical | Voltage, current/power supply, enable/PWM or external speed control, shielding/grounding, and controller compatibility |
| Process | Noise, vibration, axial seating/runout, tool stickout, PCB dust containment, and thermal behavior tested |

A better PCB spindle may require a minor mount adaptation. The 52 mm envelope
must not force selection of an inferior spindle; the mount remains a
replaceable interface until the spindle is measured and the adaptation is
reviewed.

## 10. Spoilboard and workholding

Use a replaceable process surface with a known machine datum and a repeatable
replacement/probing relationship. The current P2 reference is **230 x 180 x
12 mm**.

- **MDF:** default first sample. It is inexpensive, easy to skim, and easy to
  replace. Seal or protect edges if moisture changes the datum.
- **Cast tooling plate:** evaluate only if the measured MDF flatness, creep,
  vibration, or repeated resurfacing is inadequate; its added moving-bed mass
  must be justified.
- **Other surfaced board/phenolic:** a controlled comparison if MDF dust,
  moisture, or screw retention is a problem.

The final choice must be skimmed relative to the machine datum, measured on a
grid before and after workholding load, and replaceable without silently
changing the G54/PCB datum. Final clamps, vacuum perimeter, tape, and board
registration remain Category C until the first board process mock-up.

## 11. Physical validation hardware

### Required (buy or confirm ownership before the tests)

- 0.01 mm digital caliper plus a steel rule, machinist square, straightedge,
  feeler gauges, thread-pitch gauge, and multimeter;
- dial indicator with at least 0.005 mm readable resolution and a magnetic or
  rigid base for rail parallelism, screw runout, backlash, and 5 N deflection;
- a known 0.510 kg mass or verified 5 N spring scale and a rigid load fixture;
- one representative MGN12 sample pair/block set and one MGN9 sample
  pair/block set;
- T8x4 and T8x2 screw samples with candidate nuts;
- fixed/floating 8 mm bearing samples and 5-to-measured-journal coupler
  samples;
- M3/M4/M5 insert and fastener samples;
- PETG from the intended print process and a flat reference surface for
  coupons;
- a safe low-voltage bench supply/current measurement method for the owned
  controller and motors, with guards and an emergency disconnect.

No granite table, coordinate measuring machine, force gauge, or specialized
metrology system is assumed. If a dial indicator is unavailable, do not claim
rail parallelism, backlash, or 5 N deflection as verified; obtain or borrow
one before the gate.

### Nice to have

Granite surface plate, height gauge, gauge blocks, calibrated force gauge,
micrometer, torque screwdriver, thermal camera, microscope, spindle tachometer,
runout artifact, and a small surface grinder or controlled skim fixture.

## 12. Required physical coupons

| Coupon | Hardware | Measurements / pass evidence |
| --- | --- | --- |
| PETG process and conditioning | Intended PETG, printer, same nozzle/layer/perimeter process | Mass, dimensions, warp, layer adhesion, conditioning shift, repeatability |
| 300 mm rail-seat | Representative MGN12 rail/block and O2 base/Y seat concept | Long-axis warp, supported datum skim/shim, hole access, parallelism, carriage preload |
| MGN9 Z seat | MGN9 rail/block and X/Z backplate concept | 60 mm pair spacing, vertical square, block drag/play, tool-side clearance |
| T8 screw/nut | T8x4 and T8x2 screws with each candidate nut | Lead/pitch/starts, runout, reversal backlash, drag, preload retention, Z gravity hold |
| Fixed/floating bearing pocket | 8 mm bearings and representative cartridge | Axial retention in fixed set, free float at opposite set, runout, service replacement |
| Coupler alignment | 5 mm motor shaft and measured screw journal | Torsional reversal, axial parasitic force, misalignment, clamp access, guard clearance |
| M3/M4/M5 insert | Each selected insert family and PETG coupons | Pilot ladder, installation, pull-out, torque, wall deformation, repeat assembly, creep |
| J1/structural joint | O2 integrated gantry interface, M4 sample hardware | Seating, shear transfer, preload retention, creep, repeated disassembly, failure mode |
| Spindle mount/thermal | Candidate spindle or representative measured envelope | Clamp fit, centerline, cable/thermal clearance, TIR, vibration/noise, service access |
| Moving bed/spoilboard | 230 x 180 x 12 material and workholding sample | Flatness, board support, load distortion, replacement datum, probing access |

## 13. Minimum tests before production CAD

All of the following must be recorded as pass, fail, or not-ready with sample
IDs and instruments:

1. Identify every owned motor, controller, driver, and wiring path; confirm
   motor current/torque evidence against the X/Y 0.45 N-m and Z 0.55 N-m
   screens.
2. Measure the complete rail/block geometry and clone variation; verify two
   rails/two blocks per rail on every axis can be aligned and serviced.
3. Measure screw lead, pitch, starts, straightness, usable thread, journals,
   motor ends, nut drag, and reversal backlash; achieve the <=0.030 mm target
   or record the owner disposition for the provisional <=0.050 mm limit.
4. Verify fixed-end axial constraint in both directions and floating-end axial
   freedom; demonstrate that the motor and coupler carry no screw thrust.
5. Verify coupler torsion, misalignment, axial parasitic force, and replacement
   access with the measured shaft/journal pair.
6. Complete M3/M4/M5 insert coupons and select no pocket dimension until the
   actual insert and installation procedure pass.
7. Condition and inspect the 300 mm rail-seat/base coupon, the integrated
   gantry/joint coupon, and the MGN9 Z seat; measure warp, datum condition,
   shim/skim allowance, and repeated preload.
8. Mock up full X/Y/Z travel with measured rails, screws, nuts, bearings,
   motors, couplers, limits, probe, cables, spindle envelope, bed,
   spoilboard, and workholding; verify assembly/removal sequence.
9. Perform the separated 5 N tool-point test with the simple known load and
   indicator, recording beam/tower/joint, X/Z, base/rail-seat, and bed
   contributions where practical. Label every result measured; do not replace
   it with the 0.009410 mm calculation.
10. Measure the selected spindle/tool TIR, mass, centerline, thermal/cable
    envelope, and process suitability before freezing its mount.
11. Verify spoilboard grid flatness, resurfacing allowance, PCB support,
    registration, clamp distortion, probe repeatability, and map datum.

Until these tests are complete, the O2 structural files remain review CAD and
the hardware interface state is **not-ready**. No production STEP/STL/drawing
release and no Phase 5 production CAD may begin.

## 14. Measurement record rules

Every measurement record must include: date, operator, sample/vendor/lot ID,
instrument ID and resolution, calibration/zero check, units in millimetres or
newtons, temperature where relevant, raw readings, min/nominal/max summary,
photograph or sketch for orientation, pass/fail/not-ready status, and the
affected CAD datum/interface. A supplier drawing may be attached as a source,
but a clone or unidentified part remains not-ready until physically measured.
