# Master assembly support and fastening audit

This is the visual floating-component audit for the Phase 5 master. The
master assembly is the source object; subsystem and exploded images may
intentionally offset parts for inspection. `Attached` means the local model
has a geometric contact/intersection or a declared datum contact. `Provisional`
means the support answer exists but the exact bracket, fastener, or supplier
interface remains to be measured.

| Assembly group | Components | Supporting geometry | Fastening / retention | Audit status |
| --- | --- | --- | --- | --- |
| Fixed base | `base_left_integrated`, `base_right_integrated` | feet and support surface | M4 through/insert interfaces; base shoulders carry shear | Attached / provisional |
| Base tie | `base_center_tie` | both base sides; keyed end faces | M4 inserts or through-bolts; keys carry location | Attached / provisional |
| Y drive front | `y_motor_service_pocket`, `y_fixed_bearing_cartridge`, Y motor, coupler | base-center datum and low Y drive pocket | M4 pocket joint; NEMA17 face screws; fixed 608 retainer | Attached / provisional |
| Y drive rear | `y_floating_bearing_cartridge` | new `y_rear_bearing_bridge` anchored to the left base | M4 bridge/base bolts; radial retainer with axial float | Attached / provisional |
| Y motion | Y rails/carriages, `moving_bed_frame`, Y nut/screw | base rail seats; four bed carriage pads; nut boss | measured M3 carriage hardware and M4 nut fasteners | Attached / provisional |
| Feet | four machine feet | table/support surface and base underside | M4 through-bolt and washer | Datum contact / provisional |
| Electronics | `electronics_mount_rail`, Arduino Mega, CNC Shield | rear base standoffs and electronics rail | M4 rail joint; M3 board slots/standoffs; Mega header stack | Attached / provisional |
| X fixed drive | X fixed cartridge, X motor, coupler, screw | left gantry tower and fixed bearing cartridge | M4 cartridge screws; generic NEMA17 face; two-bore coupler | Attached / provisional |
| X floating drive | X floating cartridge and screw | right gantry tower/radial seat | M4 retainer; axial float intentionally open | Attached / provisional |
| X guide | X rails and four MGN12H blocks | printed rail shoulders and moving X/Z backbone | measured rail/carriage fasteners, M3 class | Attached / provisional |
| Gantry | left/right integrated towers and keyed beam joint | base sides; tongue/socket joint | M4 base preload and beam clamp; keys transfer shear | Attached / provisional |
| Z guide | MGN9 rails/blocks and `z_carriage_plate` | X/Z backbone and Z plate | measured M2/M3 guide hardware | Attached / provisional |
| Z drive | Z screw/nut, motor, coupler | backbone motor land, Z plate nut boss | fixed/floating bearing stack; M4 nut; NEMA17 face screws | Attached / provisional |
| Spindle | `spindle_mount_concept`, SycoTec candidate, tool envelope | Z plate rear/clamp module and two ring bores | removable M4 clamp hardware; ER11 tool retention | Attached / reference candidate |
| Workholding | spoilboard, PCB envelope, three clamps | bed datum skin and replaceable spoilboard | M4 spoilboard fasteners; M3/M4 edge clamp screws | Surface/datum contact |
| Probe | conductive probe and bracket | spoilboard datum | removable M3 clip/bracket and cable | Attached / process provisional |
| Homing | X/Y/Z limit switches and modeled brackets | respective gantry/base/XZ datums | M3 bracket screws; actuation direction open | Attached / actuation provisional |
| Cable management | controller, X/Z, and Y moving loop volumes | rail/bed/controller anchor zones | M3 clips and strain relief | Routing volume, not a structural part |
| Fastener reference | representative M4 envelope | base left interface | through-bolt/washer envelope | Reference only |

## Geometry checks behind the table

The generator checks that every named component has a non-empty supporting-part
and fastening record. The structural subset additionally uses exact BRep
intersections, with only declared joints/supports/service interfaces allowed.
The travel screen checks spindle/gantry, bed/gantry, Y-end-support,
Z-motor/gantry, and Z-motor registration at all eight X/Y/Z corners.

The switches and probe now include explicit local bracket/contact geometry in
the master component shapes. The controller Shield and driver cooling volume
remain deliberately provisional because the owner board revision and driver
modules are not identified. The cable-loop boxes are clearance/service
volumes, not claims that a final cable chain or strain relief has been chosen.

## Remaining physical evidence

- measure the actual rails, carriages, screws, nuts, bearings, couplers, and
  fastener/insert stack;
- verify the Y-end bearing bridge and low drive datum against the real bearing
  stack and bed sweep;
- identify the Arduino Mega board revision, CNC Shield revision, drivers,
  jumpers, current/voltage/cooling capability, limits/probe/spindle I/O, and
  GRBL-compatible firmware mapping;
- characterize representative owner-stock NEMA17 motors before assignment;
- inspect printed bracket, joint, and cable clearances on physical coupons.

This audit supports owner structural review; it does not change any candidate
to `HARDWARE-VALIDATED` or `RELEASED`.
