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

    # pārveido faila tipu (piemēram pbf uz osm) un filtrē rezultātus pēc robežām:
    writer = osmium.SimpleWriter(output_file)

    fp = osmium.FileProcessor(input_file)
    for obj in fp:
        if obj.is_node():
            writer.add_node(obj)
        elif obj.is_way():
            writer.add_way(obj)
        elif obj.is_relation():
            writer.add_relation(obj)
    writer.close()


if __name__ == "__main__":
    pbf_to_osm(
        f"{FOLDER}/latvia-latest.osm.pbf",
        f"{FOLDER}/test_full.osm",
        [f"{FOLDER}/riga.poly", f"{FOLDER}/marupe.poly"],
    )
