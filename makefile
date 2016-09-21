PHONY: clean test build cosmic

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/py.test
PEP8 := $(VENV)/bin/pep8
HTTP := $(VENV)/bin/http

PYSRC := $(shell find kontakt -iname '*.py')


###############
# Boilerplate #
###############

default: build

clean:
	rm -rf htmlcov .coverage .eggs


##############
# Virtualenv #
##############

$(PYTHON) $(PIP):
	virtualenv -p python3 venv
	$(PIP) install -U pip setuptools


################
# Code Quality #
################

$(PEP8): $(PYTHON)
	$(PIP) install pep8

pep8.errors: $(PEP8) $(PYSRC)
	$(PEP8) --exclude="venv" . | tee pep8.errors || true


################
# Unit Testing #
################

$(VENV)/bin/py.test: $(PIP)
	$(PIP) install pytest pytest-cov pytest-xdist

test: $(PYSRC) $(PYTHON) $(VENV)/bin/py.test pep8.errors
	$(PIP) install -U ../hyperflask
	$(PIP) install -U . sqlalchemy httpretty
	$(PYTEST) tests/*.py
