---
name: printed-structural-design
description: Design and review load-bearing PETG machine structures for stiffness, creep resistance, printability, and durable fastener and rail interfaces.
---

# Printed structural design

Use this skill for printed PETG frames, gantries, carriages, mounts, rail
supports, and structural joints. It is not a license to treat printed
plastic as dimensionally stable metal.

## Material behavior

PETG stiffness, strength, creep resistance, and dimensional stability depend
on filament, temperature, moisture, print orientation, layer bonding,
perimeter count, infill, cooling, and time under load. Treat catalogue
filament values as provisional until the actual print process is identified.

Separate these questions:

- short-term elastic stiffness under tool load;
- strength and failure mode at the worst joint;
- long-term creep under preload and spindle mass;
- thermal distortion near the spindle;
- dimensional repeatability after printing, installation, and service.

Do not use an arbitrary safety factor or infill percentage as a substitute for
identifying the load path and the dominant deformation mode.

## Geometry before infill

Prefer stiffness through geometry:

- closed box sections and monocoque skins;
- ribs aligned with load paths;
- gussets with large radii and gradual transitions;
- triangulation where it closes a shear or bending path;
- distributed interfaces that spread rail and fastener loads;
- short unsupported spans;
- generous fillets that reduce stress concentration and improve printability.

Avoid copying aluminum-extrusion cross sections without analyzing how printed
walls, layer orientation, joints, and local buckling actually carry load.
Increasing infill may add mass without adding useful section stiffness.

## Print orientation and anisotropy

Orient layers so the primary tensile, bending, peel, and shear loads do not
depend on weak inter-layer adhesion when a different orientation or geometry
can carry them more directly. Record the expected load direction relative to
the layer planes.

Every part must declare:

- intended print orientation;
- support strategy or unsupported-overhang limits;
- critical datum faces;
- critical-hole or insert operations;
- post-print conditioning and inspection;
- a realistic orientation that fits the Voron 2.4 350 usable build volume.

Do not pass a part because its default bounding box fits. Consider rotation,
support access, first-layer orientation, bed adhesion, warping risk, and
whether the critical faces can be printed or machined to the needed quality.

## Walls, perimeters, ribs, and transitions

Choose wall and perimeter counts from the calculated load path, local
buckling, screw bearing, print line width, and inspection needs. State them as
parameters or process requirements; do not scatter slicer-specific literals
through geometry.

Ribs should connect load-bearing skins and terminate with a gradual
transition. Avoid isolated thin ribs, abrupt T-junctions, sharp internal
corners, and ribs that cannot be cleaned or printed reliably. A rib that
changes load direction should have a gusset or a closed junction.

## Fasteners and joints

PETG is poor as a repeatedly loaded bearing surface when preload or creep can
change the datum. For each joint, identify whether the load is carried by:

- a through-bolt in compression or shear;
- a captive nut or metal clamp;
- a heat-set insert;
- a bearing or rail seat;
- a printed feature that is explicitly verified by a coupon.

Use heat-set inserts for serviceable threads only when their installation
temperature, boss geometry, pull-out, torque, and surrounding wall are
controlled. Use captive nuts when they improve assembly access and prevent
thread stripping. Use through-bolts or metal load spreaders where preload,
rail alignment, or creep makes an insert inadequate.

Do not make a fastener carry a bending moment through a thin printed wall
without checking edge distance, local bearing, tear-out, and load spreading.
Avoid concentrated loads at isolated bosses; connect the boss to skins or
ribs and distribute the interface.

## Rails, bearings, and precision interfaces

Rail mounting surfaces must be continuous, supported, inspectable, and
stiff relative to the tool-point requirement. A rail on a flexible printed
skin can amplify error even if the rail itself is rigid.

Provide:

- a repeatable datum face or shoulder where appropriate;
- accessible fasteners and a tightening sequence;
- clearance for carriage travel and lubrication;
- a way to align or shim without crushing PETG;
- local reinforcement at every rail and bearing interface;
- a service plan for replacing the rail, bearing, or insert.

Do not assume printed holes are bearing fits. Decide whether holes are for
clearance, alignment, drilling after printing, a bushing, or a metal insert.

## Tolerances and printability

Use process-specific tolerances based on measured printer behavior, material,
orientation, and feature size. Mark every tolerance as an assumption until
the relevant calibration coupon is measured. Do not imply micrometer accuracy
from a CAD decimal.

Check:

- first-layer and warping risk;
- bridge and overhang support;
- trapped supports or inaccessible captive nuts;
- tool access for post-processing;
- insert installation access;
- minimum wall and edge distance;
- shrinkage or distortion across the largest dimension;
- assembly order and rework access;
- cable, chip, and cleaning access.

## Structural evidence

For each primary structural part, record the dominant load cases, load path,
material and print assumptions, critical interfaces, predicted deflection or
failure mode, print orientation, and the test or inspection that will verify
the decision. If the result is sensitive to creep or layer bonding, plan a
representative coupon or long-duration preload test before release.
