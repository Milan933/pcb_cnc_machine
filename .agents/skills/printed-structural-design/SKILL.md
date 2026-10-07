---
name: printed-structural-design
description: Design and review load-bearing PETG PCB-CNC structures for stiffness, creep resistance, printability, and durable fastener and rail interfaces using the generic FDM and joint skills as a foundation.
---

# Printed structural design

Use this skill for printed PETG frames, gantries, carriages, mounts, rail
supports, and structural joints. It is not a license to treat printed
plastic as dimensionally stable metal.

## Scope and dependency boundary

This is the PCB-CNC structural overlay. Load
`.agents/skills/design-for-3d-printing/SKILL.md` for generic FDM process and
printability reasoning and
`.agents/skills/mechanical-joints-fasteners/SKILL.md` for generic joint/load
transfer reasoning. The project-specific rules below retain PETG machine
structure, rail/gantry interfaces, Voron 2.4 print-boundary assumptions, and
CNC service requirements.

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

The project fastening rule is:

> Fasteners provide preload; printed geometry provides location and shear
> transfer. Heat-set inserts are the default reusable threaded interface in
> PETG. Through-bolts are reserved for structural joints where insert
> pull-out, creep, preload, or joint moment capacity makes them necessary.

Use heat-set inserts as the primary reusable threaded interface. Standardize
the hierarchy to M3 for small covers, sensors, limits, probe hardware, and
accessories; M4 for general structural, motor, bearing, spindle, and module
joints; and M5 only for a documented high-load case. Do not add another thread
size without a technical reason. The screw supplies clamp preload; a shoulder,
step, tongue-and-groove, key, boss, pocket, registration feature, shear key,
mating planar surface, or interlocking rib should carry location and shear.
Important joints must have substantial bosses connected to ribs or skins.

Use through-bolts selectively when insert pull-out or PETG creep, high bending
moment, high clamping force, cyclic loading, or failure consequence makes an
insert inadequate. Through-bolts still require geometric shear transfer and a
documented justification; a bolt shank is not a precision locating pin by
default. A gantry crossmember must be mechanically seated with a deep
tongue-and-groove, stepped socket, keyed pocket, shoulder, or interlocking rib
and then clamped. It must not hang from M5 screws.

Do not freeze an insert pocket from a generic nominal size. The centralized
insert interface must eventually record insert OD, length, pilot range,
insertion depth, surrounding wall, edge distance, insertion direction, screw
clearance, and soldering-iron/tool access. Keep supplier-dependent dimensions
unresolved until the actual insert is selected, measured, and coupon-tested.

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

## Structural modularity and print-size boundary

Treat the Voron 2.4 350 as having a materially smaller practical usable area
than its nominal envelope. Prefer structural-part XY dimensions at or below
300 x 300 mm; use 320 mm as a conservative maximum screening limit. Any part
at or above 300 mm requires an explicit printability review covering orientation,
diagonal clearance, bed adhesion, warping, datum inspection, insert access,
and assembly access. Use indexed PETG interfaces, heat-set inserts, and
selective through-bolts to split parts when a one-piece print would compromise
stiffness, alignment, serviceability, or process evidence.

Motors, rails, carriages, lead screws and nuts, bearings, spindle, limit
switches, probe wiring, and moving-bed wiring must remain replaceable without
destroying the printed structure.

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
