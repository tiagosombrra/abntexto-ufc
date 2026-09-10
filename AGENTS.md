# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation. Repository state, not conversation memory, is authoritative.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata, or publication state:

1. resolve the actual branch and HEAD from Git and resolve `origin/main` dynamically;
2. read `docs/V3-CONTINUATION.md` first — it is the concise current operational handoff;
3. read `release/v3.0.1-final-corrections.json` — it is the machine-readable execution state for the active correction cycle;
4. read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md` — it defines R0–R6, acceptance criteria and non-goals;
5. when working in R1, also read `docs/V3.0.1-R1-TCC-SOURCE-AUDIT.md`, `docs/V3.0.1-R1.1-EVIDENCE.md`, `docs/V3.0.1-R1.2-TCC-COVERAGE-MATRIX.md`, `docs/V3.0.1-R1.2-EVIDENCE.md` and `docs/V3.0.1-R1.3-EVIDENCE.md`;
6. inspect issue #304 and draft PR #305 when remote GitHub state is available;
7. consult older v3 roadmap, phase-end, recovery and certification documents only as historical/background evidence when the current handoff or machine state points to them.

Priority on disagreement is: **current Git facts > active machine state > current continuation handoff > lot evidence > older roadmap/handoff/history documents > prior chat or memory**.

## Current release-correction state

| Fact | Current state |
|---|---|
| Target | `3.0.1` |
| Active phase | **Release** |
| Canonical branch | `main`; always resolve current SHA dynamically |
| Historical certified baseline | `111680cd934a4ea55b02f6ffe730ff5260077565`; retained as evidence, superseded as final candidate |
| Active correction branch | `release/v3.0.1-final-corrections` |
| Tracking issue | #304 |
| Draft PR | #305 |
| Publication | **BLOCKED** until R1–R6 close |
| R0 | DONE — auditable control plane |
| R1.1 | DONE — seven canonical chapter paths normalized and Static #475 PASS |
| R1.2 | DONE — pedagogical coverage inventory and historical-retention audit completed |
| R1.3 | IMPLEMENTED_PENDING_CHECKS — canonical TCC bounded rewrite committed for validation |
| R2 | PENDING — full canonical reference PDF |
| R3 | PENDING — distribution repair |
| R4 | PENDING — Web/Lite deploy + real-PDF E2E repair |
| R5 | PENDING — exact-SHA release regression |
| R6 | PENDING — maintainer acceptance and publication |
| Public `v3.0.0` | historical/superseded; never silently retarget |

The exact working-branch HEAD changes as audited lots are committed. Never copy a HEAD from this table as a current Git fact; resolve it from Git.

## Active release blockers

The correction cycle is intentionally bounded to user-facing release defects:

- canonical TCC/reference content must be coherent and pedagogically complete;
- the full canonical `template/main.tex` PDF must become a first-class certified release reference;
- public distribution must retain the full reference PDF/source in the appropriate bundle while the CTAN minimal example keeps its separate role;
- Web/Lite must have a complete static-deployment module graph and must run a real canonical PDF through its actual analysis path;
- final certification, human review, tag and publication must all bind to one exact source SHA and one frozen set of bytes.

Broad repository lifecycle cleanup, branch pruning and unrelated runtime/API refactoring remain deferred until after v3.0.1 unless a direct release blocker is proven.

## Audit discipline for every material lot

A material lot must leave, in the same work cycle:

- machine-state update;
- human-readable evidence/decision record;
- exact changed-file list or an unambiguous commit/PR diff that provides it;
- checks executed and their result/classification;
- unresolved findings carried forward explicitly;
- `docs/V3-CONTINUATION.md` synchronized whenever the next action or release status materially changes.

A failed check remains part of the audit trail after a successful rerun. Do not rewrite history to make the sequence look green.

## Canonical TCC/reference rules

The canonical undergraduate reference is rooted at `template/main.tex`. It is both a user-facing commented guide and a regression/reference corpus. The seven chapter files must remain sequential and semantically named.

The guide must distinguish:

- ABNT normative requirement;
- UFC institutional requirement;
- project/editorial policy;
- example or recommendation.

For each major user-visible formatting or document-structure topic, the final guide must explain the authority/classification, expected rendered behavior, the public `abntexto-ufc` mechanism and the test/validation evidence route. The full machine normative contract remains authoritative for atomic proof semantics; the pedagogical TCC is not a substitute for that machine contract.

Historical-retention evidence for R1.2 shows that the seven guide chapter bodies from commit `2cbd6d00318ba906e225fa37a4efb724300c3b4e` survived to the pre-R1.3 branch state as renames with zero additions/deletions. R1.3 is therefore constrained to preserve and extend that reviewed material rather than replace it wholesale.

R1.3 adds local documentation-only `\guiamecanismo` and `\guiavalidacao` callouts and closes the R1.2 guidance gaps. It must pass fresh Static and canonical-reference integration before R2 begins.

## Validator boundary

CLI/Deep and Web/Lite are distinct capability surfaces. Web/Lite must never claim Deep-only proof as PASS. The known pre-R4 defect is that `validator/app.js` imports `./normative-catalog.js` while that module is absent from the tracked static validator tree; existing synthetic cross-surface vectors do not prove the actual canonical PDF through the browser analysis path. R4 must close both issues before release.

## Release invariant

The previous exact-main certification is historical evidence only after R0 was opened. The final release candidate must be a new immutable exact SHA after R1–R4 are complete.

Required invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after human acceptance and before tagging/publication. Existing `v3.0.0` bytes remain untouched. CTAN receives only the canonical `abntexto-ufc-3.0.1.zip` frozen by R5.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Targeted CI never substitutes for R5 complete regression, and automated success never substitutes for R6 explicit maintainer visual approval.
