# Generic mechanical CAD skill framework

This framework is the reusable mechanical-design layer for Codex in this repository. It applies to machines, fixtures, robots, printer parts, enclosures, mechanisms, brackets, structural assemblies, and workshop tools. It does not assume a PCB CNC, a particular material, or build123d.

## Skill stack

| Skill | Role | Depends on |
| --- | --- | --- |
| `mechanical-cad-design` | Function-to-geometry method, datums, interfaces, load paths, parametric feature hierarchy | none; foundation |
| `mechanical-assembly-design` | Support, location, fastening, DOF, assembly order, service, and load-chain reasoning | mechanical-cad-design |
| `design-for-3d-printing` | Functional FDM orientation, section design, supports, tolerance, splits, and inspection | mechanical-cad-design |
| `mechanical-joints-fasteners` | Preload, shear, tension, bending, inserts, bolts, keys, and joint access | mechanical-cad-design; design-for-3d-printing when polymer is involved |
| `motion-mechanism-design` | Guides, shafts, bearings, transmissions, actuators, constraints, limits, and motion envelopes | mechanical-cad-design; mechanical-joints-fasteners where joints carry motion loads |
| `cad-hardware-integration` | Hardware provenance, confidence, interface/envelope models, stable IDs, and persistent libraries | mechanical-cad-design; mechanical-assembly-design |
| `cad-rendering-visualization` | Engineering views for hidden interfaces, assembly, motion, clearance, and support review | mechanical-cad-design; mechanical-assembly-design |
| `cad-design-review` | Human review gate combining automated checks with engineering sanity checks and evidence | all applicable domain skills; cad-rendering-visualization |

## Dependency graph

```text
                         mechanical-cad-design
                       /          |            \
                      /           |             \
 design-for-3d-printing   mechanical-assembly-design   cad-hardware-integration
             |                    |          \             |
             v                    v           \            v
 mechanical-joints-fasteners  motion-mechanism-design  cad-rendering-visualization
                                      \          /             |
                                       \        /              |
                                        v      v               |
                                      cad-design-review <------+
```

The graph is a loading guide, not a requirement to load every skill for every task. Start with the foundation, add only the branches the design needs, and always add design review before a readiness or release claim.

## Cross-skill workflow

```text
REQUIREMENTS
  ↓
MECHANICAL LAYOUT
  ↓
HARDWARE / INTERFACE DEFINITION
  ↓
MASTER GEOMETRY
  ↓
ASSEMBLY / CONSTRAINTS
  ↓
LOAD-PATH REVIEW
  ↓
MOTION REVIEW
  ↓
MANUFACTURING DESIGN
  ↓
DFM / FDM REVIEW
  ↓
ASSEMBLY REVIEW
  ↓
ENGINEERING VISUAL REVIEW
  ↓
EXPORT
  ↓
PHYSICAL PROTOTYPE
  ↓
MEASUREMENT
  ↓
REVISION
```

No downstream stage may silently compensate for an invalid upstream datum, interface, load path, motion constraint, or manufacturing assumption. Each stage should leave an explicit decision, assumption list, and evidence request.

## Existing project skills

The existing skills remain useful, but they sit above this generic layer:

| Existing skill | Classification | Boundary after this framework |
| --- | --- | --- |
| `cad-conventions` | REFACTOR / CNC-SPECIFIC OVERLAY | Keeps repository layout, machine coordinates, naming, build123d/export conventions, and CNC interfaces; generic geometry method lives in `mechanical-cad-design`. |
| `design-validation` | REFACTOR / CNC-SPECIFIC OVERLAY | Keeps CNC travel, spindle, PCB, PETG, and manufacturing gate rules; generic review and fail-closed evidence rules live in `cad-design-review`. |
| `motion-system-design` | REFACTOR / CNC-SPECIFIC OVERLAY | Keeps CNC axis, NEMA17, screw, limit, and homing requirements; generic mechanism reasoning lives in `motion-mechanism-design`. |
| `pcb-cnc-architecture` | KEEP / CNC-SPECIFIC OVERLAY | Remains the PCB process, force-loop, workholding, probing, and height-map architecture layer. |
| `printed-structural-design` | REFACTOR / CNC-SPECIFIC OVERLAY | Keeps PETG machine structure, rail, gantry, print-volume, and CNC service constraints; generic FDM and joint reasoning lives in the generic skills. |
| `repository-workflow` | KEEP | Remains repository/publication policy and is orthogonal to mechanical reasoning. |

Refactoring means clarifying boundaries and references, not deleting project evidence or silently changing the CNC design.

## Use with CAD backends

The reasoning contracts are backend-independent: a local frame, datum, interface, constraint, load path, representation confidence, and evidence record must exist regardless of whether the implementation uses build123d, CadQuery, FreeCAD, Fusion, Onshape, or another CAD system. The backend adapter should provide named solids, transforms, reference geometry, assembly instances, exports, and measurable feature metadata.

For build123d, use local `Plane`/`Axis`/`Location` frames, reusable builders, explicit placements, centralized parameters, named parts, and explicit STEP/STL exports. Do not make build123d syntax the engineering method.

## Later CNC application

When the CNC redesign resumes, load `mechanical-cad-design`, `mechanical-assembly-design`, `design-for-3d-printing`, `mechanical-joints-fasteners`, `motion-mechanism-design`, `cad-hardware-integration`, and `cad-design-review` as required, then add the existing CNC overlays. Begin again at requirements, datums, hardware interfaces, and force-loop layout. Do not reuse current geometry merely because it passes a solid or bounding-box test.
