#!/bin/sh
set -eu

python3 <<'PY'
from pathlib import Path
import re

tex_files = [Path('documento.tex')]
for directory in ('1-pre-textuais', '2-textuais', '3-pos-textuais'):
    tex_files.extend(sorted(Path(directory).rglob('*.tex')))

forbidden = {
    r'\\chapter\s*\{': r'\chapter',
    r'\\apendice\s*\{': r'\apendice',
    r'\\anexo\s*\{': r'\anexo',
}


def uncommented(text: str) -> str:
    lines = []
    for line in text.splitlines():
        out = []
        i = 0
        while i < len(line):
            if line[i] == '%' and (i == 0 or line[i - 1] != '\\'):
                break
            out.append(line[i])
            i += 1
        lines.append(''.join(out))
    return '\n'.join(lines)

errors = []
for path in tex_files:
    text = uncommented(path.read_text(encoding='utf-8'))
    for pattern, label in forbidden.items():
        if re.search(pattern, text):
            errors.append(f'{path}: estrutura não permitida no corpus V2: {label}')

    refs = []
    refs.extend((m.group(1), 'tex') for m in re.finditer(r'\\(?:input|include)\s*\{([^}]+)\}', text))
    refs.extend((m.group(1), 'tex') for m in re.finditer(
        r'\\(?:imprimirdedicatoria|imprimiragradecimentos|imprimirepigrafe|imprimirresumo|imprimirabstract|imprimirerrata|imprimirlistadeabreviaturasesiglas|imprimirlistadesimbolos)(?:\[[^\]]*\])?\s*\{([^}]+)\}',
        text,
    ))
    refs.extend((m.group(1), 'bib') for m in re.finditer(r'\\ufcbibliografia\s*\{([^}]+)\}', text))
    refs.extend((m.group(1), 'raw') for m in re.finditer(r'\\ufcinputlisting(?:\[[^\]]*\])?\s*\{([^}]+)\}', text))
    refs.extend((m.group(1), 'raw') for m in re.finditer(r'\\includepdf(?:\[[^\]]*\])?\s*\{([^}]+)\}', text))

    for ref, kind in refs:
        candidate = Path(ref)
        if kind == 'tex' and not candidate.suffix:
            candidate = candidate.with_suffix('.tex')
        elif kind == 'bib' and not candidate.suffix:
            candidate = candidate.with_suffix('.bib')
        if not candidate.exists():
            errors.append(f'{path}: arquivo referenciado não existe: {candidate}')

asset = Path('assets/institucional/brasao-ufc.PNG')
if not asset.is_file():
    errors.append(f'ativo institucional ausente: {asset}')

makefile = Path('Makefile').read_text(encoding='utf-8')
canonical_path = Path('abntexto-ufc.cls')
legacy_path = Path('ufctex.cls')
canonical = canonical_path.read_text(encoding='utf-8')
legacy = legacy_path.read_text(encoding='utf-8')
readme = Path('README.md').read_text(encoding='utf-8')

version_match = re.search(r'^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$', makefile, re.MULTILINE)
if not version_match:
    errors.append('Makefile: VERSION sem versão semântica válida')
else:
    version = version_match.group(1)
    if f'v{version} UFC academic document class' not in canonical:
        errors.append(f'abntexto-ufc.cls: versão diferente de v{version}')

    published_match = re.search(
        r'Versão\s+publicada\s+atual:\s*(?:\*\*)?([0-9]+\.[0-9]+\.[0-9]+)(?:\*\*)?\b',
        readme,
        re.IGNORECASE,
    )
    candidate_match = re.search(
        r'Versão\s+candidata\s+em\s+preparação:\s*(?:\*\*)?([0-9]+\.[0-9]+\.[0-9]+)(?:\*\*)?\b',
        readme,
        re.IGNORECASE,
    )
    if not published_match:
        errors.append('README.md: versão publicada atual ausente ou inválida')
    elif published_match.group(1) != version:
        if not candidate_match or candidate_match.group(1) != version:
            errors.append(
                f'README.md: VERSION {version} não coincide com versão publicada nem candidata'
            )

if r'\LoadClass{abntexto-ufc}' not in legacy:
    errors.append('ufctex.cls: wrapper de compatibilidade não carrega abntexto-ufc')

modules = re.findall(
    r'\\input\{((?:abntexto-ufc|ufctex)/[^}]+\.def)\}',
    uncommented(canonical),
)
if not modules:
    errors.append('abntexto-ufc.cls: nenhum módulo UFC carregado')
