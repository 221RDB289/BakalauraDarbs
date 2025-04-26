# noderīga informācija par ortools bibliotēku uz kā tika balstīts kods: https://developers.google.com/optimization/routing

from db import *
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.geocoders import Nominatim
from db import *
from sumolib import net
import xml.etree.ElementTree as ET


# izvada sākuma/beigu (piegādes noliktavas) koordinātas no SUMO tīkla faila:
def get_depot(address="Plieņciema iela 35"):
    # vai šīs adreses x un y koordinātas jau ir datubāzē:
    results = db_get(f"SELECT x,y FROM locations WHERE address='{address}';")
    if results:
        x, y = results[0]
    else:
        """
        citādi (ja šīs adreses x un y koordinātas nav datubāzē) - iegūst koorinātes no adreses:
        https://operations.osmfoundation.org/policies/nominatim/
        - maksimāli ir atļauts 1 pieprasījums 1 sekundē
        - rezultātus vajag saglabāt, lai pieprasījumus nevajadzētu atkārtot
        """
        geolocator = Nominatim(user_agent="221RDB289")

        # atver SUMO network mapes failu:
        net_file = "simulation_files/map.net.xml"
        network = net.readNet(net_file)

        # pārveido koordinātas uz x un y vērtībām failā un izvēlas tuvākos ceļus:
        location = geolocator.geocode(address, country_codes=["LV"])
        latitude, longitude = location.latitude, location.longitude
        x, y = network.convertLonLat2XY(longitude, latitude)

        # ievieto jaunu ierakstu datubāzē:
        db_update(
            f"INSERT INTO locations (address,latitude,longitude,x,y) VALUES{address,latitude, longitude,x,y};"
        )  # ! ielas id netiek pievienots

    return (x, y)


# izveido datu modeli no SUMO tīkla faila x un y koordinātām katrai norādītajai adresei:
def create_data_model(addresses, num_vehicles=1):
    coordinates = [
        get_depot()
    ]  # sākuma/beigu (piegādes noliktava) ir 1. saraksta pozīcijā
    for address, latitude, longitude, x, y, lane, pos in addresses:
        coordinates.append((x, y))
    data = {}
    data["coordinates"] = coordinates
    data["num_vehicles"] = num_vehicles
    data["depot"] = 0  # sākuma/beigu (piegādes noliktava) ir 1. saraksta pozīcijā
    return data


# datu modeli pārveido par attālumu matricu izmantojot Eiklīda attālumu:
def compute_euclidean_distance_matrix(locations):
    distances = {}
    for i, from_coordinates in enumerate(locations):
        distances[i] = {}
        for j, to_coordinates in enumerate(locations):
            if i == j:
                distances[i][j] = 0
            else:
                # aprēķina Eiklīda attālumu:
                distances[i][j] = int(
                    math.hypot(
                        (from_coordinates[0] - to_coordinates[0]),
                        (from_coordinates[1] - to_coordinates[1]),
                    )
                )
    return distances


# nejaušā veidā izvēlās x skaitu adreses un koordinātas
def get_random_locations(x):
    sql = f"SELECT * FROM locations WHERE lane IS NOT NULL AND address!='Plieņciema iela 35' ORDER BY RANDOM() LIMIT {x};"
    results = db_get(sql=sql)
    return results


# izveido kurjera maršrutu failu:
def create_courier_route_file(addresses, stops):
    root = ET.Element(
        "routes",
        {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:noNamespaceSchemaLocation": "http://sumo.dlr.de/xsd/routes_file.xsd",
        },
    )

    # transportlīdzekļa tips:
    vType = ET.SubElement(
        root, "vType", {"id": "myCourier", "maxSpeed": "160", "vClass": "delivery"}
    )

    # kurjera maršruts:
    trip1 = ET.SubElement(
        root,
        "trip",
        {
            "id": "courier_1",
            "type": "myCourier",
            "depart": "0",
            "from": "-908811053",
            "to": "-908811053",
        },
    )

    # piegādes punkti:
    for stop_index in stops:
        address, latitude, longitude, x, y, lane, pos = addresses[
            stop_index - 1
        ]  # -1, jo noliktava sarakstā neietilpst
        # if pos == 0:
        #     print(pos)
        #     pos = 1
        ET.SubElement(
            trip1,
            "stop",
            {
                "lane": lane,
                "endPos": f"{pos}",
                "parking": "true",
                "duration": "60",
                "friendlyPos": "true",
            },
        )

    # saglabā failu:
    tree = ET.ElementTree(root)
    tree.write("optimized_courier.trips.xml", encoding="UTF-8", xml_declaration=True)


def get_solution():
    x = 100
    addresses = get_random_locations(x)
    data = create_data_model(addresses)

    # maršrutu indeksēšanai:
    manager = pywrapcp.RoutingIndexManager(
        len(data["coordinates"]), data["num_vehicles"], data["depot"]
    )

    # maršrutēšanas modelis:
    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_euclidean_distance_matrix(data["coordinates"])

    # izvada attālumu starp 2 punktiem no attāluma matricas:
    def distance_callback(from_index, to_index):
        coordinates = manager.IndexToNode(from_index)
        to_coordinates = manager.IndexToNode(to_index)
        return distance_matrix[coordinates][to_coordinates]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # katram ceļam iegūst izmaksas:
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # pirmā atrisinājuma heiristiska:
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # iegūst atrisinājumu pēc dotajiem meklēšanas parametriem:
    solution = routing.SolveWithParameters(search_parameters)

    # saglabā maršrutu adrešu indeksu saraksta formā:
    stops = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        stops.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))
    stops.pop(0)  # noņem 1. vērtību, jo tā ir noliktava

    # izveido kurjera maršrutu failu:
    create_courier_route_file(addresses, stops)

    # print(stops)
    # print(len(stops))
    # print(len(addresses))


if __name__ == "__main__":
    get_solution()
