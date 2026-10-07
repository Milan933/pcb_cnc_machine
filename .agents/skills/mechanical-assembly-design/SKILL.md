---
name: mechanical-assembly-design
description: Design and review generic mechanical assemblies by reasoning about support, location, fastening, loads, degrees of freedom, installation, removal, service, and assembly order.
---

# Mechanical assembly design

Use this skill whenever multiple parts must work together. An assembly is a support-and-constraint system, not merely a set of solids positioned near one another.

## Component contract

For every component or subassembly, record answers to:

1. What supports it?
2. What locates it, and relative to which datum?
3. What fastens or retains it?
4. What load or motion does it transfer?
5. Which degrees of freedom must it have?
6. Which degrees of freedom must it not have?
7. How is it installed?
8. How is it removed or replaced?
9. What tools, hand clearance, and inspection access are required?

An unresolved answer is a review issue, not an invisible assumption. Production-intent assemblies must not contain unsupported or merely floating components.

## Assembly workflow

- Establish the fixed reference component and assembly coordinate system.
- Define component interfaces and local frames before placing instances.
- Choose top-down, bottom-up, or hybrid design deliberately. Use top-down layout for shared envelopes and interfaces; use bottom-up library parts for standard hardware or independently released components; use subassemblies to control complexity.
- Define kinematic relationships from intended behavior, not from convenient coincident faces.
- Build support chains from the moving or loaded element back to ground.
- Trace loads through interfaces, fasteners, seats, and structural members.
- Simulate installation and removal in the required sequence, including captive components and tool approach.
- Test the full motion range and service positions for collision, clearance, cable, and access problems.

## Degrees of freedom and constraints

Describe each relationship by the freedoms it permits and removes. A fastened relationship removes relative motion; a slider permits one translation; a revolute permits one rotation; a locating feature may constrain one direction while allowing adjustment elsewhere.

Avoid both extremes:

- **Underconstrained:** a component can drift, rotate, or separate in a way the real assembly cannot tolerate.
- **Overconstrained:** redundant locating features force parts to fight manufacturing variation, bind, or become impossible to assemble.

Distinguish connection from collision. Interference may be intentional clamping or press fit, but coincident or overlapping solids are not proof of attachment.

## Load and service reasoning

For each critical load path, identify the primary load case, the reaction surfaces, the fastener preload, local bearing and shear areas, bending leverage, and the failure consequence. Check that the support is structural rather than a visual placeholder.

Create an assembly-order list before finalizing captive nuts, bearings, shafts, covers, cable routes, or enclosed fasteners. A part that can be modeled but cannot be inserted, tightened, inspected, or replaced is not assembly-ready.

## Good vs bad

**Bad:** A bearing, motor, and rail are placed in their intended positions and declared connected because their solids do not collide.

**Good:** Each is assigned a support datum, locating shoulder or interface, fastening method, allowable DOF, installation path, tool access, service removal path, and load reaction. The complete chain is checked at both motion extremes.

This skill builds on [mechanical-cad-design](../mechanical-cad-design/SKILL.md) and feeds [cad-design-review](../cad-design-review/SKILL.md).
