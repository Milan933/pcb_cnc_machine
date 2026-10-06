# Engineering decision record: initial skill-set review

- **Record ID:** EDR-003
- **Phase:** Foundation / preparation for Phase 1
- **Status:** accepted for review
- **Date:** 2026-10-06
- **Owner:** project team
- **Affected requirements:** REQ-FN-001 through REQ-VAL-003

## Decision

The five initial skills are internally consistent enough to guide the next
engineering phase. Their boundaries are retained, with the missing
engineering inputs below tracked as unresolved rather than filled with
invented dimensions.

## Contradiction review

| Topic | Finding | Resolution |
| --- | --- | --- |
| PCB-specific priorities vs printed PETG frame | No contradiction. The architecture skill sets process priorities; the structural skill defines how the required frame is made. | Keep both. Tool-point stiffness and datum stability drive structural geometry. |
| Metal components vs predominantly printed structure | No contradiction. Metal is allowed at rails, bearings, screws, spindle, and fastener interfaces when the load path justifies it. | Require a load-path reason in the relevant decision record. |
| build123d recommendation vs CadQuery fallback | No contradiction. The CAD convention is backend-independent until the implementation spike. | Keep build123d as preliminary and CadQuery as fallback. |
| Coordinate convention | The five skills and AGENTS.md agree on X right, Y rear, and Z up. | Physical origin and homing datum remain explicitly unresolved. |
| Validation strictness vs early-stage geometry absence | No contradiction. Validation marks missing evidence not-ready; it does not claim detailed geometry is validated. | Keep foundation checks separate from future CAD-adapter checks. |

## Missing or controlled constraints

The skills do not silently decide the following items:

- exact spindle, tool, collet, runout, mass, cable, and thermal inputs;
- exact owned motor models and controller / GRBL capabilities;
- process acceptance values for isolation depth, hole size, repeatability,
  tool-point deflection, and spindle runout;
- PCB size/thickness range, registration, clamp method, spoilboard datum, and
  probing hardware;
- rail, screw, bearing, anti-backlash, and coupler selections;
- PETG print process, usable printer margins, tolerances, creep tests, and
  insert/fastener coupon results;
- dust extraction, guarding, electrical, emergency-stop, and spindle safety
  interfaces;
- final machine origin, homing offsets, and height-map storage/application
  ownership.

These are recorded in requirements/open-questions.md or are identified as
future evidence in the workflow. They are not missing by accident.

## Risks and mitigations

| Risk | Consequence | Mitigation / evidence needed | Owner |
| --- | --- | --- | --- |
| A future part module bypasses the central parameter and interface rules. | CAD becomes non-deterministic and validation loses traceability. | Review every module against cad-conventions and add a smoke test for parameter propagation. | project team |
| Printed structural guidance is interpreted as a fixed wall or infill recipe. | Weak or overbuilt parts result. | Require load-path calculations and process-specific print evidence for each primary part. | project team |
| Safety is treated as outside mechanical architecture. | Spindle and FR4 dust hazards are discovered late. | Add safety interfaces and a risk review before complete assembly release. | project team |

## Validation and review

- [x] All five SKILL.md files pass the skill-authoring validator.
- [x] Coordinate and status conventions cross-checked.
- [x] Missing inputs recorded as unresolved.
- [x] Foundation tests pass.
- [ ] Project owner reviews and accepts the skill set.

## Follow-up

Use the open questions as the Phase 1 input list. Update this record if a
future decision exposes a genuine rule conflict or changes the release
boundary.
