# V3.0.0 All-Profile Visual Validation

Updated: 2026-09-09
Status: ACTIVE — GENERATION/MAINTAINER REVIEW PENDING

## Purpose

This gate exists because Release closure requires a maintainer-visible review of the rendered result for every canonical document profile, not only automated compile/test success.

The review must use the immutable released implementation identified by tag `v3.0.0`, resolving to source SHA `05399473827da7cf6b6c8bac36edc7115481773f`. Post-tag documentation or validation infrastructure must not substitute a different class implementation.

CTAN submission is blocked until the maintainer explicitly accepts this gate.

## Canonical profiles

The class defines exactly these seven canonical document types:

| Profile | Intended review surface | Status |
|---|---|---|
| `undergraduate-capstone` | undergraduate capstone/TCC front matter, body and back matter | PENDING |
| `specialization-capstone` | specialization capstone front matter, body and back matter | PENDING |
| `masters-thesis` | master's dissertation/thesis profile front matter, body and back matter | PENDING |
| `doctoral-thesis` | doctoral thesis front matter, body and back matter | PENDING |
| `research-project` | identified research-project structure | PENDING |
| `anonymized-research-project` | anonymized research-project structure and author-hiding behavior | PENDING |
| `scientific-article` | article-specific front block, textual structure, notes/citations/references | PENDING |

## Required review bundle

For every profile the review bundle must contain:

1. the exact `.tex` source compiled for that profile;
2. the resulting final PDF;
3. compiler/build log or concise build metadata;
4. profile-specific SHA-256 values for source and PDF;
5. a top-level manifest naming the immutable `v3.0.0` source SHA and build environment.

Sources should be self-contained enough that a reviewer can identify which metadata and public commands produced the visible output. Shared bibliography/input material may be retained beside the source when required, but the manifest must make those dependencies explicit.

## Visual acceptance checklist

For each PDF inspect all pages, not only the first page. At minimum verify:

- correct profile identity and absence of elements belonging to another profile;
- cover/title/front-matter ordering where applicable;
- correct institution, program/course and degree/nature text;
- author/advisor/committee presentation and anonymization behavior where applicable;
- titles, subtitles, headings, spacing, margins and pagination;
- summaries/abstracts/keywords where applicable;
- tables, figures, lists, equations, code/algorithms when included by the profile source;
- citations, footnotes and reference formatting;
- appendices/annexes/back matter where applicable;
- no clipping, overlap, orphaned labels, broken glyphs, empty unintended pages or obviously incorrect page breaks;
- no UFC institutional mark asset unless intentionally supplied outside the distributed package; review examples should default to `coat-of-arms = false` unless the review is explicitly testing user-provided marks.

## Acceptance semantics

Automated compilation is necessary but insufficient. This gate becomes PASS only after the maintainer has been shown the seven source/PDF pairs and explicitly approves them.

If a material presentation or semantic defect is found:

1. do not modify, retarget or rebuild the immutable `v3.0.0` GitHub Release;
2. classify whether the defect is documentation/example-only or class/runtime behavior;
3. if runtime/publication bytes require correction, open a new candidate/version cycle before CTAN submission;
4. regenerate all affected profiles and repeat this gate.

## Evidence record

| Fact | Current state |
|---|---|
| Released source | `v3.0.0` → `05399473827da7cf6b6c8bac36edc7115481773f` |
| Profiles expected | 7 |
| Source/PDF pairs generated | PENDING |
| Automated compile | PENDING |
| Manifest/hashes | PENDING |
| Maintainer visual acceptance | PENDING |
| CTAN submission allowed | **NO — blocked until maintainer acceptance** |

Update this document whenever generation evidence, individual profile review results or final maintainer acceptance changes.
