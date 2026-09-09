# abntexto-ufc

Classe LaTeX comunitária para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), construída sobre a classe [`abntexto`](https://ctan.org/pkg/abntexto).

> **Status institucional:** este projeto é comunitário e não é um template oficial ou homologado pela UFC, salvo manifestação institucional explícita em sentido contrário.

## Versão 3.0.0

A série 3 introduz a classe `abntexto-ufc`, uma API pública única em inglês e suporte a perfis de trabalhos acadêmicos, projetos de pesquisa e artigos científicos. A versão 3 é incompatível em nível de API com a série 2: projetos antigos devem ser migrados em vez de misturar comandos das duas linhas.

O guia de migração está em [`docs/MIGRATING-TO-V3.md`](docs/MIGRATING-TO-V3.md).

A versão **3.0.0 está publicada no GitHub** em [`v3.0.0`](https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.0). O pacote destinado à CTAN já foi certificado, mas a submissão/aceitação pela CTAN ainda não é reivindicada neste repositório; esse estado só será atualizado após evidência externa.

## Requisitos

- LaTeX2e;
- `abntexto` 1.1 ou posterior;
- `biblatex` e `biber` para fluxos bibliográficos;
- TeX Live 2026 é o ambiente principal de certificação da versão 3.0.0.

A classe é testada com pdfLaTeX e LuaLaTeX. Recursos opcionais podem exigir pacotes adicionais, conforme o perfil e os módulos habilitados.

## Uso mínimo

```tex
\documentclass{abntexto-ufc}

\ufcsetup{
  type = doctoral-thesis,
  print-mode = single-sided,
  coat-of-arms = false,
  author = {Nome Sobrenome},
  title = {Título do trabalho},
  location = {Fortaleza},
  year = {2026},
  advisor = {Prof. Dr. Nome do Orientador}
}

\begin{document}
\ufcPrintCover
\ufcPrintTitlePage

\section{Introdução}
Texto do trabalho.
\end{document}
```

Consulte `template/main.tex` para um exemplo editável mais completo e `docs/ctan-example.tex` para o exemplo mínimo distribuído com o pacote CTAN.

## Perfis de documento

Os valores canônicos de `type` incluem:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- `scientific-article`.

A API pública completa e o mapeamento da série 2 estão documentados em [`docs/MIGRATING-TO-V3.md`](docs/MIGRATING-TO-V3.md).

## Bibliografia e normalização

O projeto usa `biblatex-abnt` e mantém uma camada de compatibilidade delimitada para requisitos da ABNT NBR 6023:2025 que ainda não estejam cobertos pela dependência publicada. A política normativa do projeto é usar a edição técnica vigente aplicável e reconciliar requisitos institucionais atuais da UFC sem reativar edições ABNT substituídas.

A base normativa e a política de vigência estão registradas em:

- [`docs/NORMATIVE-BASE.md`](docs/NORMATIVE-BASE.md);
- [`docs/NORMATIVE-CURRENCY.md`](docs/NORMATIVE-CURRENCY.md).

## Brasão e outros ativos institucionais

**O projeto não redistribui o brasão da UFC nem qualquer outra marca institucional da Universidade.** Também não redistribui arquivos proprietários das fontes Microsoft Arial ou Times New Roman.

Quando autorizado a utilizar uma marca institucional, o usuário deve fornecer o arquivo localmente por meio da configuração prevista pela classe. O bundle enviado à CTAN é validado para rejeitar ativos institucionais e fontes proprietárias.

## Distribuições

A publicação da versão 3 produz três artefatos com finalidades distintas:

- `abntexto-ufc-3.0.0.zip`: pacote canônico e enxuto para CTAN. O runtime distribuído é **somente `abntexto-ufc.cls`**; todos os módulos `.def` do repositório são incorporados deterministicamente dentro da classe e nenhum `.def` é enviado;
- `abntexto-ufc-template-3.0.0.zip`: projeto editável para uso local, que pode preservar a organização modular do repositório;
- `abntexto-ufc-overleaf-3.0.0.zip`: projeto autocontido para upload no Overleaf, incluindo a revisão fixada de `abntexto.cls` e podendo preservar a organização modular do repositório.

Somente o primeiro arquivo é destinado à CTAN. Os bundles de template e Overleaf são conveniências de distribuição do GitHub e não fazem parte do upload CTAN.

Essa separação é deliberada: a arquitetura de desenvolvimento continua modular e testável, enquanto o artefato CTAN oferece uma classe única, sem dependência em arquivos `.def` próprios do projeto.

## Desenvolvimento e validação

Entradas principais:

```bash
make static-check
make check
make release-check
make distribution-bundles
```

`make release-check` executa a regressão de release; `make distribution-bundles` produz os arquivos públicos de forma determinística e seus hashes SHA-256.

## Suporte

- Repositório: <https://github.com/tiagosombrra/abntexto-ufc>
- Issues: <https://github.com/tiagosombrra/abntexto-ufc/issues>

## Licença

O código e a documentação próprios do projeto são distribuídos sob a **LaTeX Project Public License (LPPL), versão 1.3c ou posterior**. Consulte [`LICENSE`](LICENSE).

Ativos de terceiros e marcas institucionais não são cobertos por essa licença e não são redistribuídos pelo pacote CTAN.
