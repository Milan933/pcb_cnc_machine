# EDR-015: Phase 5 complete virtual machine before physical part review

**Status:** owner-authorized implementation / candidate review boundary

**Date:** 2026-10-07

**Supersedes:** EDR-014 as the active Phase 5 scope. EDR-014 remains the
historical record of the first base-pair batch.

## Decision

Proceed from the accepted Phase 4A O2 architecture to a complete coherent
virtual PCB CNC machine before stopping for an isolated physical part review.
Convert all 19 O2 structural identities into actual parametric, fused PETG
candidate solids, place them with the complete motion/process/control
envelopes, and generate the full local STL/STEP, BOM, fastener, wiring,
assembly, and review package.

The complete machine and parts remain `PROTOTYPE-STL` / manufacturing-CAD
review candidates. They are not `HARDWARE-VALIDATED` or `RELEASED`.

## Owner direction and hardware boundary

The owner explicitly opened Phase 5 from baseline
`afe2e14089467321b323d74f928a7ab4c5ffdc1f` and directed the workflow to
continue through the complete virtual machine.

- Use the owner-supplied Arduino Mega + CNC Shield platform. Do not replace it
  without a validated technical limitation.
- Use the existing owner selection of NEMA17 motors. Do not purchase new
  motors at this stage.
- Keep exact Shield revision, installed driver modules, microstep/current/
  voltage/cooling capability, I/O mapping, firmware, and final motor
  assignment as identification/commissioning items.
- Use a generic 42.3 mm NEMA17 interface, screening 5 mm shaft and 40–48 mm
  common body envelope, with rear connector clearance.
- Keep genuinely unmeasured purchased interfaces centralized and explicitly
  `PROVISIONAL_HARDWARE_DIMENSION`.

## Alternatives considered

1. **Stop after the base pair for owner review.** This was the EDR-014
   boundary and is now superseded by the owner’s explicit complete-machine
   direction.
2. **Generate all remaining geometry as review blocks.** Rejected because the
   owner requires actual walls, ribs, rail seats, fastening interfaces,
   service access, and slicer-inspectable candidates.
3. **Continue to physical printing before completing the virtual assembly.**
   Rejected for this step because travel, force-loop, service, controller,
   workholding, and cable relationships need to be reviewed coherently first.

## Evidence produced

- `cad/parameters.py` central Phase 5 coordinate and envelope contract;
- `cad/parts/phase5_complete_structural.py` 19 actual local single-solid
  parametric candidates;
- `cad/assembly/phase5_complete_assembly.py` complete 70-component named
  assembly and travel-state builder;
- `cad/validation/phase5_complete.py` fail-closed inventory, assembly,
  interference, and eight-corner travel checks;
- local individual STL/STEP derivatives and
  `pcb_cnc_complete_assembly.step` / visualization STL;
- 12 local review images;
- complete assembly guide, coordinate system, fastener schedule, wiring
  architecture, BOM, review report, and manifest.

## Risks and mitigations

| Risk | Mitigation / open evidence |
| --- | --- |
| PETG creep and rail-seat distortion | print coupons, condition parts, measure and shim/skim datums |
| Provisional hole/bearing/insert geometry does not fit | measure representative hardware before fit claims; keep interfaces parametric |
| Owner NEMA17 electrical mismatch | characterize existing stock and selected driver before final assignment |
| Unknown shield/driver pinout or cooling | identify exact board/modules before firmware or wiring freeze |
| Spindle diameter/mass/runout differs from envelope | measure representative spindle and retain modular mount |
| Cable or service access is inadequate | inspect exploded views and perform a full-travel service mock-up |
| Complete CAD mass differs from earlier analytical estimate | treat solid-equivalent mass as calculated only; use slicer estimate and physical prints |

## Gate boundary

This record authorizes complete virtual manufacturing-CAD development and
local candidate exports. It does not authorize a production purchase order,
release-directory publication, final motor purchase, controller replacement,
or claims of measured stiffness, accuracy, runout, repeatability, electrical
compatibility, or physical fit.

The next owner gate is review of the complete package followed by measured
hardware identification and controlled first physical prints/coupons.
