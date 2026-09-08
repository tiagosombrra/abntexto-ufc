# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Step 4 bounded literal-font proof passed and its temporary executor was removed. Cleanup Static/Linux is now the active gate.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 4 CLEANUP** | Step 4 cleanup + Step 7 accepted + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization | ACCEPTED |
| 2 | Linux release baseline | ACCEPTED |
| 3 | Profile and engine certification | ACCEPTED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | **PROOF PASS — CLEANUP PENDING** |
| 5 | Scientific Article PDF/A-2b | ACCEPTED |
| 6 | Distribution/public bundle integrity | ACCEPTED |
| 7 | Issue #18 deterministic reference PDF | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

## Step 4 accepted bounded proof

| Evidence | Result |
|---|---|
| Source checkpoint | `fae338e16304ad45c353067a0b7982f73a8363c5` |
| Bounded workflow run | `34219229025` — success |
| Times New Roman / pdfLaTeX | PASS |
| Arial / pdfLaTeX | PASS |
| Times New Roman / LuaLaTeX | PASS |
| Arial / LuaLaTeX | PASS |
| Unicode extraction | PASS |
| Font embedding | PASS |
| PDF/A-2b | PASS |
| Generated-PDF artifact | `10053151610`, one-day retention |
| Artifact digest | `sha256:6b0cd0a6ac2543017a8496a1af7feeca70640f2b73862311a4325a981dc5fb60` |
| Raw proprietary fonts transported | no |
| Temporary workflow | removed after evidence capture |

Step 4 is not marked ACCEPTED until the cleanup checkpoint after workflow removal passes Static and Linux.

## Frozen remaining scope

**Step 4 cleanup validation → issue #18 deterministic reference PDF → Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 4-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
