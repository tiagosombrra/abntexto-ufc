#!/usr/bin/env python3
"""Fast, dependency-free fail-closed preflight for the 28 integrated documents."""
from __future__ import annotations

import json
import runpy
from pathlib import Path
import subprocess
import sys
import tempfile

from integrated_metadata_probe import (
    METADATA_KEYS, check_log as check_metadata_log,
    check_source as check_metadata_source,
    negative_controls as metadata_negative_controls,
    expected_receipt as metadata_receipt,
    marker as metadata_marker,
)

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "tests/integration/frontmatter/generate-integrated-locale.py"
RUNNER = ROOT / "tests/integration/frontmatter/run-integrated-locale.py"
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
PROFILES = {
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
}
ACADEMIC = {
    "undergraduate-capstone", "specialization-capstone",
    "masters-thesis", "doctoral-thesis",
}
PROJECTS = {"research-project", "anonymized-research-project"}
DUPLEX_PROFILES = {
    "masters-thesis", "doctoral-thesis", "anonymized-research-project",
}
APPROVAL_LAST_EXAMINER = {
    "undergraduate-capstone": 3,
    "specialization-capstone": 4,
    "masters-thesis": 5,
    "doctoral-thesis": 6,
}
ROLE_GENDERS = {
    "undergraduate-capstone": (False, False),
    "specialization-capstone": (True, False),
    "masters-thesis": (False, True),
    "doctoral-thesis": (True, True),
    "research-project": (True, True),
    "anonymized-research-project": (True, True),
    "scientific-article": (False, False),
}
PRETEXTUAL_COMMANDS = (
    r"\ufcPrintAcknowledgments{", r"\ufcPrintErrata{",
    r"\ufcPrintListOfIllustrations", r"\ufcPrintListOfTextTables",
    r"\ufcPrintListOfCharts", r"\ufcPrintListOfAbbreviationsAndAcronyms{",
    r"\ufcPrintListOfSymbols{",
)
TOTAL = 0


