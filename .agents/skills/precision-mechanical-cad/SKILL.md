---
name: precision-mechanical-cad
description: Create and review general-purpose precision mechanical CAD for manufacturable parts and assemblies using datums, interfaces, tolerances, fits, GD&T reasoning, load paths, kinematics, inspection, and process-aware validation.
---

# Precision mechanical CAD

Use this skill for arbitrary mechanically functional, dimensionally controlled 3D models: machined parts, printed parts, brackets, fixtures, housings, bearing blocks, shafts, couplings, structures, robots, mechanisms, tooling, enclosures, and assemblies.

This is not a PCB-CNC skill. It contains no product-specific dimensions or architecture. Add a project overlay only after the general mechanical definition is sound.

The objective is precision mechanical engineering CAD, not a visually plausible shape. A valid solid or attractive render is only one piece of evidence.

## Operating contract

Before creating geometry, establish:

- function, user and environment;
- measurable requirements and acceptance evidence;
- manufacturing process and inspection method;
- global and local coordinate systems;
- primary/secondary/tertiary datums where appropriate;
- critical interfaces, motion, loads, and service actions;
- dimensional sources, confidence, tolerances, fits, and unresolved unknowns.

Never infer a precision-critical dimension from visual appearance. Use this source priority:

1. measured hardware;
2. official manufacturer drawing or CAD;
3. applicable standard;
4. manufacturer engineering guidance;
5. reputable engineering reference;
6. explicitly marked reference or provisional assumption.

Use confidence states such as `MEASURED`, `MANUFACTURER-SPECIFIED`, `STANDARD`, `REFERENCE`, `ASSUMED`, `PROVISIONAL`, and `TO-BE-MEASURED`. If an unknown affects fit, motion, load, or datum transfer, parameterize it and block the appropriate maturity gate.

## Default reasoning chain

```text
FUNCTION → REQUIREMENTS → COORDINATE SYSTEM → DATUM STRUCTURE
→ CRITICAL INTERFACES → MOTION / DOF → LOAD PATHS → PRIMARY GEOMETRY
→ FUNCTIONAL FEATURES → MANUFACTURING STRATEGY → TOLERANCES / FITS
→ ASSEMBLY → VALIDATION → DRAWINGS / EXPORTS
```

Do not begin with arbitrary boxes, holes, or offsets. Every important feature must have a mechanical, manufacturing, inspection, safety, or service reason.

## Datum-first and interface-first modeling

Define a global frame and meaningful local frames before placing precision features. Identify the primary datum, secondary datum, tertiary datum when needed, important axes, center planes, mating faces, and inspection/reference planes. Use functional relationships rather than chains of unexplained offsets.

For every interface, record:

- mating geometry and critical dimensions;
- datum relationship and alignment requirement;
- allowable clearance, interference, or adjustment;
- load transfer and reaction surfaces;
- tolerance and fit class;
- assembly method, fastener/retention method, and removal method;
- inspection method and evidence status.

Typical interfaces include shaft/bearing, bearing/housing, motor/mount, rail/beam, carriage/moving body, screw/nut, bolt/hole, insert/boss, cover/housing, and enclosure/electronics. Build parts around these interfaces, not around cosmetic proportions.

## Dimensions, tolerances, fits, and stacks

Separate nominal size from allowable variation. Apply precision only where function requires it, and select tolerances from the process, material, temperature, mating part, assembly method, and inspection capability. Do not assign tight tolerances that the process or inspection cannot support.

Choose deliberately among clearance, transition, interference, sliding, bearing, shaft/hole, machined, and printed fits. Use an applicable ISO fit system or manufacturer recommendation when appropriate; do not reuse one clearance for every process.

For every critical assembly chain, identify contributors and evaluate worst-case or statistically appropriate accumulation as justified:

```text
datum → seat → bearing → shaft → spacer → second bearing → moving feature
```

If a stack-up is not closed, the assembly precision is not demonstrated even when every individual part is nominally accurate.

