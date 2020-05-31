class IndicesClient:
    def __init__(self, cursor):
        self.cursor = cursor

    def create(self, index, body=None, **kwargs):
        """
        Creates an index with optional settings and mappings.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-create-index.html>`_

        :arg index: The name of the index
        """

        field_names = []
        for field_name, _type in body["mappings"]["properties"].items():
            _type = _type["type"]
            unindexed = True if _type not in ("keyword", "text") else False
            field_names.append(field_name)

        columns = ", ".join(field_names)
        sql = f'CREATE VIRTUAL TABLE IF NOT EXISTS "{index}" USING fts5({columns});'
        self.cursor.execute(sql)

        return {"acknowledged": True, "shards_acknowledged": True, "index": index}

    def _add_columns(self, index, columns):
        column_names = [(col,) for col in columns]
        c.executemany(f"ALTER TABLE '{index}' ADD COLUMN ? INTEGER", column_names)

    def _get_tables(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        self.cursor.execute(sql)
        return [dict(row) for row in self.cursor.fetchall()]

    def refresh(self, index=None, params=None, headers=None):
        """
        Performs the refresh operation in one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-refresh.html>`_
        """
        pass

    def delete(self, index, params=None, headers=None):
        """
        Deletes an index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-delete-index.html>`_

        :arg index: A comma-separated list of indices to delete; use
            `_all` or `*` string to delete all indices
        """
        sql = f'drop table if exists "{index}"'
        self.cursor.execute(sql)

    def exists(self, index, params=None, headers=None):
        """
        Returns information about whether a particular index exists.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-exists.html>`_

        :arg index: A comma-separated list of index names
        """
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{index}';"
        return self.cursor.execute(sql).fetchone() is not None
