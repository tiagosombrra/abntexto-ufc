from __future__ import annotations

import json
from pathlib import Path

BASE = "e40a56deeca8c22797398b0c95835964aefd2b15"
A1_ENTRY = "908ee2eb2ec04c030d74a9a4b146fba38fb745a9"
TODAY = "2026-09-04"
PROFILE = "scientific-article"


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one match in {path}, found {count}")
    target.write_text(text.replace(old, new), encoding="utf-8")


historical = Path("/tmp/coverage-rules-article-historical.json")
if not historical.is_file():
    raise SystemExit("historical article contract was not materialized")
contract = json.loads(historical.read_text(encoding="utf-8"))
if len(contract.get("rules", [])) != 13:
    raise SystemExit("historical article contract must contain exactly 13 discovery rules")
contract["reviewed_at"] = TODAY
contract["phase"] = "V3-A1"
contract["purpose"] = (
    "Current-source scientific-article normative contract for V3-A1. Historical rules are used only as discovery input; "
    "current UFC/ABNT sources were reconfirmed before promotion. No article runtime behavior is implemented in A1."
)
for rule in contract["rules"]:
    applicability = {
        "profiles": [PROFILE],
        "institutional_default": True,
        "specific_model_precedence": [
            "publisher-or-journal-author-guidelines",
            "formally-approved-course-specific-model",
        ],
    }
    rule["applicability"] = applicability
    rule["validation"] = {
        "mode": "manual",
        "checks": ["validator-source"],
    }

