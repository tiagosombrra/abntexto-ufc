# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-3 — Semantic / Path-Consumer Closure**.
- Active Block 3 work item: **B3-D — Operational v1/v2 identity and legacy-code purge**.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `094b369a077009f212adb33e8a814ee9bb167b4a`.
- R1-S2 trunk promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 control-plane closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

`main` remains the canonical trunk and merge target. Short-lived task branches are permitted by `AGENTS.md`, but canonical phase/stage authority remains in the control-plane files on `main`.

## R1-S0 — Repository sanitation

**DONE.**

- A verified mirror and full-history Git bundle were created before destructive ref cleanup.
- Legacy `1.x`, v2.x, N-phase/N15/B2R, audit, preview, maintenance, release, temporary, and abandoned v3 branches were removed from the active namespace after preservation.
- Pull requests #157 and #158 were closed as superseded by the v3 reconstruction.
- Immutable version tags remain protected and unchanged.
- The steady-state remote development namespace is `main` plus short-lived task branches only.

## R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

S1 removed the abandoned temporary migration workflow/executor, added root `AGENTS.md`, and synchronized machine state, handoff, and roadmap. The abandoned executor did not produce a certified Block 3 migration checkpoint.

## R1-S2 — Trunk rebaseline

**DONE.**

The v3 line was promoted to `main` without rewriting history.

Verified promotion facts:

