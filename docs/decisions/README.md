# Engineering decision records

Use [000-template.md](000-template.md) for every major phase decision.
Records are append-only in intent: supersede an old record rather than
silently rewriting its rationale.

Current records:

- [EDR-001: foundation before geometry](001-foundation-scope.md)
- [EDR-002: preliminary CAD technology](002-cad-technology.md)
- [EDR-003: initial skill-set review](003-skill-set-review.md)
- [EDR-004: public repository and publication boundary](004-repository-publication.md)
- [EDR-005: Phase 1 quantitative requirements](005-phase-1-requirements.md)
- [EDR-006: Phase 2 architecture](006-phase-2-architecture.md) - accepted by
  the owner with the Phase 2A A-baseline amendment; detailed motion remains open
- [EDR-007: Phase 2A structural comparison](007-phase-2a-structural-comparison.md)
  - accepted as the Phase 2A boundary and baseline; physical evidence remains open
- [EDR-008: Phase 3 motion system](008-phase-3-motion-system.md) - owner-
  accepted motion-class baseline; exact hardware and physical evidence remain
  open
- [EDR-009: Phase 3A compact packaging](009-phase-3a-compact-packaging.md) -
  owner-accepted P2 packaging baseline; exact dimensions and physical evidence
  remain open
- [EDR-010: PETG fastening and structural modularity](010-petg-fastening-strategy.md)
  - owner-directed working strategy for Phase 4; insert dimensions and physical
  joint evidence remain open; does not authorize production CAD
- [EDR-011: Phase 4 preliminary structural concept](011-phase-4-preliminary-structural-concept.md)
  - accepted 2026-10-06 as the preliminary structural architecture baseline;
  physical evidence and production release remain blocked; the later EDR-014
  controls the first Phase 5 candidate batch
- [EDR-012: Phase 4A structural optimization](012-phase-4a-structural-optimization.md)
  - accepted 2026-10-06 as the preliminary O2 architecture baseline; physical
  evidence and production release remain blocked; the later EDR-014 controls
  the first Phase 5 candidate batch
- [EDR-013: Hardware procurement / measurement freeze](013-hardware-procurement-measurement-freeze.md)
  - proposed next-stage freeze; class quantities and samples are defined, but
  measured hardware interfaces are not manufacturing-ready
- [EDR-014: Phase 5 first base-pair manufacturing CAD](014-phase-5-base-pair-manufacturing-cad.md)
  - owner-authorized first real printable batch; `PROTOTYPE-STL` only, with
    provisional hardware interfaces and an explicit stop for owner review
- [EDR-015: Phase 5 complete virtual machine](015-phase-5-complete-virtual-machine.md)
  - owner-authorized continuation through the complete virtual machine and
    all 19 candidate structural parts; physical evidence, measured interfaces,
    and release remain open

The ten-phase workflow requires a reviewed record for each phase. Future phase
records are intentionally not fabricated before their evidence exists.
