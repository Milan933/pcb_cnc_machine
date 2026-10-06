# Engineering decision record: public repository and publication boundary

- **Record ID:** EDR-004
- **Phase:** Foundation / repository preparation
- **Status:** accepted for this foundation commit
- **Date:** 2026-10-06
- **Owner:** project team
- **Affected requirements:** REQ-CAD-001 through REQ-VAL-003

## Decision

Treat https://github.com/Milan933/pcb_cnc_machine.git as the canonical public
repository for the local working tree at D:\pcbCNC. Track source-of-truth
engineering content and keep temporary exports, caches, credentials, and
machine-specific files out of publication.

Reviewed manufacturing files may later be published only in the designated
generated/*/release/ directories after validation, a source-revision
reference, a manifest, and review evidence exist.

## Alternatives considered

1. Keep the project local or private until the mechanical design is complete.
2. Publish all generated CAD files automatically as they appear.
3. Use the specified public repository with explicit artifact classes and
   pre-push checks.

## Reasoning and evidence

The user explicitly designated the GitHub repository as public and canonical.
Public visibility makes secret exclusion and reproducibility release
requirements rather than optional cleanup. The source foundation is
appropriate for publication; detailed parts and manufacturing releases remain
out of scope until their validation gates exist.

The local repository did not exist before this task. It was initialized on
main with only the canonical origin. The remote currently exposes no refs, so
the first foundation commit will establish the branch history.

## Risks and mitigations

| Risk | Consequence | Mitigation / evidence needed | Owner |
| --- | --- | --- | --- |
| A local credential is added by accident. | Public disclosure and possible account compromise. | .gitignore rules, non-leaking audit, staged diff review, and stop-on-finding policy. | project team |
| Temporary STEP/STL output is mistaken for a release. | Unreviewed or irreproducible manufacturing artifact is published. | Ignore development outputs and require release directories, validation, manifest, and review. | project team |
| A future clone depends on files outside Git. | Design cannot be reproduced or audited. | Document dependencies and commands; keep machine-specific configuration nonessential. | project team |

## Unresolved questions

- Which CI or hosted secret-scanning service should supplement the local audit?
- What export manifest schema and release-review checklist should be required
  when manufacturing files exist?
- Which dependency lock and supported Python/CAD versions will be frozen
  during the CAD implementation spike?

## Validation and review

- [x] Canonical origin configured.
- [x] Public-boundary documentation created.
- [x] .gitignore reviewed and publication exceptions documented.
- [x] Non-leaking candidate audit passed.
- [ ] Project owner reviews the first public commit.

## Follow-up

Add CI and the release manifest schema before the first reviewed STEP/STL
publication. Do not create a version tag for this foundation commit.
