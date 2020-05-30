# locasticsearch

<p align="center">
    <em>A summary phrase to catch attention!</em>
</p>

<p align="center">
<a href="https://github.com/elyase/locasticsearch/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/elyase/locasticsearch/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/elyase/locasticsearch/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/elyase/locasticsearch/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://codecov.io/gh/elyase/locasticsearch" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/elyase/locasticsearch?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/locasticsearch" target="_blank">
    <img src="https://img.shields.io/pypi/v/locasticsearch?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/locasticsearch/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/locasticsearch.svg" alt="Python Versions">
</a>

## The Basic Idea
```
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", id=1, body=doc)
print(res['result'])

res = es.get(index="test-index", id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])




def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="nyc-restaurants",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "borough": {"type": "keyword"},
                    "cuisine": {"type": "keyword"},
                    "grade": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                }
            },
        },
        ignore=400,
    )

class TestUnicode(ElasticsearchTestCase):
    def test_indices_analyze(self):
        self.client.indices.analyze(body='{"text": "привет"}')


class TestBulk(ElasticsearchTestCase):
    def test_bulk_works_with_string_body(self):
        docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))

    def test_bulk_works_with_bytestring_body(self):
        docs = b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))    

```    

## Features

- No database

## Installing locasticsearch

Install the latest release:

```bash
pip install locasticsearch
```

Or you can clone `locasticsearch` and get started locally

```bash

# ensure you have Poetry installed
pip install --user poetry

# install all dependencies (including dev)
poetry install

# develop!

```

## Example Usage

```python
import locasticsearch

# do stuff
```

Only **Python 3.6+** is supported as required by the black, pydantic packages

## Publishing to Pypi

### Poetry's documentation

Note that it is recommended to use [API tokens](https://pypi.org/help/#apitoken) when uploading packages to PyPI.

>Once you have created a new token, you can tell Poetry to use it:

<https://python-poetry.org/docs/repositories/#configuring-credentials>

We do this using GitHub Actions' Workflows and Repository Secrets!

### Repo Secrets

Go to your repo settings and add a `PYPI_TOKEN` environment variable:

![Github Actions setup of Poetry token environment variable](images/Github-Secrets-PYPI_TOKEN-Setup.png)

### Inspect the GitHub Actions Publish Workflows

```yml
name: Publish

on:
  release:
    types:
      - created

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      ...
      ...
      ...
      - name: Publish
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: |
          poetry config pypi-token.pypi $PYPI_TOKEN
          bash scripts/publish.sh
```

> That's it!

When you make a release on GitHub, the publish workflow will run and deploy to PyPi! 🚀🎉😎

## Contributing Guide

Welcome! 😊👋

> Please see the [Contributing Guide](CONTRIBUTING.md).
