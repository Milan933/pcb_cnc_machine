# Validation architecture

The validation package is intentionally backend-independent at the
foundation stage. It currently provides:

- stable rule IDs for the required travel, clearance, access, structural, and
  printability checks;
- typed report and issue states;
- centralized-parameter consistency checks;
- planning-envelope checks;
- an explicit printable-part orientation contract;
- Phase 1 V-bit geometry, target, map-grid, envelope, and Z-budget
  consistency checks;
- standard-library tests that run before a CAD dependency is selected.

## Future CAD adapter

After the build123d implementation spike, add an adapter that exposes named
solids, transforms, swept volumes, datum faces, rail seats, fastener
locations, and feature metadata. Rules should consume this interface instead
of calling build123d or CadQuery directly.

## Release policy

The foundation checks do not validate detailed geometry because none exists.
This is a deliberate limitation. A future complete-assembly report must
identify model revision, parameter revision, CAD version, units, rule-set
version, and every not-ready rule. Export code should block release on
blocking failures or missing release evidence.
