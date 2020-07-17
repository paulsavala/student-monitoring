import psycopg2
from logzero import logger


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_connection(db_url):
    conn = None
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        conn.row_factory = dict_factory
    except psycopg2.Error as e:
        logger.error(e)
        raise psycopg2.Error('Database connection failed')
    return conn


def create_cursor(conn):
    try:
        cursor = conn.cursor()
    except psycopg2.Error as e:
        logger.error(e)
        raise psycopg2.Error('Could not create a cursor')
    return cursor


def run_query(query, cursor, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()
