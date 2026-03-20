FILES          := https://cs.washington.edu/homes/ztatlock/WEBFILES
ALL_DJ         := $(wildcard *.dj)
GENERATED_HTML := $(patsubst %.dj,%.html,$(ALL_DJ))

DRAFT_DJ       := $(shell rg -l '^\# DRAFT$$' $(ALL_DJ) 2>/dev/null || true)
PUBLIC_DJ      := $(filter-out $(DRAFT_DJ),$(ALL_DJ))

PAGES          := $(patsubst %.dj,%.html,$(PUBLIC_DJ))
DRAFT_PAGES    := $(patsubst %.dj,%.html,$(DRAFT_DJ))
STATIC_HTML    := $(filter-out 404.html,\
                   $(filter-out $(GENERATED_HTML),$(wildcard *.html)))

SITEMAP_PDFS   := $(wildcard pubs/*/*.pdf)
SITEMAP_HTML   := $(sort $(STATIC_HTML) $(PAGES))

CHECK          := scripts/check.sh
CHECK_ENV      := scripts/check_env.sh
INDEX_NOW      := scripts/index-now.sh
MKPUB          := scripts/mkpub.sh
PUB_INVENTORY  := scripts/build_pub_inventory.py
PAGE_META      := scripts/page_metadata.py
PAGE_SOURCE    := scripts/page_source.py
RENDER_META    := scripts/render_meta.py
VALIDATE_SITE  := scripts/validate_site.py

INVENTORY_PREVIEW_OUT  := state/inventory
INVENTORY_WEBFILES_OUT := /Users/ztatlock/Desktop/WEBFILES/inventory

INVENTORY_OUT ?= $(INVENTORY_PREVIEW_OUT)
YCF           ?=

.SECONDEXPANSION:
%.html: %.dj $(wildcard templates/*) $(PAGE_META) $(PAGE_SOURCE) $(RENDER_META) manifests/page-metadata.json manifests/publication-metadata.json
	$(eval TITLE := $(shell python3 $(PAGE_SOURCE) title --root . --page "$*"))
	@printf "BUILD : %-35s %s\n" "$@" "$(TITLE)"
	@if [ "$@" = "index.html" ]; then \
		cat templates/HEAD.1 \
		| sed 's#__TITLE__#$(TITLE)#' \
		| sed 's#__CANON__#https://ztatlock.net/#' \
		> $@; \
	else \
		cat templates/HEAD.1 \
		| sed 's#__TITLE__#$(TITLE)#' \
		| sed 's#__CANON__#https://ztatlock.net/$@#' \
		> $@; \
	fi
	@python3 $(RENDER_META) --root . --page "$*" --title "$(TITLE)" >> $@
	@cat templates/HEAD.2 >> $@
	@python3 $(PAGE_SOURCE) body --root . --page "$*" \
		| cat - templates/REFS \
		| sed 's#__WEBFILES__#$(FILES)#' \
		| djot \
		>> $@
	@cat templates/FOOT >> $@

.PHONY: all
all: $(PAGES) sitemap.txt sitemap.xml

.PHONY: help
help:
	@printf '%s\n' \
		'make all' \
		'make drafts' \
		'make check' \
		'make validate-site' \
		'make env-check' \
		'make inventory [INVENTORY_OUT=/path/to/out-dir]' \
		'make inventory-webfiles' \
		'make mkpub YCF=YEAR-CONF-SYS' \
		'make index-now' \
		'make clean'

sitemap.txt: $(SITEMAP_HTML) $(SITEMAP_PDFS)
	@echo "BUILD : $@"
	@rm -f $@
	@for page in $(SITEMAP_HTML) $(SITEMAP_PDFS); do \
		echo "https://ztatlock.net/$${page}"; \
	done >> $@

sitemap.xml: $(SITEMAP_HTML) $(SITEMAP_PDFS)
	@echo "BUILD : $@"
	@echo '<?xml version="1.0" encoding="UTF-8"?>' > $@
	@echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' >> $@
	@for page in $(SITEMAP_HTML) $(SITEMAP_PDFS); do \
		printf '<url>\n  <loc>%s</loc>\n  <lastmod>%s</lastmod>\n</url>\n' \
			"https://ztatlock.net/$${page}" \
			"$$(git ls-files --error-unmatch "$${page}" >/dev/null 2>&1 \
			 && git log -1 --pretty="format:%cs" "$${page}" \
			 || date +%Y-%m-%d)"; \
	done >> $@
	@echo '</urlset>' >> $@

.PHONY: drafts
drafts: $(DRAFT_PAGES)

.PHONY: check
check:
	@bash $(CHECK)

.PHONY: env-check
env-check:
	@bash $(CHECK_ENV)

.PHONY: validate-site
validate-site:
	@python3 $(VALIDATE_SITE) --root .

.PHONY: inventory
inventory:
	@python3 $(PUB_INVENTORY) --out-dir "$(INVENTORY_OUT)"

.PHONY: inventory-webfiles
inventory-webfiles:
	@python3 $(PUB_INVENTORY) --out-dir "$(INVENTORY_WEBFILES_OUT)"

.PHONY: mkpub
mkpub:
	@[ -n "$(YCF)" ] || { \
		echo "Usage: make mkpub YCF=YEAR-CONF-SYS" >&2; \
		exit 1; \
	}
	@bash $(MKPUB) "$(YCF)"

.PHONY: index-now
index-now:
	@bash $(INDEX_NOW)

.PHONY: clean
clean:
	rm -f $(GENERATED_HTML)
	rm -f sitemap.txt sitemap.xml
