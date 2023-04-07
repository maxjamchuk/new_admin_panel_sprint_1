import collections.abc as collections_abc
from contextlib import contextmanager
import dataclasses
import sqlite3

import more_itertools
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor

from constants import DEFAULT_EXTRACT_CHUNK_SIZE, DEFAULT_LOAD_CHUNK_SIZE


@contextmanager
def pg_con_context(**dsn):
    """Context managet to connect PG"""

    con = psycopg2.connect(**dsn)

    try:
        yield con
    except Exception as err:
        con.rollback()
        print(f'Error: {err}')
        raise
    else:
        con.commit()
    finally:
        con.close()


class PGSaver:
    """Load to PG"""

    def __init__(self, pg_con: _connection, batch_size: int = DEFAULT_LOAD_CHUNK_SIZE):
        self.pg_con = pg_con
        self.batch_size = batch_size

    def truncate_table(self, table_name: str) -> None:
        """Drop all rows"""
        with self.pg_con.cursor() as cur:
            cur.execute("""TRUNCATE content.%s CASCADE""" % table_name)

    def save_data(self, list_data: collections_abc.Iterable, table_name: str, dataclass: object) -> None:
        """Wrtie to DB"""

        with self.pg_con.cursor() as cur:
            for batch in more_itertools.ichunked(list_data, self.batch_size):
                data = [dataclasses.astuple(dataclass(**item)) for item in batch]
                field_names = dataclass.keys()
                self.save_dataclass_to_pg(cur, table_name, field_names, data)

    @staticmethod
    def save_dataclass_to_pg(cur: _cursor, table_name: str, field_names: list, list_data: list):
        """Write to db"""
        keys_str = ','.join(field_names)
        values_str = ','.join(['%s'] * len(field_names))
        cur.executemany(f"""
            INSERT INTO content.{table_name} ({keys_str}) 
            VALUES ({values_str})
        """, list_data)


class PGExtractor:
    """Extractor from PG"""

    def __init__(self, pg_conn: _connection, batch_size: int = DEFAULT_EXTRACT_CHUNK_SIZE) -> None:
        self.pg_conn = pg_conn
        self.batch_size = batch_size

    def extract_iteratively(self, table_name: str) -> collections_abc.Iterable:
        """Insert batches"""
        with self.pg_conn.cursor() as cur:
            cur.execute("SELECT * FROM content.%s ORDER BY id;" % (table_name,))
            while table_batch := cur.fetchmany(size=self.batch_size):
                yield from table_batch

    def extract_all(self, table_name: str) -> list:
        """Insert all"""
        with self.pg_conn.cursor() as cur:
            cur.execute("SELECT * FROM content.%s;" % (table_name,))
            return cur.fetchall()


######
def sqlite_dict_factory(cur, row):
    """Load dicts from SQLite"""
    fields = [column[0] for column in cur.description]
    return {key: value for key, value in zip(fields, row)}


@contextmanager
def sqlite_con_context(db_path: str):
    """Context managet to connect SQLite"""
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite_dict_factory
    try:
        yield con
    except Exception as err:
        con.rollback()
        print(f'Error: {err}')
        raise
    else:
        con.commit()
    finally:
        con.close()


class SQLiteExtractor:
    """Extractor from SQLite"""
    def __init__(self, sqlite_con: sqlite3.Connection, batch_size: int = DEFAULT_EXTRACT_CHUNK_SIZE) -> None:
        self.sqlite_con = sqlite_con
        self.batch_size = batch_size

    def extract_iteratively(self, table_name: str) -> collections_abc.Iterable:
        """Insert batches"""
        cur = self.sqlite_con.cursor()
        cur.execute("SELECT * FROM %s ORDER BY id;" % (table_name,))
        while table_chunk := cur.fetchmany(size=self.batch_size):
            yield from table_chunk

    def extract_all(self, table_name: str) -> list:
        """Insert all"""
        cur = self.sqlite_con.cursor()
        cur.execute("SELECT * FROM %s;" % (table_name,))
        return cur.fetchall()