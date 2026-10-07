# Parametric structural parts

`master_structural.py` contains the active Phase 5 source geometry. It derives
20 local fused PETG solids from the hardware-first master layout: real walls,
ribs, webs, rail seats, bearing cartridges, split gantry joints, service
pockets, controller support, a low Y drive, and a dedicated rear Y bearing
bridge.

Parts are generated in their local print frames. World placement belongs to
`cad/assembly/master_machine.py`. All supplier-dependent holes, bearing
retainers, insert pilots, spindle bores, and final fastener sizes remain
`PROVISIONAL_HARDWARE_DIMENSION`; candidate maturity is `PROTOTYPE-STL`.

The compatibility module `phase5_complete_structural.py` preserves the old
import path but delegates to the master-derived source.
