# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve the exact candidate SHA dynamically from Git after this control-plane synchronization is merged |
| Active phase | **Release** |
| Publication hardening | **MERGED** through PR #297 |
| Integration anchor | `25c6ab09dc38be9257d2912652074a48886d28f9` — merge result of PR #297; not the final taggable candidate because this control-plane synchronization follows it |
| Prior Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — technical evidence retained, **SUPERSEDED FOR PUBLICATION** |
| Prior artifact | `10086299397` — historical evidence only; never publish as v3.0.0 final |
| Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
| CTAN archive | one canonical upload file: `abntexto-ufc-3.0.0.zip` |
| CTAN runtime | **one generated `abntexto-ufc.cls`; zero project-owned `.def` files** |
| Repository runtime | modular source tree retained for engineering/testing |
| Final candidate | exact canonical `main` SHA that contains this post-merge control-plane synchronization and then passes final certification |
| Final tag rule | certified source SHA must equal `v3.0.0` target SHA |
| pkgcheck rule | current CTAN `pkgcheck` must pass before tag creation |

`docs/V3-CONTINUATION.md` is the shortest continuation entry point. Never use memory or a hardcoded “current main” SHA as Git authority.

## Completed publication-hardening evidence

PR #297 closed the publication defects and CTAN-shape issues. Its final head passed Static, Linux integration and Linux release check. The release check reported `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, closed former NBR 6023:2025 item 33, and produced a deterministic CTAN-grade archive with one generated class and zero project-owned `.def` files.

The retained PR artifact was manually audited before merge. The CTAN ZIP had exactly eight files below the package root, one `abntexto-ufc.cls`, zero `.def`, no vendored `abntexto.cls`, no institutional marks and no proprietary Microsoft fonts. The generated class contained all 14 tracked runtime modules exactly once and no residual project-owned `.def` input.

Those results certify the publication-hardening integration, not the final release bytes, because the protected repository uses squash merge and this control-plane synchronization intentionally follows the integration merge.

## CTAN package contract

The previous `ufctex` identity is replaced by `abntexto-ufc`. The CTAN-facing package is intentionally small and follows the single-class publication shape used by `abntexto-uece` where appropriate.

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

Hard invariants for the CTAN ZIP:

- exactly one project-owned runtime implementation file: `abntexto-ufc.cls`;
- **zero `.def` files**;
- no nested project runtime directory;
- every tracked runtime module is inlined exactly once;
- the minimal example compiles with only the generated class plus external `abntexto.cls` available;
- no UFC logos/marks, proprietary Microsoft fonts, vendored `abntexto.cls`, tests, workflows, validators, roadmaps or engineering evidence.

Only `abntexto-ufc-3.0.0.zip` is intended for CTAN. The editable-template and Overleaf ZIPs are GitHub Release conveniences and may preserve the modular source layout.

## Normative closure

Former librarian item 33 is **PASS** using primary ABNT NBR 6023:2025 authority and executable regression cases. The project verifies DOI plus applicable online availability/access elements, explicit repeated authorship, legal-person authorship, and jurisdiction disambiguation such as `SÃO PAULO (Estado)`.

## Remaining Release work

1. merge this control-plane synchronization through protected `main`;
2. resolve that exact resulting `main` SHA and treat it as the only final-candidate source;
3. run the final phase-end regression on that exact SHA, including Static and complete Linux/release checks;
4. build and retain the deterministic three-ZIP distribution plus `SHA256SUMS` from that exact SHA;
5. manually re-audit the canonical CTAN ZIP and confirm one generated `abntexto-ufc.cls`, zero `.def`, and isolated compile PASS;
6. run the current CTAN `pkgcheck` on that exact ZIP and preserve tool version, full output, checked hash and disposition of warnings;
7. freeze hashes and evidence; no rebuild after acceptance;
8. create immutable `v3.0.0` on the certified SHA;
9. create GitHub Release with the exact frozen bytes and verify re-downloaded hashes;
10. submit only `abntexto-ufc-3.0.0.zip` to CTAN and preserve receipt/acceptance evidence;
11. update post-publication documentation/state and close Release only after verification.

Invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

## Mandatory operating discipline

Every material repository modification must update the affected documentation and machine state in the same work cycle. The public README is changed only when its user-facing facts change; it must not carry transient branch or CI state. Targeted checks never replace the final phase-end regression. No publication state is inferred from a build, tag or submission without the corresponding evidence.
