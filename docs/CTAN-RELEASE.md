# GitHub / CTAN Release Guide — abntexto-ufc

Updated: 2026-09-17

This document defines the publication discipline for `abntexto-ufc`. GitHub/repository finalization and CTAN publication are separate operations: CTAN may be completed later without rebuilding or mutating certified GitHub release bytes.

## Current state

| Fact | State |
|---|---|
| GitHub published baseline | `v3.0.2` — immutable certified assets |
| v3.0.2 CTAN | exact certified archive submitted on 2026-09-17; external processing/closeout tracked in #313 |
| Active development line | `v3.0.3` |
| Active marker | `release/v3-release-candidate.json` |
| v3.0.3 candidate state | `NOT_FROZEN` |
| v3.0.3 candidate SHA | `null` |
| v3.0.3 publication authorization | `false` |
| v3.0.3 tracking | issue #328 |
| v3.0.3 implementation | PR #329 — merged |
| release-state reconciliation | PR #330 — merged |

The active release authority is `docs/V3.0.3-DISTRIBUTION-CORRECTION.md` plus the machine marker. Historical v3.0.2 release state is preserved under `release/history/v3/`.

## Immutable v3.0.2 receipt

Certified source:

```text
3a0904324e23bfc65852d730f2647ce47dc65105
```

Linux Release Check:

```text
34876949362
SCOPE=complete PASS=38 FAIL=0 SKIP=0
```

Certified publication SHA-256 values:

- CTAN: `f309ee3ddc8b748dbb1b1c81b542d3c0f24fc7a26a407887ad674d8f71c3c9dd`;
- Template: `e88d93d54099482564d2194c2e0d925640312d321897f8b553f623c451615552`;
- Overleaf: `5fb44b7600e5020784b0de1050ad1d3e5e2b529c43b3bcff6d4aa9082880a763`.

The annotated `v3.0.2` tag, GitHub Release assets and submitted CTAN ZIP must never be rebuilt, amended, replaced or retargeted. The user-bundle institutional-mark defect discovered after publication is corrected only by v3.0.3.

## Distribution contract from v3.0.3 onward

A release build produces:

- `abntexto-ufc-<version>.zip` — canonical CTAN archive;
- `abntexto-ufc-template-<version>.zip` — local editable project;
- `abntexto-ufc-overleaf-<version>.zip` — self-contained Overleaf project;
- `SHA256SUMS` — hashes for the three archives.

### CTAN surface

The CTAN archive must contain:

- one generated monolithic project-owned `abntexto-ufc.cls`;
- minimal documentation/example needed by the package;
- no project-owned modular `.def` files;
- no UFC institutional mark asset;
- no proprietary Microsoft font files;
- no repository engineering/control-plane infrastructure;
- an example configured with `coat-of-arms=false`.

### Template surface

The Template bundle must:

- include the editable TCC tutorial and runtime;
- include exactly `assets/institutional/ufc-coat-of-arms.png`;
- preserve `coat-of-arms=true` in the canonical tutorial;
- include `abntexto-ufc-reference.pdf` generated from that exact bundled source/asset;
- exclude proprietary Microsoft font files.

### Overleaf surface

The Overleaf bundle has the same institutional/reference requirements as Template and additionally vendors the pinned upstream `abntexto.cls` needed for reproducible/self-contained Overleaf use.

The distribution tests must rebuild Template/Overleaf source and prove reference-PDF identity. CTAN remains deliberately sanitized for institutional marks; Template/Overleaf are not.

## Candidate lifecycle

Normal development remains:

```text
candidate_state = NOT_FROZEN
candidate_sha = null
publication_authorized = false
```

A workflow-produced archive in this state is engineering evidence only.

Before freeze, one exact source SHA must pass:

1. Static Contract;
2. complete Linux Integration;
3. Linux Release Check;
4. current CTAN `pkgcheck` on its generated CTAN archive;
5. canonical-reference reproducibility;
6. PDF/A-2b, embedded-font, Unicode and repository-PDF validation;
7. distribution archive/rebuild checks;
8. seven supported-profile review preflights;
9. explicit maintainer visual acceptance of artifacts generated from that same SHA.

Release invariant:

```text
certified source SHA == visually approved source SHA == tagged source SHA == source SHA of published release bytes
```

## v3.0.3 GitHub finalization

The final repository-audit lot removes stale control-plane residue without changing runtime/template semantics and deliberately touches the active marker while preserving `NOT_FROZEN` so that complete release validation runs again.

After that lot is merged:

1. identify the exact resulting `main` SHA;
2. require the exact-main release workflows to pass;
3. retain the exact canonical PDF, seven review pairs, distribution ZIP and validation evidence;
4. inspect/compare those exact-source PDFs and obtain explicit maintainer visual acceptance;
5. freeze the already-certified source SHA by updating the marker to `FROZEN`, binding `candidate_sha` to that source and setting `publication_authorized=true`;
6. create annotated tag `v3.0.3` pointing to the certified source SHA;
7. create the GitHub Release using only the exact certified distribution artifact and its `SHA256SUMS`.

The freeze-control commit itself is not the publication source; the tag resolves to the earlier exact candidate SHA that generated the certified bytes.

## Deferred CTAN follow-up

CTAN publication is explicitly allowed to occur later. Do not hold GitHub repository cleanup or the GitHub Release open merely to wait for external CTAN timing.

When ready to submit v3.0.3 to CTAN:

1. use only the canonical `abntexto-ufc-3.0.3.zip` from the already-published/certified GitHub release artifact;
2. verify its SHA-256 against the release `SHA256SUMS`;
3. do not rebuild the archive locally;
4. submit that exact archive through CTAN;
5. record the CTAN receipt separately.

The pending v3.0.2 CTAN closeout remains issue #313. The v3.0.3 GitHub release remains issue #328. CTAN status must never be used as justification to change previously certified source or release bytes.

## Historical v3.0.1 procedure

The v3.0.1-specific procedure remains preserved at `docs/history/v3/release/CTAN-RELEASE-v3.0.1.md` as historical evidence only.
