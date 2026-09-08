# V3 Final Certification

Updated: 2026-09-07
Status: ACTIVE — STEP 6 CANONICAL-CHECKOUT RUNNER CORRECTION

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | ACTIVE / next after bounded cleanup | fresh current-candidate Windows/Linux proof required |
| 5 | Scientific Article PDF/A-2b | GATE PASS OBSERVED, NOT YET BOUNDED-ACCEPTED | both bounded runs reached explicit PDF/A + embedding PASS; acceptance still requires Step 6 green + executor cleanup |
| 6 | Distribution/public bundle integrity | **CORRECTION ACTIVE** | second bounded run progressed past epoch read but `git ls-files` inside the TeX Live container rejected the mounted checkout as non-canonical |
| 7 | Deterministic release reference PDF / issue #18 | QUEUED | two clean builds, identical SHA-256, preserved validation |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix |

## Bounded transport history

| Checkpoint / run | Permanent release matrix | Step 5 | Step 6 | Classification |
|---|---|---|---|---|
| `21455c3344...` / `34172047786` | `PASS=38/38` | PASS | failed on Git dubious ownership while deriving epoch | runner safe-directory provenance read |
| `247e31398...` / `34173496336` | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` | PASS | `Distribution bundle generation requires a canonical Git checkout.` | tracked-file discovery still lacked container-local Git trust |

For `247e31398...`, Static `34173496318` and Linux `34173496285` also passed. The failed bounded run uploaded artifact `10036808737`, SHA-256 `c56e1c651ce990ddd5a301c5cf60691b1081a06b7eebe66b27503e256e28e273`.

## Current correction

The failure remains bounded to Step 6 infrastructure. The archive/checksum/ZIP-safety/proprietary-font/institutional-asset predicates are unchanged.

The corrected runner contract now configures Git trust **inside the TeX Live container** before `make release-check`:

- `git config --global --add safe.directory "$PWD"` is applied only to the mounted canonical checkout used by the workflow;
- the temporary transport still uses full history and exact `SOURCE_COMMIT_SHA`;
- the same configuration is added to the permanent Linux release workflow so the persistent Step 6 gate is runnable after merge;
- product runtime, normative rules, public API and bundle-content predicates are unchanged.

The temporary `.github/workflows/final-cert-bounded-matrix.yml` must rerun the unchanged permanent `make release-check` contract. A green run is not sufficient by itself: remove the temporary workflow and require cleanup Static/Linux before Steps 5-6 become ACCEPTED.

## Step 4 design boundary

After bounded cleanup, execute fresh current-candidate literal-font evidence covering Times New Roman and Arial, pdfLaTeX/LuaLaTeX, Unicode extraction and embedding, retaining PDF/A where applicable. Historical proof is precedent only, not current-candidate certification.

## Step 7 boundary

Issue #18 remains a release-build reproducibility concern. It must not change Scientific Article or shared normative behavior. The permanent gate will pin deterministic provenance time, perform at least two clean reference-PDF rebuilds, compare SHA-256 exactly and preserve existing PDF validation/font/PDF-A checks.

## Phase-end rule

Final Certification closes only when Steps 4-7 are accepted, temporary executors are removed, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
