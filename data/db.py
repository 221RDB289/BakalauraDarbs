import sqlite3
import os

FILENAME = "data/locations.db"


# funkcijas, kurām nevajag norādīt jau gatavu datubāzes savienojumu - ja tiek izmantota paralēlā (concurrent) datubāzes piekļuve vai vienkārši vienas komandas izpilde:


def db_get(sql):
    conn = sqlite3.connect(
        FILENAME, check_same_thread=False, timeout=20, isolation_level=None
    )
    conn.execute("pragma journal_mode=WAL;")
    cur = conn.cursor()
    cur.execute("pragma encoding=UTF8")
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result


def db_update(sql):
    conn = sqlite3.connect(
        FILENAME, check_same_thread=False, timeout=20, isolation_level=None
    )
    conn.execute("pragma journal_mode=WAL;")
    cur = conn.cursor()
    cur.execute("pragma encoding=UTF8")
    cur.execute(sql)
    conn.commit()
    conn.close()


# funkcijas, kurām vajag norādīt jau gatavu datubāzes savienojumu - tā var ātrāk veikt vairākas izmaiņas pēc kārtas:


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


# lane = tuvākā ceļa id:
# pos = atrašanās vieta uz ceļa
def db_create():
    sql = """
    CREATE TABLE locations(
        address TEXT PRIMARY KEY,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        x REAL,
        y REAL,
        lane TEXT,
        pos REAL,
        used BOOL DEFAULT FALSE
    );
    """
    db_update(sql)
    print("DATABASE CREATED")


# nejaušā veidā x reizes izvēlās 2 adrešu ielas (satiksmes simulācijai):
def get_random_trips(x=1000):
    trips = []
    results = db_get(
        f"SELECT lane FROM locations WHERE pos NOT NULL ORDER BY RANDOM() LIMIT {x*2};"
    )
    i = 0
    while i < x * 2:
        trips.append((results[i][0][:-2], results[i + 1][0][:-2]))
        i += 2
    return trips


if __name__ == "__main__":
    # pirmo reizi izveido datubāzi:
    if not os.path.exists(FILENAME):
        folder = FILENAME.split("/")[0][:-2]
        if not os.path.exists(folder):
            os.mkdir(folder)
        db_create()

    # izvada datus:
    sql = "SELECT * FROM locations;"
    results = db_get(sql)
    print("NUMBER OF ROWS:", len(results))

    # testi:
    sql = "SELECT * FROM locations WHERE lane!='';"
    results = db_get(sql)
    print("NUMBER OF ROWS:", len(results))

    print(db_get("SELECT * FROM locations WHERE address='Plieņciema iela 35';")[0])

    print(db_get("SELECT * FROM locations WHERE lane='162978621#2_0';"))
