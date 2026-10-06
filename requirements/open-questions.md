# Most important unresolved engineering decisions

These questions are deliberately visible. A later phase may answer them with
analysis, a supplier data sheet, a prototype, or an experiment. Until then,
downstream CAD must not silently choose values.

## Priority 0: required before detailed motion and structural design

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

6. The original Phase 2 proposal was B, moving gantry / fixed bed. Phase 2A
   reopened the A/B comparison: which optimized PETG structure survives the
   representative tool-point, racking, creep, and datum-retention tests?
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

## Phase 1 owner disposition

The owner accepted EDR-005 on 2026-10-06. The nominal 200 x 150 mm PCB area,
0.020/0.030 mm tool-point deflection target/acceptance, 0.040 mm
non-compensatable Z allocation, and <=0.020/0.030 mm post-map residual
target/acceptance are now the Phase 2 screening baseline. They remain
unverified engineering targets.

The following questions are carried forward. They no longer block the Phase 1
gate, but they block detailed motion selection, structural release, or process
claims until they have an owner and evidence:

18. Which exact PCB stock supplier, copper weight, board thicknesses, and
    surface finish define the first physical coupon?
19. Are 0.30-1.00 mm drill tests and 0.15-0.25 mm isolation trace/space the
    intended first acceptance range, or should the process target be narrowed?
20. Is a 5 N tool-point static test load suitable for the selected tool and
    spindle, or should a measured cutting-force test replace it?
21. Which acceptance limits are release requirements and which are stretch
    targets for a first prototype?
22. Which exact controller, GRBL variant, motor models, driver current, and
    supply voltage determine achievable step rate and torque margin?
23. Which spindle supplier can document ER11 collet compatibility, runout,
    speed, mass, diameter, and thermal behavior inside the screening envelope?

## Phase 2 disposition

The owner accepted A, fixed gantry / moving Y bed, as the mechanical
architecture baseline on 2026-10-06. B, moving gantry / fixed bed, remains the
documented primary rejected alternative and must not be physically built unless
the owner reopens the architecture. The Phase 2A calculated values remain
unverified; PETG coupons and representative 5 N force-loop tests remain open.

## Phase 3 disposition boundary

The owner accepted the Phase 3 motion-class baseline under EDR-008. The
following remain open and block motion freeze, hardware-interface freeze, and
manufacturing-ready geometry, but do not reopen the accepted preliminary
Phase 4/4A architecture:

24. Which owned NEMA17 motor models, shaft lengths, rated current, holding
    torque, and torque-speed curves are available?
25. Which exact Arduino CNC Shield revision, GRBL fork, driver carrier,
    supply voltage, limit inputs, probe input, and spindle PWM path are used?
26. Which spindle defines diameter, mass, runout, cable exit, cooling, and
    ER11/tool retention?
27. Which MGN9/MGN12 supplier, preload, rail straightness, and measured rail
    seat fit will be accepted?
28. Which T8 screw straightness, end machining, nut class, preload, and wear
    results meet the <=0.030 mm backlash target?
29. Which switch/probe wiring and moving-bed cable routing preserve fault
    response and homing repeatability?
30. Do the Phase 2A PETG joints and the 1.24 kg moving-bed estimate survive
    conditioning, workholding load, and repeated motion tests?

## Phase 3A packaging disposition boundary

The owner accepted P2 as the Phase 3A packaging baseline under EDR-009. The
following packaging questions remain explicit for physical evidence and Phase
4 acceptance:

31. Does P2 retain sufficient full-travel, assembly, service, and workholding
    margin after measured hardware is installed, or is P1 needed as fallback?
32. Do the corrected P1/P2/P3 rail lengths physically clear both carriage
    blocks at every end of travel with measured supplier tolerances?
33. Does the P2 front Y motor pocket retain the calculated bed underside gap
    after the actual motor, coupler, wiring, and guard are installed?
34. Can fixed-end paired axial/angular-contact bearing cartridges be installed,
    preloaded, replaced, and kept aligned in the proposed PETG pockets?
35. Is 230 x 180 mm sufficient for the first workholding method and a future
    vacuum perimeter, or must the 240 x 190 mm P1 bed be retained?
36. Does a one-piece or near-one-piece fixed-gantry torsion box fit the Voron
    350 with its actual orientation, brim, insert, and rail-seat requirements?
37. Do exact spindle, switch, cable, and motor envelopes invalidate any P2
    clearance before manufacturing-ready structural geometry is authorized?

## PETG fastening and modularity disposition boundary

