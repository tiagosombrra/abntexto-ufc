# V3.0.0 Continuation Handoff

Updated: 2026-09-09
Status: RELEASE — PUBLICATION HARDENING

This file is the shortest safe entry point for continuing v3 work from a new ChatGPT conversation, Codex session or local clone.

## Canonical starting point

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` — resolve current SHA dynamically from `origin/main` |
| Active roadmap phase | **Release** |
| Active work branch | `release/v3-publication-hardening` |
| Previous Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — technically accepted, **SUPERSEDED FOR PUBLICATION** |
| Previous retained artifact | ID `10086299397` — historical evidence only; never publish as v3.0.0 final |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| Package id | `abntexto-ufc` |
| CTAN upload contract | exactly one archive: `abntexto-ufc-3.0.0.zip` |
| Tag contract | `v3.0.0` must point to the exact final certified `main` SHA |
| pkgcheck contract | current CTAN `pkgcheck` must pass before tag creation |

## Why the previous candidate was superseded

The prior candidate's implementation/regression evidence remains useful, but the retained release bytes contained stale publication text: the canonical archive described v2.1.0 as the stable version and the CTAN README described v3.0.0 as a development candidate. Because accepted publication bytes cannot be rebuilt in place, that candidate is not a valid final-publication source.

Release was therefore reopened only for publication hardening and the bibliography item-33 normative closure; Core Corrections, Reference PDF Validation and Scientific Article are not generically reopened.

## Publication-hardening contract

- root README is v3-oriented;
- CTAN README contains final version/license/maintainer/dependency metadata;
- no UFC logo, coat of arms or other institutional mark is redistributed;
- no proprietary Microsoft font file is redistributed;
- canonical `abntexto-ufc-3.0.0.zip` is itself CTAN-grade;
- separate template and Overleaf ZIPs are GitHub conveniences only;
- CTAN package contains runtime, README, CHANGELOG, LICENSE, manual source/PDF and minimal example source/PDF;
- repository tests/workflows/validators/evidence/roadmaps/tools are excluded from CTAN;
- stale `ufctex`, v2-publication and `development candidate` wording fails the distribution gate;
- filenames, line endings, permissions, empty files and archive layout are checked fail-closed.

## Normative item 33

The earlier NBR 6023:2025 authority gap is closed using primary current-edition evidence. Regression fixtures now verify DOI plus online availability/access data, explicit repeated authorship, legal-person authorship and `SÃO PAULO (Estado)` jurisdiction disambiguation. The class explicitly requests `repeatfields=true` from `biblatex`.

## Remaining work

1. finish publication-hardening integration and pass PR Static + complete Linux/release CI;
2. merge by the repository's protected squash workflow;
3. resolve the exact resulting `origin/main` SHA;
4. run the final **phase-end regression** on that exact SHA;
5. build the three deterministic ZIPs + `SHA256SUMS` from that exact SHA;
6. run the current CTAN `pkgcheck` against `abntexto-ufc-3.0.0.zip` and preserve version/output/hash evidence;
7. freeze bytes and hashes;
8. create immutable `v3.0.0` on that same certified SHA;
9. create GitHub Release, attach exact frozen assets, re-download and verify hashes;
10. submit only `abntexto-ufc-3.0.0.zip` to CTAN and preserve receipt/acceptance evidence;
11. synchronize final publication state and close Release only after verification.

Invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Local continuation

```bash
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
git rev-parse HEAD
```

Then read:

1. `AGENTS.md`
2. `release/v3-roadmap.json`
3. `docs/V3-CONTINUATION.md`
4. `docs/HANDOFF-V3.0.0.md`
5. `docs/ROADMAP-V3.0.0.md`
6. `docs/V3-RELEASE-READINESS.md`
7. `docs/V3-RELEASE-PHASE-END.md`
8. `docs/CTAN-RELEASE.md`
9. `docs/UFC-LIBRARIAN-REVIEW.md`

Every **material advance** updates the relevant control documents in the same work cycle. A targeted check never replaces the required final **phase-end regression**.
