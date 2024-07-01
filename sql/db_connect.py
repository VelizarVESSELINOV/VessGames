from os import getenv
from psycopg2 import connect as pgs_connect
from dotenv import load_dotenv

load_dotenv()


def db_connect():
    """Database connection."""
    host = getenv("DB_HOST")
    port = getenv("DB_PORT")
    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")
    dbname = getenv("DB_NAME")

    conn = pgs_connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
    )
    conn.autocommit = True
    print(conn)

    curr = conn.cursor()

    print(curr)
    return curr
