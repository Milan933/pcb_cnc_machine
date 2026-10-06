# Assembly

The assembly module owns deterministic placement of part instances, hardware
envelopes, coordinate frames, and assembly-level metadata. The Phase 2
`architecture_skeleton.py` module is intentionally limited to reference
envelopes, centerlines, carriage boxes, and structural bounds. The Phase 3
`motion_skeleton.py` extension adds nominal rails, screws, nuts, bearing
supports, couplers, motors, spindle, and bed envelopes, but remains review
geometry only. Neither module is a source of production printable-part
geometry.

The Phase 3A `packaging_skeleton.py` module builds the P1/P2/P3 compact
packaging variants. It adds swept-bed, swept-spindle, motor, bearing, and
home-limit reference envelopes for clearance review, but it also remains
review geometry only and must not be exported to a manufacturing release.

The Phase 4 `phase4_assembly.py` module replaces the old structural packaging
bound with the 29-part preliminary PETG concept and retains the accepted P2
motion/process/hardware references. It also builds a separated J1/J2/J3
gantry-joint study and exports review-only assembly and individual-part files
to a temporary directory. Expected overlaps are limited to explicit structural
interfaces; unexpected independent-solid overlaps fail the runner.
