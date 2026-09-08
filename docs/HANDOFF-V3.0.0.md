# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Steps 1-3 | ACCEPTED |
| Steps 5-6 bounded candidate | `13e491d18d46a86835b4ab1d7f331f6f09f38849` |
| Static / Linux on bounded candidate | `34175388673` PASS / `34175388665` PASS |
| Bounded release transport | `34175388675` **SUCCESS**, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Step 5 | article PDF/A-2b + embedding PASS; cleanup acceptance pending |
| Step 6 | 4 bundles + checksums + archive integrity PASS; cleanup acceptance pending |
| Bounded artifact | `10037419414`, SHA-256 `e0420e72c4f9afc0d58792ddb1c83df6b3bcdbc8d2db493b53d1b22e0c589da6` |
| Current batch | **Steps 5-6 temporary executor cleanup** |
| Temporary executor | removed in current cleanup checkpoint; Static/Linux cleanup acceptance pending |
| Next after cleanup | Step 4 current-candidate literal Times New Roman/Arial + Unicode + embedding proof |
| Release blocker | issue #18 deterministic reference PDF |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Successful bounded transport

Run `34175388675` on `13e491d18...` passed the unchanged permanent `make release-check` contract at `PASS=38/38`, then passed the explicit Scientific Article PDF/A-2b/font-embedding gate and distribution bundle integrity.

Step 6 produced four v3.0.0 ZIP candidates plus `SHA256SUMS`; all checksums and archive-integrity checks passed and `proprietary_fonts_redistributed=false`.

## Immediate action

1. validate the cleanup checkpoint after removal of `.github/workflows/final-cert-bounded-matrix.yml`;
2. require Static and Linux green on that cleanup SHA;
3. mark Steps 5-6 ACCEPTED only after those results are recorded;
4. execute fresh current-candidate literal Times New Roman/Arial, Unicode extraction and embedding proof;
5. resolve issue #18 deterministic reference-PDF reproducibility;
6. execute Final Certification **phase-end regression** on one immutable SHA;
7. only then activate Release.

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
