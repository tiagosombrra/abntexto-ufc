# Accessibility tagging experiment

## Status

The repository's tagged-PDF / PDF/UA work is **experimental only**.

Current certified implementation base before this closeout:

- `main`: `8ca076c05232a8fb127564c10f7c4022b1fc2112`;
- Phase 9A diagnostic baseline: #457 / PR #458;
- Phase 9B1 graphics diagnostic: #461 / PR #462;
- Phase 9B1 table-header diagnostic: #463 / PR #464;
- Phase 9B1 MathML diagnostic: #465 / PR #466;
- persistent section/class compatibility blocker: #459;
- Phase 9 adoption decision: #467.

This document records compatibility evidence and an adoption decision. It does **not** assert PDF/UA, WTPDF or PDF/A-4f conformance.

## What the experiments prove

The controlled LuaLaTeX experiments use the current LaTeX tagging interface only inside test fixtures. They do not change public templates or class defaults.

### Minimal structural baseline

The Phase 9A fixture proves:

- the generated PDF is reported as tagged;
- XMP declares PDF/UA-2;
- XMP declares PDF/A-4f;
- mapped `Document`, `P`, `L` and `LI` structure is present.

The expected `Sect` structure is absent. The repository preserves this as blocker #459 instead of treating the partial structure as conformance.

### Graphics semantics

The bounded graphics probe proves, without using memoir float/caption paths:

- one meaningful direct graphic is represented as a structural `Figure`;
- its explicit alternative text is present;
- a decorative direct graphic marked as an artifact does not create a second structural `Figure`.

### Table semantics

The bounded plain-`tabular` probe proves:

- one structural `Table`;
- three `TR` rows;
- two `TH` header cells;
- four `TD` data cells.

The probe deliberately excludes floats and captions.

### MathML semantics

The bounded LuaLaTeX math probe uses:

`tagging-setup={math/setup=mathml-SE}`

For one controlled displayed expression, the extracted structure proves:

- exactly one `Formula`;
- a MathML `math` root in the W3C MathML namespace;
- generated `mi`, `mo`, `mn` and `msup` elements.

## Known compatibility boundary

The upstream LaTeX Tagging Project continues to track `memoir` as a currently incompatible class in latex3/tagging-project#910. The issue documents unresolved or incomplete behavior including chapter/TOC structure, floats/captions and other memoir-specific interfaces.

Because `abntexto` is based on `memoir`, the repository does not infer class-level accessibility from the successful object-level probes.

Blocker #459 remains authoritative for:

- section/chapter and TOC structure;
- representative reading order;
- float/caption semantics;
- representative frontmatter and project-specific object coverage;
- any claim that `abntexto-ufc` is accessibility-ready.

## External conformance validation

As of 2026-10-06, veraPDF exposes machine-validation profiles for PDF/UA-2, WTPDF 1.0 and PDF/A-4f.

The repository already uses veraPDF for release-grade PDF/A-2b validation. The normal PR integration surface does not install or run veraPDF.

The Phase 9 decision is **not** to add PDF/UA-2/WTPDF as required gates yet.

Reason:

1. the current experimental fixtures are intentionally partial and are not a representative public-document corpus;
2. #459 already proves a class/base-class structural blocker;
3. a standards validator rejecting the current incomplete corpus would not establish a new adoption fact;
4. making such validation green by excluding known incompatible structure would create a misleading conformance signal;
5. adding a new external validator path before the representative corpus exists would increase CI and maintenance surface without enabling a valid accessibility claim.

External validation is therefore deferred, not waived.

## Adoption decision

The current decision is:

- do not enable tagging by default;
- do not expose a public accessibility opt-in mode yet;
- keep the tagged-PDF fixtures and integration probes as regression diagnostics;
- keep the public/release PDF/A-2b behavior unchanged;
- make no PDF/UA-2, WTPDF or PDF/A-4f conformance claim;
- keep #459 open as the re-entry blocker.

Successful isolated probes demonstrate useful compatibility surfaces. They are insufficient to support an accessibility product contract.

## Re-entry protocol

Accessibility work may re-enter material development when at least one of these occurs:

1. upstream `memoir` / `abntex2` tagging support changes materially;
2. the repository's toolchain changes such that the Phase 9A fail-closed baseline starts emitting the previously missing section structure;
3. a separately justified project decision funds and owns a local compatibility layer with a full regression plan.

At re-entry:

1. reconcile `main`, #459 and upstream tagging status;
2. rerun the Phase 9A minimal diagnostic before changing its contract;
3. build the previously blocked representative 9B2 corpus;
4. cover section/chapter hierarchy, TOC/reading order, floats/captions, frontmatter and representative project objects;
5. run external validation against the representative outputs using PDF/UA-2 and WTPDF 1.0 profiles, plus the intended PDF/A profile where applicable;
6. classify each failure by repository class, upstream `abntexto`/`memoir`, package or LaTeX tagging implementation;
7. only after that evidence decide whether an opt-in public mode is justified;
8. default activation requires a separate future-release decision and release-grade certification.

## Release boundary

Published v3.0.4 source, tag, GitHub Release assets and CTAN archive remain immutable.

Phase 9 does not select a new release line and does not change published accessibility claims.
