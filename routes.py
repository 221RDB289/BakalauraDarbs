import subprocess
import os
import shutil
import sys
import sumolib
from geopy.geocoders import Nominatim
import math

FOLDER = "simulation_files"
STATIC = "static_files"


# ģenerē maršrutus nejaušības gadījumā
def create_test_routes():
    if not os.path.exists(f"{FOLDER}/riga.trips.xml"):
        cmd = [
            "python",
            "randomTrips.py",
            "-n",
            f"{FOLDER}/riga.net.xml",
            "-e",
            "1000",
            "-o",
            f"{FOLDER}/riga.trips.xml",
            "--validate",
            '--trip-attributes=type="myCar"',
            "--additional-file",
            f"{STATIC}/vehicle_types.xml",
        ]
        subprocess.run(cmd)
    if shutil.which("duarouter"):
        if not os.path.exists(f"{FOLDER}/riga.rou.xml"):
            cmd = [
                "duarouter",
                "-n",
                f"{FOLDER}/riga.net.xml",
                "--route-files",
                f"{FOLDER}/riga.trips.xml",
                "-o",
                f"{FOLDER}/riga.rou.xml",
            ]
            subprocess.run(cmd)
    else:
        print("ERROR: SUMO is not installed")
        sys.exit()


# pārveido doto adresi uz tuvāko "node"
def address_to_node(
    address,
    geolocator,
    net,
):
    location = geolocator.geocode(address)
    x, y = net.convertLonLat2XY(location.longitude, location.latitude)
    print(x, y)
    return x, y
    # node = net.getClosestNode(x, y)
    # return node.id


# edges = net.getNeighboringEdges(x, y, radius)


# no koordinātēm iegūst tuvāko tīkla "node" pēc Eiklīda attāluma:
def get_closest_node(coordinates, distance, net):
    x, y = coordinates
    for node in net.getNodes():
        if node:
            xn, yn = node.getCoord()
            if math.sqrt((x - xn) ** 2 + (y - yn) ** 2) <= distance:
                print(xn, yn)
                return node.getID()
    return


if __name__ == "__main__":
    # create_test_routes()

    net = sumolib.net.readNet(f"{FOLDER}/riga.net.xml")
    radius = 500

    x = 3683.9117356822244
    y = 7678.589846183546

    # x, y = net.convertLonLat2XY(lon, lat)
    edges = net.getNeighboringEdges(x, y, radius)
    if edges:
        distancesAndEdges = sorted(
            [(dist, edge) for edge, dist in edges], key=lambda x: x[0]
        )
        dist, closestEdge = distancesAndEdges[0]
        print(closestEdge)

    # distance = 500

    # geolocator = Nominatim(user_agent="sumo_routing")
    # net = sumolib.net.readNet(f"{FOLDER}/riga.net.xml")

    # address1 = "Plieņciema iela 35, Mārupe, Mārupes pagasts, Mārupes novads, LV-2167"
    # address2 = "Zunda krastmala 10, Kurzemes rajons, Rīga, LV-1048"

    # node1 = get_closest_node(address_to_node(address=address1, geolocator=geolocator, net=net),distance, net)

    # node2 = get_closest_node(address_to_node(address=address2, geolocator=geolocator, net=net),distance, net)

    # print(f"Closest SUMO nodes: {node1}, {node2}")

    # net = sumolib.net.readNet(f"{FOLDER}/riga.net.xml")
    # for node in net.getNodes():
    #     xn,yn = node.getCoord()
    #     if math.sqrt((x-xn)**2+(y-yn)**2)
    #     print(node.getID())

    # location1 = geolocator.geocode(address1)
    # location2 = geolocator.geocode(address2)

    # print(f"Address 1: {location1.latitude}, {location1.longitude}")
    # print(f"Address 2: {location2.latitude}, {location2.longitude}")

    # net = sumolib.net.readNet(f"{FOLDER}/riga.net.xml")
    # x1, y1 = net.convertLonLat2XY(location1.longitude, location1.latitude)
    # x2, y2 = net.convertLonLat2XY(location2.longitude, location2.latitude)

    # node1 = net.getClosestNode(x1, y1)
    # node2 = net.getClosestNode(x2, y2)

    # print(f"Closest SUMO nodes: {node1.id}, {node2.id}")
