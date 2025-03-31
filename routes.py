import subprocess
import os
import shutil
import sys

FOLDER = "simulation_files"
STATIC = "static_files"

if __name__ == "__main__":
    # ģenerē maršrutus nejaušības gadījumā
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
