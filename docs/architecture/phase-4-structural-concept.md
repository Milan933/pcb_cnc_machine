# Phase 4 - preliminary structural concept

## Scope and status

This is the preliminary structural CAD concept for the owner-accepted P2
packaging baseline. It is a review model, not a manufacturing release. The
source of truth is the parameter model plus the deterministic builders in
`cad/parts/phase4_structural.py` and `cad/assembly/phase4_assembly.py`.

The concept uses the P2 reference envelope of approximately 364 x 356 x 276
mm, with a 444 x 428 x 322 mm service footprint. The PCB datum remains 200 x
150 mm; the moving bed support is 230 x 180 x 8 mm and the replaceable
spoilboard reference is 230 x 180 x 12 mm. The machine remains a fixed gantry
with a moving Y bed.

## Force-loop concept

The primary loop is:

```text
tool -> 52 mm spindle screen / clamp -> Z carriage -> dual MGN9 X/Z backplate
     -> dual MGN12 X rail seats -> split X torsion beam -> hollow towers
     -> closed base perimeter / Y rail carriers -> Y carriages -> ribbed bed
     -> PCB datum
```

The printed geometry carries location, shear, bending reaction, and torsion
through closed sections, shoulders, ribs, and broad mating surfaces. Heat-set
inserts provide reusable threads and fasteners provide clamp preload. A
one-piece 330 mm-class gantry print is not used as a mandatory part.

## Structural decomposition

All records are `PRELIMINARY`. The actual review builder also records support,
brim, warping, and layer/load concerns for every part.

| Group | Part IDs | Concept |
| --- | --- | --- |
| Base perimeter | `base_front_left`, `base_front_right`, `base_rear_left`, `base_rear_right` | Four closed 150 x 32 x 36 mm segments with indexed central seams. |
| Base side/load path | `base_left_side_member`, `base_right_side_member`, `base_center_tie` | Closed 48 x 236 x 36 mm sides and a relieved 252 x 24 x 30 mm center tie. |
| Y rail/service | `base_y_rail_carrier_left`, `base_y_rail_carrier_right`, `y_motor_service_pocket`, `y_fixed_bearing_cartridge`, `y_floating_bearing_cartridge` | 300 mm preferred-boundary rail carriers and replaceable motor/fixed/floating cartridges. |
| Feet/accessory | `machine_foot_front_left`, `machine_foot_front_right`, `machine_foot_rear_left`, `machine_foot_rear_right`, `electronics_mount_rail` | Distributed feet and an optional elevated rear electronics attachment rail. |
| Fixed gantry | `gantry_tower_left`, `gantry_tower_right`, `gantry_beam_left`, `gantry_beam_right` | Hollow 54 x 90 x 62 mm towers and a split 90 mm deep X torsion-box with front rail pads. |
| X screw support | `x_fixed_bearing_cartridge`, `x_floating_bearing_cartridge` | Replaceable axial/radial cartridges at the split beam ends. |
| X/Z moving structure | `x_carriage_plate`, `z_carriage_plate`, `z_fixed_bearing_support`, `z_motor_service_cartridge` | Ribbed backplate and short spindle force loop around dual MGN9 Z guides and T8x2. |
| Spindle | `spindle_mount_concept` | Generic 52 mm maximum spindle screen with a parametric clamp concept; actual bore remains open. |
| Moving bed | `moving_bed_frame` | 230 x 180 mm perimeter/rib frame, centered Y nut boss, narrow carriage pads, and replaceable spoilboard interface. |

The 29-part count is enforced by the dependency-light validator and matched
against the built assembly.

## Gantry joint study

The separate temporary joint study compares three equal-scale review concepts:

| ID | Concept | Load/torsion path | Risk / status |
| --- | --- | --- | --- |
| J1 | Deep tongue-and-groove/socket | Deep captured tongue, shoulder, and broad mating faces carry shear, bending, and torsion; M4 inserts clamp. | Selected provisionally; coupon, creep, and repeat-service evidence required. |
| J2 | Stepped keyed shoulder | Broad step carries bending; positive key carries shear. | Fallback if J1 cleaning or insertion is poor. |
| J3 | Interlocking ribs/shear keys | Several ribs distribute shear and torsion. | More interfaces and insert locations; retained as an alternative. |

