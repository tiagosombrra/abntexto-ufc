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
- V3-R3 is ACTIVE. R3-A/#250 is DONE from source baseline `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`; `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json` define the evidence-driven lot sequence.
- R3-B1/#252 is DONE through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. Static `33758758911` and Linux `33758758877` passed, with Linux `PASS=30 FAIL=0 SKIP=0`; the deliberate front-matter negative fixture was rejected on `dedication.position.start`.
- R3-B2/#253 is DONE through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. Static `33768911131` passed; Linux `33768911126` / job `100694266254` and independent validation `33768364069` passed `PASS=31 FAIL=0 SKIP=0`. Final contribution was 113/113 `automatic-partial` bounded-positive, 37 enforced-automatic, 14 support-only, 10 conditional-review, 6 manual-review, 1 not-applicable, zero automation gaps.
- R3-B3/#254 is DONE through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`, entered canonically after the B2→B3 control-plane checkpoint `44874c84b375396de8b9e3b24a40c47b5006f19b`. Static `33792280764` passed; Linux `33792280797` / job `100771483526` passed `PASS=31 FAIL=0 SKIP=0`; post-merge release `33794112546` / job `100777542613` passed `PASS=33 FAIL=0 SKIP=0`. The residual gate covers 302 behavior-relevant sources (134 LaTeX + 168 engineering), test/check reachability is 147/147 with zero orphans, and negative paths are coupled to positive PASS evidence by the same `rule_id`.
- R3-B4/#255 is DONE through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. Permanent engineering-language enforcement reports zero Portuguese project-owned technical diagnostics, zero retired profile IDs, zero closed unconsumed migration contracts and two live API-migration consumers; residual scope is 305 sources (134 LaTeX + 171 engineering), test/check reachability is 148/148 with zero orphans, PR Linux passed `PASS=31 FAIL=0 SKIP=0`, and post-merge release run `33816137774` passed `PASS=33 FAIL=0 SKIP=0`. B4→B5 control-plane PR #265 merged at `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` after Static `33817862525` and Linux `33817846901` = `PASS=31 FAIL=0 SKIP=0`. R3-B5/#256 is ACTIVE from that canonical checkpoint and owns R3 closeout plus the immutable R4 entry. Do not start R4 certification before B5 closes.
- R3-B1 established the front-matter fail-closed invariant. R3-B2 generalized evidence truthfulness: mechanism traceability, current rule-specific contribution and conservative proof state are distinct; `automatic-partial` contribution must come from a declared owner, `bounded-positive` is not `PROVEN`, and support-only evidence is never counted as enforcement.
- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state unless explicit current evidence authorizes a normative change.
- Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not default cheap checks.
- Do not rerun completed checks unless current-state validation requires it.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before the roadmap reaches its explicit release-ready stage.

## Branch governance

The intended steady state is `main` plus only short-lived task branches. Merged or abandoned task branches are deleted promptly. Releases are preserved by immutable version tags and GitHub Releases, not permanent release/audit branches.

## Fail-closed rule

If a required fact cannot be established from the current Git repository and canonical state files, record the ambiguity and stop advancement to the next stage. Do not infer closure from naming, memory, historical intent, or a partial certification milestone.
