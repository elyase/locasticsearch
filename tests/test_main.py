from datetime import datetime

import pytest

from locasticsearch import Locasticsearch


@pytest.fixture
def es():
    es = Locasticsearch()
    return es


def test_can_instantiate():
    es = Locasticsearch()


def test_create_index(es):
    settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "age": {"type": "integer"},
                "email": {"type": "keyword"},
                "name": {"type": "text"},
            }
        },
    }
    response = es.indices.create(index="test-index", body=settings, ignore=400)
    assert response == {
        "acknowledged": True,
        "shards_acknowledged": True,
        "index": "test-index",
    }


def test_add_doc(es):
    res = es.index(index="test", id=42, body={"firstname": "John", "lastname": "Snow"})
    assert res["_id"] == "42"

    res = es.index(index="test", body={"firstname": "John", "lastname": "Snow"})
    assert res["_id"] == "43"


def test_non_text_fields(es):
    response = es.index(
        index="test",
        id=42,
        body={"any": "data", "timestamp": datetime(2010, 10, 10, 10, 10, 10)},
    )
    response = es.get(index="test", id=42)["_source"]
    assert response["timestamp"] == "2010-10-10T10:10:10"
    assert response["any"] == "data"
