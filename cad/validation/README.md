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
