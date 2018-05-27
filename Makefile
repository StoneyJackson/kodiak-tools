VERSION:=$(shell cat VERSION)

PYTEST_COV_OPTS=--cov=src --cov-report term-missing
PYTEST_FLAKE8_OPTS=--flake8
PYTEST_MYPY_OPTS=--mypy 
PYTEST_OPTS=-v $(PYTEST_COV_OPTS) $(PYTEST_FLAKE8_OPTS) $(PYTEST_MYPY_OPTS)

build:
	mkdir build
	cp -R src build/kodiak
	pipenv lock --requirements > build/kodiak/requirements.txt
	python -m pip install -r build/kodiak/requirements.txt --src build/kodiak
	rm build/kodiak/requirements.txt
	rm -rf build/kodiak/*.dist-info
	python -m zipapp build/kodiak -p "/usr/bin/env python3" -o build/kodiak-$(VERSION).pyz

clean:
	rm -rf build

test: build
	PYTHONPATH=./src MYPYPATH=./src pytest $(PYTEST_OPTS) tests
	build/kodiak-$(VERSION).pyz unpack ~/Downloads/Homework\ 3\ Download\ May\ 25,\ 2018\ 1118\ AM.zip build/kodiak-$(VERSION)-test-result
