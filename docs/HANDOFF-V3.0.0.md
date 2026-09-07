# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active task branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Active phase | **Scientific Article** |
| Steps 1–4 | **ACCEPTED** |
| Step 4 acceptance checkpoint | `005956bd615042a12fb0393fddd4941b635f6ce3` |
| Step 4 Static / Linux | `34119007413` PASS / `34119007425` PASS, `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| Step 5 fixture preflight | `f4453337d2de94260d7ebda4cead9803a6a9cb64`; Static `34124565217` PASS; Linux `34124565158` PASS, but only the five Step 1–4 article checks ran |
| Current work | **Step 5 — first-class recommendations/conditional gate implemented; synchronized CI pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 5 implementation state

| Surface | State |
|---|---|
| Recommendation contract checker | added; freezes four rules as `recommended` + `manual` |
| Journal precedence contract | checked as `required-when-applicable`, `conditional-manual`, `target-journal-submission` |
| Positive recommended fixture | present; controlled 150–250-word / one-paragraph / three-keyword scenario |
| Outside-recommendation fixture | added; short summary + two paragraphs + fewer than three keywords |
| Two-engine integration gate | added; outside-recommendation scenario must compile successfully |
| Linux suite registration | `scientific-article-recommendations` added as a first-class `article` check |
| Proof-state promotion | none |
| Runtime normative change | none |

The fixture-only checkpoint `f445333...` is not Step 5 acceptance because its Linux run had no dedicated Step 5 gate. The synchronized commit containing the checker, outside fixture, integration gate, suite registration and this documentation is the actual Step 5 candidate. Record its SHA and workflow runs only after CI finishes.

## Acceptance gate before Step 6

1. Static contract passes on the synchronized Step 5 candidate;
2. Linux `article` passes all six first-class checks;
3. both recommendation scenarios compile with pdfLaTeX and LuaLaTeX;
4. recommendation nonconformance alone produces no hard rejection;
5. journal precedence remains conditional/manual and context-bound;
6. Steps 1–4 remain green;
7. no proof-state, authority, shared non-article runtime or librarian-review classification changes.

## Immediate action

1. publish the synchronized Step 5 candidate;
2. wait for Static and Linux `article` on that exact SHA;
3. classify any failure before changing runtime/tests;
4. if both pass, record the SHA/run IDs and mark Step 5 ACCEPTED;
5. activate Step 6 evidence hardening in the same documentation cycle;
6. later close Scientific Article only after canonical article PDF visual review and complete phase-end regression.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize phase closure by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Recommendations must not become hard compile/validation failures.
- Target-journal instructions remain conditional applicability, not generic UFC runtime law.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
