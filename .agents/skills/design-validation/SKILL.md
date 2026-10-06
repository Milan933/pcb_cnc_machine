---
name: design-validation
description: Define and implement fail-closed validation for PCB CNC travel, clearances, interfaces, printed-part fit, and assembly evidence.
---

# Design validation

Use this skill to create validation rules, geometry adapters, test fixtures,
or review reports for the PCB CNC. Validation is evidence about a particular
parameter set and model revision; it is not a replacement for engineering
judgment or a physical test.

## Validation policy

Every rule has a stable ID, a clear input contract, a severity, a result, and
evidence. Use at least these result states:

- pass: the required evidence is present and the rule is satisfied;
- fail: the evidence is present and the rule is violated;
- not-ready: required geometry, parameter, supplier, or test evidence is
  missing;
- not-applicable: the rule is explicitly outside the current scope.

Missing evidence must not silently become pass. Reports must identify the
model revision, parameter set, CAD version, units, and rule set.

## Required rule catalog

The validation architecture must provide rules for:

1. required X and Y working travel;
2. required Z working travel and selected Z range;
3. rail-carriage usable travel;
4. lead-screw usable travel and end margins;
5. solid and swept-volume collisions;
6. spindle clearance from frame, bed, clamps, and workholding;
7. spindle-to-bed clearance across tool and workholding cases;
8. motor envelope and connector clearance;
9. coupler, bearing, and screw-support clearance;
10. screw and tool accessibility during assembly and service;
11. assembly order and removal access;
12. minimum printed wall thickness;
13. minimum edge distance around fasteners, inserts, and holes;
14. continuous, supported linear-rail mounting surfaces;
15. realistic printable orientation within the usable Voron 2.4 350 volume.

The first repository iteration defines interfaces and a few geometry-free
checks. Geometry-aware rules must be added as soon as the corresponding
part or assembly data exists.

## Print-volume rule

Do not validate a printable part using only one unrotated bounding box.
Require the part to provide one or more credible print-orientation candidates.
Each candidate must include the resulting extents and, when relevant, notes
about support, bed contact, critical faces, warping, and post-processing.
Pass if at least one candidate fits within the configured usable build volume
and its manufacturing notes are acceptable. Return not-ready when no
candidate is documented.

The build volume is a constraint on the whole print setup, not just on the
solid: account for skirts or brims if required, nozzle access, bed adhesion,
support removal, and usable margins.

## Travel and interface rules

Compare required tool-point travel with actual usable travel, not rail length.
Subtract carriages, screw supports, hard stops, homing margins, tool length,
probe clearance, and workholding clearance where applicable.

For every guide and screw, validate that:

- the supported travel covers the working envelope;
- the carriage does not run into a rail or screw support;
- the screw has safe end margins and no coupler collision;
- the motor, bearing, and fasteners remain accessible;
- the mounting surface is continuous and structurally supported.

## Clearance and collision rules

Use exact solids or documented swept volumes where available. Check the
worst-case tool, spindle, board, clamp, carriage, and homing positions.
State whether a check includes cable chains, spindle cables, dust extraction,
probe hardware, and fastener heads.

Do not hide a collision with a large tolerance. Record the clearance value,
the source of the tolerance, and whether it is calculated or experimentally
verified.

## Printed-part rules

Validate the actual critical wall and load path, not a generic CAD shell.
Check local thickness, edge distance, insert envelope, fastener bearing,
rail-seat continuity, and print orientation. A part may be geometrically
printable but structurally unready; report these separately.

## Validation architecture

Keep rule definitions independent from the CAD backend. A geometry adapter
should expose named solids, transforms, bounding or swept volumes, datum
faces, and measured feature metadata. build123d or CadQuery integration must
translate into that interface rather than spreading backend calls through
every rule.

Use small deterministic fixtures for automated checks. Add physical evidence
for print dimensions, insert pull-out, rail alignment, homing repeatability,
tool-point deflection, spindle runout, and PCB process results as the design
progresses.

## Report and release behavior

Validation output should group issues by rule ID and component, distinguish
blocking errors from warnings, and include a remediation or evidence request.
Manufacturing exports are not releasable while blocking errors or not-ready
release gates remain, unless a named reviewer accepts the exception in an
engineering decision record.
