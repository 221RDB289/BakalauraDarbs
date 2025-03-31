import urllib.request
import subprocess
import os
import shutil
import sys
from modify_osm import *

FOLDER = "simulation_files"

if __name__ == "__main__":
    if not os.path.exists(f"{FOLDER}/riga.net.xml"):
        # 1. iegūst Latvijas mapi no geofabrik:
        if not os.path.exists(f"{FOLDER}/latvia-latest.osm.pbf"):
            urllib.request.urlretrieve(
                "https://download.geofabrik.de/europe/latvia-latest.osm.pbf",
                f"{FOLDER}/latvia-latest.osm.pbf",
            )
            print("Downloaded: latvia-latest.osm.pbf")

        # 2. iegūst Rīgas reģiona robežas:
        if not os.path.exists(f"{FOLDER}/riga.poly"):
            urllib.request.urlretrieve(
                "https://polygons.openstreetmap.fr/get_poly.py?id=13048688&params=0",
                f"{FOLDER}/riga.poly",
            )
            print("Downloaded: riga.poly")

        # 3. iegūst "osmosis" atrašanās vietu:
        osmosis = shutil.which("osmosis")
        if not osmosis:
            print("ERROR: osmosis is not installed")
            sys.exit()

        # 4. filtrē Rīgas reģionu no Latvijas OSM faila:
        if not os.path.exists(f"{FOLDER}/riga.osm"):
            cmd = [
                osmosis,
                "--read-pbf-fast",
                f"file={FOLDER}/latvia-latest.osm.pbf",
                "--bounding-polygon",
                f"file={FOLDER}/riga.poly",
                "--write-xml",
                f"file={FOLDER}/riga.osm",
            ]
            subprocess.run(cmd)

        # 5. modificē OSM failu, lai izlabotu neeksistējošos maksimālos ātrumus:
        if not os.path.exists(f"{FOLDER}/riga_modified.osm"):
            modify_osm()
            print("Modified: riga.osm")

        # 6. iegūst SUMO tīkla failu:
        if not os.path.exists(f"{FOLDER}/riga.net.xml"):
            if shutil.which("netconvert"):
                # cmd = [
                #     "netconvert",
                #     "--osm-files",
                #     "riga_modified.osm",
                #     "--output-file",
                #     "riga.net.xml",
                #     "--keep-edges.by-vclass",
                #     "delivery",
                #     "--remove-edges.isolated",
                #     "--remove-edges.explicit",
                #     "unused",
                #     "--junctions.join",
                #     "--edges.join",
                #     "--ramps.guess",
                #     "--tls.guess-signals",
                #     "--tls.join",
                #     "--geometry.remove",
                #     "--speed-in-kmh",
                # ]

                cmd = [
                    "netconvert",
                    "--osm-files",
                    f"{FOLDER}/riga_modified.osm",
                    "-o",
                    f"{FOLDER}/riga.net.xml",
                    "--geometry.remove",
                    "--ramps.guess",
                    "--junctions.join",
                    "--tls.guess-signals",
                    "--tls.discard-simple",
                    "--tls.join",
                    "--keep-edges.by-vclass",
                    "delivery",
                    "--remove-edges.isolated",
                    "--remove-edges.explicit",
                    "unused",
                    "--edges.join",
                    "--speed-in-kmh",
                    "--output.street-names",
                ]
                subprocess.run(cmd)
            else:
                print("ERROR: SUMO is not installed")
                sys.exit()

        # 7. nevajadzīgo failu izdzēšana:
        # os.remove(f"{FOLDER}/latvia-latest.osm.pbf")
        # os.remove(f"{FOLDER}/riga.poly")
        # os.remove(f"{FOLDER}/riga.osm")
        # os.remove(f"{FOLDER}/riga_modified.osm")
