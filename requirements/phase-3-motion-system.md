# Phase 3 motion-system requirements and screening baseline

This document records the owner-accepted Phase 3 screening baseline for the
accepted **Architecture A: fixed gantry with moving Y bed**. It selects
component classes for a review layout; it does not freeze a supplier, preload,
exact length, spindle, motor, controller revision, or printed interface.

## Owner boundary

The 200 x 150 mm PCB process area and the Architecture A force loop are the
baseline. The screened tool-point travel remains 220 x 170 x 40 mm and may be
refined only with an impact review that preserves the usable PCB area and
clamp/probe access. Phase 2A analytical values remain calculated, not
measured. The representative PETG coupons and the 5 N force-loop evidence
remain required.

## Motion requirements

| ID | Requirement | Status | Evidence / next action |
| --- | --- | --- | --- |
| REQ-MOT3-001 | Use a fixed PETG gantry, moving Y PCB bed, X moving spindle/Z carriage, and short Z axis. | Owner decision / preliminary architecture | EDR-006 owner disposition and EDR-008 proposal. |
| REQ-MOT3-002 | Preserve 200 x 150 mm usable PCB area with a nominal 20 mm bed edge margin on both axes. | Preliminary choice | Bed layout and workholding mock-up. |
| REQ-MOT3-003 | Preserve screened tool-point travel of 220 x 170 x 40 mm unless an owner-reviewed packaging change records the impact. | Preliminary choice | Motion skeleton and measured end-stop layout. |
| REQ-MOT3-004 | X and Y use separated dual MGN12-class rails with two long blocks per rail in the reference layout. | Preliminary choice | Rail sample measurement, seat coupon, and 5 N force-loop test. |
| REQ-MOT3-005 | Z uses separated dual MGN9-class rails with two long blocks per rail in the reference layout; MGN12 is the stiffness fallback. | Preliminary choice | Short-Z guide play and tool-point deflection test. |
| REQ-MOT3-006 | X and Y use T8x4 lead class; Z uses T8x2 lead class. | Preliminary choice | Motor torque-speed and whip/straightness test. |
| REQ-MOT3-007 | Each screw has a defined fixed end, floating end, axial bearing strategy, nut strategy, and serviceable coupler. | Known design rule / preliminary implementation | Bearing and nut inspection plus axial-play/backlash test. |
| REQ-MOT3-008 | Couplers transmit torque and angular misalignment only; they shall not carry screw axial load. | Known design rule | Assembly inspection and axial-load test. |
| REQ-MOT3-009 | Provisional X/Y backlash target is <=0.030 mm, with <=0.050 mm as the Phase 1 acceptance limit. | Preliminary requirement | Reversal measurement before and after cycling. |
| REQ-MOT3-010 | Preliminary structural CAD shall use a standardized common NEMA17 interface: approximately 42.3 mm mounting square, screening 5 mm shaft, 40-48 mm body envelope, and rear connector/wiring access. Final axis motors must be identified and characterized before manufacturing release. | Owner direction / preliminary interface | Record each owner-supplied motor and torque-at-speed/current evidence; exact final motor selection does not block the preliminary structural envelope. |
| REQ-MOT3-011 | Start at 8 microsteps per full step; use 16 or 32 only after the installed driver module, current, heat, missed-step, and command-rate behavior are verified. | Preliminary controller strategy | Identify the installed carrier and jumper state; do not assume an A4988/DRV8825 module. |
| REQ-MOT3-012 | The owner-supplied Arduino Mega + CNC Shield shall use a verified GRBL-compatible configuration exposing independent steps/mm, max rate, acceleration, homing, limits, probe, and spindle settings. | Known platform / unresolved implementation | Verify exact Shield revision, firmware fork, installed drivers, pin map, and I/O behavior. |
| REQ-MOT3-013 | Home X left/negative, Y front/negative, and Z up/positive; moving-bed Y semantics must be stated in machine and work coordinates. | Preliminary control strategy | Switch placement, homing repeatability, and fault-response test. |
| REQ-MOT3-014 | Motion packaging shall include screw supports, couplers, motors, cable/probe routing allowance, bed support, spoilboard, and a generic spindle envelope. | Preliminary packaging | Review-only build123d motion skeleton and measured hardware. |
| REQ-MOT3-015 | No detailed structural CAD or manufacturing export may depend on an unmeasured rail, screw, spindle, motor, controller, or nut dimension. | Known project rule | Phase 4/5 review and purchase gate. |

## Evidence status

The equations, parameter integrity checks, and nominal motion-layout skeleton
are complete. The Phase 3 gate is intentionally **not ready** until
representative owner motors and the Arduino Mega + CNC Shield assembly are
identified, installed drivers are verified, representative motion hardware is
measured, the PETG rail-seat/joint coupons are evaluated, and the motion tests
listed in `cad/parameters.py` are recorded. The owner accepted the motion
baseline on 2026-10-06; this is not a claim of machine accuracy or measured
motion performance. Phase 4 may use the generic NEMA17 interface as a
preliminary reference, but may not freeze supplier-dependent geometry.
