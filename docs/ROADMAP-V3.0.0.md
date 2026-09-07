# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE. Step 6 is ACCEPTED and Step 7 canonical article PDF validation is ACTIVE.**

| Phase | Status | Current exit requirement |
|---|---|---|
| Regression Audit | CLOSED | completed regression contract and phase-end regression |
| Core Corrections | CLOSED | candidate `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | candidate `b64074c...`; complete 55-page visual PASS + Static/Linux |
| Scientific Article | **ACTIVE — STEP 7** | canonical article PDF acceptance + Step 8 complete phase-end regression |
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
| 7 | Canonical article PDF | **ACTIVE** | real TeX Live 2026 PDF, Git provenance, every page visually inspected, temporary executor absent at acceptance |
| 8 | Scientific Article phase-end regression | QUEUED | Static + `complete` Linux + article gates on one immutable SHA |

Step 6 remains deliberately conservative: `standards/article-evidence-map.json` maps all 18 retained rules but changes zero validation modes. Required rules may have direct article-specific executable support without being promoted to full normative proof. Optional elements remain optional, recommendation rules remain manual/non-enforcing, and target-journal precedence remains conditional-manual.

## Step 7 presentation gate

The article PDF is a new canonical artifact, separate from the accepted 55-page academic-work reference PDF. Step 7 requires:

- a dedicated canonical article source exercising the accepted public runtime;
- real TeX Live 2026 compilation;
- provenance bound to a concrete Git SHA and workflow run;
- PDF hash/metadata preflight;
- complete page-by-page visual inspection;
- explicit checks for article front matter and absence of academic-work front-matter leakage;
- removal of any temporary build workflow before Step 7 is accepted.

Synthetic PDFs are not admissible.

## After Scientific Article

### Final Certification

Must run on the accepted final candidate and cover at least all document profiles, pdfLaTeX/LuaLaTeX, literal Times New Roman and Arial identity where required, Unicode extraction, font embedding, PDF/A-2b, distribution/public bundle checks, and release-reference-PDF reproducibility evidence required by issue #18.

### Release

Only after Final Certification: finalize documentation, build bundles, generate and verify checksums/assets, resolve blockers, create immutable `v3.0.0` tag and GitHub Release, and perform external publication/CTAN action only in this phase.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains explicit/fail-closed unless authoritative current-edition NBR 6023:2025 evidence is obtained.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a mandatory complete **phase-end regression** on one immutable SHA; scoped intermediate checks never close a phase.