The owner-directed fastening strategy is now the working rule for Phase 3A
and Phase 4 review interfaces. These questions remain open before any reusable
interface is frozen for manufacture:

38. Which actual M3, M4, and conditionally justified M5 heat-set insert
    families will be selected, and what are their measured OD, length, pilot,
    insertion-depth, screw-clearance, and installation-tool requirements?
39. Which PETG filament, nozzle, layer orientation, perimeter count, and
    installation-temperature procedure will be used for insert pull-out,
    torque, cracking, creep, and repeated-assembly coupons?
40. Which gantry, motor, bearing, rail, and spindle joints need a through-bolt
    or metal spreader after load, preload, moment, cyclic, and failure-
    consequence review?
41. What boss wall, edge distance, and soldering-iron/tool-access acceptance
    values will replace the current preliminary interface screens?
42. Do the Phase 4 indexed splits, especially the J1 beam and 300 mm Y rail
    carriers, pass printability and service review, and where are selective
    through-bolts justified?
43. Does the complete motor, rail, carriage, screw/nut, bearing, spindle,
    limit, probe-wiring, and moving-bed service path remain replaceable without
    destroying the printed structure?

## Phase 4 structural-concept disposition boundary

The owner accepted the Phase 3 motion baseline, P2 Phase 3A packaging
baseline, and the Phase 4/4A preliminary structural architecture baseline on
2026-10-06. The following questions remain open before hardware interfaces or
manufacturing release can be accepted:

44. Which actual MGN12/MGN9 rails, T8 screws/nuts, fixed/floating bearings,
    couplers, motors, spindle, switches, probe, and fasteners fit the P2
    reference geometry after measurement?
45. Does the 29-part decomposition print on the actual Voron 2.4 350 with
    acceptable warp, bridge quality, datum conditioning, and layer-load
    orientation, especially the 300 mm Y rail carriers?
46. Does J1 deep tongue/socket outperform J2 and J3 after PETG shear, creep,
    clamp-preload, insertion, and repeated-disassembly coupons?
47. Can all printed rail seats be shimmed, skimmed, or fitted with a
    replaceable reference strip to meet parallelism and carriage-preload needs?
48. Does the moving bed retain the PCB datum and workholding under full Y
    sweep, spoilboard replacement, cable drag, and thermal conditioning?
49. Does the measured 5 N tool-point test support the separated beam,
    tower/joint, X/Z, base, rail-seat, and moving-bed compliance screen?
50. Do the measured hardware, coupons, service mock-up, and physical 5 N test
    support the O2 baseline, or require an owner-reviewed interface change
    before production CAD?

## Hardware procurement / measurement freeze

The next controlled transition is proposed in EDR-013 and detailed in
[hardware-procurement-measurement-freeze.md](hardware-procurement-measurement-freeze.md).
These questions block manufacturing-ready interfaces and Phase 5, but do not
reopen the owner-accepted O2 mass/part-count baseline:

51. Which exact MGN12/MGN9 supplier, clone grade, rail body height, hole pitch,
    end offset, carriage pattern, preload, and play meet the measured seat and
    travel requirements?
52. Are 340/310/130 mm rails available with a valid drawing, or should the
    nearest longer standard rails be retained until the final seat is measured?
53. Which T8x4/T8x2 blank or machined screw lengths, starts, end journals,
    straightness, and nuts meet the <=0.030 mm backlash target?
54. Which fixed/floating 8 mm bearing samples meet bidirectional axial
    constraint, radial support, thermal float, drag, and service requirements?
55. Which 5 mm-to-measured-journal coupler has the lowest backlash and axial
    parasitic force without sacrificing service access?
56. Which owned NEMA17 motors meet the X/Y >=0.45 N-m and Z >=0.55 N-m screens
    at the available driver current and operating speed?
57. Which Arduino CNC Shield revision, Arduino, drivers, jumpers, supply,
    spindle output, probe input, limits, cooling, and GRBL behavior are present?
58. Which M3/M4/M5 heat-set insert families pass measured geometry and PETG
    pull-out, torque, creep, deformation, and repeated-service coupons?
59. Which spindle meets the PCB isolation/drilling/outline specification and
    what mount adaptation is needed if its body is not within the 52 mm screen?
60. Which spoilboard material and workholding method preserve the 230 x 180 x
    12 mm replaceable process datum under board load and resurfacing?
61. Does the full measured assembly retain rail/screw/bearing/motor/spindle/
    limit/probe/cable access throughout X/Y/Z travel and service sequence?
62. Does the separated measured 5 N tool-point test support the analytical
    screen without treating 0.009410 mm as measured machine performance?