Use GD&T only to communicate a functional requirement. Choose meaningful datum features and apply form, orientation, location, profile, position, runout, straightness, flatness, parallelism, perpendicularity, and coaxiality/concentricity concepts where they control function. Do not decorate a drawing or model with symbols whose tolerance zone, datum reference frame, or inspection method is not understood.

## Parametric and master-model practice

- Centralize design, hardware, manufacturing, and derived parameters separately.
- Name relationships (`shaft_axis`, `bearing_spacing`, `mounting_pitch`, `datum_height`, `clearance`) rather than scattering coordinates.
- Prefer stable reference geometry, axes, planes, skeletons, and master layouts over fragile transient edges/faces.
- Use top-down design when interfaces and motion are strongly coupled; use bottom-up design for standardized or independently controlled parts; use a hybrid deliberately.
- For complex assemblies, define hardware/interfaces, kinematic skeleton, datums/axes, motion envelopes, structural master geometry, individual components, and manufacturing detail in that order.
- Regenerate after changing major parameters and inspect interface drift.

## Feature and structural reasoning

Use holes, counterbores, countersinks, slots, pockets, bosses, ribs, gussets, shoulders, bearing/shaft/rail seats, locating features, dowel holes, keyways, retaining-ring grooves, insert pockets, nut traps, cable passages, and inspection openings only for a stated purpose.

Trace loads from application point to reaction points:

- where does the force enter and leave?
- what section carries it?
- which joints, bearings, and interfaces does it cross?
- what bending moment, torsion, shear, bearing stress, buckling, compliance, and thermal movement result?

Reason about stiffness and deflection before ultimate strength when precision matters. Use section moment of inertia, box/closed sections, webs, ribs, gussets, wider bearing spacing, and shorter load paths intelligently. Do not use decorative ribs or make everything solid as a substitute for a load path.

For precision mechanisms also check Abbe error, cosine error, lever-arm amplification, racking, backlash, preload, runout, alignment, compliance, thermal expansion, and joint flexibility.

## Kinematics, bearings, shafts, and fasteners

For each moving body explicitly state allowed and constrained translations and rotations. Detect both underconstraint and redundant overconstraint. A bearing system must assign radial and axial reactions, locating/fixed and floating roles, preload, spacing, shaft shoulders, retention, thermal movement, installation, and service. A coupler is not a bearing, and a motor bearing is not automatically an axis-thrust support.

For joints, separate location and shear transfer from clamping/preload. Check preload, tension, shear, bending, bearing stress, thread engagement, pull-out, creep, washers, inserts, nuts, dowels, shoulders, and access. Bolts are not precision locating pins by default.

For every assembly component answer: what supports it, locates it, fastens it, and loads it; which DOF it has or must not have; how it is installed and removed; what tool access is required; and whether any component is trapped.

## Manufacturing-aware definition

Select the intended process before declaring geometry manufacturable. The skill supports:

- **CNC milling:** stock, datums, setups, workholding, cutter/tool access, tool diameter, internal radii, reach, pocket depth, undercuts, tolerance, and datum transfer;
- **CNC turning:** rotational symmetry, chucking, tool access, shoulders, grooves, and retention;
- **FDM/SLA/SLS:** anisotropy, orientation, support, overhang, bridging, warping, shrinkage, compensation, walls, inserts, and post-processing;
- **laser/waterjet:** kerf, heat-affected edge, minimum feature, nesting, and datum transfer;
- **sheet metal:** bend radii, bend allowance, reliefs, tooling access, and flat pattern;
- **manual machining:** available setups, tools, workholding, inspection, and achievable tolerance.

A geometrically valid STEP file is not automatically machinable. Before a CNC-machinability claim, identify stock, datums, setup count, workholding, cutter diameter, tool reach, special tooling, and inspection strategy.

## Design for inspection

Critical geometry must be measurable. Name the inspection method and accessible features: caliper, micrometer, bore gauge, height gauge, surface plate, dial indicator, CMM, gauge, functional fit check, or other justified method. A tolerance without a credible verification method is incomplete product definition.

## Validation and maturity gates

Validate separately:

