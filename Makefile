.DEFAULT_GOAL := build

CHECK_ENV := scripts/check_env.sh
INDEX_NOW := scripts/index-now.sh
MKPUB := scripts/mkpub.sh

BUILD_SITE_MODULE := scripts.build_site
RENDER_ROUTES_MODULE := scripts.render_routes
VALIDATE_SITE_MODULE := scripts.validate_build
PUB_INVENTORY_MODULE := scripts.build_pub_inventory

ROUTES_OUT := state/routes.json

INVENTORY_STATE_OUT := state/inventory
INVENTORY_ARCHIVE_OUT := $(HOME)/Desktop/WEBFILES/inventory
INVENTORY_OUT ?= $(INVENTORY_STATE_OUT)
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
		'make inventory-webfiles (personal archive refresh)' \
		'make mkpub YCF=YEAR-CONF-SYS' \
		'make index-now' \
		'make clean'

.PHONY: test
test:
	@python3 -m unittest discover -s tests -p 'test_*.py' -t .

.PHONY: env-check
env-check:
	@bash $(CHECK_ENV)

.PHONY: inventory
inventory:
	@python3 -m $(PUB_INVENTORY_MODULE) --out-dir "$(INVENTORY_OUT)"

.PHONY: inventory-webfiles
inventory-webfiles:
	@python3 -m $(PUB_INVENTORY_MODULE) --out-dir "$(INVENTORY_ARCHIVE_OUT)"

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
