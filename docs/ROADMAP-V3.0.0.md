# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-09

## Current status

**Release is ACTIVE — GitHub publication is complete; maintainer all-profile visual validation is now the active pre-CTAN gate.** The immutable `v3.0.0` tag resolves to `05399473827da7cf6b6c8bac36edc7115481773f`, and GitHub Release `385743477` is published with byte-verified frozen assets.

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | heavy technical matrix accepted |
| Release | **ACTIVE — VISUAL VALIDATION PENDING** | generate and visually accept all seven canonical profile PDFs + sources; only then submit the frozen canonical ZIP to CTAN and preserve external evidence |

## Current Release facts

| Predicate | Current result |
|---|---|
| Certified source SHA | `05399473827da7cf6b6c8bac36edc7115481773f` |
| Immutable tag | `v3.0.0` → `05399473827da7cf6b6c8bac36edc7115481773f` |
| GitHub Release | **PUBLISHED** — https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.0 |
| Distribution artifact | `10117679639` (`sha256:7ee1b6bf4b1d54ac041db1e624d8bfcf52a1dc43897c1542b9fd969b971f40df`) |
| CTAN upload archive | `abntexto-ufc-3.0.0.zip` only (`sha256:d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71`) |
| CTAN project runtime | **`abntexto-ufc.cls` only; 0 `.def`** |
| `pkgcheck` | **PASS** — 4.1.0, zero warnings/errors |
| GitHub asset re-download | **PASS / byte-identical** |
| All-profile source/PDF generation | **ACTIVE** |
| Maintainer visual acceptance | **PENDING** |
| CTAN submission | **BLOCKED BY VISUAL ACCEPTANCE** |
| CTAN acceptance/install | **PENDING** |

## R0 — Publication documentation and package identity

**CLOSED.** Root/CTAN documentation is v3-oriented; `abntexto-ufc` replaces the historical package identity; the canonical CTAN upload is one archive; logo/font redistribution is prohibited.

## R1 — Normative item 33

**CLOSED / PASS.** Primary ABNT NBR 6023:2025 authority and executable tests cover DOI + applicable online availability/access elements, repeated authorship, legal-person authorship, and `SÃO PAULO (Estado)` jurisdiction disambiguation. The class explicitly requests `repeatfields=true` from `biblatex`.

## R2 — Monolithic CTAN runtime

**CLOSED / PASS ON FINAL PUBLICATION BYTES.** The repository stays modular. The CTAN builder recursively inlines all 14 tracked project-owned `.def` modules into one generated `abntexto-ufc.cls`; the final certified ZIP contains zero `.def` files and passed isolated compilation, deterministic rebuild and prohibited-asset checks.

Canonical CTAN content:

```text
abntexto-ufc/
├── README.md
├── CHANGELOG
├── LICENSE
├── abntexto-ufc.cls
├── abntexto-ufc.tex
├── abntexto-ufc.pdf
├── abntexto-ufc-example.tex
└── abntexto-ufc-example.pdf
```

Final evidence confirms all 14 tracked runtime modules inlined exactly once, no residual project-owned `.def` input, zero `.def` files in the ZIP, isolated example compilation, deterministic rebuild and no prohibited assets.

## R3 — Final exact-main recertification

**CLOSED / PASS.** Exact source `05399473827da7cf6b6c8bac36edc7115481773f` passed Static, complete Linux integration, Linux release check (`SCOPE=complete PASS=38 FAIL=0 SKIP=0`), deterministic distribution and final package audit.

## R4 — CTAN `pkgcheck`

**CLOSED / PASS.** `pkgcheck 4.1.0` passed on `d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71` with exit 0, zero warnings and zero errors/fatals. Evidence run `34386932488` / artifact `10118176687`.

## R5 — Freeze, tag and GitHub Release

**CLOSED / PASS.** Frozen bytes were tagged as immutable `v3.0.0`, published in GitHub Release `385743477`, re-downloaded before and after publication and proved byte-identical. Recovery verification run `34387825056` retained evidence artifact `10118391678`.

## R6 — All-profile maintainer visual validation

**ACTIVE.** Generate and present source + final PDF for every canonical class profile from the frozen `v3.0.0` implementation:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

The review bundle must include profile-specific `.tex`, PDF, build metadata/log and SHA-256 manifest. Automated compilation is necessary but not sufficient. This stage closes only after explicit maintainer acceptance of all seven rendered outputs. Detailed state lives in `docs/V3-VISUAL-VALIDATION.md`.

A material defect discovered here must not alter or retarget `v3.0.0`; it opens a correction/new-version cycle before CTAN submission.

## R7 — CTAN submission

**BLOCKED BY R6.** After maintainer visual acceptance, submit exactly one frozen file: `abntexto-ufc-3.0.0.zip`. Preserve the submission receipt, submitted hash and later acceptance/catalog/install evidence.

## R8 — Release closeout

**BLOCKED BY R7 EXTERNAL VERIFICATION.** After CTAN acceptance/catalog evidence, synchronize final state and mark Release `CLOSED`.

## Operating discipline

Every **material advance** or material repository modification must update affected documentation and machine state in the same work cycle. `README.md` is updated when user-facing facts change, not for transient branch/CI progress. Targeted checks never replace the final phase-end regression, and automated success never replaces the explicit maintainer visual-acceptance gate introduced for the seven canonical profiles.
