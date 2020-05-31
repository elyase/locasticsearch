# Locasticsearch

<p align="center">
    <em>Serverless full text search in Python</em>
</p>

Locasticsearch provides serverless full text search powered by [sqlite full text search capabilities](https://www.sqlite.org/fts5.html) but trying to be compatible with a subset of the elasticsearch API.

That way you can comfortably develop your text search appplication without needing to set up servers, but knowing that you are not locked in to a library. When you are ready to .

That said, if you are only doing basic search operations within the subset supported by this library, and you dont have a lot of documents (less than a million) that would justify going for a cluster deployment, Locasticsearch [can be a faster](benchmarks) alternative to Elasticsearch.

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

## Getting started
```
from locasticsearch import Locasticsearch
from datetime import datetime

es = Locasticsearch()

doc = {
    "author": "kimchy",
    "text": "Elasticsearch: cool. bonsai cool.",
    "timestamp": datetime(2010, 10, 10, 10, 10, 10),
}
res = es.index(index="test-index", doc_type="tweet", id=1, body=doc)

res = es.get(index="test-index", doc_type="tweet", id=1)
print(res["_source"])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res["hits"]["total"]["value"])
for hit in res["hits"]["hits"]:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
```    

## Features

- 💯% local, no server management
- ✨ Lightweight pure python, no external dependencies
- ⚡ Super fast searches thanks to [sqlite full text search capabilities](https://www.sqlite.org/fts5.html)
- 🔗 No lock in. Thanks to the API compatiblity with the official client, you can smoothly transition to Elasticsearch for scale or more features without changing your code.

## Install

```bash
pip install locasticsearch
```

## To use or not to use

You should NOT use Locasticsearch if:

- you are deploying a security sensitive application. Locasticsearch code is very prone to SQL injection attacks.
- Your searches are more complicated than what you would find in a 5 min Elasticsearch tutorial. Elasticsearch has a huge API and it is very unlikely that we can support even a sizable portion of that.
- You hate buggy libraries. Locasticsearch is a very young project so bugs are guaranteed. Check the tests to see if your needs are covered. 

You should use Locasticsearch if:

- you dont want a docker or an elasticsearch service using precious resources in your laptop
- you have basic text search needs and Elasticsearch would be overkill
- you want very easy deployments that only involve pip installs
- using Java from a python program makes you feel dirty 


