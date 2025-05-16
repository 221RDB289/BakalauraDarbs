import subprocess
import os
import shutil
import sys

FOLDER = "simulation_files"
STATIC = "static_files"


# ģenerē maršrutus nejaušības gadījumā:
def create_random_routes():
    if not os.path.exists(f"{FOLDER}/traffic.rou.xml"):
        cmd = [
            "python",
            "randomTrips.py",
            "-n",
            f"{FOLDER}/map.net.xml",
            "-b",
            "0",
            "-e",
            "28800",  # 8h = 28800s
            "--insertion-rate=2000",
            "-o",
            f"{FOLDER}/traffic.trips.xml",
            "--validate",
            "--additional-file",
            f"{STATIC}/vehicle_types.xml",
        ]
        subprocess.run(cmd)


# kurjeru maršruti:
def create_courier_routes(folder):
    # TODO: jāizmanto --routing-algorithm https://sumo.dlr.de/docs/Simulation/Routing.html
    # duarouter iestatījumi: https://sumo.dlr.de/docs/duarouter.html
    if shutil.which("duarouter"):
        if not os.path.exists(f"{folder}/courier.rou.xml"):
            cmd = [
                "duarouter",
                "-n",
                f"{FOLDER}/map.net.xml",
                "--route-files",
                f"{folder}/courier.trips.xml",
                "-o",
                f"{folder}/courier.rou.xml",
                # ja ir kļūme, tad izmantojot šīs opcijas var iegūt vairāk informāciju:
                "--verbose",
                "true",
            ]
            subprocess.run(cmd)
            print("CREATED courier routes")
            os.remove(f"{folder}/courier.rou.alt.xml")
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
    files = [f"{FOLDER}/traffic.rou.xml"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)


def get_routes():
    # remove_courier_routes()
    # create_courier_routes()

    # remove_random_routes()
    create_random_routes()


if __name__ == "__main__":
    get_routes()
