# Engineering decision record: Phase 2A structural comparison

- **Record ID:** EDR-007
- **Phase:** 2 - Architecture supplement
- **Status:** proposed / owner review required
- **Date:** 2026-10-06
- **Owner:** project team
- **Affected requirements:** REQ-ARCH-001 through REQ-ARCH-005,
  REQ-FN-003, REQ-FN-004, REQ-MOT-001, REQ-MOT-004, REQ-MOT-005,
  REQ-Z-001 through REQ-Z-004, REQ-PETG-001 through REQ-PETG-006

## Decision proposed for owner review

Do not accept EDR-006 yet. Reopen only A versus B using the focused Phase 2A
comparison. The current calculated structural baseline is **A: fixed gantry
with moving Y bed**, with **B: moving Y gantry with fixed bed** retained as a
credible process/usability alternative. This is a provisional evidence
direction, not an architecture freeze, hardware selection, production CAD
authorization, or Phase 3 start.

EDR-006 remains proposed. This record supplements and reopens its close
original B-versus-A result; it does not silently accept, supersede, or erase
the original decision record.

## Context and evidence boundary

The original Phase 2 matrix scored B 77.0 and A 73.6. Phase 2A uses the same
200 x 150 mm PCB baseline, 220 x 170 x 40 mm screened tool travel, generic
spindle envelope, guide references, PETG-first geometry constraints, and 5 N
load philosophy. A and B were optimized independently:

- A uses a deep integrated fixed U/monocoque concept, wide supports, short
  joints, neutral rail paths, and a light moving PCB bed.
- B uses a deep ribbed moving crossbeam, explicit side interfaces, a fixed
  PCB bed, and a centered Y screw with symmetric guide assumptions.

The analytical model is transparent and reproducible: equivalent beam
bending, thin-wall torsion, side/support bending, Z carriage compliance,
equivalent joint compliance, and asymmetric-force racking. It is not FEA and
does not claim measured PETG behavior.

## Calculated result

| Result | A | B |
| --- | ---: | ---: |
| Total tool-point displacement under 5 N | 0.0111 mm | 0.0269 mm |
| Target / first-prototype acceptance | pass / pass | miss / pass |
| Moving mass | 1.24 kg | 3.95 kg |
| Y screw design force | 1.498 N | 2.540 N |
| Racking edge displacement estimate | 0.0025 mm | 0.0050 mm |
| Revised matrix score | 78.0 | 75.2 |

A is the current provisional structural lead in this model. B wins the
calibration-and-usability-heavy sensitivity case (80.625 versus A 72.500), so
the matrix does not remove the need for physical evidence.

## Alternatives and risks

The alternatives remain A and B; C is not included in this focused study.
The main risks are PETG anisotropy and conditioning, rail-seat and joint
stiffness, heat-set insert and through-bolt creep, spindle mass/overhang,
actual Y friction and cable drag, and load direction. A's main process risk is
moving the PCB datum after probing. B's main structural risk is cyclic side
interface preload and racking.

## Required evidence before freeze

Print and measure representative beam-bending, torsion-box, rail-seat,
heat-set-insert creep, and through-bolt creep coupons. Then test representative
A and B force loops under 5 N in X/Y/Z with the spindle envelope, cable/probe
state, and PCB workholding installed. Record thermal and conditioning state,
tool-point displacement, racking, permanent set, datum movement, and map
validity. Feed fitted values back into `cad/parameters.py` and rerun the study.

The full method is in
[phase-2a-physical-validation.md](../architecture/phase-2a-physical-validation.md).

## Validation and review

- [x] Phase 2A inputs centralized in `cad/parameters.py`.
- [x] A/B analytical equations and contribution percentages recorded.
- [x] Dynamic moving-mass, screw-force/torque, resonance-risk, and racking screens recorded.
- [x] PETG thermal/creep/alignment, manufacturing, probing, workholding, and service trade recorded.
- [x] Revised matrix contains no duplicate generic bending criterion; sensitivity is implemented and tested.
- [x] Physical coupon plan and model-feedback gate recorded.
- [x] Architecture-only optimized A/B review skeleton and interference policy implemented.
- [x] No production CAD or manufacturing STEP/STL generated.
- [ ] Representative coupons and A/B 5 N force-loop tests completed.
- [ ] Owner reviews EDR-006 together with this proposed supplement.

## Gate

This record remains **proposed**. The architecture cannot freeze and Phase 3
cannot begin until the owner disposition is recorded and the required
physical evidence is reviewed.
