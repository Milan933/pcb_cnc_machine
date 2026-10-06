# Parametric parts

Phase 4 now contains `phase4_structural.py`, a deterministic preliminary PETG
structural concept builder for the owner-accepted P2 baseline. It creates 29
named review parts: segmented closed base members, rail carriers, service
cartridges, feet, hollow towers, split torsion-box beam segments, X/Z
carriages, spindle mount concept, and ribbed moving bed.

These parts are PRELIMINARY review geometry, not manufacturing-ready parts.
Supplier-dependent holes, insert pilot dimensions, exact bearing pockets,
spindle bore, tolerances, and final fastener patterns remain unresolved. Each
part has a centralized bounding/orientation/process contract in
`cad/parameters.py`; mandatory XY extents must remain at or below 320 mm and
preferably at or below 300 mm.

When a part module changes, keep the builder deterministic, use centralized
parameters or a documented calculation, declare its coordinate frame, and
preserve individual temporary STEP/STL export coverage in the Phase 4 runner.
