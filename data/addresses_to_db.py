# adreses ir ņemtas no: https://data.gov.lv/dati/lv/dataset/rigas-ielas-un-adreses

import xml.etree.ElementTree as ET
from db import *

FOLDER = "data"


def addresses_to_db(input_file):
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    tree = ET.parse(f"{FOLDER}/{input_file}")
    root = tree.getroot()
    values = []
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


if __name__ == "__main__":
    addresses_to_db("addresses.kml")
