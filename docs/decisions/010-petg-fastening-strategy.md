# Engineering decision record: PETG fastening and structural modularity

- **Record ID:** EDR-010
- **Phase:** applies to Phase 3A review packaging and later structural CAD
- **Status:** owner-directed working strategy; physical evidence required
- **Date:** 2026-10-06
- **Owner:** project owner / project team
- **Inputs:** Phase 1 PETG manufacturing requirements, Phase 2A structural
  comparison, Phase 3 motion classes, and Phase 3A packaging review

## Owner direction

Use the following principle throughout the project:

> Fasteners provide preload; printed geometry provides location and shear
> transfer. Heat-set inserts are the default reusable threaded interface in
> PETG. Through-bolts are reserved for structural joints where insert pull-out,
> creep, preload, or joint moment capacity makes them necessary.

This direction is incorporated into the central parameter model, project
skills, requirements, the Phase 3A validation layer, and the Phase 4
preliminary structural concept. It authorizes review-level structural
interfaces but not production structural CAD or manufacturing release.

## Standard hierarchy and interface rules

- M3 is the default for small covers, sensors, limits, probe hardware, cables,
  and accessories.
- M4 is the default for general structural, motor, bearing, spindle, and
  module joints.
- M5 is reserved for a documented high-load structural case. No additional
  thread sizes are introduced without a technical reason and decision record.
- The insert family interface must eventually carry OD, length, pilot range,
  insertion depth, surrounding wall, edge distance, insertion direction,
  screw clearance, and soldering-iron/tool access.
- Exact supplier-dependent dimensions are deliberately unresolved until the
  actual inserts are selected, measured, and tested on representative PETG
  coupons.
- Bosses for important joints connect into ribs or skins. A gantry crossmember
  must be seated by a deep tongue-and-groove, stepped socket, keyed pocket,
  shoulder, or interlocking rib; screws clamp the seat and the crossmember does
  not hang from M5 screws.
- Motors, rails, carriages, lead screws/nuts, bearings, spindle, limits, probe
  wiring, and moving-bed wiring remain replaceable.

Through-bolts remain valid when insert pull-out or creep, high bending moment,
high clamping force, cyclic loading, or failure consequence warrants them.
They still require geometric shear transfer and a written justification; bolt
shanks are not precision locating pins by default.

## Print-size modularity

The practical Voron 2.4 350 usable area is smaller than its nominal envelope.
Prefer structural-part XY dimensions at or below 300 x 300 mm, use 320 mm as
the conservative maximum screening dimension, and review every part at or
above 300 mm for orientation, diagonal clearance, warping, datum inspection,
insert access, and assembly access. Indexed PETG interfaces, inserts, and
selective through-bolts are the preferred modularity tools when a one-piece
print would exceed that boundary or prevent service.

## Evidence and implementation

Implemented review-level evidence:

- `cad/parameters.py` central M3/M4/M5 families and Phase 3A interface screens;
- `cad/fastening.py` hierarchy, boss, edge, access, geometric-transfer, M5,
  and through-bolt checks;
- `tests/test_fastening_strategy.py` deterministic positive and negative cases;
- project requirements and skills updated with the same contract;
- Phase 3A runner reports fastening status without turning unresolved supplier
  dimensions into a silent pass.

Required before a production interface is released:

- selected insert supplier/part and measured dimensions;
- PETG installation, pull-out, torque, cracking, creep, and repeated-assembly
  coupon results;
- joint load-path and through-bolt decisions where applicable;
- full-travel service mock-up showing replaceability of motion, spindle,
  limit, probe, and moving-bed hardware.

## Decision boundary

EDR-010 remains a working owner direction, not physical acceptance. The exact
insert family, structural split locations, and any through-bolt exceptions
remain open questions. It applies to the owner-accepted P2 baseline and the
Phase 4 preliminary concept; production interface release remains blocked.
