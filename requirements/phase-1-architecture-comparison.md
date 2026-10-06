# Phase 1 architecture-comparison requirements

Phase 1 does not select an architecture. It defines the evidence that Phase 2
must use to compare at least a moving-bed / fixed-gantry architecture with a
moving-gantry / fixed-bed architecture.

## Required comparison cases

### Case A: moving bed / fixed gantry

The study shall quantify the moving PCB/spoilboard mass, bed acceleration,
board disturbance, cable/probe routing, fixed-gantry stiffness, and access to
the workholding datum. The fixed gantry must still provide the required Z
force loop and tool-point access.

### Case B: moving gantry / fixed bed

The study shall quantify gantry span, moving spindle/Z mass, guide spacing,
torsional stiffness, fixed-bed workholding, cable routing, and access for
loading, probing, and spoilboard replacement.

### Case C: other architecture

An alternative architecture may be considered only if it offers a clear PCB
specific benefit, such as a shorter tool-point force loop or a more stable
workholding datum. It must use the same loads, working area, travel, and
printability assumptions as Cases A and B.

## Objective comparison matrix

| Criterion | Required evidence |
| --- | --- |
| Tool-point force loop | Diagram from cutter to PCB support; identify every printed joint and metal interface. |
| 5 N tool-point deflection | Static calculation and test plan in X, Y, and Z load directions. |
| Gantry torsion and pitch/yaw | Guide spacing, reaction moments, and measured or calculated tool-point angular error. |
| PCB datum stability | Workholding distortion, bed/spoilboard movement, board loading, and map validity. |
| Moving mass | Mass estimate with spindle, Z assembly, rails, cables, and board/bed where applicable. |
| Travel and edge access | Usable tool-point travel after carriage, screw, hard-stop, clamp, probe, and datum margins. |
| Rail and screw packaging | Candidate rail/screw lengths, end supports, carriage travel, coupler access, and service removal. |
| PETG printability | Largest component dimensions, orientation, joints, warping risk, and rail-seat post-processing. |
| Workholding and probing | PCB loading, conductive probe access, stowage, height-map coverage, and cable safety. |
| Footprint and service | Overall footprint estimate, maintenance access, chip extraction, and spindle cable management. |
| Controller implications | Homing, limit, probe, motor, and spindle interfaces for the same controller assumptions. |

## Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-ARCH-001 | Phase 2 shall compare moving-bed/fixed-gantry and moving-gantry/fixed-bed using the same option B working area, process loads, Z budget, and PETG print limits. | Known phase requirement |
| REQ-ARCH-002 | Each architecture shall document the complete tool-point force loop and identify load-dependent versus datum-dependent errors. | Known phase requirement |
| REQ-ARCH-003 | Each architecture shall include a workholding, spoilboard, conductive probing, and height-map concept before selection. | Known phase requirement |
| REQ-ARCH-004 | An alternative architecture shall be considered only when its PCB-specific benefit is stated and measured against the same matrix. | Known phase requirement |
| REQ-ARCH-005 | No architecture shall be selected from component availability, commonness, or cost alone. | Known project rule |
