# adreses ir ņemtas no: https://data.gov.lv/dati/lv/dataset/rigas-ielas-un-adreses

from sumolib import net
import xml.etree.ElementTree as ET
from data.db import *

FOLDER = "data"


# nejaušā veidā izvēlās x skaitu adreses un koordinātas vai izvada jau izvēlētās adreses:
def get_random_addresses(new=False, x=100):
    if new:
        print(f"SELECTING {x} NEW RANDOM LOCATIONS")
        conn = db_create_connection()
        db_update2(sql="UPDATE locations SET used=FALSE;", conn=conn)
        results = db_get2(
            sql=f"SELECT * FROM locations WHERE pos NOT NULL ORDER BY RANDOM() LIMIT {x};",
            conn=conn,
        )
        for r in results:
            db_update2(
                sql=f'UPDATE locations SET used=TRUE WHERE address="{r[0]}";', conn=conn
            )
        print(f"SELECTION COMPLETED")
    else:
        results = db_get(sql=f"SELECT * FROM locations WHERE used IS TRUE;")
    return results


# pievieno tuvākos ceļa galus adresēm un izvada tās adreses, kurām varēja atrast tuvāko ceļa galu:
# radius = tuvuma rādiuss metros
def lanes_to_db(addresses, radius=100):
    print(f"FINDING LANES FOR {len(addresses)} ADDRESSES")
    # atveram SUMO network mapes failu:
    network_file = "simulation_files/map.net.xml"
    network = net.readNet(network_file)
    print("LOADED: map.net.xml")
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
            # else:
            #     print(f'ERROR: lane not in range of "{p[0]}"')
    conn.close()
    print(f"FOUND LANES FOR {len(filetered_addresses)} ADDRESSES")
    return filetered_addresses


def addresses_to_db(input_file):
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    tree = ET.parse(f"{FOLDER}/{input_file}")
    root = tree.getroot()
    values = []
    print(f"TRANSFERING: {input_file} data to the database")
    conn = db_create_connection()

    # pievieno trūkstošās maksimālā braukšanas ātruma "maxspeed" vērtības:
    for Placemark in root.findall(".//kml:Placemark", namespaces=ns):
        ExtendedData = Placemark.find(".//kml:ExtendedData", namespaces=ns)
        address = ExtendedData.find(
            './/kml:SimpleData[@name="adrese"]', namespaces=ns
        ).text
        longitude, latitude = Placemark.find(
            ".//kml:Point/kml:coordinates", namespaces=ns
        ).text.split(",")
        # vai šī adrese jau ir datubāzē:
        sql = f"SELECT address FROM locations WHERE address == '{address}';"
        results = db_get2(sql=sql, conn=conn)
        if not results:
            # ievieto jaunu ierakstu datubāzē:
            sql = f"INSERT INTO locations (address,latitude,longitude) VALUES{address,latitude, longitude};"
            db_update2(sql=sql, conn=conn)
            values.append((address, latitude, longitude))
    conn.close()
    print(f"TRANSFER COMPLETED")


def prapare_addresses(x):
    if not os.path.exists(FILENAME):
        # izveido datubāzes failu:
        folder = FILENAME.split("/")[0]
        if not os.path.exists(folder):
            os.mkdir(folder)
        db_create()

        # pievieno adrešu datus datubāzē:
        addresses_to_db("addresses.kml")
        addresses = db_get(f"SELECT * FROM locations WHERE lane IS NULL;")
        filtered_addresses = lanes_to_db(addresses, 50)
        # filtered_addresses = lanes_to_db(addresses, 1000) # ja vajag visām adresēm (testa brīdī 437 adresēm nevarēja atrast tuvāko ceļu ar 100 metru rādiusu)
        random_addresses = get_random_addresses(new=True, x=x)
