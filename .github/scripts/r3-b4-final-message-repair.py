#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def apply(relative: str, replacements: dict[str, str]) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


# The checker must not treat the English word "fallback" as Portuguese.
checker = ROOT / "tests/checks/engineering_language.py"
text = checker.read_text(encoding="utf-8").replace("|fallback|apareceu", "|apareceu")
checker.write_text(text, encoding="utf-8")

apply(
    "tests/checks/frontmatter_definition_alignment.py",
    {
        "Front matter validation falhou: rótulo não localizado para {description_first_word}.": "Front matter validation failed: label not found for {description_first_word}.",
        "Front matter validation falhou: rótulo e descrição estão verticalmente desalinhados ": "Front matter validation failed: label and description are vertically misaligned ",
        "Front matter validation falhou: coluna de rótulos desalinhada na lista de {label}: ": "Front matter validation failed: label column is misaligned in the {label} list: ",
        "Front matter validation falhou: coluna de descrições desalinhada na lista de {label}: ": "Front matter validation failed: description column is misaligned in the {label} list: ",
    },
)

apply(
    "tests/integration/backmatter.sh",
    {
        "ordem pós-textual incorrect": "incorrect back-matter order",
        "estrutura baseada em capítulo reapareceu.": "chapter-based structure reappeared.",
    },
)

apply(
    "tests/integration/bibliography.sh",
    {
        "Contexto das caixas excedentes:": "Context for overfull boxes:",
        "Preflight failed: fixture bibliográfica contains warnings or overflow unrecognized.": "Preflight failed: bibliography fixture contains unrecognized warnings or overflow.",
        "citation author-date simple incorrect.": "Simple author-date citation is incorrect.",
        "citation in case uppercase incompatível with NBR 10520:2023.": "Uppercase author-date citation is incompatible with NBR 10520:2023.",
        "citation parenthetical of two authors incorrect.": "Two-author parenthetical citation is incorrect.",
        "citation textual of two authors incorrect.": "Two-author narrative citation is incorrect.",
        "citation of three authors incorrect.": "Three-author citation is incorrect.",
        "citation with et al. incorrect.": "Citation using et al. is incorrect.",
        "Desambiguação of same author/ano incorrect.": "Same-author/year disambiguation is incorrect.",
        "Ordem cronológica of same authorship incorrect.": "Chronological ordering for the same authorship is incorrect.",
        "citation textual of same authorship in years distinct incorrect.": "Narrative citation for the same authorship across distinct years is incorrect.",
        "Desambiguação of the first author same-name incorrect.": "Disambiguation of the first same-name author is incorrect.",
        "Desambiguação of the second author same-name incorrect.": "Disambiguation of the second same-name author is incorrect.",
        "form textual of the first author same-name incorrect.": "Narrative form for the first same-name author is incorrect.",
        "form textual of the second author same-name incorrect.": "Narrative form for the second same-name author is incorrect.",
        "Ordenação of authors simultaneous incorrect.": "Ordering of simultaneous authors is incorrect.",
        "citation of person corporate incorrect.": "Corporate-author citation is incorrect.",
        "citation of heading of a word incorrect.": "One-word title citation is incorrect.",
        "citation of heading without authorship incorrect.": "Title citation without authorship is incorrect.",
        "citation of heading iniciado by artigo incorrect.": "Title citation beginning with an article is incorrect.",
        "citation of citation incorrect.": "Secondary citation is incorrect.",
        "citation of citation textual incorrect.": "Narrative secondary citation is incorrect.",
        "heading of references missing.": "References heading is missing.",
        "Entrada bibliográfica não preserva sobrenome em caixa alta.": "Bibliographic entry does not preserve the uppercase surname.",
        "source consultada in the apud missing of the references.": "Consulted source in the apud citation is missing from the references.",
        "source original of the apud was incorrectly included in the references.": "Original source from the apud citation was incorrectly included in the references.",
        "E-location missing of the reference electronic.": "E-location is missing from the electronic reference.",
        "DOI missing of the reference electronic.": "DOI is missing from the electronic reference.",
        "reference of event missing.": "Event reference is missing.",
        "Evento sem cidade recebeu sine loco indevidamente.": "Event without a city incorrectly received a sine loco marker.",
        "references missing from the table of contents.": "References are missing from the table of contents.",
    },
)

