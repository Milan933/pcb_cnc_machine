# Controller, spindle, limit, probe, and cable integration

Status: owner-hardware integration architecture; exact shield revision and
driver pinout are intentionally unresolved.

The complete master includes an Arduino Mega board envelope, a provisional CNC
Shield/driver stack, a driver-cooling clearance volume, a controller service
loop, and cable-management volumes. These are review geometry from the
[hardware model register](../manufacturing/hardware-model-register.md), not a
frozen enclosure or pin map.

## Known controller boundary

The intended controller is the owner-supplied **Arduino Mega + CNC Shield**.
It is not an unknown generic platform and it is not to be replaced unless
later technical validation identifies a real limitation. The exact CNC Shield
revision and installed stepper-driver modules must be read from the physical
board before wiring is frozen.

The complete CAD includes generic board, shield, driver-clearance, connector,
and service-loop envelopes only. It does not invent a pin map from a similar
looking shield.

## Signal architecture

| Function | Physical destination | Current design state | Required identification/evidence |
| --- | --- | --- | --- |
| X step/dir/enable | X driver module | provisional | shield revision, driver module, GRBL Mega pin map |
| Y step/dir/enable | Y driver module | provisional | same; verify current and cooling |
| Z step/dir/enable | Z driver module | provisional | select strongest electrically compatible owner motor after characterization |
| X/Y/Z home limits | shield limit inputs | provisional | identify input labels, pull-ups, common ground, switch polarity, cable shielding |
| conductive probe | probe input or documented spare input | provisional | verify actual shield input and GRBL configuration |
| spindle PWM/control | shield spindle output or documented external interface | provisional | verify output voltage/current, PWM frequency, ground, and spindle controller input |
| spindle power | separate power path | provisional | identify spindle supply, fuse, switch, emergency stop, and protective earth practice |
| motor power | driver VMOT supply | provisional | verify shield and driver voltage/current/cooling ratings |
| logic power | Mega/shield logic supply | provisional | verify common ground and USB/power isolation strategy |

## Wiring rules

1. Photograph and label the installed shield and driver modules before
   removing any wire. Record board revision markings and every jumper or
   microstep configuration.
2. Identify each motor coil pair with an ohmmeter. Record motor label, body
   length, shaft dimensions, rated current if known, resistance, connector
   pinout, and mechanical condition.
3. Use separate routed bundles for motor power, spindle power/PWM, switches,
   probe, and USB/logic where practical. Provide strain relief at every moving
   loop.
4. Keep the probe reference and shield/controller ground strategy explicit;
   do not rely on the printed frame as an electrical return.
5. Set driver current from the identified module and measured motor data. Do
   not infer current capability from a generic A4988/DRV8825 photograph.
6. Verify cooling clearance around driver modules. The CAD clearance block is
   a placeholder until the installed modules and heatsinks are measured.
7. Configure GRBL-compatible firmware only after the Mega pin mapping,
   microstep jumpers, limit polarity, probe input, and spindle output are
   identified. Record the actual configuration file and firmware revision.
8. Test emergency stop and spindle inhibit independently of motion commands.
9. With spindle power disconnected, test direction, limit actuation, homing,
   probe continuity, and current settings at low speed.

No exact pin assignment, driver rating, microstep setting, spindle PWM pin,
or firmware configuration is released by this document. Those are
commissioning records tied to the owner’s measured controller hardware.
