########################################################################
## Modelo de Trabalho Acadêmico UFC / abnTeX2                          ##
## Revisão normativa e técnica: Tiago Guimarães Sombra (2026).         ##
## Build reproduzível com Biber, glossários e índice.                   ##
########################################################################

VERSION := 1.1.2
filename := documento
ENGINE ?= pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error -file-line-error
V2_LAYOUT_FIXTURES := tests/normativa/layout-anverso.tex tests/normativa/layout-frente-verso.tex
V2_PRETEXTUAL_FIXTURES := tests/normativa/pretextuais-trabalho.tex tests/normativa/pretextuais-projeto-anonimo.tex

.PHONY: all compile pdf lua preflight v2-layout-check v2-pretextual-check version clean

all: compile
pdf: compile

version:
	@echo "$(VERSION)"

compile:
	@echo "Compilando $(filename).tex com $(ENGINE) + Biber..."
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	biber $(filename)
	makeglossaries $(filename)
	makeindex $(filename)
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	$(ENGINE) $(LATEXFLAGS) $(filename).tex
	@echo "Processo finalizado com sucesso."

# Validate the Unicode/OpenType path without changing the default Overleaf flow.
lua:
	$(MAKE) clean
	$(MAKE) ENGINE=lualatex compile

# Compile the isolated v2 layout fixtures with both supported engines.
v2-layout-check:
	@set -e; \
	for engine in pdflatex lualatex; do \
		for fixture in $(V2_LAYOUT_FIXTURES); do \
			echo "Validando $$fixture com $$engine..."; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-layout.log 2>&1; then \
				cat /tmp/ufctex-v2-layout.log; exit 1; \
			fi; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-layout.log 2>&1; then \
				cat /tmp/ufctex-v2-layout.log; exit 1; \
			fi; \
		done; \
	done

# Validate pre-textual ordering, TOC isolation and anonymized-project output.
v2-pretextual-check:
	@set -e; \
	for engine in pdflatex lualatex; do \
		for fixture in $(V2_PRETEXTUAL_FIXTURES); do \
			echo "Validando $$fixture com $$engine..."; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-pretextual.log 2>&1; then \
				cat /tmp/ufctex-v2-pretextual.log; exit 1; \
			fi; \
			if ! $$engine $(LATEXFLAGS) $$fixture > /tmp/ufctex-v2-pretextual.log 2>&1; then \
				cat /tmp/ufctex-v2-pretextual.log; exit 1; \
			fi; \
		done; \
	done
	@if grep -Eiq 'dedicat[oó]ria|agradecimentos|resumo|abstract|lista de' pretextuais-trabalho.toc; then \
		echo "Preflight V2 falhou: elemento pré-textual entrou no Sumário."; \
		cat pretextuais-trabalho.toc; exit 1; \
	fi
	@grep -Eiq 'Introdu' pretextuais-trabalho.toc || \
		(echo "Preflight V2 falhou: seção textual ausente do Sumário."; exit 1)
	@if command -v pdftotext >/dev/null 2>&1; then \
		if pdftotext pretextuais-trabalho.pdf - | grep -Eiq '^Dedicat[oó]ria$$'; then \
			echo "Preflight V2 falhou: dedicatória recebeu título."; exit 1; \
		fi; \
		if pdftotext pretextuais-projeto-anonimo.pdf - | grep -Fq 'AUTOR SIGILOSO TESTE'; then \
			echo "Preflight V2 falhou: autor vazou no projeto anonimizado."; exit 1; \
		fi; \
		if pdftotext pretextuais-projeto-anonimo.pdf - | grep -Fq 'ORIENTADOR SIGILOSO TESTE'; then \
			echo "Preflight V2 falhou: orientador vazou no projeto anonimizado."; exit 1; \
		fi; \
		pdftotext pretextuais-projeto-anonimo.pdf - | grep -Fq 'PROJETO-ANONIMO-001' || \
			(echo "Preflight V2 falhou: identificador anonimizado ausente."; exit 1); \
	fi

# Local preflight: compile and reject warnings or overflowing boxes in the final log.
# Known upstream deprecations from abnTeX2 1.9.7 are filtered narrowly.
# System dependencies such as pdffonts are checked only when available.
preflight: compile v2-layout-check v2-pretextual-check
	@echo "Verificando warnings finais..."
	@warnings=$$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox' $(filename).log | \
		grep -vF -e "Package babel Warning: Name 'brazil' is deprecated." \
		          -e 'Class memoir Warning: \settocpreprocessor is marked deprecated and will be' || true); \
	if [ -n "$$warnings" ]; then \
		printf '%s\n' "$$warnings"; \
		echo "Preflight falhou: revise os avisos acima."; exit 1; \
	else \
		echo "Log final sem warnings estruturais não reconhecidos."; \
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
	@rm -f layout-anverso.pdf layout-frente-verso.pdf
	@rm -f pretextuais-trabalho.pdf pretextuais-projeto-anonimo.pdf
	@rm -f $(filename).pdf
	@echo "Processo finalizado com sucesso."
