# EDR-016: Phase 5 master assembly first and hardware-model redesign

**Status:** owner-authorized implementation / candidate structural review

**Date:** 2026-10-07

**Supersedes:** EDR-015 as the active Phase 5 methodology. EDR-015 remains
the record that opened the complete virtual-machine scope.

## Decision

Make the complete assembled PCB CNC the primary design object. Investigate and
record credible hardware references, build local derived interface/envelope
models, place the complete machine, establish motion and clearance, derive the
continuous PETG force loop, choose printable split planes and joints, then
regenerate STL/STEP derivatives and reconstruct the master from those parts.

The previous envelope-only STL package is not printable/release-authorized.
The active package is a `PROTOTYPE-STL` candidate for owner structural review;
no part is `HARDWARE-VALIDATED` or `RELEASED`.

## Owner hardware boundary

- Arduino Mega + CNC Shield is owner-supplied intended hardware. Do not
  replace it absent a validated electrical or motion limitation.
- Exact Shield revision and installed driver modules remain unresolved, along
  with microsteps, current/voltage capability, cooling, limits, probe,
  spindle PWM/control, and GRBL-compatible firmware mapping.
- Existing owner NEMA17 stock is owner-supplied; do not buy motors. Use a
  generic 42.3 mm interface, screening 5 mm shaft, 40-48 mm body envelope,
  and rear connector clearance. Assign X/Y normal suitable stock and Z the
  strongest electrically compatible candidate after characterization.
- Purchased or unmeasured hardware interfaces remain centralized and marked
  `PROVISIONAL_HARDWARE_DIMENSION`.

## Alternatives considered

1. Continue the prior 19-part envelope-heavy set: rejected; it did not make
   the assembled machine the source object.
2. Preserve exactly 19 parts for inventory convenience: rejected; the master
   required a dedicated rear Y floating-bearing bridge, producing 20 parts.
3. Commit downloaded supplier CAD: rejected where redistribution rights are
   unclear; local derived models are used and sources are tracked.
4. Replace the owner controller or purchase motors: rejected; no limitation
   has been demonstrated.

## Evidence produced

- `cad/hardware/master_hardware.py` and the hardware model register;
- `cad/assembly/master_machine.py` with 68 named components and support/
  fastening records;
- `cad/parts/master_structural.py` with 20 fused PETG candidates;
- exact structural overlap, eight-corner travel, support, and export checks;
- master STEP, visualization STL, 20 individual STEP/STL pairs, and 16
  review images;
- updated hardware identification, procurement/BOM, assembly, fastener,
  wiring, support-audit, traceability, and owner-review documents.

## Risks and mitigations

| Risk | Mitigation / open evidence |
| --- | --- |
| Reference model differs from owner hardware | source/confidence register and physical measurement before fit claim |
| PETG creep, rail-seat distortion, or joint weakness | conditioned coupons, inserts, rail-seat inspection, and force-loop tests |
| Y end support or low transmission datum differs from actual stack | dedicated bridge and explicit travel/sweep check; measure before print |
| NEMA17 motor electrical mismatch | characterize owner stock and selected driver before assignment |
| Unknown Shield/driver I/O or cooling | identify board/modules before firmware/wiring freeze |
| Spindle candidate mass/cable/runout differs | retain modular clamp and measure actual candidate |
| Cable/service access or process workholding fails | review service volumes, physical mock-up, and first-process tests |

## Gate boundary

This EDR authorizes the master-assembly-first virtual CAD implementation and
candidate exports from the owner's stated baseline
`afe2e14089467321b323d74f928a7ab4c5ffdc1f`. It does not authorize a release,
production purchase, motor purchase, controller replacement, or a claim of
measured stiffness, accuracy, runout, repeatability, electrical compatibility,
or physical fit.

Next gate: owner structural review, then measured hardware records and
controlled physical first prints/coupons.
