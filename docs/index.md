# Locasticsearch

<p align="center">
    <em>Serverless full text search in Python</em>
</p>

Locasticsearch provides serverless full text search powered by [sqlite full text search capabilities](https://www.sqlite.org/fts5.html) but trying to be compatible with (a subset of) the elasticsearch API.

That way you can comfortably develop your text search appplication without needing to set up services and smoothly transition to Elasticsearch for scale or more features without changing your code.

That said, if you are only doing basic search operations within the subset supported by this library, and dont have a lot of documents (~million) that would justify going for a cluster deployment, Locasticsearch [can be a faster](benchmarks) alternative to Elasticsearch.

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
</p>


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

- you are deploying a security sensitive application. Locasticsearch code is very prone to SQL injection attacks. This should improve in future releases.
- Your searches are more complicated than what you would find in a 5 min Elasticsearch tutorial. Elasticsearch has a huge API and it is very unlikely that we can support even a sizable portion of that.
- You hate buggy libraries. Locasticsearch is a very young project so bugs are guaranteed. You can check the tests to see if your needs are covered. 

You should use Locasticsearch if:

- you dont want a docker or an elasticsearch service using precious resources in your laptop
- you only need basic text search and Elasticsearch would be overkill
- you want very easy deployments that only involve pip installs
- using Java from a python program makes you feel dirty 

## Comparison to similar libraries

[whoosh](https://whoosh.readthedocs.io/en/latest/intro.html)

The most full featured **pure python** text search library by far:

- 👍 Supports highlight, analyzers, query expansion, several ranking functions, ...  
- 👎 Unmaintained for a long time might see a revival at https://github.com/whoosh-community/whoosh 
- 👍 Pure python so doesnt scale as well (still fast enough for small medium datasets) 

[elasticsearch](https://www.elastic.co)

The big champion of full text search. This is what you should be using in production:

* 👍 Lots of features to accomodate any use case
* 👍 Battle tested, scalable, performant
* 👎 Non python native: more complex to deploy/integrate with python project for easy use cases


[django haystack](https://django-haystack.readthedocs.io/en/master/)

Django Haystack provides an unified API that allows you to plug in different search backends (such as Solr, Elasticsearch, Whoosh, Xapian, etc.) without having to modify your code:

* 👍 Many features, boosting, highlight, autocomplete (some backend dependent though)
* 👍 Possibility to switch backends
* 👎 Library lock in.
* 👎 Despite supporting several backends, Whoosh is the only one that is python native.


[xapian](https://xapian.org/docs/bindings/python/)

* 👍 Very fast and full featured (C++) 
* 👎 No pip installable (needs system level compilation)
* 👎 The python bindings and the documentation are not that user friendly


[gensim](https://radimrehurek.com/gensim/)

While gensim focuses on topic modeling you can use `TfidfModel` and `SparseMatrixSimilarity` for text search. That said this is doesnt use an inverted index (linear search) so it has limited scalability.

* 👍 Approximate search
* 👎 Focus is on topic modeling, so no intuitive APIs for full text ingestion/search
* 👎 Doesnt support inverted indexes search (mostly full scan and approximate)


[peewee](http://docs.peewee-orm.com/en/latest/)

Peewee is actually a more general ORM but offers abstractions to use full text search on Sqlite.

* 👍 Support for full text search using several SQL backends (no elasticsearch though)
* 👍 Custom ranking and analyzer functions
* 👎 No elasticsearch compatible API


