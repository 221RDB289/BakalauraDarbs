import overpy
from geopy.geocoders import Nominatim
from db import *

"""
iegūst koorinātes no adreses:
https://operations.osmfoundation.org/policies/nominatim/
- maksimāli ir atļauts 1 pieprasījums 1 sekundē
- rezultātus vajag saglabāt, lai pieprasījumus nevajadzētu atkārtot
"""


def address_to_coordinates(geolocator, address):
    # vai šis adreses pieprasījums (vai šī adrese) jau ir datubāzē:
    sql = f"SELECT latitude,longitude FROM locations WHERE address == '{address}';"
    results = db_get(sql)
    if results:
        return results[0]
    # ja nav ieraksts datubāzē:
    else:
        location = geolocator.geocode(address, country_codes=["LV"])
        lat, long = location.latitude, location.longitude
        # ievieto jaunu ierakstu datubāzē:
        sql = f"INSERT INTO locations (address,latitude,longitude) VALUES{address,lat,long};"
        db_update(sql)
        return lat, long


if __name__ == "__main__":
    geolocator = Nominatim(user_agent="221RDB289")
    lat, long = address_to_coordinates(geolocator, "Plieņciema iela 35")
    print(lat, long)

    overpass = overpy.Overpass()

    """
    no koordinātēm iegūst tuvāko objektu OSM mapē:
    - "around" vērtība ir rādius metros
    """
    result = overpass.query(
        f"""
    way(around:10,{lat},{long});
    out body;
    """
    )
    # tuvākais ceļš:
    print(result.ways[0].id)