apply(
    "tests/integration/catalog-card.sh",
    {
        "$job: contador inesperado antes da ficha.": "$job: unexpected page counter before the catalog card.",
        "$job: rota da ficha alterou indevidamente a contagem lógica.": "$job: catalog-card route incorrectly changed the logical page count.",
        "f'{job}: ficha habilitada não ocupa o verso físico da folha de rosto.'": "f'{job}: enabled catalog card does not occupy the physical verso of the title page.'",
        "f'{job}: texto posterior à ficha não iniciou no anverso físico seguinte.'": "f'{job}: text after the catalog card did not start on the next physical recto.'",
        "f'{job}: texto em página física inesperada com ficha desabilitada; '": "f'{job}: text is on an unexpected physical page with the catalog card disabled; '",
        "f'esperado índice {expected_physical_index}, obtido {text_pages[0]}.'": "f'expected index {expected_physical_index}, measured {text_pages[0]}.'",
        "f'{job}: double-sided mode without a catalog card deve preservar verso físico em branco antes do texto.'": "f'{job}: double-sided mode without a catalog card must preserve a blank physical verso before the text.'",
    },
)

apply(
    "tests/integration/code-typography.sh",
    {
        "f'{name}: esperado 12 pt nominal, obtido {actual:.4f}'": "f'{name}: expected nominal size 12 pt, measured {actual:.4f}'",
        "f\"{marker}: conteúdo invade margem direita: \"": "f\"{marker}: content crosses the right margin: \"",
        "f\"x={box['x1']:.2f}, limite={A4_WIDTH - RIGHT:.2f}\"": "f\"x={box['x1']:.2f}, limit={A4_WIDTH - RIGHT:.2f}\"",
    },
)

apply(
    "tests/integration/documentary-source.sh",
    {
        "$job: Biber reportou warning/error.": "$job: Biber reported a warning/error.",
        "reference bibliográfica própria não permaneceu dentro of the annex.": "The annex-specific bibliographic reference did not remain inside the annex.",
    },
)

apply(
    "tests/integration/duplex-frontmatter.sh",
    {
        "f'{job}: element deveria iniciar in the recto, mas apareceu in the page física {page}: {marker}'": "f'{job}: element should start on a recto but appeared on physical page {page}: {marker}'",
    },
)

apply(
    "tests/integration/font-poc.sh",
    {
        "POC fontes: $pdf contém família textual de fallback inesperada.": "Font POC: $pdf contains an unexpected fallback text family.",
    },
)

apply(
    "tests/integration/frontmatter.sh",
    {
        "f'Front matter validation falhou: {label} inicia antes do meio da página: '": "f'Front matter validation failed: {label} starts before the page midpoint: '",
        "f'y={first_y:.2f}, meio={midpoint:.2f}'": "f'y={first_y:.2f}, midpoint={midpoint:.2f}'",
        "identifier anonymized missing.": "anonymized identifier is missing.",
        "heading front matter missing or incorrect": "front-matter heading is missing or incorrect",
        "element front matter leaked into the table of contents": "front-matter element leaked into the table of contents",
        "section textual missing from the table of contents": "textual section is missing from the table of contents",
    },
)

apply(
    "tests/integration/math.sh",
    {
        "$job: fonte matemática esperada não identificada: $expected": "$job: expected mathematics font was not identified: $expected",
        "f'número da equação não está alinhado à direita: '": "f'equation number is not right-aligned: '",
        "f'esperado xMax≈{expected_right:.2f}, obtido {rightmost[2]:.2f} ({rightmost[0]!r})'": "f'expected xMax≈{expected_right:.2f}, measured {rightmost[2]:.2f} ({rightmost[0]!r})'",
    },
)

