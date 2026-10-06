# Phase 1 working-envelope trade study

The options below compare usable PCB working area, not final machine travel.
The screening model assumes 30-50 mm total packaging allowance per axis end
pair, or 60-100 mm total, for carriage length, screw supports, guide ends,
clamps, probing, and edge access. These allowances are assumptions for a
trade study, not CAD dimensions.

## Comparison

| Option | PCB working area | Screening guide/screw envelope | Printed gantry/span screening | Voron 350 printability | Expected footprint screening | Main risk |
| --- | --- | --- | --- | --- | --- | --- |
| A | 160 x 100 mm | 220-260 mm | 220-260 mm | Comfortable; most parts can remain below the preferred 320 mm one-piece limit | Approximately 260-320 x 200-260 mm before service clearances | May underserve the intended board size and limit panelization. |
| B | 200 x 150 mm | 260-300 mm | 260-300 mm | Best balance; large parts remain conditionally printable with orientation and datum planning | Approximately 300-360 x 250-310 mm before service clearances | Gantry torsion and PETG rail-seat stiffness become central. |
| C | 250 x 180 mm | 310-350 mm | 310-350 mm | Marginal; little nominal 350 mm margin and likely split or post-processed structural parts | Approximately 350-410 x 280-340 mm before service clearances | Long spans, larger footprint, lower stiffness, and difficult one-piece printing. |

The guide/screw and gantry ranges are calculated as working area plus the
screening allowance. Actual rail and screw lengths also require carriage,
bearing, coupling, hard-stop, and assembly margins.

## Recommendation

Use option B, 200 x 150 mm nominal PCB working area, as the Phase 1
architecture-comparison baseline. It preserves the original project target,
covers a useful desktop PCB size, and remains compatible with the Voron 350
only if the architecture keeps primary printed parts near the preferred
320 mm dimension and uses realistic print orientations.

Do not freeze option B as final machine travel. Phase 2 must decide how much
additional travel is required for board registration, clamps, probing, tool
paths, and datum margins. Option A remains a lower-risk prototype baseline;
option C requires a positive stiffness and printability justification.

## Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-ENV-006 | Phase 2 shall compare options A, B, and C using the same packaging assumptions and report guide length, screw length, gantry span, footprint, stiffness, and printability. | Known phase requirement |
| REQ-ENV-007 | Option B shall be used as the provisional process baseline but shall not be frozen without an architecture EDR. | Preliminary |
| REQ-ENV-008 | Any printed component above 320 mm shall require an explicit orientation, margin, warping, and assembly-access review; above 330 mm requires a split-part or post-processing decision. | Preliminary |
