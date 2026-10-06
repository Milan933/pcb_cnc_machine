# Most important unresolved engineering decisions

These questions are deliberately visible. A later phase may answer them with
analysis, a supplier data sheet, a prototype, or an experiment. Until then,
downstream CAD must not silently choose values.

## Priority 0: required before detailed architecture

1. What spindle and tool family will be used first? Required inputs include
   nose geometry, collet or chuck, runout specification, mass, cable exit,
   cooling, speed range, and mounting interface.
2. Which owned NEMA 17 motors are available, and what are their rated current,
   holding torque, torque-speed curves, shaft dimensions, and condition?
3. What controller and GRBL variant are present? Confirm stepper-current
   capability, available axes, limit inputs, probe input, spindle control, and
   firmware travel / homing behavior.
4. What PCB size range, thickness range, panelization method, and reference
   datum must work? Include sacrificial spoilboard replacement and probing
   access.
5. What accuracy, repeatability, tool-point deflection, runout, and hole-size
   acceptance values are required for the intended PCB processes?

## Priority 1: motion and structure

6. Which axis arrangement produces the shortest Z force loop while keeping the
   printable frame aligned and serviceable?
7. Should each axis use MGN9, MGN12, another rail family, or a different
   supported guide? Compare section stiffness, carriage capacity, preload,
   rail mounting, contamination tolerance, cost, and availability.
8. Should each screw use T8x2, T8x4, another lead, or a different transmission?
   Compare resolution, speed, self-locking tendency, critical speed, backlash,
   and motor torque margin.
9. What anti-backlash strategy is acceptable over the machine's expected
   service life, and how will preload be maintained as PETG creeps?
10. Which interfaces must use through-bolts or metal brackets instead of
    inserts or captive nuts?
11. What thermal and vibration environment will the spindle create near the
    PETG frame?

## Priority 2: process and manufacturing

12. What probing hardware and electrical reference method will be used?
13. How will PCB height maps be acquired, stored, transformed, and applied in
    the toolpath workflow?
14. What minimum wall thickness, edge distance, hole clearance, and insert
    pull-out test values will be accepted for printed parts?
15. What PETG filament, nozzle, layer height, perimeter count, print
    orientation, annealing or conditioning policy, and environmental limits
    will be used?
16. What parts can be printed in one piece on the Voron 2.4 350, and where are
    joints acceptable without losing alignment?
17. What maintenance, cleaning, chip extraction, and spindle-cable management
    provisions are required?

## Decision discipline

Each answer must be added to a requirement baseline or an engineering
decision record. If a question remains open, its consequence must remain
visible in the architecture and validation report.
