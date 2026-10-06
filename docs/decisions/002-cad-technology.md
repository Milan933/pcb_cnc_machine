# Engineering decision record: preliminary CAD technology

- **Record ID:** EDR-002
- **Phase:** 5 preparation
- **Status:** preliminary recommendation
- **Date:** 2026-10-06
- **Owner:** project team
- **Affected requirements:** REQ-CAD-001 through REQ-CAD-004

## Decision

Use build123d as the preliminary CAD technology for the project, subject to a
small implementation spike before the parametric skeleton is approved.
CadQuery remains the documented fallback if the spike exposes a blocking
assembly, export, or maintainability issue.

This is a tool choice, not a permission to start detailed mechanical design.

## Context

The authoritative model must be Python-parametric, support individual parts
and a complete assembly, use centralized parameters, and export STEP and STL.
The structure is expected to contain additive-manufacturing-oriented solids
such as ribs, closed sections, monocoques, gussets, and mounting interfaces.

## Alternatives considered

### build123d

The current build123d documentation provides algebra and builder modeling
styles, explicit shape labels and locations, compound-based assembly trees,
and STEP/STL export functions. Its assembly documentation describes parent /
child placement and exporting an assembly as a unit. These features fit a
part-first, deterministic assembly architecture and make it convenient to
construct geometry from shared Python parameters.

### CadQuery

CadQuery is a credible alternative with a mature Workplane/fluent modeling
style, explicit Assembly objects, assembly constraints, and documented STEP
and STL export. It may be preferable if the project needs its particular
constraint workflow, existing examples, or stronger compatibility with a
CadQuery-specific downstream toolchain.

## Reasoning and evidence

build123d is preferred because the expected design work is dominated by
explicit solid composition and repeated parameterized structural features,
rather than by a large constraint-solved assembly. Its assembly tree,
locations, labels, and direct STEP/STL exporters match the planned
parts -> assembly -> validation -> export pipeline.

The decision is intentionally preliminary. Before Phase 5 approval, the
implementation spike must prove:

- a central parameter change updates a representative structural feature;
- a part module can be imported without side effects;
- deterministic placements and meaningful labels survive assembly creation;
- a complete assembly and an individual printable part export to STEP and
  STL;
- the chosen build123d version can support the required collision and
  bounding-volume queries, or an adapter can do so without mesh-first
  modeling;
- the workflow is usable on the project team's actual environment.

## Risks and mitigations

| Risk | Consequence | Mitigation / evidence needed | Owner |
| --- | --- | --- | --- |
| build123d API or assembly behavior changes between versions. | Scripts stop generating or placements change. | Pin the tested version, keep a small export smoke test, and record the version in the release manifest. | project team |
| Collision and printability checks are not available at the desired solid level. | Validation becomes incomplete or mesh-dependent. | Test the required queries during the spike; use an explicit CAD adapter or reconsider CadQuery. | project team |
| The team is more productive in CadQuery. | More modeling errors or slower iteration. | Compare the same small test part and assembly in both tools before freezing the choice. | project team |

## Unresolved questions

- Which build123d release and Python environment will be supported?
- Does the selected release expose all required assembly, collision, and
  export operations without undocumented APIs?
- What STEP metadata and part naming survive the chosen export path?

## Sources

- build123d import/export documentation:
  https://build123d.readthedocs.io/en/stable/import_export.html
- build123d assemblies documentation:
  https://build123d.readthedocs.io/en/latest/assemblies.html
- CadQuery import/export documentation:
  https://cadquery.readthedocs.io/en/latest/importexport.html
- CadQuery assemblies and API reference:
  https://cadquery.readthedocs.io/en/stable/classreference.html

## Validation and review

- [x] Requirements and CAD conventions reflect a parametric source of truth.
- [x] Alternative technology documented.
- [ ] Implementation spike completed.
- [ ] Tested version pinned.
- [ ] Recommendation approved for Phase 5.

## Follow-up

Run the implementation spike after the motion architecture is defined and
before detailed structural components are modeled.
