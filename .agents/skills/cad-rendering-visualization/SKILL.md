---
name: cad-rendering-visualization
description: Produce deterministic engineering CAD views that expose support, interfaces, load paths, assembly order, motion, service access, and manufacturing risks rather than beauty renders.
---

# CAD rendering and visualization

Use this skill to create review images or interactive scenes for mechanical design. A render is an inspection instrument: every view should answer an engineering question.

## Required view selection

Choose views from the risks and interfaces, not from a fixed presentation template. Typical views include:

- clear front/rear/side/top isometrics for overall support and proportion;
- orthographic views for alignment, envelope, and datum relationships;
- sections or clipping for hidden seats, bosses, bearings, inserts, and load paths;
- exploded views for assembly order and trapped hardware;
- transparent overlays for clearance, cable, and motion envelopes;
- structure-only and hardware-only views for support and interface review;
- closeups of fasteners, rail seats, bearings, shafts, motor mounts, and service access;
- minimum/maximum travel and collision-extreme views.

## Visual grammar

Use stable camera locations and visually distinct classes for structure, moving parts, standard hardware, reference envelopes, cables, and clearance volumes. Include labels or a legend when color alone is ambiguous. Do not hide questionable geometry with clipping, dark shading, or an attractive camera angle.

When a feature is provisional or unverified, show that status in the manifest or view annotation. A transparent envelope must not read like a solid support. A hidden fastener must be exposed in at least one installation view.

## Deterministic review package

Record model revision, units, camera/view name, display mode, section/clip settings, and the question each image answers. Generate the same named view set from the same source revision so changes can be compared. Use explicit tessellation and export settings for mesh derivatives; preserve the parametric model as the authority.

## Good vs bad

**Bad:** One polished isometric image with all hardware the same color and hidden interfaces.

**Good:** A small, repeatable review set shows the rail support section, motor installation path, bearing reaction, fastener access, hardware-only interfaces, structure-only load path, and motion extremes, with provisional items visually distinguishable.

Use [cad-design-review](../cad-design-review/SKILL.md) to decide which views are evidence rather than presentation.
