---
name: motion-mechanism-design
description: Select and integrate generic motion mechanisms, guides, bearings, shafts, screws, belts, couplers, actuators, limits, and cable envelopes using complete force and motion chains.
---

# Motion and mechanism design

Use this skill for mechanisms with constrained motion, whether linear, rotary, indexed, compliant, or combined. A motion component is part of a chain; evaluate the chain rather than selecting isolated hardware.

## Complete chain

For each axis or mechanism trace:

```text
actuator → transmission → coupling → shaft/screw → bearing supports
→ guide/contact constraints → moving body → load/tool → structural reactions
```

At every link identify radial, axial, torsional, moment, thermal, and misalignment loads. Include friction, preload, gravity, cable drag, acceleration, impact, and the required service margin.

## Constraint and motion model

- State the intended DOF and the constraints that remove every unwanted DOF.
- Separate axial location from radial support and distinguish fixed/locating from floating/non-locating supports.
- Avoid overconstraint: parallel guides, bearings, shafts, and couplers need a tolerance and alignment strategy.
- Define hard stops, homing/limit behavior, soft limits, moving cable envelopes, end margins, and recovery after faults.
- Check motion at minimum, nominal, and maximum positions, not just at the parked pose.

## Component reasoning

**Guides, shafts, and bushings:** evaluate span, carriage/bearing spacing, preload, moment capacity, mounting-surface stiffness, clearance, wear, contamination, lubrication, alignment, and replacement. Include linear rails and plain or rolling bushings according to their actual load and life limits.

**Bearings:** define which ring is axially located, which support is free to accommodate thermal or assembly displacement, how loads reach the housing, and how the bearing is retained and serviced.

**Leadscrews, ballscrews, belts, pulleys, and other transmissions:** check lead or ratio, resolution versus accuracy, speed, torque, efficiency, backlash, whip or critical speed, tension, wear, lubrication, and end support.

**Couplers:** check bore, clamping access, shaft engagement, torsional stiffness, angular/parallel/axial misalignment, guard clearance, service factor, and replacement. Do not use a flexible coupler as an unselected bearing or axial support.

Also check Abbe error, moment arms, racking, backlash, preload, hard-stop loads, and moving cable envelopes whenever they can affect the functional output.

**Motors and actuators:** select from duty torque/force at speed, acceleration, driver/controller compatibility, thermal duty, inertia, and failure behavior. Holding torque or package size alone is not a selection method.

## Good vs bad

**Bad:** A screw, motor, two bearings, and a guide are placed along a visually straight line, with both bearings axially clamped and the coupler assumed to absorb all error.

**Good:** The load and moment are calculated, one support locates the shaft axially, the other permits the required displacement, guide spacing reacts the moment, the coupler handles only its specified misalignment, and travel/limits/cable clearance are checked over the full stroke.

Use [mechanical-assembly-design](../mechanical-assembly-design/SKILL.md) for the mechanism’s assembly and [cad-hardware-integration](../cad-hardware-integration/SKILL.md) for component evidence.
