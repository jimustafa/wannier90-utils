#!/bin/sh

include site.mk

EXAMPLES_1=$(foreach idx,01 02 03 04,example$(idx))
EXAMPLES_2=$(foreach idx,05 06 07 09 10 11 13 17 18 19 20,example$(idx))
EXAMPLES=$(EXAMPLES_1) $(EXAMPLES_2)


default: clean $(EXAMPLES)

$(EXAMPLES):
	cp -r $(WANNIER90_DIR)/examples/$@ .
	cp Makefile $@
	make -C $@ -I ../ run-$@

$(foreach example,$(EXAMPLES_2),run-$(example)):
	$(foreach fname, $(wildcard $(basename $(wildcard *.win))*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp

run-example01:
	$(foreach fname, $(wildcard gaas.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp
	echo "write_xyz=true" >> wannier.win
	$(W90)

run-example02:
	$(foreach fname, $(wildcard lead.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp
	echo "hr_plot=true" >> wannier.win
	echo "write_xyz=true" >> wannier.win
	$(W90)

run-example03:
	$(foreach fname, $(wildcard silicon.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp wannier
	echo "hr_plot=true" >> wannier.win
	echo "write_xyz=true" >> wannier.win
	echo "bands_plot=true" >> wannier.win
	$(W90)
	echo "kpath=true" >> wannier.win
	echo "kpath_task=bands" >> wannier.win
	echo "geninterp=true" >> wannier.win
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90)

run-example04:
	$(foreach fname, $(wildcard copper.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp
	echo "hr_plot=true" >> wannier.win
	echo "write_xyz=true" >> wannier.win
	echo "bands_plot=true" >> wannier.win
	$(W90)
	echo "kpath=true" >> wannier.win
	echo "kpath_task=bands" >> wannier.win
	echo "geninterp=true" >> wannier.win
	echo "geninterp_alsofirstder=true" >> wannier.win
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90)

clean:
	rm -rf example*

.PHONY: clean $(EXAMPLES) $(foreach example,$(EXAMPLES),run-$(example))
