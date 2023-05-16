FILES := https://cs.washington.edu/homes/ztatlock/WEBFILES
PAGES := $(patsubst %.dj,%.html,$(wildcard *.dj))

%.html: %.dj REFS HEAD FOOT
	$(eval TITLE := $(shell \
			head -n 1 '$<' \
			| tr -d '#[]' \
			| sed 's#^[[:blank:]]*##' \
			| sed 's#[[:blank:]]*$$##'))
	@printf "BUILD : %-30s %s\n" "$@" "$(TITLE)"
	@cat HEAD \
		| sed 's#TITLE#$(TITLE)#' \
		> $@
	@cat $< REFS \
		| sed 's#__WEBFILES__#$(FILES)#' \
		| djot \
		>> $@
	@cat FOOT >> $@

.PHONY: all
all: $(PAGES)

.PHONY: clean
clean:
	rm -f $(PAGES)
