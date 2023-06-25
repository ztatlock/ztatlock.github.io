FILES := https://cs.washington.edu/homes/ztatlock/WEBFILES
PAGES := $(patsubst %.dj,%.html,$(wildcard *.dj))

%.html: %.dj $(wildcard templates/*)
	$(eval TITLE := $(shell \
			head -n 1 '$<' \
			| tr -d '#[]' \
			| sed 's#^[[:blank:]]*##' \
			| sed 's#[[:blank:]]*$$##'))
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
	@([ -f "$*.meta" ] && cat "$*.meta" || true) >> $@
	@cat templates/HEAD.2 >> $@
	@cat $< templates/REFS \
		| sed 's#__WEBFILES__#$(FILES)#' \
		| djot \
		>> $@
	@cat templates/FOOT >> $@

.PHONY: all
all: $(PAGES) sitemap.txt sitemap.xml

sitemap.txt: $(wildcard *.html) $(wildcard pubs/*/*.pdf)
	@echo "BUILD : $@"
	@rm -f $@
	@for page in *.html pubs/*/*.pdf; do \
		echo "https://ztatlock.net/$${page}"; \
	done >> $@

sitemap.xml: $(wildcard *.html) $(wildcard pubs/*/*.pdf)
	@echo "BUILD : $@"
	@echo '<?xml version="1.0" encoding="UTF-8"?>' > $@
	@echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' >> $@
	@for page in *.html pubs/*/*.pdf; do \
		printf '<url>\n  <loc>%s</loc>\n  <lastmod>%s</lastmod>\n</url>\n' \
			"https://ztatlock.net/$${page}" \
			"$$(git ls-files --error-unmatch "$${page}" &> /dev/null \
			 && git log -1 --pretty="format:%cs" "$${page}" \
			 || date +%Y-%m-%d)"; \
	done >> $@
	@echo '</urlset>' >> $@

.PHONY: clean
clean:
	rm -f $(PAGES)
	rm -f sitemap.txt sitemap.xml
