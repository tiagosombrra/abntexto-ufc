# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 7 DETERMINISTIC REFERENCE PDF

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | **ACCEPTED** | proof `34219229025`; cleanup `35671aef...`, Static `34224224990`, Linux `34224225080` PASS |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded `34175388675` PASS; cleanup `7307164...`, Static `34208318971`, Linux `34208318754` PASS |
| 6 | Distribution/public bundle integrity | ACCEPTED | 4 bundles, checksums and archive integrity PASS; cleanup accepted |
| 7 | Deterministic release reference PDF / issue #18 | **ACTIVE** | implement permanent deterministic proof: two clean builds, identical SHA-256, existing validation preserved |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix |

## Step 4 accepted evidence

Bounded run `34219229025` executed on source checkpoint `fae338e16304ad45c353067a0b7982f73a8363c5` and proved all four strict combinations.

| Family | Engine | Literal identity | Unicode | Embedding | PDF/A-2b |
|---|---|---|---|---|---|
| Times New Roman | pdfLaTeX | PASS | PASS | PASS | PASS |
| Arial | pdfLaTeX | PASS | PASS | PASS | PASS |
| Times New Roman | LuaLaTeX | PASS | PASS | PASS | PASS |
| Arial | LuaLaTeX | PASS | PASS | PASS | PASS |

Artifact `10053151610` contained only the four generated strict PDFs, with one-day retention and digest `sha256:6b0cd0a6ac2543017a8496a1af7feeca70640f2b73862311a4325a981dc5fb60`. No raw proprietary font files were uploaded or committed.

The temporary executor was removed. The synchronized cleanup checkpoint `35671aefd932375cad14c9121a833d7daf267817` passed Static `34224224990` and Linux `34224225080`, so Step 4 is accepted.

## Step 7 acceptance contract

Issue #18 is now the active release-build reproducibility blocker. The permanent deterministic reference-PDF gate must:

1. use a deterministic provenance time (`SOURCE_DATE_EPOCH` or an equivalent project-controlled input);
2. perform at least two clean builds of the canonical release reference PDF from the same immutable source/input state;
3. compare the resulting PDF SHA-256 values exactly and fail on any mismatch;
4. preserve the existing canonical PDF validation, font/Unicode/embedding expectations and applicable PDF/A checks rather than replacing them with hash equality;
5. keep the implementation permanent only if it belongs to normal release verification, not as a temporary proof executor.

A deterministic hash is evidence of reproducibility only for the controlled build inputs. It does not replace normative or visual acceptance already established in earlier phases.

## Phase-end rule

Final Certification closes only when Step 7 is accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
