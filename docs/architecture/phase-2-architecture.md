# Phase 2 architecture study

**Status:** accepted Architecture A baseline; original B recommendation retained as historical comparison
**Date:** 2026-10-06
**Units:** millimetres unless stated otherwise
**Boundary:** architecture and parametric skeleton only; no detailed printable
parts, manufacturing drawings, or release STEP/STL files.

## Phase 2A status note

The three-way matrix and B recommendation below are the original Phase 2
baseline. They are retained as historical comparison, not as the current
selection. The focused [Phase 2A structural comparison](phase-2a-structural-comparison.md)
reopened A versus B using independently optimized structural concepts. The
owner accepted A: fixed gantry with moving Y bed on 2026-10-06. B remains the
documented primary rejected alternative and must not be physically built unless
the owner reopens the architecture. Detailed motion hardware and structural
geometry remain open for Phase 3 and later evidence.

## Inputs accepted from Phase 1

The owner accepted EDR-005 and the following values are the common comparison
baseline:

- nominal PCB working area: 200 x 150 mm; this is not final rail or screw
  travel;
- tool-point deflection target: <=0.020 mm under a defined 5 N load, with
  <=0.030 mm first-prototype acceptance;
- non-compensatable Z allocation: 0.040 mm;
- post-map residual target/acceptance: <=0.020 / <=0.030 mm;
- conductive PCB probing and height mapping are required;
- spindle, exact rail class, exact screw lead, controller, and probing
  implementation remain unresolved.

The common screening geometry uses a preliminary tool travel of 220 x 170 x
40 mm. The extra 10 mm at each working-area edge is an architecture
assumption for registration, clamp, probe, and tool-path access. It is not a
frozen machine travel requirement.

## Candidate comparison from the original Phase 2 baseline

### A — fixed gantry with moving Y bed

The fixed gantry gives the Z/X reaction path a stationary support and can be
made very stiff with a deep printed monocoque. The moving bed must carry the
PCB, spoilboard, workholding, and any cable/probe service loop. Its dominant
risks are bed pitch under load, long rail-seat alignment, moving datum mass,
and map validity after the board has been probed and moved.

### B — moving gantry with fixed bed

The fixed bed gives the PCB a stationary datum. A pair of separated Y guide
lines carries the gantry, while a deep crossbeam carries the X and Z loop.
This is the selected preliminary architecture because it best combines a
stable workholding/probing datum with a short tool loop and practical service
access. Its gating risk is gantry torsion through the two PETG side
interfaces; that risk is addressed with a closed/deep-ribbed monocoque,
large section depth, distributed rail loads, and a physical 5 N test before
structural release.

### C — fixed gantry with fixed bed and moving XY head

This is a credible alternative rather than a count-filler: it preserves the
fixed PCB datum while testing whether a non-moving-bed arrangement can avoid a
moving gantry. The elevated XY head introduces an extra guide stack and a
longer tool-point path. Its additional joints, carriage overhang, and
alignment burden make it the lowest-ranked candidate for a PETG-first machine.

## Original preliminary architecture decision

Select **B, moving gantry / fixed bed**, as the preliminary Phase 2 winner.
Keep **A, fixed gantry / moving bed**, as the runner-up and the fallback if a
representative B gantry fails the tool-point stiffness or creep test. Reject C
for this phase because its fixed-bed benefit does not compensate for the
longer, more joint-sensitive XY-head force loop.

This is a preliminary architecture choice, not a Phase 3 hardware selection
and not an accepted EDR. The proposed interfaces are:

- X: a tool carriage on two horizontal rail centerlines across a deep gantry
  beam; the reference rail separation is 50 mm in the skeleton;
- Y: two separated side rail centerlines, approximately 220 mm apart, carrying
  the moving gantry over the fixed bed;
- Z: two vertical guide centerlines, approximately 60 mm apart, with a screw
  on the spindle centerline;
- bed: fixed, replaceable-spoilboard envelope 240 x 190 mm, with the accepted
  200 x 150 mm PCB area inside it;
- screws: centered X, centered Y, and centered Z reference lines; T8x2 and
  T8x4 remain candidates and are not frozen;
- rails: dual-guide Z is the preferred interface. Dual MGN12 is the stronger
  candidate, while dual MGN9 remains a lower-mass candidate. A single MGN12
  carriage is not the primary architecture because it does not form a
  separated moment-reaction couple;
- spindle: an envelope of approximately 52 mm diameter x 120 mm length,
  with 15 mm tool stickout and 50 mm tool-point overhang screening values;
  no spindle is selected.

This B recommendation is retained here as historical baseline context. It is
reopened for owner review by Phase 2A; the revised A/B result and evidence
boundary are recorded in the linked Phase 2A package and EDR-007.