def validate_case(case: dict, locale: str, source: str) -> None:
    """Validate the same source invariants for real cases and mutations."""
    profile = case["profile"]
    if check_metadata_source(source) != 53:
        raise ValueError(f"authored metadata probe missing: {profile}/{locale}")
    if (case["locale"] != locale or
            rf"\DocumentMetadata{{lang={LOCALES[locale]}," not in source or
            f"document-language={locale}" not in source):
        raise ValueError(f"mismatched document-language and PDF metadata: {profile}/{locale}")
    required = (
        r"\ufcPrintReferences", r"\parencite{silva2020}",
        r"\textcite{oliveira2011}", r"\ufcSource{Synthetic original}",
        r"\ufcNote{Synthetic object note}", r"\begin{tabular}",
        r"\begin{ufcobject}",
        r"\begin{ufclettereditems}", r"\begin{ufcdashedsubitems}",
        r"\begin{ufcdefinitionlist}", r"\ufcListEntry{",
        r"\ufcDocumentLanguage", r"\ufcDocumentType",
    )
    if any(x not in source for x in required):
        raise ValueError(f"missing joined core component: {profile}/{locale}")
    print_mode = "double-sided" if profile in DUPLEX_PROFILES else "single-sided"
    routing_commands = (
        ("ufcIfProjectTF", "PROJECT"),
        ("ufcIfAnonymizedProjectTF", "ANON"),
    )
    required_routing = (
        f"print-mode={print_mode}",
        "title={Integrated Multilingual Document}",
        r"\typeout{INTEGRATED-I18N-API-PRINT-MODE=\ufcPrintMode}",
        r"\typeout{INTEGRATED-I18N-API-META-TITLE=\ufcMeta{title}}",
        *(
            "\\" + command + "{INTEGRATED-" + label
            + "-TRUE-" + locale.upper() + ". "
            for command, label in routing_commands
        ),
        *(
            "}{INTEGRATED-" + label + "-FALSE-" + locale.upper() + ". "
            for _, label in routing_commands
        ),
        *(
            r"\typeout{INTEGRATED-I18N-" + label + "=TRUE}"
            for _, label in routing_commands
        ),
        *(
            r"\typeout{INTEGRATED-I18N-" + label + "=FALSE}"
            for _, label in routing_commands
        ),
    )
    if any(value not in source for value in required_routing):
        raise ValueError(f"missing or incorrect public routing source: {profile}/{locale}")
    role_options = (
        "advisor={Integrated Advisor}",
        "coadvisor={Integrated Coadvisor}",
        "advisor-feminine-label=" + ("true" if ROLE_GENDERS[profile][0] else "false"),
        "coadvisor-feminine-label=" + ("true" if ROLE_GENDERS[profile][1] else "false"),
    )
    # Match complete setup lines: "advisor-feminine-label=true" is a suffix
    # of "coadvisor-feminine-label=true" and substring matching admits mutants.
    setup_lines = {line.strip().rstrip(",") for line in source.splitlines()}
    if any(option not in setup_lines for option in role_options):
        raise ValueError(f"missing or wrong gender/role fixture: {profile}/{locale}")
    if profile in ACADEMIC:
        last = APPROVAL_LAST_EXAMINER[profile]
        for slot in range(2, last + 1):
            signatures = (
                f"examiner-{slot}={{Integrated Examiner {slot}}}",
                f"examiner-{slot}-institution={{Integrated Institution {slot}}}",
                f"examiner-{slot}-unit={{Integrated Hidden Unit {slot}}}",
            )
            if any(value not in setup_lines for value in signatures):
                raise ValueError(f"missing or incorrect committee metadata: {profile}/{locale}/{slot}")
        for slot in range(last + 1, 7):
            if any(line.startswith(f"examiner-{slot}=")
                   or line.startswith(f"examiner-{slot}-")
                   for line in setup_lines):
                raise ValueError(f"unexpected extra examiner: {profile}/{locale}/{slot}")
    elif any(line.startswith("examiner-") for line in setup_lines):
        raise ValueError(f"inapplicable committee metadata: {profile}/{locale}")
    if profile in ACADEMIC and any(command not in source
                               for command in PRETEXTUAL_COMMANDS):
        raise ValueError(f"missing academic pretextual module: {profile}/{locale}")
    if profile not in ACADEMIC and any(command in source
                                   for command in PRETEXTUAL_COMMANDS):
        raise ValueError(f"inapplicable academic frontmatter: {profile}/{locale}")
    if profile == "scientific-article":
        if r"\ufcPrintArticleFrontMatter" not in source:
            raise ValueError(f"article frontmatter absent: {profile}/{locale}")
    else:
        if r"\ufcPrintTitlePage" not in source or r"\appendix{" not in source:
            raise ValueError(f"academic/project front/back missing: {profile}/{locale}")
    if profile == "doctoral-thesis" and (
            r"\ufcPrintGlossary" not in source or r"\ufcPrintIndex" not in source):
        raise ValueError(f"doctoral optional modules missing: {profile}/{locale}")


