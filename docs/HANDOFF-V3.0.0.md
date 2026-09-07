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
| Step 5 implementation checkpoint | `6507da00275d8a69093541d6e6cb119a1b6f6cb3` |
| Step 5 orchestration correction | `02e1ea6e25c008c93f8ec3ba26af7f3cea03cf14`; Static `34129625390` PASS; auto Linux selected `article` as required |
| Step 5 latest Linux | `34129625475` FAIL, `SCOPE=article PASS=5 FAIL=1 SKIP=0` |
| Failure boundary | only `scientific-article-recommendations`; long rendered sentinel `ARTICLEADVISORYKEYTHREE` was not extracted contiguously for recommended + pdfLaTeX |
| Current work | **Step 5 — controlled keyword-sentinel robustness correction; no runtime/normative change** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Current failure classification

The orchestration correction is accepted as behavior: Static `34129625390` passed and Linux `34129625475` selected `article` for the incremental mixed orchestration + article change. Five of the six article gates then passed: validator source, profile, front block, optional foreign elements and body.

The recommendation contract checker also passed before the integration failure and preserved four `recommended` rules, one conditional journal rule and `proof_state_promoted=0`. The only failing predicate was exact extraction of the long synthetic third keyword sentinel from the recommended pdfLaTeX PDF.

This does **not** establish a runtime formatting defect. The bounded correction is to replace long synthetic keyword tokens with shorter extraction-safe sentinels and require all three recommended keywords plus the single outside-recommendation keyword to be present in generated PDF text. Runtime, rule IDs, modality, applicability and proof state remain unchanged.

## Step 5 acceptance gate before Step 6

| Gate | Required result |
|---|---|
| Static contract | PASS |
| Automatic Linux inference | `article` for the bounded Step 5 correction |
| Linux `article` | all six first-class checks PASS |
| Recommended scenario | pdfLaTeX + LuaLaTeX render summary marker and all 3 short controlled keyword markers |
| Outside-recommendation scenario | both engines render both paragraphs and the controlled single keyword marker |
| Recommendation semantics | remain non-enforcing |
| Journal precedence | remains `required-when-applicable`, `conditional-manual`, target-journal-bound |
| Steps 1–4 | remain green |
| Proof state / shared runtime | no unauthorized promotion/change |

## Immediate action

Publish the synchronized short-sentinel correction with this documentation, wait for Static and bounded Linux `article`, classify any failure before changing runtime/tests, and only after both gates pass record Step 5 as **ACCEPTED** and activate Step 6 in the same documentation cycle.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize phase closure by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Recommendations must not become hard compile/validation failures.
- Target-journal instructions remain conditional applicability, not generic UFC runtime law.
- A PDF text-extraction sentinel failure must be isolated from runtime semantics before any runtime change.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
