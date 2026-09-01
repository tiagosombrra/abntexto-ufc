########################################################################
## abntexto-ufc development and validation entry points               ##
########################################################################

VERSION := 3.0.0
TEMPLATE_DIR := template
DOCUMENT ?= main
ENGINE ?= pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error -file-line-error
TEX_ENV := TEXINPUTS=..//:

.PHONY: all pdf compile lua version clean reference-assets \
	check release-check preflight release-preflight

all: compile
pdf: compile

version:
	@echo "$(VERSION)"

reference-assets:
	@python3 tools/fetch-reference-images.py

compile:
	@echo "Compiling $(TEMPLATE_DIR)/$(DOCUMENT).tex with $(ENGINE)..."
	@cd "$(TEMPLATE_DIR)" && $(TEX_ENV) $(ENGINE) $(LATEXFLAGS) "$(DOCUMENT).tex"
	@if [ -s "$(TEMPLATE_DIR)/$(DOCUMENT).bcf" ] && grep -q '<bcf:datasource' "$(TEMPLATE_DIR)/$(DOCUMENT).bcf"; then \
		echo "Running Biber..."; \
		cd "$(TEMPLATE_DIR)" && biber "$(DOCUMENT)"; \
	else \
		echo "Biber not required."; \
	fi
	@if [ -s "$(TEMPLATE_DIR)/$(DOCUMENT).glo" ]; then \
		echo "Running makeglossaries..."; \
		cd "$(TEMPLATE_DIR)" && makeglossaries "$(DOCUMENT)"; \
	else \
		echo "Glossary processing not required."; \
	fi
	@if [ -s "$(TEMPLATE_DIR)/$(DOCUMENT).idx" ]; then \
		echo "Running makeindex..."; \
		cd "$(TEMPLATE_DIR)" && makeindex "$(DOCUMENT)"; \
	else \
		echo "Index processing not required."; \
	fi
	@cd "$(TEMPLATE_DIR)" && $(TEX_ENV) $(ENGINE) $(LATEXFLAGS) "$(DOCUMENT).tex"
	@cd "$(TEMPLATE_DIR)" && $(TEX_ENV) $(ENGINE) $(LATEXFLAGS) "$(DOCUMENT).tex"
	@echo "Document build completed successfully: $(TEMPLATE_DIR)/$(DOCUMENT).pdf"

lua:
	@$(MAKE) clean
	@$(MAKE) ENGINE=lualatex compile

check:
	@python3 tests/run.py --mode pr

release-check:
	@python3 tests/run.py --mode release

preflight: check
	@echo "Development preflight completed."

release-preflight: release-check
	@echo "Release preflight completed."

clean:
	@echo "Cleaning generated document artifacts..."
	@rm -f \
		"$(TEMPLATE_DIR)/$(DOCUMENT).aux" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).bbl" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).bcf" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).blg" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).fdb_latexmk" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).fls" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).glg" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).glo" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).gls" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).idx" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).ilg" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).ind" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).loa" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).loc" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).lof" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).lol" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).lot" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).log" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).nlo" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).nls" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).out" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).pdf" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).run.xml" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).synctex.gz" \
		"$(TEMPLATE_DIR)/$(DOCUMENT).toc"
	@rm -rf "$(TEMPLATE_DIR)/_minted-$(DOCUMENT)" _minted-*
	@echo "Generated artifacts removed."
