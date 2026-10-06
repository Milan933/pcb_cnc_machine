# Manufacturing-CAD review artifacts

The Phase 5 base-pair batch is the first real printable structural output. Run
the pinned build123d environment with:

    python -m tools.generate_phase5_base_pair

The generator writes candidate files to the ignored paths
`generated/stl/phase5-base-pair/` and `generated/step/phase5-base-pair/`, and
records the source revision, dimensions, maturity, and validation results in
`phase5-base-pair-manifest.json`.

These outputs are `PROTOTYPE-STL` review artifacts. They are intentionally not
placed in a `release/` directory and are not manufacturing-ready or
hardware-validated.
