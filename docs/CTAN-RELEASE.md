# CTAN / GitHub Release Guide — abntexto-ufc

Updated: 2026-09-14

This document defines the current release discipline for the frozen v3.0.2 candidate and later post-v3.0.1 development. The v3.0.2 publication source is already bound to one immutable candidate SHA.

## Current state

| Fact | State |
|---|---|
| Published baseline | `v3.0.1` — immutable historical release |
| Current development line | `v3.0.2` |
| Active release marker | `release/v3-release-candidate.json` |
| Candidate state | `FROZEN` |
| Candidate SHA | `3a0904324e23bfc65852d730f2647ce47dc65105` |
| Publication authorization | true — exact certified bytes only |
| Preparation state | P8 frozen / ready to publish; annotated tag `v3.0.2` already exists and resolves exactly to the frozen candidate SHA |
| Tracking issue | #313 |
| Historical v3/v3.0.1 release state | `release/history/v3/` |
| CTAN runtime shape | one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files |
| P7 visual entry gate | accepted on 2026-09-14 for `94a0538806561a89d9871ff88624dd7673a5f7e3` |
| Final candidate visual gate | PASS on 2026-09-14 for `3a0904324e23bfc65852d730f2647ce47dc65105` |
| Tag | `v3.0.2` exists and resolves to `3a0904324e23bfc65852d730f2647ce47dc65105` |
| GitHub Release | PENDING |
| CTAN publication | PENDING |

The v3.0.1-specific publication procedure is retained at `docs/history/v3/release/CTAN-RELEASE-v3.0.1.md`.

## Release-candidate lifecycle

Normal development keeps the active marker in `NOT_FROZEN` state with no candidate SHA and no publication authorization. For v3.0.2, that transition is complete: the marker is `FROZEN`, publication is authorized for the exact certified bytes, and the frozen candidate SHA is `3a0904324e23bfc65852d730f2647ce47dc65105`.

Changing the marker is a release-control event and forces complete Linux Integration plus the release-grade validation path. The freeze-control commit is not the publication source. The annotated `v3.0.2` tag has now been created and resolves exactly to the frozen candidate SHA; it must not be moved or recreated.

No candidate may be treated as frozen until all of the following are true on one immutable source SHA:

1. Static Contract passes;
2. complete applicable Linux Integration passes;
3. Linux Release Check passes;
4. current CTAN `pkgcheck` passes on the exact generated archive;
5. canonical reference and supported profile artifacts are generated from that same SHA;
6. PDF/A, embedded-font, geometry and distribution checks pass;
7. the maintainer explicitly accepts the visual artifacts.

Invariant for any future release:

```text
certified source SHA == visually approved source SHA == tagged source SHA == source SHA of published bytes
```

Published tags and release assets are immutable historical facts. They must never be silently retargeted or rebuilt to represent later source.

## Frozen v3.0.2 publication receipt

Certified publication source: `3a0904324e23bfc65852d730f2647ce47dc65105`.

Linux Release Check run: `34876949362`.

Certified archive checksums:

- CTAN: `f309ee3ddc8b748dbb1b1c81b542d3c0f24fc7a26a407887ad674d8f71c3c9dd`;
- Template: `e88d93d54099482564d2194c2e0d925640312d321897f8b553f623c451615552`;
- Overleaf: `5fb44b7600e5020784b0de1050ad1d3e5e2b529c43b3bcff6d4aa9082880a763`.

Do not rebuild, amend or substitute these archives after freeze. The tag, GitHub Release assets and CTAN submission must refer to the source/bytes above.

## Distribution contract

A candidate release continues to produce:

- one canonical CTAN-grade ZIP;
- one editable template ZIP;
- one self-contained Overleaf ZIP;
- `SHA256SUMS` covering the public archives.

Only the canonical CTAN-grade archive is submitted to CTAN.

The CTAN archive must remain small and self-contained from the project's perspective:

- one generated project-owned runtime class;
- zero project-owned `.def` files;
- no institutional mark asset;
- no proprietary Microsoft font;
- no repository engineering/control-plane infrastructure;
- no complete pedagogical reference PDF unless a concrete CTAN requirement later justifies it.

Template and Overleaf bundles may contain the sanitized complete pedagogical reference PDF, subject to the existing reproducibility and distribution gates.

## Evidence discipline

Building a candidate is not publication. A green workflow is not maintainer visual acceptance. A GitHub Release is not CTAN acceptance.

Release claims must be backed by immutable GitHub run/artifact facts and, where applicable, explicit CTAN submission/acceptance evidence.

