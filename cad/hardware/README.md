# Hardware representations

`master_hardware.py` is the local derived hardware layer for the Phase 5
master assembly. It contains dimensionally controlled interface/envelope
builders for the guide, screw, bearing, coupler, motor, controller, spindle,
limit, probe, and fastener classes.

These are not silently downloaded supplier models. Source URLs, confidence,
classification, and repository reuse treatment are recorded in
[`docs/manufacturing/hardware-model-register.md`](../../docs/manufacturing/hardware-model-register.md)
and `HARDWARE_MODEL_REGISTER`. Supplier-dependent geometry remains
`REFERENCE-CAD`, `ENVELOPE-ONLY`, or `PROVISIONAL` until the actual hardware is
identified and measured.

The owner controller is recorded as **OWNER-SUPPLIED Arduino Mega + CNC
Shield**. Existing NEMA17 stock is **OWNER-SUPPLIED - DO NOT BUY**; the local
motor model is a generic 42.3 mm interface with rear connector clearance.
