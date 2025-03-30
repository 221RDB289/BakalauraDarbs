import xml.etree.ElementTree as ET

if __name__ == "__main__":
    tree = ET.parse("riga.osm")
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
                way.append(new_tag)

    # saglabā modificēto failu utf-8 formātā
    tree.write("riga_modified.osm", encoding="utf-8", xml_declaration=True)
