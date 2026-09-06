# abntexto-ufc

Template LaTeX comunitário para trabalhos acadêmicos da Universidade Federal do Ceará (UFC), construído sobre o `abntexto`.

> **Importante:** este é um projeto comunitário. Ele não deve ser apresentado como template oficial ou homologado pela UFC sem manifestação institucional explícita.

## Qual versão devo usar?

A versão estável publicada atualmente é a **v2.1.0**. Se você está escrevendo um TCC, trabalho de especialização, dissertação, tese ou projeto de pesquisa agora, use essa release em vez de clonar a branch `main`.

A v3.0.0 está em desenvolvimento e ainda não foi publicada. Ela introduz a nova classe `abntexto-ufc` e outros recursos, mas não deve ser usada como versão estável até a publicação da release.

- Release estável: <https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v2.1.0>
- Template para Overleaf: <https://github.com/tiagosombrra/abntexto-ufc/releases/download/v2.1.0/modelo-latex-ufc-overleaf-2.1.0.zip>
- Template para uso local: <https://github.com/tiagosombrra/abntexto-ufc/releases/download/v2.1.0/modelo-latex-ufc-2.1.0.zip>
- PDF de referência da v2.1.0: <https://github.com/tiagosombrra/abntexto-ufc/releases/download/v2.1.0/ufctex-2.1.0-reference.pdf>

## Usando no Overleaf

Esta é a forma mais simples de começar.

1. Baixe `modelo-latex-ufc-overleaf-2.1.0.zip` pelo link acima.
2. No Overleaf, escolha **New Project > Upload Project**.
3. Envie o arquivo ZIP sem descompactá-lo.
4. Confirme `documento.tex` como arquivo principal do projeto, caso o Overleaf não o selecione automaticamente.
5. Compile o projeto.
6. Substitua os dados de exemplo pelos dados do seu trabalho e edite os arquivos das pastas de conteúdo.

O bundle do Overleaf inclui a dependência `abntexto.cls` necessária para a versão estável, evitando depender da versão instalada globalmente no serviço.

## Usando localmente

Recomenda-se uma instalação atual do **TeX Live 2026**.

1. Baixe `modelo-latex-ufc-2.1.0.zip`.
2. Descompacte o arquivo em uma pasta de trabalho.
3. Abra um terminal nessa pasta.
4. Compile com:

```bash
make compile
```

O documento principal é `documento.tex`. O PDF gerado é `documento.pdf`.

Para remover arquivos auxiliares de compilação:

```bash
make clean
```

A bibliografia usa `biblatex` e `biber`; o `Makefile` executa o fluxo necessário durante a compilação.

## Estrutura do template estável

```text
documento.tex
1-pre-textuais/
2-textuais/
3-pos-textuais/
figuras/
```

Use essa organização como ponto de partida:

- `documento.tex`: configuração geral e montagem do documento;
- `1-pre-textuais/`: errata, dedicatória, agradecimentos, epígrafe, resumo, abstract e listas;
- `2-textuais/`: introdução, fundamentação, metodologia, resultados, conclusão e demais seções do texto;
- `3-pos-textuais/`: referências, apêndices e anexos;
- `figuras/`: imagens usadas no trabalho.

Evite concentrar todo o conteúdo em `documento.tex`. Manter capítulos e elementos em arquivos separados facilita revisão, colaboração e controle de versão.

## Configuração básica

Na versão estável v2.1.0, a classe é `ufctex`. Um exemplo reduzido para uma tese é:

```tex
\documentclass{ufctex}

\ufcsetup{
  tipo = tese,
  impressao = anverso,
  capa = auto,
  ficha-catalografica = nao,
  brasao = sim,
  fonte = times,
  fonte-estrita = nao,
  programa-doutorado = {Programa de Pós-Graduação em Ciência da Computação},
  titulo-doutor = {Ciência da Computação},
  area-doutorado = {Computação Gráfica},
  autor = {Nome Completo do Autor},
  titulo = {Título do Trabalho},
  local = {Fortaleza},
  ano = {2026},
  orientador = {Prof. Dr. Nome do Orientador},
  tabelas = nativo,
  codigo = nenhum,
  algoritmos = nenhum,
  glossario = nenhum,
  indice = nenhum
}
```