Historical v3/v3.0.1 machine state is preserved under `release/history/v3/` and must not be promoted back into active authority.


## Local publication handoff for v3.0.2

Publication after freeze is intentionally an operator-local action. Do not rebuild the archives.

From a clean Git checkout with GitHub CLI authenticated:

```bash
set -euo pipefail

repo="tiagosombrra/abntexto-ufc"
candidate="3a0904324e23bfc65852d730f2647ce47dc65105"
run_id="34876949362"
artifact="abntexto-ufc-v3.0.2-distribution-34876949362"
out=".release/v3.0.2"

git fetch --tags origin

test "$(git rev-parse 'v3.0.2^{}')" = "$candidate"
git show v3.0.2 --no-patch --format=fuller

rm -rf "$out"
mkdir -p "$out"

gh run download "$run_id" \
  --repo "$repo" \
  --name "$artifact" \
  --dir "$out"

cd "$out"
sha256sum -c SHA256SUMS

printf '%s  %s\n' \
  f309ee3ddc8b748dbb1b1c81b542d3c0f24fc7a26a407887ad674d8f71c3c9dd \
  abntexto-ufc-3.0.2.zip | sha256sum -c -

printf '%s  %s\n' \
  e88d93d54099482564d2194c2e0d925640312d321897f8b553f623c451615552 \
  abntexto-ufc-template-3.0.2.zip | sha256sum -c -

printf '%s  %s\n' \
  5fb44b7600e5020784b0de1050ad1d3e5e2b529c43b3bcff6d4aa9082880a763 \
  abntexto-ufc-overleaf-3.0.2.zip | sha256sum -c -
```

Only after all four checksum validations pass, create the GitHub Release from the existing tag and attach the certified public files:

```bash
cd "$(git rev-parse --show-toplevel)"

cat > .release/v3.0.2/release-notes.md <<'EOF'
# abntexto-ufc v3.0.2

Corrective and usability-focused v3 release certified from source commit:

`3a0904324e23bfc65852d730f2647ce47dc65105`

## What changed

- Restores the UFC institutional coat of arms on research-project cover profiles while preserving the explicit opt-out.
- Replaces the oversized canonical manual-style TCC with a compact five-chapter, 22-page tutorial.
- Separates tutorial, user guide, exhaustive command reference, normative traceability and regression responsibilities.
- Makes Template/Overleaf bundles self-contained with the user-facing documentation.
- Removes the unused external reference-photo download path.
- Strengthens Linux Integration so every PR event is scoped from the full PR diff, preventing a documentation-only tail commit from hiding technical changes.

## Final certification

- Frozen/tagged source: `3a0904324e23bfc65852d730f2647ce47dc65105`.
- Linux Release Check run: `34876949362`.
- Complete validation: `PASS=38 FAIL=0 SKIP=0`.
- Canonical tutorial: 22 pages, inside the 15–35 page budget.
- Canonical reproducibility, PDF/A-2b, embedded fonts, repository PDF validation and Unicode: PASS.
- Scientific article PDF/A: PASS.
- Distribution bundles: PASS.
- CTAN `pkgcheck 4.1.0`: PASS.
- Seven review pairs: preflight PASS and maintainer visual acceptance PASS.

## Distribution assets

These are the exact frozen files from the certified Linux Release Check. Do not rebuild them for this release.

- `abntexto-ufc-3.0.2.zip` — canonical CTAN submission archive.
- `abntexto-ufc-template-3.0.2.zip` — local/template bundle.
- `abntexto-ufc-overleaf-3.0.2.zip` — Overleaf-oriented bundle.
- `SHA256SUMS` — certified checksums.
EOF

gh release create v3.0.2 \
  .release/v3.0.2/abntexto-ufc-3.0.2.zip \
  .release/v3.0.2/abntexto-ufc-template-3.0.2.zip \
  .release/v3.0.2/abntexto-ufc-overleaf-3.0.2.zip \
  .release/v3.0.2/SHA256SUMS \
  --repo "$repo" \
  --title "abntexto-ufc v3.0.2" \
  --notes-file .release/v3.0.2/release-notes.md
```

After GitHub Release creation:

1. verify the Release asset checksums against the certified values;
2. submit only `abntexto-ufc-3.0.2.zip` to CTAN;
3. wait for CTAN acceptance/publication;
4. only after both GitHub Release and CTAN publication are confirmed, archive the active release marker/status as historical publication evidence.

Do not run `make distribution-bundles` for publication after freeze. The certified workflow artifact is the publication source.
