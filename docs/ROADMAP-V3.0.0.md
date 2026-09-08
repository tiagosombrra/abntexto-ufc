# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-3 are accepted. Step 5 has passed its explicit PDF/A/embedding gate in both bounded transports. Step 6 remains active: the first run exposed Git ownership during epoch derivation; the second progressed further and exposed container-local Git trust during tracked-file discovery. The correction remains bounded to Step 6 and the remaining scope stays frozen.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 6 RUNNER CORRECTION** | Steps 4-7 accepted + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization | ACCEPTED |
| 2 | Linux release baseline | ACCEPTED — release `34168471371`; cleanup `0609f929...` Static/Linux green |
| 3 | Profile and engine certification | ACCEPTED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | ACTIVE / next after bounded cleanup |
| 5 | Scientific Article PDF/A-2b | **GATE PASS OBSERVED — bounded acceptance waits for Step 6 green + temporary executor cleanup** |
| 6 | Distribution/public bundle integrity | **CORRECTION ACTIVE — canonical-checkout trust inside TeX Live container** |
| 7 | Issue #18 deterministic reference PDF | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

## Bounded transport classification

| Checkpoint / run | Result before Step 6 | Step 6 result | Classification |
|---|---|---|---|
| `21455c3344...` / `34172047786` | release `PASS=38/38`; article PDF/A PASS | Git dubious ownership while deriving deterministic epoch | runner ownership / provenance read |
| `247e31398...` / `34173496336` | release `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; article PDF/A + embedding PASS | `Distribution bundle generation requires a canonical Git checkout.` | `git ls-files` tracked-file discovery still lacks container-local trust |

`247e31398...` also passed Static `34173496318` and Linux `34173496285`. Its failed bounded transport artifact is `10036808737`, SHA-256 `c56e1c651ce990ddd5a301c5cf60691b1081a06b7eebe66b27503e256e28e273`.

The current correction configures `safe.directory` inside the TeX Live container before the permanent `make release-check`, both in temporary bounded transport and the permanent Linux release workflow. It does not change LaTeX runtime, public API, normative rules or distribution integrity predicates.

`make release-check` remains the permanent Step 5/6 contract. `.github/workflows/final-cert-bounded-matrix.yml` remains temporary transport only and must be removed after a successful corrected run before Steps 5-6 can be accepted.

## Closure-scope freeze

No new roadmap phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 4-8. Accepted shared, librarian-review, Reference PDF and Scientific Article semantics remain closed absent a concrete regression.

The finite path is: rerun corrected Step 6; remove transport and pass cleanup CI; complete Step 4; resolve issue #18; execute Final Certification phase-end regression; then Release.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase or create a new workstream by themselves.
