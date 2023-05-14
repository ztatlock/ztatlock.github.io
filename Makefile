PAGES = $(patsubst %.dj,%.html,$(wildcard *.dj))

%.html: %.dj REFS HEAD FOOT
	$(eval PAGE := $(shell basename $< .dj))
	@echo
	@echo "BUILD $(PAGE)"
	cat HEAD | sed 's/__PAGE__/$(PAGE)/' > $@
	cat $< REFS | djot >> $@
	cat FOOT >> $@

.PHONY: all
all: $(PAGES)

.PHONY: clean
clean:
	rm -f $(PAGES)
