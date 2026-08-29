# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-29

Checkpoint: **N15-B2R is technically closed. B2R-B4 is DONE and fully certified on `main` `a4f2660ef46826c7d61a7dc3d9de6554f6d6a825`. This branch performs the bounded post-merge documentation sync only. Scientific-article runtime N15-B2B remains blocked until this state-sync is exact-head certified, merged, and the resulting `main` is re-certified.**

State-sync branch:

`docs/n15-b2r-b4-post-merge-sync`

Live Git/PR/CI state is the execution authority. Do not create receipt-only follow-up commits merely to record transient state-sync SHAs.

## Mandatory guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording or locators;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- v2.x public API migration is additive;
- supported Portuguese setup keys/values/commands/environments remain supported;
- final B2R public-API runtime blob: `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- final B2R inventory remains exactly 132 setup keys / 79 scoped values / 77 commands / 11 environments / 2 extension hooks;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles;
- class version remains v2.1.0 until N15-C;
- physical branch cleanup remains deferred until final certification/tag;
- N15-B2B must start only from the certified `main` produced after this bounded state-sync.

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
| N15-B2R-B4 | EN/PT semantic/output equivalence + exact-head closure | DONE — PR #155 |
| B2R-B4 state sync | bounded documentation closure | ACTIVE |
| N15-B2B | scientific-article runtime | BLOCKED only by state-sync certification |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by N15-B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## Frozen B2R contracts

- B1 public-API baseline: `release/n15-b2r-b-public-api.json`, blob `c1f545e0e707822959db851a74d29f4068dff731`;
- B2 setup aliases: `release/n15-b2r-b2-setup-aliases.json`, blob `19df208fb59af5ea37556d962e5986a43094c7f5`;
- B3 command/environment aliases: `release/n15-b2r-b3-command-environment-aliases.json`, blob `bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`;
- B4 equivalence record: `release/n15-b2r-b4-en-pt-equivalence.json`;
- public-API runtime: `abntexto-ufc/public-api.def`, blob `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- N12 workflow: blob `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

Final public inventory:

- 67 compatibility setup keys + 65 canonical setup keys = 132;
- 45 compatibility scoped values + 34 canonical scoped values = 79;
- 47 prior commands + 30 canonical commands = 77;
- 6 prior UFC environments + 5 canonical environments = 11;
- 2 extension hooks unchanged.

Portuguese v2.x compatibility remains supported. `type=article` and its compatibility form remain reserved-only until N15-B2B implements runtime support.

## B2R-B4 — DONE

B4 certified that the completed canonical-English public vocabulary is behaviorally equivalent to the supported Portuguese compatibility vocabulary without changing the frozen runtime.

Observable equivalence required and passed:

1. exact reviewed setup/command/environment forwarding;
2. exact normalized internal-state equality;
3. exact `pdftotext -layout` equality;
4. equal page count and page dimensions;
5. equal generated TOC/list/bibliography artifacts;
6. equal fixed-parameter per-page raster SHA-256;
7. PDF/A-2b declaration for both paired outputs.

Final B4 runtime evidence on the exact PR head reported:

- 66 normalized state lines equal;
- 23 pages;
- raster SHA-256 equality across all 23 pages;
- state/text/geometry/auxiliary/raster/PDF-A predicates all `true`;
- structural validation `PASS=16 FAIL=0 SKIP=0`;
- no public-runtime/API divergence observed.

### PR #155 exact-head closure

Final exact PR head:

`44c9c5082598b82e67a0b3ef009c4bb71a584571`

Pre-merge state:

- `behind_by=0`;
- Normative Source Contract #442 — SUCCESS, run `33262519263`;
- LaTeX preflight #1115 — SUCCESS, run `33262519254`;
- B4 paired equivalence gate — SUCCESS.

PR #155 was squash-merged with expected-head protection, producing:

`main` `a4f2660ef46826c7d61a7dc3d9de6554f6d6a825`

### Post-merge certification

On exact `main` `a4f2660e...`:

- Normative Source Contract #443 — SUCCESS, run `33263191118`;
- LaTeX preflight push #1116 — SUCCESS, run `33263191096`;
- exact/dispatched Gate T #1117 — SUCCESS, run `33263196260`;
- Distribution #249 — SUCCESS, run `33263191120`.

Gate T #1117 confirmed SUCCESS for:

- reference document + PDF/A-2b;
- 12-profile matrix + PDF/A-2b;
- objects/bibliography;
- post-textuals;
- layout/fonts/pre-textuals/projects structure including B4;
- Overleaf stable proxy;
- Windows literal Times New Roman/Arial build;
- Windows literal-font identity, Unicode extraction, embedding and PDF/A-2b certification;
- aggregate `latex-preflight`.

Distribution #249 confirmed SUCCESS for:

- Gate T prerequisite;
- release preflight;
- release PDF/A-2b;
- deterministic release bundles;
- Overleaf import bundle proxy;
- candidate upload;
- aggregate distribution preflight.

GitHub Release publication was correctly skipped because no release tag exists.

## State-sync closure rule

This branch is documentation-only. It must not modify runtime, tests, normative contracts or workflows. Closure procedure:

1. exact-head Source + LaTeX preflight SUCCESS;
2. `behind_by=0`;
3. squash-merge with expected-head protection;
4. re-certify resulting `main` through Source, Gate T and Distribution;
5. do not create another receipt-only documentation PR;
6. after the resulting `main` is certified, begin N15-B2B from that exact SHA.

The state-sync PR body/final execution report may record its own exact-head and resulting-main receipts; the tracked documentation does not need an unbounded receipt loop.

## Next phase — N15-B2B

N15-B2B is the first runtime phase after B2R. It must consume the already-approved scientific-article source/normative contract from N15-B2A and implement canonical article support without weakening the certified thesis/dissertation/project profiles.

Before implementation, re-open the B2A contract and current profile-routing code, then define the smallest runtime delta. Expected canonical engineering surface remains `articles.def` and reserved setup value `type=article`; Portuguese compatibility must follow the established additive v2.x policy.
