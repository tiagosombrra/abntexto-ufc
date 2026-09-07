# V3 Final Certification — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — BOUNDED CERTIFICATION MATRIX

## Entry facts

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481` SUCCESS; Linux `34154045509` SUCCESS with `SCOPE=complete PASS=36 FAIL=0 SKIP=0`; canonical article PDF visual review PASS 5/5.

PR #286 was squash-merged into canonical `main` as `22e3c19235fa5245505b92d919a09d31eb2bfecb`. Active branch `cert/v3-final-certification` / PR #289 was created from exactly that SHA.

Entry synchronization checkpoint `aa6cc4a1754bae4ee1b9b89b58441e6cf44d7951` passed Static `34161228915`; Linux `34161228823` succeeded with documentation-only heavy skip. Step 1 is accepted.

Release-baseline transport `f8be323027b42eefcdbe3d13b2f269abdd6ec17f` passed Static `34168471299`, Linux `34168471312`, and the exact permanent `make release-check` contract in run `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Artifact `10035242168` has digest `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604`.

The temporary transport workflow was removed. Cleanup checkpoint `0609f9296ab48799e1b5f6b5cd32141c26ab10c0` then passed Static `34170123785` and Linux `34170123765`. Therefore Step 2 is **ACCEPTED**.

## Certification sequence

| Step | Work | State | Acceptance |
|---:|---|---|---|
| 1 | Entry synchronization and branch handoff | **ACCEPTED** | `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS |
| 2 | Linux release baseline | **ACCEPTED** | transport `f8be323...`; release `34168471371`, `PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...`; Static `34170123785`; Linux `34170123765` |
| 3 | Profile and engine matrix | **ACCEPTED** | complete release baseline includes six non-article profiles under pdfLaTeX/LuaLaTeX plus canonical scientific-article profile under both engines |
| 4 | Literal fonts, Unicode and embedding | ACTIVE | final-candidate literal Times New Roman/Arial identity, Unicode extraction and embedding evidence required; no proprietary-font redistribution |
| 5 | PDF/A certification | ACTIVE — BOUNDED GAP | release baseline covers reference/non-article PDF/A routes; explicit final-candidate scientific-article PDF/A proof remains required |
| 6 | Distribution/public bundles | ACTIVE — BOUNDED GAP | build package/public-distribution artifacts from the certification candidate and verify integrity |
| 7 | Deterministic release reference PDF — issue #18 | QUEUED | pinned deterministic epoch, two clean builds and identical SHA-256 while existing visual/text/font/PDF-A evidence stays intact |
| 8 | Final Certification phase-end regression | QUEUED | one immutable SHA passes Static, complete Linux, release/certification matrix and phase-specific evidence |

## Closure-scope freeze

The remaining v3.0.0 certification scope is frozen to Steps 4-8 above. No new roadmap workstream is created merely because a validator exposes a defect. Any newly discovered problem must be classified inside the existing step whose acceptance predicate it violates. A new step/phase is permitted only if current repository authority demonstrates that none of the existing acceptance predicates can represent the blocker.

This prevents certification from becoming an open-ended redesign cycle. Accepted shared, librarian-review, Reference PDF and Scientific Article semantics are not reopened unless a concrete regression proves them broken.

## Step 3 acceptance basis

`tests/integration/profile-matrix.sh` exercises all six supported non-article profiles under both pdfLaTeX and LuaLaTeX, including A4, PDF/A declaration, embedded-font, structure and semantic checks. `tests/integration/scientific-article-profile.sh` exercises the canonical `scientific-article` profile under both engines. Both gates are part of the complete release selection that passed in `34168471371`; no runtime change occurred in the cleanup checkpoint. Step 3 therefore requires no redundant rerun merely to restate already-current evidence.

## Issue #18 boundary

Issue #18 is a P0 v3.0.0 release blocker. Acceptance requires one deterministic release epoch (`SOURCE_DATE_EPOCH` or equivalent documented mechanism), stable PDF metadata/document ID, at least two controlled clean builds of the same reference PDF and identical SHA-256 digests. Reproducibility is additional evidence and must not replace existing visual/text/font/PDF-A validation.

## Non-negotiable boundaries

- Do not reopen accepted shared or Scientific Article runtime solely for packaging/reproducibility concerns.
- Preserve librarian review state 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW.
- Item 33 remains fail-closed absent authoritative current NBR 6023:2025 evidence.
- Do not redistribute proprietary Microsoft fonts.
- Linux release evidence does not by itself substitute for literal-font/platform certification.
- CTAN/external publication remains blocked until Release.
- Tests and validators are not weakened to obtain green status.

## Phase exit

Final Certification closes only after the bounded remaining matrix (Steps 4-7) is accepted and the complete **phase-end regression** passes on one immutable candidate. A **material advance** updates this plan, handoff, roadmap, release readiness and machine state in the same work cycle.
