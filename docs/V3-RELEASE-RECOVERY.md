# V3 Release Recovery — 3.0.1

Updated: 2026-09-09
Status: ACTIVE — RECOVERY CANDIDATE PREPARATION

## Purpose

This document records the fail-closed recovery after a public GitHub `v3.0.0` tag and Release were found to exist before the repository's final exact-SHA release sequence had been completed.

The recovery does not reopen accepted v3 runtime, public API, normative, librarian-review, document-profile or typography decisions. It reopens only the Release publication boundary.

## Observed publication mismatch

The repository's final release contract requires:

```text
certified source SHA == visually approved source SHA == tagged SHA == source SHA of published release bytes
```

The public `v3.0.0` tag points to `05399473827da7cf6b6c8bac36edc7115481773f`, while the later exact-main state containing the final pkgcheck and seven-profile human-acceptance gates is `395899e1b2336ed268335d68e59e03452880c15e`.

A public GitHub Release named `abntexto-ufc 3.0.0` also exists for the earlier tag and has downloadable assets. Those bytes are therefore historical public artifacts and must not be silently replaced, retagged as if immutable, or submitted to CTAN as the final package.

No public CTAN acceptance/install evidence for `abntexto-ufc` was established when this recovery was opened.

## Recovery decision

The first publication candidate allowed to satisfy the current release contract is `3.0.1`.

The recovery intentionally changes only release/version/control surfaces:

- canonical version metadata;
- package/manual/README/CHANGELOG release metadata;
- release workflows and distribution tests where the version was hard-coded;
- machine roadmap, release-candidate marker and operational handoffs.

Project-owned runtime `.def` modules, accepted public API semantics, normative rules, layout rules and document-profile behavior are out of scope unless a fresh regression demonstrates an actual defect.

## Historical v3.0.0 disposition

`v3.0.0` is classified as **premature-publication / superseded-for-final-publication**.

Policy:

1. do not silently move the existing `v3.0.0` tag to another commit;
2. do not treat the existing GitHub Release assets as the canonical final CTAN bytes;
3. do not submit `abntexto-ufc-3.0.0.zip` to CTAN as the recovered final release;
4. preserve the historical state long enough to maintain auditability;
5. publish the recovered package under `v3.0.1` only after the complete current release sequence passes.

Any later decision to delete, edit or visibly mark the historical GitHub Release is an explicit publication-state action and must not be confused with source-tree recovery.

## Recovery acceptance sequence

1. merge the recovery control/version changes to canonical `main`;
2. resolve the resulting exact `main` SHA dynamically from Git;
3. require Static, complete Linux integration and Linux release check on that exact SHA;
4. require current CTAN `pkgcheck` against `abntexto-ufc-3.0.1.zip` and classify all output;
5. retain and physically audit the deterministic three-ZIP distribution plus `SHA256SUMS`;
6. regenerate PDF + corresponding `.tex` for all seven supported profiles from the exact candidate;
7. require A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight for every profile PDF;
8. obtain explicit maintainer visual approval for all seven pairs;
9. freeze exact publication hashes/evidence and prohibit rebuilds;
10. create immutable `v3.0.1` on the certified and visually approved SHA;
11. create the GitHub Release from the frozen assets and verify re-downloaded hashes;
12. submit exactly `abntexto-ufc-3.0.1.zip` to CTAN;
13. retain CTAN submission, acceptance and install evidence before Release closure.

## Scope impact

The version bump changes `abntexto-ufc.cls` identity metadata and archive bytes, so the final 3.0.1 candidate requires fresh exact-SHA release certification. Retained Windows/literal-font evidence remains scope-valid unless font runtime, engine behavior or the Windows certification contract changes.

Every material advance must update the affected control documents and machine state. Targeted checks do not replace the mandatory Release phase-end regression, and automated success does not replace explicit maintainer visual approval.
