# Lai iegūtu/atjaunotu Rīgas mapi:
1. Jāinstalē [Python](https://www.python.org/downloads/)
1. Jāinstalē [Java](https://www.oracle.com/java/technologies/downloads/)
3. Jāinstalē [SUMO](https://sumo.dlr.de/docs/Installing/index.html)
4. Jāinstalē [osmosis](https://wiki.openstreetmap.org/wiki/Osmosis)
5. Jālejupielādē šī [github repozitorijs](https://github.com/221RDB289/BakalauraDarbs/archive/refs/heads/main.zip)
6. Jāatver repozitoriju cmd terminālī un jāizpilda komanda `python get_osm.py`

wsl --install
restart
wsl.exe --install Ubuntu
wsl.exe -d Ubuntu

sudo apt update
sudo apt install osmium-tool
osmium extract -p combined.poly latvia-latest.osm.pbf -o map.osm



# Python bibliotēkas simulācijām un optimizācijām:
## Izmantotās bibliotēkas:
- `pip install traci`
- `pip install ortools`
- `pip install geopy`
- `pip install pyproj`
- `pip install rtree`
- `pip install overpy`
- `pip install osmium`
- `pip install shapely`
## Var arī instalēt projektā lietotās bibliotēku versijas:
- `pip install -r requirements.txt`