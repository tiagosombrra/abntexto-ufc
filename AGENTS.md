# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation. Repository state, not conversation memory, is authoritative.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata, or publication state:

1. resolve the actual branch and HEAD from Git and resolve `origin/main` dynamically;
2. read `docs/V3-CONTINUATION.md` first — it is the concise current operational handoff;
3. read `release/v3.0.1-final-corrections.json` — it is the machine-readable execution state for the active correction cycle;
4. read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md` — it defines R0–R6, acceptance criteria and non-goals;
5. read the evidence document for the active lot: R1 evidence is under `docs/V3.0.1-R1*.md`; R2 uses `docs/V3.0.1-R2-EVIDENCE.md`; later lots must add and reference their own evidence document before closure;
6. inspect issue #304 and PR #305 when remote GitHub state is available;
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
| PR | #305 — ready-for-review only to execute CI; not merge-ready |
| Publication | **BLOCKED** until R1–R6 close |
| R0 | DONE — auditable control plane |
| R1.1 | DONE — seven canonical chapter paths normalized and Static #475 PASS |
| R1.2 | DONE — pedagogical coverage inventory and historical-retention audit completed |
| R1.3 | DONE — bounded TCC rewrite; Static #484 + Linux #405 `PASS=3 FAIL=0 SKIP=0` on `704cedaa...` |
| R2 | IMPLEMENTED_PENDING_EVIDENCE — canonical PDF/provenance artifact wiring under CI validation |
| R3 | PENDING — distribution repair |
| R4 | PENDING — Web/Lite deploy + real-PDF E2E repair |
| R5 | PENDING — exact-SHA release regression |
| R6 | PENDING — maintainer acceptance and publication |
| Public `v3.0.0` | historical/superseded; never silently retarget |

The exact working-branch HEAD changes as audited lots are committed. Never copy a HEAD from this table as a current Git fact; resolve it from Git.

## Active release blockers

The correction cycle is intentionally bounded to user-facing release defects:

- R2 must prove that the full canonical `template/main.tex` PDF is a first-class exact-SHA release reference;
- public distribution must retain the full reference PDF/source in the appropriate bundle while the CTAN minimal example keeps its separate role;
- Web/Lite must have a complete static-deployment module graph and must run a real canonical PDF through its actual analysis path;
- final certification, human review, tag and publication must all bind to one exact source SHA and one frozen set of bytes.

The canonical TCC/reference content blocker itself is closed by R1.3. Broad repository lifecycle cleanup, branch pruning and unrelated runtime/API refactoring remain deferred until after v3.0.1 unless a direct release blocker is proven.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification/release result, active-lot acceptance state, artifact provenance, reproducibility state, candidate transport, tag/release state or publication readiness. Every material advance must update the affected machine state, lot evidence and `docs/V3-CONTINUATION.md` in the same work cycle.

A material lot must leave an exact changed-file record or unambiguous commit/PR diff, executed checks with classification, and unresolved findings carried forward explicitly. A failed check remains part of the audit trail after a successful rerun; do not rewrite history to make the sequence look green.

## Mandatory phase-end regression

Targeted checks are development evidence only. The final candidate must undergo the **phase-end regression** defined by the repository release contract before the Release phase can close. The phase-end regression binds the complete applicable matrix to one immutable exact SHA; targeted CI or a draft/scoped Linux success never substitutes for it.

## Canonical TCC/reference rules

The canonical undergraduate reference is rooted at `template/main.tex`. It is both a user-facing commented guide and a regression/reference corpus. The seven chapter files must remain sequential and semantically named.

The guide must distinguish ABNT normative requirements, UFC institutional requirements, project/editorial policy, and examples/recommendations. For each major user-visible formatting or document-structure topic, the final guide must explain the authority/classification, expected rendered behavior, the public `abntexto-ufc` mechanism and the test/validation evidence route. The full machine normative contract remains authoritative for atomic proof semantics; the pedagogical TCC is not a substitute for that machine contract.

Historical-retention evidence for R1.2 shows that the seven guide chapter bodies from commit `2cbd6d00318ba906e225fa37a4efb724300c3b4e` survived to the pre-R1.3 branch state as renames with zero additions/deletions. R1.3 preserved and extended that reviewed material rather than replacing it wholesale.

R1.3 closed on source SHA `704cedaa9960b87ae6035ac08fa4cc4c286ea9aa` with Static #484 PASS and Linux #405 `reference-document` PASS (`reference`, `reference-corpus`, `pdf-validator`; no failures or skips). Earlier failed runs remain evidence in `docs/V3.0.1-R1.3-EVIDENCE.md`.

## Canonical reference artifact rule

R2 reuses the existing deterministic release-reference build rather than create a competing generator. `make release-check` invokes `tests/integration/release-reference-reproducibility.sh`, which produces `artifacts/validation/release-reference-pdf.pdf` and `artifacts/validation/release-reference-reproducibility.json` from two independent clean builds.

The Linux Release Check must fail closed unless that evidence reports `PASS`, identifies the current `SOURCE_COMMIT_SHA`, identifies `template/main.tex` as the canonical source, records two byte-identical clean builds, matches the actual retained PDF SHA-256, and records PASS for font embedding, portable CLI/Deep PDF validation, PDF/A-2b and Unicode extraction. On success, the workflow publishes the PDF and provenance JSON together as a dedicated `canonical-reference` artifact. The generic validation artifact may coexist but is not the first-class identity surface.

A release-workflow-only change is CI orchestration and selects the PR `smoke` integration scope because the same change directly triggers Linux Release Check, which is the authoritative heavy R2 path. This exception must never override release-candidate markers: candidate markers still force `complete`.

R2 remains open until the implementation SHA has fresh Static, scoped Linux and Linux Release Check evidence, the dedicated artifact is verified, and the full PDF receives page-by-page development visual inspection. That visual inspection is engineering evidence only and does not substitute for R6 maintainer acceptance.

## Validator boundary

CLI/Deep and Web/Lite are distinct capability surfaces. Web/Lite must never claim Deep-only proof as PASS. The known pre-R4 defect is that `validator/app.js` imports `./normative-catalog.js` while that module is absent from the tracked static validator tree; existing synthetic cross-surface vectors do not prove the actual canonical PDF through the browser analysis path. R4 must close both issues before release.

## Release invariant

The previous exact-main certification is historical evidence only after R0 was opened. The final release candidate must be a new immutable exact SHA after R1–R4 are complete.

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after human acceptance and before tagging/publication. Existing `v3.0.0` bytes remain untouched. CTAN receives only the canonical `abntexto-ufc-3.0.1.zip` frozen by R5.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Automated success never substitutes for R6 explicit maintainer visual approval.
