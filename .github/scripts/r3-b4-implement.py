#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PROFILE_MAP = {
    "tccgraduacao": "undergraduate-capstone",
    "tccespecializacao": "specialization-capstone",
    "dissertacao": "masters-thesis",
    "tese": "doctoral-thesis",
    "projeto": "research-project",
    "projetoanonimizado": "anonymized-research-project",
}

MACHINE_JSON_FILES = (
    "standards/catalog.json",
    "standards/coverage-rules-frontmatter.json",
    "standards/coverage-rules-project.json",
    "standards/frontmatter-approval-scenario.json",
    "standards/frontmatter-cover-scenario.json",
)

DIAGNOSTIC_ROOTS = (
    ROOT / "tests" / "checks",
    ROOT / "tests" / "integration",
    ROOT / "tests" / "smoke",
    ROOT / "tools",
    ROOT / "validator",
)

PHRASES = (
    ("warning ou overflow não reconhecidos", "unrecognized warning or overflow"),
    ("warning ou overflow não reconhecido", "unrecognized warning or overflow"),
    ("evidência JSON não foi gerada", "JSON evidence was not generated"),
    ("evidência de alinhamento não foi gerada", "alignment evidence was not generated"),
    ("não foi isolado tipograficamente", "was not typographically isolated"),
    ("não está em itálico", "is not italic"),
    ("não foi gerada", "was not generated"),
    ("não foi gerado", "was not generated"),
    ("não foi apresentada", "was not presented"),
    ("não foi apresentado", "was not presented"),
    ("não foi preservado", "was not preserved"),
    ("não foi localizado", "was not found"),
    ("não foi localizada", "was not found"),
    ("não localizada", "not found"),
    ("não localizado", "not found"),
    ("não reconhecidos", "unrecognized"),
    ("não reconhecido", "unrecognized"),
    ("não reconhecida", "unrecognized"),
    ("não cabe integralmente", "does not fit entirely"),
    ("não expõe", "does not expose"),
    ("não contém", "does not contain"),
    ("não está", "is not"),
    ("não foi", "was not"),
    ("entrou indevidamente", "was incorrectly included"),
    ("entrou no Sumário", "leaked into the table of contents"),
    ("ausente do Sumário", "missing from the table of contents"),
    ("ausentes do Sumário", "missing from the table of contents"),
    ("inicia antes do meio da página", "starts before the page midpoint"),
    ("recebeu título", "received a heading"),
    ("vazou no projeto anonimizado", "leaked into the anonymized research project"),
    ("usou a IES no lugar da entidade de submissão", "used the institution instead of the submission entity"),
    ("item pós-textual", "back-matter item"),
    ("elemento pós-textual", "back-matter element"),
    ("conteúdo pós-textual", "back-matter content"),
    ("elemento pré-textual", "front-matter element"),
    ("folha de aprovação", "approval page"),
    ("folha de rosto", "title page"),
    ("ficha catalográfica", "catalog card"),
    ("nota de rodapé", "footnote"),
    ("notas de rodapé", "footnotes"),
    ("líder pontilhado espaçado", "spaced dotted leader"),
    ("líder pontilhado", "dotted leader"),
    ("citação direta curta", "short direct quotation"),
    ("citação direta", "direct quotation"),
    ("citação indireta", "indirect citation"),
    ("fonte externa", "external source"),
    ("fonte consultada", "consulted source"),
    ("fontes documentais", "documentary sources"),
    ("trabalho multivolume", "multi-volume work"),
    ("trabalhos multivolume", "multi-volume works"),
    ("geometria de objetos", "object geometry"),
    ("geometria vetorial", "vector geometry"),
    ("hierarquia de seções", "section hierarchy"),
    ("indicativos de seção", "section indicators"),
    ("títulos de seção", "section headings"),
    ("seção primária", "primary section"),
    ("espaçamento de subseção", "subsection spacing"),
    ("layout de referências", "reference layout"),
    ("espaçamento das referências", "reference spacing"),
    ("sistema de citações UFC", "UFC citation system"),
    ("sistema autor-data UFC", "UFC author-date system"),
    ("página e margens", "page and margins"),
    ("geometria da paginação", "pagination geometry"),
    ("tipografia de tabela", "table typography"),
    ("equação destacada", "displayed equation"),
    ("numeração de algoritmos", "algorithm numbering"),
    ("matemática e equações", "mathematics and equations"),
    ("listas opcionais", "optional lists"),
    ("lista de objeto", "object list"),
    ("lista de objetos", "object list"),
    ("lista de figuras", "list of figures"),
    ("lista de tabelas", "list of tables"),
    ("lista de quadros", "list of frames"),
    ("lista de gráficos", "list of charts"),
    ("lista de códigos", "list of code listings"),
    ("lista unificada", "unified list"),
    ("início em anverso", "recto start"),
    ("início de seção primária em anverso", "primary-section recto start"),
    ("recuo suspenso", "hanging indent"),
    ("centralização", "centering"),
    ("atribuição de fonte", "source attribution"),
    ("apêndice/anexo", "appendix/annex"),
    ("índice/glossário", "index/glossary"),
    ("resumo/abstract", "summary/abstract"),
    ("dedicatória e epígrafes", "dedication and epigraphs"),
    ("alinhamento de dedicatória e epígrafes", "dedication and epigraph alignment"),
    ("apresentação textual", "text presentation"),
    ("orientação CAPES", "CAPES guidance"),
    ("tipografia e geometria", "typography and geometry"),
    ("tipografia de código/algoritmo", "code/algorithm typography"),
    ("tipografia de código e algoritmos", "code and algorithm typography"),
    ("citações e referências", "citations and references"),
    ("política matemática", "mathematics policy"),
    ("política", "policy"),
)

