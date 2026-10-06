# Export

The Phase 2 and Phase 3 spikes export deterministic review-only skeleton STEP
and STL derivatives to an explicit temporary directory. They are not
manufacturing files and are not written to the repository's release
directories.

The Phase 4 structural runner follows the same boundary. It exports the
preliminary assembly, 29 individual structural concept parts, and the J1/J2/J3
joint study only to an explicit temporary directory. `generated/*/release/`
remains forbidden until the structural concept is accepted, hardware and
insert dimensions are measured, physical evidence passes, and a later release
decision authorizes manufacturing artifacts.

The future export layer must generate reproducible STEP and STL files from the
parametric source, write an export manifest, and refuse to publish outputs
when validation has blocking errors. It must preserve the distinction between
source geometry, development artifacts, and reviewed release artifacts.
