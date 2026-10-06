# Agent instructions for PCB CNC

## Current boundary

The repository has completed Phase 2 architecture review. EDR-005 is accepted
by the project owner, and EDR-006/EDR-007 record the owner-accepted **A:
fixed gantry with moving Y bed** baseline. B, moving gantry/fixed bed, remains
the documented primary rejected alternative and must not be physically built
unless the owner reopens the architecture.

The owner accepted the Phase 3 motion baseline and the P2 Phase 3A packaging
baseline on 2026-10-06. Phase 4 preliminary structural CAD is now authorized
under proposed EDR-011. Work may create parametric PETG structural concept
parts, a complete review assembly, joint and rail-seat studies, preliminary
calculations, print planning, and a split preliminary BOM. It must not silently
turn a preliminary or calculated value into a measured engineering fact.

The Phase 4 boundary does not authorize manufacturing-ready CAD, production
STL/STEP/drawing generation, final insert pilot dimensions, final vendor
dimensions, or Phase 5. Review-only CAD exports must remain temporary. PETG
coupons, joint/rail-seat/bearing-pocket tests, actual hardware measurements,
service mock-ups, and representative force-loop evidence remain required.

## Canonical public repository

This is an intentionally public repository. The canonical remote is:

    https://github.com/Milan933/pcb_cnc_machine.git

The local working repository is D:\pcbCNC. For any Git, commit, branch,
publication, or release task, read
[.agents/skills/repository-workflow/SKILL.md](.agents/skills/repository-workflow/SKILL.md).
Verify the configured remote before pushing. Do not force-push, rewrite
published history, delete remote branches or tags, or publish secrets.

The public repository may contain reviewed source, documentation, requirements,
decision records, validation, tests, BOM data, and explicitly approved
manufacturing artifacts. It must not contain credentials, private keys,
machine-specific secrets, local caches, virtual environments, or unrelated
personal files. Use the repository audit before a commit intended for push.

## Source of truth

Use the following order when resolving project intent:

1. explicit user requirements in requirements/requirements.md;
2. the quantitative Phase 1 requirements in requirements/phase-1-*.md;
3. approved engineering decision records in docs/decisions;
4. centralized values in cad/parameters.py;
5. the project skills in .agents/skills;
6. implementation details in part and assembly modules.

If two sources disagree, stop and record the conflict in a decision record.
Never repair a contradiction by changing a lower-level file silently.

## Engineering rules

- This is a PCB-specific machine. Optimize for tool-point stiffness, runout,
  repeatability, probing, and controlled shallow cuts rather than metal-cutting
  force or material-removal rate.
- The structural frame is predominantly printed PETG. Do not replace it with
  aluminum extrusion or plate by default. If a metal component is proposed,
  document the mechanical reason and its load path.
- Prefer monocoques, box sections, ribs, gussets, triangulation, distributed
  interfaces, and short force loops over simply increasing infill.
- Treat PETG creep, anisotropy, print orientation, fastener bearing, and
  long-term preload loss as design inputs.
- Use heat-set inserts as the default reusable PETG threaded interface. The
  governing joint rule is that fasteners provide preload while printed
  geometry provides location and shear transfer. Standardize M3 for small or
  accessory hardware, M4 for general structural/module joints, and M5 only
  with a documented technical justification. Through-bolts remain selective,
  require geometric shear transfer and a written reason, and are not precision
  locating pins by default.
- Keep insert OD, length, pilot range, insertion depth, boss wall, edge
  distance, direction, screw clearance, and soldering-iron/tool access in the
  central interface contract. Do not freeze pilot dimensions until actual
  inserts are selected, measured, and coupon-tested.
- Prefer structural-part XY dimensions at or below 300 mm and use 320 mm as a
  conservative maximum; parts at or above 300 mm require explicit printability
  and modularity review. Keep motors, rails, carriages, screws/nuts, bearings,
  spindle, limits, probe wiring, and moving-bed wiring replaceable.
- All dimensions belong in the centralized parameter model or in a documented
  calculation. Do not scatter unexplained literals through CAD code.
- The authoritative model is parametric. Meshes are manufacturing derivatives,
  never the source of truth.
- A printable part must have a documented realistic print orientation within
  the usable Voron 2.4 350 build volume. A bounding-box-only check is
  insufficient.
- Every major phase requires an engineering decision record covering the
  decision, alternatives, reasoning, risks, and unresolved questions.
- Validation should fail closed when required evidence is absent.
- The Phase 2 skeleton may contain only axis centerlines, envelopes,
  carriage boxes, screw references, and structural bounding volumes. The Phase
  3 extension may add nominal rails, carriages, screws, nuts, bearing-support,
  coupler, motor, spindle, and bed envelopes, but it remains a review-only
  reference model and is not a manufacturing model.
- Phase 4 structural parts remain PRELIMINARY concepts. Every mandatory PETG
  part must stay at or below 320 mm in both build-plate axes, preferably at or
  below 300 mm, and must document orientation, support, brim/warping, and
  layer/load concerns. Geometry provides location and shear; fasteners provide
  preload.

## Coordinate convention

The project convention is:

- X: left to right, positive to the right when facing the machine;
- Y: front to back, positive toward the rear of the machine;
- Z: down to up, positive upward from the workholding reference plane.

The physical location of the machine origin and the final bed datum remain
controlled design decisions. Part code must not invent an origin placement.

## Working style

Before changing geometry or selecting hardware:

1. identify whether a value is known, assumed, preliminary, calculated, or
   verified;
2. update the relevant requirement or decision record;
3. use the relevant project skill;
4. run the applicable validation and tests;
5. summarize new risks and unresolved decisions.

Keep generated artifacts out of source control unless they are explicitly
reviewed manufacturing deliverables. Prefer small, inspectable modules over
large scripts with hidden placement or export behavior.

- Source-of-truth parametric CAD is normally tracked. Temporary exports remain
  ignored. Reviewed release exports may be committed only under the designated
  generated/*/release/ directories after validation and review.
- A fresh clone must eventually be able to install dependencies, run
  validation, generate the assembly, export STEP/STL, and run tests without
  undocumented files outside the repository.