## PETG structural principle

The machine shall not copy aluminium-extrusion geometry in PETG. The B
gantry concept is a closed/deep-ribbed monocoque or torsion-box-like section
with large section depth, gradual fillets, gussets at the side transitions,
and distributed metal-backed rail and fastener interfaces. The first
crossbeam envelope is approximately 280 mm clear span and 320 mm outer width,
so a one-piece printed primary beam remains within the preferred 320 mm
screening limit. This does not pass printability: layer direction, bed
contact, warping, rail-seat post-processing, and creep still require Phase 6
evidence.

The structural load path must be carried by skins, ribs, and through-bolted or
metal-spread interfaces where preload and alignment matter. Infill percentage
is not a stiffness model. PETG anisotropy, moisture, temperature, long-term
preload, and local fastener bearing remain design inputs.

## Gantry section trade

| Section concept | Bending | Torsion | PETG load path | Printability / service | Phase 2 disposition |
| --- | --- | --- | --- | --- | --- |
| Closed rectangular box | good | good | continuous skins; local wall buckling must be checked | good if one-piece; internal access is limited | viable baseline |
| Deep ribbed box | very good per mass | good to very good | ribs align the shear path and distribute side loads | good within 320 mm; inspectable faces | preferred concept |
| Torsion box | good | very good | skins and internal webs close roll loads | more joints/supports and harder cleaning | reserve if B torsion test fails |
| Double-wall monocoque | very good | good to very good | broad interfaces reduce PETG bearing/creep concentration | good if the skins remain one piece; post-process datums | combine with the preferred ribbed concept |

The selected skeleton does not choose wall thickness, rib pitch, infill,
fastener size, or print orientation. Those belong to detailed structural
design after the architecture gate.

## Z-axis comparison

The common screening load is 5 N at 50 mm overhang, producing a 250 Nmm
transverse moment. With 60 mm guide spacing, the idealized rail-couple force
is approximately 4.17 N. A single rail has no separated guide couple and
therefore concentrates pitch/yaw moment in one rail seat and carriage.

| Z option | Benefit | Risk | Disposition |
| --- | --- | --- | --- |
| one MGN12 carriage | lowest mass and simplest print envelope | one reaction line; poor moment closure for an offset spindle | not the primary Z layout |
| dual MGN9 | lower mass, adequate interface width if the seats are stiff | lower section/mounting margin and more alignment sensitivity | retain as a measured lower-mass candidate |
| dual MGN12 | better rail/seat moment margin and load spreading | more mass, width, and PETG interface area | preferred interface candidate; exact class remains open |

The Z carriage is deliberately short: the skeleton uses 40 mm tool travel,
15 mm tool stickout, and 50 mm tool-point overhang as screening values. It
does not maximize Z travel at the expense of the tool loop.

## Y bed, workholding, and probing

The B bed remains fixed while the gantry moves. The architecture reserves a
240 x 190 mm replaceable spoilboard envelope, with a controlled workholding
datum and a conductive probe datum outside the cutting sweep. The probe must
be stowable before cutting, detect an open circuit as a stop condition, and
allow a <=25 mm map grid with a 12.5 mm refinement without moving the board.
The map is valid only for the same clamping state, tool, fixture, and thermal
condition.

The A bed would use the same support and registration concept, but the entire
bed/spoilboard/PCB stack would move. That increases moving mass and cable
fatigue and makes a post-probe movement error a first-order risk. C retains a
fixed bed but makes probe access and cable routing compete with the elevated
XY head.

## Lead-screw placement

The preliminary line is centered between the associated guide lines for all
three axes. Centering the Y screw between the two side rails minimizes
gantry/bed racking. A second Y screw is a contingency only if measured
friction, sag, or torsion requires it; it is not added for symmetry alone.
The screw line is an interface envelope, not a T8x2/T8x4 selection. Axial
bearing, thermal end, nut preload, coupler access, backlash, critical speed,
and motor torque move to Phase 3.

## Skeleton packaging result

The architecture-only build123d skeleton uses the controlled values in
`cad/parameters.py` and includes only reference geometry. Its nominal machine
packaging bounding box is 340 x 290 x 220 mm including reference screw end
margins; this is not a printed-part size or a service-clearance guarantee.
The primary gantry/base bounds remain at or below the preferred 320 mm
one-piece screening dimension.

See [the force-loop study](phase-2-force-loop.md), [the weighted trade
matrix](phase-2-decision-matrix.md), [the Phase 2A structural comparison](phase-2a-structural-comparison.md),
and [the build123d spike report](phase-2-build123d-spike.md). The owner
disposition is recorded in [EDR-006](../decisions/006-phase-2-architecture.md)
and [EDR-007](../decisions/007-phase-2a-structural-comparison.md).
