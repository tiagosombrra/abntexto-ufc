# Exemplos públicos editáveis: estudo reprodutível de malhas

Estes documentos são **exemplos acadêmicos didáticos**, distintos dos testes
sintéticos `INTEGRATED-*` e `R4-*` de `tests/integration/frontmatter/`.
Todos os dados científicos são derivados de
[study.json](../canonical-mesh-study/study.json), nunca de medições
de desempenho não realizadas.

## Conteúdo

O gerador produz **28 fontes TeX editáveis**, correspondentes a sete tipos
documentais (`undergraduate-capstone`, `specialization-capstone`,
`masters-thesis`, `doctoral-thesis`, `research-project`,
`anonymized-research-project` e `scientific-article`) nos idiomas
`pt`, `en`, `es` e `fr`.

Cada documento contém título e estrutura próprios do gênero, introdução,
objetivos, método matemático, figura vetorial de três malhas, tabela com
contagens determinísticas, discussão das limitações e referências reais.
O texto de projetos diferencia os **resultados esperados** dos valores
topológicos já calculados na demonstração. Nenhum documento declara
contribuição inédita, superioridade algorítmica ou homologação institucional.

Os dados de autor, orientação, titulação e programa são **demonstrativos**.
Devem ser substituídos e conferidos com o curso ou edital antes de qualquer
submissão. As traduções dos nomes institucionais em ES/FR são descritivas,
não nomes jurídicos homologados.

## Gerar e verificar

A partir da raiz do repositório, com Python 3 e biblioteca padrão:

```bash
python3 tools/examples/generate_public_mesh_documents.py
python3 tools/examples/generate_public_mesh_documents.py --check
python3 tests/checks/examples/public_mesh_documents.py
```

Os arquivos editáveis aparecem em
`artifacts/public-mesh-documents/<idioma>/<perfil>.tex`. Os resumos
de apoio ficam na mesma pasta. Os desenhos originais e a seção
matemática são gerados em `artifacts/canonical-mesh-study/`.

O manifesto `artifacts/public-mesh-documents/manifest.json` identifica
os SHA256 da fonte matemática, do conteúdo editorial, do gerador e de
cada arquivo. Reexecuções idênticas devem produzir os mesmos bytes. O
comando `--check` rejeita alteração manual dos arquivos gerados.

## Compilação experimental

Para o TCC em português (TeX Live 2026, compilação iniciada na **raiz
do repositório**, com `abntexto`, Biber e os pacotes da classe):

```bash
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -jobname=public-mesh-tcc-pt \
  artifacts/public-mesh-documents/pt/undergraduate-capstone.tex
biber public-mesh-tcc-pt
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -jobname=public-mesh-tcc-pt \
  artifacts/public-mesh-documents/pt/undergraduate-capstone.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -jobname=public-mesh-tcc-pt \
  artifacts/public-mesh-documents/pt/undergraduate-capstone.tex
```

A ordem deve ser repetida para os demais perfis e idiomas com o respectivo
arquivo `.tex` e nome de job exclusivo. **A existência da fonte não
comprova que os 28 documentos compilam**. Toda compilação exigirá logs,
hashes, inventário de páginas e revisão própria. `pdfstandard=A-2b`
configura a produção pretendida, mas não constitui certificação PDF/A
sem validação independente.

## Separação dos produtos e status

- **Corpus R4 de regressão:** permanece em
  `tests/integration/frontmatter/generate-comprehensive-corpus.py`
  (PR #568); suas sentinelas são intencionais e não devem ser apagadas.
- **Exemplos públicos:** gerados exclusivamente por
  `tools/examples/generate_public_mesh_documents.py`. São fontes
  editáveis com linguagem natural e dados reais calculados.
- **Template de uso do projeto:** permanece em `template/`.
  Os presentes exemplos não substituem a Release publicada.
- **R5:** revisão visual/normativa de todas as páginas e autorização
  expressa continuam **PENDENTES**; versão 3.1.0 **NÃO PUBLICADA**.

O projeto ABNTEXTO-UFC é comunitário e não constitui um modelo
oficialmente homologado pela Universidade Federal do Ceará.

## Responsabilidade do workflow de CI

O fluxo dedicado `.github/workflows/public-mesh-examples.yml` é a raiz de
execução dos testes de fonte e PDF destes exemplos. Ele roda apenas a
compilação focal de um TCC por idioma; a matriz 28-PDF completa e a auditoria
R5 permanecem portas independentes de homologação, não suprimidas por este CI.
