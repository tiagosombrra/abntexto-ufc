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
| Steps 5-6 | ACCEPTED — bounded `34175388675`; cleanup `7307164...`; Static `34208318971`; Linux `34208318754` |
| Steps 5-6 acceptance sync | `237cb53b65c91052a469ab67991ea78e71ade283`; Static `34218086750`; Linux `34218086734` |
| Current batch | **Step 4 — literal Times New Roman/Arial + Unicode + embedding** |
| Step 4 executor | `.github/workflows/final-cert-literal-fonts.yml` — temporary, proof-only |
| Release blocker | issue #18 deterministic reference PDF |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 4 execution boundary

The current material advance starts fresh literal-font proof on the actual Final Certification branch. The bounded workflow must compile and validate all four combinations:

| Family | pdfLaTeX | LuaLaTeX |
|---|---|---|
| Times New Roman | required | required |
| Arial | required | required |

The downstream gate must prove literal family identity, Unicode extraction, embedding and PDF/A-2b. Proprietary raw font files must not be committed or uploaded. Only bounded generated PDF evidence may be transported, with short artifact retention.

The temporary workflow is not permanent product infrastructure. Step 4 remains ACTIVE until the proof succeeds, the workflow is removed and the cleanup checkpoint passes Static and Linux.

## Immediate action

1. let the bounded Step 4 workflow execute on the current checkpoint;
2. classify any failure before changing code/tests;
3. if proof is green, record workflow/artifact evidence;
4. remove `.github/workflows/final-cert-literal-fonts.yml`;
5. require cleanup Static/Linux and then mark Step 4 ACCEPTED;
6. resolve issue #18 deterministic reference-PDF reproducibility;
7. execute Final Certification **phase-end regression** on one immutable SHA;
8. only then activate Release.

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
