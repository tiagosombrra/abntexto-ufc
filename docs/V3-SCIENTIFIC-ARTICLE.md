# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: CLOSED — PHASE-END REGRESSION ACCEPTED

## Accepted phase result

The Scientific Article phase is complete. The retained authority product remains exactly 18 source-backed article rules from `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.

| Step | Work | Final state | Evidence |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | completed two-engine profile gate |
| 2 | Required article front block | ACCEPTED | article-specific rendered evidence |
| 3 | Optional foreign title and summary | ACCEPTED | independent present/absent matrix |
| 4 | Textual structure and body typography | ACCEPTED | required structure/body gate |
| 5 | Recommendations and conditional applicability | ACCEPTED | recommendations remained non-enforcing; journal boundary conditional |
| 6 | Evidence hardening | ACCEPTED | `e941a7f9...`; exact 18-rule map; zero validation-mode promotions |
| 7 | Canonical article PDF | ACCEPTED | build `f62ac703...`; run `34153348385`; PDF SHA-256 `0152134e...`; 5/5 visual PASS; executor removed |
| 8 | Phase-end regression | **ACCEPTED** | candidate `923d11ef...`; Static `34154045481`; complete Linux `34154045509`; `PASS=36 FAIL=0 SKIP=0` |

## Phase-end candidate

`923d11ef668b02ec4de3cad4906ad5ac1f527eaf` is the accepted immutable Scientific Article candidate. Its Linux run selected `complete` scope and executed every article-specific executable gate plus the shared repository/profile matrix. The same checkpoint also proved the Step 7 cleanup state after removal of the temporary artifact workflow.

Full record: `docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md`.

## Canonical article PDF

Canonical source: `template/scientific-article.tex`.

| Artifact fact | Value |
|---|---|
| Build SHA | `f62ac703d8992af96b79cf83e125350ee561bd92` |
| Workflow | `34153348385` — SUCCESS |
| Artifact ID | `10030160290` |
| PDF SHA-256 | `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db` |
| Pages | 5 A4 |
| PDF version | 1.7 |
| Fonts embedded | PASS |
| Complete visual review | PASS — 5/5, unexplained FAIL 0 |

Primary-section new-page whitespace remains an **observation, not a defect**, because the retained article contract contains no no-page-break rule.

## Preserved boundaries

- One canonical `scientific-article` profile; no compatibility alias.
- Required, optional, recommended and conditional semantics remain distinct.
- Shared implementation reuse is not counted as proof by itself.
- Recommendations remain advisory/non-enforcing.
- Journal precedence remains conditional-manual.
- Librarian item 33 remains fail-closed.

## Handoff

Scientific Article is CLOSED and **Final Certification** is ACTIVE. Certification implementation starts only after PR #286 is merged and a fresh `cert/v3-final-certification` branch is created from updated main.

Every subsequent **material advance** updates the active certification documentation. Final Certification still requires its own complete **phase-end regression** on one immutable SHA.
