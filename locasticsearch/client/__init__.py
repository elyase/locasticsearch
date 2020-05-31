import logging
import sqlite3
import time
from datetime import date, datetime

from .indices import IndicesClient

logger = logging.getLogger("elasticsearch")


def _escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = ",".join(value)

    # dates and datetimes into isoformat
    elif isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # don't decode bytestrings
    elif isinstance(value, bytes):
        return value

    return str(value)


class Locasticsearch:
    def __init__(self, database=":memory:", **kwargs):
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

        self.indices = IndicesClient(self.cursor)

    def _get_columns(self, index):
        if not self.indices.exists(index):
            return []
        sql = f'select * from "{index}"'
        self.cursor.execute(sql)
        return [col[0] for col in self.cursor.description]

    def index(self, index, body, id=None, **kwargs):
        """
        Creates or updates a document in an index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-index_.html>`_

        :arg index: The name of the index
        :arg body: The document
        :arg id: Document ID
        """

        query_fields = list(body.keys())

        # check if new columns need to be added
        columns = self._get_columns(index)
        if not set(columns) == set(query_fields):
            self.indices.delete(index)
            _template = {
                "mappings": {
                    "properties": {field: {"type": "text"} for field in query_fields}
                },
            }
            self.indices.create(index=index, body=_template)

        if id is not None:
            query_fields = ["rowid"] + query_fields

        values = tuple(_escape(val) for val in body.values())
        if id is not None:
            values = [str(id)] + list(values)
            values = tuple(values)

        query_fields = ", ".join(query_fields)
        sql = f'INSERT INTO "{index}"({query_fields}) VALUES {values};'

        try:
            self.cursor.execute(sql)
        except sqlite3.IntegrityError:
            pass

        response = {
            "_index": index,
            "_type": "_doc",
            "_id": str(id) if id is not None else str(self.cursor.lastrowid),
            "_version": 1,
            "result": "created",
            "_shards": {"total": 1, "successful": 1, "failed": 0},
        }
        return response

    def get(self, index, id, **kwargs):
        sql = f'SELECT * FROM "{index}" WHERE rowid={id};'
        self.cursor.execute(sql)
        record = dict(self.cursor.fetchone())
        response = {
            "_index": index,
            "_type": "_doc",
            "_id": str(id),
            "_version": 1,
            "_seq_no": 10,
            "_primary_term": 1,
            "found": True,
            "_source": record,
        }
        return response

    def search(self, index=None, body=None):
        """
        Returns results matching a query.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-search.html>`_
        :arg body: The search definition using the Query DSL
        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        """

        # match_all
        if "match_all" in body["query"]:
            sql = f'SELECT * FROM "{index}";'

        if "multi_match" in body["query"]:
            multi_match = body["query"]["multi_match"]["query"]
            # fields = body["query"]["multi_match"]["fields"]
            sql = f'SELECT * FROM "{index}" WHERE "{index}" MATCH "{multi_match}";'

        start = time.process_time()
        rows = self.cursor.execute(sql).fetchall()
        elapsed_time = round(time.process_time() - start / 1000)

        response = {
            "took": elapsed_time,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": len(rows), "relation": "eq"},
                "max_score": "fix this",
                "hits": [
                    {
                        "_index": index,
                        "_type": "_doc",
                        "_id": "fix this",
                        "_score": "fix this",
                        "_source": dict(row),
                    }
                    for row in rows
                ],
            },
        }

        return response

    def bulk(self, body, index=None, doc_type=None, params=None, headers=None):
        """
        Allows to perform multiple index/update/delete operations in a single request.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-bulk.html>`_

        :arg body: The operation definition and data (action-data
            pairs), separated by newlines
        :arg index: Default index for items which don't provide one
        :arg doc_type: Default document type for items which don't
            provide one
        :arg _source: True or false to return the _source field or not,
            or default list of fields to return, can be overridden on each sub-
            request
        :arg _source_excludes: Default list of fields to exclude from
            the returned _source field, can be overridden on each sub-request
        :arg _source_includes: Default list of fields to extract and
            return from the _source field, can be overridden on each sub-request
        :arg pipeline: The pipeline id to preprocess incoming documents
            with
        :arg refresh: If `true` then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh
            to make this operation visible to search, if `false` (the default) then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the bulk operation. Defaults
            to 1, meaning the primary shard only. Set to `all` for all shard copies,
            otherwise set to any non-negative value less than or equal to the total
            number of copies for the shard (number of replicas + 1)
        """
        pass
