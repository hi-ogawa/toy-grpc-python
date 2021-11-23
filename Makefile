.PHONY: $(shell grep --no-filename -E '^[a-zA-Z_/-]+:' $(MAKEFILE_LIST) | sed 's/:.*//')
SHELL := /bin/bash
PYTHON ?= poetry run python

lint/fix:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

lint:
	$(PYTHON) -m black --check --diff .
	$(PYTHON) -m isort --check --diff .
