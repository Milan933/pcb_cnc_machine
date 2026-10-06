# Owned hardware identification sheets

These are fill-in records for the hardware already owned by the project. Do
not purchase replacement motors or a controller until the sheets are complete
and the measured results are compared with the motion requirements.

## NEMA17 motor sheet

Create one copy of this table for each motor, including spares.

| Field | Motor M__ record |
| --- | --- |
| Inventory ID / photograph |  |
| Manufacturer and model |  |
| Body length and measured body envelope |  |
| Mounting pattern | 42.3 mm square nominal; measured hole/face details: |
| Rated phase current |  |
| Holding torque and source |  |
| Torque-speed curve/source |  |
| Phase resistance A-B / B-C and test current |  |
| Step angle |  |
| Shaft diameter, length, flat, and usable engagement | 5 mm is a screening expectation, not a fact |
| Connector, pinout, and wire colors |  |
| Bearing play/noise |  |
| Temperature under identified driver/current |  |
| Candidate axis | X / Y / Z / spare |
| Screening result | X/Y >=0.45 N-m; Z >=0.55 N-m; torque-at-speed evidence: |
| Owner disposition |  |

Use a caliper for body/shaft dimensions, an ohmmeter for winding resistance,
the motor label/datasheet for identity, and a guarded low-speed bench test for
direction, noise, temperature, and missed-step behavior. Do not infer torque
from frame size or holding torque from a marketplace photograph.

## Arduino CNC Shield / GRBL controller sheet

| Field | Controller record |
| --- | --- |
| Controller inventory ID / photographs |  |
| Shield revision and visible markings |  |
| Arduino type and board revision |  |
| GRBL fork/version and settings dump |  |
| Driver carrier positions/models | X:  / Y:  / Z:  |
| A4988/DRV8825/other marking |  |
| Microstep jumper configuration | X:  / Y:  / Z:  |
| Motor supply voltage and current capability |  |
| Driver current-limit method and measured setting |  |
| Heatsink/fan/cooling arrangement |  |
| STEP/DIR pin mapping |  |
| Limit inputs and pull-up/fault behavior | X:  / Y:  / Z:  |
| Probe input and open-circuit behavior |  |
| Spindle enable/PWM/output voltage |  |
| Grounding, shielding, and cable entry |  |
| Homing direction, pull-off, debounce, soft limits, alarm behavior |  |
| Bench-test result |  |
| Owner disposition |  |

Identify the board physically with photographs and continuity checks before
wiring. A driver IC datasheet does not establish the capability of a clone
carrier, its cooling, or its current limit.
