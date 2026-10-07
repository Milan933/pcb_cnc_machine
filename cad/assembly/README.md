# Master assembly

`master_machine.py` is the primary Phase 5 design object. It places the
derived structural solids around local hardware/interface models, records the
support and fastening answer for every named component, and builds the
nominal plus eight travel-state assemblies.

The master includes fixed structure, moving bed, guides, screws, nuts,
bearings, couplers, generic owner-stock NEMA17s, SycoTec ER11 candidate,
workholding, probe, limits, Arduino Mega + provisional CNC Shield, cooling
clearance, and cable-service volumes. It remains a compound so serviceable
boundaries and intentional interfaces are visible.

`phase5_complete_assembly.py` is a compatibility import path that delegates
to the master builder. The old architecture and motion skeletons remain
historical review tools; they do not define the active manufacturing package.
