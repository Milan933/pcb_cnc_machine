# Phase 1 Z error budget

This is an initial allocation for isolation routing, not a measured machine
accuracy specification. The budget separates errors that can be measured and
compensated from errors that change during cutting or cannot be inferred from
a surface map.

## Why Z matters

For a V-bit, depth changes the effective isolation width. At a 60 degree
included angle, every 0.010 mm of depth error changes the ideal width by
approximately 0.0115 mm. At a 30 degree included angle, the corresponding
change is approximately 0.0054 mm. Depth that is too shallow can leave copper;
depth that is too deep removes unnecessary FR4 and widens the isolation.

The machine therefore needs a stable mechanical Z datum even when height
mapping is available. Mapping compensates a measured board surface; it does
not compensate a spindle that deflects under cutting load, a board that moves
after probing, or a thermal shift that changes during the job.

## Initial allocation

| Error source | Initial allocation / coverage | Mapping status | Engineering treatment |
| --- | ---: | --- | --- |
| Printed structure and Z force-loop deflection at process load | 0.015 mm | Not reliably compensatable | Geometry, guide spacing, short overhang, and 5 N load test. |
| Linear-guide play or preload loss | 0.005 mm | Not compensatable | Guide selection, supported seats, preload and repeatability test. |
| Lead-screw axial play and compliance | 0.005 mm | Not compensatable | Bearing arrangement and anti-backlash strategy. |
| Spindle, collet, and tool axial seating | 0.005 mm | Not compensatable by board map | Tool-touch repeatability and axial seating/runout test. |
| Workholding distortion that changes between map and cut | 0.005 mm | Not reliably compensatable | Uniform support, controlled clamp/tape procedure, re-check. |
| Thermal drift during one job | 0.005 mm | Not reliably compensatable | Warm-up, temperature observation, or re-probe policy. |
| Spoilboard plus PCB surface variation to be covered | 0.100 mm coverage | Compensatable if stable | Map domain must cover the entire cut region and datum. |
| Conductive probe repeatability | 0.010 mm residual allocation | Measurement residual | Repeated probing test with actual clip, board, cable, and input. |
| Height-map interpolation residual | 0.010 mm residual allocation | Compensation residual | Compare 25 mm and 12.5 mm grids against independent points. |

The non-compensatable allocations sum to 0.040 mm. This is the initial
mechanical Z budget. It is not a claim that a printed PETG structure already
achieves it.

## Proposed acceptance levels

1. Static machine contribution excluding board surface variation: target
   <=0.040 mm worst-case allocation; provisional acceptance <=0.050 mm.
2. Post-map surface residual at independent check points: target <=0.020 mm;
   provisional acceptance <=0.030 mm.
3. A height map shall be rejected if probing repeatability, open-circuit
   behavior, or interpolation residual cannot be demonstrated.
4. A job shall be re-probed when the board, tape/fixture, tool, datum, or
   thermal condition changes materially.

The two levels must not be added as though every term is independent or
simultaneous. The first is the machine contribution; the second is the
remaining surface-tracking error after a valid map.

## What can and cannot be compensated

| Error | Can a surface map compensate it? | Reason |
| --- | --- | --- |
| Stable spoilboard plane error | Yes, within the measured domain | It is a repeatable spatial surface. |
| Stable PCB warp while clamped | Usually, if the board does not move after probing | Map must use the same clamping state as cutting. |
| Tape thickness or overlap | Partly, if measured and uniform | Overlap, bubbles, and local compression are not safely inferred. |
| Z guide play | No | Motion direction and load can change it. |
| Screw axial play/backlash | No | It is motion-state dependent. |
| Spindle/tool axial seating | No | It changes with tool installation and contact condition. |
| Tool-point cutting deflection | No, unless load and compliance are separately modeled | It varies with toolpath load and direction. |
| Thermal drift during a job | Not from a static map | It changes with time and spindle temperature. |
| Probe repeatability | Only statistically | It is measurement noise and must be included in residual error. |

## Requirement IDs

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-Z-001 | The initial non-compensatable Z error allocation shall be <=0.040 mm. | Preliminary |
| REQ-Z-002 | A valid height map shall reduce independent surface-check residual to <=0.020 mm target and <=0.030 mm provisional acceptance. | Preliminary |
| REQ-Z-003 | Probe repeatability, interpolation residual, tool seating, structural deflection, and board movement shall be tested as separate terms. | Known process rule |
| REQ-Z-004 | Mapping shall never be used to hide load-dependent Z deflection or an unstable workholding datum. | Known design rule |
