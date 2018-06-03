VERSION:=$(shell cat VERSION)

PYTEST_COV_OPTS=--cov=src --cov-report term-missing
PYTEST_FLAKE8_OPTS=--flake8

PYTEST_MYPY_OPTS=--mypy
PYTEST_OPTS=-v $(PYTEST_COV_OPTS) $(PYTEST_FLAKE8_OPTS) $(PYTEST_MYPY_OPTS)

dist: Makefile Pipfile Pipfile.lock VERSION $(wildcard *.py)
	rm -rf dist
	mkdir -p dist
	cp -R src dist/kodiak
	pipenv lock --requirements > dist/kodiak/requirements.txt
	python -m pip install -r dist/kodiak/requirements.txt --target dist/kodiak
	rm dist/kodiak/requirements.txt
	rm -rf dist/kodiak/*.dist-info
	python -m zipapp dist/kodiak -p "/usr/bin/env python3" -o dist/kodiak.pyz

clean:
	rm -rf dist
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .tox

test: dist
	tox

bump-major:
	bumpversion --no-tag major


bump-minor:
	bumpversion --no-tag minor


bump-patch:
	bumpversion --no-tag patch


release:
	git checkout master
	git pull
	make clean
	make test 	# builds new dist too
	make release-message
	@echo -n "Continue relesae? " && read ans && [ $$ans == y ]
	echo test
	bumpversion release
	make clean
	make test   # build dist again with new version number
	git push origin master --tags
	make release-post
	bumpversion --no-tag patch
	git push origin master


release-message:
	mkdir -p .release
	git log $(shell git describe --tags --abbrev=0)..HEAD >> .release/message.md
	nvim .release/message.md


release-post: release/message dist/kodiak.pyz
	hub release create --asset dist/kodiak.pyz --file .release/message.md v$(VERSION)
