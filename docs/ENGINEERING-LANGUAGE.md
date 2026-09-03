# Engineering Language Policy

Updated: 2026-09-03

`abntexto-ufc` v3 uses English for every project-owned engineering surface.

This includes repository paths and filenames, the LaTeX project API and internal identifiers, source comments, technical diagnostics, scripts, tests, workflows, validator controls and technical UI, JSON/schema terminology, and active engineering documentation.

Portuguese remains valid when it is academic or authoritative content rather than project engineering nomenclature: rendered academic prose and headings, sample metadata values, bibliography data, official UFC/ABNT names or wording, literal Portuguese output under test, and identifiers owned by an upstream dependency at an explicit integration boundary.

An English engineering file may contain Portuguese academic content. For example, `template/frontmatter/acknowledgments.tex` may contain acknowledgments in Portuguese and `template/chapters/1-introduction.tex` may render `\section{Introdução}`.

Project-owned comments and diagnostics must be English. Rendered academic labels may be Portuguese when required by the document profile.

Historical engineering identifiers belong to Git history, tags, releases, issues, pull requests, and certified SHAs. The active v3 tree does not retain history directories, compatibility artifacts, duplicate old/new documentation, or dormant files solely for future convenience. Closed migration mappings may remain only when a permanent enforcement gate or the active reconstruction control plane consumes them; otherwise they are consolidated or removed.

Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. R2-B5 made `tests/checks/v3_api_residual.py` part of the permanent static contract, and R3-A proved that current enforcement is incomplete: path checks do not yet police all project-owned technical comments/diagnostics/UI, and some machine scenario/profile identifiers remain Portuguese. R3-B1 repaired behavior-affecting front-matter generator/observer defects needed for truthful evidence but deliberately did not absorb the broader language-policy cleanup. R3-B4/#255 still owns the scoped permanent language-enforcement repair. R3-B2/#253 closed at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` without broadening language policy; R3-B3/#254 is the current stage and owns engineering residual/test-integrity scope. The final invariants remain: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime or behavior-affecting engineering generators, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree. Rendered academic Portuguese, official wording, bibliography data, literal output under test, and genuine upstream identifiers remain protected content/boundaries.
