# CTAN / GitHub Release Guide — abntexto-ufc

Updated: 2026-09-17

This document preserves the frozen v3.0.2 publication receipt and defines the distribution discipline used by later corrective development. The v3.0.2 publication source is bound to one immutable candidate SHA and must not be rebuilt.

## Current state

| Fact | State |
|---|---|
| CTAN published baseline | `v3.0.1` — immutable historical release |
| GitHub published release | `v3.0.2` — immutable certified assets |
| Current release marker | `release/v3-release-candidate.json` still records the v3.0.2 frozen receipt pending CTAN publication reconciliation |
| v3.0.2 candidate state | `FROZEN` |
| v3.0.2 candidate SHA | `3a0904324e23bfc65852d730f2647ce47dc65105` |
| v3.0.2 publication authorization | true — exact certified bytes only |
| v3.0.2 tracking issue | #313 |
| v3.0.3 distribution correction | issue #328 / PR #329 |
| Historical v3/v3.0.1 release state | `release/history/v3/` |
| CTAN runtime shape | one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files |
| P7 visual entry gate | accepted on 2026-09-14 for `94a0538806561a89d9871ff88624dd7673a5f7e3` |
| Final v3.0.2 candidate visual gate | PASS on 2026-09-14 for `3a0904324e23bfc65852d730f2647ce47dc65105` |
| Tag | `v3.0.2` resolves exactly to `3a0904324e23bfc65852d730f2647ce47dc65105` |
| GitHub Release | PUBLISHED on 2026-09-15 |
| CTAN v3.0.2 | SUBMITTED on 2026-09-17; processing/acceptance pending |

The v3.0.1-specific publication procedure is retained at `docs/history/v3/release/CTAN-RELEASE-v3.0.1.md`.

## Release-candidate lifecycle

Normal development keeps the active marker in `NOT_FROZEN` state with no candidate SHA and no publication authorization. For v3.0.2, the marker remains frozen as a publication receipt until CTAN publication is reconciled:

- `candidate_state = FROZEN`;
- `candidate_sha = 3a0904324e23bfc65852d730f2647ce47dc65105`;
- `publication_authorized = true`.

Changing the active marker is a release-control event and forces complete Linux Integration plus the release-grade validation path. The freeze-control commit is not the publication source. The annotated `v3.0.2` tag resolves exactly to the frozen candidate SHA and must not be moved or recreated.

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

Do not rebuild, amend or substitute these archives after freeze. The v3.0.2 tag, GitHub Release assets and CTAN submission refer to the exact bytes above.

The Template/Overleaf omission of the institutional PNG in v3.0.2 was discovered only after publication. It is corrected in the v3.0.3 line rather than by replacing historical v3.0.2 assets.

## Distribution contract

A candidate release produces:

- one canonical CTAN-grade ZIP;
- one editable Template ZIP;
- one self-contained Overleaf ZIP;
- `SHA256SUMS` covering the public archives.

Only the canonical CTAN-grade archive is submitted to CTAN.

### CTAN archive

The CTAN archive must remain small and self-contained from the project's perspective:

- one generated project-owned runtime class;
- zero project-owned `.def` files;
- no institutional mark asset;
- no proprietary Microsoft font;
- no repository engineering/control-plane infrastructure;
- no complete pedagogical reference PDF unless a concrete CTAN requirement later justifies it;
- its minimal example uses `coat-of-arms=false`.

### Template and Overleaf bundles

From the v3.0.3 corrective line onward, both user-facing bundles must:

- include exactly `assets/institutional/ufc-coat-of-arms.png`;
- preserve the canonical tutorial setting `coat-of-arms=true`;
- include `abntexto-ufc-reference.pdf` generated from that exact bundled source and institutional PNG;
- remain reproducible and rebuild the embedded reference byte-identically under the release gate;
- exclude proprietary Microsoft font files.

The Overleaf bundle additionally vendors the pinned upstream `abntexto.cls`; the standard Template bundle keeps that dependency external.

This surface-specific distinction is deliberate: **CTAN is sanitized for institutional marks; Template and Overleaf are not**.

## Evidence discipline

Building a candidate is not publication. A green workflow is not maintainer visual acceptance. A GitHub Release is not CTAN acceptance.

Release claims must be backed by immutable GitHub run/artifact facts and, where applicable, explicit CTAN submission/acceptance evidence.

Historical v3/v3.0.1 machine state is preserved under `release/history/v3/` and must not be promoted back into active authority.

## Local publication handoff for v3.0.2 — historical operator receipt

The following commands document how the already-published v3.0.2 GitHub Release was created from the frozen artifact. They are retained as historical evidence and must not be rerun to replace assets.

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

The v3.0.2 GitHub Release was then created from the existing immutable tag with those exact files. The CTAN submission uses only `abntexto-ufc-3.0.2.zip`.

After CTAN confirms/publicly exposes v3.0.2:

1. record the CTAN acceptance/publication evidence in #313;
2. archive/reconcile the active v3.0.2 release marker/status;
3. close #313 after the final post-publication consistency check;
4. only then perform the explicit version/release-marker transition for the v3.0.3 corrective line.

Do not run `make distribution-bundles` to reconstruct v3.0.2 publication assets. The certified workflow artifact remains the immutable v3.0.2 publication source.
