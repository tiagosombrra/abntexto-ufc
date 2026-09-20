# Repository maintenance roadmap

This document is the current durable map for repository-wide maintenance and organization work. The authoritative tracking issue is #359.

It does not redefine release state. Publication and development-line facts remain owned by `release/v3-release-candidate.json` and `docs/RELEASE-STATE.md`.

## Invariants

- Published v3.0.4 source, annotated tag, GitHub Release assets and checksums remain immutable.
- CTAN follow-up remains tracked by issue #356 until external acceptance/publication is confirmed.
- `abntexto-ufc.cls` remains the canonical project-owned runtime at repository root.
- Historical evidence under `docs/history/v3/` and `release/history/v3/` is not reorganized retroactively merely for aesthetics.
- Every material phase uses a bounded branch/PR, records checks and carries unresolved findings forward.
- Structural changes must reduce path coupling before moving large groups of files.

## Phase map

| Phase | Scope | Current state |
|---|---|---|
| 0 | v3.0.4 CTAN external closeout | waiting for external CTAN acceptance under #356 |
| 1 | metadata consistency and anti-drift | in review — PR #360, tracked by #359 |
| 2 | recursive discovery and path-decoupling preparation | pending |
| 3 | `standards/` taxonomy | pending |
| 4 | `tests/` taxonomy | pending |
| 5 | supporting repository structure (`release/`, CTAN example, tools, examples) | pending |
| 6 | self-contained Web/Lite hardening | pending |
| 7 | Windows-first portability smoke coverage | pending |
| 8 | provenance, LPPL/asset metadata and archival integration | pending |
| 9 | tagged-PDF/PDF-UA experiment | pending |
| 10 | next release certification and publication | pending |

## Phase 1 acceptance criteria

Phase 1 implementation is carried by PR #360. It is complete only when:

1. `CITATION.cff` identifies published v3.0.4 and its publication date;
2. `docs/ARCHITECTURE.md` no longer duplicates volatile current release/development-line values;
3. `docs/RELEASE-STATE.md` records issue #353 as completed and closed;
4. Static Contract executes an explicit metadata-consistency check;
5. the phase PR passes all required repository checks;
6. issue #359 receives the merge/check receipt.

## Next-phase gate

Phase 2 must start from current `main` only after Phase 1 is merged and reconciled. It must first make test/resource discovery resilient to nested paths before any large taxonomy move is attempted.
