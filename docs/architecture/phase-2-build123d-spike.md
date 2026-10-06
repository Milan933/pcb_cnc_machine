# Phase 2 build123d implementation spike

**Status:** passed as an architecture review spike; production CAD not
approved
**Tested runtime:** CPython 3.10.11, Windows 64-bit
**Tested package:** build123d 0.12.0, pinned in
`requirements/cad-phase-2.txt`
**Units:** millimetres

## Scope

The spike exercises the CAD conventions and validation boundary with a
deterministic architecture skeleton. It builds candidates A, B, and C from
`PHASE2_SKELETON_PARAMETERS`, places named components in the project
coordinate convention, reports a compound bounding box, exports review-only
STEP and STL derivatives, and performs exact-solid intersection checks.

The skeleton contains only:

- working and tool-travel envelopes;
- bed and base bounding volumes;
- gantry structural bounding volumes;
- rail and screw centerline reference tubes;
- carriage boxes and a maximum spindle/tool envelope.

It contains no detailed printable walls, ribs, holes, fasteners, cosmetic
geometry, or manufacturing release geometry.

## Reproducible command

Create the isolated environment outside the clone, install the pinned
dependency, and run the spike with a temporary output directory:

```text
python -m venv <temp>\pcbCNC-phase2-build123d-venv
<temp>\pcbCNC-phase2-build123d-venv\Scripts\python.exe -m pip install -r requirements\cad-phase-2.txt
<temp>\pcbCNC-phase2-build123d-venv\Scripts\python.exe -m tools.run_phase2_cad_spike --output-dir <temp>\pcbCNC-phase2-spike-output
```

The output directory is deliberately outside `generated/*/release/` and the
resulting STEP/STL files are review derivatives only. They are not
manufacturing exports and are not committed.

## Observed result

The spike passed for all candidates:

| Candidate | Components | Bounding box min | Bounding box max | Size | STEP/STL | Unexpected overlaps |
| --- | ---: | --- | --- | --- | --- | ---: |
| A | 19 | (-170, -145, -40) | (170, 145, 180) | 340 x 290 x 220 | non-empty | 0 |
| B | 19 | (-170, -145, -40) | (170, 145, 180) | 340 x 290 x 220 | non-empty | 0 |
| C | 20 | (-170, -145, -40) | (170, 145, 180) | 340 x 290 x 220 | non-empty | 0 |

The six reported overlaps per candidate are documented interface contacts:
base-to-bed, base-to-each-gantry-side interface, carriage-to-spindle,
carriage-to-gantry, and spindle-to-gantry. Process-envelope and centerline
references are excluded from the solid-overlap scan because they are not
solids intended to define clearance. Any other exact-solid overlap fails the
spike command.

The build123d implementation therefore met the architecture-stage needs for
deterministic geometry, placement, STEP export, STL review export, bounding
queries, and an explicit interference policy. A CadQuery comparison was not
required because build123d did not expose a blocking issue. CadQuery remains
the documented fallback if a later detailed-assembly or export requirement
breaks this interface.

The API behavior used by the spike is documented by the official
[build123d import/export guide](https://build123d.readthedocs.io/en/stable/import_export.html)
and [assembly guide](https://build123d.readthedocs.io/en/latest/assemblies.html).

## Phase 2A optimized review spike

The focused follow-up uses the same pinned build123d runtime and the same
screening envelope, but builds only A and B with
`structural_variant="phase2a"`. It remains an architecture-only bound: the A
integrated U/monocoque and B deep ribbed beam are review volumes, not
printable parts. Run:

```text
<temp>\pcbCNC-phase2-build123d-venv\Scripts\python.exe -m tools.run_phase2a_study --output-dir <temp>\pcbCNC-phase2a-study-output
```

The observed Phase 2A result is A: 18 components, 340 x 290 x 220 mm, and B:
19 components, 340 x 290 x 220 mm. Both produce non-empty STEP/STL review
derivatives and zero unexpected solid overlaps. Outputs remain outside Git.
