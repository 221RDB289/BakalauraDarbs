import xml.etree.ElementTree as ET

if __name__ == "__main__":
    tree = ET.parse("riga.osm")
    root = tree.getroot()

    # adds maxspeed limits to urban and rural areas that don't have a maxspeed defined
    for way in root.iter("way"):
        for tag in way.iter("tag"):
            # if the way has a maxspeed tag, then we can skip it
            if tag.attrib.get("k") == "maxspeed":
                break
            # otherwise we need to specify the max speed (make a new tag)
            if tag.attrib.get("k") == "maxspeed:type":
                new_tag = ET.Element("tag")
                new_tag.set("k", "maxspeed")
                # urban = 50 km/h
                if tag.attrib["v"] == "LV:urban":
                    new_tag.set("v", "50")
                # rural = 80 or 90 km/h
                elif tag.attrib["v"] == "LV:rural":
                    surface = way.find(".//tag[@k='surface']").attrib["v"]
                    if surface == "asphalt":
                        new_tag.set("v", "90")
                    else:
                        new_tag.set("v", "80")
                # trunk = 50 km/h
                elif tag.attrib["v"] == "LV:trunk":
                    new_tag.set("v", "50")
                # its probably a number
                else:
                    print(f'INFO: tag.attrib["v"] = {tag.attrib["v"]}')
                    new_tag.set("v", tag.attrib["v"])
                way.append(new_tag)

    # modified file with utf-8
    tree.write("riga_modified.osm", encoding="utf-8", xml_declaration=True)
