import osmium

FOLDER = "simulation_files2"


def pbf_to_osm(infile, outfile):
    writer = osmium.SimpleWriter(outfile)

    for obj in osmium.FileProcessor(infile):
        obj.bounds
        if obj.is_node():
            writer.add_node(obj)
        elif obj.is_way():
            writer.add_way(obj)
        elif obj.is_relation():
            writer.add_relation(obj)

    writer.close()


if __name__ == "__main__":
    pbf_to_osm(f"{FOLDER}/latvia-latest.osm.pbf", f"{FOLDER}/test.osm")
