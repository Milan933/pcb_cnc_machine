# Manufacturing-CAD review artifacts

The Phase 5 base-pair batch is retained as the historical first real printable
structural output. The active complete-machine pass is the real printable
19-part structural output. Run the pinned build123d environment with:

    python -m tools.generate_phase5_complete_machine

The generator writes candidate files to the ignored paths
`generated/stl/phase5-base-pair/` and `generated/step/phase5-base-pair/`, and
records the source revision, dimensions, maturity, and validation results in
`phase5-complete-machine-manifest.json`.

The generator writes individual candidates to the ignored paths
`generated/stl/phase5-complete-machine/` and
`generated/step/phase5-complete-machine/`, plus local review images under
`generated/drawings/phase5-complete-machine/`.

These outputs are `PROTOTYPE-STL` review artifacts. They are intentionally not
placed in a `release/` directory and are not manufacturing-ready or
hardware-validated. The tracked owner package is
[phase5-complete-machine-review.md](phase5-complete-machine-review.md).
