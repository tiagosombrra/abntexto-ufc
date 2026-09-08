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
| Steps 1-6 | ACCEPTED |
| Step 7 clean bounded proof | **PASS** — run `34231038578` on `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` |
| Deterministic proof | epoch `1788873426`; 2 clean builds; SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` |
| Step 7 cleanup checkpoint | `34e6bf8299e582803d1726e8dd699271c356fda5` |
| Cleanup Static | `34232017286` — SUCCESS |
| Cleanup Linux | `34232017359` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Temporary executor | absent |
| Issue #18 | **CLOSED — completed** |
| Current batch | **Step 8 — Final Certification phase-end regression preparation** |
| Final phase gate | one immutable candidate, complete matrix |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 7 acceptance

Run `34231038578` proved deterministic release-reference-PDF generation from source `9ba5905...`: deterministic epoch `1788873426`, two independent clean builds, identical PDF SHA-256 `1c92535f...`, and PASS for font embedding, portable UFC PDF validation, Unicode extraction and PDF/A-2b. Cleanup checkpoint `34e6bf8...` then removed `.github/workflows/final-cert-step7-repro.yml` and passed Static `34232017286` plus complete Linux `34232017359`. The permanent gate remains `make release-reference-reproducibility` inside `make release-check`.

Issue #18 now has this evidence recorded and is closed as completed.

## Immediate action

| Order | Action | Acceptance boundary |
|---:|---|---|
| 1 | Synchronize Step 7 acceptance and issue #18 closure | current documentation cycle |
| 2 | Prepare one immutable Step 8 candidate | do not amend after CI starts |
| 3 | Run Static + complete Linux + full release/certification matrix | all green on same accepted candidate |
| 4 | Record candidate SHA/run IDs and close Final Certification | only after complete matrix |
| 5 | Activate Release | no earlier publication action |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
