# Calculation plan

Calculations are evidence, not decoration. Every calculation records its
inputs, units, assumptions, result, sensitivity, and whether it has been
experimentally verified.

## Planned calculations

### Commanded motion resolution

For a screw-driven axis, the nominal commanded linear increment is:

    increment = lead / (motor_steps_per_revolution * commanded_microsteps)

This is a command resolution, not an accuracy or repeatability claim. Backlash,
elasticity, screw error, driver behavior, and controller limits must be
considered separately.

### Screw speed and feed

    linear_speed = screw_lead * screw_revolutions_per_minute

The selected speed must also satisfy motor torque, screw critical-speed,
nut-life, lubrication, vibration, and process-feed constraints.

### Tool loading and Z force loop

Use a documented cutting-force estimate or measured force at the selected tool,
material, depth, width, and feed. Resolve that load through the spindle mount,
Z guide spacing, gantry, base, and workholding. Report tool-point deflection
and angular error, not only a bulk frame stress number.

### Rail and bearing loading

Use the actual carriage spacing, load direction, preload, overhang, and
moment. A catalogue static rating alone is insufficient for tool-point
stiffness.

### Printed structure

Use a conservative PETG material model that identifies filament, print
orientation, temperature, layer bonding, perimeter count, and conditioning.
Separate short-term stiffness from creep and long-term preload retention.

## Calculation record policy

Do not add more significant figures than the inputs justify. Label values as
known, assumed, preliminary, calculated, or verified. If a result changes an
architecture decision, create or update an engineering decision record.

The current Phase 1 equations and screening calculations are in
[phase-1-calculations.md](phase-1-calculations.md).

The focused A/B equivalent-section, joint, dynamic, racking, and sensitivity
calculations are in
[phase-2a-structural-calculations.md](phase-2a-structural-calculations.md).

The Phase 3 screw resolution, torque, guide-reaction, and critical-speed
screen is in
[phase-3-motion-calculations.md](phase-3-motion-calculations.md).
