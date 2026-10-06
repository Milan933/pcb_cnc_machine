# Phase 5 complete-machine coordinate system

Status: controlled virtual-CAD convention; physical datums remain to be
measured.

All coordinates are millimetres. The machine is a fixed gantry with a moving
Y bed.

| Axis / datum | Definition |
| --- | --- |
| X | Left to right when facing the machine; positive to the right. |
| Y | Front to rear; positive toward the rear. |
| Z | Up from the nominal PCB top surface; positive upward. |
| MCS origin | Centre of the nominal PCB top surface `(0, 0, 0)`. |
| Work origin | G54/front-left PCB datum `(-100, -75, 0)`; probing may refine Z. |
| PCB envelope | X `-100..100`, Y `-75..75`, nominal Z `0..1.6`. |
| Work area | 200 x 150 mm. |
| Tool-point travel | X 220 mm, Y 170 mm, Z 40 mm. |
| Tool-point screening limits | X `-110..110`, Y `-85..85`, Z `-25..15`. |

The travel limits are tool-point screening coordinates, not measured machine
limits. The complete CAD assembly uses the nominal tool-point at Z = -5 mm
and applies the Z travel as a displacement around that state when checking
the eight travel corners.

## Assembly placement references

The fixed base pair is placed at X = -174 and +24 mm, Y = -150 mm, Z = -56
mm. The integrated gantry sides are placed around Y = -100 mm and begin at
the base datum. The X/Z backbone is nominally `(-45, -105, 8)`. The moving
bed frame is nominally `(-120, -90, -32)` and the replaceable 230 x 180 x 12
mm spoilboard is at `(-115, -90, -12)`.

These placements are assembly references, not instructions to skip leveling,
shimming, or datum inspection. Printed rail seats are not precision datums
until they are conditioned and measured.

## Datum hierarchy

1. Use a stable table/support surface to establish the four feet.
2. Level and square the two base modules before tightening the center tie.
3. Use the printed rail shoulders only as alignment references; shim or skim
   the rail seats after PETG conditioning.
4. Set one Y rail as the master, then indicate the second rail parallel to it.
5. Square the two gantry towers to the Y rails before clamping the beam joint.
6. Set the lower X rail first, then establish the 60 mm rail-center spacing.
7. Match the dual Z rails to the measured MGN9 carriage spacing.
8. Level the moving bed to the X/Y datum, then skim or shim the spoilboard.
9. Tram the spindle mount to the spoilboard with a test bar before cutting.

The exact rail holes, bearing seats, insert pilots, spindle bore, and
controller openings remain `PROVISIONAL_HARDWARE_DIMENSION` until the owner
identifies and measures representative hardware.
