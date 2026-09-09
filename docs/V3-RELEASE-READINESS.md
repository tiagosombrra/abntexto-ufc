# V3.0.0 Release Readiness

Updated: 2026-09-09
Status: ACTIVE — GITHUB PUBLISHED / MAINTAINER VISUAL VALIDATION PENDING / CTAN BLOCKED

## Phase readiness

| Phase | State | Evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | technical/runtime certification accepted |
| Release | **ACTIVE — VISUAL VALIDATION PENDING** | exact source certified; pkgcheck/tag/GitHub publication PASS; seven-profile maintainer review must pass before CTAN submission |

GitHub v3.0.0 publication is complete and byte-verified. CTAN submission is intentionally blocked until the maintainer inspects generated source + PDF pairs for every canonical document profile and explicitly accepts them.

## Completed Release hardening

PR #297 was merged through protected `main`. Its final head passed Static, Linux integration and Linux release check with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.

The merged work:

- replaced stale v2/pre-publication distribution documentation;
- finalized CTAN metadata for v3.0.0;
- closed former librarian item 33 against primary ABNT NBR 6023:2025 authority;
- made `abntexto-ufc-3.0.0.zip` the only CTAN upload archive;
- generated one monolithic `abntexto-ufc.cls` from modular project sources;
- made any project-owned `.def` in the CTAN ZIP a hard failure;
- proved isolated compilation without the modular runtime directory;
- excluded UFC marks and proprietary Microsoft fonts fail-closed;
- moved current CTAN `pkgcheck` before immutable tag creation.

The retained pre-merge CTAN artifact was manually inspected and confirmed `1 cls / 0 def`, 14/14 runtime modules inlined exactly once, no residual project-owned `.def` input, no vendored `abntexto.cls`, and no prohibited assets.

## Released-source contract

The accepted released source is exactly:

`05399473827da7cf6b6c8bac36edc7115481773f`

Immutable annotated tag `v3.0.0` resolves to that source, and GitHub Release `385743477` contains only the frozen publication assets produced from it. The invariant is satisfied:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

Post-tag documentation or validation infrastructure may advance `main`; such commits do not change the v3.0.0 source. Any material defect found during the remaining human review must not mutate or retarget `v3.0.0`; it requires a correction/new-version cycle before CTAN submission.

## Maintainer all-profile visual validation gate

Before any CTAN submission, generate from the frozen v3.0.0 implementation and present the source plus rendered PDF for all seven canonical `type` values defined by the class:

1. `undergraduate-capstone` — undergraduate capstone / TCC;
2. `specialization-capstone` — specialization capstone;
3. `masters-thesis` — master's thesis/dissertation profile;
4. `doctoral-thesis` — doctoral thesis;
5. `research-project` — identified research project;
6. `anonymized-research-project` — anonymized research project;
7. `scientific-article` — scientific article.

The review artifact must preserve, for each profile, at minimum:

- the exact `.tex` source used to compile it;
- the corresponding final PDF;
- build/log metadata sufficient to identify the source/tag and engine;
- a manifest mapping profile → source → PDF → SHA-256.

Acceptance is explicitly human/maintainer-facing. Automated compilation success does not replace visual inspection. Record the outcome in `docs/V3-VISUAL-VALIDATION.md`.

## CTAN final package contract

`abntexto-ufc-3.0.0.zip` contains exactly one top-level `abntexto-ufc/` directory and these eight files:

```text
README.md
CHANGELOG
LICENSE
abntexto-ufc.cls
abntexto-ufc.tex
abntexto-ufc.pdf
abntexto-ufc-example.tex
abntexto-ufc-example.pdf
```

Hard requirements include one project-owned runtime `.cls`, zero project-owned `.def`, no nested runtime tree, no vendored `abntexto.cls`, no UFC marks, no proprietary Microsoft fonts, no development infrastructure, and successful isolated example compilation.

## Remaining gates

| Order | Gate | State |
|---:|---|---|
| 1 | Publication-hardening integration | **PASS / MERGED** |
| 2 | Post-merge control-plane synchronization | **PASS / MERGED** |
| 3 | Exact resulting source SHA resolved | **PASS — `05399473827da7cf6b6c8bac36edc7115481773f`** |
| 4 | Static + complete Linux + Linux release check on exact SHA | **PASS** |
| 5 | Deterministic three-ZIP distribution + `SHA256SUMS` | **PASS — artifact `10117679639`** |
| 6 | Final CTAN ZIP audit: one class, zero `.def`, isolated compile | **PASS** |
| 7 | Current CTAN `pkgcheck` | **PASS — 4.1.0, zero warnings/errors** |
| 8 | Freeze hashes/evidence; prohibit rebuild | **PASS** |
| 9 | Immutable `v3.0.0` on certified SHA | **PASS** |
| 10 | GitHub Release + re-download/hash verification | **PASS — Release `385743477`** |
| 11 | Generate seven canonical source + PDF review pairs from frozen v3.0.0 | **ACTIVE** |
| 12 | Maintainer visually validates all seven PDFs and sources | **PENDING USER ACCEPTANCE** |
| 13 | Submit canonical ZIP to CTAN; preserve receipt/acceptance evidence | **BLOCKED BY 12** |
| 14 | Synchronize final CTAN facts and close Release | **BLOCKED BY 13** |

## Current blockers

- all seven canonical rendered examples have not yet been presented and accepted by the maintainer;
- CTAN submission is blocked until that acceptance is recorded;
- consequently, CTAN acceptance/catalog/install evidence does not yet exist.

GitHub publication is complete and verified. No v3.0.0 source or asset rebuild is permitted. Every subsequent material advance updates affected documentation and machine state in the same work cycle.
