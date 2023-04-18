import logging
import os
import sqlite3

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor

from constants import TABLES
from mapper import DataMapper
from sql_tools import pg_con_context, PGSaver, sqlite_con_context, SQLiteExtractor


load_dotenv()

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(os.environ.get('LOG_LEVEL', 'DEBUG'))


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection, tables: tuple):
    """Основной метод загрузки данных из SQLite в Postgres"""

    postgres_saver = PGSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(sqlite_conn)
    data_mapper = DataMapper()

    for table_name, table_dataclass in tables:
        logger.info('Clean table %s' % table_name)
        postgres_saver.truncate_table(table_name)
        logger.info('Extract and load table %s' % table_name)
        postgres_saver.truncate_table(table_name)
        batch_data_iterator = sqlite_extractor.extract_iteratively(table_name)
        batch_data_iterator = data_mapper.map_sqlite_to_pg_iterator(batch_data_iterator)
        postgres_saver.save_data(batch_data_iterator, table_name, table_dataclass)
        logger.info('Done for table %s' % table_name)


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432)
    }
    sqlite_path = os.environ.get('SQLITE_PATH')
    with \
        sqlite_con_context(sqlite_path) as sqlite_conn, \
        pg_con_context(**dsl, cursor_factory=RealDictCursor) as pg_conn:
        
        load_from_sqlite(sqlite_conn, pg_conn, TABLES)
