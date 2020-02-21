# If you have not used make before then checkout the following link:
#    https://www.gnu.org/software/make/manual/html_node/
.PHONY: clean \
	test build venv

all: clean
clean:
	rm -rf $(PWD)/build
	rm -rf $(PWD)/dist
	rm -rf $(PWD)/reflex_cli.egg-info

venv:
	test -d ./venv || python3 -m venv ./venv
	. ./venv/bin/activate;

test: venv
	coverage run -m unittest discover
	coverage report

build: venv
	python setup.py install
