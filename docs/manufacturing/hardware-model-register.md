# Persistent hardware CAD model register

The authoritative registry is
[`cad/library/hardware-model-manifest.json`](../../cad/library/hardware-model-manifest.json).
It assigns stable `HW-*` IDs, records source provenance and reuse treatment,
points to the project-generated parametric model, and declares which master
assembly instances consume each model.

The legacy [`HARDWARE_MODEL_REGISTER`](../../cad/hardware/master_hardware.py)
remains as a compatibility source register for existing Phase 5 reports. New
assembly work must use the persistent library wrappers and stable IDs under
[`cad/library/`](../../cad/library/).

## Current provenance summary

| Measure | Count | Meaning |
| --- | ---: | --- |
| External CAD/model offerings discovered | 6 | HIWIN MGN12H, HIWIN MGN9H, Arduino Mega CAD resources, SycoTec spindle STEP, Omron D2F CAD access, MISUMI coupling CAD |
| External files downloaded | 0 | No vendor binary CAD was acquired in this task |
| External files legally committed | 0 | The public repository contains no third-party CAD binary |
| Not committed because license/access is unclear | 5 | HIWIN, SycoTec, Omron, and MISUMI source-CAD offerings |
| Project-generated reference/interface models | 14 | All entries in the authoritative manifest have committed local parametric geometry |

Arduino's open-hardware references are attributed, but the committed
mechanical representation is still project-generated rather than a copied
vendor file. No original filename or checksum is asserted when a file was not
downloaded.

## Stable IDs used by the master assembly

The current master resolves these 14 IDs:

`HW-BRG-608-REF`, `HW-CPL-5X8-REF`, `HW-CTRL-ARDUINO-MEGA-REF`,
`HW-CTRL-CNC-SHIELD-PROV`, `HW-FST-M4-REF`, `HW-LM-MGN12H-REF`,
`HW-LM-MGN9H-REF`, `HW-LN-T8-ABN-REF`, `HW-LS-T8X2-ENV`,
`HW-LS-T8X4-ENV`, `HW-MOTOR-NEMA17-REF`, `HW-PROBE-CONDUCTIVE-REF`,
`HW-SPINDLE-5045-ER11-001`, and `HW-SW-D2F-REF`.

The master uses these models for mechanical clearance, mounting, service,
motion, and load-path review. The models do not upgrade owner hardware to
measured or manufacturing-validated status.

## Missing or measurement-dependent hardware

- Exact Arduino Mega board revision and CNC Shield revision;
- installed driver modules, microstep jumpers, current/voltage capability,
  cooling, limits, probe, spindle PWM/control, and GRBL-compatible mapping;
- representative owner NEMA17 identity, body/shaft/connector/current data,
  and evidence-based X/Y/Z assignment;
- actual MGN rails/carriages, T8 screws/nuts, 608 bearings, couplers,
  switches, inserts, fasteners, probe, and spindle/clamp dimensions;
- spindle cable exit, cooling, runout, and final axial envelope.

Run the dependency-light schema check with:

```text
python -B tools/validate_hardware_library.py
```

Third-party attribution and publication boundaries are documented in
[`cad/library/THIRD_PARTY_NOTICE.md`](../../cad/library/THIRD_PARTY_NOTICE.md).