- **geometric:** valid manifold solids, dimensions, no zero-thickness accidents;
- **assembly:** interference, clearance, travel, tool access, sequence, and removal;
- **mechanical:** load path, stiffness/deflection, supports, constraints, and joint behavior;
- **manufacturing:** process capability, workholding, tool/support access, and post-processing;
- **dimensional:** tolerances, fits, stack-ups, alignment, and inspection;
- **human engineering:** physical plausibility, serviceability, proportions, and obvious nonsense.

Use these maturity states:

| State | Minimum evidence |
| --- | --- |
| `CONCEPT` | Function, major requirements, layout, assumptions, and alternatives. |
| `DIMENSIONAL-CONCEPT` | Critical interfaces, datum scheme, dimension sources, preliminary tolerances, and envelopes. |
| `PROTOTYPE` | Parametric geometry, process screen, assembly/motion review, and known provisional interfaces. |
| `MANUFACTURING-CANDIDATE` | Process/setup or print dossier, controlled tolerances/fits, inspection plan, assembly/service review, and high-quality engineering views. |
| `VALIDATED` | Measured critical dimensions, physical fit/function tests, process evidence, and closed blocking review findings. |
| `RELEASED` | Controlled source revision, drawings/PMI, BOM/provenance, reproducible exports, approval, and change control. |

A valid STL, STEP, or passing automated test cannot promote a model by itself.

## Visual review and deliverables

Before a manufacturing-candidate or release claim, create engineering views that expose the questions a reviewer must answer: clear isometric and orthographic views, sections through hidden seats and load paths, exploded assembly views, transparent clearance/motion overlays, hardware-only and structure-only views, interface closeups, and motion/service extremes. Use labels, legends, stable camera names, model revision, units, and a stated question per view. These are review evidence, not beauty renders.

Depending on the project, provide only the outputs that support manufacture and assembly:

- parametric source and controlled parameters;
- STEP part and assembly exports;
- STL/mesh only where additive manufacturing or visualization requires it;
- engineering drawings or model-based definition/PMI;
- critical-dimension and tolerance/fit tables;
- BOM and hardware provenance;
- assembly/service instructions;
- inspection plan and validation report.

Do not generate documentation solely to satisfy a checklist; each artifact must support a manufacturing, assembly, inspection, or review decision.

## CAD-system independence and build123d

The methodology must work with build123d, CadQuery, FreeCAD, Fusion, SolidWorks, Inventor, Onshape, or another parametric system. Keep the engineering contract independent of API syntax.

For build123d, use robust named parameters, reusable functions/classes, local `Plane`/`Axis`/`Location` frames, deterministic transforms, explicit assemblies, stable reference geometry, and explicit STEP/STL export settings. Avoid fragile topology references, hidden import-time exports, unexplained magic numbers, and fusion that hides service boundaries. Keep reference hardware/envelopes separate from manufactured parts and route geometry through validation adapters.

## Required self-review

Before completing a precision CAD task, answer:

- Is every critical dimension justified and confidence-labeled?
- Are datums, fits, tolerances, GD&T intent, and tolerance stacks explicit?
- Are interfaces, load paths, DOFs, bearings, fasteners, and service actions credible?
- Can every part be manufactured and inspected by the selected process?
- Can every component and fastener actually be assembled, removed, and replaced?
- Are commercial models dimensionally credible and provenance-controlled?
- Did automated checks and human engineering review both pass?
- Would a machinist, fabricator, or inspector know what to make and verify?

If any critical answer is no or unknown, retain the appropriate provisional state.

## Compact example

**Bad:** A bearing housing is modeled as a visually centered cylinder cut from a block, with a guessed bore and no inspection or retention plan.

**Good:** The bearing source and confidence are recorded, the housing datum/shoulder/retention and fit are defined, shaft alignment and load reactions are checked, machining or printing constraints are explicit, and the bore/face inspection method is named.

Read the supporting [research notes](references/engineering-references.md), [anti-pattern catalog](references/anti-patterns.md), and [generic examples/exercises](references/examples-and-exercises.md) when the task requires detailed precision practice.
