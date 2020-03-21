PROJECT_ROOT=../

.PHONY: all
all: dev.txt dev-local.txt

.PHONY: install-dev
install-dev: dev.txt dev-local.txt
	pip-sync $^

dev-local.txt: dev.txt

%.txt: %.in
	pip-compile $<
