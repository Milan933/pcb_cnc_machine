# Phase 1 PETG manufacturing constraints

These are process assumptions and screening requirements for the Voron 2.4
350, not guaranteed printer capability. The actual usable volume, filament,
nozzle, layer height, orientation, and conditioning policy must be measured
before structural release.

## Build-volume limits

The nominal printer volume is approximately 350 x 350 x 350 mm. Until a
printer-specific calibration is recorded:

- 320 mm is the preferred maximum dimension for a one-piece structural part;
- 330 mm is a conditional screening limit requiring explicit orientation,
  bed-contact, warping, and post-processing evidence;
- a part above 330 mm requires a split-part or alternate manufacturing EDR;
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

- Heat-set inserts are for serviceable threads only where boss geometry,
  installation temperature, pull-out, torque, and surrounding walls are
  controlled by a coupon.
- Captive nuts are allowed when they improve assembly access and prevent
  thread stripping.
- Through-bolts or metal load spreaders are preferred where rail alignment,
  repeated preload, spindle mass, or PETG creep would make an insert
  unreliable.
- Through-bolt holes shall have documented edge distance, bearing area, and
  tightening access.

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
| REQ-PETG-001 | Primary parts shall be <=320 mm preferred and <=330 mm conditional in their documented print orientation. | Preliminary |
| REQ-PETG-002 | Parts above 330 mm shall require a split-part or alternate-manufacturing decision record. | Preliminary |
| REQ-PETG-003 | Every structural part shall document anisotropy, warping, bed contact, support, critical datums, and post-processing. | Known design rule |
| REQ-PETG-004 | Hole, slot, insert, and dimensional tolerances shall be calibrated on representative coupons before freezing CAD interfaces. | Known process rule |
| REQ-PETG-005 | Primary rail, bearing, screw, and spindle interfaces shall spread load and provide a measured or post-processed datum. | Preliminary |
| REQ-PETG-006 | Through-bolts, inserts, and captive nuts shall be selected from the load path and creep risk, not convenience alone. | Known design rule |
