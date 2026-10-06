# Phase 1 PETG manufacturing constraints

These are process assumptions and screening requirements for the Voron 2.4
350, not guaranteed printer capability. The actual usable volume, filament,
nozzle, layer height, orientation, and conditioning policy must be measured
before structural release.

## Build-volume limits

The nominal printer volume is approximately 350 x 350 x 350 mm, but the
practical usable area is smaller. Until a printer-specific calibration is
recorded:

- 300 mm is the preferred maximum XY dimension for a structural part;
- 320 mm is the conservative maximum screening dimension;
- any part at or above 300 mm requires explicit orientation, diagonal,
  bed-contact, warping, datum, insert-access, and post-processing review;
- a part above 320 mm requires a split-part or alternate manufacturing EDR;
- a 15 mm nominal margin per side from the 350 mm envelope is a planning
  assumption, not a verified usable margin.

The print-volume validator must use documented orientation candidates, not an
unrotated bounding box alone.

## Orientation and anisotropy

Every primary structural part shall record:

- layer direction relative to the dominant load;
- bed-contact and first-layer strategy;
- support and overhang plan;
- critical datum faces;
- insert and through-hole orientation;
- warp/shrink risk over the largest span;
- post-print conditioning and inspection.

Orient load paths so primary tension, peel, and shear do not depend on weak
inter-layer adhesion when an alternative orientation or closed geometry can
carry the load more directly. Do not use an arbitrary infill percentage as a
stiffness requirement.

## Dimensional and hole-tolerance starting assumptions

These values are calibration-coupon starting points only:

- as-printed dimensional variation: target <=0.20 mm over a 100 mm feature;
- as-printed dimensional variation: target <=0.50 mm over a 300 mm feature;
- critical rail seats, bearing bores, datum faces, and insert pockets shall
  not be treated as precise solely because CAD dimensions have decimals;
- print a hole/slot coupon with nominal, -0.10, +0.10, and +0.20 mm offsets
  before freezing clearance-hole parameters;
- measure each insert pocket and fastener interface on the actual print
  process.

These assumptions must be replaced by measured printer/process data before
they become design acceptance limits.

## Joints and fasteners

Use distributed load paths. A rail, spindle mount, screw support, or gantry
joint shall not transfer a major moment through an isolated PETG boss.

The project rule is: **fasteners provide preload; printed geometry provides
location and shear transfer. Heat-set inserts are the default reusable
threaded interface in PETG. Through-bolts are reserved for structural joints
where insert pull-out, creep, preload, or joint moment capacity makes them
necessary.**

- Use M3 for small covers, sensors, limits, probe hardware, and accessories;
  M4 for general structural, motor, bearing, spindle, and module joints; and
  M5 only with an explicit high-load justification. Do not add thread sizes
  without a technical reason.
- Use shoulders, steps, tongues/grooves, keys, bosses, pockets, registration,
  shear keys, mating faces, or interlocking ribs for location and shear. Join
  important bosses into ribs or skins.
- A gantry crossmember shall seat in a deep tongue-and-groove, stepped socket,
  keyed pocket, shoulder, or interlocking rib. Screws clamp the seated joint;
  the crossmember must not hang from M5 screws.
- Through-bolts remain selective. They require geometric shear transfer and a
  documented pull-out, creep, preload, moment, cyclic-load, or failure-
  consequence reason; bolt shanks are not precision locating pins by default.
- Insert interface parameters shall eventually record OD, length, pilot range,
  insertion depth, wall, edge distance, insertion direction, screw clearance,
  and soldering-iron/tool access. Exact pilot dimensions remain unresolved
  until the actual inserts are selected, measured, and coupon-tested.
- Captive nuts are allowed when they improve assembly access and prevent
  thread stripping, but they do not replace geometric load transfer.

## Rail and bearing mounting

An as-printed PETG surface is not accepted as a precision linear-rail datum
without measurement. Phase 2/6 shall evaluate:

- a continuous supported rail seat;
- a printed datum shoulder or a post-machined/shimmed metal interface;
- fastener access and tightening order;
- replacement and alignment procedure;
- bearing/rail load spreading into ribs, skins, or a metal interface;
- clearance for lubrication, carriage travel, and cleaning.

Possible post-processing includes scraping, sanding only where it does not
destroy a datum, drilling/reaming, machining a replaceable insert, and
shimming. The selected operation and inspection method must be recorded.

## Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-PETG-001 | Structural parts should be <=300 mm preferred in XY and shall use <=320 mm as the conservative maximum screening dimension. | Preliminary owner direction |
| REQ-PETG-002 | Parts at or above 300 mm require explicit printability/access review; parts above 320 mm require a split-part or alternate-manufacturing decision record. | Preliminary owner direction |
| REQ-PETG-003 | Every structural part shall document anisotropy, warping, bed contact, support, critical datums, and post-processing. | Known design rule |
| REQ-PETG-004 | Hole, slot, insert, and dimensional tolerances shall be calibrated on representative coupons before freezing CAD interfaces. | Known process rule |
| REQ-PETG-005 | Primary rail, bearing, screw, and spindle interfaces shall spread load and provide a measured or post-processed datum. | Preliminary |
| REQ-PETG-006 | Heat-set inserts shall be the default reusable PETG thread using the M3/M4/M5 hierarchy; through-bolts require a documented structural justification and geometric shear transfer. | Known owner direction |
| REQ-PETG-007 | Every reusable insert interface shall declare boss material, edge distance, insertion direction, screw clearance, and soldering-iron/tool access; exact pilot dimensions remain not-ready until measured inserts and coupons exist. | Preliminary owner direction |
| REQ-PETG-008 | Structural modularity shall prefer indexed PETG interfaces and serviceable joints, with motors, rails, carriages, screws/nuts, bearings, spindle, limits, probe wiring, and moving-bed wiring replaceable. | Preliminary owner direction |
