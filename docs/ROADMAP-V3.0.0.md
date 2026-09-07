# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE. Steps 1–6 are ACCEPTED and Step 7 canonical article PDF provenance build is ACTIVE.**

| Phase | Status | Current exit requirement |
|---|---|---|
| Regression Audit | CLOSED | completed regression contract and phase-end regression |
| Core Corrections | CLOSED | candidate `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | candidate `b64074c...`; complete 55-page visual PASS + Static/Linux |
| Scientific Article | **ACTIVE — STEP 7 PROVENANCE BUILD** | canonical article PDF acceptance + Step 8 complete phase-end regression |
| Final Certification | QUEUED | complete platform/font/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | packaging, checksums, tag/release and publication verification |

Canonical `main` is `fbf7cc4839ce318024a7d1ed517dd50fab5773ac`. Active article work is PR #286 on `feat/v3-scientific-article`, reconciled with current main through `85cf22b6fe5d117bb2611a2865911e0d20a19363`.

## Scientific Article roadmap

| Step | Work | State | Gate |
|---:|---|---|---|
| 1 | Profile and metadata | ACCEPTED | completed |
| 2 | Required front block | ACCEPTED | completed |
| 3 | Optional foreign title/summary | ACCEPTED | completed |
| 4 | Body structure and typography | ACCEPTED | completed |
| 5 | Recommendations and journal applicability | ACCEPTED | completed |
| 6 | Exact 18-rule evidence ownership map | **ACCEPTED** | `e941a7f9...`; Static `34146793998`; Linux `34146794016`; zero validation-mode promotions |
| 7 | Canonical article PDF | **ACTIVE — BUILD** | `template/scientific-article.tex`; real TeX Live 2026 PDF; Git provenance; every page visually inspected; temporary executor removed before acceptance |
| 8 | Scientific Article phase-end regression | QUEUED | Static + `complete` Linux + article gates on one immutable SHA |

## Step 7 executor lifecycle

| Surface | State |
|---|---|
| Canonical source | `template/scientific-article.tex` |
| Validation record | `docs/V3-SCIENTIFIC-ARTICLE-PDF-VALIDATION.md` |
| Temporary workflow | `.github/workflows/tmp-scientific-article-pdf.yml` — ACTIVE |
| Artifact provenance | PENDING build |
| Visual review | PENDING artifact recovery |

The temporary workflow is not part of the permanent CI architecture. It exists only to generate the bounded Step 7 artifact and must be removed immediately after artifact recovery.

## Step 7 presentation gate

The article PDF is a new canonical artifact, separate from the accepted 55-page academic-work reference PDF. Step 7 requires a dedicated canonical article source, real TeX Live 2026 compilation, provenance bound to a concrete Git SHA/workflow run, PDF hash/metadata preflight, complete page-by-page visual inspection, explicit leakage checks, and temporary-executor removal before acceptance. Synthetic PDFs are inadmissible.

## After Scientific Article

Final Certification must run on the accepted final candidate and cover at least all document profiles, pdfLaTeX/LuaLaTeX, literal Times New Roman and Arial identity where required, Unicode extraction, font embedding, PDF/A-2b, distribution/public bundle checks, and release-reference-PDF reproducibility evidence required by issue #18.

Release follows only after Final Certification and includes final documentation, bundles, checksums/assets, immutable `v3.0.0` tag/GitHub Release and any external publication/CTAN action.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains explicit/fail-closed unless authoritative current-edition NBR 6023:2025 evidence is obtained.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a mandatory complete **phase-end regression** on one immutable SHA; scoped intermediate checks never close a phase.
