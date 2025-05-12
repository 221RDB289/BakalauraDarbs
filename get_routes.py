import subprocess
import os
import shutil
import sys
import sumolib
from geopy.geocoders import Nominatim
import math

FOLDER = "simulation_files"
STATIC = "static_files"


# ģenerē maršrutus nejaušības gadījumā:
def create_random_routes():
    if not os.path.exists(f"{FOLDER}/traffic.trips.xml"):
        cmd = [
            "python",
            "randomTrips.py",
            "-n",
            f"{FOLDER}/map.net.xml",
            "-b",
            "0",
            "-e",
            "14400",  # 8h = 28800s
            "--insertion-rate=30000",
            "-o",
            f"{FOLDER}/traffic.trips.xml",
            "--validate",
            "--additional-file",
            f"{STATIC}/vehicle_types.xml",
        ]
        subprocess.run(cmd)
    if shutil.which("duarouter"):
        if not os.path.exists(f"{FOLDER}/traffic.rou.xml"):
            cmd = [
                "duarouter",
                "-n",
                f"{FOLDER}/map.net.xml",
                "--route-files",
                f"{FOLDER}/traffic.trips.xml",
                "-o",
                f"{FOLDER}/traffic.rou.xml",
            ]
            subprocess.run(cmd)
            print("CREATED random/traffic routes")
            os.remove("traffic.rou.alt.xml")
            os.remove("traffic.trips.xml")
    else:
        print("ERROR: SUMO is not installed")
        sys.exit()


# kurjeru maršruti:
def create_courier_routes():
    # TODO: jāizmanto --routing-algorithm https://sumo.dlr.de/docs/Simulation/Routing.html
    # duarouter iestatījumi: https://sumo.dlr.de/docs/duarouter.html
    if shutil.which("duarouter"):
        if not os.path.exists(f"{FOLDER}/courier.rou.xml"):
            cmd = [
                "duarouter",
                "-n",
                f"{FOLDER}/map.net.xml",
                "--route-files",
                f"{FOLDER}/courier.trips.xml",
                "-o",
                f"{FOLDER}/courier.rou.xml",
                # ja ir kļūme, tad izmantojot šīs opcijas var iegūt vairāk informāciju:
                # "--verbose",
                # "true",
            ]
            subprocess.run(cmd)
            print("CREATED courier routes")
            os.remove("courier.rou.alt.xml")
            os.remove("courier.trips.xml")
    else:
        print("ERROR: SUMO is not installed")
        sys.exit()


# kurjeru maršrutu failu izdzēšana:
def remove_courier_routes():
    files = [f"{FOLDER}/courier.rou.xml", f"{FOLDER}/courier.rou.alt.xml"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)


# nejaušo maršrutu failu izdzēšana:
def remove_random_routes():
    files = [
        f"{FOLDER}/traffic.rou.xml",
        f"{FOLDER}/traffic.rou.alt.xml",
        f"{FOLDER}/traffic.trips.xml",
    ]
    for f in files:
        if os.path.exists(f):
            os.remove(f)


def get_routes():
    # remove_courier_routes()
    # create_courier_routes()

    remove_random_routes()
    create_random_routes()


if __name__ == "__main__":
    get_routes()
