# If you have not used make before then checkout the following link:
#    https://www.gnu.org/software/make/manual/html_node/
.PHONY: clean \
	test build venv \
	lint

RANDINT=$(shell python -c 'from random import randint; print(randint(0, 100));')
VENV_BIN_PATH=./venv/bin

all: clean
clean:
	rm -rf $(PWD)/build
	rm -rf $(PWD)/dist
	rm -rf $(PWD)/reflex_cli.egg-info

venv: ./venv/bin/activate

./venv/bin/activate: requirements.txt
	test -d ./venv || python -m venv ./venv
	./venv/bin/activate; pip install --upgrade pip; pip install -Ur requirements.txt; pip install -Ur requirements-dev.txt
	touch ./venv/bin/activate

test: venv
	$(VENV_BIN_PATH)/coverage run -m unittest discover
	$(VENV_BIN_PATH)/coverage report

lint: venv
	$(VENV_BIN_PATH)/black ./reflex_cli/
	$(VENV_BIN_PATH)/pylint ./reflex_cli/

build: venv
	python setup.py install

install: venv
	VERSION=0.$(RANDINT) python setup.py install
	reflex --version