apply(
    "tests/integration/multivolume.sh",
    {
        "$job: folha de rosto não avançou a sequência 101 → 102.": "$job: title page did not advance the sequence 101 → 102.",
    },
)

apply(
    "tests/integration/object-geometry.sh",
    {
        "f'{name}: esperado {expected:.4f}, obtido {actual:.4f}'": "f'{name}: expected {expected:.4f}, measured {actual:.4f}'",
    },
)

apply(
    "tests/integration/object.sh",
    {
        "Contexto das caixas excedentes:": "Context for overfull boxes:",
        "f'Preflight falhou: líder pontilhado ausente na lista de objeto: {marker}'": "f'Preflight failed: dotted leader is missing from the object list: {marker}'",
    },
)

apply(
    "tests/integration/profile-matrix.sh",
    {
        "Validating profile completo $profile with $engine...": "Validating complete profile $profile with $engine...",
        "Preflight failed: Biber reportou warning/error in $profile/$engine.": "Preflight failed: Biber reported a warning/error in $profile/$engine.",
        "profile $profile/$engine: declaração PDF/A part 2 missing.": "Profile $profile/$engine: PDF/A part 2 declaration is missing.",
        "profile $profile/$engine: declaração PDF/A-2b missing.": "Profile $profile/$engine: PDF/A-2b declaration is missing.",
        "profile $profile/$engine: page não is A4.": "Profile $profile/$engine: page is not A4.",
        "profile $profile/$engine: documento completo gerou apenas ${pages:-0} pages.": "Profile $profile/$engine: complete document generated only ${pages:-0} pages.",
        "f'profile {profile}: content semântico missing: {marker}'": "f'Profile {profile}: semantic content is missing: {marker}'",
        "f'profile {profile}: content estrutural missing: {marker}'": "f'Profile {profile}: structural content is missing: {marker}'",
        "f'profile {profile}: structure of capítulo reapareceu.'": "f'Profile {profile}: chapter-based structure reappeared.'",
        "f'profile anonymized vazou dado protegido: {secret}'": "f'Anonymized profile leaked protected data: {secret}'",
        "f'profile {profile}: author expected missing.'": "f'Profile {profile}: expected author is missing.'",
        "f'profile {profile}: element of work acadêmico apareceu incorrectly: {forbidden}'": "f'Profile {profile}: academic-work element appeared incorrectly: {forbidden}'",
        "profile $profile/$engine: Introdução missing from the table of contents.": "Profile $profile/$engine: Introduction is missing from the table of contents.",
        "profile $profile/$engine: Metodologia missing from the table of contents.": "Profile $profile/$engine: Methodology is missing from the table of contents.",
        "profile $profile/$engine: entry anômala with asterisco in the table of contents.": "Profile $profile/$engine: anomalous asterisk entry found in the table of contents.",
        "Matrix completa of profiles gate completed.": "Complete profile matrix gate completed.",
    },
)

