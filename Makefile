all: test requirements.freeze.txt

.PHONY: lint-pylint
lint-pylint:
	pylint ./reflex_cli

.PHONY: lint-black
lint-black:
	black ./

.PHONY: test-unit
test-unit:
	pytest ./test/test_**.py

.PHONY: test-coverage
test-coverage:
	pytest --cov=./reflex_cli ./test --cov-report=xml --cov-report=html


.PHONY: lint
lint: lint-pylint

.PHONY: lint-fix
lint-fix: lint-black

.PHONY: test
test: test-coverage

pre-commit: .pre-commit .pre-commit-config.yaml
	# Installs .git/hooks/pre-commit
	pre-commit install

# Actual files to make
requirements.freeze.txt: requirements.txt
	pip freeze > requirements.freeze.txt
