.DEFAULT_GOAL := help

.PHONY: help
help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean-build clean-pyc

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -type f -name '*.pyc' -exec rm -f {} +
	find . -type f -name '*.pyo' -exec rm -f {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: test
test: ## run tests quickly with the default Python
	poetry run python runtests.py

.PHONY: test-all
test-all: ## run tests on every Python version with tox
	poetry run tox

.PHONY: coverage
coverage: ## check code coverage quickly with the default Python
	poetry run coverage run --source django_use_email_as_username runtests.py
	poetry run coverage report -m
	poetry run coverage html
	open htmlcov/index.html

.PHONY: docs
docs: ## generate Sphinx HTML documentation
	rm -f docs/django-use-email-as-username.rst
	rm -f docs/modules.rst
	poetry run $(MAKE) -C docs clean
	poetry run $(MAKE) -C docs html
	open docs/_build/html/index.html
