# GitHub / CTAN Release Guide — abntexto-ufc

This document defines the reusable publication discipline for `abntexto-ufc`. Current publication facts belong in `docs/RELEASE-STATE.md`; completed release-specific evidence belongs under `docs/history/v3/` and `release/history/v3/`.

GitHub publication and CTAN submission are separate operations. CTAN may be completed later without rebuilding or mutating certified GitHub release bytes.

## Distribution contract

A release build produces:

- `abntexto-ufc-<version>.zip` — canonical CTAN archive;
- `abntexto-ufc-template-<version>.zip` — local editable project;
- `abntexto-ufc-overleaf-<version>.zip` — self-contained Overleaf project;
- `SHA256SUMS` — hashes for the three archives.

### CTAN surface

The CTAN archive must contain:

- one canonical project-owned `abntexto-ufc.cls` runtime;
- minimal documentation/example required by the package;
- no UFC institutional mark asset;
- no proprietary Microsoft font files;
- no repository engineering/control-plane infrastructure;
- an example configured with `coat-of-arms=false`.

The exact internal source architecture may evolve, but the CTAN surface must remain self-contained for the project-owned runtime and must not expose development-only modules unless a future reviewed packaging contract explicitly requires them.

### Template surface

The Template bundle must:

- include the editable TCC tutorial and supported project runtime;
- include exactly `assets/institutional/ufc-coat-of-arms.png`;
- preserve `coat-of-arms=true` in the canonical tutorial;
- include `abntexto-ufc-reference.pdf` generated from that exact bundled source/asset;
- exclude proprietary Microsoft font files.

### Overleaf surface

The Overleaf bundle has the same institutional/reference requirements as Template and additionally vendors the pinned upstream `abntexto.cls` needed for reproducible/self-contained Overleaf use.

Distribution tests must rebuild Template/Overleaf source and prove reference-PDF identity.

## Candidate lifecycle

Normal unreleased development begins without publication authority. Before freeze, one exact source SHA must pass:

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

## Freeze and GitHub publication

After one exact source SHA satisfies all technical and human gates:

1. record that already-certified source SHA as the frozen candidate;
2. authorize publication without changing the publication source;
3. merge any control-plane-only freeze receipt through the protected branch;
4. create an annotated version tag pointing to the certified source SHA, not a later control commit;
5. publish a GitHub Release using only the exact retained distribution artifacts from the certified workflow;
6. verify the published asset digests against the certified `SHA256SUMS`;
7. record a durable publication receipt;
8. move completed release-specific narrative/evidence out of active documentation.

Never rebuild artifacts merely to upload them to GitHub Releases.

## Deferred CTAN follow-up

When CTAN publication occurs after GitHub publication:

1. obtain the canonical `abntexto-ufc-<version>.zip` from the already-published GitHub Release;
2. verify its SHA-256 against the published `SHA256SUMS`;
3. do not rebuild the archive locally;
4. submit that exact archive through CTAN;
5. record the external submission/publication receipt without modifying the frozen GitHub release.

## Published releases

Published tags, GitHub Release assets and checksums are immutable project evidence. Any correction belongs to a later version.

For the current published version and exact hashes, read `docs/RELEASE-STATE.md`.
