import sys
import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS lists ("
    "id SERIAL PRIMARY KEY,"
    "name VARCHAR(80) NOT NULL,"
    "description VARCHAR(80)"
    ")",
    "CREATE TABLE IF NOT EXISTS tasks ("
    "id SERIAL PRIMARY KEY,"
    "name VARCHAR(80) NOT NULL,"
    "description VARCHAR(80),"
    "list_id INTEGER REFERENCES lists(id) ON DELETE CASCADE"
    ")",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


def run(url):
    if url is None:
        print("Missing: DATABASE_URL", file=sys.stderr)
        sys.exit(1)
    initialize(url)
