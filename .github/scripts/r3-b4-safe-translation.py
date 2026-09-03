#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "tests/checks/engineering_language.py"

checker_text = CHECKER.read_text(encoding="utf-8")

subprocess.run(
    [
        "git", "checkout", "origin/main", "--",
        "tests/checks", "tests/integration", "tests/smoke", "tools", "validator", "tests/static.py",
    ],
    cwd=ROOT,
    check=True,
)
CHECKER.write_text(checker_text, encoding="utf-8")

# Re-apply the B4 source-level machine changes after restoring executables.
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

static = ROOT / "tests/static.py"
text = static.read_text(encoding="utf-8")
anchor = '    "tests/checks/repository_contract.py",\n'
text = text.replace(anchor, anchor + '    "tests/checks/engineering_language.py",\n')
static.write_text(text, encoding="utf-8")

title_page = ROOT / "tests/checks/normative_frontmatter_title_page.py"
text = title_page.read_text(encoding="utf-8")
text = text.replace('"projeto": {"title_page": project_title_index, "present": project_present}', '"research-project": {"title_page": project_title_index, "present": project_present}')
text = text.replace('"projetoanonimizado": {"title_page": anon_title_index, "present": anon_present}', '"anonymized-research-project": {"title_page": anon_title_index, "present": anon_present}')
title_page.write_text(text, encoding="utf-8")

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
    raise SystemExit(f"approval profile rewrite count={count}")
approval.write_text(text, encoding="utf-8")

research = ROOT / "tests/integration/research-project.sh"
text = research.read_text(encoding="utf-8")
for source, target in (
    ("projeto-15287", "research-project-15287"),
    ("projeto-sem-capa", "research-project-without-cover"),
    ("pretextuais-projeto-anonimo", "frontmatter-anonymized-research-project"),
):
    text = text.replace(source, target)
research.write_text(text, encoding="utf-8")

PORTUGUESE_SIGNAL = re.compile(
    r"\b(?:auditoria|validando|falhou|conclu[ií]d[oa]|ausente(?:s)?|incorret[oa]|desconhecid[oa]|evid[eê]ncia|"
    r"p[aá]gina(?:s)?|r[oó]tulo(?:s)?|descri[cç][aã]o|desalinhad[oa]|marcador(?:es)?|m[eé]trica(?:s)?|"
    r"comando(?:s)?|conte[uú]do|t[ií]tulo(?:s)?|refer[eê]ncia(?:s)?|cita[cç][aã]o|espa[cç]amento|se[cç][aã]o|"
    r"perfil(?:s)?|sum[aá]rio|capa|orientador|identificador|navega[cç][aã]o|fotografia(?:s)?|ap[eê]ndice|anexo|"
    r"[ií]ndice|gloss[aá]rio|dedicat[oó]ria|ep[ií]grafe|agradecimentos|bras[aã]o)\b",
    re.IGNORECASE,
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
    ("não localizada", "not found"),
    ("não localizado", "not found"),
    ("não reconhecidos", "unrecognized"),
    ("não reconhecido", "unrecognized"),
    ("não reconhecida", "unrecognized"),
    ("não cabe integralmente", "does not fit entirely"),
    ("não está", "is not"),
    ("não foi", "was not"),
    ("entrou indevidamente", "was incorrectly included"),
    ("entrou no Sumário", "leaked into the table of contents"),
    ("ausente do Sumário", "missing from the table of contents"),
    ("ausentes do Sumário", "missing from the table of contents"),
    ("inicia antes do meio da página", "starts before the page midpoint"),
    ("recebeu título", "received a heading"),
    ("vazou no projeto anonimizado", "leaked into the anonymized research project"),
    ("folha de aprovação", "approval page"),
    ("folha de rosto", "title page"),
    ("ficha catalográfica", "catalog card"),
    ("notas de rodapé", "footnotes"),
    ("nota de rodapé", "footnote"),
    ("líder pontilhado espaçado", "spaced dotted leader"),
    ("líder pontilhado", "dotted leader"),
    ("citação direta curta", "short direct quotation"),
    ("citação direta", "direct quotation"),
    ("citação indireta", "indirect citation"),
    ("fonte externa", "external source"),
    ("fontes documentais", "documentary sources"),
    ("trabalho multivolume", "multi-volume work"),
    ("trabalhos multivolume", "multi-volume works"),
    ("geometria de objetos", "object geometry"),
    ("geometria vetorial", "vector geometry"),
    ("hierarquia de seções", "section hierarchy"),
    ("indicativos de seção", "section indicators"),
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
    ("lista de figuras", "list of figures"),
    ("lista de tabelas", "list of tables"),
    ("lista de quadros", "list of frames"),
    ("lista de gráficos", "list of charts"),
    ("lista de códigos", "list of code listings"),
    ("lista unificada", "unified list"),
    ("apêndice/anexo", "appendix/annex"),
    ("índice/glossário", "index/glossary"),
    ("resumo/abstract", "summary/abstract"),
    ("dedicatória e epígrafes", "dedication and epigraphs"),
    ("orientação CAPES", "CAPES guidance"),
    ("tipografia de código/algoritmo", "code/algorithm typography"),
)

