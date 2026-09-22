# Engineering Language Policy

Updated: 2026-09-19

`abntexto-ufc` uses English for project-owned engineering surfaces: repository paths and filenames, the LaTeX project API and internal identifiers, source comments, technical diagnostics, scripts, tests, workflows, validator controls/UI, JSON/schema terminology and active engineering documentation.

Portuguese remains appropriate when it is academic or authoritative content rather than project engineering nomenclature: rendered academic prose/headings, sample metadata values, bibliography data, official UFC/ABNT/CAPES names or wording, literal Portuguese output under test and identifiers genuinely owned by an upstream dependency at an explicit integration boundary.

## Permanent enforcement

`tests/checks/repository/engineering_language.py` is the permanent static enforcement surface.

It protects canonical project-owned technical identifiers and rejects retired/noncanonical project engineering terminology in active machine/runtime contracts.

A gate that reports zero violations while known project-owned Portuguese technical diagnostics remain is defective. The correct response is to strengthen the detector and correct the diagnostics, not to weaken the policy.

## Scope boundary

Allowed Portuguese includes:

- rendered academic prose and headings;
- bibliography and metadata values;
- official institutional/normative names and wording;
- literal Portuguese output intentionally exercised by a test;
- genuine dependency-owned identifiers at a documented integration boundary.

Project-owned comments, diagnostics, CLI/UI messages, test failure messages, machine-state nomenclature and active technical documentation remain English.

Broad stopword matching is not a substitute for diagnostic/context-aware enforcement.

## Canonical identifiers and authority

The canonical scientific-article profile identifier is `scientific-article`; `article.*` is the project-owned article rule namespace.

Current repository/status authority comes from:

- current Git/GitHub facts;
- `release/v3-release-candidate.json`;
- `docs/RELEASE-STATE.md`;
- current durable technical documentation.

Historical control/lifecycle documents may preserve earlier terminology as audit evidence under controlled history, but they do not define current engineering language.

## Ongoing guard

The policy is permanent. Any material change that introduces noncanonical project-owned engineering terminology must be corrected before acceptance.

Academic/rendered Portuguese content must not be anglicized merely to satisfy an engineering-language check.
