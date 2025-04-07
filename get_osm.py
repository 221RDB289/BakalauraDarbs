import urllib.request
import subprocess
import os
import shutil
import sys
from modify_osm import *

FOLDER = "simulation_files"
TEMP = "temp_files"
STATIC = "static_files"

if __name__ == "__main__":
    # izveido mapes, ja tās neeksistē:
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(TEMP):
        os.mkdir(TEMP)

    # izveido failus, ja tādi neeksistē:
    if not os.path.exists(f"{FOLDER}/map_network.net.xml"):
        # 1. iegūst Latvijas mapi no geofabrik:
        if not os.path.exists(f"{TEMP}/latvia-latest.osm.pbf"):
            urllib.request.urlretrieve(
                "https://download.geofabrik.de/europe/latvia-latest.osm.pbf",
                f"{TEMP}/latvia-latest.osm.pbf",
            )
            print("Downloaded: latvia-latest.osm.pbf")

        # 2. iegūst Rīgas reģiona robežas:
        if not os.path.exists(f"{TEMP}/riga.poly"):
            urllib.request.urlretrieve(
                "https://polygons.openstreetmap.fr/get_poly.py?id=13048688&params=0",
                f"{TEMP}/riga.poly",
            )
            print("Downloaded: riga.poly")

        # 3. iegūst Mārupes pagasta reģiona robežas:
        if not os.path.exists(f"{TEMP}/marupe.poly"):
            urllib.request.urlretrieve(
                "https://polygons.openstreetmap.fr/get_poly.py?id=13048774&params=0",
                f"{TEMP}/marupe.poly",
            )
            print("Downloaded: marupe.poly")

        # 4. apvieno robežas:
        if not os.path.exists(f"{TEMP}/combined.poly"):
            # nolasa un apvieno datus no robežu failiem:
            with open(f"{TEMP}/riga.poly", mode="r", encoding="utf-8") as f:
                combined = f.read().rsplit("\n", 2)[
                    0
                ]  # noņem pēdējās 2 līnijas no faila
            with open(f"{TEMP}/marupe.poly", mode="r", encoding="utf-8") as f:
                combined += (
                    "\n2\n" + f.read().split("\n", 2)[2]
                )  # pievieno 1 līniju un noņem pirmās 2 līnijas no faila
            # izveido apvienoto robežu failu:
            with open(f"{TEMP}/combined.poly", mode="w", encoding="utf-8") as f:
                f.write(combined)
            print("Combined polygons: combined.poly")

        # 5. iegūst "osmosis" atrašanās vietu:
        osmosis = shutil.which("osmosis")
        if not osmosis:
            print("ERROR: osmosis is not installed")
            sys.exit()

        # 6. filtrē izvēlētos reģionus no Latvijas OSM faila:
        if not os.path.exists(f"{TEMP}/map_filtered.osm"):
            cmd = [
                osmosis,
                "--read-pbf-fast",
                f"file={TEMP}/latvia-latest.osm.pbf",
                "--bounding-polygon",
                f"file={TEMP}/combined.poly",
                "--write-xml",
                f"file={TEMP}/map_filtered.osm",
            ]
            subprocess.run(cmd)

        # 7. modificē OSM failu, lai izlabotu neeksistējošos maksimālos ātrumus:
        if not os.path.exists(f"{TEMP}/map_modified.osm"):
            modify_osm(TEMP, "map_filtered.osm", "map_modified.osm")
            print("Modified the map: map_modified.osm")

        # 8. iegūst SUMO tīkla failu:
        if not os.path.exists(f"{FOLDER}/map_network.net.xml"):
            if shutil.which("netconvert"):
                cmd = [
                    "netconvert",
                    "--osm-files",
                    f"{TEMP}/map_modified.osm",
                    "-o",
                    f"{FOLDER}/map_network.net.xml",
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

        # 9. filtrē tikai ēkas
        if not os.path.exists(f"{FOLDER}/buildings.poly.xml"):
            if shutil.which("polyconvert"):
                cmd = [
                    "polyconvert",
                    "--osm-files",
                    f"{TEMP}/map_modified.osm",
                    "-o",
                    f"{FOLDER}/buildings.poly.xml",
                    "--discard",
                    "--type-file",
                    f"{STATIC}/building_types.xml",
                ]
                subprocess.run(cmd)
            else:
                print("ERROR: SUMO is not installed")
                sys.exit()

        # 10. nevajadzīgo failu izdzēšana:
        # os.remove(f"{FOLDER}/latvia-latest.osm.pbf")
        # os.remove(f"{FOLDER}/riga.poly")
        # os.remove(f"{FOLDER}/riga.osm")
        # os.remove(f"{FOLDER}/riga_modified.osm")
