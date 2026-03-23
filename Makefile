.DEFAULT_GOAL := build

CHECK_ENV := scripts/check_env.sh
INDEX_NOW := scripts/index-now.sh
MKPUB := scripts/mkpub.sh

BUILD_SITE_MODULE := scripts.build_site
RENDER_ROUTES_MODULE := scripts.render_routes
VALIDATE_SITE_MODULE := scripts.validate_build
PUB_INVENTORY_MODULE := scripts.build_pub_inventory

ROUTES_OUT := state/routes.json

INVENTORY_PREVIEW_OUT := state/inventory
INVENTORY_WEBFILES_OUT := /Users/ztatlock/Desktop/WEBFILES/inventory
INVENTORY_OUT ?= $(INVENTORY_PREVIEW_OUT)
YCF ?=

.PHONY: all
all: build

.PHONY: build
build:
	@python3 -m $(BUILD_SITE_MODULE) --root .

.PHONY: check
check: build
	@python3 -m $(VALIDATE_SITE_MODULE) --root .

.PHONY: routes
routes:
	@mkdir -p "$(dir $(ROUTES_OUT))"
	@python3 -m $(RENDER_ROUTES_MODULE) --root . > "$(ROUTES_OUT)"

.PHONY: help
help:
	@printf '%s\n' \
		'make build' \
		'make check' \
		'make routes' \
		'make test' \
		'make env-check' \
		'make inventory [INVENTORY_OUT=/path/to/out-dir]' \
		'make inventory-webfiles' \
		'make mkpub YCF=YEAR-CONF-SYS' \
		'make index-now' \
		'make clean'

.PHONY: test
test:
	@python3 -m unittest \
		tests/test_build_pub_inventory.py \
		tests/test_publication_record.py \
		tests/test_scaffold_publication.py \
		tests/test_route_model.py \
		tests/test_route_discovery.py \
		tests/test_source_validate.py \
		tests/test_page_metadata.py \
		tests/test_page_renderer.py \
		tests/test_site_builder.py \
		tests/test_sitemap_builder.py \
		tests/test_artifact_validate.py \
		tests/test_build_validate.py \
		tests/test_people_registry.py \
		tests/test_people_refs.py \
		tests/test_people_refs_audit.py \
		tests/test_djot_refs.py

.PHONY: env-check
env-check:
	@bash $(CHECK_ENV)

.PHONY: inventory
inventory:
	@python3 -m $(PUB_INVENTORY_MODULE) --out-dir "$(INVENTORY_OUT)"

.PHONY: inventory-webfiles
inventory-webfiles:
	@python3 -m $(PUB_INVENTORY_MODULE) --out-dir "$(INVENTORY_WEBFILES_OUT)"

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
	rm -rf build
	rm -f "$(ROUTES_OUT)"
	rm -f state/site.refs.djot