The J1 selection is a concept decision, not an exact insert pattern. The
joint study is exported separately so owner review can inspect the load path
without mistaking it for the final beam.

## Rail-seat strategy

The rail references remain the accepted P2 classes and lengths:

| Axis | Reference | Printed concept | Alignment / post-process |
| --- | --- | --- | --- |
| Y | Dual MGN12, 310 mm | Two 28 x 300 mm carrier pads with load-spreading ribs. | Establish one master shoulder, shim the opposite rail, torque datum-outward, and measure over the full support. |
| X | Dual MGN12, 340 mm, 60 mm vertical spacing | Beam-integrated broad lower/upper pads with shoulders; the pad envelope is included in each split beam. | Reference lower rail first, set the 60 mm spacing, then measure straightness/parallelism; skim or use a replaceable strip if needed. |
| Z | Dual MGN9, 130 mm, approximately 60 mm spacing | Rib-integrated vertical pads on the X carriage backplate. | Match the second rail to the first with a gauge/carriage reference; shim or post-process the faces. |

The model deliberately does not claim raw PETG flatness or supplier hole
patterns. Actual rail cross-sections, screw spacing, fastener edge distance,
and insert pockets wait for measured hardware and coupons.

## Moving bed and workholding

The bed uses four perimeter beams, transverse ribs, a centered T8x4 nut boss,
and small carriage pads aligned with the 220 mm Y guide spacing. The frame is
not a solid plate. The 8 mm bed support and 12 mm spoilboard are separate P2
interfaces. Tape and low-profile edge clamps remain the first workholding
concept; vacuum is not assumed. The full 230 x 180 mm bed must be checked over
the 170 mm Y travel, with PCB datum and probe-cable access retained.

## Serviceability and assembly order

The concept keeps NEMA17 motors, fixed/floating cartridges, couplers, T8
screws/nuts, MGN12/MGN9 rails and carriages, spindle, limits, probe/wiring,
moving-bed wiring, and spoilboard replaceable. The planned sequence is:

1. Condition/inspect base members and install feet.
2. Join indexed front/rear segments and side members.
3. Install Y carriers, datum strips, cartridges, and centered screw.
4. Install the Y motor pocket, coupler, motor, and moving-bed carriage set.
5. Install towers and verify base shoulders.
6. Insert the J1 split X beam and clamp the seated joint.
7. Align X rail seats and install X rails, carriages, and cartridges.
8. Install the X carriage, Z rails, Z supports, motor cartridge, and coupler.
9. Install spindle, limits, probe brackets, electronics rail, and covers.
10. Install spoilboard/workholding and verify full travel and clearances.

Physical access and repeated-disassembly evidence are still required.

## Printability boundary

Every mandatory part is documented with a realistic orientation and process
concerns. The two Y rail carriers are exactly 300 mm in their long XY axis,
so they are preferred-boundary parts requiring printer-specific conditioning,
brim, datum inspection, and shim/skimming evidence. No mandatory part exceeds
320 mm in either build-plate axis. The split beam, rather than a mandatory
330 mm single print, is the current modularity choice.

The current build123d runner exports review-only files to a temporary directory
and validates:

- structural parts against the P2 XYZ envelope;
- the actual structural part count and built bounding boxes;
- the P2 rail, screw, motor, bearing, spindle, bed, and limit references;
- expected interface overlaps versus unexpected independent-solid overlap;
- non-empty STEP/STL assembly, individual-part, and joint-study files.

Run it with the pinned external environment:

```text
python -m tools.run_phase4_preliminary_study --output-dir <temporary-directory>
```

The result is intentionally `not-ready` for physical evidence even when the
automated review checks pass. Phase 4 acceptance, manufacturing release, and
Phase 5 remain outside this concept document.
