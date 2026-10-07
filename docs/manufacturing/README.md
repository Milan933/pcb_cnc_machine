# Manufacturing-CAD review artifacts

The active Phase 5 package is master-assembly-first. The complete CNC is
constructed from credible hardware references and local derived interface
models; the PETG parts are then derived from that assembly. The superseded
envelope-only STL set must not be printed or released.

Reusable hardware references are persistent under
[`cad/library/`](../../cad/library/), with the authoritative
[hardware-model manifest](../../cad/library/hardware-model-manifest.json).
The current package contains 14 project-generated hardware models and no
downloaded third-party CAD binaries.

Run the pinned build123d environment with:

    C:\Users\milan\pcbCNC-cad-env\Scripts\python.exe -m tools.generate_phase5_complete_machine

The generator writes 20 individual candidate STEP/STL files, a complete
master STEP and visualization STL, 16 review PNGs, scene meshes, and the
tracked [manifest](phase5-complete-machine-manifest.json). Current outputs are
under:

- `generated/stl/phase5-complete-machine/`;
- `generated/step/phase5-complete-machine/`;
- `generated/drawings/phase5-complete-machine/`.

These are `PROTOTYPE-STL` / manufacturing-CAD review artifacts. They are not
`HARDWARE-VALIDATED`, `RELEASED`, or placed in a `release/` directory. See the
[owner review](phase5-complete-machine-review.md),
[hardware register](hardware-model-register.md), and
[support audit](master-assembly-support-audit.md). Validate the library with
`python -B tools/validate_hardware_library.py`.
