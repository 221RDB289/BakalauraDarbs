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
def create_random_routes():
    if not os.path.exists(f"{FOLDER}/other.trips.xml"):
        cmd = [
            "python",
            "randomTrips.py",
            "-n",
            f"{FOLDER}/map.net.xml",
            "-e",
            "1000",
            "-o",
            f"{FOLDER}/other.trips.xml",
            "--validate",
            '--trip-attributes=type="myCar"',
            "--additional-file",
            f"{STATIC}/vehicle_types.xml",
        ]
        subprocess.run(cmd)
    if shutil.which("duarouter"):
        if not os.path.exists(f"{FOLDER}/other.rou.xml"):
            cmd = [
                "duarouter",
                "-n",
                f"{FOLDER}/map.net.xml",
                "--route-files",
                f"{FOLDER}/other.trips.xml",
                "-o",
                f"{FOLDER}/other.rou.xml",
            ]
            subprocess.run(cmd)
            print("CREATED random routes")
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
                f"optimized_courier.trips.xml",
                "-o",
                f"{FOLDER}/courier.rou.xml",
                # ja ir kļūme, tad izmantojot šīs opcijas var iegūt vairāk informāciju:
                # "--verbose",
                # "true",
            ]
            subprocess.run(cmd)
            print("CREATED courier routes")
    else:
        print("ERROR: SUMO is not installed")
        sys.exit()


if __name__ == "__main__":
    create_random_routes()
    create_courier_routes()
