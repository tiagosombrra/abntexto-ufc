# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. The permanent Linux release baseline and cleanup checkpoint are accepted; profile/engine certification is also accepted. Remaining work is frozen to a bounded certification matrix plus Release.**

| Phase | Status | Accepted evidence / exit requirement |
|---|---|---|
| Regression Audit | CLOSED | completed regression contract and phase-end regression |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — BOUNDED MATRIX** | literal-font/Unicode, explicit article PDF/A, distribution, issue #18, immutable phase-end regression |
| Release | QUEUED | final checksums/tag/release/publication after certification |

PR #289 carries Final Certification from canonical main `22e3c192...`.

## Final Certification roadmap

| Step | Work | State | Evidence / acceptance |
|---:|---|---|---|
| 1 | Entry synchronization and certification branch handoff | **ACCEPTED** | `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS |
| 2 | Linux release baseline | **ACCEPTED** | `f8be323...`; release `34168471371`, `PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...`; Static `34170123785`; Linux `34170123765` |
| 3 | Full profile and engine certification | **ACCEPTED** | six non-article profiles × pdfLaTeX/LuaLaTeX plus scientific article × both engines are in the accepted complete release evidence |
| 4 | Literal Times New Roman/Arial, Unicode and embedding evidence | ACTIVE | final-candidate literal identity/extraction/embedding proof; no proprietary-font redistribution |
| 5 | PDF/A-2b certification | ACTIVE — BOUNDED GAP | release baseline covers reference/non-article routes; explicit article proof remains |
| 6 | Public/distribution bundle integrity | ACTIVE — BOUNDED GAP | package/public-distribution integrity from certification candidate |
| 7 | Issue #18 deterministic release-reference-PDF reproducibility | QUEUED | pinned epoch + two clean builds + identical SHA-256 with existing validation preserved |
| 8 | Final Certification phase-end regression | QUEUED | one immutable SHA passes Static, complete Linux and complete certification matrix |

## Closure-scope freeze

No new roadmap phase or certification step is created unless current repository authority proves that an existing acceptance predicate cannot represent a blocking defect. New findings are classified inside Steps 4-8. Accepted shared, librarian-review, Reference PDF and Scientific Article semantics are not reopened absent a concrete regression.

This is the finite path to v3.0.0: finish Steps 4-8, then execute Release. Item 33 remains an explicit authority gap rather than a hidden implementation task.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains explicit/fail-closed unless authoritative current-edition NBR 6023:2025 evidence is obtained.

## Gate before Release

Release cannot activate until Final Certification passes on one immutable candidate, issue #18 is resolved with deterministic digest evidence, no certification blocker remains, and all acceptance documentation is synchronized.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a mandatory complete **phase-end regression** on one immutable SHA; targeted intermediate checks never close a phase or create a new workstream by themselves.
