# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE. Steps 1–6 are ACCEPTED. Step 7 has a provenance-bound 5-page visual PASS and is at the cleanup-checkpoint CI gate.**

| Phase | Status | Current exit requirement |
|---|---|---|
| Regression Audit | CLOSED | completed regression contract and phase-end regression |
| Core Corrections | CLOSED | candidate `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | candidate `b64074c...`; complete 55-page visual PASS + Static/Linux |
| Scientific Article | **ACTIVE — STEP 7 CLEANUP CI** | Step 7 cleanup acceptance + Step 8 complete phase-end regression |
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
| 6 | Exact 18-rule evidence ownership map | ACCEPTED | `e941a7f9...`; Static `34146793998`; Linux `34146794016`; zero validation-mode promotions |
| 7 | Canonical article PDF | **VISUAL-PASS — CLEANUP CI PENDING** | artifact `f62ac703...`; run `34153348385`; 5/5 visual PASS; temporary executor removed; cleanup checkpoint CI must pass |
| 8 | Scientific Article phase-end regression | QUEUED | Static + `complete` Linux + article gates on one immutable SHA |

## Step 7 artifact

| Evidence | Result |
|---|---|
| Source | `template/scientific-article.tex` |
| Build SHA | `f62ac703d8992af96b79cf83e125350ee561bd92` |
| Workflow | `34153348385` — SUCCESS |
| PDF SHA-256 | `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db` |
| Pages | 5 |
| Geometry | A4 |
| Embedded fonts | PASS |
| Complete visual review | PASS — 5/5 |
| Unexplained visual FAIL | 0 |
| Temporary executor | removed by cleanup checkpoint |

Primary-section new-page behavior is recorded as a **non-blocking observation**. The retained article contract defines section presence and body typography but does not define a no-page-break predicate; no new requirement is invented from presentation preference.

## Next gate

After the cleanup checkpoint is green, Step 7 becomes ACCEPTED and Step 8 becomes ACTIVE. Step 8 must use one immutable candidate and `complete` Linux scope; scoped intermediate runs cannot close Scientific Article.

## After Scientific Article

Final Certification must run on the accepted final candidate and cover all profiles, pdfLaTeX/LuaLaTeX, literal Times New Roman and Arial identity where required, Unicode extraction, font embedding, PDF/A-2b, distribution/public bundle checks, and issue #18 reproducibility evidence.

Release follows only after Final Certification and includes final documentation, bundles, checksums/assets, immutable `v3.0.0` tag/GitHub Release and external publication actions.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains explicit/fail-closed unless authoritative current-edition NBR 6023:2025 evidence is obtained.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a mandatory complete **phase-end regression** on one immutable SHA; scoped intermediate checks never close a phase.
