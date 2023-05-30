FILES := https://cs.washington.edu/homes/ztatlock/WEBFILES
PAGES := $(patsubst %.dj,%.html,$(wildcard *.dj))

%.html: %.dj $(wildcard templates/*)
	$(eval TITLE := $(shell \
			head -n 1 '$<' \
			| tr -d '#[]' \
			| sed 's#^[[:blank:]]*##' \
			| sed 's#[[:blank:]]*$$##'))
	@printf "BUILD : %-35s %s\n" "$@" "$(TITLE)"
	@cat templates/HEAD.1 \
		| sed 's#__TITLE__#$(TITLE)#' \
		> $@
	@([ -f "$*.meta" ] && cat "$*.meta" || true) >> $@
	@cat templates/HEAD.2 >> $@
	@cat $< templates/REFS \
		| sed 's#__WEBFILES__#$(FILES)#' \
		| djot \
		>> $@
	@cat templates/FOOT >> $@

.PHONY: all
all: $(PAGES) sitemap.txt

sitemap.txt: $(wildcard *.html)
	@echo "BUILD : $@"
	@rm -f $@
	@for page in *.html; do \
		echo "https://ztatlock.net/$${page}"; \
	done >> $@
	@for paper in pubs/*/*.pdf; do \
		echo "https://ztatlock.net/$${paper}"; \
	done >> $@

.PHONY: clean
clean:
	rm -f $(PAGES)
	rm -f sitemap.txt