WORDS = {
    "Auditoria": "Audit", "auditoria": "audit", "Validando": "Validating", "validando": "validating",
    "falhou": "failed", "Falhou": "Failed", "concluído": "completed", "concluída": "completed",
    "ausente": "missing", "ausentes": "missing", "incorreto": "incorrect", "incorreta": "incorrect",
    "desconhecido": "unknown", "desconhecida": "unknown", "evidência": "evidence", "página": "page",
    "páginas": "pages", "palavra": "word", "rótulo": "label", "rótulos": "labels", "descrição": "description",
    "descrições": "descriptions", "coluna": "column", "desalinhada": "misaligned", "desalinhado": "misaligned",
    "verticalmente": "vertically", "marcador": "marker", "marcadores": "markers", "métrica": "metric", "métricas": "metrics",
    "comando": "command", "comandos": "commands", "arquivo": "file", "arquivos": "files", "conteúdo": "content",
    "elemento": "element", "elementos": "elements", "título": "heading", "títulos": "headings", "fonte": "source", "fontes": "sources",
    "referência": "reference", "referências": "references", "citação": "citation", "citações": "citations", "Sumário": "table of contents",
    "sumário": "table of contents", "capa": "cover", "autor": "author", "orientador": "advisor", "identificador": "identifier",
    "tabela": "table", "tabelas": "tables", "figura": "figure", "figuras": "figures", "quadro": "frame", "quadros": "frames",
    "gráfico": "chart", "gráficos": "charts", "código": "code", "algoritmo": "algorithm", "algoritmos": "algorithms",
    "lista": "list", "listas": "lists", "ilustração": "illustration", "ilustrações": "illustrations", "nota": "note",
    "espaçamento": "spacing", "seção": "section", "seções": "sections", "perfil": "profile", "perfis": "profiles", "matriz": "matrix",
    "trabalho": "work", "obrigatório": "required", "obrigatória": "required", "obrigatórias": "required", "esperado": "expected",
    "esperada": "expected", "encontrados": "found", "encontrado": "found", "encontrada": "found", "fotografia": "photograph",
    "fotografias": "photographs", "navegação": "navigation", "bloco": "block", "entrada": "entry", "entradas": "entries",
    "caixa": "case", "preservada": "preserved", "preservado": "preserved", "convertida": "converted", "alta": "uppercase",
    "primeira": "first", "primeiro": "first", "segundo": "second", "poucas": "too few", "paginação": "pagination",
    "geométrico": "geometric", "geométrica": "geometric", "apêndice": "appendix", "anexo": "annex", "índice": "index",
    "glossário": "glossary", "agradecimentos": "acknowledgements", "dedicatória": "dedication", "epígrafe": "epigraph",
    "resumo": "summary", "anverso": "recto", "brasão": "coat of arms", "carregado": "loaded", "padrão": "default",
    "projeto": "research project", "anonimizado": "anonymized", "regressão": "regression", "julgamento": "judgment",
    "opcional": "optional", "complementar": "supplemental", "apresentada": "presented", "forma": "form", "autor-data": "author-date",
    "extração": "extraction", "texto": "text", "estrutura": "structure", "contém": "contains", "estão": "are", "está": "is",
    "simples": "simple", "parentética": "parenthetical", "dois": "two", "três": "three", "autores": "authors", "autoria": "authorship",
    "anos": "years", "distintos": "distinct", "homônimo": "same-name", "simultâneos": "simultaneous", "pessoa": "person", "jurídica": "corporate",
    "sem": "without", "cidade": "city", "evento": "event", "eletrônica": "electronic", "original": "original", "sobrenome": "surname",
    "indevidamente": "incorrectly", "gerada": "generated", "gerado": "generated", "foi": "was", "foram": "were", "é": "is", "são": "are",
    "com": "with", "para": "for", "por": "by", "ou": "or", "mesmo": "same", "mesma": "same", "uma": "a", "um": "a",
}