- source checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`;
- former certified v2 `main`: `ce659b578b4fc9cc929af4aadc3e613df469ba77`;
- promotion mode: direct fast-forward;
- reference build passed on TeX Live 2026;
- agreed Python, shell, normative, validator-source, and diff-integrity gates passed;
- permanent CI remained intentionally absent;
- the stale `latex-preflight` status requirement remains deferred until R1-BLOCK-7.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** via PR #159, merged at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

- stale active project paths and consumers were reconciled;
- producer/consumer path references were normalized to the current repository layout;
- no later-block distribution/CI work was absorbed.

### B3-B — Normative process-identity closure

**DONE** via PR #160, squash-merged at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.

B3-B removed obsolete active process identity from validator/scenario/checker/fixture/evidence surfaces while preserving normative semantics.

Verified closure evidence:

- validator phase ownership removed;
- active scenario `phase` metadata/readers removed where obsolete;
- 172 phase-qualified markers migrated to functional namespaces;
- final functional namespaces include `IL` (illustration), `HL` (multiline hanging), `SI` (section indicator), and `SS` (subsection spacing);
- active N6/N9/N10 markers: 0;
- stale active phase diagnostics: 0;
- active lower-case N5–N15 process identities in B3-B scope: 0;
- active legacy `N*-EVIDENCE` labels: 0; `VALIDATION-EVIDENCE` is the shared active label;
- migrated producer/consumer mismatches: 0;
- namespace collisions: 0;
- normative rule IDs changed: 0;
- numeric expected values changed: 0;
- numeric tolerances changed: 0;
- proof state changed: false;
- runtime/API R2 changes: 0;
- B5/B6/B7/B8/control-plane/CI changes in B3-B: 0.

Functional differential validation for B3-B classified 29/29 relevant tests:

- 21 PASS;
- 8 BASELINE_EQUIVALENT_BLOCKED;
- 0 regressions introduced by B3-B;
- 0 unresolved classifications.

### B3-C — Runner/evidence integrity and bounded portability

**DONE.**

B3-C closed all eight defects exposed during B3-B differential validation without changing normative rule IDs, expected numeric values, numeric tolerances, proof state, or runtime/API semantics.

B3-C1 closed six producer/consumer and portability defects through replacement PR #168, squash-merged at `da775552be190bf09d8a790c33e9f7f4582da699`:

1. catalog card runner/file handoff;
2. long-quotation evidence producer/consumer path alignment;
3. research-project TeX job/Biber artifact naming;
4. short direct citation UTF-8 checker process;
5. vector-rule validation tolerance-key bindings;
6. table-IBGE same-run vector calibration production.

The original draft PR #164 was closed unmerged only because the connector could not transition its draft state; PR #168 used the exact same implementation branch/content.

B3-C2 closed the two remaining checker defects through PR #169, squash-merged at `625e82f9ef4780989d4635e500d72d09eab02992`:

7. appendix/annex obsolete undefined-`scope` process-progress accounting removed while preserving the exact 13-rule campaign;
8. footnote separator migrated from a bespoke stroked-line-only SVG parser to the shared vector-rule parser supporting stroked lines and filled thin rectangles, while retaining the same 50 mm length, left-margin origin, vertical relation, and validation-policy tolerances.

Issue #163 is closed as the operational B3-C continuity record. No temporary validation workflow remains in the repository.

### B3-D — Operational v1/v2 identity and legacy-code purge

**ACTIVE.** Operational continuity is tracked in issue #171.

Completed bounded lots:

- **B3-D1:** stale runner identity removed from catalog-card, research-project and font POC;
- **B3-D2A:** stale V2 diagnostic/gate labels removed from six internal runners; merged at `f4d703b34df53868f782598dd9502c0da684c345`;
- **B3-D2B:** stale v2-qualified temp/log identity removed from algorithm-numbering, object-geometry, minted, duplex-backmatter and multivolume; producer/consumer paths were changed together; merged at `094b369a077009f212adb33e8a814ee9bb167b4a`.

The live-tree audit distinguishes four legitimate retained legacy-reference classes: **certified history**, **migration contract**, **compatibility boundary**, and **negative test**. Everything else must be treated as active residue until proven otherwise.

New non-negotiable B3-D closure rule: **dead or superseded legacy implementation/test code is removed, not renamed or stored as an archive inside the active tree.** In particular, surviving `tests/v2-*` and other v1/v2-era helpers must be audited for a real current or assigned future consumer. A file that has no such consumer is deletion candidate; a file assigned to B5/R2 may remain only with an explicit classification.

B3-D closes only when:

- current file/directory, runner, temp, log and gate identity is free of v1/V1/v2/V2 qualification;
- no dead legacy implementation/test artifact remains merely for reference;
- every remaining textual legacy-version reference is explicitly classified;
- runtime/API compatibility work assigned to R2 has not been rewritten prematurely.

### Remaining Block 3 sequence

After B3-D:

- **B3-E:** close project-owned `oracle` engineering terminology where it is not a legitimate domain/testing term;
- **B3-F:** final live-tree residual audit and Block 3 closure.

Do not broaden Block 3 into permanent CI or distribution reconstruction. However, B3-D must audit whether legacy distribution/test helpers are actually live; dead code can be deleted now, while active distribution reconstruction remains B5.

## Non-negotiable rules

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, immutable tags, releases, issues, pull requests, certified SHAs, and verified external backups.

Every project-owned technical surface is English. Portuguese is limited to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, and current runtime/upstream identifiers at explicit boundaries. R1 must not rewrite the current Portuguese runtime API; that belongs to R2.

Permanent automatic CI remains absent during structural R1 reconstruction. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs remain candidate/certification work.

Do not rerun completed checks unless the current state or a relevant change justifies it.

## Previously closed R1 implementation blocks

- **Block 1 — canonical physical naming:** `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.
- **Block 2 — legacy purge and active-tree minimization:** `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

## Certified Block 3 checkpoints before the control rebaseline

1. `8d8f7081b123999618d4d6e5ec5009a18ce0a89b` — central normative loaders use `standards/`.
2. `4fd0e61ea198ed1307e511895b254c59f5ea0dc4` — negative-path and normative-complement consumers use current paths/checkers.
3. `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3` — canonical reference-document build restored on `template/`.
4. `1b6db7598d69a6a0d8442d09e589fa8d2e151477` — layout/font/PDF/locator gates reconnected.
5. `d4a348c6bb1600f0fc616c1ce23c1636db606097` — PDF validator/PDF-A gates target `template/main.pdf`.
6. `1cd88899bd25592944e37042419aa146e39c1de6` — front matter rebaselined end-to-end.
7. `66c1005f326ee6523e420165ddb9de595ef49d3d` — test-migration contract reconciled.
8. `bde108b7ff0076605643e870ae7cd86ce69a7e76` — standards consumers and generated-bytecode hygiene reconciled.
9. `91424aab55b08d0931654cd895db9ac7925ca15c` — validation ownership normalized to current runner IDs.
10. `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6` — prior one-shot workflow scaffolding removed; latest certified clean implementation checkpoint before S0/S1.
11. `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04` — B3-A path-consumer reconciliation merged through PR #159.
12. `dbc7f774df2cd0ac1b0f6479653290c6f19b6809` — B3-B normative process-identity closure merged through PR #160.
13. `da775552be190bf09d8a790c33e9f7f4582da699` — B3-C1 runner/evidence integrity repairs merged through PR #168.
14. `625e82f9ef4780989d4635e500d72d09eab02992` — B3-C2 final checker repairs merged through PR #169; B3-C closure checkpoint.
15. `f4d703b34df53868f782598dd9502c0da684c345` — B3-D2A stale diagnostic identity cleanup.
16. `094b369a077009f212adb33e8a814ee9bb167b4a` — B3-D2B stale temp/log identity cleanup; current certified implementation checkpoint.

## Immediate action

Continue **B3-D** from canonical remote `main` at `094b369a077009f212adb33e8a814ee9bb167b4a`. Finish the remaining operational v2/V2 runner cleanup, then audit surviving v1/v2-era test/distribution helpers for actual consumers. Delete dead/superseded artifacts, classify legitimate retained references, and only then advance to B3-E and B3-F.
