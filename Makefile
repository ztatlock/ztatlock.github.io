FILES := https://cs.washington.edu/homes/ztatlock/WEBFILES
PAGES := $(patsubst %.dj,%.html,$(wildcard *.dj))

%.html: %.dj templates/REFS templates/HEAD templates/FOOT
	$(eval TITLE := $(shell \
			head -n 1 '$<' \
			| tr -d '#[]' \
			| sed 's#^[[:blank:]]*##' \
			| sed 's#[[:blank:]]*$$##'))
	@printf "BUILD : %-35s %s\n" "$@" "$(TITLE)"
	@cat templates/HEAD \
		| sed 's#TITLE#$(TITLE)#' \
		> $@
	@cat $< templates/REFS \
		| sed 's#__WEBFILES__#$(FILES)#' \
		| djot \
		>> $@
	@cat templates/FOOT >> $@

.PHONY: all
all: $(PAGES)

.PHONY: clean
clean:
	rm -f $(PAGES)
