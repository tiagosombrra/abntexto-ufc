# Scientific Article — Phase-end Regression

Updated: 2026-09-07  
Status: ACCEPTED

## Accepted immutable candidate

| Evidence | Result |
|---|---|
| Candidate SHA | `923d11ef668b02ec4de3cad4906ad5ac1f527eaf` |
| Static contract | `34154045481` — SUCCESS |
| Linux integration | `34154045509` — SUCCESS |
| Linux scope | `complete` |
| Linux summary | `PASS=36 FAIL=0 SKIP=0` |
| Canonical article artifact source | `f62ac703d8992af96b79cf83e125350ee561bd92` |
| Artifact workflow | `34153348385` — SUCCESS |
| PDF SHA-256 | `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db` |
| Visual review | PASS — 5/5 pages, 0 unexplained failures |
| Temporary artifact executor | absent from candidate |

## Why this candidate closes both Step 7 and Step 8

Step 7 required the synchronized cleanup checkpoint to pass Static and its selected Linux scope after removal of the temporary PDF-build executor. Both passed on `923d11ef...`.

Step 8 required one immutable SHA to pass Static, **complete** Linux integration, all article-specific executable gates and the accepted canonical article-PDF evidence. The Linux orchestration selected `complete` for `923d11ef...` and executed 36 checks. The article profile, required front block, optional foreign elements, textual structure/body typography, recommendations/conditional-applicability gate, shared profile matrix and all repository-wide checks passed.

The already provenance-bound canonical article PDF remained the accepted Step 7 presentation artifact and had been completely inspected at 200 DPI before candidate publication. No synthetic or stale PDF is used as evidence.

## Article authority boundary

The retained contract remains exactly 18 source-backed rules. No recommendation was promoted to a hard failure, journal precedence remains conditional, and shared mechanisms are not treated as article-specific proof by themselves.

The visible new-page behavior for primary article sections remains a non-blocking observation because the retained authority defines no no-page-break predicate.

Librarian item 33 remains `NORMATIVE-REVIEW` and fail-closed pending authoritative current NBR 6023:2025 evidence.

## Phase decision

**Scientific Article is CLOSED. Final Certification may become ACTIVE.**

The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`; the concrete accepted SHA is recorded here and in evidence fields, not substituted into that sentinel.

## Operating discipline

This acceptance is a **material advance** and therefore requires synchronized handoff, roadmap and machine-state documentation. Every subsequent phase still requires its own complete **phase-end regression** on one immutable candidate.
