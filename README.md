# abntexto-ufc

Classe LaTeX comunitária para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), construída sobre a classe [`abntexto`](https://ctan.org/pkg/abntexto).

> **Status institucional:** este é um projeto comunitário. Ele não é um template oficial ou homologado pela UFC, salvo manifestação institucional explícita em sentido contrário.

## Acesso rápido

- **Site do projeto:** https://tiagosombrra.github.io/abntexto-ufc/
- **Validador Web/Lite:** https://tiagosombrra.github.io/abntexto-ufc/validator/
- **Releases e downloads:** https://github.com/tiagosombrra/abntexto-ufc/releases
- **Repositório:** https://github.com/tiagosombrra/abntexto-ufc
- **Issues / suporte técnico:** https://github.com/tiagosombrra/abntexto-ufc/issues
- **Migração da série 2 para a série 3:** [docs/MIGRATING-TO-V3.md](docs/MIGRATING-TO-V3.md)
- **Base normativa:** [docs/NORMATIVE-BASE.md](docs/NORMATIVE-BASE.md)

O site e o validador são publicados a partir do mesmo repositório. Se o site estiver temporariamente indisponível, a aplicação Web/Lite também pode ser servida localmente a partir da pasta `validator/`.

## O que é este projeto

O `abntexto-ufc` organiza em uma única classe LaTeX:

- perfis de TCC, dissertação, tese, projeto de pesquisa e artigo científico;
- elementos pré-textuais, textuais e pós-textuais usados nos trabalhos acadêmicos;
- regras de layout, objetos acadêmicos, citações e bibliografia;
- uma camada de requisitos institucionais da UFC sobre a base ABNT aplicável;
- um TCC canônico comentado que funciona simultaneamente como guia de uso e corpus de regressão;
- validadores Web/Lite e CLI/Deep;
- distribuição separada para CTAN, uso local e Overleaf.

A série 3 usa uma API pública única em inglês. Ela é incompatível em nível de API com a série 2; projetos antigos devem ser migrados, e não misturados com comandos das duas linhas.

## Para quem é

| Público | Caminho recomendado |
|---|---|
| Estudante que quer começar rapidamente | use o ZIP **Overleaf** ou o ZIP **Template** de uma Release |
| Usuário de Overleaf | baixe `abntexto-ufc-overleaf-<versão>.zip` e faça upload como novo projeto |
| Usuário local de LaTeX | baixe `abntexto-ufc-template-<versão>.zip` e edite `main.tex` |
| Orientador / biblioteca | use `abntexto-ufc-reference.pdf` como referência visual e o validador como apoio |
| Usuário avançado / mantenedor | use o repositório, os testes e o pacote CTAN canônico |
| Quem já usa a série 2 | comece pelo [guia de migração](docs/MIGRATING-TO-V3.md) |

## Qual arquivo da Release devo baixar?

Cada Release produz artefatos com funções diferentes.

| Arquivo | Finalidade | O que contém | Uso recomendado |
|---|---|---|---|
| `abntexto-ufc-<versão>.zip` | pacote canônico para CTAN | classe monolítica gerada, documentação mínima e exemplo CTAN | publicação/instalação de pacote; não é o melhor ponto de partida para um TCC |
| `abntexto-ufc-template-<versão>.zip` | projeto local editável | fonte completa do TCC, runtime do projeto e `abntexto-ufc-reference.pdf` | usuários locais com TeX Live e dependência `abntexto` instalada |
| `abntexto-ufc-overleaf-<versão>.zip` | projeto autocontido para Overleaf | fonte completa, revisão fixada de `abntexto.cls` e o mesmo PDF de referência | caminho mais simples para começar no Overleaf |
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
3. Use TeX Live 2026, ambiente principal de certificação da versão 3.0.1.
4. Garanta `abntexto` 1.1 ou posterior e `biblatex`/`biber`.
5. Abra e compile `main.tex` no seu editor LaTeX.

O documento canônico usa bibliografia e outros recursos que podem exigir mais de uma passagem de compilação. Um editor LaTeX configurado com Biber é o caminho mais simples.

### Pacote CTAN

`abntexto-ufc-<versão>.zip` é o arquivo canônico submetido ao CTAN. O runtime público desse pacote é `abntexto-ufc.cls`; os módulos internos de desenvolvimento são incorporados deterministicamente à classe.

Depois que a versão estiver disponível no CTAN/TeX Live, a instalação normal pela distribuição TeX é preferível a extrair manualmente esse ZIP.

## Uso mínimo

```tex
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
\ufcPrintCover
\ufcPrintTitlePage

\section{Introdução}
Texto do trabalho.
\end{document}
```

Para um exemplo completo, use `template/main.tex`. Nos bundles de Template e Overleaf, a mesma fonte pública vem acompanhada de `abntexto-ufc-reference.pdf`, um guia pedagógico completo gerado da mesma fonte certificada.

## Perfis de documento

Os valores canônicos de `type` incluem:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- `scientific-article`.

O TCC canônico explica a configuração e mostra os principais elementos, objetos e regras em contexto.

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

## Base normativa

O projeto separa quatro tipos de decisão:

1. requisito normativo ABNT aplicável;
2. requisito institucional vigente da UFC;
3. política editorial/técnica do projeto;
4. exemplo ou recomendação de uso.

A política é usar a edição técnica vigente aplicável e não reativar normas substituídas apenas por compatibilidade histórica.

Documentos principais:

- [Base normativa](docs/NORMATIVE-BASE.md)
- [Vigência normativa](docs/NORMATIVE-CURRENCY.md)
- [Guia do validador Web/Lite](validator/README.md)

A camada bibliográfica usa `biblatex-abnt` e mantém compatibilidade delimitada para requisitos da ABNT NBR 6023:2025 ainda não cobertos pela dependência publicada.

## Brasão, marcas e fontes proprietárias

O projeto **não redistribui o brasão da UFC nem outras marcas institucionais**. Também não redistribui arquivos proprietários das fontes Microsoft Arial ou Times New Roman.

Quando houver autorização para uso de uma marca institucional, o usuário fornece o ativo localmente pela configuração da classe. Os bundles públicos são gerados com `coat-of-arms = false`, e o PDF público de referência é compilado dessa mesma fonte sanitizada.

## Estrutura do repositório

| Caminho | Papel |
|---|---|
| `abntexto-ufc/` | implementação modular de desenvolvimento da classe |
| `abntexto-ufc.cls` | entrada compatível do repositório; o pacote CTAN recebe a classe monolítica gerada |
| `template/` | TCC canônico comentado e exemplos de frontmatter/chapters/backmatter |
| `validator/` | aplicação estática Web/Lite e contrato do validador |
| `standards/` | catálogo normativo, precedência e rastreabilidade |
| `tests/` | contratos estáticos, integração, regressão e fixtures |
| `tools/` | geração de bundles, validação e utilitários de engenharia |
| `docs/` | documentação de uso, normas, migração, certificação e release |
| `release/` | estado de máquina e marcadores auditáveis de release |
| `site/` | landing page publicada pelo GitHub Pages |
| `.github/workflows/` | CI, certificação, release e publicação do site |

## Como a versão é certificada

A versão 3.0.1 usa um processo fail-closed. O mesmo candidato precisa passar:

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
SHA certificado == SHA aprovado visualmente == SHA da tag v3.0.1 == SHA que gerou os arquivos publicados
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

Ao relatar um problema, informe o perfil de documento, engine LaTeX, versão da classe e um exemplo mínimo quando possível.

## Licença

O código e a documentação próprios do projeto são distribuídos sob a **LaTeX Project Public License (LPPL), versão 1.3c ou posterior**. Consulte [`LICENSE`](LICENSE).

Ativos de terceiros e marcas institucionais não são cobertos por essa licença e não são redistribuídos pelo pacote CTAN.