def check(out: Path) -> None:
    global TOTAL
    seen = set()
    for locale, bcp in LOCALES.items():
        subprocess.run([sys.executable, str(GENERATOR), "--locale", locale,
                        "--output", str(out)], cwd=ROOT, check=True,
                       capture_output=True, text=True)
        folder = out / locale
        cases = json.loads((folder / "source-index.json").read_text(encoding="utf-8"))
        if len(cases) != 7 or {r["profile"] for r in cases} != PROFILES:
            raise ValueError(f"incomplete seven-profile manifest for {locale}")
        for c in cases:
            key = (c["profile"], c["locale"])
            if key in seen or c["locale"] != locale:
                raise ValueError(f"duplicate or wrong locale case: {key}")
            seen.add(key)
            tex = Path(c["source"]).read_text(encoding="utf-8")
            validate_case(c, locale, tex)
            support = [Path(source) for source in c["support_sources"]]
            if len(support) != (6 if c["profile"] in ACADEMIC else 2):
                raise ValueError(f"unexpected pretextual support inputs: {key}")
            for source in support:
                if not source.is_file():
                    raise ValueError(f"unavailable synthetic input: {source}")
            if c["profile"] in ACADEMIC:
                markers = {
                    "ack": f"INTEGRATED-AUTHORED-GRATITUDE-{locale.upper()}",
                    "errata": f"INTEGRATED-AUTHORED-CORRECTIONS-{locale.upper()}",
                    "abbreviations": f"INTEGRATED-ABBREVIATION-{locale.upper()}",
                    "symbols": f"INTEGRATED-SYMBOL-{locale.upper()}",
                }
                for suffix, marker in markers.items():
                    source = next((
                        p for p in support
                        if p.name.endswith(f"-{suffix}.tex")
                    ), None)
                    if source is None or marker not in source.read_text(encoding="utf-8"):
                        raise ValueError(f"missing populated author content: {key}/{suffix}")
            TOTAL += 1
    if TOTAL != 28 or len(seen) != 28:
        raise ValueError(f"expected 28 distinct generated sources, got {TOTAL}")
    # Exercise the SAME production-source guard with deliberately corrupted
    # cases. Mutation detection alone is not a meaningful negative test.
    sample = (out / "en" / "integrated-doctoral-thesis-en.tex").read_text()
    fixture = {"profile": "doctoral-thesis", "locale": "en"}
    damaged = {
        "glossary": sample.replace(r"\ufcPrintGlossary", "", 1),
        "wrong_pdf_lang": sample.replace(
            r"\DocumentMetadata{lang=en-US,", r"\DocumentMetadata{lang=pt-BR,", 1),
        "missing_references": sample.replace(r"\ufcPrintReferences", "", 1),
        "missing_lettered_items": sample.replace(r"\begin{ufclettereditems}", "", 1),
        "missing_dashed_items": sample.replace(r"\begin{ufcdashedsubitems}", "", 1),
        "missing_definition_list": sample.replace(r"\begin{ufcdefinitionlist}", "", 1),
        "missing_list_entry": sample.replace(r"\ufcListEntry{", "", 1),
        "missing_api_language": sample.replace(r"\ufcDocumentLanguage", "", 1),
        "missing_api_type": sample.replace(r"\ufcDocumentType", "", 1),
        "missing_api_print_mode": sample.replace(r"\ufcPrintMode", "", 1),
        "missing_api_meta_title": sample.replace(r"\ufcMeta{title}", "", 1),
        "missing_coadvisor": sample.replace(
            "coadvisor={Integrated Coadvisor}", "", 1),
        "wrong_advisor_gender": sample.replace(
            "advisor-feminine-label=true", "advisor-feminine-label=false", 1),
        "wrong_coadvisor_gender": sample.replace(
            "coadvisor-feminine-label=true", "coadvisor-feminine-label=false", 1),
        "missing_examiner_6": sample.replace(
            "examiner-6={Integrated Examiner 6}", "examiner-6={}", 1),
        "missing_examiner_6_institution": sample.replace(
            "examiner-6-institution={Integrated Institution 6}",
            "examiner-6-institution={}", 1),
        "missing_examiner_6_unit": sample.replace(
            "examiner-6-unit={Integrated Hidden Unit 6}",
            "examiner-6-unit={}", 1),
        "alter_author_title": sample.replace(
            "title={Integrated Multilingual Document}",
            "title={Changed Title}", 1),
        "wrong_print_mode": sample.replace(
            "print-mode=double-sided", "print-mode=single-sided", 1),
        "missing_project_route": sample.replace(
            r"\ufcIfProjectTF{INTEGRATED-PROJECT-TRUE-EN.", "", 1),
        "missing_anon_route": sample.replace(
            r"\ufcIfAnonymizedProjectTF{INTEGRATED-ANON-TRUE-EN.", "", 1),
        "inverted_project_true_arm": sample.replace(
            "INTEGRATED-PROJECT-TRUE-EN.",
            "INTEGRATED-PROJECT-FALSE-EN.", 1),
        "inverted_anon_true_arm": sample.replace(
            "INTEGRATED-ANON-TRUE-EN.",
            "INTEGRATED-ANON-FALSE-EN.", 1),
        **{
            "missing_pretextual_" + str(index):
                sample.replace(command, "", 1)
            for index, command in enumerate(PRETEXTUAL_COMMANDS)
        },
    }
    # Cover the distinguishing anonymized profile as well as ordinary
    # academic cases so a normal project cannot masquerade as anonymous.
    anonymous = (out / "en" / "integrated-anonymized-research-project-en.tex").read_text()
    anon_fixture = {"profile": "anonymized-research-project", "locale": "en"}
    anon_damaged = {
        "anonymized_wrong_print_mode": anonymous.replace(
            "print-mode=double-sided", "print-mode=single-sided", 1),
        "anonymized_removed_conditional": anonymous.replace(
            r"\ufcIfAnonymizedProjectTF{INTEGRATED-ANON-TRUE-EN.", "", 1),
        "anonymized_missing_advisor": anonymous.replace(
            "advisor={Integrated Advisor}", "advisor={}", 1),
        "anonymized_missing_coadvisor": anonymous.replace(
            "coadvisor={Integrated Coadvisor}", "coadvisor={}", 1),
        "anonymized_wrong_advisor_gender": anonymous.replace(
            "advisor-feminine-label=true", "advisor-feminine-label=false", 1),
        "anonymized_wrong_coadvisor_gender": anonymous.replace(
            "coadvisor-feminine-label=true", "coadvisor-feminine-label=false", 1),
    }
    for label, mutant in damaged.items():
        if mutant == sample:
            raise ValueError(f"mutation ineffective: {label}")
        try:
            validate_case(fixture, "en", mutant)
        except ValueError:
            pass
        else:
            raise ValueError(f"negative mutation was accepted: {label}")
    for label, mutant in anon_damaged.items():
        if mutant == anonymous:
            raise ValueError(f"ineffective anonymized mutation: {label}")
        try:
            validate_case(anon_fixture, "en", mutant)
        except ValueError:
            pass
        else:
            raise ValueError(f"anonymized mutation accepted: {label}")


