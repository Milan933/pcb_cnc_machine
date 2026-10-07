---
name: cad-hardware-integration
description: Integrate commercial and owner-supplied hardware into generic CAD assemblies with provenance, confidence levels, stable IDs, critical dimensions, interface models, and reproducible local references.
---

# CAD hardware integration

Use this skill when a design depends on a purchased, inherited, or externally sourced component. Hardware geometry is evidence with a confidence level, not decoration.

## Evidence priority

Prefer, in order:

1. official CAD from the manufacturer with clear redistribution terms;
2. official dimensional drawing or datasheet;
3. manufacturer dimensions and application guidance;
4. reputable distributor CAD with provenance and cross-checks;
5. verified community model with independent dimensional checks;
6. locally generated reference, interface, or envelope model.

If redistribution rights are unclear, preserve the URL, original filename if known, retrieval date, license/access status, checksum when a file is obtained, and a local parametric model with only the geometry needed for the design. Do not silently copy third-party CAD into a public repository.

## Representation levels

Classify every model as one of:

- **VISUAL MODEL:** appearance or context only; no fit or load claim.
- **ENVELOPE MODEL:** outer size, keep-out, travel, or massing screen.
- **INTERFACE MODEL:** mounting faces, holes, axes, clearances, and service interfaces are represented.
- **VERIFIED MECHANICAL MODEL:** critical dimensions and behavior have been checked against a controlled source or measured hardware.

Do not promote a lower-confidence representation by implication. A model can be interface-accurate while omitting cosmetic features.

## Persistent library contract

Use a stable component ID for every reusable hardware model. Its record should include category, manufacturer, part number, source URL, source type, local model path, format, license/redistribution status, retrieval date, verification status, critical dimensions, confidence, and notes. Assemblies should reference the ID rather than a temporary filename or a copied solid.

Verify dimensions that control fit, motion, load, service access, and datum transfer. Record owner-measured values separately from catalog values, and keep unresolved dimensions parametric. Reuse the same library model everywhere so revisions and confidence changes propagate visibly.

## Good vs bad

**Bad:** Download a visually accurate bearing model from an unknown CAD site, rename it, and use its unverified faces as assembly datums.

**Good:** Record the supplier and source, classify the model, verify bore/OD/width and the retaining interface, keep a lightweight local interface model when license terms are unclear, and expose the confidence in the assembly manifest.

Use [mechanical-cad-design](../mechanical-cad-design/SKILL.md) for local frames and [cad-design-review](../cad-design-review/SKILL.md) for evidence gates.
