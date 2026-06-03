import os
from pathlib import Path

import psycopg2


user = os.environ.get("PGUSER", "postgres")
password = os.environ.get("PGPASSWORD", "123")
host = os.environ.get("HOST", "127.0.0.1")
database_name = os.environ.get("PGDATABASE", "songster")


def db_connection():
    db = (
        "dbname='" + database_name + "' "
        "user=" + user + " "
        "host=" + host + " "
        "password=" + password
    )
    return psycopg2.connect(db)


def run_sql_file(cur, file_name):
    sql_path = Path(__file__).parent / "sql" / file_name
    cur.execute(sql_path.read_text())


def init_db():
    from scripts.import_liked_songs import import_liked_songs

    conn = db_connection()
    cur = conn.cursor()

    run_sql_file(cur, "schema.sql")
    run_sql_file(cur, "seed.sql")
    import_liked_songs(cur)

    conn.commit()
    cur.close()
    conn.close()
