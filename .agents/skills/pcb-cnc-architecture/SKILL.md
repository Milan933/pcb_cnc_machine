---
name: pcb-cnc-architecture
description: Define or review the system architecture of a small PCB-focused CNC, including force loops, workholding, probing, height mapping, and process-specific priorities.
---

# PCB CNC architecture

Use this skill when selecting or reviewing the machine-level architecture.
It applies before detailed part geometry and whenever a mechanical choice
changes the tool-point force loop, PCB datum, or process capability.

## Scope and dependency boundary

This skill is intentionally retained as a PCB-CNC-specific overlay. It adds
FR4 isolation routing, drilling, outline cutting, PCB workholding, probing,
height mapping, spindle, and process-datum requirements to the generic
mechanical architecture and review skills. It should not be used as a generic
machine-design template.

## Primary design objective

Optimize the machine for FR4 isolation routing, PCB drilling, and PCB outline
cutting. The important output is a stable, repeatable tool point over a
clamped PCB, not maximum material-removal rate.

PCB milling differs from general-purpose CNC machining because:

- the tool is often small and sensitive to runout;
- isolation depth can be a small fraction of a millimeter;
- PCB stock is thin and can bend or move under clamping;
- board flatness and height variation directly change copper isolation;
- drilling is sensitive to axial alignment, runout, and retract behavior;
- the expected cutting forces are lower, so tool-point deflection,
  vibration, and datum stability dominate rather than bulk cutting force;
- FR4 dust and abrasive glass fibers require containment, extraction, and
  service planning.

Do not import a heavy metal-mill architecture merely because it is familiar.
Use the smallest structure that closes the force loop with adequate stiffness,
service access, and process margin.

## Priority stack

When requirements conflict, review them in this order:

1. safety, containment, and reliable machine limits;
2. PCB datum stability and workholding;
3. low tool-point deflection and low spindle runout;
4. short force loops and adequate gantry rigidity;
5. probing and height-map repeatability;
6. required travel and service access;
7. speed, cost, and convenience.

Record any deliberate priority inversion in an engineering decision record.

## Mechanical architecture rules

### Force loop

Trace the load from tool tip through spindle mount, Z carriage, guides,
gantry, base, workholding, and PCB. Prefer a short, direct, closed load path.
Do not count a component as stiff merely because its material is strong:
interfaces, joints, guide spacing, and bending leverage often dominate.

### Spindle overhang

Keep the tool and spindle nose as close as practical to the Z guide support.
Minimize unsupported tool length, adapter stacks, and tall moving plates.
Account for collet, tool, probe clearance, and the actual cutting datum rather
than measuring only to the spindle body.

### Z axis

Make Z as short as the work envelope and tool-change/service needs allow.
Place guides to resist both transverse force and spindle moment. The design
must show how Z preload, spindle mass, cable drag, and cutting load are
reacted without concentrating load in a single printed boss.

### Gantry

The gantry must resist pitch, yaw, and roll at the tool point. Use guide
spacing, closed printed sections, ribs, and distributed mounting interfaces
to control bending and torsion. A nominally wide travel target is not free:
the resulting span and moving mass must be included in the trade study.

## PCB interfaces

### Workholding

Workholding must:

- support thin board stock over the routed region;
- avoid bowing the PCB through uneven clamp force;
- establish a repeatable XY and Z datum;
- leave room for probing and tool access;
- remain secure through drilling and outline cutting;
- allow loading, unloading, and cleaning without disturbing machine datums.

Document the board size range, thickness range, registration method, clamp
loads, and any vacuum or adhesive assumptions. Do not hide these in CAD.

### Spoilboard

Treat the spoilboard as a replaceable process surface, not as an arbitrary
structural plate. Define its mounting datum, replacement method, flatness
verification, probing relationship, and allowable resurfacing. The design must
prevent a worn or resurfaced spoilboard from silently changing the machine
coordinate system.

### Probing

Reserve a mechanically stable probe datum and a controller interface. Decide
whether probing establishes tool length, PCB surface, XY registration, or more
than one of these. Probe repeatability must be measured with the actual probe
and cable routing.

### PCB height mapping

A height map compensates measured board or fixture variation; it does not
repair a moving gantry, loose rail, or unstable workholding. Define:

- the machine datum and PCB datum;
- the safe probing region and grid or adaptive sampling policy;
- probe force and repeatability;
- map storage and job association;
- interpolation and boundary behavior;
- how the map is applied to isolation and outline toolpaths;
- how stale or invalid maps are rejected.

Keep the map within the measured region and re-probe whenever the board,
fixture, tool, or datum changes in a way that affects the measurement.

## Process-specific requirements

### Isolation routing

Prioritize spindle/tool runout, short tool overhang, repeatable shallow Z
depth, PCB support, height mapping, and low vibration. Evaluate tool-point
deflection at the actual cutter and depth; a large frame stress margin does
not prove isolation quality.

### Drilling

Prioritize axial alignment, spindle runout, tool retention, board support,
controlled feed/retract, chip evacuation, and hole-size verification. Include
the drilling cycle and tool length in the Z travel budget.

### Outline cutting

Prioritize secure board registration, full-area support, safe depth margin,
chip and dust control, and a strategy for the final pass. If tabs or a
perimeter fixture are needed, treat them as process requirements and validate
their effect on board datum and cleanup.

## Architecture deliverables

Every architecture option should include a force-loop sketch, travel budget,
datum/workholding concept, probing concept, service access, major interfaces,
and risks. Select an architecture only after comparing at least one credible
alternative and recording unresolved dependencies.