WORDS = {
    "Auditoria": "Audit",
    "auditoria": "audit",
    "Validando": "Validating",
    "validando": "validating",
    "falhou": "failed",
    "Falhou": "Failed",
    "concluído": "completed",
    "concluída": "completed",
    "ausente": "missing",
    "ausentes": "missing",
    "incorreto": "incorrect",
    "incorreta": "incorrect",
    "desconhecido": "unknown",
    "desconhecida": "unknown",
    "evidência": "evidence",
    "página": "page",
    "páginas": "pages",
    "palavra": "word",
    "rótulo": "label",
    "rótulos": "labels",
    "descrição": "description",
    "descrições": "descriptions",
    "coluna": "column",
    "desalinhada": "misaligned",
    "desalinhado": "misaligned",
    "verticalmente": "vertically",
    "marcador": "marker",
    "marcadores": "markers",
    "métrica": "metric",
    "métricas": "metrics",
    "comando": "command",
    "comandos": "commands",
    "arquivo": "file",
    "arquivos": "files",
    "conteúdo": "content",
    "elemento": "element",
    "elementos": "elements",
    "título": "heading",
    "títulos": "headings",
    "fonte": "source",
    "fontes": "sources",
    "referência": "reference",
    "referências": "references",
    "citação": "citation",
    "citações": "citations",
    "direta": "direct",
    "indireta": "indirect",
    "Sumário": "table of contents",
    "sumário": "table of contents",
    "capa": "cover",
    "autor": "author",
    "orientador": "advisor",
    "identificador": "identifier",
    "tabela": "table",
    "tabelas": "tables",
    "figura": "figure",
    "figuras": "figures",
    "quadro": "frame",
    "quadros": "frames",
    "gráfico": "chart",
    "gráficos": "charts",
    "código": "code",
    "algoritmo": "algorithm",
    "algoritmos": "algorithms",
    "lista": "list",
    "listas": "lists",
    "ilustração": "illustration",
    "ilustrações": "illustrations",
    "nota": "note",
    "espaçamento": "spacing",
    "seção": "section",
    "seções": "sections",
    "perfil": "profile",
    "perfis": "profiles",
    "matriz": "matrix",
    "trabalho": "work",
    "obrigatório": "required",
    "obrigatória": "required",
    "esperado": "expected",
    "esperada": "expected",
    "encontrados": "found",
    "encontrado": "found",
    "encontrada": "found",
    "fotografia": "photograph",
    "fotografias": "photographs",
    "licenciada": "licensed",
    "navegação": "navigation",
    "bloco": "block",
    "entrada": "entry",
    "entradas": "entries",
    "caixa": "case",
    "preservada": "preserved",
    "convertida": "converted",
    "alta": "uppercase",
    "primeira": "first",
    "primeiro": "first",
    "poucas": "too few",
    "paginação": "pagination",
    "geométrico": "geometric",
    "geométrica": "geometric",
    "apêndice": "appendix",
    "anexo": "annex",
    "índice": "index",
    "glossário": "glossary",
    "agradecimentos": "acknowledgements",
    "dedicatória": "dedication",
    "epígrafe": "epigraph",
    "resumo": "summary",
    "anverso": "recto",
    "brasão": "coat of arms",
    "carregado": "loaded",
    "padrão": "default",
    "projeto": "research project",
    "anonimizado": "anonymized",
    "obrigatória": "required",
    "obrigatórias": "required",
    "indevido": "invalid",
    "regressão": "regression",
    "julgamento": "judgment",
    "opcional": "optional",
    "preservado": "preserved",
    "complementar": "supplemental",
    "apresentada": "presented",
    "forma": "form",
    "autor-data": "author-date",
    "extração": "extraction",
    "texto": "text",
    "fontes": "fonts",
    "estrutura": "structure",
    "fixture": "fixture",
    "contém": "contains",
    "estão": "are",
    "está": "is",
}

