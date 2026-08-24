# abntexto-ufc changelog

## 2.2.0 — 2026-08-24

- renamed the canonical package, class and runtime module identity to `abntexto-ufc`;
- retained `ufctex.cls` only as a deprecated project compatibility wrapper and excluded it from CTAN;
- removed the UFC institutional mark from CTAN and from generated public release archives, while preserving local `brasao-arquivo` support;
- reduced the CTAN archive to the installable runtime, essential documentation and a portable minimal example;
- strengthened deterministic archive, binary-asset, licensing and canonical-identity gates;
- migrated current CI, Windows font support and Gate T status contexts to the canonical identity;
- added typed normative evidence classification and a conservative rule-level proof-state baseline;
- preserved the distinction between source traceability, executable evidence and measured final-PDF proof;
- migrated the PDF validator workflow to the Node-24-compatible GitHub Actions stack;
- kept the v2.1.0 release immutable and historical references under their original identity.

This release does not treat the existence of a normative rule or regression test as automatic proof of final-PDF conformance. The project continues the explicit normative-verification roadmap separately from CTAN distribution certification.

## 2.1.0 — 2026-08-23

- based the UFC class on the `abntexto` 1.1+ base;
- added modular V2 configuration and current upstream/normative compatibility adapters;
- added current UFC/ABNT normative profiles and regression coverage;
- added Times New Roman and Arial policies for pdfLaTeX and LuaLaTeX;
- added PDF/A-2b, font embedding and Windows literal-font certification;
- added table, code, algorithm, bibliography, duplex and profile validation;
- fixed code and algorithm line numbers to remain inside the 3 cm text margin;
- aligned labels and descriptions in abbreviation/acronym and symbol lists, with geometric regression coverage;
- added an independent PDF validator with strict, portable and accessibility profiles;
- added deterministic GitHub, Overleaf and CTAN release bundles;
- consolidated the CTAN archive into a browsing-friendly layout without a redundant nested TDS ZIP;
- completed the unrestricted final Gate F audit of code, documentation, licenses, CI and release artifacts.

Validated through Gate T, deterministic distribution preflight, a real Overleaf import smoke test and the final normative/visual audit.
