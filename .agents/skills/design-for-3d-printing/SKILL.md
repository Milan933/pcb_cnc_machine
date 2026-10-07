---
name: design-for-3d-printing
description: Design functional FDM parts and assemblies around anisotropic strength, print orientation, walls, supports, tolerances, inserts, split planes, and inspection rather than infill alone.
---

# Design for FDM 3D printing

Use this skill for functional FDM parts in any material or product. Treat the printed process as part of the design: material, nozzle, layer height, perimeter strategy, temperature, moisture, cooling, bed adhesion, and post-processing all affect the result.

## Start with the load path and print process

Before choosing a wall or infill value, identify:

- the dominant tension, compression, bending, shear, peel, impact, and creep loads;
- the load direction relative to layer planes and perimeter loops;
- the critical datums, holes, seats, insert regions, and inspection faces;
- the intended printer, nozzle, layer height, material, orientation, and support strategy;
- the expected environment, temperature, moisture, and service duration.

Orient layers and perimeter paths so critical loads are carried by continuous material and perimeters where possible. Do not treat isotropic catalogue strength as the printed-part strength.

## Geometry-first printability

Prefer stiffness through geometry: closed sections, skins, ribs that connect load-bearing faces, gussets with gradual transitions, bosses tied into ribs or skins, short unsupported spans, and distributed interfaces. Infill is a process variable; it is not a substitute for a load path or section stiffness.

Review:

- wall and perimeter count at every critical feature;
- local buckling and bearing around holes;
- overhangs, bridges, support removal, and trapped support;
- elephant foot, warping, shrinkage, seam location, and bed adhesion;
- hole compensation and tolerance by orientation and feature size;
- whether a critical face should be printed on the bed, machined, or inspected after printing.

## Split and join strategy

When a part exceeds the practical print envelope, do not split at an arbitrary visual midpoint. Place split planes using bending moment, shear transfer, datum continuity, print orientation, assembly access, and service needs. Use keyed joints, shoulders, tongue-and-groove features, registration bosses, shear keys, and clamped interfaces. Keep the split out of the most highly loaded or least inspectable region unless analysis supports it.

Use a multi-part assembly when it improves orientation, strength, service, or inspection. A single-piece print is not inherently better.

## Polymer joint interfaces

Reserve solid material around heat-set inserts, captive nuts, through-bolts, and bearing seats. The insert supplier and actual material/process determine the pilot, depth, wall, and installation conditions; use a provisional envelope until those are measured and coupon-tested. Provide installation-tool access and prevent screw bottoming or jack-out.

## Manufacturing dossier

Every functional printed part should record:

- print orientation and build-volume candidate;
- load direction relative to layers;
- wall/perimeter and infill intent;
- supports, bridges, overhang limits, and bed-contact surfaces;
- critical dimensions, tolerance assumptions, hole compensation, and post-processing;
- insert/fastener installation procedure;
- inspection points and the first physical test.

## Good vs bad

**Bad:** Increase infill to 80% inside a thin, open bracket whose rail load still travels through a weak layer boundary and a narrow boss.

**Good:** Reorient the bracket, thicken the load-bearing skins, connect the boss to a gusseted section, provide a supported seat, and validate the hole and insert with a coupon. Infill is selected afterward for print reliability and local support.

Use [mechanical-joints-fasteners](../mechanical-joints-fasteners/SKILL.md) for joint sizing and [the anti-pattern catalog](../mechanical-cad-anti-patterns.md) for common FDM failures.
