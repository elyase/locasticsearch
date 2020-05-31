.PHONY: help

# Shell that make should use
SHELL:=bash

# Capture git branch and hash information
# https://stackoverflow.com/questions/43008842/capture-git-branch-name-in-makefile-variable
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
HASH := $(shell git rev-parse HEAD)

# - to suppress if it doesn't exist
-include make.env

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# adds anything that has a double # comment to the phony help list
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ".:*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

python-three-six:
python-three-six: ## setup python3.6 virtual environment using poetry
	poetry env use python3.6
	poetry install

python-three-seven:
python-three-seven: ## setup python3.7 virtual environment using poetry
	poetry env use python3.7
	poetry install

python-three-eight:
python-three-eight: ## setup python3.6 virtual environment using poetry
	poetry env use python3.8
	poetry install

pre-commit:
pre-commit:  ## setup pre-commit within poetry
	poetry run pre-commit install

lint: ## lint the code
lint:
	bash scripts/lint.sh

format: ## format the code
format:
	bash scripts/format.sh

test: ## lint the code
test:
	bash scripts/test.sh

docs-live: ## make live docs
docs-live:
	bash scripts/docs-live.sh

deploy-docs: ## deploy the docs, if on master branch
deploy-docs:
	# https://www.mkdocs.org/user-guide/deploying-your-docs/

	# moved script to bash file for easy of reading
	bash scripts/deploy-docs.sh

install: ## uninstall and install package with python
install:
	poetry remove ./locasticsearch
	poetry add ./locasticsearch
