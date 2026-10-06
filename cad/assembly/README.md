# Assembly

The assembly module owns deterministic placement of part instances, hardware
envelopes, coordinate frames, and assembly-level metadata. The Phase 2
`architecture_skeleton.py` module is intentionally limited to reference
envelopes, centerlines, carriage boxes, and structural bounds. It must not
grow detailed printable-part geometry before the Phase 2 gate.
