# Engineering Language Policy

Updated: 2026-08-30

`abntexto-ufc` v3 uses English for every project-owned engineering surface.

This includes repository paths and filenames, the LaTeX project API and internal identifiers, source comments, technical diagnostics, scripts, tests, workflows, validator controls and technical UI, JSON/schema terminology, and active engineering documentation.

Portuguese remains valid when it is academic or authoritative content rather than project engineering nomenclature: rendered academic prose and headings, sample metadata values, bibliography data, official UFC/ABNT names or wording, literal Portuguese output under test, and identifiers owned by an upstream dependency at an explicit integration boundary.

An English engineering file may contain Portuguese academic content. For example, `template/frontmatter/acknowledgments.tex` may contain acknowledgments in Portuguese and `template/chapters/1-introduction.tex` may render `\section{Introdução}`.

Project-owned comments and diagnostics must be English. Rendered academic labels may be Portuguese when required by the document profile.

Historical engineering identifiers belong to Git history, tags, releases, issues, pull requests, and certified SHAs. The active v3 tree does not retain history directories, compatibility artifacts, duplicate old/new documentation, or dormant files solely for future convenience. Closed migration mappings may remain only when a permanent enforcement gate or the active reconstruction control plane consumes them; otherwise they are consolidated or removed.

Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. R2-B5 made `tests/checks/v3_api_residual.py` part of the permanent static contract, closing removed project API/runtime residuals while allowing classified migration documentation and genuine upstream boundaries. The final invariants are: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree. R3-A now inventories any remaining engineering-language enforcement gaps before bounded hardening work is defined.
