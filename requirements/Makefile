.PHONY: all
all: setup.txt dev.txt

.PHONY: install-dev
install-dev: setup.txt dev.txt
	pip-sync $^
	pip install -e ../

setup.txt: ../setup.py
	pip-compile $< --output-file $@

dev.txt: dev.in setup.txt
	pip-compile $<
