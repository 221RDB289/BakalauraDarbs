import urllib.request
import subprocess
import os
import shutil
import sys
import xml.etree.ElementTree as ET

# robežām:
from shapely.geometry import Polygon
from shapely.ops import transform, unary_union
import pyproj


FOLDER = "simulation_files"
TEMP = "temp_files"
STATIC = "static_files"


# ----------------------------------------------------------------------------------------------------------------------------------
# modificē OSM failu pārveidojot ielu maksimālos braukšanas ātrumus uz sklaitliskām vērtībām, kur tas ir nepieciešams:
# ----------------------------------------------------------------------------------------------------------------------------------
def modify_osm(FOLDER, input_file, output_file):
    tree = ET.parse(f"{FOLDER}/{input_file}")
    root = tree.getroot()

    # pievieno trūkstošās maksimālā braukšanas ātruma "maxspeed" vērtības:
    i = 0
    for way in root.iter("way"):
        for tag in way.iter("tag"):
            # ja taga k vērtība ir "maxspeed":
            if tag.attrib.get("k") == "maxspeed":
                # ja "maxspeed" ir skaitliska vērtība:
                if tag.attrib["v"].isnumeric():
                    break
                # ja "maxspeed" nav skaitliska vērtība:
                else:
                    tag.set("v", "50")
                    i += 1
                    break
            # ja ir norādīts tags ar k vērtību "maxspeed:type":
            if tag.attrib.get("k") == "maxspeed:type":
                # izveido jaunu "maxspeed" tagu:
                new_tag = ET.Element("tag")
                new_tag.set("k", "maxspeed")

                # urban = 50 km/h
                # pieņemam, ka Rīgā "rural" un "trunk" kategorijām arī limits ir 50 km/h:
                if (
                    tag.attrib["v"] == "LV:urban"
                    or tag.attrib["v"] == "LV:rural"
                    or tag.attrib["v"] == "LV:trunk"
                ):
                    new_tag.set("v", "50")

                # pieņemam, ka pārējās kategorijas ir skaitliskas vērtības:
                else:
                    if tag.attrib["v"].isnumeric():
                        new_tag.set("v", tag.attrib["v"])
                    else:
                        print(
                            f'ERROR: tag v="{tag.attrib["v"]}" is not a numeric value"'
                        )

                # noņemam arī pašreizējo tagu, lai maksimālā ātruma tags būtu pirms maksimālā ātruma tipa:
                way.remove(tag)
                way.append(new_tag)
                way.append(tag)
                i += 1
                break

    print(f"MODIFIED: {i} cases")
    # saglabā modificēto failu utf-8 formātā:
    tree.write(f"{FOLDER}/{output_file}", encoding="utf-8", xml_declaration=True)


# ----------------------------------------------------------------------------------------------------------------------------------
# funkcijas darbībām ar robežām:
# ----------------------------------------------------------------------------------------------------------------------------------


# izvada Polgon objektu no .poly faila:
def read_poly(filepath):
    coordinates = []
    with open(filepath, "r") as f:
        lines = f.readlines()[2:-2]  # izņemot pirmās 2 un pēdējās 2 līnijas
    for line in lines:
        temp = line.strip().split(" ")
        longitude = temp[0]
        latitude = temp[-1]
        coordinates.append((longitude, latitude))
    return Polygon(coordinates)


# palielina poly objektu par "extended_distance_meters" metriem uz āru:
def buffer_polygon(poly, extended_distance_meters=3500):
    # pārveido koordinātas uz metriem saprotamām vērtībām:
    project = pyproj.Transformer.from_crs(
        "EPSG:4326", "EPSG:3857", always_xy=True
    ).transform
    poly_meters = transform(project, poly)

    # palielina poly objektu par "extended_distance_meters" metriem uz āru:
    poly_m_buffered = poly_meters.buffer(extended_distance_meters)

    # pārveido atpakaļ uz koordinātām:
    project_back = pyproj.Transformer.from_crs(
        "EPSG:3857", "EPSG:4326", always_xy=True
    ).transform
    poly_buffered = transform(project_back, poly_m_buffered)

    return poly_buffered


# ieraksta Polygon objektu .poly failā:
def write_poly(poly, filepath=f"{TEMP}/combined.poly"):
    with open(filepath, "w") as f:
        f.write("polygon\n1\n")
        for longitude, latitude in poly.exterior.coords:
            f.write(f"\t{longitude}\t{latitude}\n")
        f.write("END\nEND\n")


