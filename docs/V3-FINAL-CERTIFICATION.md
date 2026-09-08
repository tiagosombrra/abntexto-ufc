# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEPS 5-6 CLEANUP AFTER BOUNDED PASS

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | NEXT AFTER CLEANUP | fresh current-candidate proof required; historical V2 evidence is precedent only |
| 5 | Scientific Article PDF/A-2b | **PASS OBSERVED — CLEANUP ACCEPTANCE PENDING** | `13e491d18...`; bounded `34175388675`; PDF/A-2b PASS and font embedding PASS |
| 6 | Distribution/public bundle integrity | **PASS OBSERVED — CLEANUP ACCEPTANCE PENDING** | four distribution artifacts, SHA256SUMS verification and ZIP integrity PASS in `34175388675` |
| 7 | Deterministic release reference PDF / issue #18 | QUEUED | two clean builds, identical SHA-256, preserved validation |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix |

## Bounded transport history

| Checkpoint / run | Permanent release matrix | Step 5 | Step 6 | Classification |
|---|---|---|---|---|
| `21455c3344...` / `34172047786` | `PASS=38/38` | PASS | Git ownership failure while deriving epoch | runner safe-directory provenance read |
| `247e31398...` / `34173496336` | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` | PASS | canonical-checkout failure in tracked-file discovery | container-local Git trust |
| `13e491d18...` / `34175388675` | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` | **PASS** | **PASS** | corrected runner trust accepted technically; cleanup lifecycle now required |

The successful bounded checkpoint `13e491d18d46a86835b4ab1d7f331f6f09f38849` also passed Static `34175388673` and Linux `34175388665`.

## Successful Step 5 evidence

`34175388675` emitted:

`FINAL-CERTIFICATION-EVIDENCE surface=scientific-article-pdfa status=PASS profile=scientific-article engine=pdflatex pdfa=2b font_embedding=PASS`

The canonical Scientific Article build remained on the accepted runtime and passed the complete permanent release suite before this explicit certification gate.

## Successful Step 6 evidence

The same run generated and verified:

- `abntexto-ufc-3.0.0.zip`;
- `abntexto-ufc-ctan-3.0.0.zip`;
- `abntexto-ufc-overleaf-3.0.0.zip`;
- `abntexto-ufc-template-3.0.0.zip`;
- `SHA256SUMS`.

Evidence:

`FINAL-CERTIFICATION-EVIDENCE surface=distribution-bundles status=PASS version=3.0.0 artifacts=4 checksums=PASS archive_integrity=PASS source_date_epoch=1788829436 proprietary_fonts_redistributed=false`

Bounded artifact: ID `10037419414`, upload SHA-256 `e0420e72c4f9afc0d58792ddb1c83df6b3bcdbc8d2db493b53d1b22e0c589da6`.

## Cleanup gate

The temporary `.github/workflows/final-cert-bounded-matrix.yml` has served its bounded transport purpose and is removed in the synchronization/cleanup checkpoint that follows `13e491d18...`.

Steps 5-6 become **ACCEPTED** only after that cleanup checkpoint passes Static and Linux. The permanent contract remains `make release-check`; no release, runtime, normative or archive-integrity predicate is weakened.

## Step 4 design boundary

After cleanup acceptance, execute fresh current-candidate literal-font evidence covering Times New Roman and Arial, pdfLaTeX/LuaLaTeX, Unicode extraction and embedding, retaining PDF/A where applicable. Proprietary fonts must not be redistributed.

## Step 7 boundary

Issue #18 remains a release-build reproducibility concern. The permanent gate must pin deterministic provenance time, perform at least two clean reference-PDF rebuilds, compare SHA-256 exactly and preserve existing PDF validation/font/PDF-A checks.

## Phase-end rule

Final Certification closes only when Steps 4-7 are accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
