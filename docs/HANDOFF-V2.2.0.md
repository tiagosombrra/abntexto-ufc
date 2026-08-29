# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-29

Checkpoint: **N15-B2R is fully DONE and re-certified. N15-B2B scientific-article runtime is ACTIVE on `feat/n15-b2b-scientific-article-runtime`, created from certified `main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`.**

Live Git/PR/CI state is the execution authority. Do not create receipt-only follow-up commits merely to record transient SHAs.

## Mandatory guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording or locators;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- v2.x public API migration is additive;
- supported Portuguese setup keys/values/commands/environments remain supported;
- final B2R public-API runtime blob: `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- final B2R inventory remains exactly 132 setup keys / 79 scoped values / 77 commands / 11 environments / 2 extension hooks;
- B2B article values are a later layered delta and do not rewrite those historical counts;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles;
- class version remains v2.1.0 until N15-C;
- physical branch cleanup remains deferred until final certification/tag;
- N15-B2C may begin only after B2B exact-head merge and resulting-main certification.

## Canonical roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| N0–N14 | normative/runtime/evidence baseline | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 |
| N15-B1 | source completeness/authority reconciliation | DONE — PR #144 |
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 |
| N15-B2R-A1 | internal module English naming | DONE — PR #146 |
| N15-B2R-A2 | user/example/distribution layout naming | DONE — PR #148 + state sync |
| N15-B2R-B1 | public-API baseline + executable contract | DONE — PR #150 + PR #151 |
| N15-B2R-B2 | canonical setup keys/values + Portuguese compatibility | DONE — PR #152 + PR #153 |
| N15-B2R-B3 | canonical commands/environments + compatibility wrappers | DONE — PR #154 |
| N15-B2R-B4 | EN/PT semantic/output equivalence | DONE — PR #155 |
| B2R-B4 state sync | bounded documentation closure | DONE — PR #156 |
| N15-B2B | scientific-article runtime | ACTIVE |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B certification |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by N15-B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## Certified B2R closure and B2B base

PR #156 exact head:

`1a4b5feb5517dd820d010613b24d2fffd346d6e5`

Pre-merge closure:

- `behind_by=0`;
- Normative Source Contract #444 — SUCCESS, run `33265851911`;
- LaTeX preflight #1118 — SUCCESS, run `33265851907`.

Protected squash merge produced:

`main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`

That exact main is the certified N15-B2B base. Post-merge certification:

- Normative Source Contract #445 — SUCCESS, run `33266313000`;
- LaTeX preflight/Gate T #1119 — SUCCESS, run `33266312999`;
- Distribution #250 — SUCCESS, run `33266313007`.

Gate T #1119 confirmed:

- reference document + PDF/A-2b;
- 12-profile matrix + PDF/A-2b;
- objects/bibliography;
- post-textuals;
- layout/fonts/pre-textuals/projects structure;
- Overleaf stable proxy;
- Windows literal Times New Roman/Arial build;
- Windows literal-font identity, Unicode extraction, embedding and PDF/A-2b certification;
- aggregate `latex-preflight`.

Distribution #250 confirmed:

- Gate T prerequisite;
- release preflight;
- release PDF/A-2b;
- deterministic release bundles;
- Overleaf import bundle proxy;
- candidate upload;
- aggregate distribution preflight.

GitHub Release publication was correctly skipped because no release tag exists.

## Frozen B2R contracts

- B1 public-API baseline: `release/n15-b2r-b-public-api.json`, blob `c1f545e0e707822959db851a74d29f4068dff731`;
- B2 setup aliases: `release/n15-b2r-b2-setup-aliases.json`, blob `19df208fb59af5ea37556d962e5986a43094c7f5`;
- B3 command/environment aliases: `release/n15-b2r-b3-command-environment-aliases.json`, blob `bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`;
- B4 equivalence record: `release/n15-b2r-b4-en-pt-equivalence.json`;
- public-API runtime: `abntexto-ufc/public-api.def`, blob `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- N12 workflow: blob `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

Final B2R public inventory:

- 67 compatibility setup keys + 65 canonical setup keys = 132;
- 45 compatibility scoped values + 34 canonical scoped values = 79;
- 47 prior commands + 30 canonical commands = 77;
- 6 prior UFC environments + 5 canonical environments = 11;
- 2 extension hooks unchanged.

Portuguese v2.x compatibility remains supported.

## N15-B2B — scientific-article runtime — ACTIVE

Branch:

`feat/n15-b2b-scientific-article-runtime`

Base:

`ce659b578b4fc9cc929af4aadc3e613df469ba77`

Source-backed normative contract:

- `normativa/coverage-rules-article.json`;
- blob `5612c07841dad97b915af88474f9b48d8346597e`;
- 13 reviewed `article.*` predicates from N15-B2A.

Machine runtime ledger:

`release/n15-b2b-article-runtime.json`

### B2B runtime boundary

B2B is deliberately smaller than a new document-class API redesign.

It adds only the previously reserved scoped values:

- canonical `type=article`;
- compatibility `tipo=artigo`.

It adds no setup key, public command, public environment or extension hook. It reuses existing metadata and command surfaces and keeps `abntexto-ufc/public-api.def` byte-frozen.

The implementation lives in:

`abntexto-ufc/articles.def`

The class loads it after bibliography compatibility and before backmatter/public API so it can specialize existing behavior only for the article profile while canonical wrappers continue to target the same underlying commands.

### Article profile behavior under B2A contract

The active implementation targets:

- A4;
- margins 3 cm left/top and 2 cm right/bottom;
- single-sided layout regardless of a conflicting general print-mode input;
- visible Arabic pagination from page 1, upper-right at the institutional offsets;
- 12 pt text, justified, single spacing, 2 cm first-line indent;
- first-page title/authorship/submission-date/approval-date block;
- inline `Resumo` + palavras-chave and `Abstract` + keywords without separate pre-textual pages;
- required numbered textual sections Introdução, Desenvolvimento and Considerações finais;
- continuous primary-section flow without automatic page starts;
- references in the same article flow rather than on a forced new page;
- no separate cover, title leaf, approval leaf or table of contents for article profile.

Recommendations such as 150–250 summary words, at least three keywords and Arial/Times New Roman remain advisory and are not hard errors.

### Reused public surfaces

- `author`, `title`, `subtitle`, `title-variant`;
- `approval-date`;
- standard LaTeX `\date{...}` for submission date;
- `\ufcPrintSummary`;
- `\ufcPrintAbstract`;
- `\ufcPrintReferences`;
- existing canonical/compatibility cover/title/approval/TOC calls, which dispatch to article no-op or first-page behavior as appropriate.

Author curriculum/affiliation/contact are represented by a footnote attached to the existing author content in the B2B baseline rather than by widening the public metadata surface.

### Runtime ownership rule

`layout.def` remains the unique owner of the internal primary-section break implementation. `articles.def` must not redefine that internal function. Continuous article flow is achieved by conditional specialization of the already exported `\ufcPrimarySectionBreak` and `\ufcPretextualBreak` commands.

This protects the repository's internal ownership invariant and avoids regressions in academic-work/project profiles.

### B2B executable checks

New B2B checks:

- `tests/checks/article_runtime_contract.py` — freezes B2A/B2R/N12 inputs and verifies the article delta boundary;
- `tests/v2-article-check.sh` — builds canonical article with pdfLaTeX/LuaLaTeX, validates semantic structure, PDF/A, font embedding, A4 geometry, first-page pagination, continuous sections and canonical/PT equivalence;
- `tests/smoke/perfil-artigo.tex` — canonical article fixture;
- `tests/fixtures/artigo-resumo.tex` and `tests/fixtures/artigo-abstract.tex` — language-specific front-matter fixtures.

`tests/run.py` registers `article-runtime` and makes the existing `profiles` check depend on it. This routes B2B through the frozen N12 workflow without modifying `.github/workflows/latex-preflight.yml`.

### Existing-profile non-regression

The original six document profiles remain in the 12-build matrix across pdfLaTeX/LuaLaTeX. B2B's new article gate runs in addition to that matrix; it does not replace or weaken it.

## Immediate closure procedure for B2B

1. finish static review of the B2B branch and ensure documentation/ledger match the implementation;
2. open the B2B PR from the exact branch head to `main`;
3. require exact-head Source + LaTeX preflight SUCCESS;
4. inspect article-runtime evidence and any exact failed logs rather than weakening checks speculatively;
5. require `behind_by=0`;
6. squash-merge with expected-head protection;
7. re-certify resulting `main` through Source, Gate T and Distribution;
8. synchronize B2B status to DONE without creating an unbounded receipt loop;
9. only then begin N15-B2C evidence/proof-state closure.

## Next phase — N15-B2C

B2C is not a second runtime implementation. Its responsibility is evidence closure: connect the B2A predicates to the certified B2B runtime observations, strengthen any missing automated evidence where justified, update proof-state artifacts without overstating what is proven, and prepare article support for the N15-B3 pre-release sweep.
