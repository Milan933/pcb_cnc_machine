# Generic mechanical CAD anti-pattern catalog

Use these names in reviews and validation findings. Each finding should identify the affected component, evidence view or calculation, consequence, correction, and status.

## FLOATING COMPONENT

- **Symptom:** A component is positioned in the assembly but has no support, locating feature, or fastening relationship.
- **Why/detect:** Follow the support chain and attempt to move the component; a visual overlap is not a connection.
- **Correction:** Add a real seat, interface, retention method, and assembly/service sequence, or remove the component from the production-intent assembly.

## MAGIC BOX

- **Symptom:** A block is sized approximately and holes are added until the layout looks plausible.
- **Why/detect:** No function, datum, interface, load, or parameter explains the dimensions.
- **Correction:** Start from requirements, functional frames, envelopes, load paths, and named feature parameters.

## DECORATIVE RIB

- **Symptom:** A thin rib is added for a stronger appearance but does not connect load-bearing skins or close a shear path.
- **Why/detect:** Remove the rib mentally or trace force flow through its endpoints; no meaningful reaction or section change is present.
- **Correction:** Connect it to real load-bearing geometry with a suitable section and transition, or delete it.

## BOLTS-AS-DOWELS

- **Symptom:** Fastener shanks are expected to establish precision location under load without a locating strategy.
- **Why/detect:** Joint position depends on clearance holes, friction, or bolt bending instead of a shoulder, key, dowel, or controlled datum.
- **Correction:** Separate preload from location and design explicit shear/registration geometry or a justified precision fit.

## IMPOSSIBLE FASTENER

- **Symptom:** A screw, nut, wrench, or driver cannot reach its interface in the assembly or service pose.
- **Why/detect:** Animate the tool approach and tightening sequence with neighboring solids present.
- **Correction:** Reorient the fastener, add access, change the joint or assembly order, or make the obstruction removable.

## TRAPPED HARDWARE

- **Symptom:** A bearing, nut, insert, shaft, cable, or captive component must be installed before a later part that permanently blocks it.
- **Why/detect:** Simulate build and replacement order from an empty frame and from the service state.
- **Correction:** Provide a removable cover, capture feature, insertion path, split, or different assembly sequence.

## UNSUPPORTED RAIL

- **Symptom:** A guide or precision rail is mounted on a thin, discontinuous, flexible, or inaccessible surface.
- **Why/detect:** Inspect the rail seat in section, check fastener reactions and guide moments, and inspect tightening access.
- **Correction:** Provide a continuous datum shoulder and supported mounting surface, distribute reactions, and define alignment/service access.

## COUPLER-AS-BEARING

- **Symptom:** A flexible shaft coupler is expected to carry radial, axial, or bending loads not supported by bearings.
- **Why/detect:** Trace every shaft reaction and compare it with the coupler’s specified misalignment and load capability.
- **Correction:** Add or redesign bearing supports; let the coupler transmit torque and accommodate only its intended misalignment.

## VISUAL-ONLY ASSEMBLY

- **Symptom:** Solids appear assembled, but there are no constraints, interfaces, load paths, installation rules, or service evidence.
- **Why/detect:** Hide structure and hardware in turn, attempt to remove a component, and ask what actually locates it.
- **Correction:** Create an assembly ledger and explicit support, location, fastening, DOF, and access contracts.

## TEST-PASSES-SO-DESIGN-IS-GOOD

- **Symptom:** Valid solids, bounding boxes, and non-interference are treated as release evidence.
- **Why/detect:** Ask whether a human has reviewed load paths, fastener access, proportions, motion, process orientation, and maintenance.
- **Correction:** Add a human-review gate with engineering views, named findings, and physical evidence requests.

## ARBITRARY SPLIT PLANE

- **Symptom:** A large printed part is split at a convenient or visually centered plane without structural reasoning.
- **Why/detect:** Compare the split with bending moment, shear transfer, datum continuity, print orientation, and assembly access.
- **Correction:** Move the split to a low-risk, inspectable region and add keys, shoulders, shear transfer, clamping, and alignment evidence.

## INFILL-AS-STRUCTURE

- **Symptom:** More infill is used to compensate for weak walls, poor layer orientation, or a missing section/load path.
- **Why/detect:** Inspect perimeter paths and the critical load route; if the interface depends on sparse interior material, the design is process-fragile.
- **Correction:** Improve section geometry, skins, ribs, bosses, orientation, and local solid regions before selecting infill.

## UNVERIFIED-VENDOR-MODEL

- **Symptom:** A downloaded CAD model is used as an exact interface or datum without provenance or dimensional checks.
- **Why/detect:** Ask for source, license, revision, critical dimensions, and measured confirmation.
- **Correction:** Classify confidence, use only verified interfaces, or create a local parametric envelope/interface model with a stable ID.

## OVERCONSTRAINED MOTION

- **Symptom:** Multiple guides, bearings, shafts, or mates fight small alignment errors and bind.
- **Why/detect:** Count constraints and identify which support accommodates parallelism, thermal growth, and assembly variation.
- **Correction:** Assign locating/floating roles, add adjustment or compliance intentionally, and validate the full tolerance stack.

## UNDERCONSTRAINED MOTION

- **Symptom:** A moving member can rack, twist, drift, separate, or rotate in an unintended DOF.
- **Why/detect:** Exercise the mechanism with supports and fasteners hidden; inspect all six relative DOF and end stops.
- **Correction:** Add the missing guide, constraint, retention, preload, or hard stop and document the intended DOF.

## DATUM DRIFT

- **Symptom:** Critical features are chained from arbitrary transient faces or changing cosmetic geometry.
- **Why/detect:** Regenerate or revise a feature and observe whether interfaces move without a requirement changing.
- **Correction:** Anchor interfaces to named functional datums, symmetry, axes, or master-layout references.

## TOLERANCE HOPE

- **Symptom:** Exact CAD dimensions are expected to make printed or assembled parts fit without process evidence.
- **Why/detect:** No tolerance stack, material/process assumption, calibration coupon, or measurement plan exists.
- **Correction:** Assign tolerances by process and feature, print a representative coupon, measure, and revise the controlled parameter.
