# Assembly

The assembly module owns deterministic placement of part instances, hardware
envelopes, coordinate frames, and assembly-level metadata. The Phase 2
`architecture_skeleton.py` module is intentionally limited to reference
envelopes, centerlines, carriage boxes, and structural bounds. The Phase 3
`motion_skeleton.py` extension adds nominal rails, screws, nuts, bearing
supports, couplers, motors, spindle, and bed envelopes, but remains review
geometry only. Neither module is a source of production printable-part
geometry.
