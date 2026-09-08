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
| Bounded release transport | `34175388675` SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Steps 5-6 cleanup checkpoint | `7307164ba4cf924beecb6678c7af5b79d551d513` |
| Cleanup Static / Linux | `34208318971` SUCCESS / `34208318754` SUCCESS |
| Step 5 | **ACCEPTED** — Scientific Article PDF/A-2b + embedding PASS |
| Step 6 | **ACCEPTED** — 4 bundles + checksums + archive integrity PASS |
| Temporary executor | none active |
| Current batch | **Step 4 — literal Times New Roman/Arial + Unicode + embedding** |
| Release blocker | issue #18 deterministic reference PDF |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Steps 5-6 accepted cleanup

The bounded proof-only workflow succeeded at `13e491d18...` and was removed at cleanup checkpoint `7307164...`. Static `34208318971` and Linux `34208318754` both passed after removal. The temporary-executor lifecycle is therefore closed and Steps 5-6 are accepted without moving bounded-only orchestration into permanent product runtime.

## Immediate action

1. execute fresh current-candidate literal Times New Roman and Arial proof on Windows for pdfLaTeX and LuaLaTeX;
2. certify literal family identity, Unicode extraction and embedding without redistributing proprietary fonts;
3. remove any temporary Step 4 executor and require cleanup Static/Linux before accepting Step 4;
4. resolve issue #18 with deterministic reference-PDF proof;
5. execute Final Certification **phase-end regression** on one immutable SHA;
6. only then activate Release.

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
