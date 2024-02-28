import sqlite3
from contextlib import contextmanager


@contextmanager
def sqlite_connector(db_name: str):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()
