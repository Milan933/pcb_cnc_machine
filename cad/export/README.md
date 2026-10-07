# Export boundary

The active exporter is `tools/generate_phase5_complete_machine.py`. It
generates reproducible individual STEP/STL derivatives, the complete
`pcb_cnc_master_assembly.step` and visualization STL, a scene manifest, and
16 review images from the hardware-first master source.

Outputs are candidate engineering artifacts under the allowlisted
`generated/stl/phase5-complete-machine/`,
`generated/step/phase5-complete-machine/`, and
`generated/drawings/phase5-complete-machine/` paths. No output is a release;
`PROTOTYPE-STL` remains the highest permitted maturity until measured
hardware, print coupons, fit, alignment, service, electrical, and commissioning
evidence exist.
