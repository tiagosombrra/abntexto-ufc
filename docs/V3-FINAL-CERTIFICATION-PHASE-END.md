# V3 Final Certification — Phase-end Regression

Updated: 2026-09-08
Status: PREPARATION

## Purpose

This document binds Final Certification Step 8 to one immutable candidate. Every **material advance** must remain synchronized with the handoff, roadmap, readiness document and `release/v3-roadmap.json`. Targeted checks do not replace the mandatory **phase-end regression**.

## Accepted prerequisites

| Surface | Accepted evidence |
|---|---|
| Steps 1-6 | ACCEPTED |
| Step 7 deterministic proof | run `34231038578` — SUCCESS |
| Step 7 clean source | `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` |
| Deterministic PDF | 2 clean builds, SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` |
| Step 7 cleanup checkpoint | `34e6bf8299e582803d1726e8dd699271c356fda5` |
| Cleanup Static | `34232017286` — SUCCESS |
| Cleanup Linux | `34232017359` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Temporary executor | absent |
| Permanent reproducibility gate | retained as `make release-reference-reproducibility` inside `make release-check` |
| Issue #18 | CLOSED — acceptance evidence recorded in the issue |

## Immutable candidate gate

Final Certification may close only after one immutable candidate SHA passes all of the following without modifying that candidate after CI begins:

1. Static contract;
2. complete Linux integration;
3. complete Linux release/certification contract (`make release-check`);
4. accepted literal-font/Unicode/embedding/PDF-A and distribution predicates remain intact;
5. deterministic release-reference-PDF gate remains green;
6. no temporary certification executor is present;
7. librarian item 33 remains explicitly fail-closed rather than being converted into speculative runtime behavior.

The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`. The actual candidate SHA is recorded only after the immutable Git commit exists.

## Exit rule

After the candidate passes the complete matrix, record its SHA and run IDs, mark Final Certification `CLOSED`, activate `Release`, and execute a final phase-transition documentation cycle. Any failure reopens work inside Final Certification and is classified before code or test changes.
