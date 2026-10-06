# Validation architecture

The validation package remains backend-independent for rule logic. In Phase 2
it also provides parameter checks for the architecture skeleton; the CAD
backend is isolated in `cad/assembly/architecture_skeleton.py`. It currently
provides:

- stable rule IDs for the required travel, clearance, access, structural, and
  printability checks;
- typed report and issue states;
- centralized-parameter consistency checks;
- planning-envelope checks;
- an explicit printable-part orientation contract;
- Phase 1 V-bit geometry, target, map-grid, envelope, and Z-budget
  consistency checks;
- Phase 2 travel, bed, gantry, Z-guide, overhang, and print-bound checks;
- Phase 2A analytical-input ordering, positive-value, section, mass, and
  conditional print-bound checks;
- Phase 3A swept two-carriage rail lengths, bed/motor/spindle/tool/limit
  clearance screens, compact Z-stack checks, and review-model containment;
- PETG fastening hierarchy and interface checks for M3/M4/M5 family
  completeness, preliminary boss material, edge distance, installation-tool
  access, geometric location/shear transfer, M5 justification, and selective
  through-bolt justification; unresolved supplier dimensions are explicit
  not-ready warnings;
- Phase 4 preliminary structural part-bound/orientation checks, J1/J2/J3
  joint-contract checks, rail-seat strategy checks, accepted-P2 motion-reference
  containment, expected-versus-unexpected structural overlap, preliminary
  5 N contribution screening, and explicit service/physical-evidence
  not-ready states;
- standard-library tests that run without a CAD dependency, plus a pinned
  build123d spike for exact skeleton bounds and interference evidence.

## Future CAD adapter

The next CAD-validation layer must expose named solids, transforms, swept
volumes, datum faces, rail seats, fastener locations, and feature metadata.
Rules should consume this interface instead of calling build123d or CadQuery
directly.

## Release policy

The Phase 2 skeleton checks do not validate detailed geometry because none
exists. This is a deliberate limitation. A future complete-assembly report must
identify model revision, parameter revision, CAD version, units, rule-set
version, and every not-ready rule. Export code should block release on
blocking failures or missing release evidence.

Phase 2A adds a reproducible calculation and review-skeleton runner, but its
static estimates are not measured stiffness evidence. The runner blocks on
invalid inputs or unexpected CAD overlaps; a target miss is reported as an
engineering result and is not silently converted to a pass.

Phase 3A adds P1/P2/P3 packaging calculations and temporary build123d review
exports. The packaging pass does not accept the gate, freeze exact hardware,
or authorize manufacturing-ready parts. The owner-accepted P2 baseline now
feeds Phase 4 preliminary structural review.

The Phase 3A fastening report can pass its review-level rule checks while
remaining `not-ready`: actual insert OD, length, pilot, insertion depth,
screw-clearance, and PETG coupon results are required before manufacturing
interfaces are released.

Phase 4 adds a 29-part preliminary structural concept and review assembly. Its
automated runner may pass geometry, containment, interference, and export
checks while the overall report remains `not-ready` for owner review, measured
hardware, print/joint/rail-seat coupons, service mock-up, and physical 5 N
force-loop evidence. Phase 4 acceptance and Phase 5 remain blocked.
