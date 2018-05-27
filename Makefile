build:
	mkdir build
	cp -R src build/kodiak
	pipenv lock --requirements > build/kodiak/requirements.txt
	python -m pip install -r build/kodiak/requirements.txt --target build/kodiak
	rm build/kodiak/requirements.txt
	rm -rf build/kodiak/*.dist-info
	python -m zipapp build/kodiak -p "/usr/bin/env python3"

clean:
	rm -rf build
