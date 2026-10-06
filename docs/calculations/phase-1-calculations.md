# Phase 1 calculations and derivations

This document records the equations behind the quantitative requirements.
Inputs are either user requirements, identified comparator data, or explicit
screening assumptions. Results are not machine measurements.

## Copper thickness

The planning conversion is:

    1 oz/ft2 approximately 0.035 mm
    0.5 oz/ft2 approximately 0.0175 mm
    2 oz/ft2 approximately 0.070 mm

The actual copper and plating stack must be measured or obtained from the
board supplier. The calculation only establishes why 0.05-0.15 mm is a
reasonable isolation-depth trial window.

## V-bit width and depth sensitivity

For included angle theta, depth d, and tip width t:

    w = t + 2 d tan(theta / 2)
    dw/dd = 2 tan(theta / 2)

Ignoring the tip width:

| Included angle | Width at 0.05 mm | Width at 0.10 mm | Width at 0.15 mm | Width change per 0.01 mm depth |
| ---: | ---: | ---: | ---: | ---: |
| 30 degrees | 0.0268 mm | 0.0536 mm | 0.0804 mm | 0.0054 mm |
| 60 degrees | 0.0577 mm | 0.1155 mm | 0.1732 mm | 0.0115 mm |

The effective width also includes the tool tip, runout, deflection, burrs, and
the fact that the copper/FR4 cut is not ideal geometry. This is why the
requirements separate V-bit angle, depth, spindle runout, height variation,
and tool-point deflection.

## Commanded screw resolution

For a motor with N full steps/revolution, M commanded microsteps/full step,
and screw lead L:

    nominal_command_increment = L / (N M)

Using the conditional example N = 200, M = 16:

| Lead | Nominal increment |
| ---: | ---: |
| 2 mm/rev | 0.000625 mm |
| 4 mm/rev | 0.00125 mm |

These numbers do not establish positioning accuracy. They omit motor torque,
driver current, microstep nonlinearity, screw pitch error, backlash,
compliance, guide play, and controller step-rate limits.

## Feed-rate screening windows

For a cutter with flute count n, spindle speed r, and assumed chip load c:

    feed = r n c

The initial chip-load assumptions are 0.005-0.015 mm/tooth for small PCB
cutters. They are intentionally broad and must be replaced with tool-maker
data or coupon results.

- A single-flute isolation tool at 12,000-26,000 rpm gives
  60-390 mm/min; the rounded initial trial window is 100-600 mm/min.
- A two-flute outline tool at the same speeds gives 120-780 mm/min; the
  rounded initial trial window is 100-800 mm/min.
- Drilling uses a separate 30-200 mm/min window with controlled retract or
  peck behavior rather than applying the milling chip-load equation blindly.

Bantam's published comparator allows much larger feed settings and says that
small tools, high spindle speed, low pass depth, secure fixturing, and
experimentation matter. It is used here as a scale reference, not as a direct
FR4 prescription.

## Tool-point stiffness

With a 5 N screening load and 0.020 mm tool-point deflection target:

    minimum screening stiffness = 5 N / 0.020 mm = 250 N/mm

The test must state load direction, tool-point location, spindle/tool state,
measurement instrument, and whether the board/spoilboard is included. A
static stiffness result does not establish dynamic cutting performance.

## Z budget

The six non-compensatable allocations are:

    0.015 + 0.005 + 0.005 + 0.005 + 0.005 + 0.005 = 0.040 mm

Board and spoilboard variation has a separate 0.100 mm map-coverage allowance.
The proposed post-map residual is <=0.020 mm target and <=0.030 mm provisional
acceptance. These are separate budgets, not a claim that all error terms can
be added or removed by software.

## Envelope packaging assumption

For an option with PCB working area W x D and 60-100 mm total packaging
allowance per axis:

    screening guide/screw envelope = working area + 60-100 mm

This produces the A/B/C comparison in requirements/phase-1-envelope-trade.md.
The allowance must be replaced by actual carriage, bearing, hard-stop, clamp,
probe, and service dimensions during Phase 2.

## Source references

- [JLCPCB copper-weight guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight)
- [Bantam PCB engraving-bit guide](https://support.bantamtools.com/hc/en-us/articles/115001656913-Engraving-Bit-Isolation-Milling)
- [Bantam PCB mill specifications](https://content.bantamtools.com/tech-specs-desktop-pcb-milling-machine)
- [Bantam speeds and feeds overview](https://support.bantamtools.com/hc/en-us/articles/7750017313811-Speeds-Feeds-Overview)
- [Bantam archived comparator ranges](https://support.bantamtools.com/hc/en-us/articles/115001658374-Speeds-and-Feeds-Archive-reference)
