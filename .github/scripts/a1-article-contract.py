from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "e40a56deeca8c22797398b0c95835964aefd2b15"
A1_ENTRY = "908ee2eb2ec04c030d74a9a4b146fba38fb745a9"
FOUNDATION = "c79f3c73f1d51a30175e8259269504d029442a1c"
TODAY = "2026-09-04"
ARTICLE_EVIDENCE = "article.source-review"


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one occurrence, found {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def insert_before_once(path: str, marker: str, block: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if block.strip() in text:
        return
    if text.count(marker) != 1:
        raise SystemExit(f"{path}: insertion marker count is {text.count(marker)} for {marker!r}")
    p.write_text(text.replace(marker, block.rstrip() + "\n\n" + marker), encoding="utf-8")


def append_section_once(path: str, heading: str, body: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if heading in text:
        return
    p.write_text(text.rstrip() + f"\n\n{heading}\n\n{body.rstrip()}\n", encoding="utf-8")


def set_source_checked(data: dict, source_ids: set[str]) -> None:
    by_id = {source["id"]: source for source in data["sources"]}
    missing = sorted(source_ids - set(by_id))
    if missing:
        raise SystemExit(f"missing source records: {missing}")
    for source_id in source_ids:
        by_id[source_id]["checked_at"] = TODAY


article_sources = {
    "ufc-normalizacao-2026",
    "ufc-guia-artigos-2022",
    "abnt-nbr-6022-2018",
    "abnt-nbr-10520-2023",
    "abnt-nbr-6023-2025",
    "abnt-nbr-6024-2012",
    "abnt-nbr-6028-2021",
    "ibge-tabular-1993",
}

catalog = load("standards/catalog.json")
set_source_checked(catalog, article_sources)
article_guide = next(source for source in catalog["sources"] if source["id"] == "ufc-guia-artigos-2022")
article_guide["notes"] = (
    "Fonte institucional atual para o perfil artigo. Referências internas antigas à NBR 10520:2002 e "
    "NBR 6023:2018 não selecionam a edição técnica vigente. V3-A1 reconfirmou em 2026-09-04 que "
    "citações usam NBR 10520:2023 e referências usam NBR 6023:2025 sob a política de precedência atual."
)
save("standards/catalog.json", catalog)

precedence = load("standards/precedence.json")
precedence["reviewed_at"] = TODAY
principle = (
    "No perfil de artigo científico, guias UFC específicos de domínio e normas ABNT vigentes substituem "
    "referências técnicas obsoletas embutidas no guia de artigos sem invalidar requisitos institucionais compatíveis."
)
if principle not in precedence["principles"]:
    precedence["principles"].append(principle)
save("standards/precedence.json", precedence)

source_audit = load("standards/source-audit.json")
source_audit["reviewed_at"] = TODAY
set_source_checked(source_audit, article_sources)
source_audit["v3_a1_article_reconfirmation"] = {
    "status": "DONE",
    "reviewed_at": TODAY,
    "entry_main_sha": A1_ENTRY,
    "implementation_base_main_sha": BASE,
    "current_article_guide": "ufc-guia-artigos-2022",
    "current_article_presentation_standard": "abnt-nbr-6022-2018",
    "current_cross_cutting_standards": [
        "abnt-nbr-10520-2023",
        "abnt-nbr-6023-2025",
        "abnt-nbr-6024-2012",
        "abnt-nbr-6028-2021",
        "ibge-tabular-1993",
    ],
    "stale_embedded_references": {
        "abnt-nbr-10520-2002": "abnt-nbr-10520-2023",
        "abnt-nbr-6023-2018": "abnt-nbr-6023-2025",
    },
    "runtime_implementation_started": False,
}
save("standards/source-audit.json", source_audit)

status_policy = load("standards/source-status-policy.json")
status_policy["reviewed_at"] = TODAY
save("standards/source-status-policy.json", status_policy)

evidence_registry = load("standards/evidence-registry.json")
evidence_registry["reviewed_at"] = TODAY
if not any(entry["id"] == ARTICLE_EVIDENCE for entry in evidence_registry["evidence"]):
    evidence_registry["evidence"].append(
        {
            "id": ARTICLE_EVIDENCE,
            "type": "manual",
            "description": (
                "V3-A1 manual source/locator/applicability review for scientific-article rules. "
                "This classifies source evidence only and is not article runtime proof."
            ),
            "target": {"review": "docs/ARTICLE-NORMATIVE-CONTRACT.md"},
        }
    )
save("standards/evidence-registry.json", evidence_registry)


def rule(rule_id: str, requirement: str, locator: str, normativity: str, kind: str, values: dict,
         sources: list[str], scope: str = "technical", mode: str = "manual", applicability: dict | None = None) -> dict:
    result = {
        "id": rule_id,
        "category": "scientific-article",
        "requirement": requirement,
        "locator": locator,
        "normativity": normativity,
        "kind": kind,
        "values": values,
        "validation": {"mode": mode, "checks": [ARTICLE_EVIDENCE]},
        "scope": scope,
        "sources": sources,
    }
    if applicability is not None:
        result["applicability"] = applicability
    return result


article_rules = [
    rule(
        "article.title.primary.required",
        "O artigo apresenta título e eventual subtítulo no idioma principal do texto.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8",
        "required",
        "article-element-presence",
        {"element": "primary-title", "required": True},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.authorship.required",
        "O artigo identifica a autoria.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8",
        "required",
        "article-element-presence",
        {"element": "authorship", "required": True},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.summary.primary.required",
        "O artigo apresenta resumo no idioma principal do texto.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8",
        "required",
        "article-element-presence",
        {"element": "primary-summary", "required": True},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.dates.submission-approval.required",
        "O artigo registra as datas de submissão e aprovação aplicáveis ao contexto acadêmico.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11",
        "required",
        "article-dates",
        {"submission_date": True, "approval_date": True},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.introduction.required",
        "A parte textual do artigo contém introdução.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12",
        "required",
        "article-text-structure",
        {"element": "introduction", "required": True},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.development.required",
        "A parte textual do artigo contém desenvolvimento.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12",
        "required",
        "article-text-structure",
        {"element": "development", "required": True},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.final-considerations.required",
        "A parte textual do artigo contém considerações finais.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12",
        "required",
        "article-text-structure",
        {"element": "final-considerations", "required": True},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.references.required",
        "O artigo contém lista de referências.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12",
        "required",
        "article-element-presence",
        {"element": "references", "required": True, "format_standard": "abnt-nbr-6023-2025"},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.title.foreign.optional",
        "Título e subtítulo em outro idioma são elementos opcionais.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8-9",
        "optional",
        "article-element-optionality",
        {"element": "foreign-title", "required": False},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.summary.foreign.optional",
        "Resumo em outro idioma é elemento opcional no perfil geral da UFC.",
        "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11",
        "optional",
        "article-element-optionality",
        {"element": "foreign-summary", "required": False},
        ["abnt-nbr-6022-2018", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.title.primary.typography",
        "O título principal segue a apresentação institucional indicada pelo guia UFC para artigos.",
        "Guia UFC de Artigos 2022, p. 9",
        "required",
        "article-title-typography",
        {"alignment": "center", "case": "uppercase", "weight": "bold", "font_size_pt": 12, "line_spacing": "single"},
        ["ufc-guia-artigos-2022"],
        scope="institutional",
    ),
    rule(
        "article.authorship.metadata.footnote",
        "A identificação complementar do autor é apresentada em nota de rodapé conforme o guia UFC.",
        "Guia UFC de Artigos 2022, p. 9",
        "required",
        "article-author-metadata",
        {"placement": "footnote", "includes_affiliation_or_biographical_note": True, "contact_supported": True},
        ["ufc-guia-artigos-2022"],
        scope="institutional",
    ),
    rule(
        "article.authorship.alignment.recommended",
        "O alinhamento à direita para o nome do autor é uma recomendação institucional, não requisito técnico obrigatório.",
        "Guia UFC de Artigos 2022, p. 9",
        "recommended",
        "article-author-alignment",
        {"recommended_alignment": "right"},
        ["ufc-guia-artigos-2022"],
        scope="institutional",
    ),
    rule(
        "article.body.typography",
        "Os elementos textuais seguem a apresentação institucional indicada pelo guia UFC para artigos.",
        "Guia UFC de Artigos 2022, p. 12",
        "required",
        "article-body-typography",
        {"font_size_pt": 12, "alignment": "justified", "first_line_indent_cm": 2, "line_spacing": "single"},
        ["ufc-guia-artigos-2022"],
        scope="institutional",
    ),
    rule(
        "article.summary.word-count.recommended",
        "Para artigos, o intervalo de 150 a 250 palavras no resumo é tratado como recomendação, não como requisito absoluto.",
        "ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10-11",
        "recommended",
        "article-summary-length",
        {"recommended_min_words": 150, "recommended_max_words": 250},
        ["abnt-nbr-6028-2021", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.summary.keywords.minimum.recommended",
        "A indicação de pelo menos três palavras-chave é tratada como recomendação.",
        "ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10-11",
        "recommended",
        "article-summary-keywords",
        {"recommended_min_keywords": 3},
        ["abnt-nbr-6028-2021", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.summary.single-paragraph.recommended",
        "A redação do resumo em parágrafo único é tratada conservadoramente como recomendação no contrato A1.",
        "ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10-11",
        "recommended",
        "article-summary-paragraphs",
        {"recommended_paragraphs": 1},
        ["abnt-nbr-6028-2021", "ufc-guia-artigos-2022"],
    ),
    rule(
        "article.journal-guidelines.precedence",
        "Quando o artigo for submetido a periódico com instruções próprias, essas instruções devem ser verificadas como condição de aplicabilidade do perfil genérico UFC.",
        "Guia UFC de Artigos 2022, p. 6",
        "required-when-applicable",
        "article-journal-boundary",
        {"journal_specific_instructions_must_be_checked": True, "generic_ufc_profile_is_fallback": True},
        ["ufc-guia-artigos-2022"],
        scope="institutional",
        mode="conditional-manual",
        applicability={"context": "target-journal-submission"},
    ),
]

coverage = {
    "schema_version": 1,
    "reviewed_at": TODAY,
    "purpose": (
        "V3-A1 scientific-article normative contract. Rules are source-backed but intentionally manual/conditional-manual "
        "until V3-A2 implements article runtime and article-specific executable evidence."
    ),
    "rules": article_rules,
}
save("standards/coverage-rules-article.json", coverage)


def unavailable(source_id: str) -> dict:
    return {
        "source_id": source_id,
        "status": "UNAVAILABLE_WITH_REASON",
        "checked_at": TODAY,
        "locator": None,
        "reason": (
            "The current edition was reconfirmed, but licensed ABNT clause text was not directly available to the A1 executor; "
            "no proprietary clause wording or locator is asserted from memory."
        ),
    }


def verified(source_id: str, locator: str) -> dict:
    return {"source_id": source_id, "status": "VERIFIED", "checked_at": TODAY, "locator": locator}


def ruleset(ruleset_id: str, rule_ids: list[str], locator: str, source_checks: list[dict]) -> dict:
    states = {item["status"] for item in source_checks}
    if states == {"VERIFIED"}:
        status = "VERIFIED"
    elif states == {"UNAVAILABLE_WITH_REASON"}:
        status = "UNAVAILABLE_WITH_REASON"
    else:
        status = "PARTIAL_WITH_REASON"
    return {
        "id": ruleset_id,
        "status": status,
        "rule_ids": rule_ids,
        "current_locator": locator,
        "source_checks": source_checks,
    }

locator_audit = {
    "schema_version": 1,
    "reviewed_at": TODAY,
    "rulesets": [
        ruleset(
            "article-structure-core",
            ["article.title.primary.required", "article.authorship.required", "article.summary.primary.required"],
            "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8",
            [unavailable("abnt-nbr-6022-2018"), verified("ufc-guia-artigos-2022", "p. 8")],
        ),
        ruleset(
            "article-dates",
            ["article.dates.submission-approval.required"],
            "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11",
            [unavailable("abnt-nbr-6022-2018"), verified("ufc-guia-artigos-2022", "p. 8, 11")],
        ),
        ruleset(
            "article-text-core",
            ["article.introduction.required", "article.development.required", "article.final-considerations.required", "article.references.required"],
            "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12",
            [unavailable("abnt-nbr-6022-2018"), verified("ufc-guia-artigos-2022", "p. 8, 12")],
        ),
        ruleset(
            "article-foreign-title",
            ["article.title.foreign.optional"],
            "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8-9",
            [unavailable("abnt-nbr-6022-2018"), verified("ufc-guia-artigos-2022", "p. 8-9")],
        ),
        ruleset(
            "article-foreign-summary",
            ["article.summary.foreign.optional"],
            "ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11",
            [unavailable("abnt-nbr-6022-2018"), verified("ufc-guia-artigos-2022", "p. 8, 11")],
        ),
        ruleset(
            "article-title-typography",
            ["article.title.primary.typography"],
            "Guia UFC de Artigos 2022, p. 9",
            [verified("ufc-guia-artigos-2022", "p. 9")],
        ),
        ruleset(
            "article-author-metadata",
            ["article.authorship.metadata.footnote"],
            "Guia UFC de Artigos 2022, p. 9",
            [verified("ufc-guia-artigos-2022", "p. 9")],
        ),
        ruleset(
            "article-author-alignment",
            ["article.authorship.alignment.recommended"],
            "Guia UFC de Artigos 2022, p. 9",
            [verified("ufc-guia-artigos-2022", "p. 9")],
        ),
        ruleset(
            "article-body-typography",
            ["article.body.typography"],
            "Guia UFC de Artigos 2022, p. 12",
            [verified("ufc-guia-artigos-2022", "p. 12")],
        ),
        ruleset(
            "article-summary-recommendations",
            ["article.summary.word-count.recommended", "article.summary.keywords.minimum.recommended", "article.summary.single-paragraph.recommended"],
            "ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10-11",
            [unavailable("abnt-nbr-6028-2021"), verified("ufc-guia-artigos-2022", "p. 10-11")],
        ),
        ruleset(
            "article-journal-boundary",
            ["article.journal-guidelines.precedence"],
            "Guia UFC de Artigos 2022, p. 6",
            [verified("ufc-guia-artigos-2022", "p. 6")],
        ),
    ],
}
save("standards/locator-audit-article.json", locator_audit)

contribution = load("standards/evidence-contribution-policy.json")
contribution["reviewed_at"] = TODAY
for item in article_rules:
    rid = item["id"]
    mode = item["validation"]["mode"]
    contribution["nonautomatic_rules"][rid] = {
        "class": "conditional-review" if mode == "conditional-manual" else "manual-review",
        "mode": mode,
        "rationale": (
            "V3-A1 classifies the rule from current source evidence only; article runtime and executable rule evidence are intentionally deferred to V3-A2."
        ),
    }
save("standards/evidence-contribution-policy.json", contribution)

# Allow article rules only in the active article phases, and require A1 to stay source-only.
checker = Path("tests/checks/normative_full_contract.py")
text = checker.read_text(encoding="utf-8")
if "import json\n" not in text:
    text = text.replace("from __future__ import annotations\n\nimport re\n", "from __future__ import annotations\n\nimport json\nimport re\n")
old = '''    article_rules = sorted(rule_id for rule_id in rules if rule_id.startswith("article."))\n    if article_rules:\n        fail(\n            "article rules became operational before V3-A1: "\n            + ", ".join(article_rules)\n        )\n'''
new = '''    article_rules = sorted(rule_id for rule_id in rules if rule_id.startswith("article."))\n    roadmap = json.loads((ROOT / "release" / "v3-roadmap.json").read_text(encoding="utf-8"))\n    phase = roadmap.get("phase")\n    if article_rules and phase not in {"V3-A1", "V3-A2"}:\n        fail("article rules are active outside the article roadmap phases")\n    if phase == "V3-A1":\n        if not article_rules:\n            fail("V3-A1 requires the source-backed article rule contract")\n        for rule_id in article_rules:\n            validation = rules[rule_id]["validation"]\n            if validation["mode"] not in {"manual", "conditional-manual"}:\n                fail(f"{rule_id}: A1 must not claim executable article validation")\n            if validation["checks"] != ["article.source-review"]:\n                fail(f"{rule_id}: A1 article evidence must be source-review only")\n'''
if old not in text:
    raise SystemExit("normative_full_contract article guard drifted")
text = text.replace(old, new)
old_uncovered = '''    uncovered = sorted(\n        rule_id\n        for rule_id in extension_ids\n        if rules[rule_id]["validation"]["mode"] != "not-applicable"\n        and not (set(rules[rule_id]["validation"]["checks"]) & gates)\n    )\n'''
new_uncovered = '''    runner_required_modes = {"automatic", "automatic-deep", "automatic-partial", "automatic-policy", "conditional"}\n    uncovered = sorted(\n        rule_id\n        for rule_id in extension_ids\n        if rules[rule_id]["validation"]["mode"] in runner_required_modes\n        and not (set(rules[rule_id]["validation"]["checks"]) & gates)\n    )\n'''
if old_uncovered not in text:
    raise SystemExit("normative_full_contract uncovered guard drifted")
text = text.replace(old_uncovered, new_uncovered)
checker.write_text(text, encoding="utf-8")

# Human-readable article contract.
rows = "\n".join(
    f"| `{item['id']}` | {item['normativity']} | {item['validation']['mode']} | {item['locator']} |"
    for item in article_rules
)
Path("docs/ARTICLE-NORMATIVE-CONTRACT.md").write_text(
    f"""# Scientific Article Normative Contract — V3-A1

Updated: {TODAY}

This document records the source-backed scientific-article contract reconstructed in V3-A1. It is a human-readable view of `standards/coverage-rules-article.json`; the machine-readable standards files remain authoritative for validation.

## Scope and entry

- A1 canonical entry: `{A1_ENTRY}`.
- Certified non-article foundation: `{FOUNDATION}`; unchanged by A1.
- A1 implementation base: `{BASE}`.
- Runtime/profile implementation: **not allowed in A1**.
- Article rules introduced: **{len(article_rules)}** — 17 manual and 1 conditional-manual.
- A1 evidence owner: `{ARTICLE_EVIDENCE}`; source classification only, never runtime proof.

## Reconfirmed authority set

The current UFC normalization page continues to expose the corrected 2022 scientific-article guide (file corrected in 2023). The article guide remains the institutional article-specific baseline, while current technical editions govern technical domains. The current article presentation standard remains ABNT NBR 6022:2018. Cross-cutting article requirements inherit the current citation, reference, section-numbering, abstract and tabular standards already present in the v3 source registry: NBR 10520:2023, NBR 6023:2025, NBR 6024:2012, NBR 6028:2021 and IBGE tabular guidance.

The corrected UFC article guide still embeds obsolete references to NBR 10520:2002 and NBR 6023:2018. Those editions are contextual only. They do not override the current NBR 10520:2023 and NBR 6023:2025 entries.

## Precedence

For article-specific technical requirements, the current applicable technical standard governs and compatible UFC article guidance supports it. For UFC institutional presentation details not defined as technical-standard requirements, the current UFC article guide governs. For citations and references, the current cross-cutting v3 contracts govern their domains rather than the stale editions embedded in the older article guide. For submission to a specific periodical, the journal's own instructions are an applicability boundary and must be checked before treating the generic UFC article profile as sufficient.

## Requirement versus recommendation

A1 preserves modality. `deve`/mandatory-element statements are represented as requirements. `convém`, `sugerimos` and optional-element statements are not promoted to mandatory rules. In particular, the 150–250-word summary interval, a minimum of three keywords, a single-paragraph summary and right-aligned authorship are conservative recommendations in A1.

## Rule contract

| Rule | Normativity | A1 validation | Locator |
|---|---|---|---|
{rows}

## Locator/proof policy

Public UFC guide locators are verified directly. Where a rule also depends on proprietary ABNT clause text that was not directly available to this execution, `standards/locator-audit-article.json` records `PARTIAL_WITH_REASON`: the current edition is reconfirmed, but no clause wording or exact proprietary locator is invented. Every A1 article rule therefore remains `MANUAL` or `CONDITIONAL` in proof state. No article rule is `PROVEN`, and no existing green foundation gate is counted as article enforcement.

## V3-A2 bounded implementation contract

A2 may implement only the canonical `scientific-article` profile and executable tests needed to realize the A1 rule set. It must reuse the current cross-cutting citation/reference/section/table machinery rather than fork it; preserve the certified non-article foundation; keep recommendation/optional semantics distinct from requirements; add positive and negative article-specific evidence before promoting proof state; and keep journal-specific instructions as a conditional boundary. Any source conflict discovered in A2 returns to source review instead of being resolved by runtime guesswork.
""",
    encoding="utf-8",
)

replace_once(
    "docs/NORMATIVE-BASE.md",
    "| Research projects | ABNT NBR 15287:2025 |\n| Abstracts/reviews | ABNT NBR 6028:2021 |",
    "| Research projects | ABNT NBR 15287:2025 |\n| Scientific articles | ABNT NBR 6022:2018, with current cross-cutting citation/reference/summary standards |\n| Abstracts/reviews | ABNT NBR 6028:2021 |",
)
replace_once(
    "docs/NORMATIVE-BASE.md",
    "The active v3 foundation covers academic works and research projects. The scientific-article profile is not part of the active foundation tree during V3-R1 through V3-R5. Its previously researched normative evidence remains recoverable from Git history and is reintroduced only when V3-A1 starts.",
    "The certified v3 foundation covers academic works and research projects. V3-A1 has now reintroduced a source-backed scientific-article normative contract without adding article runtime behavior. Article rules are manual/conditional during A1 and become implementation candidates only in V3-A2. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
)
replace_once(
    "docs/NORMATIVE-CURRENCY.md",
    "Scientific-article support is intentionally outside the active foundation scope until V3-A1. The previously researched article source contract is preserved by Git history rather than by dormant v3 files. When V3-A1 starts, article sources and predicates must be reconfirmed against then-current technical and UFC institutional sources before runtime implementation resumes.",
    "V3-A1 reconfirmed the corrected UFC scientific-article guide (2022, corrected file dated 2023-04-27) and ABNT NBR 6022:2018 as the current article-presentation basis. The guide's embedded NBR 10520:2002 and NBR 6023:2018 references are superseded for their technical domains by NBR 10520:2023 and NBR 6023:2025. The A1 contract therefore preserves compatible institutional article guidance while using current cross-cutting technical editions. No article runtime implementation is part of A1.",
)

roadmap_path = "docs/ROADMAP-V3.0.0.md"
replace_once(
    roadmap_path,
    "| V3-A1 | ACTIVE | issue #275; exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` | source/normative article contract only; runtime work not started | reconfirm article authorities/currency/precedence and derive conservative rule contract |",
    "| V3-A1 | ACTIVE — CONTRACT CANDIDATE | issue #275; exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; implementation base `e40a56deeca8c22797398b0c95835964aefd2b15`; certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` | current article sources reconfirmed; 18 source-backed rules; 17 manual + 1 conditional-manual; runtime still absent | validate/merge A1 source contract, then record exact A2 entry |",
)
replace_once(
    roadmap_path,
    "## Immediate action\n\nExecute V3-A1/#275 source reconciliation. Keep the certified non-article foundation `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged unless current source evidence demonstrates a separately bounded cross-cutting conflict. V3-A2 and actual CTAN submission remain blocked.",
    "## V3-A1 source-contract candidate\n\nA1 reconfirmed the corrected UFC article guide, NBR 6022:2018 and the current cross-cutting NBR 10520:2023, NBR 6023:2025, NBR 6024:2012, NBR 6028:2021 and IBGE tabular basis. The new article contract contains 18 rules. All remain manual or conditional-manual, and ABNT locators unavailable without licensed clause access are explicitly `PARTIAL_WITH_REASON`. The certified foundation is unchanged and no article runtime/profile code exists in this lot.\n\n## Immediate action\n\nValidate and merge the A1 source-contract candidate. After its immutable main SHA exists, close #275 and activate V3-A2 from that exact predecessor. V3-A2 runtime work and actual CTAN submission remain blocked until that checkpoint is canonical.",
)

replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "- V3-A1/#275: **ACTIVE** from exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.\n- A1 is source/normative-contract work only; article runtime implementation is forbidden in A1.",
    "- V3-A1/#275: **ACTIVE — SOURCE CONTRACT CANDIDATE** from exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.\n- A1 implementation base: `e40a56deeca8c22797398b0c95835964aefd2b15`.\n- Current article authority set reconfirmed on 2026-09-04; 18 article rules are registered as 17 manual + 1 conditional-manual.\n- A1 evidence is source-only (`article.source-review`); no article runtime/profile implementation or article proof promotion is allowed in A1.",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "Execute V3-A1/#275 from exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`. Reconfirm current UFC scientific-article guidance and applicable ABNT authorities, currency, precedence, locators, applicability and requirement/recommendation distinctions. Build a conservative article normative contract before any article runtime implementation. Historical pre-v3 article research is discovery evidence only, never authority to restore blindly.",
    "Validate and merge the V3-A1 source-contract candidate. The source set and 18-rule conservative contract are now reconstructed; ABNT clause locators not directly available are recorded as partial-with-reason rather than guessed. After merge, capture the immutable A1 closeout SHA, close #275 and activate V3-A2. Do not implement article runtime before that exact-entry checkpoint.",
)

replace_once(
    "AGENTS.md",
    "- V3-R3, V3-R4 and V3-R5 are DONE. R5/#272 preserved certified product `c79f3c73f1d51a30175e8259269504d029442a1c`, passed release gate `33866258865` = `PASS=33 FAIL=0 SKIP=0`, package audit `33869888601`, and PR #276 gates, then closed at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`. V3-A1/#275 is ACTIVE from that exact SHA. A1 is source/normative-contract work only: no article runtime/profile implementation is allowed before A1 closes.",
    "- V3-R3, V3-R4 and V3-R5 are DONE. R5/#272 preserved certified product `c79f3c73f1d51a30175e8259269504d029442a1c`, passed release gate `33866258865` = `PASS=33 FAIL=0 SKIP=0`, package audit `33869888601`, and PR #276 gates, then closed at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`. V3-A1/#275 is ACTIVE from that exact SHA. Its current candidate reconfirms the article source set and registers 18 rules as source-only manual/conditional evidence. No article runtime/profile implementation or proof promotion is allowed before A1 closes canonically.",
)

insert_before_once(
    "README.md",
    "## Current v3 repository layout",
    """## V3-A1 scientific-article contract

The current A1 candidate reconfirms the UFC article guide and applicable current ABNT/cross-cutting sources, then registers 18 article rules without implementing an article runtime profile. Seventeen rules are manual and one is conditional-manual; inaccessible licensed ABNT clause locators remain explicitly partial rather than inferred. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.""",
)

append_section_once(
    "docs/ARCHITECTURE.md",
    "## V3-A1 scientific-article boundary",
    "V3-A1 adds only the source/rule contract under `standards/`. `coverage-rules-article.json` is consumed by the existing full-contract loader, while `locator-audit-article.json`, `article.source-review`, proof-state and contribution policy keep every article rule manual/conditional until A2. No article runtime module, profile implementation, template branch, validator shortcut or compatibility alias is introduced in A1. Cross-cutting citation/reference/section/table machinery remains shared rather than forked.",
)
append_section_once(
    "docs/ENGINEERING-LANGUAGE.md",
    "## V3-A1 article identifiers",
    "The A1 machine namespace is `article.*` and the future profile name is `scientific-article`. These are project-owned English identifiers. Portuguese remains in the academic requirements and rendered content where appropriate. Historical Portuguese machine IDs are discovery evidence only and are not restored.",
)
append_section_once(
    "docs/CTAN-RELEASE.md",
    "## V3-A1 release boundary",
    "A1 changes the normative source/rule contract but does not authorize CTAN submission. V3-A2 article runtime/test implementation must close and the roadmap must explicitly reach a release action before any upload. The certified non-article foundation remains unchanged during A1.",
)

roadmap = load("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-A1" or roadmap.get("stage") != "V3-A1":
    raise SystemExit("unexpected machine-state phase for A1")
for key in ("a1", "a1_preparation"):
    block = roadmap[key]
    block.update(
        {
            "work_started": True,
            "source_reconfirmation_status": "DONE",
            "source_reconfirmation_reviewed_at": TODAY,
            "normative_contract_status": "CANDIDATE",
            "implementation_base_main_sha": BASE,
            "article_rule_count": len(article_rules),
            "article_manual_rules": 17,
            "article_conditional_manual_rules": 1,
            "runtime_implementation_allowed": False,
            "runtime_implementation_started": False,
            "ctan_submission_allowed": False,
        }
    )
roadmap["a1_contract_candidate"] = {
    "status": "READY_FOR_GATES",
    "issue": 275,
    "entry_main_sha": A1_ENTRY,
    "implementation_base_main_sha": BASE,
    "certified_foundation_product_sha": FOUNDATION,
    "reviewed_at": TODAY,
    "article_rule_count": len(article_rules),
    "manual_rules": 17,
    "conditional_manual_rules": 1,
    "source_evidence_id": ARTICLE_EVIDENCE,
    "runtime_files_added": 0,
    "public_runtime_api_changed": False,
    "certified_foundation_changed": False,
    "proof_state_promoted": False,
    "stale_embedded_editions": {
        "NBR 10520:2002": "NBR 10520:2023",
        "NBR 6023:2018": "NBR 6023:2025",
    },
    "a2_activation_pending": True,
}
save("release/v3-roadmap.json", roadmap)

print(f"A1 article source contract reconciled: rules={len(article_rules)} runtime=0 foundation={FOUNDATION}")
