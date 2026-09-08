# V3 Final Certification — Phase-end Regression

Updated: 2026-09-08
Status: CANDIDATE — RUNNING

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
| Step 8 transport preparation | `4d94e9cd7a565eac2e226360bd2b4a92fee52586`; Static `34235990523` SUCCESS; complete Linux `34235990383` SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |

## Candidate transport

The permanent `.github/workflows/linux-release-check.yml` supports normal `push` to `main`, `workflow_dispatch`, and a tightly scoped `pull_request` route only when `release/final-certification-candidate.json` is present in the PR diff. The marker is a one-shot transport trigger, not a second validator. The workflow executes the existing permanent repository contract `make release-check`.

The preparation transport is accepted. The marker is now present on the synchronized candidate and is removed only after candidate acceptance during the Final Certification -> Release transition.

## Candidate history

Marker-only/intermediate commits created before the synchronized control plane are **REJECTED AS CANDIDATES**. They did not satisfy the same-cycle documentation rule and therefore cannot close the phase, regardless of workflow outcome.

The synchronized candidate is the first commit containing both the marker and this candidate-running control state. Its exact SHA is obtained only after commit creation and then recorded externally in PR/evidence metadata. The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`.

## Immutable candidate gate

The synchronized candidate is not amended after CI begins. That exact candidate must pass:

1. Static contract;
2. complete Linux integration;
3. Linux release check running the permanent `make release-check` contract;
4. all accepted literal-font/Unicode/embedding/PDF-A/distribution predicates remain intact;
5. deterministic release-reference-PDF gate remains green;
6. no temporary certification executor is present;
7. librarian item 33 remains explicitly fail-closed.

Any failure is classified before code or test changes. A rejected candidate is never amended; a corrected state creates a new candidate commit.

## Exit rule

After the synchronized candidate passes the complete matrix, record its SHA and run IDs/conclusions, mark Final Certification `CLOSED`, activate `Release`, remove the one-shot candidate marker, and execute the phase-transition documentation cycle.
