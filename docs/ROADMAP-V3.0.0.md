# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-3 and 5-6 are accepted. Step 4 is executing a fresh current-candidate literal Times New Roman/Arial, Unicode, embedding and PDF/A proof through a temporary bounded workflow.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 4 EXECUTION** | Steps 4 and 7 accepted + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization | ACCEPTED |
| 2 | Linux release baseline | ACCEPTED |
| 3 | Profile and engine certification | ACCEPTED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | **ACTIVE — BOUNDED PROOF** |
| 5 | Scientific Article PDF/A-2b | ACCEPTED |
| 6 | Distribution/public bundle integrity | ACCEPTED |
| 7 | Issue #18 deterministic reference PDF | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

## Accepted Steps 5-6 evidence

| Surface | Evidence |
|---|---|
| Bounded release transport | `34175388675`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Cleanup checkpoint | `7307164ba4cf924beecb6678c7af5b79d551d513` |
| Cleanup Static / Linux | `34208318971` PASS / `34208318754` PASS |
| Acceptance sync | `237cb53b65c91052a469ab67991ea78e71ade283`; Static `34218086750`; Linux `34218086734` |

## Step 4 bounded proof

Temporary executor: `.github/workflows/final-cert-literal-fonts.yml`.

It is restricted to current-candidate proof and must cover Times New Roman and Arial with both pdfLaTeX and LuaLaTeX. Linux post-validation must verify literal identity, Unicode extraction, embedding and PDF/A-2b. The executor must not transport raw proprietary font files and must be removed after evidence capture. Cleanup Static/Linux is required before Step 4 acceptance.

## Frozen remaining scope

**Step 4 proof + cleanup → issue #18 deterministic reference PDF → Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 4-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
