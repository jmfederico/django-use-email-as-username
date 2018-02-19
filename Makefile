.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## check style with flake8
	pipenv check --style django_use_email_as_username tests

test: ## run tests quickly with the default Python
	pipenv run python runtests.py

test-all: ## run tests on every Python version with tox
	pipenv run tox

coverage: ## check code coverage quickly with the default Python
	pipenv run coverage run --source django_use_email_as_username runtests.py
	pipenv run coverage report -m
	pipenv run coverage html
	open htmlcov/index.html

docs: ## generate Sphinx HTML documentation
	rm -f docs/django-use-email-as-username.rst
	rm -f docs/modules.rst
	pipenv run $(MAKE) -C docs clean
	pipenv run $(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean ## package and upload a release
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*

sdist: clean ## package
	pipenv run python setup.py sdist
	ls -l dist
