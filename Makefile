########################################################################
## Modelo de Trabalho Acadêmico UFC / abnTeX2                          ##
## Revisão normativa e técnica: Tiago Guimarães Sombra (2026).         ##
## Build reproduzível com Biber, glossários e índice.                   ##
########################################################################

filename := documento
ENGINE ?= pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all compile pdf lua preflight clean

all: compile
pdf: compile

compile:
	@echo "Compilando $(filename).tex com $(ENGINE) + Biber..."
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	biber $(filename)
	makeglossaries $(filename)
	makeindex $(filename)
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	@echo "Processo finalizado com sucesso."

# Valida o fluxo Unicode/OpenType sem mudar o padrão do Overleaf.
lua:
	$(MAKE) clean
	$(MAKE) ENGINE=lualatex compile

# Preflight local: compila e reprova warnings/caixas excedentes no log final.
# Dependências de sistema como pdffonts são verificadas apenas quando disponíveis.
preflight: compile
	@echo "Verificando warnings finais..."
	@if grep -E "LaTeX Warning:|Package [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox" $(filename).log; then \
		echo "Preflight falhou: revise os avisos acima."; exit 1; \
	else \
		echo "Log final sem warnings estruturais."; \
	fi
	@if command -v pdffonts >/dev/null 2>&1; then \
		if pdffonts $(filename).pdf | tail -n +3 | awk 'NF && $$6 != "yes" {bad=1} END{exit bad}'; then \
			echo "Fontes do PDF incorporadas."; \
		else \
			echo "Preflight falhou: há fonte não incorporada."; exit 1; \
		fi; \
	fi

clean:
	@echo "Limpando arquivos auxiliares..."
	@rm -f *.out *.aux *.alg *.acr *.dvi *.gls *.log *.bbl *.blg *.bcf *.run.xml
	@rm -f *.ntn *.not *.lof *.lot *.toc *.loa *.lsg *.nlo *.nls *.ilg *.ind
	@rm -f *.glg *.glo *.xdy *.acn *.idx *.loq *.lol *.fls *.fdb_latexmk *.synctex.gz *~
	@rm -f $(filename).pdf
	@echo "Processo finalizado com sucesso."
