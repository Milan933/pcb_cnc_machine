# Engineering decision record: Phase 1 quantitative requirements

- **Record ID:** EDR-005
- **Phase:** 1 - Requirements
- **Status:** proposed / engineering review required
- **Date:** 2026-10-06
- **Owner:** project team
- **Affected requirements:** REQ-PCB-*, REQ-SPN-*, REQ-WHL-*, REQ-PROBE-*, REQ-MOT-*, REQ-Z-*, REQ-ENV-006 through REQ-ENV-008, AT-*

## Decision

Adopt the following as the Phase 1 screening baseline, without treating any
value as physically verified:

1. Use a nominal 200 x 150 mm PCB working area, option B, for architecture
   comparison. Do not freeze final tool travel or axis architecture.
2. Use 1 oz copper / 0.035 mm as the primary process reference, while
   covering 0.5-2 oz and 0.8-2.0 mm board thickness in the process envelope.
3. Evaluate 30 degree and 60 degree V-bit isolation tools, with a
   0.05-0.15 mm isolation-depth trial window and 0.10 mm initial coupon depth.
4. Use preliminary machine screening targets of 0.05 mm calibrated XY error,
   0.03 mm repeatability, 0.03 mm backlash, and 0.020 mm tool-point deflection
   under a defined 5 N load. Provisional acceptance limits are looser as
   documented in the requirements.
5. Allocate 0.040 mm to non-compensatable machine Z error and require
   <=0.020 mm target / <=0.030 mm provisional acceptance for post-map surface
   residual.
6. Screen spindle envelopes around 10,000-30,000 rpm, 50-150 W,
   0.30-0.80 kg, approximately 25/40/52 mm body classes, and ER11-class
   tooling. Do not select a spindle.

## Alternatives considered

### Working area

- 160 x 100 mm: lower span and easier PETG printability, but may underserve
  the intended board size.
- 200 x 150 mm: balances useful PCB area and the Voron 350 constraint.
- 250 x 180 mm: offers more board area but consumes print margin and increases
  gantry span, torsion, footprint, and rail/screw length.

### Isolation tool/process

- V-bit: depth-sensitive effective width but small cutting footprint and
  fine-feature capability.
- Small flat end mill: more direct three-dimensional geometry but smaller tools
  are fragile and demand runout/stiffness.
- Broad, deep isolation cut: more tolerant of board height in some cases but
  removes more FR4 and widens the isolation.

### Z compensation

- No map: simpler control but requires a very flat board/fixture and tighter
  mechanical height control.
- Map only: can correct a stable surface but cannot correct cutting deflection,
  tool seating, guide play, or board movement.
- Mechanical datum plus map: selected as the requirements direction because it
  separates structural and process-surface error.

## Reasoning and evidence

JLCPCB's copper guidance gives 1 oz as approximately 35 micrometres and
identifies 0.5 oz, 1 oz, and 2 oz classes. Bantam Tools' PCB guidance
identifies 30 degree engraving bits in 0.003 inch and 0.005 inch tip classes,
measured board/tape thickness, a 0.20 mm default comparator depth, and flat
end mills for holes/outlines. Its published machine specifications provide an
8,500-26,000 rpm, ER11, 50 W typical / 120 W peak comparison point.

Those sources describe different machines and FR-1 workflows. They justify
tool-family and scale comparisons, not direct FR4 performance claims. The
project-specific numbers are derived in
docs/calculations/phase-1-calculations.md and must be tested with coupons.

## Risks and mitigations

| Risk | Consequence | Mitigation / evidence needed | Owner |
| --- | --- | --- | --- |
| The 200 x 150 recommendation is confused with final machine travel. | Clamps, datum access, or probing space are lost. | Keep PCB area and tool travel separate until Phase 2 packaging is complete. | project team |
| V-bit depth or board warp dominates trace width. | Copper remains or isolation becomes too wide. | Use measured board/tape thickness, height maps, depth ladders, and independent surface checks. | project team |
| PETG structure cannot meet the 0.040 mm mechanical Z allocation. | Isolation depth is load- or temperature-dependent. | Use a 5 N tool-point test, creep coupons, short force loops, and redesign before architecture approval. | project team |
| Spindle runout or collet quality dominates small tools. | Fine trace/space targets fail despite good motion tests. | Measure TIR at the tool, test ER11 collets, and separate runout from XY accuracy. | project team |
| Feed windows are treated as final recipes. | Tool breakage, rubbing, heat, or poor FR4 cuts. | Test one variable at a time and replace assumptions with tool-maker data or coupons. | project team |

## Unresolved questions

See the Phase 1 additions in requirements/open-questions.md. Exact stock,
spindle, controller, motor data, process acceptance levels, test load, and
map implementation remain open.

## Validation and review

- [x] Traceable Phase 1 requirement IDs created.
- [x] Calculations and source references documented.
- [x] Automated internal-consistency checks and tests added.
- [x] Acceptance-test plan created.
- [x] Repository audit and existing tests run before commit.
- [ ] Project owner reviews the provisional values.
- [ ] Phase 1 gate is accepted.

## Follow-up

Review this EDR and the linked requirements. Only after Phase 1 acceptance
should Phase 2 compare moving-bed, moving-gantry, or another architecture.
