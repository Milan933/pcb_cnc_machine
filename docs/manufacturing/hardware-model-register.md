# Phase 5 hardware model and source register

The master assembly uses locally derived interface/envelope geometry. No
third-party CAD file is committed when redistribution permission is unclear.
Each source below is a dimensional reference, not proof that the owner's
component matches it.

## Register

| Component | Source / representative | Local model | Classification | Confidence / action |
| --- | --- | --- | --- | --- |
| X/Y guide | [HIWIN MG catalog](https://hiwin-linearmotion.com/images/products/linear-guide/mg-series/mg.pdf), MGN12/MGN12H | rail section, hole pattern screen, carriage envelope | `REFERENCE-CAD` | High dimensional reference; measure rail, block, preload, and hole stations |
| Z guide | [HIWIN MG catalog](https://hiwin-linearmotion.com/images/products/linear-guide/mg-series/mg.pdf), MGN9/MGN9H | rail and carriage envelope | `REFERENCE-CAD` | High family reference; exact variant remains open |
| X/Y screw | no supplier selected; T8x4 class | non-helical 8 mm / journal envelope | `ENVELOPE-ONLY` | Measure lead, starts, journals, straightness, nut, and axial stack |
| Z screw | no supplier selected; T8x2 class | non-helical 8 mm / journal envelope | `ENVELOPE-ONLY` | Measure gravity-hold, backlash, and axial support |
| Anti-backlash nuts | no supplier selected | body/flange screening envelope | `PROVISIONAL` | Do not publish supplier-specific fit before measurement |
| 608 bearings | [SKF 608-2RSH reference](https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-608-2RSH) | 8 x 22 x 7 mm annular envelope | `REFERENCE-CAD` | Measure actual bearing stack and fixed/floating arrangement |
| Flexible couplers | [MISUMI reference family](https://my.c.misumi-ec.com/book/MYS_EconomySeries_e-promobook202308/files/basic-html/page239.html) | representative 5-to-8 mm bore, 20 x 30 mm envelope | `REFERENCE-CAD` | Measure bores, length, set-screw access, and axial float |
| Owner NEMA17 stock | owner hardware; no single model assumed | 42.3 mm frame, 31 mm mounting pitch, 5 mm shaft screen, 40-48 mm body | `ENVELOPE-ONLY` | **OWNER-SUPPLIED - DO NOT BUY**; characterize stock before axis assignment |
| Arduino Mega | [Arduino Mega 2560 Rev3 datasheet](https://docs.arduino.cc/resources/datasheets/A000067-datasheet.pdf) | 101.52 x 53.3 x 1.6 mm board plus connector envelope | `REFERENCE-CAD` | Owner board is intended platform; verify revision and connectors |
| CNC Shield | owner hardware; exact revision unknown | 100 x 60 x 18 mm provisional board/driver volume | `PROVISIONAL` | **OWNER-SUPPLIED - DO NOT REPLACE** absent validated limitation; identify revision and drivers |
| ER11 spindle candidate | [SycoTec 5045 AC-ER11](https://sycotec.eu/en/product/5045-ac-er11/) | local 45 x 140 mm derived envelope | `REFERENCE-CAD` | Candidate only; official STEP remains external because reuse rights are unclear |
| Limit switch | [Omron D2F dimensional datasheet](https://omronfs.omron.com/en_US/ecb/products/pdf/en-d2f.pdf) | body, lever, and mounting envelope | `REFERENCE-CAD` | Verify actual switch, actuation, connector, and bracket |
| Conductive probe | no supplier selected | touch plate, terminal, and cable-entry concept | `PROVISIONAL` | Verify electrical circuit, contact, repeatability, and service access |

## Repository treatment

- The public repository contains the parameterized local derived models in
  [`cad/hardware/master_hardware.py`](../../cad/hardware/master_hardware.py)
  and this traceability register.
- Supplier CAD is not mirrored into the repository. The register records the
  source and reuse decision; local geometry is rebuilt from controlled
  dimensions and labeled as reference, envelope-only, or provisional.
- A source with a downloadable CAD file is not automatically a redistribution
  license. The official SycoTec CAD is therefore used only as an external
  investigation lead at this stage.

## Owner hardware identification boundary

The controller record is now known, not generic:

`OWNER-SUPPLIED - ARDUINO MEGA + CNC SHIELD`

Still unresolved are the exact Shield revision, installed driver modules,
microstep jumper configuration, motor-current capability, supply-voltage
capability, cooling, limit inputs, probe input, spindle PWM/control outputs,
and GRBL-compatible firmware/configuration strategy. Record these in
[`hardware-identification-sheets.md`](../../requirements/hardware-identification-sheets.md)
before wiring or firmware is frozen.

The motors are also known as owner stock, not a purchase gap. The structural
interface intentionally remains generic. For representative candidates,
record model/label, body length, shaft diameter/length, step angle, current,
resistance, connector/pinout, torque class, and mechanical condition. Assign
normal suitable stock to X/Y and the strongest electrically compatible stock
to Z. Do not infer torque from frame size.

## Confidence vocabulary

| Label | Meaning |
| --- | --- |
| `REFERENCE-CAD` | Credible public dimensional source exists; actual hardware still needs verification |
| `ENVELOPE-ONLY` | Project-level interface screen with no supplier-specific model claim |
| `PROVISIONAL` | Geometry exists to enable assembly/clearance review, but the interface or source is materially unresolved |
| `HARDWARE-VALIDATED` | Not used by this Phase 5 package; requires measured owner hardware and physical evidence |

The current master is therefore a `PROTOTYPE-STL` candidate and never a
`HARDWARE-VALIDATED` or `RELEASED` artifact.
