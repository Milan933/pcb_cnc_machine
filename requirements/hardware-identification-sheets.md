# Owned hardware identification sheets

These are fill-in records for hardware already owned by the project. The
status boundary is explicit:

- **NEMA17 motors: OWNER-SUPPLIED — DO NOT BUY.** Final axis assignment is
  made from the owner's stock after characterization.
- **Controller: OWNER-SUPPLIED — ARDUINO MEGA + CNC SHIELD.** Do not replace
  it unless later electrical or motion validation identifies an actual
  limitation.

The exact motor identities, CNC Shield revision, installed driver modules, and
electrical behavior still require measurement. Those items block final
electrical/mechanical interfaces and commissioning, but an unselected final
motor does not block the preliminary structural CAD envelope.

The Phase 5 local reference/envelope source and reuse decisions are tracked in
the [hardware model register](../docs/manufacturing/hardware-model-register.md).

## NEMA17 motor sheet

Create one copy of this table for each motor, including spares.

| Field | Motor M__ record |
| --- | --- |
| Owner hardware status | OWNER-SUPPLIED — DO NOT BUY |
| Inventory ID / photograph |  |
| Manufacturer and model |  |
| Body length and measured body envelope | Common 40-48 mm body screen; measure actual body and connector-side clearance |
| Mounting pattern | Standard NEMA17 interface, approximately 42.3 mm square nominal; measured hole/face details: |
| Rated phase current |  |
| Holding torque and source |  |
| Torque-speed curve/source |  |
| Phase resistance A-B / B-C and test current |  |
| Step angle |  |
| Shaft diameter, length, flat, and usable engagement | 5 mm is a screening expectation, not a fact |
| Connector, pinout, and wire colors |  |
| Rear connector/wiring access envelope | Record connector exit, bend radius, strain relief, and cable service path |
| Bearing play/noise |  |
| Temperature under identified driver/current |  |
| Candidate axis | X / Y / Z / spare |
| Screening result | X/Y >=0.45 N-m; Z >=0.55 N-m; torque-at-speed evidence: |
| Owner disposition |  |

Use a caliper for body/shaft dimensions, an ohmmeter for winding resistance,
the motor label/datasheet for identity, and a guarded low-speed bench test for
direction, noise, temperature, and missed-step behavior. Do not infer torque
from frame size or holding torque from a marketplace photograph. The generic
preliminary CAD interface is a common 42.3 mm NEMA17 mounting square, a
screening 5 mm shaft, and a 40-48 mm body envelope with rear connector and
wiring access. Exact pilot, shaft engagement, body length, and connector
clearance remain measured values before manufacturing release.

### Motor assignment strategy

- Assign normal suitable owner-supplied motors to X/Y after current, torque at
  operating speed, shaft, connector, and condition checks.
- Assign the strongest suitable owner-supplied motor to Z only if it remains
  electrically compatible with the identified driver and supply.
- Do not purchase new stepper motors at this stage. Exact final motor choice
  is a commissioning and manufacturing-interface decision, not a reason to
  block the generic preliminary structural CAD envelope.

## Arduino Mega + CNC Shield / GRBL controller sheet

The known controller platform is **OWNER-SUPPLIED — ARDUINO MEGA + CNC
SHIELD** and is intended for this machine. The exact CNC Shield revision and
installed stepper-driver modules remain unresolved. Do not recommend a
replacement controller unless later bench or motion validation identifies a
real limitation.

| Field | Controller record |
| --- | --- |
| Owner hardware status | OWNER-SUPPLIED — DO NOT REPLACE absent a validated limitation |
| Controller inventory ID / photographs |  |
| Shield revision and visible markings |  |
| Arduino type and board revision | Arduino Mega; exact board/revision: |
| Firmware/configuration strategy | GRBL-compatible firmware/configuration; exact fork/version/settings dump: |
| Driver carrier positions/models | X:  / Y:  / Z:  |
| A4988/DRV8825/other marking |  |
| Microstep jumper configuration | X:  / Y:  / Z:  |
| Supported microstep configuration | Per installed driver carrier and jumper state: |
| Motor supply voltage capability |  |
| Motor-current capability | Driver/current-limit evidence and measured setting: |
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
wiring. Verify supported microsteps, motor-current capability, supply-voltage
capability, cooling, limit inputs, probe input, spindle PWM/control outputs,
and the GRBL-compatible firmware/configuration strategy. A driver IC
datasheet does not establish the capability of a clone carrier, its cooling,
or its current limit.
