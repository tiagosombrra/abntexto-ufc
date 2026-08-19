# Modelo LaTeX UFC

Template comunitário para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), com uma classe própria baseada em `abntexto`.

**Versão atual: 2.0.0 — 19/08/2026.** A linha estável 1.x permanece preservada na branch `1.x` para documentos legados.

Este projeto não é um modelo oficial da UFC. Antes da entrega, confira as orientações vigentes do Sistema de Bibliotecas, do curso, do programa e do edital aplicável.

## V2

A V2 substitui a arquitetura histórica baseada diretamente em `abntex2` por:

```text
documento.tex
    |
    +-- ufctex.cls
          +-- core.def
          +-- layout.def
          +-- modulos.def
          +-- pretextuais.def
          +-- projetos.def
          +-- objetos.def
          +-- bibliografia.def
          +-- postextuais.def
          +-- compat-abntexto.def
          +-- compat-nbr6023-2025.def
          +-- compat-v1.def
```

`ufctex` requer `abntexto` 1.1 ou superior. A política normativa e a matriz de implementação estão em `docs/NORMAS.md`.

## Uso rápido

O ponto de entrada é `documento.tex`. Para trabalhos destinados a depósito institucional, preserve `\DocumentMetadata` antes de `\documentclass`:

```tex
\DocumentMetadata{
  lang = pt-BR,
  pdfstandard = A-2b,
  pdfversion = 1.7
}

\documentclass{ufctex}

\ufcsetup{
  tipo = tccgraduacao,
  impressao = anverso,
  autor = {Nome Sobrenome},
  titulo = {Título do Trabalho},
  local = {Fortaleza},
  ano = {2026}
}
```

O perfil PDF/A-2b é a escolha técnica adotada pelo template para produzir um PDF/A validável. A exigência institucional da UFC é por PDF/A; o subtipo PDF/A-2b não é apresentado pelo projeto como uma imposição específica da Universidade.

Depois:

1. escolha o perfil do documento;
2. preencha os metadados em `\ufcsetup`;
3. edite os arquivos em `1-pre-textuais`, `2-textuais` e `3-pos-textuais`;
4. mantenha `documento.tex` como arquivo principal;
5. compile e revise o PDF final;
6. para depósito, execute também a validação PDF/A de release.

## Perfis

| Perfil | Uso |
|---|---|
| `tccgraduacao` | trabalho de graduação |
| `tccespecializacao` | trabalho de especialização |
| `dissertacao` | dissertação de mestrado |
| `tese` | tese de doutorado |
| `projeto` | projeto de pesquisa identificado |
| `projetoanonimizado` | projeto de pesquisa com identificação pessoal suprimida |

A impressão pode ser configurada como `anverso` ou `frente-verso`.

No modo `frente-verso`, as margens são espelhadas em todo o miolo: anverso com esquerda/superior de 3 cm e direita/inferior de 2 cm; verso com direita/superior de 3 cm e esquerda/inferior de 2 cm. Elementos pré-textuais, exceto a ficha catalográfica, e seções primárias são conduzidos ao próximo anverso quando necessário. Os pós-textuais controlados pela V2 usam a mesma política de início em anverso.

## Estrutura textual

O perfil normativo V2 é baseado em seções. Use:

```tex
\section{Introdução}
\subsection{Fundamentação}
\subsubsection{Detalhamento}
```

`\chapter` não faz parte do perfil V2.

## Elementos pré-textuais

Exemplo:

```tex
\pretextual
\imprimircapa
\imprimirfolhaderosto
\imprimirfolhadeaprovacao
\imprimirdedicatoria{1-pre-textuais/dedicatoria}
\imprimiragradecimentos{1-pre-textuais/agradecimentos}
\imprimirepigrafe{1-pre-textuais/epigrafe}
\imprimirresumo{1-pre-textuais/resumo}
\imprimirabstract{1-pre-textuais/abstract}
\imprimirlistadeilustracoes
\imprimirlistadetabelas
\imprimirsumario
```

O documento de referência mantém resumo e abstract na faixa de 150 a 500 palavras. As palavras-chave são apresentadas em sequência após o resumo/abstract.

A Lista de Ilustrações reúne figuras, gráficos e quadros na ordem de ocorrência. Tabelas permanecem em lista própria. Listas específicas de figuras, gráficos e quadros também estão disponíveis.

## Objetos

A API principal usa as áreas de legenda do `abntexto`:

```tex
\legend{figure}{Título da figura}
\ufcfonte{Elaboração própria.}
\ufcnota{Nota opcional.}
\label{fig:exemplo}
\begin{ufcobjeto}[here]
  \centering
  \includegraphics[width=.8\linewidth]{figuras/exemplo}
\end{ufcobjeto}
```

O mesmo padrão é usado para `table`, `quadro`, `grafico`, `codigo` e `algoritmo`, conforme o módulo habilitado.

Para ilustrações, informe sempre a fonte com `\ufcfonte{...}`, inclusive quando o conteúdo for de elaboração própria. Os exemplos normativos e a suíte de objetos validam a presença da fonte nos documentos de teste.

## Módulos opcionais

```tex
\ufcsetup{
  tabelas = tabularray,
  codigo = listings,
  algoritmos = algpseudocodex,
  glossario = glossaries,
  indice = imakeidx
}
```

Valores principais:

- `tabelas`: `nativo` ou `tabularray`;
- `codigo`: `nenhum`, `listings` ou `minted`;
- `algoritmos`: `nenhum` ou `algpseudocodex`;
- `glossario`: `nenhum` ou `glossaries`;
- `indice`: `nenhum` ou `imakeidx`.

`minted` exige o suporte externo correspondente no ambiente de compilação.

