# Engineering Language Policy

Updated: 2026-09-05

`abntexto-ufc` v3 uses English for every project-owned engineering surface: repository paths and filenames, the LaTeX project API and internal identifiers, source comments, technical diagnostics, scripts, tests, workflows, validator controls/UI, JSON/schema terminology, and active engineering documentation.

Portuguese remains valid when it is academic or authoritative content rather than project engineering nomenclature: rendered academic prose and headings, sample metadata values, bibliography data, official UFC/ABNT/CAPES names or wording, literal Portuguese output under test, and identifiers owned by an upstream dependency at an explicit integration boundary.

## Permanent enforcement

`tests/checks/engineering_language.py` is the permanent static enforcement surface. It also protects canonical English v3 profile/API identifiers and rejects retired Portuguese technical identifiers in active machine/runtime contracts.

A gate that reports zero violations while known project-owned Portuguese technical diagnostics remain is itself defective. The correct response is to strengthen the detector and translate the diagnostics, not weaken the policy or reclassify project-owned technical messages as academic content.

## Core Corrections hardening

Initial hardening implementation `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee` added high-confidence mixed-language phrase detection, expanded the self-test from 7 to 11 cases, and translated known mixed diagnostics in `multivolume.sh` and `references-6023.sh`.

Synchronized checkpoint `fd3727d89848eb52a9c79021cd9765ad9e1806db` correctly failed Static run `33970711005`: the stronger detector exposed another project-owned Portuguese diagnostic in `tests/integration/algorithm-numbering.sh` (`número de linha duplicado`). This is a successful fail-closed discovery, not a reason to weaken the detector.

Correction implementation `5c5b9593cd12f3b6fa3108b579514c3c25edcb54` now:

- translates all project-owned diagnostic messages in `algorithm-numbering.sh` to English;
- extends high-confidence detection for the newly exposed line-numbering phrases;
- expands the detector self-test to 13 cases;
- retains the earlier translations in `multivolume.sh` and `references-6023.sh`;
- preserves Portuguese academic/rendered strings and bibliography data.

The hardening finding remains open until a synchronized checkpoint containing `5c5b9593...` passes Static contract and full Linux integration. Any further diagnostic exposed by the stronger detector must be corrected rather than hidden.

## Scope boundary

Allowed Portuguese includes rendered academic prose/headings, bibliography and metadata data values, official wording/names, literal Portuguese output intentionally exercised by a test, and genuine upstream identifiers at a documented integration boundary.

Project-owned comments, diagnostics, CLI/UI messages, test failure messages, machine-state nomenclature and current technical documentation remain English. Broad stopword-style matching is not an acceptable substitute for diagnostic/context-aware detection.

## Canonical identifiers and phase authority

The canonical article profile identifier is `scientific-article`; `article.*` is the project-owned rule namespace. Historical Portuguese profile identifiers are not restored.

Current phase/status authority comes from `release/v3-roadmap.json`, `docs/HANDOFF-V3.0.0.md`, and `docs/ROADMAP-V3.0.0.md`. Historical opaque stage names may appear only as Git/issue/PR evidence and do not define current work.
