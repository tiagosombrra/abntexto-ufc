# V3 Final Certification — Phase-end Regression

Updated: 2026-09-08
Status: ACCEPTED — PHASE CLOSED

## Purpose

This document records the immutable Final Certification phase-end regression. Every **material advance** remains synchronized with handoff, roadmap, readiness and `release/v3-roadmap.json`. Targeted checks never replace the mandatory **phase-end regression**.

## Accepted candidate

| Predicate | Accepted evidence |
|---|---|
| Immutable candidate | `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Static contract | `34239890649` — SUCCESS |
| Linux integration | `34239890614` — SUCCESS; heavy integration executed |
| Linux scope | `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Linux release check | `34239890548` — SUCCESS |
| Release validation matrix | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Scientific Article PDF/A-2b | PASS |
| Distribution bundles | 4 artifacts; checksums/archive integrity PASS; proprietary fonts redistributed=false |
| Release reference reproducibility | PASS; 2 builds; SHA-256 `ae4d7755d18e05abd572a0ad95e5696e54302f9ac236b1efc004d46f57216479` |
| Release-check PR merge ref | `66c3e9766cf55ffc001f388ef250d8082d988435` |
| Temporary certification executor | absent |
| Issue #18 | CLOSED — completed |
| Librarian item 33 | remains explicit `NORMATIVE-REVIEW`, fail-closed |

The release-check workflow is associated with the immutable candidate PR and, by GitHub PR semantics, executed against the candidate merged with current `main`; that checkout was `66c3e976...`. This does not modify the accepted candidate and all required candidate-associated workflows concluded successfully.

## Candidate history

| Candidate | Result | Decision |
|---|---|---|
| `fc907856ac4ba0febf4d44fb408407a0fc2e94d4` | Static green; Linux workflow green but heavy integration skipped as documentation-only | REJECTED |
| `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` | Static green; complete Linux 36/36; release matrix 38/38 | **ACCEPTED** |

## Closure decision

Final Certification is **CLOSED**. The one-shot `release/final-certification-candidate.json` marker is removed in the separate synchronized phase-transition commit. `Release` becomes the sole active phase.

No runtime, normative predicate, tolerance, shared/article semantics or librarian classification is changed by the transition.

## Release boundary

Release execution must follow the repository release-readiness/CTAN documentation and must itself end with a complete **phase-end regression** on one immutable Release candidate before the Release phase is closed.
