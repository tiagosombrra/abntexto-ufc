# abntexto-ufc

Classe LaTeX comunitária para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), construída sobre a classe [`abntexto`](https://ctan.org/pkg/abntexto).

> **Status institucional:** este é um projeto comunitário. Ele não é um template oficial ou homologado pela UFC, salvo manifestação institucional explícita em sentido contrário.

> **Versões:** a última versão publicada é a **v3.0.5**. A **v3.1.0 está em desenvolvimento**, sem tag, Release pública ou publicação CTAN. Os exemplos de internacionalização identificados como v3.1.0 abaixo se referem ao código de desenvolvimento (`main`), não aos ZIPs já publicados. Para uso acadêmico em produção, prefira o ZIP correspondente a uma [Release publicada](https://github.com/tiagosombrra/abntexto-ufc/releases).

## Acesso rápido

- **Site do projeto:** https://tiagosombrra.github.io/abntexto-ufc/
- **Validador Web/Lite:** https://tiagosombrra.github.io/abntexto-ufc/validator/
- **Releases e downloads:** https://github.com/tiagosombrra/abntexto-ufc/releases
- **Repositório:** https://github.com/tiagosombrra/abntexto-ufc
- **Issues / suporte técnico:** https://github.com/tiagosombrra/abntexto-ufc/issues
- **Tutorial e fluxo de uso:** [docs/USER-GUIDE.md](docs/USER-GUIDE.md)
- **Referência completa de comandos:** [docs/COMMAND-REFERENCE.md](docs/COMMAND-REFERENCE.md)
- **Documentação técnica e manutenção:** [docs/README.md](docs/README.md)
- **Histórico de versões:** [CHANGELOG.md](CHANGELOG.md)
- **Base normativa:** [docs/NORMATIVE-BASE.md](docs/NORMATIVE-BASE.md)

O site e o validador são publicados a partir do mesmo repositório. Se o site estiver temporariamente indisponível, a aplicação Web/Lite também pode ser servida localmente a partir da pasta `validator/`.

## O que é este projeto

O `abntexto-ufc` organiza em uma única classe LaTeX:

- perfis de TCC, dissertação, tese, projeto de pesquisa e artigo científico;
- elementos pré-textuais, textuais e pós-textuais usados nos trabalhos acadêmicos;
- regras de layout, objetos acadêmicos, citações e bibliografia;
- uma camada de requisitos institucionais da UFC sobre a base ABNT aplicável;
- um TCC tutorial curto, compilável e realista, separado da referência exaustiva de comandos e da cobertura de regressão;
- validadores Web/Lite e CLI/Deep;
- distribuição separada para CTAN, uso local e Overleaf.

O projeto usa uma única API pública canônica em inglês, sem traduzir nomes de comandos e opções. O português é o idioma padrão. Na linha **v3.1.0 em desenvolvimento**, o idioma principal e os rótulos gerados pela classe podem ser configurados para português, inglês, espanhol e francês. Isso **não traduz automaticamente** o texto do autor, dados bibliográficos nem nomes oficiais de instituições.

## Comece em poucos minutos

1. **Escolha uma versão:** para um trabalho a ser entregue, use a [v3.0.5 publicada](https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.5). A `main` documenta recursos **v3.1.0 ainda não publicados**, destinados a avaliação e desenvolvimento.
2. **Escolha o ambiente:** no Overleaf, importe o ZIP `abntexto-ufc-overleaf-3.0.5.zip`; localmente, extraia `abntexto-ufc-template-3.0.5.zip` e prepare TeX Live, `abntexto` e Biber. Preserve o conteúdo das pastas.
3. **Edite e confira:** escolha `type`, preencha `\ufcsetup{...}`, substitua os arquivos de exemplo, compile e revise o PDF inteiro. Use o [guia passo a passo](docs/USER-GUIDE.md) para os sete perfis e os comandos opcionais.

O uso de `main` **não atualiza** automaticamente uma instalação publicada da v3.0.5; configurações de `document-language=en|es|fr` e a correção de listagens aninhadas descritas abaixo pertencem à v3.1.0 em desenvolvimento.

## Para quem é

| Público | Caminho recomendado |
|---|---|
| Estudante que quer começar rapidamente | use o ZIP **Overleaf** ou o ZIP **Template** de uma Release |
| Usuário de Overleaf | baixe `abntexto-ufc-overleaf-<versão>.zip` e faça upload como novo projeto |
| Usuário local de LaTeX | baixe `abntexto-ufc-template-<versão>.zip` e edite `main.tex` |
| Orientador / biblioteca | use `abntexto-ufc-reference.pdf` como referência visual e o validador como apoio |
| Usuário avançado / mantenedor | use o repositório, os testes e o pacote CTAN canônico |
| Quem mantém ou contribui com o projeto | comece pelo [índice técnico](docs/README.md) e por [CONTRIBUTING.md](CONTRIBUTING.md) |

## Qual arquivo da Release devo baixar?

Cada Release produz artefatos com funções diferentes.

| Arquivo | Finalidade | O que contém | Uso recomendado |
|---|---|---|---|
| `abntexto-ufc-<versão>.zip` | pacote canônico para CTAN | classe canônica única, documentação mínima e exemplo CTAN; sem ativo institucional da UFC | publicação/instalação de pacote; não é o melhor ponto de partida para um TCC |
| `abntexto-ufc-template-<versão>.zip` | projeto local editável | fonte completa do TCC, runtime do projeto, brasão institucional usado pelo exemplo e `abntexto-ufc-reference.pdf` | usuários locais com TeX Live e dependência `abntexto` instalada |
| `abntexto-ufc-overleaf-<versão>.zip` | projeto autocontido para Overleaf | fonte completa, brasão institucional usado pelo exemplo, revisão fixada de `abntexto.cls` e o mesmo PDF de referência | caminho mais simples para começar no Overleaf |
| `SHA256SUMS` | integridade | hashes dos artefatos da distribuição | conferência de downloads e auditoria |

### Overleaf

1. Abra a página de [Releases](https://github.com/tiagosombrra/abntexto-ufc/releases).
2. Baixe `abntexto-ufc-overleaf-<versão>.zip`.
3. No Overleaf, escolha **New Project → Upload Project**.
4. Envie o ZIP sem reorganizar as pastas.
5. Edite `main.tex`, os arquivos de `frontmatter/`, `chapters/` e `backmatter/`.

O bundle Overleaf é autocontido justamente para reduzir diferenças de versão da dependência principal.

### Uso local

1. Baixe `abntexto-ufc-template-<versão>.zip`.
2. Extraia o arquivo preservando a estrutura de diretórios.
3. Use TeX Live 2026, ambiente principal de certificação da série 3.
4. Garanta `abntexto` 1.1 ou posterior e `biblatex`/`biber`.
5. Abra e compile `main.tex` no seu editor LaTeX.

O documento canônico usa bibliografia e outros recursos que podem exigir mais de uma passagem de compilação. Um editor LaTeX configurado com Biber é o caminho mais simples.

### Pacote CTAN

`abntexto-ufc-<versão>.zip` é o arquivo canônico submetido ao CTAN. O runtime público desse pacote é o mesmo `abntexto-ufc.cls` canônico rastreado e testado no repositório; não existe uma etapa separada de inlining de módulos.

O pacote CTAN não redistribui o brasão da UFC. O exemplo CTAN usa `coat-of-arms=false`; usuários que desejarem o brasão ao instalar somente pelo CTAN devem fornecer o ativo localmente ou usar um dos bundles de usuário da Release.

Depois que a versão estiver disponível no CTAN/TeX Live, a instalação normal pela distribuição TeX é preferível a extrair manualmente esse ZIP.

## Uso mínimo

```tex
\DocumentMetadata{lang=pt-BR,pdfstandard=A-2b,pdfversion=1.7}
\documentclass{abntexto-ufc}

\ufcsetup{
  type = undergraduate-capstone,
  print-mode = single-sided,
  coat-of-arms = false,
  author = {Nome Sobrenome},
  title = {Título do trabalho},
  location = {Fortaleza},
  year = {2026},
  advisor = {Prof. Dr. Nome do Orientador}
}

\begin{document}
\pretextual
\ufcPrintCover
\ufcPrintTitlePage

\textual
\section{Introdução}
Texto do trabalho.
\end{document}
```

Para aprender pelo exemplo completo, use `template/main.tex`. Ele é um TCC tutorial: mostra o fluxo real de edição e usa os recursos principais no contexto em que aparecem. Nos bundles de Template e Overleaf, essa fonte mantém `coat-of-arms=true`, inclui `assets/institutional/ufc-coat-of-arms.png` e vem acompanhada de `abntexto-ufc-reference.pdf`, gerado a partir da mesma fonte distribuída.

Para consulta sem inflar o TCC, use [docs/USER-GUIDE.md](docs/USER-GUIDE.md) e [docs/COMMAND-REFERENCE.md](docs/COMMAND-REFERENCE.md). Casos extremos e cobertura normativa permanecem em `tests/` e `standards/`, não no texto acadêmico do tutorial.

## Idiomas e internacionalização — somente v3.1.0 em desenvolvimento

A internacionalização é opt-in: `document-language=pt|en|es|fr` seleciona o idioma principal e os textos automáticos cobertos pela classe, enquanto `labels-language=pt|en|es|fr` permite escolher separadamente os nove títulos pré-textuais gerais. Se não informar um idioma, o comportamento legado permanece em português. Os **identificadores dos comandos LaTeX continuam em inglês**.

Exemplo de configuração para inglês **no código de desenvolvimento v3.1.0** (substitua os metadados pelo conteúdo real):

```tex
\DocumentMetadata{lang=en-US,pdfstandard=A-2b,pdfversion=1.7}
\documentclass{abntexto-ufc}
\ufcsetup{
  type = undergraduate-capstone,
  document-language = en,
  labels-language = en,
  coat-of-arms = false,
  author = {Example Author},
  title = {Example Academic Work}
}
```

O idioma do PDF declarado em `\DocumentMetadata` é **independente** do idioma Babel configurado por `document-language`; ambos devem ser coerentes. Para espanhol use `es`/`es-ES`; para francês `fr`/`fr-FR`; para português `pt`/`pt-BR`. Conteúdos de resumo, palavras-chave e nomes institucionais exigem edição e revisão humanas.

A cobertura atual de desenvolvimento inclui matrizes de documentos completos em quatro idiomas e **72/72 identificadores da API pública com recibos individuais de prova funcional delimitada**: 13 suítes originais, 10 ZIPs autenticados, 310 PDFs e 4.952 referências SHA-256. Esse resultado **não significa** aprovação irrestrita de todos os perfis, mecanismos TeX, cenários ou normas UFC/ABNT, nem revisão linguística/visual institucional. O ledger histórico da classe anterior permanece preservado e a certificação formal global da nova classe continua pendente. Consulte [configuração e resumos multilíngues](docs/USER-GUIDE.md), [referência da API](docs/COMMAND-REFERENCE.md), [matriz de evidências](docs/I18N-COMPLETION-MATRIX.md) e [roadmap da v3.1.0](https://github.com/tiagosombrra/abntexto-ufc/issues/489).

## Perfis de documento

Os valores canônicos de `type` incluem:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- `scientific-article`.

O TCC tutorial mostra o fluxo normal de um trabalho; a documentação separada explica a configuração completa, e os testes exercitam os casos especializados.

## Validação

### Web/Lite

Acesse:

**https://tiagosombrra.github.io/abntexto-ufc/validator/**

O Web/Lite processa o PDF selecionado no navegador. O arquivo não é enviado para um servidor do projeto. A aplicação carrega a versão fixada do PDF.js a partir do jsDelivr, portanto a primeira carga da aplicação exige acesso à rede.

O modo Web/Lite verifica, entre outros pontos, abertura do PDF, tamanho A4, geometria disponível ao navegador, elementos estruturais, metadados e sinais de acessibilidade. Ele **não substitui** a validação profunda de incorporação de fontes ou PDF/A: essas verificações permanecem como `MANUAL REVIEW` na superfície Web/Lite.

### CLI/Deep

Para validação local mais profunda:

```bash
python3 tools/validate-ufc-pdf.py arquivo.pdf --profile strict
```

Perfis disponíveis:

- `strict`: validação acadêmica estrita;
- `portable`: aceita determinados fallbacks portáveis e é o perfil usado pelo E2E Web/Lite do TCC público;
- `accessibility`: adiciona exigências de acessibilidade e revisões manuais.

Exemplo com saída JSON:

```bash
python3 tools/validate-ufc-pdf.py arquivo.pdf --profile strict --format json --output report.json
```

O CLI/Deep usa ferramentas locais como Poppler e, quando disponível, veraPDF para verificações que o navegador não deve declarar automaticamente como PASS.

## Perguntas frequentes e diagnóstico

**Posso usar a v3.1.0 em um trabalho para entrega?** Ela ainda é uma prévia de desenvolvimento, sem Release ou CTAN próprios. Para depósito acadêmico, prefira a v3.0.5 publicada e confirme os requisitos atuais do curso e do programa.

**A capa não mostra o brasão ou aparece erro de imagem ausente.** O exemplo mínimo usa `coat-of-arms=false` para não depender de um arquivo institucional. Os bundles Template e Overleaf trazem o brasão utilizado pelo tutorial e configuram `coat-of-arms=true`; quem trabalha com o pacote CTAN deve providenciar o ativo separadamente, se aplicável.

**Citações ou referências aparecem como interrogações.** Confira `backmatter/references.bib`, as chaves de citação e a execução de Biber entre as passagens de LaTeX. Executar apenas uma vez `pdflatex` não reproduz necessariamente o resultado do tutorial completo.

**O PDF mostra idioma ou palavras-chave errados.** Na v3.1.0, configure `document-language` com `pt|en|es|fr`, escolha `labels-language` somente quando quiser títulos pré-textuais diferentes, e declare o `lang` BCP 47 correspondente em `\DocumentMetadata` antes da classe. O conteúdo dos resumos e os nomes oficiais não são traduzidos automaticamente.

**Uma listagem externa falha dentro de `ufcobject` ou `place`.** Na v3.1.0, use a API `\ufcInputListing` com `code=listings`, e não presuma que `\lstinputlisting` nativo receba a mesma correção. Para listagens longas que precisam quebrar entre páginas, faça a importação diretamente no fluxo textual, fora dessas caixas. Consulte a [referência da API](docs/COMMAND-REFERENCE.md).

**O validador Web/Lite aprovou o PDF: ele está conforme PDF/A e ABNT/UFC?** Não necessariamente. O Web/Lite não certifica profundamente fontes incorporadas nem PDF/A, e nenhuma das ferramentas substitui uma inspeção normativa, visual e linguística. Utilize o CLI/Deep e as regras oficiais de depósito aplicáveis.

## Base normativa

O projeto separa quatro tipos de decisão:

1. requisito normativo ABNT aplicável;
2. requisito institucional vigente da UFC;
3. política editorial/técnica do projeto;
4. exemplo ou recomendação de uso.

A política é usar a edição técnica vigente aplicável e não reativar normas substituídas apenas por compatibilidade histórica.

Documentos principais:

- [Guia de uso](docs/USER-GUIDE.md)
- [Referência de comandos](docs/COMMAND-REFERENCE.md)
- [Base normativa](docs/NORMATIVE-BASE.md)
- [Vigência normativa](docs/NORMATIVE-CURRENCY.md)
- [Guia do validador Web/Lite](validator/README.md)

A camada bibliográfica usa `biblatex-abnt` e mantém compatibilidade delimitada para requisitos da ABNT NBR 6023:2025 ainda não cobertos pela dependência publicada.

## Brasão, marcas e fontes proprietárias

A política de distribuição distingue o pacote CTAN dos bundles voltados ao usuário final:

- o pacote canônico submetido ao **CTAN não redistribui o brasão da UFC nem outras marcas institucionais** e não redistribui arquivos proprietários das fontes Microsoft Arial ou Times New Roman;
- os bundles **Template** e **Overleaf** incluem `assets/institutional/ufc-coat-of-arms.png`, mantêm `coat-of-arms=true` no TCC tutorial e incorporam um `abntexto-ufc-reference.pdf` gerado com esse mesmo ativo;
- `coat-of-arms=false` continua disponível para submissões externas, processos cegos ou qualquer situação em que a marca institucional não deva aparecer.

Nos perfis `research-project` e `anonymized-research-project`, uma capa institucional UFC usa o brasão por padrão, em consonância com a apresentação mostrada no Guia de Normalização de Projetos de Pesquisa da UFC. Essa é uma política de apresentação institucional do projeto, não uma promoção do brasão a requisito da ABNT. O perfil anonimizado atual oculta autor e orientador, mas não oculta a instituição por si só.

As marcas institucionais não são cobertas pela LPPL do projeto. A inclusão do ativo nos bundles Template/Overleaf não altera a identidade comunitária e não oficial do projeto.

## Estrutura do repositório

| Caminho | Papel |
|---|---|
| `abntexto-ufc.cls` | fonte canônica única do runtime; usada diretamente por testes, Template, Overleaf e CTAN |
| `template/` | TCC tutorial curto e editável, com frontmatter/chapters/backmatter de exemplo |
| `validator/` | aplicação estática Web/Lite e contrato do validador |
| `standards/` | catálogo normativo, precedência e rastreabilidade |
| `tests/` | contratos estáticos, integração, regressão e fixtures |
| `tools/` | geração de bundles, validação e utilitários de engenharia |
| `docs/` | documentação de uso, arquitetura, normas, validação, certificação e release |
| `release/` | estado de máquina e marcadores auditáveis de release |
| `site/` | landing page publicada pelo GitHub Pages |
| `.github/workflows/` | CI, certificação, release e publicação do site |

## Como uma versão é certificada

As releases do projeto usam um processo fail-closed. O mesmo candidato precisa passar:

- contrato estático;
- regressão Linux completa;
- TCC canônico e corpus de referência;
- CLI/Deep e Web/Lite com PDF real;
- PDF/A-2b e incorporação de fontes;
- geração/rebuild dos bundles públicos;
- `pkgcheck` corrente do CTAN;
- sete pares PDF/TEX de perfis suportados;
- revisão humana final antes da tag.

O contrato de publicação é:

```text
SHA certificado == SHA aprovado visualmente == SHA da tag da versão == SHA que gerou os arquivos publicados
```

Depois da aprovação humana final, os artefatos não podem ser reconstruídos.

## Desenvolvimento

Entradas principais:

```bash
make static-check
make check
make release-check
make distribution-bundles
```

- `make static-check`: contratos rápidos de fonte, documentação e consistência;
- `make check`: integração padrão;
- `make release-check`: regressão de release;
- `make distribution-bundles`: gera os três artefatos públicos e `SHA256SUMS`.

## Suporte e contribuição

- Issues: https://github.com/tiagosombrra/abntexto-ufc/issues
- Código: https://github.com/tiagosombrra/abntexto-ufc
- Releases: https://github.com/tiagosombrra/abntexto-ufc/releases
- Contribuição: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Segurança: [`SECURITY.md`](SECURITY.md)
- Citação acadêmica: [`CITATION.cff`](CITATION.cff)

Ao relatar um problema, informe o perfil de documento, engine LaTeX, versão da classe e um exemplo mínimo quando possível.

## Licença

O código e a documentação próprios do projeto são distribuídos sob a **LaTeX Project Public License (LPPL), versão 1.3c ou posterior**. Consulte [`LICENSE`](LICENSE).

Status de manutenção LPPL: `maintained`. O **Current Maintainer** é **Tiago Guimarães Sombra**. Para a distribuição CTAN, a identidade exata do `Work` é enumerada em [`release/ctan/README.md`](release/ctan/README.md).

Ativos de terceiros e marcas institucionais não são cobertos por essa licença. O pacote CTAN não os redistribui; os bundles Template/Overleaf podem incluir o ativo institucional mantido pelo projeto conforme a política de distribuição acima. O PDF.js vendorizado mantém sua licença Apache-2.0 e metadados próprios de proveniência.
