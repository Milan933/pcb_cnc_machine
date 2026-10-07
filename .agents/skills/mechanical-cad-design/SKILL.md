---
name: mechanical-cad-design
description: Design or review generic parametric mechanical geometry for machines, fixtures, mechanisms, brackets, enclosures, and structural parts using function, datums, interfaces, load paths, and manufacturing constraints.
---

# Mechanical CAD design

Use this as the foundational mechanical-CAD skill for any product or mechanism. It is deliberately independent of a machine type, material, or CAD backend. Load a domain overlay only when the product requirements require one.

The design objective is a traceable mechanical solution, not a visually plausible solid. Geometry must be explainable from function, requirements, datums, interfaces, load paths, manufacturing, and service.

## Design chain

Work through this chain explicitly:

```text
FUNCTION → REQUIREMENTS → DATUMS → INTERFACES → LOAD PATHS
→ PRIMARY GEOMETRY → FUNCTIONAL FEATURES → MANUFACTURING FEATURES → DETAILING
```

For every major feature, be able to state:

- the requirement or interface it serves;
- the datum or reference that controls it;
- the load, motion, clearance, or manufacturing reason for its size;
- the evidence that will verify it.

Do not default to “make a box approximately this size and add holes.” If a dimension is not derived, measured, selected from hardware, or intentionally screened as an envelope, label it as an assumption and keep it editable.

## Recommended sequence

1. Define the operating function, users, environment, loads, motion, service life, and manufacturing process.
2. Convert those needs into measurable requirements and acceptance evidence.
3. Choose primary datums: functional origin, mounting plane, axis, symmetry plane, and inspection references.
4. Establish a coordinate frame and named interface frames before detailed geometry.
5. Lay out interfaces, clearance volumes, motion limits, and the dominant force paths.
6. Build the primary load-carrying geometry: sections, skins, plates, shafts, seats, shoulders, and supports.
7. Add functional features: bosses, ribs, gussets, pockets, bearing seats, rail seats, alignment keys, and access openings.
8. Add manufacturing features: draft or chamfers, fillets, print splits, tool clearance, insert pockets, and post-processing allowances.
9. Add only detailing that improves function, inspection, safety, service, or communication.
10. Validate geometry, interfaces, load paths, manufacturing, assembly, and review evidence separately.

## Datums and reference strategy

Use stable functional references rather than transient face selections wherever possible. A datum should answer what is being located, what variation matters, and how it will be inspected. Use symmetry when it is functionally real; do not introduce symmetry that hides independent adjustment or manufacturing variation.

Name local frames by purpose, such as `mounting_datum`, `shaft_axis`, `bearing_seat`, or `interface_motor`. Record handedness, units, positive directions, and the parent frame. A component should be buildable in its local frame and placed in the assembly through an explicit transform.

Use master layouts, skeletons, or reference geometry for shared interfaces and envelope relationships. Keep manufactured solids separate from reference and clearance geometry so a visual envelope cannot silently become a load-bearing feature.

## Feature and parameter discipline

- Centralize dimensions that control more than one component.
- Give every repeated interface a reusable feature function or schema.
- Use meaningful parameter names and units; avoid unexplained magic numbers.
- Preserve design intent when changing dimensions: constraints should express relationships, not merely reproduce a snapshot.
- Prefer shoulders, seats, keys, and mating faces for location over hole coincidence alone.
- Treat fillets, chamfers, and cosmetic detail as late features unless they affect stress, fit, printability, or safety.
- Check local wall thickness, section stiffness, stress concentrations, and access at the actual interface rather than only at the part bounding box.

## Parametric CAD implementation

The engineering method must remain portable across CAD systems. In build123d or a similar scripted system:

- keep parameters and interface contracts separate from feature construction;
- build reusable parts in a documented local frame;
- use `Plane`, `Axis`, and `Location` objects for named references and deterministic transforms;
- keep exports explicit and outside import-time geometry construction;
- separate hardware/reference geometry from manufactured geometry;
- use small feature functions and validation helpers rather than one monolithic script;
- export STEP as the editable exchange derivative and STL/mesh as a manufacturing derivative, never as the source of truth.

## Good vs bad

**Bad:** A motor bracket is a rectangular block sized from a screenshot, with four holes added until the motor appears centered.

**Good:** The motor interface frame is defined from the mounting pattern, shaft center, body envelope, connector access, installation direction, and reaction moment. The bracket section and bosses are then sized from the load path, print orientation, fastener access, and service removal path.

Read [the generic engineering references](../mechanical-cad-references.md) for the research basis and [the anti-pattern catalog](../mechanical-cad-anti-patterns.md) when reviewing a design.
