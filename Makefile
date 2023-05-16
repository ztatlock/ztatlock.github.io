PAGES = $(patsubst %.dj,%.html,$(wildcard *.dj))

%.html: %.dj REFS HEAD FOOT
	$(eval TITLE := $(shell \
			head -n 1 '$<' \
			| tr -d '#[]' \
			| sed 's#^[[:blank:]]*##' \
			| sed 's#[[:blank:]]*$$##'))
	@printf "BUILD : %-30s %s\n" "$@" "$(TITLE)"
	@cat HEAD | sed 's#TITLE#$(TITLE)#' > $@
	@cat $< REFS | djot >> $@
	@cat FOOT >> $@

.PHONY: all
all: $(PAGES)

.PHONY: clean
clean:
	rm -f $(PAGES)
