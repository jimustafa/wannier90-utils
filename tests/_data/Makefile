include site.mk


WANNIER90_VERSIONS := 2.0.1 2.1 3.0.0 3.1.0


default: clean $(WANNIER90_VERSIONS)

$(WANNIER90_VERSIONS):
	mkdir -p wannier90-$@
	cp particular.mk wannier90-$@
	WANNIER90_ROOT=$(WANNIER90_ROOT) WANNIER90_VERSION=$@ make -C wannier90-$@ -f particular.mk -I ../

clean:
	- rm -rf $(foreach version,$(WANNIER90_VERSIONS),wannier90-$(version))

.PHONY: default $(WANNIER90_VERSIONS) clean
