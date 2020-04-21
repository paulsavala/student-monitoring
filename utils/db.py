import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_connection(db):
    conn = None
    conn.row_factory = dict_factory
    try:
        conn = sqlite3.connect(db)
    except sqlite3.Error as e:
        print(e)
        raise sqlite3.Error(f'Database {db} does not exist')
    return conn


def create_cursor(conn):
    try:
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(e)
        raise sqlite3.Error('Could not create a cursor')
    return cursor


def run_query(query, cursor):
    cursor.execute(query)
    return cursor.fetchall()
