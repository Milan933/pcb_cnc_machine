# Export

The Phase 2 and Phase 3 spikes export deterministic review-only skeleton STEP
and STL derivatives to an explicit temporary directory. They are not
manufacturing files and are not written to the repository's release
directories.

The future export layer must generate reproducible STEP and STL files from the
parametric source, write an export manifest, and refuse to publish outputs
when validation has blocking errors. It must preserve the distinction between
source geometry, development artifacts, and reviewed release artifacts.
