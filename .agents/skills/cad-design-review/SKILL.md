---
name: cad-design-review
description: Perform rigorous generic mechanical CAD reviews that combine automated geometry checks with human engineering sanity checks, evidence gates, load-path review, assembly review, and manufacturing review.
---

# CAD design review

Use this skill before calling a mechanical design ready for manufacture, release, or physical integration. Automated solid validity, bounding boxes, interference, and print-envelope checks are necessary but never sufficient.

## Review gate

Require an explicit human-review state. Use `not-ready`, `review-required`, `candidate`, and `released` (or an equivalent controlled vocabulary). A design cannot advance because tests happen to pass; missing evidence remains not-ready.

## Review sequence

1. Confirm requirements, assumptions, material/process, hardware provenance, and model revision.
2. Review datums, interfaces, coordinate frames, and tolerance strategy.
3. Trace every major force and motion path to a real support.
4. Inspect the assembly ledger: support, location, fastening, DOF, installation, removal, and tool access.
5. Exercise full travel, service positions, assembly order, and cable/keep-out volumes.
6. Review structural sections, joints, print orientation, split planes, and dominant failure modes.
7. Check hardware confidence and unresolved measurements.
8. Generate engineering views and conduct a human visual review with named findings.
9. Record evidence requests, owners, severity, and disposition. Do not silently waive a blocking issue.

## Sanity-check checklist

Look deliberately for:

- floating or visually attached components;
- disconnected structure, fake support, or a broken load path;
- inaccessible screws, bearings, inserts, cables, tools, or service parts;
- rails or bearings mounted on inadequate or discontinuous structure;
- long unsupported spans, extreme cantilevers, or implausible proportions;
- thin walls, isolated bosses, meaningless ribs, weak layer orientation, or infill-dependent strength;
- trapped hardware, impossible assembly order, bad split locations, and no replacement path;
- unnecessary mass, part count, or cosmetic complexity;
- overconstrained or underconstrained motion;
- unverified vendor models used as exact datums;
- evidence that a test passes while the design is mechanically nonsensical.

## Evidence format

Each finding should identify component/feature, view or rule, observed condition, consequence, severity, correction or evidence request, and status. Separate automated results from human review observations. Include high-quality isometric, orthographic, section, exploded, transparent, hardware-only, structure-only, and motion-extreme views as appropriate.

## Good vs bad

**Bad:** “All solids are valid, no bounding boxes overlap, therefore release.”

**Good:** Solid and clearance checks pass, then a reviewer follows the load path, attempts fastener installation, checks bearing replacement, inspects the print orientation and split, exercises motion extremes, and records the remaining physical evidence before assigning candidate or release status.

This is the downstream review gate for [mechanical-assembly-design](../mechanical-assembly-design/SKILL.md), [design-for-3d-printing](../design-for-3d-printing/SKILL.md), [motion-mechanism-design](../motion-mechanism-design/SKILL.md), and [cad-hardware-integration](../cad-hardware-integration/SKILL.md).
