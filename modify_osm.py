import xml.etree.ElementTree as ET


def modify_osm(FOLDER, input_file, output_file):
    tree = ET.parse(f"{FOLDER}/{input_file}")
    root = tree.getroot()

    # pievieno trūkstošās maksimālā braukšanas ātruma "maxspeed" vērtības:
    for way in root.iter("way"):
        for tag in way.iter("tag"):
            # ja ir "maxspeed":
            if tag.attrib.get("k") == "maxspeed":
                break
            # pievieno "maxspeed" vērtību:
            if tag.attrib.get("k") == "maxspeed:type":
                new_tag = ET.Element("tag")
                new_tag.set("k", "maxspeed")

                # urban = 50 km/h
                # pieņemam, ka Rīgā "rural" un "trunk" kategorijām arī limits ir 50 km/h
                if (
                    tag.attrib["v"] == "LV:urban"
                    or tag.attrib["v"] == "LV:rural"
                    or tag.attrib["v"] == "LV:trunk"
                ):
                    new_tag.set("v", "50")

                # pieņemam, ka pārējās kategorijas ir skaitliskas vērtības
                else:
                    # katram gadījumam izprintējam vērtību terminālī
                    print(f'INFO: tag.attrib["v"] = {tag.attrib["v"]}')
                    new_tag.set("v", tag.attrib["v"])

                # noņemam arī pašreizējo vērtību, lai maksimālais ātrums būtu pirms vecās vērtības
                way.remove(tag)
                way.append(new_tag)
                way.append(tag)

    # saglabā modificēto failu utf-8 formātā
    tree.write(f"{FOLDER}/{output_file}", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    TEMP = "temp_files"
    input_file = "map_filtered.osm"
    output_file = "map_modified.osm"
    modify_osm(TEMP, input_file, output_file)
