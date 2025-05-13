from data.db import get_random_trips
import xml.etree.ElementTree as ET

FOLDER = "simulation_files"


# izveido satiksmes (parasto mašīnu) maršrutu failu:
def create_traffic_route_file():
    trips = get_random_trips(x=10000)

    root = ET.Element(
        "routes",
        {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:noNamespaceSchemaLocation": "http://sumo.dlr.de/xsd/routes_file.xsd",
        },
    )

    # transportlīdzekļa tips (elivery nevis passenger, jo dažas tuvākās ielas adresēm nav ar passenger tipa atļauju):
    vType = ET.SubElement(
        root, "vType", {"id": "myCar", "maxSpeed": "180", "vClass": "delivery"}
    )

    for i, trip_data in enumerate(trips):

        # maršruts:
        trip = ET.SubElement(
            root,
            "trip",
            {
                "id": f"car_{i}",  # mašīnas numurs
                "type": "myCar",
                "depart": "0",
                "from": trip_data[0],
                "to": trip_data[1],
            },
        )

    # saglabā failu:
    tree = ET.ElementTree(root)
    tree.write(f"{FOLDER}/traffic.trips.xml", encoding="UTF-8", xml_declaration=True)
