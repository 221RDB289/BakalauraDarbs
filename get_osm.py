import urllib.request
import subprocess
import os
import shutil
import sys
from modify_osm import *

if __name__ == "__main__":
    if not os.path.exists("riga.net.xml"):
        # 1. iegūst Latvijas mapi no geofabrik:
        if not os.path.exists("latvia-latest.osm.pbf"):
            urllib.request.urlretrieve(
                "https://download.geofabrik.de/europe/latvia-latest.osm.pbf",
                "latvia-latest.osm.pbf",
            )
            print("Downloaded: latvia-latest.osm.pbf")

        # 2. iegūst Rīgas reģiona robežas:
        if not os.path.exists("riga.poly"):
            urllib.request.urlretrieve(
                "https://polygons.openstreetmap.fr/get_poly.py?id=13048688&params=0",
                "riga.poly",
            )
            print("Downloaded: riga.poly")

        # 3. iegūst "osmosis" atrašanās vietu:
        osmosis = shutil.which("osmosis")
        if not osmosis:
            print("ERROR: osmosis is not installed")
            sys.exit()

        # 4. filtrē Rīgas reģionu no Latvijas OSM faila:
        if not os.path.exists("riga.osm"):
            cmd = [
                osmosis,
                "--read-pbf-fast",
                "file=latvia-latest.osm.pbf",
                "--bounding-polygon",
                "file=riga.poly",
                "--write-xml",
                "file=riga.osm",
            ]
            subprocess.run(cmd)

        # 5. modificē OSM failu, lai izlabotu neeksistējošos maksimālos ātrumus:
        if not os.path.exists("riga_modified.osm"):
            modify_osm()
            print("Modified: riga.osm")

        # 6. iegūst SUMO tīkla failu:
        if not os.path.exists("riga.net.xml"):
            if shutil.which("netconvert"):
                cmd = [
                    "netconvert",
                    "--osm-files",
                    "riga_modified.osm",
                    "--output-file",
                    "riga.net.xml",
                    "--keep-edges.by-vclass",
                    "delivery",
                    "--remove-edges.isolated",
                    "--remove-edges.explicit",
                    "unused",
                    "--junctions.join",
                    "--geometry.remove",
                    "--keep-nodes-unregulated",
                    "--speed-in-kmh",
                    "--ramps.guess",
                    "--tls.guess-signals",
                    "--tls.join",
                    # "--ignore-errors",
                ]
                subprocess.run(cmd)
            else:
                print("ERROR: SUMO is not installed")
                sys.exit()

        # 7. nevajadzīgo failu izdzēšana:
        os.remove("latvia-latest.osm.pbf")
        os.remove("riga.poly")
        os.remove("riga.osm")
        os.remove("riga_modified.osm")
