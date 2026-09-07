# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`, created from canonical main `22e3c19235fa5245505b92d919a09d31eb2bfecb`.**

| Phase | Status | Accepted evidence / exit requirement |
|---|---|---|
| Regression Audit | CLOSED | completed regression contract and phase-end regression |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; Static `34154045481`; complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — BASELINE ENTRY** | release baseline, complete certification matrix, issue #18, immutable phase-end regression |
| Release | QUEUED | final bundles/checksums/tag/release/publication after certification |

PR #286 is merged. Active certification branch is `cert/v3-final-certification` from exact merged main SHA `22e3c192...`.

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization and certification branch handoff | ACTIVE — checkpoint pending CI |
| 2 | Linux release baseline | QUEUED |
| 3 | Full profile and engine certification | QUEUED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding evidence | QUEUED |
| 5 | PDF/A-2b certification | QUEUED |
| 6 | Public/distribution bundle integrity | QUEUED |
| 7 | Issue #18 deterministic release-reference-PDF reproducibility | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

Execution details: `docs/V3-FINAL-CERTIFICATION.md`.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains explicit/fail-closed unless authoritative current-edition NBR 6023:2025 evidence is obtained.

## Gate before Release

Release cannot activate until Final Certification passes on one immutable candidate, issue #18 is resolved with deterministic digest evidence, no certification blocker remains, and all acceptance documentation is synchronized.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a mandatory complete **phase-end regression** on one immutable SHA; targeted/scoped intermediate checks never close a phase.
