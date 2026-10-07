# Phase 5 master-assembly-first manufacturing CAD

**Status:** owner-authorized virtual-machine phase; candidate outputs only

The owner opened Phase 5 from baseline
`afe2e14089467321b323d74f928a7ab4c5ffdc1f` and directed the project to finish
the complete assembled machine before physical part review. The master
assembly is primary; printable splits are derived from it.

## Required outputs

1. A central coordinate, work-origin, travel, envelope, motor, spindle,
   controller, and provisional-interface parameter contract.
2. Credible local hardware/interface models with source, permission/reuse,
   confidence, and measurement status tracked.
3. A complete master assembly containing fixed structure, moving bed, rails,
   carriages, screws, nuts, bearings, couplers, owner-stock motor envelopes,
   spindle candidate, workholding, PCB, probe, limits, Arduino Mega + CNC
   Shield, cooling/service volumes, cable routes, and fastener references.
4. A derived continuous PETG structure with real walls, ribs, rail seats,
   keyed/shouldered split joints, bearing supports, controller support, and
   fastening/load-path interfaces. The inventory may change when the master
   requires a support part; the active inventory is 20 parts.
5. A deterministic eight-corner X/Y/Z travel and clearance screen, exact
   BRep structural-overlap classification, support/fastening audit, and
   reconstruction from the derived parts plus hardware models.
6. Individual STL/STEP derivatives, a complete master STEP, a visualization
   STL, and 16 review images suitable for owner review and OrcaSlicer
   inspection.
7. Updated inventory, hardware register, BOM, assembly guide, coordinate
   instructions, fastener schedule, wiring/controller record, support audit,
   traceability, manifest, tests, and EDR.

## Fixed architecture and owner hardware

- fixed gantry, moving Y bed, 200 x 150 mm PCB work area;
- dual MGN12-class X/Y guides and dual MGN9-class Z guides;
- T8x4 X/Y and T8x2 Z screening screw classes;
- **OWNER-SUPPLIED NEMA17 stock - DO NOT BUY**; use a generic 42.3 mm
  interface, screening 5 mm shaft, 40-48 mm common body, and rear connector
  clearance; assign X/Y normal suitable stock and Z the strongest electrically
  compatible stock after characterization;
- **OWNER-SUPPLIED Arduino Mega + CNC Shield - DO NOT REPLACE** absent a
  validated limitation; exact Shield revision and driver modules remain open;
- verify Shield microsteps, current/voltage capability, cooling, limit inputs,
  probe input, spindle PWM/control outputs, and GRBL-compatible firmware;
- spindle remains a realistic ER11 candidate/interface until actual hardware,
  mass, cable, heat, and runout are measured.

## Manufacturing boundary

Hardware-dependent interfaces are explicitly
`PROVISIONAL_HARDWARE_DIMENSION`. This permits test-printable candidate STL
and STEP generation but blocks `HARDWARE-VALIDATED` and `RELEASED` maturity.
No third-party CAD is redistributed where permission is unclear; local derived
models are the repository source.

All structural candidates must be valid one-solid shapes and fit the
conservative 320 mm individual-part screening envelope. The two base sides
are conditional 320 mm Y prints needed to preserve the 310 mm Y rail seat;
verify the owner's Voron 350 usable volume and long-axis process distortion.

The current generator is:

```text
C:\Users\milan\pcbCNC-cad-env\Scripts\python.exe -m tools.generate_phase5_complete_machine
```

Outputs remain under `generated/*/phase5-complete-machine/`, never a
`release/` directory. The next gate is owner structural review followed by
hardware identification, coupons, physical first prints, fit/alignment,
electrical verification, and commissioning evidence.
