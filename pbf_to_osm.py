import osmium
import shapely.geometry
import sys
import re

FOLDER = "simulation_files2"


def pbf_to_osm(input_file, output_file, poly_files):
    # apvieno robežas un pārveido to "Polygon" datu tipā:
    polygon_coordinates = []
    for poly_file in poly_files:
        with open(poly_file, mode="r", encoding="utf-8") as f:
            lines = f.readlines()[2:-2]
        for line in lines:
            coordinates = line.strip().split(" ")
            polygon_coordinates.append((coordinates[0], coordinates[-1]))
    polygon = shapely.geometry.Polygon(polygon_coordinates)
    # print(polygon)
    # sys.exit()

    # pārveido faila tipu (piemēram pbf uz osm) un filtrē rezultātus pēc robežām:
    writer = osmium.SimpleWriter(output_file)

    fp = osmium.FileProcessor(input_file)
    fp.with_locations()
    # fp.with_areas()
    used_nodes = []
    used_ways = []
    used_relations = []
    for obj in fp:
        if obj.is_node():
            # ja "node" objekts ir norādītajā reģionā:
            point = shapely.geometry.Point(obj.lon, obj.lat)
            if point.within(polygon):
                used_nodes.append(obj.id)
                writer.add_node(obj)
        elif obj.is_way():
            # ja vismaz viens "node" objekts no "way" objekta ir norādītajā reģionā:
            for node in obj.nodes:
                point = shapely.geometry.Point(node.lon, node.lat)
                if point.within(polygon):
                    used_ways.append(obj.id)
                    writer.add_way(obj)
                    break
        elif obj.is_relation():
            # ja vismaz viens no "way" objektiem ir jau pievienots osm failam:....................................
            for ref in obj.members:
                ref = str(ref)
                if ref.startswith("n"):
                    if int(re.findall("\d+", ref)[0]) in used_nodes:
                        writer.add_relation(obj)
                        break
                elif ref.startswith("w"):
                    if int(re.findall("\d+", ref)[0]) in used_ways:
                        writer.add_relation(obj)
                        break
                elif ref.startswith("r"):
                    if int(re.findall("\d+", ref)[0]) in used_relations:
                        writer.add_relation(obj)
                        break
                else:
                    print("ERROR:", obj)

    writer.close()


if __name__ == "__main__":
    pbf_to_osm(
        f"{FOLDER}/latvia-latest.osm.pbf",
        f"{FOLDER}/test2.osm",
        [f"{FOLDER}/riga.poly", f"{FOLDER}/marupe.poly"],
    )
