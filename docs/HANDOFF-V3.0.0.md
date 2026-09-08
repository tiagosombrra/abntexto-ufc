# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED — release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...`; Static `34170123785`; Linux `34170123765` |
| Profile/engine matrix | ACCEPTED |
| Current batch | **Bounded Matrix Validation — Step 6 runner ownership correction** |
| Bounded transport result | `21455c3344...`: Static `34172047639` PASS, Linux `34172047586` PASS, release transport `34172047786` FAIL after the permanent 38/38 release suite and Step 5 passed |
| Failure classification | Step 6 infrastructure: Docker-mounted checkout was rejected by Git safe-directory protection while deriving `SOURCE_DATE_EPOCH`; no product/runtime/normative predicate failed |
| Evidence artifact from failed transport | ID `10036350950`, SHA-256 `5dd4d212bafa16702947065ef0848c9387e63e16d7d7523fee14d1d529a96432` |
| Temporary executor | `.github/workflows/final-cert-bounded-matrix.yml` remains active only for corrected rerun; remove before Steps 5-6 acceptance |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Current material advance

The first bounded transport established three useful facts before failing:

| Surface | Result |
|---|---|
| Existing permanent release matrix | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Scientific Article PDF/A + embedding | **PASS** — explicit `FINAL-CERTIFICATION-EVIDENCE surface=scientific-article-pdfa` |
| Distribution/public bundles | **NOT EXECUTED TO COMPLETION** — failed while reading Git timestamp because container ownership triggered Git safe-directory protection |

The Step 6 correction does not weaken bundle validation. The distribution gate now performs Git provenance reads with `git -c safe.directory="$PWD"`, and the temporary workflow checks out full history so the exact `SOURCE_COMMIT_SHA` timestamp is available. The corrected transport must rerun the same permanent `make release-check` contract.

## Frozen remaining path

| Order | Work | Acceptance |
|---:|---|---|
| 1 | Correct and rerun Step 6 distribution validation | corrected release transport PASS |
| 2 | Remove temporary bounded workflow and validate cleanup | cleanup Static + Linux PASS; then Steps 5-6 accepted |
| 3 | Literal Times New Roman/Arial + Unicode + embedding | current final-candidate identity/extraction/embedding proof |
| 4 | Issue #18 deterministic reference PDF | two controlled clean builds with identical SHA-256 and preserved validation |
| 5 | Final Certification phase-end regression | one immutable candidate with complete matrix |
| 6 | Release | final docs/checksums/tag/GitHub Release/publication verification |

A failure remains inside the row whose predicate it violates. It does not create a new roadmap workstream.

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a concrete regression is discovered.
- Item 33 remains fail-closed and is not a hidden release task.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until Release.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted checks never authorize a phase transition or create a new workstream by themselves.