Edite apenas os valores correspondentes ao seu trabalho. O template distribuído contém um exemplo mais completo, com os demais campos e elementos opcionais.

## Tipos de trabalho disponíveis na v2.1.0

| Valor de `tipo` | Uso |
|---|---|
| `tccgraduacao` | trabalho de graduação |
| `tccespecializacao` | trabalho de especialização |
| `dissertacao` | dissertação de mestrado |
| `tese` | tese de doutorado |
| `projeto` | projeto de pesquisa identificado |
| `projetoanonimizado` | projeto de pesquisa com dados pessoais suprimidos |

A impressão pode ser configurada como `anverso` ou `frente-verso`.

## Referências bibliográficas

As referências ficam em:

```text
3-pos-textuais/referencias.bib
```

No arquivo `.bib`, cada obra recebe uma chave que pode ser usada nas citações do texto. A versão estável usa `biblatex-abnt` e `biber`.

Ao adicionar ou alterar referências, faça uma compilação completa pelo `make compile` para que o Biber seja executado quando necessário.

## Figuras, tabelas, código e algoritmos

O template de exemplo já contém casos de uso desses elementos. Em geral:

- coloque as imagens em `figuras/`;
- mantenha título, fonte e nota associados ao objeto correspondente;
- habilite módulos de código, algoritmos, glossário ou índice somente quando forem necessários;
- para tabelas, escolha o backend previsto pela configuração do template em vez de misturar implementações sem necessidade.

O PDF de referência da release é a melhor forma de visualizar os elementos disponíveis antes de adaptá-los ao seu trabalho.

## Fontes

A configuração suporta Times New Roman e Arial conforme a política do template. Em ambientes portáteis, a classe pode usar famílias de fallback compatíveis quando o modo de fonte estrita estiver desativado.

As fontes proprietárias da Microsoft **não são distribuídas** pelo projeto. Se você precisar exigir a família literal instalada no computador, use a configuração de fonte estrita prevista pela versão do template e garanta que a fonte esteja disponível no sistema.

## Ficha catalográfica

Na versão estável, a ficha catalográfica é opcional e pode ser inserida como PDF externo quando aplicável. Gere a ficha pelo serviço institucional adequado e siga o exemplo incluído no template.

## Apêndices e anexos

Use apêndice para material elaborado pelo próprio autor e anexo para material externo incorporado ao trabalho. Os exemplos distribuídos mostram como inserir ambos e como manter a identificação e a fonte do material externo.

## Problemas comuns

| Problema | O que verificar |
|---|---|
| Referências não aparecem | compile pelo `make compile` ou confirme se o Biber foi executado |
| Imagem não encontrada | confira o caminho e se o arquivo foi incluído na pasta do projeto |
| Fonte literal indisponível | desative o modo estrito ou instale legalmente a fonte requerida no sistema |
| Overleaf não compila após upload | confirme que `documento.tex` é o arquivo principal e use o bundle específico para Overleaf |
| Mudança de versão quebra comandos | confira se o projeto está usando a mesma release do template; não misture APIs da v2 e da v3 |

## Desenvolvimento da v3

A v3.0.0 ainda está em desenvolvimento. Ela usa a classe `abntexto-ufc` e uma API diferente da v2.1.0. O perfil de artigo científico também está sendo desenvolvido nessa linha e ainda não faz parte de uma release estável.

Se você está contribuindo com a v3, consulte:

- `docs/ROADMAP-V3.0.0.md`;
- `docs/HANDOFF-V3.0.0.md`;
- `docs/MIGRATING-TO-V3.md`.

O histórico de implementação, resultados de CI, decisões normativas, issues e evidências de regressão ficam nesses documentos e no GitHub, não neste guia de uso.

## Licença

O código e a documentação do projeto são distribuídos conforme `LICENSE` (LPPL 1.3c ou posterior). Ativos institucionais e arquivos de terceiros podem possuir condições próprias de uso e distribuição.
