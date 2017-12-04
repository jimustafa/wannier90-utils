WANNIER90_DIR = $(WANNIER90_ROOT)/wannier90-$(WANNIER90_VERSION)

W90=$(abspath $(WANNIER90_DIR)/wannier90.x)
POSTW90=$(abspath $(WANNIER90_DIR)/postw90.x)

EXAMPLES_1=$(foreach idx,01 02 03 04,example$(idx))
EXAMPLES_2=$(foreach idx,05 06 07 09 10 11 13 17 18 19 20,example$(idx))
EXAMPLES=$(EXAMPLES_1) $(EXAMPLES_2)


define write_hr
	$(if $(filter $(shell echo $(subst .,,$(WANNIER90_VERSION))\>=210 | bc), 1), echo "write_hr=true" >> wannier.win, echo "hr_plot=true" >> wannier.win)
endef

define modify_win
	$(call write_hr)
	echo "write_xyz=true" >> wannier.win
	echo "bands_plot=true" >> wannier.win
	echo "kpath=true" >> wannier.win
	echo "kpath_task=bands" >> wannier.win
	echo "geninterp=true" >> wannier.win
endef


default: clean $(EXAMPLES)

$(EXAMPLES):
	cp -r $(WANNIER90_DIR)/examples/$@ .
	cp particular.mk $@
	make -C $@ -f particular.mk run-$@

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
	$(call write_hr)
	echo "write_xyz=true" >> wannier.win
	$(W90)

run-example03:
	$(foreach fname, $(wildcard silicon.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp
	$(call modify_win)
	$(W90)
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90)

run-example04:
	$(foreach fname, $(wildcard copper.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp
	$(call modify_win)
	echo "geninterp_alsofirstder=true" >> wannier.win
	$(W90)
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90)

clean:
	rm -rf example*

.PHONY: clean $(EXAMPLES) $(foreach example,$(EXAMPLES),run-$(example))