Path("standards/coverage-rules-article.json").write_text(
    json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

article_doc = f"""# V3-A1 Scientific-Article Normative Contract

Updated: {TODAY}

## Status

V3-A1/#275 is **ACTIVE**. This checkpoint reintroduces the scientific-article normative contract only. It does not add a LaTeX article profile, runtime branch, template example, validator assertion, distribution artifact, or compatibility alias.

Canonical profile identifier: `{PROFILE}`.

A1 exact entry recorded by the control plane: `{A1_ENTRY}`. A1 implementation work starts from activation checkpoint `{BASE}`.

## Current source decision

The current UFC normalization page, updated on 4 March 2026, still publishes the corrected scientific-article guide. The guide is the 2022 edition distributed in the corrected file dated 27 April 2023. It remains an institutional guide, not authority to select obsolete technical editions embedded in its bibliography.

Current article-specific and cross-cutting source set:

| Source | A1 decision | Role |
|---|---|---|
| UFC scientific-article guide, 2022 / corrected file 2023-04-27 | current institutional guide | article-specific presentation |
| UFC Resolution 17/CEPE, 2017 | current institutional normalization boundary | ABNT default or formally approved course-specific model |
| ABNT NBR 6022:2018 | current article-presentation technical standard | article structure/presentation |
| ABNT NBR 6028:2021 | current | abstracts |
| ABNT NBR 6024:2012 | current | progressive section numbering |
| ABNT NBR 10520:2023 | current | citations; supersedes the 2002 edition cited by the article guide |
| ABNT NBR 6023:2025 | current | references; supersedes the 2018 edition cited by the article guide |
| IBGE tabular rules, 3rd ed., 1993 | current delegated guidance where tabular presentation applies | numerical tables |

The guide itself instructs authors to consult journal-specific submission rules before submitting an article. The UFC institutional normalization resolution also permits formally approved course-specific models. Therefore the generic `{PROFILE}` contract is the institutional default, not an unconditional override of a more specific governing model.

## Promoted A1 rules

The 13 historical predicates were reviewed as discovery input and promoted only where the current source decision still supports them. Machine applicability uses `{PROFILE}`; no retired Portuguese profile identifier is restored.

| Rule | Normativity | A1 proof state | Main source |
|---|---|---|---|
| `article.structure.required` | required | MANUAL | NBR 6022 + UFC guide |
| `article.title.presentation` | required | MANUAL | UFC guide |
| `article.authorship.presentation` | required | MANUAL | UFC guide |
| `article.abstract.presentation` | required | MANUAL | UFC guide + NBR 6028 |
| `article.abstract.length.recommended` | recommendation | MANUAL | UFC guide |
| `article.dates.required` | required | MANUAL | UFC guide |
| `article.textual.required-sections` | required | MANUAL | UFC guide + NBR 6024/NBR 6022 |
| `article.textual.typography` | required | MANUAL | UFC guide |
| `article.references.required-placement` | required | MANUAL | UFC guide + current NBR 6023 |
| `article.page.margins` | required | MANUAL | UFC guide |
| `article.font.family.recommended` | recommendation | MANUAL | UFC guide |
| `article.pagination` | required | MANUAL | UFC guide |
| `article.sections.continuous` | required | MANUAL | UFC guide + NBR 6024 |

`manual` is intentional: source registration and `validator-source` traceability prove that the predicate is classified, not that a current article PDF satisfies it. A2 may promote individual rules only after article-specific positive/negative/rendered evidence exists.

## Rules deliberately not duplicated

Cross-cutting citation and reference semantics already belong to the current global NBR 10520:2023 and NBR 6023:2025 contracts. A1 does not fork them into article-only copies. The article manifest records only article-specific structure, placement and presentation predicates.

## Bounded V3-A2 implementation contract

A2 may implement only the behavior needed to satisfy the A1 article contract:

1. add the canonical `{PROFILE}` document-profile route without compatibility aliases;
2. add article-specific pre-textual composition for title, authorship, abstract/keywords and dates;
3. add article textual/post-textual layout overrides for one-sided continuous article flow, margins, typography, references placement and pagination;
4. add one canonical article template/example using the closed v3 API;
5. add article-specific positive, negative and rendered evidence, promoting proof state rule by rule rather than globally;
6. extend profile/distribution tests only where the article profile is actually public;
7. prove existing academic-work and research-project profiles are unchanged.

A2 must not reopen the removed v2 API, change current non-article normative predicates without explicit cross-cutting evidence, redistribute proprietary fonts, or perform CTAN submission.

## Exit criteria for A1

A1 closes only when the 13-rule manifest is accepted by the full normative loader, currency/precedence/locator/traceability/proof-state checks are green, `make static-check` is green, runtime/article implementation remains absent, and the canonical closeout records the exact A2 entry SHA.
"""
Path("docs/A1-ARTICLE-NORMATIVE-CONTRACT.md").write_text(article_doc, encoding="utf-8")

replace_once(
    "docs/NORMATIVE-BASE.md",
    "Updated: 2026-08-30",
    f"Updated: {TODAY}",
)
replace_once(
    "docs/NORMATIVE-BASE.md",
    "| Research projects | ABNT NBR 15287:2025 |\n| Abstracts/reviews | ABNT NBR 6028:2021 |",
    "| Research projects | ABNT NBR 15287:2025 |\n| Scientific articles | ABNT NBR 6022:2018, complemented by the current UFC article guide within its institutional scope |\n| Abstracts/reviews | ABNT NBR 6028:2021 |",
)
replace_once(
    "docs/NORMATIVE-BASE.md",
    "The active v3 foundation covers academic works and research projects. The scientific-article profile is not part of the active foundation tree during V3-R1 through V3-R5. Its previously researched normative evidence remains recoverable from Git history and is reintroduced only when V3-A1 starts.",
    "The certified v3 foundation covers academic works and research projects. V3-A1 has now reintroduced the source-backed normative contract for the canonical `scientific-article` profile, but no article runtime/profile implementation exists yet. The generic UFC article contract applies as the institutional default; publisher/journal author instructions and formally approved course-specific models remain explicit higher-specificity applicability boundaries. Runtime implementation belongs only to V3-A2 after A1 closes canonically.",
)

replace_once(
    "docs/NORMATIVE-CURRENCY.md",
    "Updated: 2026-08-30",
    f"Updated: {TODAY}",
)
replace_once(
    "docs/NORMATIVE-CURRENCY.md",
    "Scientific-article support is intentionally outside the active foundation scope until V3-A1. The previously researched article source contract is preserved by Git history rather than by dormant v3 files. When V3-A1 starts, article sources and predicates must be reconfirmed against then-current technical and UFC institutional sources before runtime implementation resumes.",
    "V3-A1 reconfirmed the scientific-article source set before restoring any active article rule manifest. The current UFC normalization page still publishes the corrected 2022 article guide (file corrected 2023-04-27). That guide remains institutionally current but cites obsolete NBR 10520:2002 and NBR 6023:2018 editions internally; those citations do not govern. Current cross-cutting editions remain NBR 10520:2023 and NBR 6023:2025, while NBR 6022:2018 remains the current article-presentation standard in the reviewed source set. The A1 article rules are manual/conservative until V3-A2 supplies article-specific implementation evidence.",
)

roadmap = load("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-A1" or roadmap.get("stage") != "V3-A1":
    raise SystemExit("unexpected active roadmap stage")
active = roadmap.get("active_implementation_lot", {})
if active.get("issue") != 275 or active.get("entry_main_sha") != A1_ENTRY:
    raise SystemExit("A1 active implementation lot does not match canonical entry")
roadmap["updated_at"] = TODAY
roadmap["a1_progress"] = {
    "status": "SOURCE_CONTRACT_VALIDATING",
    "issue": 275,
    "entry_main_sha": A1_ENTRY,
    "activation_main_sha": BASE,
    "profile_id": PROFILE,
    "source_reviewed_at": TODAY,
    "article_rule_count": 13,
    "validation_mode": "manual",
    "runtime_article_profile_present": False,
    "public_runtime_api_changed": False,
    "existing_foundation_runtime_changed": False,
    "normative_contract_changed": True,
    "proof_state_policy_changed": False,
    "current_source_set": [
        "ufc-guia-artigos-2022",
        "abnt-nbr-6022-2018",
        "abnt-nbr-6028-2021",
        "abnt-nbr-6024-2012",
        "abnt-nbr-10520-2023",
        "abnt-nbr-6023-2025",
        "ibge-tabular-1993",
    ],
    "a2_scope_document": "docs/A1-ARTICLE-NORMATIVE-CONTRACT.md",
}
save("release/v3-roadmap.json", roadmap)
