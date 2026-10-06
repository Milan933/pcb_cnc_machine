# Engineering decision record: Phase 3A compact packaging

- **Record ID:** EDR-009
- **Phase:** 3A - compact packaging optimization
- **Status:** owner-accepted P2 packaging baseline; physical evidence open
- **Date:** 2026-10-06
- **Owner:** project owner / project team
- **Architecture input:** EDR-006 and EDR-007; Architecture A remains the baseline
- **Motion input:** EDR-008; component classes remain the current technical baseline

## Owner-accepted packaging baseline

Carry **P2 - balanced compact/serviceable** as the accepted Phase 3A
packaging baseline, with P1 as the serviceability fallback and P3 as an
aggressive comparison only. Begin Phase 4 preliminary structural concept work
under EDR-011.

P2 is a 364 x 356 x 276 mm review body with a 444 x 428 x 322 mm service
footprint. It preserves the 200 x 150 mm PCB area and 220 x 170 x 40 mm
screened tool travel. It uses a 230 x 180 x 8 mm moving-bed support and a
230 x 180 x 12 mm spoilboard reference, leaving 15 mm PCB perimeter per side.

Its packaging references are:

- X: 340 mm MGN12H rail, two blocks per rail at +/-30 mm, nominal 360 mm
  T8x4 screw with 340 mm conservative unsupported span;
- Y: 310 mm MGN12H rail, two blocks per rail at +/-40 mm, nominal 330 mm
  T8x4 screw with 310 mm conservative unsupported span;
- Z: 130 mm MGN9H rail, two blocks per rail at +/-20 mm, nominal 145 mm
  T8x2 screw with 130 mm conservative unsupported span and 40 mm travel;
- X/Z guide spacing remains approximately 60 mm and Y guide spacing remains
  220 mm;
- fixed/floating 8 mm bearing topology remains unchanged;
- owner-supplied NEMA17s remain direct axial drives in removable recessed
  pockets using the generic 42.3 mm / 5 mm / 40-48 mm preliminary interface;
  rear connector/wiring access must remain serviceable for multiple motors;
- no belt transmission is introduced.

The owner-directed fastening strategy from EDR-010 applies to these review
interfaces: heat-set inserts are the default reusable PETG thread, fasteners
provide clamp preload, and seated shoulders/keys/pockets/ribs provide
location and shear. The gantry crossmember must be mechanically seated rather
than suspended from M5 screws. Exact insert dimensions and any through-bolt
exceptions remain open until hardware and PETG joint evidence exist.

These are packaging envelopes and preliminary cut-length screens, not exact
purchase or production dimensions.

## Alternatives

### P1 - conservative serviceable

P1 retains a 240 x 190 mm bed, 20 mm PCB perimeter, wider carriage pitch,
larger bearing envelopes, and 394 x 385 x 296 mm body. It is the fallback when
fastener access, bearing preload, or PETG interface evidence is more important
than footprint.

### P3 - aggressive minimum practical

P3 reaches 344 x 334 x 268 mm, but reduces screened travel to 210 x 160 mm,
bed margins to 10 mm, transverse bed overhang to zero, and swept-bed body
clearance to 2 mm per end. It is not recommended without an owner decision and
an assembly/service mock-up.

## Reasoning

The original 400 x 400 x 310 mm machine envelope was not caused by the Y
220 mm rail spacing alone. It was the union of exposed motor/support
envelopes, structural bounds, a 240 x 190 mm bed, and an upper/lower motor
stack. More importantly, the earlier 300/280/100 mm rail references did not
include the full two-block carriage group in the swept travel budget.

P2 addresses the causes with controlled carriage pitch, explicit swept rail
length, recessed direct motors, compact replaceable bearing cartridges,
reduced but useful bed perimeter, and a lower Z reference. The dependency-light
checks pass, and the pinned build123d review models export non-empty STEP/STL
files with no unexpected solid interferences.

## Forced reconsideration of the motion baseline

The guide topology, rail classes, screw leads, guide spacing, fixed/floating
bearing concept, direct-drive rule, and 40 mm Z travel were **not** reopened.
Packaging did force two corrections to preliminary reference values:

1. X/Y/Z rail lengths must grow to 340/310/130 mm for P2 because 300/280/100
   mm do not prove full swept travel with two blocks per rail.
2. Conservative P2 commissioning feeds become 520/650/1100 mm/min because the
   longer unsupported screw spans reduce the 70% critical-speed screen.

This is a physical-compatibility correction within the same motion class, not
a new transmission or architecture decision.

## Risks and mitigations

| Risk | Consequence | Mitigation |
| --- | --- | --- |
| P2 3 mm full-sweep end clearance is too tight after tolerances. | Bed or front/rear cover contact. | Build a full-travel mock-up; reserve P1 if needed. |
| Y motor is only 4.85 mm below the bed support underside in the envelope screen. | Collision after hardware or fastener growth. | Measure motor, add a removable underside guard, and verify at both travel ends. |
| Printed bearing pockets or insert bosses creep or lose preload. | Axial play, backlash, screw misalignment, or joint slip. | Use replaceable cartridges, substantial rib-connected bosses, geometric seats, and PETG bearing-pocket/rail-seat/insert coupons. |
| P2 bed perimeter is inadequate for a future vacuum seal. | Workholding distortion or leakage. | Use tape/low-profile clamps first; treat vacuum as a separate study. |
| P3 end margins and front service access are too small. | Impossible assembly or maintenance. | Do not select P3 without a mock-up and owner approval. |
| Generic spindle envelope differs from hardware. | Z clearance and force loop invalid. | Identify and measure spindle before structural CAD. |

## Validation and review

- [x] P1/P2/P3 centralized packaging variants added.
- [x] Owner-directed M3/M4/M5 insert hierarchy and geometric load-transfer
      contract added to the review layer.
- [x] Boss wall, edge distance, tool access, M5 justification, and
      through-bolt justification checks added.
- [x] X/Y/Z swept rail-length calculation added.
- [x] Bed, motor, spindle, tool, limit, bearing, and Z-stack review envelopes added.
- [x] Dependency-light tests pass.
- [x] Pinned build123d review exports pass containment and interference checks.
- [x] Owner selects and accepts P2 as the packaging baseline on 2026-10-06.
- [ ] Full-travel assembly and service-access mock-up passes.
- [ ] PETG rail-seat, bearing-pocket, fastener, and motor-pocket coupons pass.
- [ ] Actual insert family measured; pilot, insertion depth, clearance, tool
      access, pull-out, torque, creep, and repeated-assembly values replace the
      preliminary screen.
- [ ] Exact spindle/motor/switch/bearing/screw hardware measured.

## Gate

The owner accepted EDR-009 and selected P2 on 2026-10-06. The baseline is
accepted for Phase 4 preliminary structural concept work, not as a
manufacturing freeze. Exact hardware, full-travel/service mock-up, PETG
coupons, measured spindle/motor/switch/bearing/screw dimensions, and
workholding evidence remain open. The later Phase 4/4A preliminary
architecture acceptance does not change this measurement boundary; production
exports and later Phase 5 batches remain outside this record. EDR-014 later
authorizes only the first base-pair candidate batch; it does not change this
measurement boundary.
