# Phase 3A PETG fastening and structural modularity strategy

**Status:** owner-directed strategy applied to review interfaces; physical
insert, coupon, and joint evidence remain open. This document does not accept
production CAD, or authorize manufacturing release. It is the working
fastening strategy for the owner-accepted P2 baseline and Phase 4 preliminary
structural concept.

## Core principle

> Fasteners provide preload; printed geometry provides location and shear
> transfer. Heat-set inserts are the default reusable threaded interface in
> PETG. Through-bolts are reserved for structural joints where insert pull-out,
> creep, preload, or joint moment capacity makes them necessary.

The screw is a clamp. A shoulder, step, tongue-and-groove, keyed pocket,
registration feature, shear key, substantial boss, mating planar surface, or
interlocking rib carries location and shear. Important bosses connect into
ribs or skins instead of loading an isolated PETG wall.

## Standard hierarchy

| Size | Default use | Boundary |
| --- | --- | --- |
| M3 | Small covers, sensors, limit switches, probe hardware, cables, and accessories | Do not use for a joint whose boss or preload screen is inadequate. |
| M4 | General structural, motor, bearing, spindle, and module joints | Default structural insert size. |
| M5 | High-load structural joint only | Requires a recorded load-path/capacity justification; not the gantry default. |

No fourth thread size is permitted without an engineering reason and an
updated decision record. The Phase 3A central parameter model contains only
M3/M4/M5.

## Insert interface contract

Each reusable insert family and part interface must eventually declare:

- nominal thread size;
- insert outer diameter and length;
- pilot-hole range and insertion depth;
- minimum surrounding boss wall and edge distance;
- insertion direction and layer/load orientation;
- screw-clearance envelope;
- soldering-iron or insertion-tool access envelope;
- installation temperature, pull-out, torque, cracking, creep, and repeated-
  assembly evidence;
- service/replacement path and the geometric feature carrying location/shear.

The current Phase 3A model carries the contract and preliminary boss,
edge-distance, and tool-access screens. Supplier-dependent OD, length, pilot,
insertion-depth, and screw-clearance values are intentionally `None` until the
actual insert is selected, measured, and tested. A review screen must not be
used to freeze a manufacturing pocket.

## Joint rules applied to Phase 3A

- The gantry crossmember is conceptually seated in a deep tongue-and-groove,
  stepped socket, keyed pocket, shoulder, or interlocking rib. Fasteners clamp
  that seat; the crossmember must not hang from M5 screws.
- Motor pockets, bearing supports, rail seats, spindle mounts, covers, limits,
  probe mounts, and module interfaces use heat-set inserts by default and
  retain removable service access.
- Rail and bearing interfaces use a continuous supported datum and geometric
  seating. The fasteners are not precision locating pins by default.
- Through-bolts are a selective escalation for insert pull-out or creep, high
  moment/preload, cyclic loading, or high failure consequence. A through-bolt
  still requires a geometric shear path and a written justification.
- Motors, rails, carriages, lead screws/nuts, bearings, spindle, limits,
  probe wiring, and moving-bed wiring remain replaceable.

## Print-size and modularity boundary

The practical Voron 2.4 350 usable area is smaller than its nominal 350 mm
envelope. Prefer structural-part XY dimensions at or below 300 x 300 mm; use
320 mm as the conservative maximum. Parts at or above 300 mm require explicit
orientation, diagonal, bed-contact, warping, datum, insert-access, and
assembly review. Indexed PETG interfaces, inserts, and selective through-bolts
are preferred where splitting a part improves fit, serviceability, or
printability without weakening the load path.

## Automated checks and evidence boundary

`cad/fastening.py` and `tests/test_fastening_strategy.py` provide the first
dependency-light checks:

- exact M3/M4/M5 hierarchy and intended-use mapping;
- family completeness and explicit unresolved supplier dimensions;
- positive boss material, edge distance, and insertion-tool access;
- a non-empty geometric load-transfer feature;
- M5 size justification;
- through-bolt justification and geometry.

The report status remains `not-ready` until actual insert dimensions and
representative PETG coupon results exist, even when review-level geometric
rules pass. The Phase 3A packaging runner reports this status alongside its
review-only STEP/STL containment results. Phase 4 preliminary structural
concept work is authorized, but production interfaces remain blocked.
