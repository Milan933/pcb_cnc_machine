# Precision mechanical CAD anti-patterns

Use the pattern name in findings. For each occurrence record the affected feature, evidence, consequence, correction, and maturity impact.

## MAGIC BOX

- **Symptom:** A block is sized by appearance and holes are added until it looks plausible.
- **Engineering problem:** Function, datums, interfaces, and load paths are absent or hidden.
- **Detection:** No parameter or requirement explains the important dimensions.
- **Correction:** Start with requirements, frames, interfaces, loads, process, and inspection.

## FLOATING COMPONENT

- **Symptom:** A component is placed in an assembly without a real support or retention path.
- **Engineering problem:** It cannot transmit its load or remain located in the real product.
- **Detection:** Hide neighboring solids and follow the support chain; test unintended DOF.
- **Correction:** Add a seat, datum, joint, retention, and assembly/service procedure.

## VISUAL-ONLY ASSEMBLY

- **Symptom:** Solids appear together but have no explicit interfaces, constraints, or installation logic.
- **Engineering problem:** Collision-free placement is mistaken for a functioning assembly.
- **Detection:** Ask what supports, locates, fastens, moves, and removes each component.
- **Correction:** Create a component ledger, kinematic relationships, load paths, and assembly sequence.

## UNSUPPORTED RAIL

- **Symptom:** A precision rail is mounted to a thin, discontinuous, flexible, or inaccessible surface.
- **Engineering problem:** Rail stiffness cannot compensate for structural deflection or poor datum transfer.
- **Detection:** Inspect the seat in section and evaluate guide moments, fastener reactions, and tightening access.
- **Correction:** Provide a continuous supported datum, distributed fastening, alignment method, and service access.

## COUPLER-AS-BEARING

- **Symptom:** A flexible coupler is expected to carry radial, axial, or bending load.
- **Engineering problem:** Coupler deflection and reaction loads damage bearings, accuracy, or service life.
- **Detection:** Trace shaft reactions and compare them with the coupler's rated torque and misalignment behavior.
- **Correction:** Add proper radial/axial bearing supports; let the coupler transmit torque and accommodate only intended error.

## BOLTS-AS-DOWELS

- **Symptom:** Clearance-hole bolts are assumed to provide precision location or all shear transfer.
- **Engineering problem:** Joint position depends on friction, bolt bending, or uncontrolled clearance.
- **Detection:** Remove preload from the reasoning and identify the geometric locating feature.
- **Correction:** Add shoulders, keys, dowels, seats, or a justified controlled fit; use bolts primarily for clamp.

## IMPOSSIBLE FASTENER ACCESS

- **Symptom:** A screw, nut, wrench, driver, or torque tool cannot reach its joint.
- **Engineering problem:** The part cannot be assembled, torqued, inspected, or serviced.
- **Detection:** Simulate tool approach with all neighboring parts present.
- **Correction:** Reorient the joint, add clearance, change the fastener, or create a removable access path.

## TRAPPED COMPONENT

- **Symptom:** A bearing, shaft, insert, cable, or captive nut must be installed before a part that later blocks it.
- **Engineering problem:** Initial assembly or future replacement is impossible without destructive disassembly.
- **Detection:** Walk the assembly from empty frame to complete product and back through service removal.
- **Correction:** Change order, capture strategy, split plane, cover, or insertion path.

## DECORATIVE RIB

- **Symptom:** A thin rib is added for appearance but does not connect meaningful load-bearing surfaces.
- **Engineering problem:** It adds complexity or stress concentration without increasing useful stiffness.
- **Detection:** Trace the load through both rib endpoints and inspect its section/orientation.
- **Correction:** Connect a real load path with a suitable transition or remove the rib.

## ARBITRARY SPLIT

- **Symptom:** A part is split at a convenient midpoint solely because of printer or stock size.
- **Engineering problem:** The split may interrupt high moment, shear, datum, or inspection regions.
- **Detection:** Compare split location with loads, process orientation, alignment, access, and service.
- **Correction:** Move it to a low-risk inspectable region and add keyed/shouldered shear transfer and clamp.

## INFILL-AS-ENGINEERING

- **Symptom:** High infill is used to compensate for thin skins, weak layer direction, or a missing section.
- **Engineering problem:** Strength/stiffness remains process-sensitive and poorly controlled.
- **Detection:** Trace the critical load through perimeters, walls, bosses, and ribs before considering infill.
- **Correction:** Improve section geometry, orientation, local solid regions, and interfaces first.

## UNVERIFIED DIMENSION

- **Symptom:** A catalog-like or downloaded value is used as exact without a source or measurement.
- **Engineering problem:** Fit, alignment, clearance, or load claims are unsupported.
- **Detection:** Require source, revision, confidence, critical-dimension list, and physical confirmation.
- **Correction:** Mark it provisional, parameterize it, and block the relevant gate until verified.

## FALSE PRECISION

- **Symptom:** CAD decimals imply accuracy tighter than the process, material, or inspection can deliver.
- **Engineering problem:** The model communicates a false requirement and creates unpayable manufacturing expectations.
- **Detection:** Compare tolerance to process capability, thermal state, datum method, and inspection resolution.
- **Correction:** Apply functional tolerances only where needed and document the process/inspection basis.

## OVERCONSTRAINED MECHANISM

- **Symptom:** Redundant guides, bearings, mates, or locating features fight small alignment errors.
- **Engineering problem:** The mechanism binds, loads bearings, or becomes unassemblable.
- **Detection:** Count independent constraints and identify the intentional compliance or floating support.
- **Correction:** Assign locating/floating roles, adjustment, or controlled preload and verify the tolerance stack.

## UNDERCONSTRAINED MECHANISM

- **Symptom:** A body can rack, twist, separate, or drift in an unintended DOF.
- **Engineering problem:** Accuracy, safety, and load transfer are not controlled.
- **Detection:** Exercise all six relative DOF with supports and fasteners hidden.
- **Correction:** Add the missing guide, constraint, retention, preload, or hard stop.

## UNMANUFACTURABLE POCKET

- **Symptom:** A pocket has square internal corners, excessive depth, inaccessible surfaces, or no setup plan.
- **Engineering problem:** The selected tool cannot reach or produce the feature economically or accurately.
- **Detection:** Map stock, setup, cutter diameter, tool reach, corner radius, chip evacuation, and workholding.
- **Correction:** Add tool radius/relief, change dimensions, split the part, or select a justified special process.

## IMPOSSIBLE TOOL ACCESS

- **Symptom:** A cutter, drill, wrench, insert tool, or inspection probe cannot reach the feature.
- **Engineering problem:** Manufacturing, assembly, or verification cannot be completed as modeled.
- **Detection:** Use an explicit tool/inspection envelope in the relevant setup and service pose.
- **Correction:** Reorient, add an opening, alter the feature, change setup, or document special tooling.

## TOLERANCE-BY-GUESSING

- **Symptom:** A universal clearance or tight tolerance is copied from another project.
- **Engineering problem:** Process variation, material, fit, and stack-up are ignored.
- **Detection:** Ask for function, manufacturing process, mating tolerance, temperature, and inspection evidence.
- **Correction:** Derive the requirement, select a fit/tolerance system, stack it, and validate with a coupon or part.

## TESTS-PASS-THEREFORE-DESIGN-IS-GOOD

- **Symptom:** Valid solids, bounding boxes, and non-interference are treated as release evidence.
- **Engineering problem:** Mechanical nonsense can pass geometric checks.
- **Detection:** Require human load-path, assembly, manufacturing, inspection, service, and proportion review.
- **Correction:** Use the human-review gate and record named findings before advancing maturity.
