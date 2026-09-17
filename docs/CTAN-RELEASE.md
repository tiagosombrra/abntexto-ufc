# CTAN / GitHub Release Guide — abntexto-ufc

Updated: 2026-09-17

This document defines the publication discipline for `abntexto-ufc`, preserves the immutable v3.0.2 publication receipt, and records the current v3.0.3 corrective line.

## Current state

| Fact | State |
|---|---|
| CTAN public baseline | `v3.0.1` |
| CTAN v3.0.2 | exact certified archive submitted on 2026-09-17; processing/acceptance pending |
| GitHub published release | `v3.0.2` — immutable certified assets |
| Active development line | `v3.0.3` |
| Active release marker | `release/v3-release-candidate.json` |
| v3.0.3 candidate state | `NOT_FROZEN` |
| v3.0.3 candidate SHA | `null` |
| v3.0.3 publication authorization | `false` |
| v3.0.3 tracking issue | #328 |
| v3.0.3 implementation PR | #329 — merged |
| v3.0.3 implementation baseline | `0de4501ed11beccfc2fefff371ecb8fb21e97d07` |
| Historical v3.0.2 marker | `release/history/v3/v3.0.2-release-candidate.json` |
| CTAN runtime shape | one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files |

The v3.0.1-specific publication procedure is retained at `docs/history/v3/release/CTAN-RELEASE-v3.0.1.md`.

The v3.0.2 tag, GitHub Release and CTAN submission are historical publication facts. The active release-control authority has already advanced to v3.0.3; v3.0.2 CTAN processing is not a development blocker, but it remains a publication-order gate for the later v3.0.3 CTAN update.

## Release-candidate lifecycle

Normal development keeps the active marker in `NOT_FROZEN` state with no candidate SHA and no publication authorization:

- `candidate_state = NOT_FROZEN`;
- `candidate_sha = null`;
- `publication_authorized = false`.

A versioned archive produced while the marker is `NOT_FROZEN` is engineering evidence only. It is not a publication artifact.

No candidate may be treated as frozen until all of the following are true on one immutable source SHA:

1. Static Contract passes;
2. complete applicable Linux Integration passes;
3. Linux Release Check passes;
4. current CTAN `pkgcheck` passes on the exact generated CTAN archive;
5. canonical reference and all supported profile artifacts are generated from that same SHA;
6. PDF/A, embedded-font, geometry, reproducibility and distribution checks pass;
7. the maintainer explicitly accepts the visual artifacts generated from that same SHA;
8. the release-control marker is advanced through the repository's governed freeze procedure without changing the publication source identity.

Invariant for every release:

```text
certified source SHA == visually approved source SHA == tagged source SHA == source SHA of published bytes
```

Published tags and release assets are immutable historical facts. They must never be silently retargeted, rebuilt or replaced to represent later source.

## Frozen v3.0.2 publication receipt

Certified publication source:

```text
3a0904324e23bfc65852d730f2647ce47dc65105
```

Linux Release Check run:

```text
34876949362
```

Certified archive checksums:

- CTAN: `f309ee3ddc8b748dbb1b1c81b542d3c0f24fc7a26a407887ad674d8f71c3c9dd`;
- Template: `e88d93d54099482564d2194c2e0d925640312d321897f8b553f623c451615552`;
- Overleaf: `5fb44b7600e5020784b0de1050ad1d3e5e2b529c43b3bcff6d4aa9082880a763`.

The GitHub Release was published on 2026-09-15. The exact certified CTAN archive was submitted on 2026-09-17 and remains under CTAN processing at the time of this update.

Do not rebuild, amend or substitute any v3.0.2 publication archive. The Template/Overleaf omission of the institutional PNG in v3.0.2 was discovered only after GitHub publication and is corrected by v3.0.3 rather than by rewriting historical v3.0.2 bytes.

## v3.0.3 corrective implementation evidence

PR #329 was squash-merged into `main` as:

```text
0de4501ed11beccfc2fefff371ecb8fb21e97d07
```

The exact post-merge SHA passed:

- Static Contract #598;
- Linux Integration #511;
- Linux Release Check #184, run `35253966868`;
- complete validation: `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- CTAN `pkgcheck 4.1.0`;
- canonical reference reproducibility with two byte-identical clean builds;
- embedded-font validation;
- repository PDF validation;
- PDF/A-2b validation;
- Unicode extraction validation;
- scientific-article PDF/A certification;
- distribution-bundle integrity and checksum verification;
- seven-profile automated release-review preflight.

Canonical reference evidence on that implementation baseline:

```text
SHA-256 c6dbcbc8cee6e77f8629b10b2178ced6acb2e296566c6016c362140692605877
```

The same run records:

```text
ctan_institutional_marks_redistributed=false
template_overleaf_coat_of_arms=true
proprietary_fonts_redistributed=false
```

The seven-profile review artifact is technically valid but still records `maintainer_approval=PENDING`.

This SHA is **not** frozen. Documentation reconciliation after PR #329 changes repository history, so the eventual v3.0.3 freeze must bind the exact final post-documentation SHA and its matching technical and visual evidence. The run above proves the merged implementation baseline; it does not authorize publication by itself.

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
- no UFC institutional mark asset;
- no proprietary Microsoft font;
- no repository engineering/control-plane infrastructure;
- no complete pedagogical reference PDF unless a concrete CTAN requirement later justifies it;
- its minimal example uses `coat-of-arms=false`.

### Template and Overleaf bundles

From v3.0.3 onward, both user-facing bundles must:

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

Historical machine state is preserved under `release/history/v3/` and must not be promoted back into active authority.

## Historical v3.0.2 local publication receipt

The following commands document how the already-published v3.0.2 GitHub Release material was recovered from the certified workflow. They are historical evidence and must not be rerun to replace assets.

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

The CTAN submission for v3.0.2 uses only `abntexto-ufc-3.0.2.zip`.

## Remaining ordered work

### v3.0.2 external closeout

When CTAN publicly exposes v3.0.2:

1. record acceptance/publication evidence and date in #313 and the historical v3.0.2 release receipt;
2. perform a final publication consistency check against the immutable submitted SHA-256;
3. close #313 once the historical receipt is complete.

No v3.0.2 artifact rebuild is part of this closeout.

### v3.0.3 release preparation

After the documentation reconciliation PR is merged:

1. identify the exact final `main` SHA;
2. run/confirm Static Contract and Linux Integration on that SHA;
3. run Linux Release Check on that exact SHA and retain its canonical PDF, seven review pairs and distribution artifacts;
4. verify `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, current CTAN `pkgcheck`, reproducibility and bundle-policy evidence;
5. perform explicit maintainer visual review of the canonical PDF and all seven profile pairs from that same SHA;
6. freeze exactly that candidate through the release-control procedure and authorize publication;
7. create annotated tag `v3.0.3` from the frozen candidate only;
8. publish the GitHub Release using only the exact certified distribution artifact and its `SHA256SUMS`;
9. submit the v3.0.3 CTAN archive only after CTAN has accepted/published v3.0.2;
10. record GitHub/CTAN receipts and close #328 only after publication closeout.

Do not reconstruct release assets locally after the candidate is frozen. The exact certified workflow artifact is the publication source.
