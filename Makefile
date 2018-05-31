VERSION:=$(shell cat VERSION)

PYTEST_COV_OPTS=--cov=src --cov-report term-missing
PYTEST_FLAKE8_OPTS=--flake8

PYTEST_MYPY_OPTS=--mypy
PYTEST_OPTS=-v $(PYTEST_COV_OPTS) $(PYTEST_FLAKE8_OPTS) $(PYTEST_MYPY_OPTS)

dist: VERSION $(wildcard *.py)
	rm -rf dist
	mkdir -p dist
	cp -R src dist/kodiak-tools
	pipenv lock --requirements > dist/kodiak-tools/requirements.txt
	python -m pip install -r dist/kodiak-tools/requirements.txt --src dist/kodiak-tools
	rm dist/kodiak-tools/requirements.txt
	rm -rf dist/kodiak-tools/*.dist-info
	python -m zipapp dist/kodiak-tools -p "/usr/bin/env python3" -o dist/kodiak-tools-$(VERSION).pyz

clean:
	rm -rf dist

test:
	PYTHONPATH=./src MYPYPATH=./src pytest $(PYTEST_OPTS) tests
