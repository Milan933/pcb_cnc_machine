# Phase 2 force-loop and compliance study

This is a screening model for the three architecture candidates. It uses the
same load and envelope for each option and deliberately stops at relative
compliance and load-path identification. It is not FEA and does not claim a
machine deflection result.

## Common load case

The accepted Phase 1 static screening load is 5 N at the process tool point.
The Phase 2 design point uses the Phase 1 preferred 50 mm tool-point
overhang:

```text
M_tool = F * e = 5 N * 50 mm = 250 Nmm = 0.25 Nm
```

For two guide reaction lines separated by 60 mm:

```text
F_guide_couple = M_tool / s = 250 Nmm / 60 mm = 4.17 N
```

This is an ideal static couple calculation. It excludes preload loss,
friction, bearing clearance, local PETG compliance, spindle mass, cable load,
and dynamic cutting forces. A single rail does not get this separated couple;
its carriage and rail seat must react the full moment.

For an order-of-magnitude beam comparison only, use an effective PETG modulus
of 2,000 N/mm² and an idealized 40 x 60 mm rectangular section:

```text
I = b*h^3/12 = 40*60^3/12 = 720,000 mm^4
delta_ideal = F*L^3/(48*E*I) for L = 280 mm
            ~= 0.0016 mm
```

The last number is an ideal section-only result, not a predicted machine
deflection. Printed skins, layer orientation, rail seats, fastener bearing,
side joints, and creep can dominate it. The useful conclusion is that
increasing section depth and closing the torsion path matter more than
claiming a high infill percentage.

## Complete force-loop traces

| Candidate | Force loop from tool back to PCB | Main cantilever / bend | PETG joint and interface risk | Dominant compliance to test |
| --- | --- | --- | --- | --- |
| A fixed gantry / moving Y bed | tool -> spindle -> mount -> Z carriage -> X carriage/gantry -> fixed side supports -> base -> Y rails/screw -> moving bed/spoilboard -> PCB -> tool | bed pitch and support between the two Y rails; gantry is the favorable portion | bed rail seats, screw nut mount, fixed gantry-to-base joints, and board support | moving bed support plus fixed gantry joint; board datum changes if the bed settles after probing |
| B moving gantry / fixed bed | tool -> spindle -> mount -> Z carriage -> X carriage -> deep crossbeam -> two gantry side interfaces -> Y rails/screw/base -> fixed bed/spoilboard -> PCB -> tool | crossbeam roll and side-interface pitch/yaw while the gantry translates | two moving side interfaces, Y rail seats, crossbeam skins, and distributed screw loads | gantry torsion and PETG side joints; verify tool point in X/Y/Z under the 5 N load |
| C fixed gantry / fixed bed / moving XY head | tool -> spindle -> mount -> Z carriage -> moving XY head -> elevated Y cross-slide -> fixed gantry -> base -> fixed bed/spoilboard -> PCB -> tool | elevated head stack and carriage overhang | extra guide seats, cross-slide joints, moving-head datum, and cable/probe routing | moving XY head pitch/yaw; the fixed bed does not remove the long head loop |

The nominal path-length figures below are skeleton bookkeeping values, not
measured center-of-compliance distances:

| Candidate | Nominal loop-length screen | Relative to B |
| --- | ---: | ---: |
| A | approximately 360 mm | 1.09 |
| B | approximately 330 mm | 1.00 |
| C | approximately 470 mm | 1.42 |

The B result is favorable because the fixed bed closes the datum side of the
loop while the moving gantry can keep the Z carriage near the beam. Its risk
is not loop length alone: a shallow or poorly joined beam would lose the
benefit through torsion.

## Direction-specific evidence plan

The architecture gate shall not accept one bulk displacement number. The
representative B gantry and Z interface need these tests before detailed
structural release:

1. Apply 5 N in X at the tool point and measure tool-point displacement and
   gantry roll.
2. Apply 5 N in Y and separate crossbeam bending from side-interface yaw.
3. Apply 5 N in Z and separate Z guide/screw compliance from bed/support
   motion.
4. Repeat after a representative PETG conditioning/preload interval to
   expose creep and insert/through-bolt preload loss.
5. Repeat with the spindle envelope, cable routing, probe stowed, and PCB
   workholding installed; otherwise the test is only a bare-frame check.

The target is <=0.020 mm at the tool point under the defined test load, with
<=0.030 mm as first-prototype acceptance. The Phase 1 non-compensatable Z
budget remains 0.040 mm; a height map may not be used to hide load-dependent
deflection, guide play, spindle/tool seating error, or board movement.

## Compliance mitigations carried into the skeleton

- 60 mm Z guide spacing and a centerline screw are explicit reference
  interfaces.
- X and Y screws are centered between separated guide lines to reduce racking.
- B uses a deep 60 mm section-depth screening bound rather than an aluminium
  extrusion cross-section.
- The B gantry is sized for a closed/deep-ribbed monocoque with distributed
  side loads; detailed wall and rib geometry is intentionally absent.
- The bed is fixed, so workholding and height mapping do not ride on a moving
  spoilboard.
- The skeleton records expected interfaces separately from unexpected solid
  overlaps; the build123d spike reports zero unexpected overlaps for A, B,
  and C.
