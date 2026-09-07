# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` at `789c6f3f4669ae36c3d4fe831ae939a340592568` |
| Shared-foundation integration checkpoint | `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active task branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Main reconciliation merge | `ae7e2cf2484e0b4329cc30ea80a95d0788e0e9f4` |
| Active phase | **Scientific Article** |
| Steps 1–5 | **ACCEPTED** |
| Step 5 acceptance checkpoint | `55fa1c8dc1b503c119d564950d04141cf45ad345` |
| Step 5 Static | `34132291198` PASS |
| Step 5 Linux | `34132291304` PASS, bounded `article` scope, all six first-class checks green |
| Step 6 activation checkpoint | `947f740f35c581ea101242b75181978f8f3a7f1b`; Static `34134609837` PASS |
| Current work | **Step 6 — evidence hardening and truthful article-specific proof-state mapping** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Repository reconciliation

`main` advanced from the shared-foundation integration checkpoint `e6833ed...` to `789c6f3...` with the accepted scoped Linux orchestration. PR #286 then became dirty against its updated base. The active article branch was reconciled by merge commit `ae7e2cf...`, with `789c6f3...` as the second parent.

The article branch already contained a stricter superset of the orchestration logic, including fail-closed fallback to the full PR range when an incremental synchronize endpoint is unavailable. The reconciliation therefore keeps the newer branch behavior while restoring current-main ancestry. This reconciliation is a control-plane advance only; it does not promote article proof state or accept Step 6.

## Step 5 acceptance

The Step 5 evidence-harness correction is accepted. Static `34132291198` and Linux `34132291304` passed. Recommended defaults remained advisory, outside-recommendation scenarios remained valid, journal precedence remained target-journal-bound and conditional-manual, and Step 5 did not promote normative proof state.

## Step 6 objective

Step 6 creates an explicit article-specific evidence map for the retained 18 rules. Evidence state may be promoted only when a rule has a direct article-specific executable observer or rejection predicate. Shared mechanisms, profile registration, or positive compilation alone are not proof.

| Rule family | Step 6 treatment |
|---|---|
| required front block / required textual structure / article body typography | direct article-specific executable evidence is required before executable proof ownership is declared |
| optional foreign elements | preserve optionality and map present/absent article scenarios |
| recommended author alignment / summary limits / keyword count / single paragraph | remain non-enforcing; positive evidence is advisory/default evidence |
| journal precedence | remains `required-when-applicable`, `conditional-manual`, `target-journal-submission` |

## Immediate action

1. validate the reconciled branch/control-plane checkpoint;
2. inventory all 18 article rules against current Step 1–5 executable evidence;
3. add a machine-readable article-specific evidence map and static contract checker;
4. promote only truthfully supported validation/evidence ownership and retain manual/conditional states elsewhere;
5. synchronize plan, roadmap, handoff, normative contract when applicable and machine state in the same material-advance cycle;
6. run Static and the Linux scope selected by the changed surfaces;
7. record Step 6 acceptance before activating Step 7 canonical article PDF work.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope, branch/base reconciliation and checkpoint facts remain synchronized with roadmap and machine state.

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
