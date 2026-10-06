# Phase 1 process requirements

This document converts the PCB manufacturing intent into a preliminary
process envelope. It is a requirements baseline for architecture comparison,
not a final tool library or a claim of machine capability.

## Evidence status

- **Known**: directly stated by the project brief or an identified source.
- **Preliminary**: proposed engineering target for trade studies.
- **Assumption**: adopted to enable a calculation and requiring confirmation.
- **Calculated**: derived by the equations in
  docs/calculations/phase-1-calculations.md.
- **Verified**: measured on the eventual machine or a representative coupon.

No Phase 1 value marked preliminary or assumption is physically verified.

## Stock and copper baseline

The initial stock envelope is rigid FR4 or a comparable PCB laminate with
outer copper between 0.5 oz and 2 oz. A 1 oz outer layer is approximately
0.035 mm copper; 0.5 oz and 2 oz are approximately 0.0175 mm and 0.070 mm.
These are planning conversions, not a substitute for measuring the supplied
board. Actual finished copper can vary with plating and fabrication.

For architecture screening, use PCB thickness from 0.8 mm to 2.0 mm. The
actual stock thickness and tape or adhesive thickness must be measured for
each job because the Z datum depends on the assembled stack.

Sources:

- [JLCPCB copper-weight guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight)
- [JLCPCB PCB material and thickness example](https://jlcpcb.com/blog/what-is-a-protoboard-and-why-engineers-use-it)

## Tool families

The machine shall be designed around replaceable tool envelopes rather than a
single assumed cutter:

| Tool family | Phase 1 screening use | Requirement status |
| --- | --- | --- |
| 30 degree V-bit / engraving bit, 0.003-0.005 inch tip class | Fine isolation routing. The included angle and tip size control the effective cut width. | Preliminary candidate; source comparator. |
| 60 degree V-bit | More robust isolation candidate with a wider depth-dependent cut. | Preliminary candidate; compare by coupon. |
| Small flat end mill, approximately 0.20-0.40 mm | Fine three-dimensional trace or clearance work where a V-bit is unsuitable. | Preliminary candidate. |
| Flat end mill near 1/32 inch / 0.794 mm | Holes and outline cutting comparator. | Preliminary candidate; verify tool availability and runout. |
| PCB drill, approximately 0.30-1.00 mm | Through-hole drilling test range. | Preliminary process envelope, not a final drill set. |

Bantam Tools documents 30 degree PCB engraving bits with 0.003 inch and
0.005 inch tip classes, and recommends a flat end mill for holes and board
outlines. That guidance is for a different machine and FR-1 blanks, but it
supports evaluating the same tool families for this project.

Source: [Bantam Tools engraving-bit isolation guide](https://support.bantamtools.com/hc/en-us/articles/115001656913-Engraving-Bit-Isolation-Milling)

## Isolation routing

For an ideal V-bit with included angle theta, depth d below the geometric tip,
and effective tip width t:

    isolation_width = t + 2 * d * tan(theta / 2)

The equation excludes tip radius, tool runout, deflection, burrs, copper
adhesion, and board height variation. It is therefore a geometry calculation,
not a manufactured trace-spacing guarantee.

The first process window is:

- isolation depth: 0.05-0.15 mm;
- initial coupon depth: 0.10 mm;
- full-angle candidates: 30 degrees and 60 degrees;
- initial isolation feed window: 100-600 mm/min;
- initial process sweep: 100, 200, and 300 mm/min at several depths;
- starting spindle-speed window: 12,000-26,000 rpm, inside the broader
  machine requirement of 10,000-30,000 rpm.

The 0.05-0.15 mm depth is a provisional FR4 starting window: it removes a
nominal 1 oz copper layer while limiting unnecessary glass-epoxy removal.
Bantam's PCB software uses 0.20 mm as a default comparator depth and warns
that deeper V-bit cuts become wider; this project shall test shallower FR4
depths rather than adopting 0.20 mm as a requirement.

Requirements:

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-PCB-ISO-001 | The process shall support a repeatable isolation-depth window of 0.05-0.15 mm for initial FR4 trials. | Preliminary |
| REQ-PCB-ISO-002 | The CAM and motion system shall permit depth increments of 0.01 mm or finer as commanded increments; this is not an accuracy claim. | Preliminary |
| REQ-PCB-ISO-003 | The design shall support a 30 degree fine-isolation tool and a wider-angle comparison tool without changing the machine datum architecture. | Preliminary |
| REQ-PCB-ISO-004 | The process shall provide a coupon ladder at multiple depths and feeds before a trace/space capability is claimed. | Known process rule |
| REQ-PCB-ISO-005 | The tool path shall distinguish trace geometry, clearance width, and copper thickness; a generic accuracy number is not sufficient. | Known process rule |

## Geometric accuracy, repeatability, and error sources

These are separate requirements:

- **Geometric accuracy**: calibrated coordinate error over the working area.
- **Repeatability**: spread when returning to the same coordinate from the same
  or alternating directions.
- **Backlash**: reversal-dependent offset that appears when motion direction
  changes.
- **Tool-point deflection**: load-dependent displacement; calibration cannot
  remove it.
- **Spindle runout**: radial or axial tool motion caused by spindle, collet,
  tool, and seating; it is not controller resolution.
- **PCB height variation**: board, tape, spoilboard, and clamping variation;
  some of it can be measured and compensated with a map.

The proposed numerical targets are in
requirements/phase-1-motion-structure.md and
requirements/phase-1-z-error-budget.md.

## Drilling

The initial drilling requirement covers 0.30-1.00 mm drill diameters and
0.8-2.0 mm PCB thickness. The machine shall provide:

- axial tool alignment and a rigid spindle/tool interface;
- a supported board and sacrificial surface below every hole;
- tool length and board-top datum control;
- controlled plunge and retract, with a peck strategy available for small
  drills or poor chip evacuation;
- XY registration repeatability separate from hole-size measurement;
- spindle runout measurement using the actual collet and drill.

The initial drilling feed window is 30-200 mm/min. It is a test window derived
from small-tool chip-load assumptions, not a supplier recommendation. The
controller shall permit slower probing and drilling moves independently from
rapid travel.

Requirements:

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-PCB-DRL-001 | The machine shall support a measured and repeatable PCB-top datum before drilling. | Preliminary |
| REQ-PCB-DRL-002 | Drill tests shall report center registration, hole diameter, breakout, burrs, and tool condition separately. | Known process rule |
| REQ-PCB-DRL-003 | The drilling cycle shall support controlled plunge, retract, and an optional peck strategy. | Preliminary |

## Outline/profile cutting

Use a flat end mill rather than a V-bit for the primary outline comparator.
The initial screening tool is near 1/32 inch / 0.794 mm, with smaller tools
considered only when the board geometry requires them. The machine shall
support multiple passes through the board plus a sacrificial spoilboard depth,
secure board support through the final pass, chip/dust extraction, and a
registration method that remains valid after the cut is complete.

The initial outline feed window is 100-800 mm/min. Begin at the low end until
tool load and chip evacuation are measured.

Requirements:

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-PCB-OUT-001 | Outline cutting shall support 0.8-2.0 mm board thickness plus a controlled spoilboard penetration allowance. | Preliminary |
| REQ-PCB-OUT-002 | The board shall remain supported and registered during the final outline pass; tabs or an equivalent retention method shall be evaluated. | Preliminary |
| REQ-PCB-OUT-003 | Outline tests shall report dimensional error, corner behavior, burrs, and board movement separately. | Known process rule |

## Spindle and speed requirements

Bantam's published PCB-mill comparator lists 8,500-26,000 rpm, 50 W typical /
120 W peak consumption, an ER-11 collet for 1/8 inch shanks, and a 0.25 mm
smallest recommended end mill. The values below intentionally define a
screening envelope rather than selecting a Bantam-like spindle.

| ID | Requirement | Proposed envelope | Status |
| --- | --- | --- | --- |
| REQ-SPN-001 | Usable speed range for small PCB tools | 10,000-30,000 rpm; initial process trials 12,000-26,000 rpm | Preliminary |
| REQ-SPN-002 | Tool-point radial runout | Target <=0.010 mm TIR; provisional acceptance maximum <=0.020 mm TIR at the measured tool shank | Preliminary, must be measured |
| REQ-SPN-003 | Spindle power class | 50-150 W continuous/equivalent screening class; more power is not automatically better for PCB work | Assumption |
| REQ-SPN-004 | Spindle mass class | 0.30-0.80 kg screening envelope; architecture shall test a heavier class only with a tool-point stiffness justification | Assumption |
| REQ-SPN-005 | Diameter classes | Compare approximately 25 mm, 40 mm, and 52 mm body classes for mount stiffness, mass, and access | Preliminary candidates |
| REQ-SPN-006 | Tool holding | Evaluate ER11-class tooling for 3.175 mm / 1/8 inch shanks and smaller matched collets; verify actual collet range and runout with the selected supplier | Preliminary requirement |
| REQ-SPN-007 | Axial seating | Establish a separate axial seating/runout measurement; radial runout alone does not prove Z accuracy | Known process rule |

Sources:

- [Bantam Tools PCB mill specifications](https://content.bantamtools.com/tech-specs-desktop-pcb-milling-machine)
- [Bantam Tools speeds and feeds guidance](https://support.bantamtools.com/hc/en-us/articles/7750017313811-Speeds-Feeds-Overview)

## Workholding, spoilboard, probing, and mapping

The machine shall use a replaceable or serviceable spoilboard with a defined
machine datum, board datum, replacement method, and flatness verification.
The spoilboard is a process surface, not an unmeasured structural reference.

Tape or adhesive workholding may be evaluated for thin boards. A single,
uniform layer is required for the baseline test; overlap, wrinkles, bubbles,
and debris are prohibited in the test setup. Tape thickness shall be measured
and included in the Z setup. Bantam reports approximately 0.076 mm for common
Scotch tape and 0.15-0.20 mm for a high-strength tape class, while also
warning that actual thickness must be measured.

Conductive Z probing shall provide:

- a probe input compatible with the controller;
- a stable probe clip or conductive reference that cannot enter the toolpath;
- an electrical path from the copper surface or a defined conductive plate to
  the probe circuit;
- a failure response when the circuit is open;
- a safe retract and a way to stow the probe before cutting.

Copper is conductive, but solder mask, oxide, adhesive, contamination, and
isolated copper regions can break the electrical path. The probing method
must not assume that every visible PCB surface is electrically continuous.

The initial height-map requirement is a maximum 25 mm grid spacing across the
selected PCB area, with a 12.5 mm refinement option for regions that fail the
interpolation check. Map residual error target is <=0.020 mm and provisional
acceptance is <=0.030 mm at independent check points.

Requirements:

| ID | Requirement | Status |
| --- | --- | --- |
| REQ-WHL-001 | Replaceable spoilboard and PCB workholding shall preserve a repeatable machine/board datum. | Preliminary |
| REQ-WHL-002 | Tape or adhesive workholding shall be uniform, measured, and removable without changing the structural datum. | Preliminary |
| REQ-PROBE-001 | Conductive Z probing shall detect an open circuit as a stop condition. | Preliminary safety/process requirement |
| REQ-PROBE-002 | The probe shall be stowed outside the swept tool volume before cutting. | Preliminary safety/process requirement |
| REQ-PROBE-003 | Height mapping shall support <=25 mm nominal grid spacing and a finer 12.5 mm refinement. | Preliminary |
| REQ-PROBE-004 | A map shall record board/fixture identity, datum, grid, probe result, and job association; stale maps shall be rejected. | Preliminary |

Sources:

- [Bantam PCB probing system](https://support.bantamtools.com/hc/en-us/articles/115001829134-Installing-and-Using-the-PCB-Probing-System)
- [Bantam material setup and tape thickness](https://support.bantamtools.com/hc/en-us/articles/115001656533-Set-Up-Your-Material)
- [Bantam FR-1 fixturing and tool guidance](https://support.bantamtools.com/hc/en-us/articles/360057134214-FR-1-PCB-Blanks)
- [Bantam PCB troubleshooting for flatness](https://support.bantamtools.com/hc/en-us/articles/115001656893-Troubleshooting-Your-Circuit-Board)
