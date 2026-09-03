# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation during the v3 reconstruction.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. Compare Git facts, machine state, handoff, and roadmap.
6. If phase, stage, branch, checkpoint, or temporary-artifact state disagrees, stop feature work and reconcile the control plane first.
7. Only after reconciliation inspect implementation details, pull requests, workflow history, or old commits.

Memory, old pull requests, workflow names, historical branches, and prior chat context never override the current repository state.

## Current reconstruction rules

- v3 target: `3.0.0`.
- R1 is structural reconstruction. Do not perform the Portuguese runtime API rewrite during R1; that belongs to R2.
- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- The active repository is not an archive. Historical evidence belongs in Git history, tags, releases, issues, pull requests, certified SHAs, and external verified backups.
- Do not create archive/history branches in the active repository.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before a checkpoint.
- Permanent automatic CI is introduced only through R1-BLOCK-7 and must remain a thin orchestration layer over repository-owned entry points.
- R1-BLOCK-7 is DONE. `Static contract`, `Linux integration`, and `Linux release check` are the only permanent workflows. B7-D confirmed read-only permissions, pinned actions, bounded concurrency, stable repository-owned entry points, and zero temporary workflow residue.
- The `Stable branches` ruleset currently has no required-status rule. The recorded recommendation is to require `Static contract` and `Linux integration`; `Linux release check` remains post-merge/manual.
- R1-BLOCK-8 is DONE. The certified R1 candidate is `9b1752565ac217c04ffa22a9ef272cdf078af380`.
- Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix; final Linux run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b.
- V3-R2 is DONE through R2-B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`. R2-A plus R2-B1 through R2-B5 are complete and recorded in `docs/R2-API-OWNERSHIP.md`.
- R2-B1 merged through PR #236 at `ded5e77733795aa2958606e899d4e27f12f64df4`; final `Linux integration` run `33668283890` passed `PASS=30 FAIL=0 SKIP=0`.
- R2-B2 merged through PR #242 at `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; final `Linux integration` run `33680378846` passed `PASS=30 FAIL=0 SKIP=0`, with strengthened residual audit `33680252116` green. Closeout PR #243 passed `Static contract` `33696690560` and `Linux integration` `33696690567` at `PASS=30 FAIL=0 SKIP=0`, then squash-merged as canonical B3 entry `0650845b922271fc134d20ef2a8c36ebb999ef91`; issue #237 is closed completed.
- R2-B3 is DONE through PR #245 at `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`; Static `33704346418` and Linux `33704346429` passed `PASS=30 FAIL=0 SKIP=0`. Structural/object APIs and project-owned object IDs are directly owned; genuine upstream `grafico` / `quadro` remain only at integration boundaries.
- R2-B4 is DONE through PR #247 at `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`; final Static `33736117556` and Linux `33736117558` passed `PASS=30 FAIL=0 SKIP=0`. Bibliography/reference/glossary/index commands are directly owned; B4 left `public-api.def` empty for its B5 physical removal.
- R2-B5/#240 is DONE. `public-api.def` and its class load are absent; `docs/MIGRATING-TO-V3.md` is the user migration guide; `tests/checks/v3_api_residual.py` is the permanent fail-closed residual gate. Static `33743809498`, Linux `33743809431`, and post-merge release `33745603468` are green.
- V3-R3 is ACTIVE in R3-A via issue #250. R3-A is inventory/planning only: classify standards/proof-state, semantic-test, and engineering-language gaps before defining implementation lots.
- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state unless explicit current evidence authorizes a normative change.
- Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not default cheap checks.
- Do not rerun completed checks unless current-state validation requires it.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before the roadmap reaches its explicit release-ready stage.

## Branch governance

The intended steady state is `main` plus only short-lived task branches. Merged or abandoned task branches are deleted promptly. Releases are preserved by immutable version tags and GitHub Releases, not permanent release/audit branches.

## Fail-closed rule

If a required fact cannot be established from the current Git repository and canonical state files, record the ambiguity and stop advancement to the next stage. Do not infer closure from naming, memory, historical intent, or a partial certification milestone.
