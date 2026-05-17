from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager
import os


pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=20,
    dsn=os.getenv("DATABASE_URL")
)

@contextmanager
def get_conn():
    conn = pool.getconn()

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)
