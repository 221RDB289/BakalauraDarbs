from get_osm import get_osm
from get_routes import get_routes
from data.addresses import prapare_addresses
from data.optimization import get_solution
import os
import shutil
from traffic import create_traffic_route_file


def delete_old():
    # izdzēš veco datubāzes failu:
    if os.path.exists("data/locations.db"):
        os.remove("data/locations.db")

    # izdzēš vecās mapes:
    folders = ["temp_files", "simulation_files", "output"]
    for f in folders:
        if os.path.exists(f):
            shutil.rmtree(f)


if __name__ == "__main__":
    delete_old()

    # izveido jaunus failus un mapes:
    get_osm()
    prapare_addresses(100)
    # get_solution()
    # get_solution()
    # create_traffic_route_file()
    # get_routes()

    # izdzēš pagaidu failus un mapi, jo tie vairs nebūs nepieciešami:
    # if os.path.exists("temp_files"):
    #     shutil.rmtree("temp_files")
