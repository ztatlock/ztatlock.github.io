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
PUBLICATION_RECORD := scripts/publication_record.py
RENDER_REFS_MODULE := scripts.render_site_refs
RENDER_PAGE_HTML_MODULE := scripts.render_page_html
VALIDATE_SITE_MODULE := scripts.validate_site
BUILD_PREVIEW_MODULE := scripts.build_preview_site
RENDER_ROUTES_MODULE := scripts.render_routes
VALIDATE_PREVIEW_MODULE := scripts.validate_preview_build
RENDER_PAGE_HTML := scripts/render_page_html.py
RENDER_REFS    := scripts/render_site_refs.py
VALIDATE_SITE  := scripts/validate_site.py
BUILD_PREVIEW  := scripts/build_preview_site.py
RENDER_ROUTES  := scripts/render_routes.py
VALIDATE_PREVIEW := scripts/validate_preview_build.py
RENDERED_REFS  := state/site.refs.djot
ROUTES_PREVIEW := state/routes-preview.json

PUBLICATION_INPUTS := $(wildcard pubs/*/*)
SITE_DATA         := $(wildcard site/data/*)
SITEBUILD_MODULES := $(wildcard scripts/sitebuild/*.py)

INVENTORY_PREVIEW_OUT  := state/inventory
INVENTORY_WEBFILES_OUT := /Users/ztatlock/Desktop/WEBFILES/inventory

INVENTORY_OUT ?= $(INVENTORY_PREVIEW_OUT)
YCF           ?=

.SECONDEXPANSION:
$(RENDERED_REFS): $(RENDER_REFS) $(SITE_DATA) $(SITEBUILD_MODULES) templates/REFS
	@mkdir -p "$(dir $@)"
	@python3 -m $(RENDER_REFS_MODULE) --root . > $@

$(ROUTES_PREVIEW): $(RENDER_ROUTES) $(SITEBUILD_MODULES) $(PUBLICATION_INPUTS) $(SITE_DATA) $(wildcard *.dj) $(wildcard *.html) Makefile
	@mkdir -p "$(dir $@)"
	@python3 -m $(RENDER_ROUTES_MODULE) --root . > $@

%.html: %.dj Makefile $(wildcard templates/*) $(PAGE_META) $(PAGE_SOURCE) $(PUBLICATION_RECORD) $(RENDER_PAGE_HTML) $(RENDERED_REFS) $(PUBLICATION_INPUTS) $(SITE_DATA) $(SITEBUILD_MODULES)
	@printf "BUILD : %-35s\n" "$@"
	@if [ "$@" = "index.html" ]; then \
		CANON="https://ztatlock.net/"; \
	else \
		CANON="https://ztatlock.net/$@"; \
	fi; \
	python3 -m $(RENDER_PAGE_HTML_MODULE) \
		--root . \
		--page "$*" \
		--canonical-url "$$CANON" \
		--refs-file "$(RENDERED_REFS)" \
		--webfiles-url "$(FILES)" \
		> $@

.PHONY: all
all: $(PAGES) sitemap.txt sitemap.xml

.PHONY: help
help:
	@printf '%s\n' \
		'make all' \
		'make drafts' \
		'make test' \
		'make check' \
		'make build-preview' \
		'make check-preview' \
		'make routes-preview' \
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

.PHONY: build-preview
build-preview:
	@python3 -m $(BUILD_PREVIEW_MODULE) --root .

.PHONY: check-preview
check-preview: build-preview
	@python3 -m $(VALIDATE_PREVIEW_MODULE) --root .

.PHONY: routes-preview
routes-preview: $(ROUTES_PREVIEW)

.PHONY: test
test:
	@python3 -m unittest \
		tests/test_route_model.py \
		tests/test_route_discovery.py \
		tests/test_page_renderer.py \
		tests/test_sitemap_builder.py \
		tests/test_artifact_validate.py \
		tests/test_preview_validate.py \
		tests/test_people_registry.py \
		tests/test_people_refs.py \
		tests/test_people_refs_audit.py \
		tests/test_djot_refs.py

.PHONY: env-check
env-check:
	@bash $(CHECK_ENV)

.PHONY: validate-site
validate-site:
	@python3 -m $(VALIDATE_SITE_MODULE) --root .

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
