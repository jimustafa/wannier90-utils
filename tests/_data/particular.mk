WANNIER90_DIR = $(WANNIER90_ROOT)/wannier90-$(WANNIER90_VERSION)

W90=$(abspath $(WANNIER90_DIR)/wannier90.x)
POSTW90=$(abspath $(WANNIER90_DIR)/postw90.x)

EXAMPLES_1=$(foreach idx,01 02 03 04,example$(idx))
EXAMPLES_2=$(foreach idx,05 06 07 09 10 11 13 17 18 19 20,example$(idx))
EXAMPLES=$(EXAMPLES_1) $(EXAMPLES_2)

ifeq ($(WANNIER90_VERSION), 2.0.1)
	WRITE_HR="hr_plot=true"
else
	WRITE_HR="write_hr=true"
endif

define modify_win
	echo $(WRITE_HR) >> wannier.win
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
	$(W90) -pp wannier

run-example01:
	$(foreach fname, $(wildcard gaas.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp wannier
	echo "write_xyz=true" >> wannier.win
	$(W90) wannier

run-example02:
	$(foreach fname, $(wildcard lead.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp wannier
	echo $(WRITE_HR) >> wannier.win
	echo "write_xyz=true" >> wannier.win
	$(W90) wannier

run-example03:
	$(foreach fname, $(wildcard silicon.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp wannier
	$(call modify_win)
	$(W90) wannier
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90) wannier

run-example04:
	$(foreach fname, $(wildcard copper.*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
	$(W90) -pp wannier
	$(call modify_win)
	echo "geninterp_alsofirstder=true" >> wannier.win
	$(W90) wannier
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90) wannier

clean:
	rm -rf example*

.PHONY: clean $(EXAMPLES) $(foreach example,$(EXAMPLES),run-$(example))