## Fonte tipográfica

O Guia UFC admite Arial ou Times New Roman. A V2 segue uma estratégia portável:

- com LuaLaTeX, usa Times New Roman quando a fonte está instalada e acessível;
- sem Times New Roman no ambiente LuaLaTeX, usa TeX Gyre Termes e emite warning;
- com pdfLaTeX, usa NewTX como família portável de desenho Times.

NewTX e TeX Gyre Termes não devem ser descritas como a própria Times New Roman. Quando o curso ou programa exigir identidade literal da família tipográfica, prefira LuaLaTeX em um ambiente que disponibilize Times New Roman e confira as fontes incorporadas no PDF final.

## Citações e referências

A V2 usa `biblatex` com Biber e estilo ABNT:

```tex
\ufcbibliografia{3-pos-textuais/referencias.bib}
```

No texto:

```tex
\textcite{chave}
\parencite{chave}
```

Ao final:

```tex
\imprimirreferencias
```

As referências são apresentadas com espaçamento simples dentro de cada entrada e um intervalo equivalente a uma linha simples entre entradas. A camada `compat-nbr6023-2025.def` mantém isolados os ajustes transitórios necessários enquanto o suporte equivalente não estiver disponível no upstream.

## Pós-textuais

```tex
\imprimirreferencias
\imprimirglossario

\appendix{Título do apêndice}
\annex{Título do anexo}

\imprimirindice
```

Apêndices, anexos, glossário e índice são opcionais.

## Compilação

Fluxo padrão:

```bash
make
```

O `Makefile` usa pdfLaTeX por padrão e executa Biber, glossários e índice quando configurados pelo documento de referência.

LuaLaTeX:

```bash
make lua
```

Validação completa de desenvolvimento:

```bash
make preflight
```

Validação pré-release, incluindo conformidade PDF/A-2b com veraPDF:

```bash
make release-preflight
```

O gate PDF/A usa a instalação local de `verapdf` quando disponível. Como alternativa, usa Docker com a imagem estável `verapdf/cli:v1.30.2`. Arquivos incorporados pelo usuário, especialmente PDFs e imagens externos, podem alterar a conformidade; por isso o PDF final de depósito deve ser validado novamente.

A suíte V2 cobre o documento de referência, PDF/A, layout, geometria real do PDF, duplex, pré-textuais, objetos, bibliografia, projetos, perfis, pós-textuais e compatibilidade pública da API da linha anterior. O gate externo usa TeX Live 2026.

## Entrega institucional UFC

Na política institucional vigente consultada em agosto de 2026:

- TCC, dissertações e teses destinados ao repositório devem ser entregues em arquivo eletrônico PDF/A;
- a folha de aprovação da versão destinada ao repositório deve ser apresentada sem as assinaturas dos membros da banca;
- a representação visual da ficha catalográfica tornou-se facultativa para TCC, dissertações e teses, e o serviço CATALOG foi descontinuado pela UFC em 2026.

Por isso, `ficha-catalografica = nao` permanece como padrão da V2. O comando de inclusão continua disponível para situações em que um programa, edital ou acervo específico ainda o solicite.

A folha de aprovação gerada pela classe contém identificação e linhas da banca, mas não insere imagens de assinaturas. Não acrescente assinaturas digitalizadas à cópia destinada ao repositório quando a orientação institucional aplicável determinar sua ausência.

## Overleaf

Importe o projeto completo e mantenha `documento.tex` como arquivo principal. Use uma versão recente do TeX Live que contenha `abntexto` 1.1 ou superior. pdfLaTeX é o caminho padrão; LuaLaTeX também é suportado.

Preserve `\DocumentMetadata` antes de `\documentclass` quando precisar gerar PDF/A. A validação independente com veraPDF deve ser feita após baixar o PDF final.

Caso use `minted`, habilite o fluxo exigido por esse pacote no ambiente de compilação.

## Migração da V1

A V2 é uma mudança de plataforma. Para documentos novos, não carregue `lib/preambulo.tex` nem use `abntex2` diretamente.

Principais mudanças:

| V1 | V2 |
|---|---|
| `\documentclass{abntex2}` | `\documentclass{ufctex}` |
| `\input{lib/preambulo}` | removido do documento principal |
| configuração histórica distribuída | `\ufcsetup{...}` |
| `\chapter` como nível principal | `\section` |
| helpers `\UFCfig`, `\UFCtab`, `\UFCqua` | `\legend` + `\ufcfonte` + `ufcobjeto` |
| configuração bibliográfica no preâmbulo | `\ufcbibliografia{arquivo.bib}` |

A camada `compat-v1.def` existe para facilitar transição e regressão, mas não define o estilo recomendado para documentos novos.

## Compatibilidade

A V2 é validada com pdfLaTeX e LuaLaTeX. O desenvolvimento local pode usar uma distribuição mais nova, mas a certificação do projeto é feita no ambiente definido pelo GitHub Actions com TeX Live 2026 e `abntexto` estável.

## Normas

Consulte `docs/NORMAS.md` para:

- edições normativas adotadas;
- precedência entre ABNT e requisitos institucionais;
- mapa norma → implementação;
- políticas UFC verificadas em 2026;
- patches temporários de compatibilidade;
- política dos gates de validação.

Não declare conformidade apenas porque o documento compilou ou porque o PDF contém metadados PDF/A. A revisão final deve considerar as exigências específicas aplicáveis ao trabalho e, para depósito, a validação independente do arquivo final.

## Linha 1.x

A última série baseada diretamente em `abntex2` permanece disponível na branch `1.x` para manutenção e documentos legados. Novos documentos devem usar a V2.

## Licença

Consulte `LICENSE`.