def check_list_page_mutations() -> None:
    """Test the real PDF-list predicate against aggregate-list false positives."""
    namespace = runpy.run_path(str(RUNNER), run_name="i18n_preflight_runner")
    predicate = namespace["check_dedicated_list_pages"]
    pages = [
        # Inherited illustration list duplicates entries from both objects.
        "LIST OF ILLUSTRATIONS\nINTEGRATED-CHART-EN\nINTEGRATED-TEXTTABLE-EN",
        "             LIST OF TEXT TABLES\nINTEGRATED-TEXTTABLE-EN",
        "                 LIST OF CHARTS\nINTEGRATED-CHART-EN",
        "INTEGRATED-SECTION-EN\nINTEGRATED-CHART-EN\nINTEGRATED-TEXTTABLE-EN",
    ]
    good = "\f".join(pages) + "\f"
    result = predicate(good, "en")
    if set(result) != {"charts", "text-tables"}:
        raise ValueError("positive dedicated list-page predicate failed")
    variants = {
        "aggregate_only_chart": (
            "                 LIST OF CHARTS\nINTEGRATED-CHART-EN", "LIST OF CHARTS"
        ),
        "aggregate_only_text_table": (
            "             LIST OF TEXT TABLES\nINTEGRATED-TEXTTABLE-EN",
            "LIST OF TEXT TABLES",
        ),
        "chart_body_missing": (
            "INTEGRATED-SECTION-EN\nINTEGRATED-CHART-EN\n"
            "INTEGRATED-TEXTTABLE-EN",
            "INTEGRATED-SECTION-EN\nINTEGRATED-TEXTTABLE-EN",
        ),
        "text_table_body_missing": (
            "INTEGRATED-SECTION-EN\nINTEGRATED-CHART-EN\n"
            "INTEGRATED-TEXTTABLE-EN",
            "INTEGRATED-SECTION-EN\nINTEGRATED-CHART-EN",
        ),
    }
    for label, (before, after) in variants.items():
        mutant = good.replace(before, after, 1)
        if mutant == good:
            raise ValueError(f"ineffective dedicated-list mutation: {label}")
        try:
            predicate(mutant, "en")
        except ValueError:
            pass
        else:
            raise ValueError(
                f"dedicated list accepted false-positive aggregate: {label}"
            )