# ----------------------------------------------------------------------------------------------------------------------------------
# SUMO tīkla faila pilns iegūšanas un apstrādes process:
# ----------------------------------------------------------------------------------------------------------------------------------
def get_osm():
    # izveido nepieciešamās mapes, ja tās neeksistē:
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(TEMP):
        os.mkdir(TEMP)
    # izveido rezultātu mapi, gadījumā, ja to lietotājs ir izdzēsis:
    if not os.path.exists("output"):
        os.mkdir("output")

    # izveido failus, ja tādi neeksistē:
    if not os.path.exists(f"{FOLDER}/map.net.xml"):
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

        # 4. apvieno robežas, kā arī izpleš Rīgas robežu:
        if not os.path.exists(f"{TEMP}/combined.poly"):
            riga_poly = read_poly(f"{TEMP}/riga.poly")
            riga_poly_buffered = buffer_polygon(
                riga_poly, extended_distance_meters=5000
            )  # + 5 km
            marupe_poly = read_poly(f"{TEMP}/marupe.poly")
            combined_poly = unary_union([riga_poly_buffered, marupe_poly])
            write_poly(combined_poly)
            print("Combined and modified polygons: combined.poly")

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

        # 8. iegūst sākotnējo SUMO tīkla failu:
        if not os.path.exists(f"{TEMP}/map_temp.net.xml"):
            if shutil.which("netconvert"):
                cmd = [
                    "netconvert",
                    "--osm-files",
                    f"{TEMP}/map_modified.osm",
                    "--output-file",
                    f"{TEMP}/map_temp.net.xml",
                    "--geometry.remove=true",
                    "--ramps.guess=true",
                    "--junctions.join=true",
                    "--tls.guess-signals=true",
                    "--tls.discard-simple=true",
                    "--tls.join=true",
                    "--keep-edges.by-vclass=delivery",
                    "--remove-edges.isolated=true",
                    "--edges.join=true",
                    "--keep-edges.components=1",
                    "--speed-in-kmh=true",
                    "--output.street-names=true",
                ]
                subprocess.run(cmd)
            else:
                print("ERROR: SUMO is not installed")
                sys.exit()

        # 9. pārbauda kurām ielām var piekļūt no konkrētās ielas (ņemot vērā ielu virzienus):
        if not os.path.exists(f"{TEMP}/selection_from.txt"):
            cmd = [
                "python",
                "netcheck.py",
                f"{TEMP}/map_temp.net.xml",
                "--source",
                "908811053",
                "--selection-output",
                f"{TEMP}/selection_from.txt",
            ]
            subprocess.run(cmd)

        # 10. pārbauda kuras ielas var nokļūt konkrētajai ielai (ņemot vērā ielu virzienus):
        if not os.path.exists(f"{TEMP}/selection_to.txt"):
            cmd = [
                "python",
                "netcheck.py",
                f"{TEMP}/map_temp.net.xml",
                "--destination",
                "908811053",
                "--selection-output",
                f"{TEMP}/selection_to.txt",
            ]
            subprocess.run(cmd)

        # 11. apvieno pareizās ielas vienā failā:
        if not os.path.exists(f"{TEMP}/selection_combined.txt"):
            with open(f"{TEMP}/selection_from.txt", "r") as f:
                edges1 = set(line.strip() for line in f)
            with open(f"{TEMP}/selection_to.txt", "r") as f:
                edges2 = set(line.strip() for line in f)
            edges = edges1.intersection(edges2)
            with open(f"{TEMP}/selection_combined.txt", "w") as f:
                for edge in edges:
                    f.write(f"{edge}\n")
            print("Combined and edges: selection_combined.txt")

        # 12. iegūst beigu SUMO tīkla failu:
        if not os.path.exists(f"{FOLDER}/map.net.xml"):
            if shutil.which("netconvert"):
                cmd = [
                    "netconvert",
                    "--sumo-net-file",
                    f"{TEMP}/map_temp.net.xml",
                    "--output-file",
                    f"{FOLDER}/map.net.xml",
                    "--keep-edges.input-file",
                    f"{TEMP}/selection_combined.txt",
                ]
                subprocess.run(cmd)
            else:
                print("ERROR: SUMO is not installed")
                sys.exit()

        # 13. iegūst ēkas:
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


if __name__ == "__main__":
    get_osm()
