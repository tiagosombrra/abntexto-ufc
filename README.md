# abntexto-ufc

Classe LaTeX comunitária para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), construída sobre a classe [`abntexto`](https://ctan.org/pkg/abntexto).

> **Status institucional:** este projeto é comunitário e não é um template oficial ou homologado pela UFC, salvo manifestação institucional explícita em sentido contrário.

## Versão 3.0.1

A série 3 introduz a classe `abntexto-ufc`, uma API pública única em inglês e suporte a perfis de trabalhos acadêmicos, projetos de pesquisa e artigos científicos. A versão 3 é incompatível em nível de API com a série 2: projetos antigos devem ser migrados em vez de misturar comandos das duas linhas.

A versão 3.0.1 é a linha de recuperação de publicação da série 3. Ela preserva a API pública e as semânticas normativa, de perfis e tipográfica já aceitas, e inclui a correção de runtime da lista unificada de ilustrações da PR #302. Os artefatos finais são recertificados a partir do mesmo SHA antes da publicação e da submissão ao CTAN.

O guia de migração está em [`docs/MIGRATING-TO-V3.md`](docs/MIGRATING-TO-V3.md).

## Requisitos

- LaTeX2e;
- `abntexto` 1.1 ou posterior;
- `biblatex` e `biber` para fluxos bibliográficos;
- TeX Live 2026 é o ambiente principal de certificação da versão 3.0.1.

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

Consulte `template/main.tex` para o TCC canônico comentado e `docs/ctan-example.tex` para o exemplo mínimo do pacote CTAN. Nos bundles públicos de template e Overleaf, o TCC completo também é fornecido compilado como `abntexto-ufc-reference.pdf` a partir da mesma fonte pública sanitizada.

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

Quando autorizado a utilizar uma marca institucional, o usuário deve fornecer o arquivo localmente por meio da configuração prevista pela classe. O bundle enviado à CTAN é validado para rejeitar ativos institucionais e fontes proprietárias. Os bundles públicos de template/Overleaf também sanitizam `main.tex` para `coat-of-arms = false`; o PDF de referência distribuído é compilado dessa fonte sanitizada e não do PDF de desenvolvimento que possa usar uma marca fornecida localmente.

## Distribuições

A publicação da versão 3.0.1 produz três artefatos com finalidades distintas:

- `abntexto-ufc-3.0.1.zip`: pacote canônico e enxuto para CTAN. O runtime distribuído é **somente `abntexto-ufc.cls`**; todos os módulos `.def` do repositório são incorporados deterministicamente dentro da classe e nenhum `.def` é enviado. Esse pacote mantém um exemplo mínimo próprio e não carrega o TCC pedagógico completo;
- `abntexto-ufc-template-3.0.1.zip`: projeto editável para uso local, com a fonte pública completa do TCC e o PDF gerado `abntexto-ufc-reference.pdf`; `abntexto` permanece dependência externa;
- `abntexto-ufc-overleaf-3.0.1.zip`: projeto autocontido para upload no Overleaf, incluindo a revisão fixada de `abntexto.cls`, a mesma fonte pública completa e `abntexto-ufc-reference.pdf`.

Somente o primeiro arquivo é destinado à CTAN. Os bundles de template e Overleaf são conveniências de distribuição do GitHub e não fazem parte do upload CTAN.

Há, portanto, dois papéis intencionalmente distintos. O exemplo CTAN é pequeno e serve para documentação/compilação isolada do pacote; `abntexto-ufc-reference.pdf` é o guia pedagógico completo para o usuário. O gate de distribuição extrai os bundles de template e Overleaf, recompila o `main.tex` sanitizado sob o mesmo contrato determinístico e exige que o SHA-256 do PDF recompilado seja idêntico ao PDF embutido.

Essa separação preserva a arquitetura de desenvolvimento modular e testável, mantém o artefato CTAN enxuto e oferece nos bundles de uso um documento completo que demonstra a estrutura e os recursos do projeto.

## Desenvolvimento e validação

Entradas principais:

```bash
make static-check
make check
make release-check
make distribution-bundles
```

`make release-check` executa a regressão de release; `make distribution-bundles` produz os arquivos públicos de forma determinística, incluindo o PDF completo de referência nos bundles de uso, e seus hashes SHA-256.

## Suporte

- Repositório: <https://github.com/tiagosombrra/abntexto-ufc>
- Issues: <https://github.com/tiagosombrra/abntexto-ufc/issues>

## Licença

O código e a documentação próprios do projeto são distribuídos sob a **LaTeX Project Public License (LPPL), versão 1.3c ou posterior**. Consulte [`LICENSE`](LICENSE).

Ativos de terceiros e marcas institucionais não são cobertos por essa licença e não são redistribuídos pelo pacote CTAN.