def check_role_page_mutations() -> None:
    """Check production PDF predicate with genuine expected/foreign role pairs."""
    run = runpy.run_path(str(RUNNER), run_name="i18n_role_preflight_runner")
    predicate = run["check_role_title_page"]
    labels = run["ROLE_LABELS"]
    cases = run["ROLE_GENDERS"]
    for locale in LOCALES:
        for profile in ACADEMIC:
            genders = cases[profile]
            first = labels[locale][0][int(genders[0])]
            second = labels[locale][1][int(genders[1])]
            title = (
                "Integrated Multilingual Document\n"
                + first + ": Integrated Advisor.\n"
                + second + ": Integrated Coadvisor.\n"
            )
            good = "COVER PAGE\f" + title + "\fEXAMINING COMMITTEE\nIntegrated Advisor\f"
            result = predicate(good, profile, locale)
            if result.get("applicability") != "title-page":
                raise ValueError(f"missing role positive control: {profile}/{locale}")
            mutants = {
                "missing_advisor": good.replace(first + ": Integrated Advisor.", "", 1),
                "missing_coadvisor": good.replace(second + ": Integrated Coadvisor.", "", 1),
                "advisor_wrong_name": good.replace(
                    first + ": Integrated Advisor.", first + ": Other Advisor.", 1),
                "coadvisor_wrong_name": good.replace(
                    second + ": Integrated Coadvisor.", second + ": Other Coadvisor.", 1),
                # Exact-label negative controls: in English the word "Advisor"
                # is a suffix of "Co-advisor", but this is NOT the advisor role.
                "advisor_wrong_role": good.replace(
                    first + ": Integrated Advisor.",
                    labels[locale][1][int(genders[1])] + ": Integrated Advisor.", 1),
                "coadvisor_wrong_role": good.replace(
                    second + ": Integrated Coadvisor.",
                    labels[locale][0][int(genders[0])] + ": Integrated Coadvisor.", 1),
            }
            if labels[locale][0][0] != labels[locale][0][1]:
                wrong = labels[locale][0][1-int(genders[0])]
                mutants["wrong_advisor_gender"] = good.replace(
                    first + ": Integrated Advisor.", wrong + ": Integrated Advisor.", 1)
            if labels[locale][1][0] != labels[locale][1][1]:
                wrong = labels[locale][1][1-int(genders[1])]
                mutants["wrong_coadvisor_gender"] = good.replace(
                    second + ": Integrated Coadvisor.", wrong + ": Integrated Coadvisor.", 1)
            for label, bad in mutants.items():
                if bad == good:
                    raise ValueError(f"ineffective role PDF mutation: {label}/{locale}")
                try:
                    predicate(bad, profile, locale)
                except ValueError:
                    pass
                else:
                    raise ValueError(f"role PDF mutation passed: {label}/{profile}/{locale}")
        # Anonymous source still supplies both names; they must be absent from
        # ALL rendered PDF pages, not merely the second title page.
        good = "COVER\fIntegrated Multilingual Document\nREDACTED\fPROJECT BODY\f"
        result = predicate(good, "anonymized-research-project", locale)
        if not result.get("names_redacted"):
            raise ValueError(f"anonymous positive control failed: {locale}")
        for kind, corrupt in (
            ("advisor", good + "\fIntegrated Advisor"),
            ("coadvisor", good + "\fIntegrated Coadvisor"),
            ("role_label", good.replace(
                "REDACTED", labels[locale][0][0] + ": REDACTED", 1)),
        ):
            try:
                predicate(corrupt, "anonymized-research-project", locale)
            except ValueError:
                pass
            else:
                raise ValueError(f"anonymous leak mutation passed: {kind}/{locale}")


