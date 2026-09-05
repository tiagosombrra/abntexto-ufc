# Engineering Language Policy

Updated: 2026-09-05

`abntexto-ufc` v3 uses English for every project-owned engineering surface.

This includes repository paths and filenames, the LaTeX project API and internal identifiers, source comments, technical diagnostics, scripts, tests, workflows, validator controls and technical UI, JSON/schema terminology, and active engineering documentation.

Portuguese remains valid when it is academic or authoritative content rather than project engineering nomenclature: rendered academic prose and headings, sample metadata values, bibliography data, official UFC/ABNT names or wording, literal Portuguese output under test, and identifiers owned by an upstream dependency at an explicit integration boundary.

An English engineering file may therefore contain Portuguese academic content. For example, template prose may render `Introdução`, bibliography fixtures may contain Portuguese titles, and tests may search for required academic labels such as `SUMÁRIO`. These are not engineering-language violations.

## Permanent enforcement

`tests/checks/engineering_language.py` is the permanent static enforcement surface for project-owned engineering language. It also protects the canonical English v3 profile/API identifiers and rejects retired Portuguese technical identifiers in active machine/runtime contracts.

A gate that reports zero violations while known project-owned Portuguese technical diagnostics remain is itself defective. The correct response is to strengthen the detector and translate the diagnostics, not to weaken the policy or classify project-owned technical messages as academic content.

## Current false-negative correction

The Core Corrections regression found mixed Portuguese/English project-owned diagnostics that the previous term matcher missed, including mixed phrases in `tests/integration/multivolume.sh` and `tests/integration/references-6023.sh`.

Implementation `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee` corrects this evidence gap by:

- adding a high-confidence mixed-language phrase matcher alongside the existing Portuguese technical-term matcher;
- expanding the detector self-test from 7 to 11 cases, including former false negatives;
- translating the known project-owned diagnostics in `multivolume.sh` to English;
- translating the known project-owned diagnostics in `references-6023.sh` to English;
- retaining explicit protection for academic/rendered Portuguese and official/literal content.

The correction remains acceptance-pending until a synchronized branch checkpoint passes Static contract and full Linux integration. If stronger detection reveals additional project-owned mixed diagnostics, those diagnostics must be corrected before the finding closes.

## Scope boundary

The enforcement must remain narrow enough not to reinterpret normal Portuguese academic content as engineering nomenclature. Broad stopword-style matching is not an acceptable substitute for project-owned diagnostic/context detection.

Allowed Portuguese includes:

- rendered academic prose and headings;
- bibliography and metadata data values;
- official UFC/ABNT/CAPES wording and names;
- literal Portuguese output intentionally exercised by a test;
- genuine upstream identifiers at a documented integration boundary.

Project-owned comments, diagnostics, CLI/UI messages, test failure messages, machine-state nomenclature and current technical documentation remain English.

## Canonical identifiers and phase authority

The canonical article profile identifier is `scientific-article`; `article.*` is the project-owned rule namespace. Historical Portuguese profile identifiers are not restored.

Current phase/status authority comes from `release/v3-roadmap.json`, `docs/HANDOFF-V3.0.0.md`, and `docs/ROADMAP-V3.0.0.md`. Historical opaque stage names may appear only as Git/issue/PR evidence and do not define current work.
