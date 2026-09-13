# CTAN / GitHub Release Guide — abntexto-ufc

Updated: 2026-09-13

This document defines the current release discipline for post-v3.0.1 development. It is intentionally version-neutral until a new candidate is frozen.

## Current state

| Fact | State |
|---|---|
| Published baseline | `v3.0.1` — immutable historical release |
| Current development line | `v3.0.2` |
| Active release marker | `release/v3-release-candidate.json` |
| Candidate state | `NOT_FROZEN` |
| Candidate SHA | none |
| Publication authorization | false |
| Tracking issue | #313 |
| Historical v3/v3.0.1 release state | `release/history/v3/` |
| CTAN runtime shape | one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files |
| Human visual gate | required before any future tag/publication |

The v3.0.1-specific publication procedure is retained at `docs/history/v3/release/CTAN-RELEASE-v3.0.1.md`.

## Release-candidate lifecycle

Normal development keeps the active marker in `NOT_FROZEN` state with no candidate SHA and no publication authorization.

A future release-preparation lot must deliberately update the marker and the release contract together. Because the marker path is a GitHub Actions trigger, changing it forces complete Linux Integration and the release-grade validation path.

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