# Function words are replaced only inside diagnostic string arguments, never in test operands.
FUNCTION_WORDS = {
    "das": "of the", "dos": "of the", "da": "of the", "do": "of the", "de": "of", "nas": "in the", "nos": "in the",
    "na": "in the", "no": "in the", "em": "in", "e": "and",
}


def translate_message(body: str) -> str:
    success = re.match(r"^Gate\s+(?:de|da|do)\s+(.+?)\s+conclu[ií]d[oa]\.?$", body, flags=re.IGNORECASE)
    if success:
        return translate_message(success.group(1)).strip().capitalize() + " gate completed."
    audit = re.match(r"^Auditoria\s+(?:de|da|do)?\s*(.+?)\s+falhou:\s*(.+)$", body, flags=re.IGNORECASE)
    if audit:
        return translate_message(audit.group(1)).strip().capitalize() + " audit failed: " + translate_message(audit.group(2)).strip()
    for source, target in PHRASES:
        body = body.replace(source, target)
    for mapping in (WORDS, FUNCTION_WORDS):
        for source, target in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
            body = re.sub(rf"(?<![\w-]){re.escape(source)}(?![\w-])", target, body, flags=re.IGNORECASE)
    return body

CALL_PATTERNS = (
    re.compile(r"(?P<prefix>\becho\s+)(?P<q>['\"])(?P<body>.*?)(?P=q)"),
    re.compile(r"(?P<prefix>\bprintf\s+)(?P<q>['\"])(?P<body>.*?)(?P=q)"),
    re.compile(r"(?P<prefix>\bfail_semantic\s+)(?P<q>['\"])(?P<body>.*?)(?P=q)"),
    re.compile(r"(?P<prefix>raise\s+SystemExit\(f?)(?P<q>['\"])(?P<body>.*?)(?P=q)"),
    re.compile(r"(?P<prefix>\bprint\(f?)(?P<q>['\"])(?P<body>.*?)(?P=q)"),
    re.compile(r"(?P<prefix>errors\.append\(f?)(?P<q>['\"])(?P<body>.*?)(?P=q)"),
)


def translate_calls(line: str) -> str:
    for pattern in CALL_PATTERNS:
        def repl(match: re.Match[str]) -> str:
            body = match.group("body")
            if not PORTUGUESE_SIGNAL.search(body):
                return match.group(0)
            translated = translate_message(body)
            return match.group("prefix") + match.group("q") + translated + match.group("q")
        line = pattern.sub(repl, line)
    stripped = line.lstrip()
    if stripped.startswith(("#", "//", "/*", "* ")) and PORTUGUESE_SIGNAL.search(line):
        prefix_len = len(line) - len(stripped)
        marker = "#" if stripped.startswith("#") else "//" if stripped.startswith("//") else "*"
        if marker == "#":
            payload = stripped[1:]
            line = line[:prefix_len] + "#" + translate_message(payload)
        elif marker == "//":
            payload = stripped[2:]
            line = line[:prefix_len] + "//" + translate_message(payload)
    return line

roots = [ROOT / "tests/checks", ROOT / "tests/integration", ROOT / "tests/smoke", ROOT / "tools", ROOT / "validator"]
suffixes = {".py", ".sh", ".js", ".yml", ".yaml", ".ps1"}
for root in roots:
    for path in sorted(item for item in root.rglob("*") if item.is_file() and item.suffix in suffixes):
        if path == CHECKER:
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        translated = [translate_calls(line) for line in lines]
        if translated != lines:
            path.write_text("".join(translated), encoding="utf-8")

print("R3-B4 safe diagnostic translation applied without modifying test operands.")
