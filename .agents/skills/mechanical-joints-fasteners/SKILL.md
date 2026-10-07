---
name: mechanical-joints-fasteners
description: Design generic mechanical joints for preload, shear, tension, bending, bearing, pull-out, creep, alignment, tolerance, access, and service life, including joints in printed polymers.
---

# Mechanical joints and fasteners

Use this skill whenever parts are bolted, clamped, inserted, keyed, pinned, press-fit, or otherwise joined. Start from the joint load and function, not from a preferred screw size.

## Core rule

> Fasteners provide clamping and preload. Geometry provides location and, where practical, shear transfer.

This rule does not forbid a bolt from carrying shear or locating a joint; it requires the designer to justify that choice and check bearing, slip, clearance, fatigue, tolerance, and failure consequence. A bolt shank is not automatically a precision datum.

## Joint design sequence

1. Define the joint function: clamp, locate, transmit torque, carry shear, seal, permit adjustment, or allow service removal.
2. Identify preload, separation, slip, shear, tension, bending moment, impact, fatigue, thermal, and creep cases.
3. Select the load-transfer surfaces: mating faces, shoulders, keys, splines, dowels, tongues, bearing seats, bosses, or clamped friction.
4. Select fastener type, size, grade, quantity, spacing, tightening access, and replacement strategy.
5. Check preload retention, local bearing, edge distance, tear-out, pull-through, thread stripping, insert pull-out, joint slip, and member bending.
6. Check tolerance stack-up, assembly sequence, tool clearance, washer/head clearance, and service removal.
7. Define inspection and test evidence: torque, clamp gap, alignment, pull-out, slip, fatigue, or environmental exposure as appropriate.

## Printed polymer joints

For heat-set inserts or captive nuts, record the actual insert outer diameter, length, pilot range, insertion depth, boss/wall material, edge distance, insertion direction, mating-hole clearance, and tool access. Do not freeze supplier-dependent dimensions from a nominal thread label. Install flush or to the supplier’s specified condition; prevent the screw from bottoming.

For a printed boss or through-bolt, connect the load into skins or ribs, avoid isolated thin walls, and check local crushing, creep, layer separation, and jack-out. Use a compression limiter or metal washer/interface when polymer compression would otherwise control preload retention.

## Access and maintainability

A joint is not complete until a tool can approach the fastener, the part can be held during tightening, the joint can be inspected, and the hardware can be removed without destroying unrelated parts. Check both initial assembly and the most likely service operation.

## Good vs bad

**Bad:** Four screws are placed around a bracket and assumed to locate it against lateral load because the holes line up.

**Good:** A shoulder and keyed face carry lateral shear, the screws clamp the mating faces, edge distances and boss walls are checked, the tightening sequence is accessible, and one fastener can be removed for service without losing the datum.

Use [design-for-3d-printing](../design-for-3d-printing/SKILL.md) for printed-process constraints and [mechanical-assembly-design](../mechanical-assembly-design/SKILL.md) for installation and DOF.
