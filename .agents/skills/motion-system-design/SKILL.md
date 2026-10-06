---
name: motion-system-design
description: Select and review CNC axes, guides, screws, motors, bearings, couplers, limits, and homing using travel, stiffness, speed, load, and service requirements.
---

# Motion-system design

Use this skill to compare motion-system candidates and integrate them into a
PCB CNC architecture. Candidate names are not selections. Select from
requirements and evidence.

## Selection sequence

1. Allocate required tool-point travel and clearance, including tool length,
   workholding, probe access, and safe retracts.
2. Define the force and moment at each guide and screw interface.
3. Compare axis layouts for Z loop length, moving mass, span, alignment, and
   service access.
4. Select guide, screw or transmission, bearing, motor, coupling, and limit
   interfaces as a compatible set.
5. Verify commanded resolution, speed, torque margin, backlash, critical
   speed, stiffness, and assembly access.
6. Record the choice, alternatives, inputs, and remaining tests in an EDR.

## NEMA 17 motors

NEMA 17 is a frame-size family, not a torque specification. Identify each
owned motor by model and measure or obtain:

- rated current and winding resistance;
- holding torque and torque-speed curve;
- shaft diameter, length, and flats;
- connector and mounting pattern;
- temperature and duty limits;
- condition and bearing play.

Select a motor from torque at the required speed and acceleration, not holding
torque alone. Include screw efficiency, preload, friction, moving mass,
cutting load, cable drag, and a documented margin. Confirm that the owned
driver/controller can supply the required current and voltage.

## Linear guides

Compare MGN9, MGN12, and any other candidate by rail and carriage stiffness,
moment capacity, preload, carriage spacing, mounting surface requirements,
contamination tolerance, availability, and serviceability. MGN9 or MGN12 must
not be selected merely because the machine is small.

Use guide spacing and carriage arrangement to resist the actual tool moment.
Do not rely on one small carriage to react a wide spindle load if a distributed
arrangement materially improves pitch, yaw, or roll stiffness.

## Lead screws and transmissions

Evaluate T8x2 and T8x4, plus alternatives if justified, using:

- lead and nominal commanded resolution;
- required speed and acceleration;
- motor torque at speed;
- efficiency and heat;
- backlash and anti-backlash behavior;
- critical speed and whip;
- axial support and nut preload;
- contamination and lubrication;
- availability and replacement.

Nominal commanded increment for a screw is:

    lead / (full_steps_per_revolution * commanded_microsteps)

This is neither accuracy nor repeatability. Account for screw pitch error,
backlash, compliance, driver current, and controller step limits.

Linear speed is approximately:

    lead * screw_revolutions_per_minute

Use consistent units and record whether the lead is per revolution or pitch
per thread. Do not promise a feed rate from this equation alone.

## Bearing arrangements and couplers

Define which bearings locate the screw axially, which allow thermal or
assembly movement, and how axial load reaches the structural frame. Prevent
the motor bearing or flexible coupler from carrying loads for which it was not
selected.

A coupler must accommodate measured alignment error without becoming a
significant torsional spring or axial support. Check bore, shaft length,
clamping access, guard clearance, and service replacement.

## Axis layouts

For X and Y, compare moving-gantry, moving-bed, and other layouts against PCB
support, moving mass, rail span, cable management, and access. For Z, minimize
tool overhang and moving stack height while preserving the required
30-50 mm preliminary travel range and tool/workholding clearance.

Do not freeze an axis layout until the travel budget includes carriage
lengths, screw supports, hard stops, tool length, probe clearance, and
homing/limit margins.

## Limits and homing

Provide independent, accessible limit or homing switches with a known
actuation direction and repeatability. Define:

- homing sequence and safe movement;
- switch mounting stiffness;
- hard-stop relationship;
- normally-open or normally-closed policy;
- cable routing and shielding;
- controller input and firmware behavior;
- soft travel limits after homing;
- recovery behavior after a switch fault.

Do not use a flexible printed feature as the only homing datum without a
repeatability test.

## Motion evidence

The motion decision record must show travel budgets, guide loads and moments,
screw speed and torque calculations, motor and driver data, backlash strategy,
bearing arrangement, switch access, and unresolved supplier or test inputs.
