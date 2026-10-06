# Export

The Phase 2 and Phase 3 spikes export deterministic review-only skeleton STEP
and STL derivatives to an explicit temporary directory. They are not
manufacturing files and are not written to the repository's release
directories.

The Phase 4 structural runner follows the same boundary. It exports the
preliminary assembly, 29 individual structural concept parts, and the J1/J2/J3
joint study only to an explicit temporary directory. The Phase 5 base-pair
runner additionally creates real fused `base_left_integrated` and
`base_right_integrated` STEP/STL candidates under ignored
`generated/step/phase5-base-pair/` and `generated/stl/phase5-base-pair/`.
Those candidates are `PROTOTYPE-STL`; `generated/*/release/` remains forbidden
until physical evidence, measured interfaces, and a later release decision
authorize manufacturing artifacts.

The Phase 5 export layer generates reproducible STEP and STL files from the
parametric source, writes `docs/manufacturing/phase5-base-pair-manifest.json`,
and refuses to complete when candidate geometry or export validation has
blocking errors. It preserves the distinction between source geometry,
development artifacts, candidate review artifacts, and reviewed release
artifacts.
