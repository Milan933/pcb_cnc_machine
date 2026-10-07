---
name: cad-conventions
description: Apply the PCB-CNC-specific parametric CAD architecture, coordinates, naming, reusable interfaces, assembly placement, and STEP/STL export conventions after the generic mechanical CAD method is loaded.
---

# CAD conventions

Use this skill whenever creating or reviewing CAD source, a part module, an
assembly, an export script, or a geometry-facing validation adapter.

## Scope and dependency boundary

This is a PCB-CNC overlay, not the generic mechanical design method. Load
`.agents/skills/mechanical-cad-design/SKILL.md` for function-to-geometry,
datums, load paths, and feature reasoning; load the generic assembly, FDM,
joint, hardware, motion, rendering, and review skills as needed. The rules
below preserve this project's coordinate, source-layout, naming, export, and
owner-hardware conventions.

## Technology direction

The current preliminary recommendation is build123d, pending the
implementation spike in EDR-002. Keep the CAD architecture independent
enough that a CadQuery adapter remains possible until the recommendation is
approved.

The source of truth is parametric solid geometry. STL is a manufacturing
derivative and must never be edited as the authoritative model.

## Coordinate convention

Use millimeters internally and document units at every external interface.
The global direction convention is:

- X: left to right, positive to the right when facing the machine;
- Y: front to back, positive toward the rear;
- Z: down to up, positive upward from the workholding reference plane.

The final machine-origin location, bed datum, and homing offsets are
controlled parameters that must be selected in architecture. Do not invent
their physical placements inside a part module.

Each part and assembly instance must document its local frame, datum face,
positive axes, and placement relative to the global frame.

## Source layout

Keep responsibilities separate:

- cad/parameters.py: centralized project and interface parameters;
- cad/parts: individual parametric printable or structural parts;
- cad/hardware: controlled hardware envelopes and interfaces;
- cad/assembly: deterministic instance placement and assembly metadata;
- cad/validation: geometry-independent and geometry-aware checks;
- cad/export: reproducible export and manifest generation.

Part modules should build geometry, not perform hidden exports or mutate global
state on import. Export functions should be explicit and deterministic.

## Parameter discipline

Every important dimension must come from the central parameter model or a
part-specific interface parameter that is documented and traceable. Avoid
duplicating a dimension in multiple modules. If two interfaces intentionally
use different values, give them different names and record why.

Tag values as known, assumed, preliminary, calculated, or experimentally
verified in documentation. Do not give an unresolved dimension fake precision
just because a CAD API accepts a decimal.

## Part and assembly naming

Use stable, meaningful names based on function, for example:

- printed_frame_base;
- printed_gantry_beam;
- z_carriage;
- x_rail_left;
- spindle_mount;
- pcb_spoilboard.

Names must not encode a temporary layout choice or an unrecorded supplier
part number. Assembly instances must be uniquely identifiable and placements
must be deterministic across runs.

## Reusable interfaces

Create reusable functions for:

- mounting-hole patterns;
- rail and carriage interfaces;
- screw-support interfaces;
- motor mounting patterns;
- insert and captive-nut pockets;
- standard fastener envelopes;
- datums and reference frames.

An interface function must state its coordinate assumptions, clearances,
fastener access, and which values are controlled by parameters. Avoid copying
hole coordinates by hand across part modules.

For PETG reusable joints, use a parameterized heat-set insert interface with
fields for nominal size, insert outer diameter, insert length, pilot-hole
range, insertion depth, surrounding boss wall, edge distance, insertion
direction, screw clearance, and soldering-iron or insertion-tool access. The
actual supplier dimensions may be unresolved in a review envelope, but the
interface must report that not-ready state rather than inventing exact pilot
values. The default size hierarchy is M3 for small/accessory hardware, M4 for
general structural/module joints, and M5 only with a documented technical
justification.

Every important joint must separately identify the preload fastener and the
printed geometric load-transfer feature. Use shoulders, steps,
tongue-and-grooves, keys, pockets, bosses, registration, shear keys, mating
faces, or interlocking ribs for location and shear. Through-bolts are a
selective escalation for insert pull-out/creep, high preload or moment,
cyclic loading, or high failure consequence; they still require a geometric
shear path and must not be treated as precision locating pins by default.

The fixed gantry crossmember interface must be modeled as a mechanically
seated joint with a deep tongue-and-groove, stepped socket, keyed pocket,
shoulder, or interlocking rib. Do not model it as a plate suspended from M5
screws. Keep these reusable interface concepts centralized so Phase 3A
packaging, future printed parts, and validation consume the same contract.

## Hardware representations

Represent standard hardware with enough geometry for clearance, access,
collision, and load-path review. Link the representation to a supplier or
specification when selected. An envelope may be used during early trade
studies, but it must be marked as an envelope and must not be mistaken for a
verified model.

## Assembly and exports

The assembly module owns placement, labels, colors if useful, and part
relationships. Avoid fusing parts in the authoritative assembly when doing so
would hide service boundaries, interfaces, or collision evidence.

The export layer must be able to produce:

- a complete assembly STEP;
- individual printable-part STEP;
- individual printable-part STL;
- a reviewed export manifest with source revision, parameters, CAD version,
  units, and validation status.

STL tessellation settings must be explicit and appropriate to the feature
size. Export must refuse or clearly mark outputs when blocking validation
errors exist.
