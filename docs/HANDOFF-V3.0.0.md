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
| Steps 1–5 | **ACCEPTED** |
| Step 5 acceptance checkpoint | `55fa1c8dc1b503c119d564950d04141cf45ad345` |
| Step 5 Static | `34132291198` PASS |
| Step 5 Linux | `34132291304` PASS, bounded `article` scope, all six first-class checks green |
| Step 5 recommendation evidence | pdfLaTeX + LuaLaTeX; recommended + outside-recommendation scenarios; 3/3 controlled recommended keyword markers; outside keyword marker; recommendation hard failures `0`; journal precedence `conditional-manual`; `proof_state_promoted=0` |
| Current work | **Step 6 — evidence hardening and truthful article-specific proof-state mapping** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 5 acceptance

The Step 5 evidence-harness correction is accepted. The shortened synthetic keyword sentinels removed the extraction brittleness without changing article runtime, rule IDs, locators, normativity, applicability or proof state. Static `34132291198` passed, and Linux `34132291304` selected the bounded `article` scope and passed validator source, article profile, front block, optional foreign elements, body, and recommendations.

The recommendation gate proved both engines and both controlled scenarios. Recommended defaults remained advisory, short and multi-paragraph summaries remained compilable, fewer than three keywords remained compilable, journal precedence remained target-journal-bound and conditional-manual, and Step 5 did not promote normative proof state.

## Step 6 objective

Step 6 creates an explicit article-specific evidence map for the retained 18 rules. Evidence state may be promoted only when a rule has a direct article-specific executable observer or rejection predicate. Shared mechanisms, mere profile registration, or positive compilation alone are not proof.

The evidence classification must preserve these boundaries:

| Rule family | Step 6 treatment |
|---|---|
| required front block / required textual structure / article body typography | may be promoted only when mapped to direct article-specific executable evidence |
| optional foreign elements | record article-specific positive/absence evidence without converting optionality into a requirement |
| recommended author alignment / summary limits / keyword count / single paragraph | remain non-enforcing; positive evidence is advisory/default evidence, not a hard validator predicate |
| journal precedence | remains `required-when-applicable`, `conditional-manual`, `target-journal-submission` |

## Immediate action

1. inventory all 18 article rules against current Step 1–5 executable evidence;
2. add a machine-readable article-specific evidence map and a static contract checker;
3. promote only truthfully supported proof states and retain manual/conditional states elsewhere;
4. synchronize plan, roadmap, handoff and machine state in the same material-advance cycle;
5. run Static and the required Linux scope dictated by the changed surfaces;
6. record Step 6 acceptance before activating Step 7 canonical article PDF work.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize phase closure by themselves. Scientific Article Step 8 requires `complete` Linux.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Recommendations must not become hard compile/validation failures.
- Target-journal instructions remain conditional applicability, not generic UFC runtime law.
- Shared implementation is not article proof.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
