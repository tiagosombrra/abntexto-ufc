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
- R1-BLOCK-8 is ACTIVE via issue #227. PR #230 merged the bounded Windows/literal-font tooling repair at `d2c24fc85351a410ea1f0101887b2a5228077741`.
- B8 strict POC certification is DONE: run `33609817951` generated Times New Roman/Arial × pdfLaTeX/LuaLaTeX on hosted Windows; Linux certification verified literal identity, Unicode extraction, embedding and PDF/A-2b for all four artifacts.
- B8 is not closed by the POC. The immediate product gate is full `template/main.tex` certification from the canonical merged B8 tooling checkpoint, followed by final control-plane reconciliation and issue #227 closure only if that candidate proof passes fail-closed.
- Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not default cheap checks.
- Do not rerun completed checks unless current-state validation requires it.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission or V3-R2 runtime/API migration while R1-BLOCK-8 remains active.

## Branch governance

The intended steady state is `main` plus only short-lived task branches. Merged or abandoned task branches are deleted promptly. Releases are preserved by immutable version tags and GitHub Releases, not permanent release/audit branches.

## Fail-closed rule

If a required fact cannot be established from the current Git repository and canonical state files, record the ambiguity and stop advancement to the next stage. Do not infer closure from naming, memory, historical intent, or a partial certification milestone.
