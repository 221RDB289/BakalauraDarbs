import overpy
from geopy.geocoders import Nominatim
from db import *
from sumolib import net

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
        latitude, longitude = location.latitude, location.longitude
        # ievieto jaunu ierakstu datubāzē:
        sql = f"INSERT INTO locations (address,latitude,longitude) VALUES{address,latitude, longitude};"
        db_update(sql)
        return latitude, longitude


if __name__ == "__main__":
    geolocator = Nominatim(user_agent="221RDB289")

    """
    no koordinātēm iegūst tuvāko objektu OSM mapē:
    - "around" vērtība ir rādius metros
    """

    # atveram SUMO network mapes failu:
    net_file = "simulation_files/map.net.xml"
    network = net.readNet(net_file)
    print("LOADED: map.net.xml")

    # pārveido koordinātas uz x un y vērtībām failā un izvēlas tuvākos ceļus:
    latitude, longitude = address_to_coordinates(geolocator, "Plieņciema iela 35")
    radius = 50
    x, y = network.convertLonLat2XY(longitude, latitude)
    edges = network.getNeighboringEdges(x, y, radius)
    # izvēlas pašu tuvāko ceļa galu:
    if len(edges) > 0:
        distancesAndEdges = sorted(
            [(dist, edge) for edge, dist in edges], key=lambda x: x[0]
        )
        dist, closestEdge = distancesAndEdges[0]
        # print(dist, closestEdge)
        print(closestEdge._id)

    # testa adrese
    latitude, longitude = address_to_coordinates(geolocator, "Dārziņu 32. līnija 22")
    # pārveido koordinātas uz x un y vērtībām failā un izvēlas tuvākos ceļus:
    radius = 50
    x, y = network.convertLonLat2XY(longitude, latitude)
    lanes = network.getNeighboringLanes(x, y, radius)

    # izvēlas pašu tuvāko ceļa galu:
    if len(lanes) > 0:
        distances_and_lanes = sorted(
            [(dist, lane) for lane, dist in lanes], key=lambda x: x[0]
        )
        # for dist, lane in distances_and_lanes:
        #     print(dist, lane.getID())
        dist, closestLane = distances_and_lanes[0]
        lane_id = closestLane.getID()
        # precīza māajs pozīcijas iegūšana uz ceļa:
        pos = closestLane.getClosestLanePosAndDist((x, y))[0]
        print(lane_id, pos)
