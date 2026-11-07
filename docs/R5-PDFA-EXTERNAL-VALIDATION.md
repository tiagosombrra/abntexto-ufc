# R5 — verificação externa PDF/A-2b dos 28 exemplos E3

**Estado:** workflow independente de diagnóstico. Não concede aprovação R5
nem autoriza a publicação da versão 3.1.0.

## Entradas imutáveis

O workflow `.github/workflows/r5-pdfa-exact-e3.yml` recupera exatamente
os quatro artefatos originais `public-full7-{pt,en,es,fr}-42387260385`
produzidos pela [execução 42387260385](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/42387260385)
da [PR #575](https://github.com/tiagosombrra/abntexto-ufc/pull/575).

O commit exato esperado é
`1ac95dd4bcdef08e3a469469b7fdcf8d0b8f8232`, que compila os
sete tipos acadêmicos em quatro idiomas com a composição diagnóstica
das correções #563 (metadados/bookmarks), #565 (legendas ES/FR) e
#566 (tipografia/sumário/banca).

O estágio de entrada confere a identidade do commit, os recibos PDF
de cada idioma e os **28 SHA256 dos arquivos PDF originais**. Nenhum PDF
é regravado, otimizado ou convertido antes de ser apresentado ao veraPDF.

## Como reproduzir

Na PR independente, o evento `pull_request` dispara uma execução
sem modificações na classe. O job baixa os arquivos pelo GitHub CLI,
executa o contêiner público oficial `verapdf/cli:latest` e registra
seu **digest real imutável** antes de validar.

Comando efetivo no runner:

```bash
docker run --rm -v "$PWD/artifacts/r5-pdfa/pdfs:/data:ro" \
  verapdf/cli:latest --flavour 2b --format raw --recurse /data \
  > artifacts/r5-pdfa/verapdf-raw.xml \
  2> artifacts/r5-pdfa/verapdf-stderr.log
```

O relatório XML é interpretado com fail-closed: exige exatamente
28 resultados distintos, o perfil **PDF/A-2b**, campos
`isCompliant`, detalhes de regra, ausência de erros de parse,
checagem de totais e rastreabilidade dos hashes. Em qualquer falha,
o job fica vermelho e os arquivos de evidência disponíveis são
preservados como artefatos.

A imagem Docker com a tag `latest` **não é imutável**. Por esse
motivo o workflow registra `RepoDigests` da imagem usada.
Uma versão de certificação definitiva deverá usar esse digest fixado,
além de registrar a versão completa do programa.

Documentação da ferramenta:
- https://software.verapdf.org/
- https://docs.verapdf.org/cli/validation/
- https://hub.docker.com/r/verapdf/cli

## Limites do parecer

A aprovação da regra ISO 19005-2 (PDF/A-2b) não garante conformidade
PDF/UA, acessibilidade textual, normas ABNT, regras UFC ou qualidade
científica dos exemplos. Em particular, o gate de revisão humana
individual R5 continua aberto em #572. Os **32 PDFs sintéticos R4
com 300 versos candidatos** compõem uma matriz separada, também
ainda sem aprovação normativa.

**Não mesclar automaticamente; publicação proibida.**
`v3.1.0 UNRELEASED`; `publication_authorized=false`.
