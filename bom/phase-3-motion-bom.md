# Phase 3 preliminary motion BOM

**Status:** review BOM / sample characterization only
**Decision record:** [EDR-008](../docs/decisions/008-phase-3-motion-system.md)

This is a component-class BOM, not a production purchasing release. “Sample
only” means one representative item may be bought for measurement/coupons;
final quantity, supplier, preload, length, and fit remain open.

| Item | Qty in reference layout | Preliminary class / envelope | Status | Purchase boundary / evidence |
| --- | ---: | --- | --- | --- |
| X linear rail | 2 | MGN12H class, 300 mm reference | sample only | Measure straightness, preload, rail width, hole pattern, and seat fit before final length. |
| X long carriage block | 4 | MGN12H class, two per rail | sample only | Verify block play, drag, preload, and actual mounting face. |
| Y linear rail | 2 | MGN12H class, 280 mm reference | sample only | Moving-bed datum; verify parallelism and PETG-seat coupon. |
| Y long carriage block | 4 | MGN12H class, two per rail | sample only | Verify carriage play and bed pitch/racking after preload. |
| Z linear rail | 2 | MGN9H class, 100 mm reference | sample only | MGN12H is the stiffness fallback; measure short-Z play and seat fit. |
| Z long carriage block | 4 | MGN9H class, two per rail | sample only | Verify tool-point moment response; do not substitute one rail as baseline. |
| X lead screw | 1 | T8x4, 300 mm reference span | sample only | Final cut/end machining and straightness are not frozen. |
| Y lead screw | 1 | T8x4, 280 mm reference span | sample only | Final length depends on bearing/support packaging. |
| Z lead screw | 1 | T8x2, 120 mm reference span | sample only | Test gravity hold, power-off descent, and axial play. |
| Anti-backlash nut | 3 | Adjustable split/dual brass; polymer alternative | sample only | X/Y default; Z only after drag and wear test. |
| Fixed screw support | 3 axis sets | Paired angular-contact or BK08-class, 8 mm bore | sample only | Fixed end carries axial load; exact block and fit are open. |
| Floating screw support | 3 | BF08-class radial support, 8 mm bore | sample only | Radial-only support with axial float. |
| Flexible coupler | 3 | 5 mm motor to 8 mm screw | sample only | Torque transmission only; never an axial bearing. |
| NEMA17 motor | 3 | 42.3 mm square, 40-48 mm body, 5 mm shaft | owner-owned / identify first | Record model, current, torque-speed curve, shaft length, and condition. |
| Driver carrier | 3 | A4988 or DRV8825 candidate | owner-owned / identify first | Verify carrier cooling/current limit; start at 8 microsteps. |
| GRBL/CNC Shield controller | 1 | GRBL 1.1-compatible, exact revision open | owner-owned / identify first | Verify STEP/DIR, limits, probe, spindle enable/PWM, supply, and firmware. |
| Home/limit switch | 6 nominal | One home and one opposite hard limit per axis | do not buy final set | Board pin behavior and switch type/wiring remain open; NC is preferred if supported. |
| Conductive probe / touch plate | 1 | Fault-detectable probe input | do not buy final unit | Verify electrical noise margin, open-circuit fault response, and map workflow. |
| Spindle | 1 | ER11-compatible screening envelope, approx. 52 mm diameter x 120 mm length | do not buy final unit | Measure diameter, mass, runout, cable exit, cooling, and mounting interface first. |
| PCB bed / spoilboard | 1 set | 240 x 190 mm moving support; 200 x 150 mm PCB area | structural design deferred | No production PETG geometry in Phase 3; retain 20 mm edge margin. |

The guideway capacity and moment reference comes from the
[official HIWIN MGN/MGW catalog](https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E-2.pdf).
Driver capability must be checked against the identified carrier using the
[Allegro A4988 documentation](https://www.allegromicro.com/en/products/motor-drivers/brush-dc-motor-drivers/a4988)
or the [TI DRV8825 datasheet](https://www.ti.com/lit/ds/symlink/drv8825.pdf),
not from the class name alone.
