# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; always resolve exact candidate SHA dynamically from Git |
| Active phase | **Release — final exact-main recertification / human approval** |
| Publication hardening | **MERGED** through PR #297 |
| Post-hardening control synchronization | **MERGED** through PR #298, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Final release gates | current CTAN `pkgcheck` + explicit seven-profile PDF/`.tex` maintainer approval |
| Prior Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **SUPERSEDED FOR PUBLICATION** |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN archive | one canonical upload file: `abntexto-ufc-3.0.0.zip` |
| CTAN runtime | **one generated `abntexto-ufc.cls`; zero project-owned `.def` files** |
| Exact-main Linux gate | release-marker push forces complete Linux scope |
| CTAN pkgcheck | executable pre-tag Linux release gate using current CTAN package at run time |
| Human acceptance | seven exact-candidate PDF/`.tex` pairs require explicit maintainer approval |
| Final tag rule | certified SHA = visually approved SHA = `v3.0.0` SHA = publication source SHA |

`docs/V3-CONTINUATION.md` is the shortest continuation entry point. Memory and hardcoded old SHAs are not Git authority.

## Accepted publication-hardening evidence

PR #297 closed the publication defects and CTAN-shape issues. Its protected merge produced `25c6ab09dc38be9257d2912652074a48886d28f9`. Exact-main release run `34355988612` subsequently demonstrated `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, NBR 6023 item 33 PASS, scientific-article PDF/A-2b PASS and deterministic distribution PASS.

The baseline canonical CTAN ZIP was physically audited as exactly eight files under one package root, one `abntexto-ufc.cls`, zero `.def`, no vendored `abntexto.cls`, no institutional marks and no proprietary Microsoft fonts. The generated class contained all 14 tracked runtime modules exactly once.

PR #298 then synchronized the post-hardening machine/control state and configured complete Linux integration on exact-main release-marker pushes. The final candidate definition additionally requires executable current-CTAN `pkgcheck` evidence and explicit maintainer review of all seven supported document profiles.

## Mandatory final seven-profile review

Before tag/freeze, present PDF and corresponding `.tex` source for:

1. undergraduate capstone;
2. specialization capstone;
3. master's thesis;
4. doctoral thesis;
5. research project;
6. anonymized research project;
7. scientific article.

All final pairs must come from the same exact candidate SHA and pinned release dependency set. Required preflight includes A4, PDF/A-2b, embedded fonts and no recognized warnings/overflows. The gate closes only after explicit maintainer approval.

A preliminary set from `25c6ab09...` already passed 7/7 automated preflight and page-by-page assistant inspection. It remains preliminary because later tracked release-control commits require regeneration on the final exact candidate.

## CTAN package contract

```text
abntexto-ufc/
├── README.md
├── CHANGELOG
├── LICENSE
├── abntexto-ufc.cls
├── abntexto-ufc.tex
├── abntexto-ufc.pdf
├── abntexto-ufc-example.tex
└── abntexto-ufc-example.pdf
```

Hard invariants: one project-owned runtime class; **zero `.def` files**; no nested project runtime directory; every tracked runtime module inlined exactly once; isolated example compile; no UFC marks, proprietary Microsoft fonts, vendored `abntexto.cls` or repository engineering infrastructure in CTAN.

Only `abntexto-ufc-3.0.0.zip` is submitted to CTAN. Template and Overleaf ZIPs are GitHub Release conveniences.

## pkgcheck evidence contract

The final Linux release run must preserve current `pkgcheck` version, complete output and checked ZIP SHA-256. A tool error blocks Release. Warnings require explicit review before freeze; they are not silently waived by a zero exit status.

## Remaining Release work

1. resolve the exact canonical `main` SHA containing the final release gates;
2. require Static, automatic complete Linux integration and Linux release check — including current CTAN `pkgcheck` — on that SHA;
3. retain and physically re-audit deterministic distribution bytes;
4. regenerate all seven exact-candidate PDF/`.tex` review pairs and obtain explicit maintainer approval;
5. freeze hashes/evidence;
6. create immutable `v3.0.0` on the same certified and visually approved SHA;
7. create GitHub Release and verify re-downloaded hashes;
8. submit only canonical ZIP to CTAN;
9. retain receipt/acceptance/install evidence;
10. synchronize final publication facts and close Release.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Windows/literal-font evidence

Retained Windows literal-font certification remains scope-valid because the final Release-control changes do not alter font runtime or engine behavior. Any font/engine/certification-relevant implementation change before freeze forces a fresh Windows run.

Every **material advance** updates affected documentation and machine state in the same work cycle. Targeted checks never replace the required **phase-end regression**. No build, tag or submission is treated as CTAN acceptance without explicit external evidence.