from db import *

FODLER = "data"


# nejaušā veidā izvēlās x skaitu adreses un koordinātas
def get_random_locations(x):
    sql = f"SELECT * FROM locations ORDER BY RANDOM() LIMIT {x};"
    results = db_get(sql=sql)
    return results

# TODO: generate packages? get node ids?

def save_to_file(filename, packages):
    with open(file=f"{FODLER}/{filename}", mode="w", encoding="utf-8") as f:
        for p in packages:
            f.write(f"{p[0]};{p[1]};{p[2]}\n")


if __name__ == "__main__":
    # nejaušā veidā izvēlās x skaitu adreses
    x = 100
    filename = "packages.csv"
    packages = get_random_locations(x)
    # for p in packages:
    #     print(r)
    save_to_file(filename, packages)
