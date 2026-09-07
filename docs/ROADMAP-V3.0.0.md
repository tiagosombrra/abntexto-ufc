# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE. Step 6 evidence hardening is implemented and awaiting synchronized CI acceptance.**

| Phase | Status | Current exit requirement |
|---|---|---|
| Regression Audit | CLOSED | Completed regression contract and phase-end regression |
| Core Corrections | CLOSED | Candidate `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | Candidate `b64074c...`; complete 55-page visual PASS + Static/Linux |
| Scientific Article | **ACTIVE — STEP 6 CI PENDING** | Steps 6–8 below |
| Final Certification | QUEUED | Complete platform/font/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | Packaging, checksums, tag/release and publication verification |

Canonical `main` is `fbf7cc4839ce318024a7d1ed517dd50fab5773ac`. PR #288 fixed the stale README/control-plane state on main. Active article work is PR #286 on `feat/v3-scientific-article`, reconciled with current main through `85cf22b6fe5d117bb2611a2865911e0d20a19363`.

## Scientific Article remaining roadmap

| Step | Work | State | Gate |
|---:|---|---|---|
| 1 | Profile and metadata | ACCEPTED | completed |
| 2 | Required front block | ACCEPTED | completed |
| 3 | Optional foreign title/summary | ACCEPTED | completed |
| 4 | Body structure and typography | ACCEPTED | completed |
| 5 | Recommendations and journal applicability | ACCEPTED | completed |
| 6 | Exact 18-rule evidence ownership map | **IMPLEMENTED — CI PENDING** | Static + selected Linux scope green on synchronized checkpoint |
| 7 | Canonical article PDF | QUEUED | real TeX Live 2026 PDF, Git provenance, every page visually inspected |
| 8 | Scientific Article phase-end regression | QUEUED | Static + `complete` Linux + article gates on one immutable SHA |

Step 6 is deliberately conservative: `standards/article-evidence-map.json` maps all 18 retained rules but changes **zero** validation modes. Required rules may have direct article-specific executable support without being promoted to full normative proof. Optional elements remain optional, recommendation rules remain manual/non-enforcing, and target-journal precedence remains conditional-manual.

## After Scientific Article

### Final Certification

Must run on the accepted final candidate and cover at least:

- all document profiles, including Scientific Article;
- pdfLaTeX and LuaLaTeX;
- literal Times New Roman and Arial identity where certification requires it;
- Unicode extraction;
- font embedding;
- PDF/A-2b;
- distribution/public bundle checks;
- release-reference-PDF reproducibility evidence required by issue #18.

### Release

Only after Final Certification:

- finalize user/developer documentation;
- build public/distribution bundles;
- generate and verify checksums/assets;
- resolve release-readiness blockers;
- create immutable `v3.0.0` tag and GitHub Release;
- perform any external publication/CTAN action only in this phase.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 is not converted into speculative NBR 6023:2025 runtime behavior. It remains explicit/fail-closed unless authoritative current-edition evidence is obtained.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a mandatory complete **phase-end regression** on one immutable SHA; scoped intermediate checks never close a phase.
