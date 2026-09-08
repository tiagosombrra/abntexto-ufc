# V3 Final Certification — Phase-end Regression

Updated: 2026-09-08
Status: PREPARATION — RELEASE-MATRIX PR TRANSPORT

## Purpose

This document binds Final Certification Step 8 to one immutable candidate. Every **material advance** remains synchronized with handoff, roadmap, readiness and `release/v3-roadmap.json`. Targeted checks do not replace the mandatory **phase-end regression**.

## Accepted prerequisites

| Surface | Accepted evidence |
|---|---|
| Steps 1-6 | ACCEPTED |
| Step 7 deterministic proof | `34231038578` — SUCCESS |
| Step 7 cleanup | `34e6bf8299e582803d1726e8dd699271c356fda5`; Static `34232017286`; complete Linux `34232017359` |
| Deterministic PDF | 2 clean builds; SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` |
| Temporary executor | absent |
| Permanent reproducibility gate | `make release-reference-reproducibility` inside `make release-check` |
| Issue #18 | CLOSED — completed |

## Step 8 release-matrix transport

The permanent `.github/workflows/linux-release-check.yml` supports two production paths and one tightly scoped certification path:

- `push` to `main`, unchanged for normal release validation;
- `workflow_dispatch`, unchanged for manual execution;
- `pull_request` only when `release/final-certification-candidate.json` is present in the PR diff.

The candidate marker is a one-shot Final Certification transport trigger, not a second validator and not a replacement for `make release-check`. The workflow executes the same permanent repository release contract. The marker is removed in the phase-transition cleanup after the immutable candidate is accepted.

This orchestration change must pass Static and complete Linux before the immutable candidate is created.

## Immutable candidate gate

The candidate commit will add `release/final-certification-candidate.json` and synchronously mark Step 8 as running. It is not amended after CI begins. That exact candidate must pass:

1. Static contract;
2. complete Linux integration;
3. Linux release check running the permanent `make release-check` contract;
4. all accepted literal-font/Unicode/embedding/PDF-A/distribution predicates remain intact;
5. deterministic release-reference-PDF gate remains green;
6. no temporary certification executor is present;
7. librarian item 33 remains explicitly fail-closed.

The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`; the exact Git candidate SHA is recorded only after the immutable commit exists.

## Exit rule

After the candidate passes the complete matrix, record its SHA/run IDs, mark Final Certification `CLOSED`, activate `Release`, remove the one-shot candidate marker, and execute the phase-transition documentation cycle. Any failure is classified before code or test changes.
