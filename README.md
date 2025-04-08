# Lai iegūtu/atjaunotu Rīgas mapi (Windows operētājsistēmai):
1. Jāinstalē [Python](https://www.python.org/downloads/) (projektā tika izmantota [Python 3.11.9 versija](https://www.python.org/downloads/release/python-3119/))
1. Jāinstalē [Java](https://www.oracle.com/java/technologies/downloads/) (projektā tika izmantota [JDK 21 versija](https://www.oracle.com/java/technologies/downloads/#jdk24-windows))
3. Jāinstalē [SUMO](https://sumo.dlr.de/docs/Installing/index.html) (projektā tika izmantota [SUMO 1.22.0 versija](https://sumo.dlr.de/releases/1.22.0/))
4. Jāinstalē [osmosis](https://wiki.openstreetmap.org/wiki/Osmosis) (projektā tika izmantota [osmosis 0.49.2 versija](https://github.com/openstreetmap/osmosis/releases/tag/0.49.2))
5. Jāievieto norāde uz `osmosis.bat` faila mapi sistēmas vides mainīgo sarakstā (system environment variables):
    - Windows meklēšanas logā ierakstīt un atvērt: `sysdm.cpl`
    - Aiziet uz "Advanced" sadaļu un atvērt "Enviroment variables"
    - Zem "System variables" sadaļas sameklēt un atvērt "Path"
    - Izveidot jaunu ierakstu uz folderi, kur atrodas `osmosis.bat` (piemēram `C:\osmosis-0.49.2\bin`) un saglabāt izmaiņas
6. Jālejupielādē šī [github repozitorijs](https://github.com/221RDB289/BakalauraDarbs/archive/refs/heads/main.zip)
7. Jāatver repozitoriju cmd terminālī un jāizpilda komanda `python get_osm.py`

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
# Adrešu dati
Rīgas adreses un koordinātas tika iegūtas no [data.gov.lv](https://data.gov.lv/dati/lv/dataset/rigas-ielas-un-adreses)