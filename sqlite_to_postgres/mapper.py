import collections.abc as collections_abc

from constants import MAP_DATA_FIELDS


class DataMapper:
    """PQ SQLite mapper"""

    @classmethod
    def map_sqlite_to_pg_iterator(cls, data_iterator: collections_abc.Iterable) -> collections_abc.Iterable:
        yield from (cls.map_sqlite_to_pg_data(data) for data in data_iterator)

    @classmethod
    def map_pg_to_sqlite_iterator(cls, data_iterator: collections_abc.Iterable) -> collections_abc.Iterable:
        yield from (cls.map_pg_to_sqlite_data(data) for data in data_iterator)

    @staticmethod
    def map_sqlite_to_pg_data(data: dict) -> dict:
        for field_from, field_to in MAP_DATA_FIELDS:
            if field_from in data:
                data[field_to] = data.pop(field_from)
        return data

    @staticmethod
    def map_pg_to_sqlite_data(data: dict) -> dict:
        for field_to, field_from in MAP_DATA_FIELDS:
            if field_from in data:
                data[field_to] = data.pop(field_from)
        return data
