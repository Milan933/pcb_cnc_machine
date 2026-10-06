# Phase 3A - compact packaging review

## Purpose and boundary

This review responds to the poor efficiency of the preliminary Phase 3
reference envelope: approximately 384.3 x 384.3 x 300.65 mm of skeleton for
only a 200 x 150 mm PCB area. It preserves the owner-directed Architecture A
and Phase 3 motion-class baseline. It creates review envelopes only; no
production PETG part or manufacturing export is produced.

The implementation is in:

- `cad/parameters.py` - centralized P1/P2/P3 inputs;
- `cad/packaging_phase3a.py` - rail, screw, bed, and Z-stack calculations;
- `cad/assembly/packaging_skeleton.py` - review-only variant geometry;
- `cad/validation/phase3a.py` - fail-closed packaging and containment checks;
- `tools/run_phase3a_packaging_study.py` - temporary STEP/STL review runner.

## What made the old envelope large

The old X maximum was set by a left-side motor/support envelope extending to
approximately -214.3 mm while the opposite fixed-gantry bound ended at
approximately +170 mm. The old Y minimum was set by the exposed front motor,
with the rear structural/reference bound at approximately +170 mm. The old Z
minimum was the underside of that Y motor at approximately -50.65 mm and its
maximum was the upper Z motor at +250 mm.

The 220 mm Y guide spacing was mistakenly easy to read as a front/rear
footprint driver. It is transverse across the moving bed. The actual Y length
comes from tool travel, the two-carriage longitudinal group, rail end margins,
fixed/floating support envelopes, and the front motor/service package.

## Packaging rules applied

1. Rail length is sized from the swept two-block group, not just tool travel.
2. The moving bed may overhang the carriage rows; it is not forced to be as
   wide as a guide-to-guide plate.
3. X/Y motors remain direct axial drives and are recessed into removable
   pockets. No belt transmission is introduced.
4. Fixed ends carry axial screw load; floating ends are radial-only. Bearing
   pockets are replaceable review envelopes, not production housings.
5. The Y bed is checked as a full-travel union envelope. The front motor has a
   declared vertical gap below the bed underside.
6. Spindle and tool envelopes are swept/contained at the review level, and
   home-limit boxes have explicit service-clearance references.
7. Structural bounds remain printable envelopes and must not be mistaken for
   walls, ribs, insert bosses, rail seats, or fastener details.

## Variant comparison

| Variant | Body envelope | Service footprint | Bed support | Tool travel | Rails X/Y/Z | Screws X/Y/Z | Assessment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 conservative | 394 x 385 x 296 | 474 x 465 x 344 | 240 x 190 | 220 x 170 x 40 | 370 / 340 / 145 | 390 / 360 / 160 | Most serviceable; only modest footprint gain |
| P2 balanced | 364 x 356 x 276 | 444 x 428 x 322 | 230 x 180 | 220 x 170 x 40 | 340 / 310 / 130 | 360 / 330 / 145 | Recommended compact baseline |
| P3 aggressive | 344 x 334 x 268 | 414 x 404 x 318 | 220 x 170 | 210 x 160 x 40 | 320 / 280 / 125 | 340 / 300 / 140 | Smallest practical screen; conditional |

P2 reduces the old skeleton's X/Y/Z dimensions by approximately 20.3, 28.3,
and 24.65 mm respectively while keeping the full Phase 3 XY travel. P3 is
smaller, but gives up 10 mm of X and Y screened travel, has no transverse bed
overhang beyond the 220 mm guide spacing, and leaves only 2 mm per-end body
clearance for the swept bed.

## Recommended packaging

Carry P2 forward as the packaging review baseline, not as a Phase 3 gate
acceptance. It keeps the 200 x 150 mm PCB area, 220 x 170 x 40 mm screened
tool travel, 230 x 180 mm bed, 15 mm PCB perimeter, 5 mm bed overhang beyond
the guide spacing, and enough longitudinal bed overhang for support. Its
364 x 356 x 276 mm body is materially smaller than the old 400 x 400 x 310 mm
machine envelope while preserving a removable cover concept for every motor
and fixed/floating bearing end.

P1 remains the fallback if P2 access or PETG coupon evidence fails. P3 remains
a comparison only until the owner explicitly accepts its smaller XY margin,
tight end clearances, and constrained front-panel service.

## Bearing and motor packaging study

P1 keeps BK08/BF08-class external screening envelopes. P2 changes only the
packaging concept: standardized 8 mm bearing cartridges sit in replaceable
printed pockets, with a paired axial/angular-contact concept at the fixed end
and a single radial bearing with axial float at the far end. P3 tightens the
same interfaces further. None of these is a production housing.

NEMA17s remain direct axial. P2 places X in a removable side pocket, Y in a
front cross-member pocket, and Z in a removable upper pocket. Recessing is
allowed only if the shaft remains coaxial, the motor can be removed without
disassembling the gantry, heat can escape, coupler set screws are reachable,
and homing/limit wiring is protected.

## PETG and print-volume implications

The intended additive packaging is a structural monocoque/bound with bearing
pockets, motor recesses, embedded-nut access, rail-seat ribs, and removable
hardware covers. The current skeleton does not model those details. The
largest future packaging print screens are P1 340 x 80 x 170 mm, P2 330 x 72 x
155 mm, and P3 320 x 68 x 145 mm, all within the nominal 350 mm printer volume
on paper. A one-piece or near-one-piece fixed-gantry torsion box is the target;
split side interfaces remain the fallback until orientation, diagonal, insert,
and rail-seat coupon evidence exists.

## Gate recommendation

Do not accept the Phase 3A gate yet. The owner should select P1/P2/P3 after a
full-travel assembly mock-up and service-access review. The CAD and dependency-
light checks pass, but exact motors, spindle, switches, bearing fits, screw
straightness, PETG creep/rail-seat behavior, and workholding remain unverified.
Phase 4 remains explicitly blocked.
