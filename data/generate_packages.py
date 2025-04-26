from db import *
from sumolib import net


FODLER = "data"


# pievieno tuvākos ceļa galus adresēm un izvada tās adreses, kurām varēja atrast tuvāko ceļa galu:
def lanes_to_db(addresses):
    print(f"FINDING LANES FOR {len(addresses)} ADDRESSES")
    # atveram SUMO network mapes failu:
    network_file = "simulation_files/map.net.xml"
    network = net.readNet(network_file)
    print("LOADED: map.net.xml")
    radius = 100  # tuvuma rādiuss metros
    conn = db_create_connection()
    filetered_addresses = []

    # katrai piegādes adresei:
    for p in addresses:
        # ja datubāzē šai adresei nav norādīts tuvākais ceļš "lane":
        if not p[5]:
            # pārveido koordinātas uz x un y vērtībām failā un izvēlas tuvākos ceļa galus:
            x, y = network.convertLonLat2XY(p[2], p[1])
            lanes = network.getNeighboringLanes(x, y, radius)

            # izvēlas pašu tuvāko ceļa galu:
            if len(lanes) > 0:
                distances_and_lanes = sorted(
                    [(dist, lane) for lane, dist in lanes], key=lambda x: x[0]
                )
                dist, closestLane = distances_and_lanes[0]
                lane_id = closestLane.getID()
                # precīza māajs pozīcijas iegūšana uz ceļa:
                pos = closestLane.getClosestLanePosAndDist((x, y))[0]
                # pievieno jaunus datus (x,y,lane,pos) datubāzē:
                sql = f'UPDATE locations SET x={x},y={y},lane="{lane_id}", pos={pos} WHERE address="{p[0]}";'
                db_update2(sql=sql, conn=conn)
                filetered_addresses.append(
                    p[0:2] + (x, y, lane_id, pos)
                )  # (address, latitude, longitude, x,y,lane,pos)
            else:
                print(f'ERROR: lane not in range of "{p[0]}"')
    conn.close()
    print(f"FOUND LANES FOR {len(filetered_addresses)} ADDRESSES")
    return filetered_addresses


# nejaušā veidā izvēlās x skaitu adreses un koordinātas
def get_random_locations(x):
    print(f"GENERATING {x} RANDOM LOCATIONS")
    sql = f"SELECT * FROM locations ORDER BY RANDOM() LIMIT {x};"
    results = db_get(sql=sql)
    print(f"GENERATION COMPLETED")
    return results


# TODO: generate more package data?


def save_packages_to_file(filename, packages):
    with open(file=f"{FODLER}/{filename}", mode="w", encoding="utf-8") as f:
        for p in packages:
            f.write(f"{p[0]};{p[1]};{p[2]};{p[3]};{p[4]};{p[5]}\n")
    print(f"SAVED TO: {filename}")


# izvada tuple tipa sarakstu:
def read_packages_from_file(filename):
    with open(file=f"{FODLER}/{filename}", mode="r", encoding="utf-8") as f:
        packages = []
        for line in f.read().split("\n"):
            if line:
                packages.append(tuple(line.split(";")))
        print(f"READ DATA FROM: {filename}")
        return packages


if __name__ == "__main__":
    # nejaušā veidā izvēlās x skaitu adreses un to koordinātas no datubāzes:
    x = 100
    filename = "packages.csv"
    addresses = get_random_locations(x)

    # filtrē pēc ceļa galiem:
    filtered_addresses = lanes_to_db(addresses)
    save_packages_to_file(filename, filtered_addresses)

    # izlasa paciņu datos no faila
    addresses = read_packages_from_file(filename)
    # print(addresses)
