# Engineering Language Policy

Updated: 2026-09-05

`abntexto-ufc` v3 uses English for every project-owned engineering surface: repository paths and filenames, the LaTeX project API and internal identifiers, source comments, technical diagnostics, scripts, tests, workflows, validator controls/UI, JSON/schema terminology, and active engineering documentation.

Portuguese remains valid when it is academic or authoritative content rather than project engineering nomenclature: rendered academic prose and headings, sample metadata values, bibliography data, official UFC/ABNT/CAPES names or wording, literal Portuguese output under test, and identifiers owned by an upstream dependency at an explicit integration boundary.

## Permanent enforcement

`tests/checks/engineering_language.py` is the permanent static enforcement surface. It protects canonical English v3 profile/API identifiers, rejects retired Portuguese technical identifiers in active machine/runtime contracts, and audits project-owned technical diagnostics.

A gate that reports zero violations while known project-owned Portuguese technical diagnostics remain is itself defective. The correct response is to strengthen the detector and translate the diagnostics, not weaken the policy or reclassify project-owned technical messages as academic content.

## Core Corrections hardening

The current hardening cycle deliberately uses stronger detection to discover old evidence debt.

- Initial hardening translated known mixed diagnostics in `multivolume.sh` and `references-6023.sh` and strengthened the mixed-language matcher.
- Static `33970711005` exposed `algorithm-numbering.sh`; its complete diagnostic surface was translated.
- Static `33970988780` exposed temporary documentation-governance drift; this was corrected without weakening the language gate.
- Static `33971156481` then exposed catalog-card/duplex/vector diagnostic surfaces; implementation `1129935fe5e4f97d6fe3798fd5e4777760f0d61b` translated those surfaces and expanded detector self-tests to 18 cases.
- Static `33971849196` on synchronized checkpoint `0818bc2c5f50f6f1c60d4cef98d1c85031cb2fcd` passed repository and phase-governance checks, then exposed five remaining technical diagnostics in `tests/integration/backmatter.sh`.
- Current implementation `a1c139a6efa8bacefcd3294f01b1f7ed3447a8dd` translates the complete `backmatter.sh` engineering diagnostic surface and changes its technical job identifier from Portuguese to English while preserving rendered Portuguese literals used as evidence.

The finding remains open until a synchronized checkpoint on top of `a1c139...` passes Static contract and full Linux integration. Any further diagnostic exposed by the stronger detector must be corrected rather than hidden.

## Detection design rule

Detection must remain contextual and high-confidence. Broad stopword-style matching is not acceptable because it can confuse legitimate academic Portuguese with project-owned technical language.

When a newly added phrase rule exposes one line, inspect the complete related test/gate surface. The policy is to remove the whole project-owned diagnostic debt in that surface, not patch only the first reported token.

## Scope boundary

Allowed Portuguese includes rendered academic prose/headings, bibliography and metadata data values, official wording/names, literal Portuguese output intentionally exercised by a test, and genuine upstream identifiers at a documented integration boundary.

Project-owned comments, diagnostics, CLI/UI messages, test failure messages, machine-state nomenclature and current technical documentation remain English.

## Canonical identifiers and phase authority

The canonical article profile identifier is `scientific-article`; `article.*` is the project-owned rule namespace. Historical Portuguese profile identifiers are not restored.

Current phase/status authority comes from `release/v3-roadmap.json`, `docs/HANDOFF-V3.0.0.md`, and `docs/ROADMAP-V3.0.0.md`. Historical opaque stage names may appear only as Git/issue/PR evidence and do not define current work.