DIAGNOSTIC_MARKERS = (
    "echo ",
    "printf ",
    "raise SystemExit",
    "fail_semantic",
    "errors.append",
    "print(",
    "ArgumentParser(",
    "help=",
    "description=",
    "throw new Error",
    "console.",
)


def replace_exact_json_values(value):
    if isinstance(value, dict):
        return {key: replace_exact_json_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_exact_json_values(item) for item in value]
    if isinstance(value, str):
        return PROFILE_MAP.get(value, value)
    return value


def update_json(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload = replace_exact_json_values(payload)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def diagnostic_or_comment(line: str) -> bool:
    stripped = line.lstrip()
    if stripped.startswith("#!"):
        return False
    if stripped.startswith(("#", "//", "/*", "* ")):
        return True
    return any(marker in line for marker in DIAGNOSTIC_MARKERS)


def translate_text(text: str) -> str:
    for source, target in PHRASES:
        text = text.replace(source, target)
    for source, target in sorted(WORDS.items(), key=lambda item: len(item[0]), reverse=True):
        text = re.sub(rf"(?<![\w-]){re.escape(source)}(?![\w-])", target, text, flags=re.IGNORECASE if source[0].islower() else 0)
    text = text.replace("Gate de ", "Gate for ").replace("Gate da ", "Gate for ").replace("Gate do ", "Gate for ")
    text = text.replace("Audit de ", "Audit for ").replace("Audit da ", "Audit for ").replace("Audit do ", "Audit for ")
    text = text.replace(" de front matter", " for front matter")
    text = text.replace(" para ", " for ")
    return text


def translate_engineering_sources() -> None:
    suffixes = {".py", ".sh", ".js", ".yml", ".yaml", ".ps1"}
    for root in DIAGNOSTIC_ROOTS:
        if not root.exists():
            continue
        for path in sorted(item for item in root.rglob("*") if item.is_file() and item.suffix in suffixes):
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            changed = False
            output: list[str] = []
            for line in lines:
                if diagnostic_or_comment(line):
                    translated = translate_text(line)
                    changed = changed or translated != line
                    line = translated
                output.append(line)
            if changed:
                path.write_text("".join(output), encoding="utf-8")


def update_machine_consumers() -> None:
    approval = ROOT / "tests/integration/frontmatter-approval-evidence.sh"
    text = approval.read_text(encoding="utf-8")
    text = text.replace(
        'academic_profiles="tccgraduacao tccespecializacao dissertacao tese"',
        'academic_profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis"',
    )
    text = text.replace(
        'suppressed_profiles="projeto projetoanonimizado"',
        'suppressed_profiles="research-project anonymized-research-project"',
    )
    case_pattern = re.compile(
        r"  case \"\$profile\" in\n"
        r"    tccgraduacao\) document_type=\"undergraduate-capstone\" ;;\n"
        r"    tccespecializacao\) document_type=\"specialization-capstone\" ;;\n"
        r"    dissertacao\) document_type=\"masters-thesis\" ;;\n"
        r"    tese\) document_type=\"doctoral-thesis\" ;;\n"
        r"    projeto\) document_type=\"research-project\" ;;\n"
        r"    projetoanonimizado\) document_type=\"anonymized-research-project\" ;;\n"
        r"    \*\).*?\n"
        r"      ;;\n"
        r"  esac\n",
        flags=re.DOTALL,
    )
    text, count = case_pattern.subn('  document_type="$profile"\n', text)
    if count != 1:
        raise SystemExit(f"approval profile mapping rewrite count={count}")
    approval.write_text(text, encoding="utf-8")

    title_page = ROOT / "tests/checks/normative_frontmatter_title_page.py"
    text = title_page.read_text(encoding="utf-8")
    text = text.replace('"projeto": {"title_page": project_title_index, "present": project_present}', '"research-project": {"title_page": project_title_index, "present": project_present}')
    text = text.replace('"projetoanonimizado": {"title_page": anon_title_index, "present": anon_present}', '"anonymized-research-project": {"title_page": anon_title_index, "present": anon_present}')
    title_page.write_text(text, encoding="utf-8")

    project_rule = ROOT / "standards/coverage-rules-project.json"
    text = project_rule.read_text(encoding="utf-8")
    text = text.replace("perfil projetoanonimizado", "perfil anonymized-research-project")
    project_rule.write_text(text, encoding="utf-8")

    research = ROOT / "tests/integration/research-project.sh"
    text = research.read_text(encoding="utf-8")
    for source, target in (
        ("projeto-15287", "research-project-15287"),
        ("projeto-sem-capa", "research-project-without-cover"),
        ("pretextuais-projeto-anonimo", "frontmatter-anonymized-research-project"),
    ):
        text = text.replace(source, target)
    research.write_text(text, encoding="utf-8")

    scenario = ROOT / "standards/research-project-structure-final-pdf-scenario.json"
    payload = json.loads(scenario.read_text(encoding="utf-8"))
    if payload.get("pdf") == "projeto-15287.pdf":
        payload["pdf"] = "research-project-15287.pdf"
    scenario.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remove_closed_contracts() -> None:
    canonical = ROOT / "tests/checks/canonical_identity.py"
    text = canonical.read_text(encoding="utf-8")
    text = text.replace('    "release/v3-path-migration.json",\n', '')
    text = text.replace('    "release/v3-test-migration.json",\n', '')
    canonical.write_text(text, encoding="utf-8")

    repository = ROOT / "tests/checks/repository_contract.py"
    text = repository.read_text(encoding="utf-8")
    text = text.replace('    "release/v3-path-migration.json",\n', '')
    text = text.replace('    "release/v3-test-migration.json",\n', '')
    repository.write_text(text, encoding="utf-8")

    for relative in ("release/v3-test-migration.json", "release/v3-path-migration.json"):
        path = ROOT / relative
        if path.exists():
            path.unlink()


def add_language_checker() -> None:
    checker = ROOT / "tests/checks/engineering_language.py"
    checker.write_text('''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXECUTABLE_ROOTS = ("tests/checks/", "tests/integration/", "tests/smoke/", "tools/", "validator/", ".github/workflows/")
SOURCE_SUFFIXES = {".py", ".sh", ".js", ".yml", ".yaml", ".ps1"}
DIAGNOSTIC_MARKERS = ("echo ", "printf ", "raise SystemExit", "fail_semantic", "errors.append", "print(", "ArgumentParser(", "help=", "description=", "throw new Error", "console.")
PORTUGUESE_TECHNICAL_TERMS = re.compile(r"\\b(?:auditoria|validando|falhou|conclu[ií]d[oa]|ausente(?:s)?|incorret[oa]|desconhecid[oa]|evid[eê]ncia|p[aá]gina(?:s)?|r[oó]tulo(?:s)?|descri[cç][aã]o|desalinhad[oa]|marcador(?:es)?|m[eé]trica(?:s)?|comando(?:s)?|conte[uú]do|t[ií]tulo(?:s)?|refer[eê]ncia(?:s)?|cita[cç][aã]o|espa[cç]amento|se[cç][aã]o|perfil(?:s)?|sum[aá]rio|capa|orientador|identificador|navega[cç][aã]o|fotografia(?:s)?|ap[eê]ndice|anexo|[ií]ndice|gloss[aá]rio|dedicat[oó]ria|ep[ií]grafe|agradecimentos|bras[aã]o)\\b", re.IGNORECASE)
RETIRED_PROFILE_IDS = re.compile(r"(?<![A-Za-z0-9_-])(?:tccgraduacao|tccespecializacao|dissertacao|tese|projetoanonimizado|projeto)(?![A-Za-z0-9_-])")
MACHINE_FILES = (
    "standards/catalog.json",
    "standards/coverage-rules-frontmatter.json",
    "standards/coverage-rules-project.json",
    "standards/frontmatter-approval-scenario.json",
    "standards/frontmatter-cover-scenario.json",
    "tests/checks/normative_frontmatter_title_page.py",
    "tests/integration/frontmatter-approval-evidence.sh",
)
ACADEMIC_LITERAL_ALLOWLIST = ("SUMÁRIO", "REFERÊNCIAS", "APÊNDICE", "ANEXO", "ÍNDICE REMISSIVO")


def tracked() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / item.decode() for item in output.split(b"\\0") if item]


def is_comment_or_diagnostic(line: str) -> bool:
    stripped = line.lstrip()
    if stripped.startswith("#!"):
        return False
    if stripped.startswith(("#", "//", "/*", "* ")):
        return True
    return any(marker in line for marker in DIAGNOSTIC_MARKERS)


def normalized_diagnostic(line: str) -> str:
    result = line
    for literal in ACADEMIC_LITERAL_ALLOWLIST:
        result = result.replace(literal, "")
    return result


def audit() -> list[str]:
    errors: list[str] = []
    for path in tracked():
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix not in SOURCE_SUFFIXES or not rel.startswith(EXECUTABLE_ROOTS):
            continue
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if is_comment_or_diagnostic(line) and PORTUGUESE_TECHNICAL_TERMS.search(normalized_diagnostic(line)):
                errors.append(f"{rel}:{number}: Portuguese project-owned engineering text: {line.strip()}")
    for rel in MACHINE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if RETIRED_PROFILE_IDS.search(line):
                errors.append(f"{rel}:{number}: retired Portuguese technical profile identifier: {line.strip()}")
    api = ROOT / "release/v3-api-migration.json"
    if not api.is_file():
        errors.append("release/v3-api-migration.json: live migration contract is missing")
    for removed in (ROOT / "release/v3-test-migration.json", ROOT / "release/v3-path-migration.json"):
        if removed.exists():
            errors.append(f"{removed.relative_to(ROOT)}: closed unconsumed migration contract remains active")
    for consumer in ("tests/checks/v3_api_residual.py", "tests/checks/profile_matrix_contract.py"):
        if "release/v3-api-migration.json" not in (ROOT / consumer).read_text(encoding="utf-8"):
            errors.append(f"{consumer}: expected live API migration contract consumer is missing")
    return errors


def self_test() -> None:
    assert PORTUGUESE_TECHNICAL_TERMS.search("echo 'Auditoria falhou: evidência ausente.'")
    assert not PORTUGUESE_TECHNICAL_TERMS.search("echo 'Audit failed: evidence is missing.'")
    assert not PORTUGUESE_TECHNICAL_TERMS.search(normalized_diagnostic("echo 'Expected rendered heading: SUMÁRIO'"))
    assert RETIRED_PROFILE_IDS.search('"profile": "tccgraduacao"')
    assert not RETIRED_PROFILE_IDS.search('"profile": "undergraduate-capstone"')
    normative = json.loads('{"requirement":"A capa é elemento obrigatório."}')
    assert "obrigatório" in normative["requirement"]
    print("ENGINEERING-LANGUAGE-SELFTEST status=PASS cases=6")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enforce project-owned engineering language boundaries.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    errors = audit()
    if errors:
        print("Engineering language contract failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(f"Engineering language contract failed with {len(errors)} issue(s).")
    print("ENGINEERING-LANGUAGE-EVIDENCE status=PASS portuguese_technical_diagnostics=0 retired_profile_ids=0 closed_unconsumed_contracts=0 live_api_contract_consumers=2")


if __name__ == "__main__":
    main()
''', encoding="utf-8")

    static = ROOT / "tests/static.py"
    text = static.read_text(encoding="utf-8")
    anchor = '    "tests/checks/repository_contract.py",\n'
    if '"tests/checks/engineering_language.py"' not in text:
        text = text.replace(anchor, anchor + '    "tests/checks/engineering_language.py",\n')
    static.write_text(text, encoding="utf-8")


def main() -> None:
    for relative in MACHINE_JSON_FILES:
        update_json(ROOT / relative)
    update_machine_consumers()
    remove_closed_contracts()
    translate_engineering_sources()
    add_language_checker()

    # The checker itself must not inherit translated policy strings from the sweep.
    print("R3-B4 implementation applied.")


if __name__ == "__main__":
    main()
