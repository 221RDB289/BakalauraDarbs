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
    latitude, longitude = address_to_coordinates(geolocator, "Plieņciema iela 35")
    print(latitude, longitude)

    """
    no koordinātēm iegūst tuvāko objektu OSM mapē:
    - "around" vērtība ir rādius metros
    """

    # overpass = overpy.Overpass()

    # result = overpass.query(
    #     f"""
    # way(around:10,{latitude},{longitude});
    # out body;
    # """
    # )
    # print(result.ways[0].id)

    # result = overpass.query(
    #     f"""
    # node(around:10,{latitude},{longitude});
    # out body;
    # """
    # )
    # # tuvākais node:
    # node_id = result.nodes[0].id
    # print(node_id)




    # # atveram SUMO network failu:
    # net_file = "simulation_files/map.net.xml"
    # net = net.readNet(net_file)

    # print('LOADED: map.net.xml')

    # # node = net.getNode(str(node_id))
    # node = net.getClosestNode(longitude, latitude)
    # print(node)
    # # atrod tuvāko ielu x metru attālumā:
    # edges = node.getOutgoing()
    # print(edges)
    # edges = net.getNeighboringEdges(longitude, latitude, 1000)
    # print(edges)

    # # atrod tuvāko
    # if nearest:
    #     distance, edge = nearest[0]
    #     print(f"Closest edge ID: {edge.getID()}")
    # else:
    #     print("No edge found nearby.")







    # atveram SUMO network mapes failu:
    net_file = "simulation_files/map.net.xml"
    net = net.readNet(net_file)

    print('LOADED: map.net.xml')

    # pārveido koordinātas uz x un y vērtībām failā un izvēlas tuvākos ceļus:
    radius = 50
    x, y = net.convertLonLat2XY(longitude, latitude)
    edges = net.getNeighboringEdges(x, y, radius)
    print(len(edges))
    # izvēlas pašu tuvāko ceļu:
    if len(edges) > 0:
        distancesAndEdges = sorted([(dist, edge) for edge, dist in edges], key=lambda x:x[0])
        dist, closestEdge = distancesAndEdges[0]
        print(dist, closestEdge)
        print(closestEdge._id)