apply(
    "tests/integration/reference-corpus.sh",
    {
        "file of navigation missing": "navigation file is missing",
        "photograph licenciada missing": "licensed photograph is missing",
        "SHA-1 divergente in": "SHA-1 mismatch in",
        "f'Corpus falhou: esperado exatamente uma entrada para {start}: '": "f'Corpus failed: expected exactly one entry for {start}: '",
        "f'{marker}; encontradas {len(matches)}.'": "f'{marker}; found {len(matches)}.'",
        "reference não resolvida found in the PDF": "unresolved reference found in the PDF",
        "fallback of photograph apareceu quando photographs of reference eram required": "photograph fallback appeared while reference photographs were required",
        "expected exatamente a block of banca, found": "expected exactly one committee block, found",
        "banca does not fit entirely in the approval page": "committee does not fit entirely on the approval page",
        "entry with case preserved missing of": "case-preserved entry is missing from",
        "entry incorrectly converted for case uppercase in": "entry was incorrectly converted to uppercase in",
        "expected a table of contents principal, found": "expected one main table of contents, found",
        "fim of the table of contents not found antes of the first section textual": "end of the table of contents was not found before the first textual section",
        "entry required missing of the table of contents": "required entry is missing from the table of contents",
        "too few entries paginadas in the table of contents comentado": "too few paginated entries in the annotated table of contents",
        "f'Corpus falhou: {len(undotted)} entrada(s) do sumário sem líder pontilhado espaçado: {sample}'": "f'Corpus failed: {len(undotted)} table-of-contents entries lack spaced dotted leaders: {sample}'",
        "f'Corpus falhou: intervalo físico do sumário excede páginas BBox: '": "f'Corpus failed: physical table-of-contents range exceeds BBox pages: '",
        "f'Corpus falhou: esperado um título primário no sumário para {marker}; encontrados {len(matches)}.'": "f'Corpus failed: expected one primary table-of-contents heading for {marker}; found {len(matches)}.'",
        "f'Corpus falhou: {marker} desalinhado no sumário: '": "f'Corpus failed: {marker} is misaligned in the table of contents: '",
        "f'x={actual_x:.2f}, referência={reference_x:.2f}'": "f'x={actual_x:.2f}, reference={reference_x:.2f}'",
        "Corpus visual, didático and semântico of the documento of reference validado.": "Visual, instructional, and semantic reference corpus validated.",
        "'$marker' missing of $file": "'$marker' is missing from $file",
    },
)

apply(
    "tests/integration/reference-spacing.sh",
    {
        "f'Referências: {name} deve equivaler a uma linha simples; razão={ratio:.4f}'": "f'References: {name} must equal one single-spaced line; ratio={ratio:.4f}'",
        "f'Referências: espaçamento interno deve ser simples; baselinestretch={stretch:.4f}'": "f'References: internal spacing must be single; baselinestretch={stretch:.4f}'",
    },
)

apply(
    "tests/integration/references-6023.sh",
    {
        "NBR 6023:2025: evento sem cidade recebeu sine loco.": "NBR 6023:2025: event without a city received a sine loco marker.",
        "NBR 6023:2025: documento eletrônico recebeu indicador of publicação unknown.": "NBR 6023:2025: electronic document received an unknown publication marker.",
        "NBR 6023:2025: documento impresso sem dados perdeu [S. l.] ou [s. n.].": "NBR 6023:2025: print document without publication data lost [S. l.] or [s. n.].",
        "NBR 6023:2025: entrevistado não aparece como autor principal.": "NBR 6023:2025: interviewee does not appear as the primary author.",
        "NBR 6023:2025: ISSN opcional não foi preservado.": "NBR 6023:2025: optional ISSN was not preserved.",
    },
)

apply(
    "tests/integration/research-project.sh",
    {
        "coat of arms was loaded by default in the cover of research project": "coat of arms was loaded by default on the research-project cover",
        "coat of arms was loaded by default in the research project anonymized": "coat of arms was loaded by default in the anonymized research project",
        "content required of the fixture missing": "required fixture content is missing",
        "cover of research project usou a IES in the lugar of the entidade of submissão": "research-project cover used the institution instead of the submission entity",
        "elemento de trabalho final apareceu no projeto": "final-academic-work element appeared in the research project",
        "cover optional was impressa apesar of cover = false": "optional cover was rendered despite cover = false",
        "title page required missing in the research project without cover": "required title page is missing from the research project without a cover",
        "Projeto anonimizado: autor vazou no PDF.": "Anonymized research project: author leaked into the PDF.",
        "research project anonymized: advisor vazou in the PDF.": "Anonymized research project: advisor leaked into the PDF.",
        "research project anonymized: identifier público missing.": "Anonymized research project: public identifier is missing.",
        "item missing from the table of contents": "item is missing from the table of contents",
        "element pré-textual indevido leaked into the table of contents of the research project": "invalid front-matter element leaked into the research-project table of contents",
    },
)

apply(
    "tests/integration/table-ibge.sh",
    {
        "f'{name}: esperado {expected:.4f}, obtido {value:.4f}'": "f'{name}: expected {expected:.4f}, measured {value:.4f}'",
    },
)

print("R3-B4 final diagnostic message repair applied.")
