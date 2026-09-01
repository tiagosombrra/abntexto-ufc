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
- Permanent automatic CI is introduced only through R1-BLOCK-7 and must remain a thin orchestration layer over repository-owned entry points. `Static contract` is the current permanent fast workflow and delegates to `make static-check`.
- B7-C1 certified the repository-owned `make check` contract on a clean TeX Live 2026 runner. B7-C2 is DONE and permanently provides `.github/workflows/linux-integration.yml` with stable `Linux integration` status: draft and narrowly allowlisted documentation/control-plane-only PRs skip the expensive TeX step, every other or unknown path runs `make check`, superseded PR runs are cancelled, and manual dispatch forces full integration. B7-C3 is ACTIVE and may add only bounded release orchestration as a thin consumer of `make release-check`. Final Windows/font/PDF-A certification remains B8-owned.
- Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not default cheap checks.
- Do not rerun completed checks unless current-state validation requires it.

## Branch governance

The intended steady state is `main` plus only short-lived task branches. Merged or abandoned task branches are deleted promptly. Releases are preserved by immutable version tags and GitHub Releases, not permanent release/audit branches.

## Fail-closed rule

If a required fact cannot be established from the current Git repository and canonical state files, record the ambiguity and stop advancement to the next stage. Do not infer closure from naming, memory, or historical intent.
