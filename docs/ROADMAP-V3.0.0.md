# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. The permanent Linux release baseline has passed; the temporary executor is removed in the current cleanup candidate and Step 2 awaits cleanup-candidate CI before acceptance.**

| Phase | Status | Accepted evidence / exit requirement |
|---|---|---|
| Regression Audit | CLOSED | completed regression contract and phase-end regression |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — RELEASE BASELINE CLEANUP CANDIDATE** | cleanup CI, remaining certification matrix, issue #18, immutable phase-end regression |
| Release | QUEUED | final bundles/checksums/tag/release/publication after certification |

PR #289 carries Final Certification from canonical main `22e3c192...`.

## Final Certification roadmap

| Step | Work | State | Evidence / acceptance |
|---:|---|---|---|
| 1 | Entry synchronization and certification branch handoff | **ACCEPTED** | `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS |
| 2 | Linux release baseline | **PASS EXECUTION — CLEANUP CI PENDING** | transport `f8be323...`; Static `34168471299`; Linux `34168471312`; release run `34168471371`; `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; artifact `10035242168`; executor removed in cleanup candidate |
| 3 | Full profile and engine certification | QUEUED | all supported profiles and required engines green on final-candidate evidence |
| 4 | Literal Times New Roman/Arial, Unicode and embedding evidence | QUEUED | literal identity, extraction and embedding evidence valid without font redistribution |
| 5 | PDF/A-2b certification | QUEUED | established certification route green on final candidate |
| 6 | Public/distribution bundle integrity | QUEUED | bundle/package integrity green from same candidate |
| 7 | Issue #18 deterministic release-reference-PDF reproducibility | QUEUED | pinned epoch + two clean builds + identical SHA-256 with existing validation preserved |
| 8 | Final Certification phase-end regression | QUEUED | one immutable SHA passes Static, complete Linux and complete certification matrix |

## Release baseline cleanup rule

The transport workflow proved the permanent `make release-check` contract at `f8be323...` and produced artifact digest `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604`. It is now removed. The bounded baseline is accepted only after the cleanup candidate itself passes Static and Linux, proving no temporary executor remains and no cleanup regression was introduced.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains explicit/fail-closed unless authoritative current-edition NBR 6023:2025 evidence is obtained.

## Gate before Release

Release cannot activate until Final Certification passes on one immutable candidate, issue #18 is resolved with deterministic digest evidence, no certification blocker remains, and all acceptance documentation is synchronized.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a mandatory complete **phase-end regression** on one immutable SHA; targeted/scoped intermediate checks never close a phase.
