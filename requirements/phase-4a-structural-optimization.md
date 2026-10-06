# Phase 4A - structural optimization requirements

**Status:** accepted as preliminary O2 architecture; Phase 5 first base-pair
manufacturing-CAD batch authorized, with release and remaining parts closed

Phase 4A records the owner-accepted O2 architecture before hardware-specific
CAD. It does not freeze vendor hardware or mark interfaces manufacturing-ready.
The owner has separately authorized Phase 5 to establish manufacturing-CAD
conventions using only `base_left_integrated` and `base_right_integrated`.

## Baseline

The comparison starts from the reproducible Phase 4 P2 concept:

- 29 named PETG structural parts, including 16 classified as critical
  structural;
- 4,573,458.863 mm3 CAD solid-equivalent volume and 5.808293 kg at the
  centralized PETG density;
- 3.20-4.36 kg estimated installed printed PETG mass, excluding hardware,
  support, brims, and process waste;
- 0.012648 mm preliminary tool-point deflection at 5 N;
- 363 x 353 x 275 mm built reference assembly bounds;
- no unexpected CAD solid interference and 47 dependency-light tests passing;
- Historical Phase 4 recommendation: **REQUIRE PHASE4A STRUCTURAL
  OPTIMIZATION**; the owner has now accepted O2 as the preliminary baseline.

The baseline critical structural register is:

base_front_left, base_front_right, base_rear_left, base_rear_right,
base_left_side_member, base_right_side_member, base_y_rail_carrier_left,
base_y_rail_carrier_right, base_center_tie, gantry_tower_left,
gantry_tower_right, gantry_beam_left, gantry_beam_right, x_carriage_plate,
z_carriage_plate, and moving_bed_frame.

## Optimization objectives

The priority order is:

1. simplify the primary cutting-force loop;
2. reduce critical PETG part count;
3. reduce critical PETG-to-PETG joint count;
4. preserve or improve stiffness;
5. preserve alignment and measurable rail datums;
6. preserve serviceability of hardware and process interfaces;
7. preserve Voron 2.4 printability;
8. reduce unnecessary PETG mass.

Mass is a secondary objective. The model remains review geometry and does not
claim measured PETG behavior.

## Acceptance screens

At 5 N tool-point load:

- target: <= 0.020 mm;
- preferred: <= 0.015 mm;
- acceptance limit: <= 0.030 mm.

A result above 0.015 mm is allowed only with an explicit architectural
simplification and owner justification. The optimization must not be tuned
near 0.020 mm. A calculated screen is not FEA or a physical test.

For a Voron 2.4 350 mm class printer, preferred XY extent is <=300 mm and the
conservative maximum is <=320 mm. No mandatory part may exceed 320 mm without
a new owner decision and printer-specific proof.

## Controlled candidates

| Candidate | Intent | Structural change | Serviceability | Alignment risk |
| --- | --- | --- | --- | --- |
| O1 | Conservative | Consolidate only the X/Z support; retain the Phase 4 base and gantry decomposition. | Very high | Low change |
| O2 | Balanced | Integrate each base/Y/perimeter side, each tower/beam side, and the X/Z backbone while retaining replaceable hardware modules. | High | Moderate and inspectable |
| O3 | Aggressive | Integrate base/Y/tower/beam/X-bearing envelopes into two large side modules and remove feet/electronics parts. | Reduced | Highest |

O2 is the selected preliminary compromise because it reduces the load-path
seams without embedding the replaceable rail, screw, bearing, motor, spindle,
foot, or electronics hardware.

## Structural and manufacturing rules

- The fixed gantry remains a split J1 center interface; J1 remains proposed,
  not production-frozen.
- Closed sections, torsion boxes, ribs, shoulders, keys, and mating faces carry
  shear and location. Fasteners provide clamp preload.
- M3 remains the rail/accessory class, M4 the default structural/module class,
  and M5 requires a load/creep/preload justification.
- Actual rail, carriage, screw, nut, bearing, coupler, motor, spindle,
  insert, and fastener dimensions remain open until measured.
- Y rail seats remain supported datum strips requiring conditioning,
  skim/shim, parallelism measurement, and post-print inspection.
- Motors, fixed/floating bearing supports, screws/nuts, couplers, rails,
  spindle, limits, probe, wiring, feet, and spoilboard remain service targets.

## Evidence gate

The preliminary architecture is accepted, but the following evidence remains
required before manufacturing release and before the remaining O2 parts are
started: conditioned 300 mm PETG coupons, rail-seat and joint tests, actual
hardware measurements, full-travel and service mock-up, and a separated 5 N
force-loop measurement. Under EDR-014, the first base pair may be generated as
`PROTOTYPE-STL` with explicitly marked provisional hardware dimensions; it is
not `RELEASED` or `HARDWARE-VALIDATED`.
