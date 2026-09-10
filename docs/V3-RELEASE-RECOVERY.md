# V3 Release Recovery — 3.0.1

Updated: 2026-09-10
Status: ACTIVE — COMBINED RUNTIME-FIX + RECOVERY CANDIDATE PREPARATION

## Purpose

This document records the fail-closed recovery after a public GitHub `v3.0.0` tag and Release were found to exist before the repository's final exact-SHA release sequence had been completed.

The recovery originally reopened only the Release publication boundary. During recovery, PR #302 exposed and corrected a concrete runtime defect in the populated unified illustration list. That fix was independently reviewed, covered by a populated regression case, and squash-merged to canonical `main` as `6d06d4ed42b2187b1483ea219ee055cfe975ece2` before the final 3.0.1 candidate was frozen. Consequently, the final 3.0.1 candidate must certify the combined #302 runtime correction and the release-recovery/control changes as one exact source state.

Accepted v3 public API semantics, normative rules, librarian-review conclusions, document profiles and typography remain closed except where the #302 illustration-list defect directly required a runtime correction.

## Observed publication mismatch

The repository's final release contract requires:

```text
certified source SHA == visually approved source SHA == tagged SHA == source SHA of published release bytes
```

The public `v3.0.0` tag points to `05399473827da7cf6b6c8bac36edc7115481773f`, while the later exact-main state containing the final pkgcheck and seven-profile human-acceptance gates is `395899e1b2336ed268335d68e59e03452880c15e`.

A public GitHub Release named `abntexto-ufc 3.0.0` also exists for the earlier tag and has downloadable assets. Those bytes are therefore historical public artifacts and must not be silently replaced, retagged as if immutable, or submitted to CTAN as the final package.

No public CTAN acceptance/install evidence for `abntexto-ufc` was established when this recovery was opened.

## Post-v3.0.0 runtime correction included in 3.0.1

PR #302, `fix: render populated unified illustration lists safely`, corrected the project-owned `l@loii` renderer so populated unified illustration-list entries follow the two-argument `abntexto` list-entry contract. The regression fixture now writes and renders a real illustration-list entry and fails on warnings/overflows.

PR #302 was squash-merged to `main` as:

```text
6d06d4ed42b2187b1483ea219ee055cfe975ece2
```

The recovery branch was then reconciled with that exact `main` state using a merge commit with both histories as parents. Therefore, all subsequent 3.0.1 certification evidence must be generated from a candidate containing this runtime fix. Pre-#302 certification evidence is historical baseline evidence only.

## Recovery decision

The first publication candidate allowed to satisfy the current release contract is `3.0.1`.

The 3.0.1 scope now contains two deliberate classes of change:

- the scoped #302 runtime correction for populated unified illustration-list rendering and its regression fixture;
- canonical version metadata;
- package/manual/README/CHANGELOG release metadata;
- release workflows and distribution tests where the version was hard-coded;
- exact-candidate generation and retention of the seven PDF/TeX review pairs required by the existing human gate;
- machine roadmap, release-candidate marker and operational handoffs.

No other project-owned runtime module, public API semantic, normative rule, document-profile behavior or typographic rule is reopened unless the fresh combined regression demonstrates an actual defect.

## Historical v3.0.0 disposition

`v3.0.0` is classified as **premature-publication / superseded-for-final-publication**.

Policy:

1. do not silently move the existing `v3.0.0` tag to another commit;
2. do not treat the existing GitHub Release assets as the canonical final CTAN bytes;
3. do not submit `abntexto-ufc-3.0.0.zip` to CTAN as the recovered final release;
4. preserve the historical state long enough to maintain auditability;
5. publish the recovered package under `v3.0.1` only after the complete current release sequence passes.

Any later decision to delete, edit or visibly mark the historical GitHub Release is an explicit publication-state action and must not be confused with source-tree recovery.

## Exact-candidate human-review artifact

The Linux release workflow must retain the material needed for the mandatory human gate instead of leaving it only in temporary build paths.

`tests/integration/release-review-pairs.sh` generates the six non-article profile sources from the canonical profile fixture and uses `template/scientific-article.tex` for the article profile. It compiles the seven pairs with the pinned `abntexto` revision `4c03fd7b5a7af089627dedb547c53cad4eed2a2a`, injected through an isolated temporary `TEXINPUTS` path so the working tree is not modified.

Before retention, every PDF must pass A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight. The resulting CI artifact contains:

- seven `.tex` sources;
- seven corresponding PDFs;
- `SHA256SUMS` for all 14 pair files;
- `manifest.json` with source SHA, release version, pinned upstream commit, pair hashes and `maintainer_visual_approval = PENDING`.

The artifact name is derived from the canonical release version and workflow run. CI generation proves provenance and preflight only; it never records maintainer approval automatically.

## Recovery acceptance sequence

1. reconcile the recovery branch with canonical `main` containing PR #302;
2. require Static, **complete** Linux integration and Linux release check on the combined recovery head before merge;
3. merge the combined recovery to canonical `main` only after those PR gates pass;
4. resolve the resulting exact canonical `main` SHA dynamically from Git;
5. require Static, complete Linux integration and Linux release check again on that exact post-merge SHA;
6. require current CTAN `pkgcheck` against `abntexto-ufc-3.0.1.zip` and classify all output;
7. retain and physically audit the deterministic three-ZIP distribution plus `SHA256SUMS`;
8. require the same Linux release run to generate and retain the seven exact-candidate PDF/`.tex` review pairs plus hashes/manifest;
9. require A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight for every profile PDF;
10. obtain explicit maintainer visual approval for all seven pairs;
11. freeze exact publication hashes/evidence and prohibit rebuilds;
12. create immutable `v3.0.1` on the certified and visually approved SHA;
13. create the GitHub Release from the frozen assets and verify re-downloaded hashes;
14. submit exactly `abntexto-ufc-3.0.1.zip` to CTAN;
15. retain CTAN submission, acceptance and install evidence before Release closure.

## Scope impact

Both the #302 runtime correction and the 3.0.1 version/release changes affect publication bytes, so the final 3.0.1 candidate requires a fresh exact-SHA release certification. The existing pre-#302 and pre-recovery release runs remain useful only as historical baselines.

Retained Windows/literal-font evidence remains scope-valid because #302 does not alter font runtime, font setup, engine behavior or the Windows certification contract. Any later change to those surfaces forces fresh Windows recertification.

Every material advance must update the affected control documents and machine state. Targeted checks do not replace the mandatory Release phase-end regression, a green workflow whose heavy integration step was skipped does not satisfy the gate, and automated success does not replace explicit maintainer visual approval.
