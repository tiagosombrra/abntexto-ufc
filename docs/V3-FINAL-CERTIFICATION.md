# V3 Final Certification

Updated: 2026-09-07
Status: ACTIVE — STEP 6 RUNNER-INTEGRATION CORRECTION

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every material advance is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable phase-end candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | ACTIVE / next after current bounded cleanup | fresh current-candidate Windows/Linux proof required |
| 5 | Scientific Article PDF/A-2b | GATE PASS OBSERVED, NOT YET BOUNDED-ACCEPTED | run `34172047786` emitted explicit PASS after embedding and veraPDF checks; acceptance still requires corrected transport + executor cleanup |
| 6 | Distribution/public bundle integrity | **CORRECTION ACTIVE** | run `34172047786` stopped before bundle construction because Git safe-directory protection rejected Docker-mounted checkout ownership while deriving the deterministic epoch |
| 7 | Deterministic release reference PDF / issue #18 | QUEUED | two clean builds, identical SHA-256, preserved validation |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix |

## Bounded transport result

Checkpoint `21455c3344bfe0413dbe44f29b9cfae5bee58521`:

| Evidence | Result |
|---|---|
| Static `34172047639` | PASS |
| Linux `34172047586` | PASS |
| temporary bounded release run `34172047786` | FAIL |
| permanent release matrix inside run | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Scientific Article PDF/A | PASS |
| Scientific Article font embedding | PASS |
| distribution bundle gate | infrastructure stop before bundle build: `fatal: detected dubious ownership in repository` |
| diagnostic artifact | `10036350950`; SHA-256 `5dd4d212bafa16702947065ef0848c9387e63e16d7d7523fee14d1d529a96432` |

## Failure classification and correction

The failure is bounded to Step 6 runner integration. `tests/integration/distribution-bundles.sh` derived its deterministic epoch through a Git command. Inside the TeX Live Docker container, the mounted checkout has ownership different from the container user, so Git's safe-directory guard rejected the read.

The correction preserves the same bundle predicate:

- use `git -c safe.directory="$PWD"` only for the provenance timestamp read;
- when `SOURCE_COMMIT_SHA` is provided, derive the epoch from that exact source commit;
- make the temporary transport checkout full history so the PR head commit is resolvable;
- retain all four archive, checksum, ZIP-safety, proprietary-font and institutional-asset checks unchanged.

No LaTeX runtime, public API, normative rule, librarian-review state or Step 5 predicate changes.

## Corrected bounded gate

The corrected branch state must pass the same temporary `.github/workflows/final-cert-bounded-matrix.yml` transport running permanent `make release-check`. After a green run, remove the temporary workflow and require cleanup Static and Linux before Steps 5-6 become ACCEPTED.

## Step 4 design boundary

After bounded cleanup, execute a fresh current-candidate literal-font matrix. Historical R4 proof is useful precedent but does not replace current-candidate evidence after Scientific Article integration. Current proof must cover Times New Roman and Arial, pdfLaTeX/LuaLaTeX, Unicode extraction and embedding, with PDF/A retained where applicable. Temporary transport must be removed after classification.

## Step 7 boundary

Issue #18 is a release-build reproducibility concern. It must not change Scientific Article or shared normative behavior. The permanent release gate will pin deterministic provenance time, perform at least two clean reference-PDF rebuilds, compare SHA-256 exactly and preserve existing PDF validation/font/PDF-A checks.

## Phase-end rule

Final Certification closes only when Steps 4-7 are accepted, temporary executors are removed, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification evidence matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
