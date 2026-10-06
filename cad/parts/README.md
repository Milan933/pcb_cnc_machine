# Parametric parts

Phase 4 now contains `phase4_structural.py`, a deterministic preliminary PETG
structural concept builder for the owner-accepted P2 baseline. It creates 29
named review parts: segmented closed base members, rail carriers, service
cartridges, feet, hollow towers, split torsion-box beam segments, X/Z
carriages, spindle mount concept, and ribbed moving bed.

These Phase 4/4A parts are PRELIMINARY review geometry, not manufacturing-
ready parts. Supplier-dependent holes, insert pilot dimensions, exact bearing
pockets, spindle bore, tolerances, and final fastener patterns remain
unresolved. The separate `phase5_structural.py` module contains the historical
first two fused base candidates. The active `phase5_complete_structural.py`
module contains all 19 actual local fused structural candidates. Their rail,
screw, bearing, insert, spindle, and controller-dependent interfaces are
explicitly `PROVISIONAL_HARDWARE_DIMENSION` and their maturity is
`PROTOTYPE-STL`.

When a part module changes, keep the builder deterministic, use centralized
parameters or a documented calculation, declare its coordinate frame, and
preserve individual temporary STEP/STL export coverage. Complete-machine
assembly placement remains owned by `cad/assembly/phase5_complete_assembly.py`;
do not bake world placement into local printable parts.
