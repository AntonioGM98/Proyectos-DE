current-dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SHELL = /bin/sh

help: ## show make targets
	@awk 'BEGIN {FS = ":.*?## "} /[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf " \033[36m%-20s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)

start: install-deps config-files ## install dependencies, add githooks and create secrets

config-files: ## add githooks
	git config core.hooksPath .githooks

install-deps: ## install all dependencies of Pipfile
	@if [ -z $(shell which pipenv) ]; then echo "ERROR: missing software required (pip install pipenv)" > /dev/stderr && exit 1; fi
	@PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

install: ## install dependency, ex: make install dep=requests ver=2.26.0
	@PIPENV_VENV_IN_PROJECT=1 pipenv install $(dep)==$(ver)

install-dev: ## install dev dependency, ex: make install-dev dep=requests ver=2.26.0
	@PIPENV_VENV_IN_PROJECT=1 pipenv install $(dep)==$(ver) --dev

uninstall: ## uninstall dependency, ex: make uninstall dep=requests
	@pipenv uninstall $(dep)

run: ## run api ex: 'make run'
	@echo Running project...
	@bash -c "set -o allexport; source ./env/local.properties; set +o allexport && export PYTHONPATH=app && pipenv run app"

run-tests: ## run tests
	@bash -c "set -o allexport; source ./env/test.properties; set +o allexport \
	&& pipenv run tests"
	@pipenv run architecture-tests

run-stress-tests: ## run stress tests, ex: 'make run-stress-tests host=test.data.iberia.com'
	@pipenv run stress-tests --host $(host)

format: ## run isort and black to apply format code
	@pipenv run isort
	@pipenv run black

check-format: ## check the format import rules and code with isort, black, flake8
	@pipenv run check-isort
	@pipenv run check-black
	@pipenv run check-flake8

check-types: ## run static type checker with mypy
	@pipenv run check-types

start-infra: ## start local infra
	@docker compose up

stop-infra: ## stop local infra
	@docker compose down

.PHONY: help start config-files install-deps install install-dev uninstall run run-tests run-stress-tests format check-format check-types start-infra stop-infra