def check_committee_page_mutations() -> None:
    """Verify the real PDF approval predicate rejects missing/overflow labels."""
    run = runpy.run_path(str(RUNNER), run_name="i18n_committee_preflight_runner")
    predicate = run["check_committee_approval_page"]
    headings = run["COMMITTEE_HEADINGS"]
    maxima = run["APPROVAL_LAST_EXAMINER"]
    for locale in LOCALES:
        for profile in ACADEMIC:
            last = maxima[profile]
            # Match the real Babel PDF typography: French ASCII apostrophe
            # in the source heading is extracted as U+2019 RIGHT SINGLE QUOTE.
            rendered_heading = headings[locale].replace("'", "’")
            lines = [rendered_heading]
            for slot in range(2, last + 1):
                lines.extend((f"Integrated Examiner {slot}", f"Integrated Institution {slot}"))
            approval = "\n".join(lines)
            good = "COVER\fTITLE\f" + approval + "\fMANUSCRIPT BODY\f"
            positive = predicate(good, profile, locale)
            if positive.get("last_examiner") != last or not positive.get("single_page"):
                raise ValueError(f"committee positive control failed: {profile}/{locale}")
            mutants = {
                "wrong_heading": good.replace(rendered_heading, "WRONG COMMITTEE", 1),
                "missing_member": good.replace(f"Integrated Examiner {last}", "", 1),
                "missing_institution": good.replace(f"Integrated Institution {last}", "", 1),
                "split_signature_across_pages": good.replace(
                    f"Integrated Institution {last}", "\fIntegrated Institution " + str(last), 1),
                "metadata_unit_leak": good + f"Integrated Hidden Unit {last}",
                "extraneous_member": good + "\fIntegrated Examiner 7\n",
                "signature_elsewhere": good.replace(
                    f"Integrated Examiner {last}", "", 1)
                    + f"Integrated Examiner {last}",
            }
            for label, damaged in mutants.items():
                if label == "extraneous_member":
                    # Require an otherwise valid but unconfigured slot 6 to be absent
                    # for all profiles with fewer than the maximum six examiners.
                    if last == 6:
                        continue
                    damaged = good + f"Integrated Examiner {last + 1}"
                if damaged == good:
                    raise ValueError(f"ineffective committee mutation: {label}/{profile}/{locale}")
                try:
                    predicate(damaged, profile, locale)
                except ValueError:
                    pass
                else:
                    raise ValueError(f"committee PDF mutation passed: {label}/{profile}/{locale}")
        if predicate("COVER\fTITLE\fMANUSCRIPT BODY\f", "scientific-article", locale)[
            "applicability"] != "not-applicable":
            raise ValueError(f"article committee applicability failed: {locale}")
        try:
            predicate("COVER\fTITLE\fIntegrated Examiner 2\f",
                      "research-project", locale)
        except ValueError:
            pass
        else:
            raise ValueError(f"inapplicable project committee passed: {locale}")


def main() -> None:
    for path in (GENERATOR, RUNNER, Path(__file__),
                 ROOT / "tests/integration/frontmatter/integrated_metadata_probe.py"):
        subprocess.run([sys.executable, "-m", "py_compile", str(path)],
                       cwd=ROOT, check=True, capture_output=True, text=True)
    with tempfile.TemporaryDirectory(prefix="abntexto-i18n-28-preflight-") as tmp:
        check(Path(tmp))
    check_list_page_mutations()
    check_role_page_mutations()
    check_committee_page_mutations()
    metadata_mutations = metadata_negative_controls()
    if metadata_mutations != 8:
        raise ValueError(f"incorrect metadata negative coverage: {metadata_mutations}")
    print("INTEGRATED-I18N-PREFLIGHT status=PASS profiles=7 locales=4 "
          "generated_tex=28 summary_inputs=56 academic_pretextual_sources=64 public_routes=PASS role_gender_mutations=PASS committee_mutations=PASS metadata_keys=53 metadata_mutations=PASS dedicated_list_mutations=PASS "
          "bibliography=5kinds components=present negatives=PASS")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"INTEGRATED-I18N-PREFLIGHT status=FAIL reason={exc}") from exc
