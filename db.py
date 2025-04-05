import sqlite3
import os

FILENAME = "data/locations.db"


# funkcijas, kurām nevajag norādīt jau gatavu datubāzes savienojumu - tas labi noder vienlaicīgai komandu izpildei (Concurrent execution):


def db_get(sql):
    conn = sqlite3.connect(FILENAME, check_same_thread=False)
    cur = conn.cursor()
    cur.execute("pragma encoding=UTF8")
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result


def db_update(sql):
    conn = sqlite3.connect(FILENAME, check_same_thread=False, timeout=10)
    conn.execute("pragma journal_mode=WAL;")
    cur = conn.cursor()
    cur.execute("pragma encoding=UTF8")
    cur.execute(sql)
    conn.commit()
    conn.close()


# funkcijas, kurām vajag norādīt jau gatavu datubāzes savienojumu:


def db_get2(sql, conn):
    cur = conn.cursor()
    cur.execute("pragma encoding=UTF8")
    cur.execute(sql)
    result = cur.fetchall()
    return result


def db_update2(sql, conn):
    cur = conn.cursor()
    cur.execute("pragma encoding=UTF8")
    cur.execute(sql)
    conn.commit()


# citas funkcijas:


def db_create_connection():
    conn = sqlite3.connect(FILENAME)
    return conn


def db_create():
    sql = """
    CREATE TABLE locations(
        address TEXT PRIMARY KEY,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );
    """
    db_update(sql)


if __name__ == "__main__":
    if not os.path.exists(FILENAME):
        folder = FILENAME.split("/")[0]
        if not os.path.exists(folder):
            os.mkdir(folder)
        db_create()
