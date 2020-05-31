#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place locasticsearch tests --exclude=__init__.py
black locasticsearch tests
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --thirdparty locasticsearch --apply locasticsearch tests
