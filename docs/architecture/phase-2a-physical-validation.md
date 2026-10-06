# Phase 2A physical validation plan

**Status:** required evidence before architecture freeze
**Boundary:** representative coupons and frame interfaces only; no production
part release

## Measurement rules

Every coupon record shall identify filament batch, nozzle and layer process,
perimeter/wall count, print orientation, support and bed-contact strategy,
conditioning time and temperature, insert/bolt hardware, tightening torque,
load direction, instrument, resolution, uncertainty, and permanent-set
inspection. Record loading and unloading so elastic stiffness is separated
from slip and creep.

## Coupon set

| Coupon | Purpose | Minimum measurement |
| --- | --- | --- |
| Beam bending | Fit effective `EI` and joint compliance for A/B deep sections | 5 N and 10 N tool-point displacement, load/unload, residual set |
| Torsion box | Fit effective `GJ` and roll response | known torque/couple, angular twist, pre/post conditioning |
| Rail seat | Measure datum deformation and load spreading | rail movement under lateral force and moment after representative torque |
| Heat-set insert | Measure preload loss and insert rotation/pull behavior | torque/projection/datum at 0, 1, 7, 30 days and temperature |
| Through-bolt joint | Measure clamp relaxation and slip | clamp length, slip, rail datum after thermal and cyclic loading |

## Representative A/B test

After coupons, build one representative A and one representative B force-loop
assembly with the proposed guide spacing, spindle envelope, tool overhang,
workholding, probe/cable state, and structural interfaces. Apply 5 N in X, Y,
and Z at the tool point. Measure direct displacement, roll/pitch/yaw, rail
datum movement, and any board/workholding movement. Repeat after conditioning
and after representative low-acceleration Y cycles.

The A test must include a probe-to-cut movement-state check because its PCB
datum travels with the bed. The B test must include differential side-force
and gantry-racking measurements because its fixed bed can otherwise make a
moving-gantry error look like a stable process datum.

## Feedback gate

Replace the Phase 2A equivalent inputs with fitted values, rerun the analytical
study, and update the matrix. A target miss, permanent datum shift, preload
loss, unexpected racking, or unacceptable board movement reopens the A/B
decision. A height map cannot compensate for load-dependent machine movement,
backlash, spindle seating error, or fixture slip.

No architecture freeze is allowed until the owner has reviewed the updated
calculation, physical measurements, and the remaining spindle/motion/process
choices.
