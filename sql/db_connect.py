from psycopg2 import connect as pgs_connect


def db_connect():
    """Database connection."""
    host = "localhost"
    port = 5432
    user = "app_service"
    password = "_a7r13uVF9i£"
    dbname = "vgame_store"

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
