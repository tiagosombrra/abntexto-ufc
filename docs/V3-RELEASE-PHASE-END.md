# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-09
Status: REOPENED — NEW FINAL PHASE-END REGRESSION REQUIRED

## Purpose

This document records the Release regression boundary after the publication audit discovered defects in the previously accepted distribution bytes.

## Previous candidate status

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` remains immutable historical evidence and previously passed:

| Gate | Historical result |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Linux integration | `34303586778` — SUCCESS, complete scope |
| Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Deterministic reference PDF | PASS; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65` |
| Retained artifact | ID `10086299397`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |

However, its distribution bytes are **SUPERSEDED FOR PUBLICATION**. The audit found stale v2/pre-publication README content and a CTAN README that labeled 3.0.0 a development candidate. Those files must not be published or submitted to CTAN.

This does not invalidate the earlier runtime/reference evidence; it invalidates that candidate as the final Release publication anchor.

## New Release phase-end contract

A new final candidate is required after publication hardening is merged to canonical `main`.

The final candidate must be one immutable SHA and satisfy:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

A pull-request head is not sufficient if the repository later squash-merges it. Final certification therefore runs on the exact post-merge canonical `main` SHA.

Minimum final evidence:

1. Static contract on exact candidate SHA;
2. complete Linux integration on exact candidate SHA;
3. `make release-check` on exact candidate SHA;
4. applicable Windows/literal-font/PDF-A recertification if affected by this batch;
5. deterministic build of exactly three ZIPs plus `SHA256SUMS`;
6. canonical CTAN-grade `abntexto-ufc-3.0.0.zip` structural/semantic gate PASS;
7. current CTAN `pkgcheck` PASS/reviewed-warning result against that exact ZIP;
8. frozen asset hashes and retained evidence before tag creation.

## Publication-hardening package boundary

The final public archives are:

- `abntexto-ufc-3.0.0.zip` — canonical package and the **only CTAN upload archive**;
- `abntexto-ufc-template-3.0.0.zip` — editable local template;
- `abntexto-ufc-overleaf-3.0.0.zip` — self-contained Overleaf convenience bundle;
- `SHA256SUMS` — GitHub Release integrity manifest.

The canonical package has one `abntexto-ufc/` root and includes only runtime, concise documentation, CHANGELOG, LICENSE and minimal example source/PDF. It excludes institutional marks, proprietary Microsoft fonts, vendored `abntexto.cls`, CI/tests/tools/validators/evidence and repository control-plane files.

## Normative state

The librarian review is now **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW**. Former item 33 has primary NBR 6023:2025 authority and executable regression evidence for DOI/online availability, repeated authorship and legal-person/jurisdiction cases.

## Current phase boundary

Release remains ACTIVE. No `v3.0.0` tag, GitHub Release or CTAN publication is authorized until the new final phase-end regression completes.

Required order:

1. integrate publication hardening;
2. certify exact post-merge `main` SHA;
3. run current `pkgcheck` on exact canonical package bytes;
4. freeze hashes/evidence;
5. create immutable tag;
6. publish GitHub Release and verify downloaded hashes;
7. submit one canonical ZIP to CTAN and retain external evidence;
8. synchronize final state and close Release.

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks never replace the final **phase-end regression**.