module_names = {Path(module).name for module in modules}
if 'fontes.def' not in module_names:
    errors.append('abntexto-ufc.cls: módulo obrigatório fontes.def não carregado')
for module in modules:
    if not Path(module).is_file():
        errors.append(f'abntexto-ufc.cls: módulo carregado não existe: {module}')

institutional = Path('abntexto-ufc/institucional.def').read_text(encoding='utf-8')
if 'brasao-arquivo' not in institutional:
    errors.append('abntexto-ufc/institucional.def: chave brasao-arquivo ausente')
if 'assets/institucional/brasao-ufc.PNG' not in institutional:
    errors.append('abntexto-ufc/institucional.def: caminho compatível padrão do brasão ausente')

builder = Path('tools/build-release-bundles.py').read_text(encoding='utf-8')
ctan_match = re.search(
    r'def build_ctan_bundle\(.*?(?=\ndef write_checksums\()',
    builder,
    re.DOTALL,
)
if not ctan_match:
    errors.append('tools/build-release-bundles.py: função build_ctan_bundle ausente')
else:
    ctan_builder = ctan_match.group(0)
    if 'assets/institucional' in ctan_builder:
        errors.append('CTAN builder ainda inclui assets/institucional')
    if 'reference_pdf' in ctan_builder or '-reference.pdf' in ctan_builder:
        errors.append('CTAN builder ainda inclui PDF de referência com marca institucional')
    if 'DOC_SOURCE_INPUTS' in ctan_builder or 'doc/example/' in ctan_builder:
        errors.append('CTAN builder ainda inclui árvore completa do documento de referência')
    if 'prepare-windows-fonts.ps1' in ctan_builder or 'convert-encoding-to-unicode.ps1' in ctan_builder:
        errors.append('CTAN builder ainda inclui scripts específicos do projeto')
    if 'docs/ctan-example.tex' not in ctan_builder:
        errors.append('CTAN builder não inclui o exemplo mínimo portátil')

release_infrastructure = (
    'tools/build-release-bundles.py',
    'tools/fetch-abntexto.py',
    'tools/fetch-reference-images.py',
    'tools/download-actions-artifact.py',
    'tests/v2-canonical-identity-check.py',
    'tests/v2-ctan-policy-check.py',
    'tests/v2-ctan-archive-check.py',
    'tests/v2-release-package-check.py',
    'tests/v2-overleaf-bundle-check.py',
    'tests/v2-release-metadata-check.py',
    'tests/v2-repository-audit.py',
    'tests/v2-reference-corpus-check.sh',
    'tests/v2-algorithm-numbering-check.sh',
    'docs/README-CTAN.md',
    'docs/CHANGELOG-CTAN.md',
    'docs/ctan-example.tex',
    'docs/AUDITORIA-V2.md',
    'figuras/LICENCAS.md',
    '.github/workflows/distribution.yml',
    '.github/workflows/reference-validation.yml',
)
for required in release_infrastructure:
    if not Path(required).is_file():
        errors.append(f'infraestrutura de distribuição/validação ausente: {required}')

microsoft_fonts = {
    'times.ttf', 'timesbd.ttf', 'timesi.ttf', 'timesbi.ttf',
    'arial.ttf', 'arialbd.ttf', 'ariali.ttf', 'arialbi.ttf',
}
for path in Path('.').rglob('*'):
    if path.is_file() and path.name.lower() in microsoft_fonts:
        errors.append(f'fonte Microsoft proprietária não pode ser versionada: {path}')

if errors:
    raise SystemExit('\n'.join(errors))
PY

python3 tests/v2-canonical-identity-check.py
python3 tests/v2-ctan-policy-check.py

for script in tests/v2-*.sh; do
  sh -n "$script" || {
    echo "Shell inválido: $script"
    exit 1
  }
done

python3 -m py_compile \
  tools/build-release-bundles.py \
  tools/fetch-abntexto.py \
  tools/fetch-reference-images.py \
  tools/download-actions-artifact.py \
  tests/v2-canonical-identity-check.py \
  tests/v2-ctan-policy-check.py \
  tests/v2-ctan-archive-check.py \
  tests/v2-repository-audit.py \
  tests/v2-release-package-check.py \
  tests/v2-overleaf-bundle-check.py \
  tests/v2-release-metadata-check.py

echo 'Gate V2 de consistência da distribuição concluído.'
