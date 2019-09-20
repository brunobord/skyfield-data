help:
	@echo "Skyfield data - Makefile targets (devs only)"
	@echo
	@echo " * download: Download all files if necessary, default options."
	@echo "             (see \`python download.py --help\` for options)"
	@echo " * clean: remove all skyfield data from data directory."
	@echo " * package: build python source package."
	@echo ""
	@echo " * install-dev: Install the requirements to execute download.py"

download:
	python3 download.py

clean:
	rm -f skyfield_data/data/*

package:
	python3 setup.py sdist bdist_wheel

install-dev:
	pip install -e .[dev]
