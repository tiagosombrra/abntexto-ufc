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
    r'\\Caption\s*\{': r'\Caption',
    r'\\UFC(?:fig|tab|qua)\b': r'\UFCfig/\UFCtab/\UFCqua',
    r'\\Fonte\s*\{': r'\Fonte',
    r'\\documentclass\s*(?:\[[^\]]*\])?\s*\{abntex2\}': 'abntex2',
    r'\\input\s*\{lib/(?:preambulo|ufctex)': 'lib V1',
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
            errors.append(f'{path}: API/estrutura V1 ativa: {label}')

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

if Path('lib').exists():
    errors.append('a pasta lib/ pertence à linha 1.x e não deve existir na distribuição V2')

asset = Path('assets/institucional/brasao-ufc.PNG')
if not asset.is_file():
    errors.append(f'ativo institucional ausente: {asset}')

makefile = Path('Makefile').read_text(encoding='utf-8')
cls = Path('ufctex.cls').read_text(encoding='utf-8')
readme = Path('README.md').read_text(encoding='utf-8')

if not re.search(r'^VERSION\s*:?=\s*2\.0\.0\s*$', makefile, re.MULTILINE):
    errors.append('Makefile: versão diferente de 2.0.0')
if 'v2.0.0 UFC academic document class' not in cls:
    errors.append('ufctex.cls: versão diferente de v2.0.0')
if 'Versão atual: 2.0.0' not in readme:
    errors.append('README.md: versão diferente de 2.0.0')
for module in ('institucional.def', 'trabalhos.def'):
    if rf'\input{{ufctex/{module}}}' not in cls:
        errors.append(f'ufctex.cls: módulo {module} não carregado')

if errors:
    raise SystemExit('\n'.join(errors))
PY

for script in tests/v2-*.sh; do
  sh -n "$script" || {
    echo "Shell inválido: $script"
    exit 1
  }
done

echo 'Gate V2 de consistência da distribuição concluído.'
