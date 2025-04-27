from shapely.geometry import Polygon
from shapely.ops import transform, unary_union
import pyproj

TEMP = "temp_files"


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


if __name__ == "__main__":
    riga_poly = read_poly(f"{TEMP}/riga.poly")
    riga_poly_buffered = buffer_polygon(riga_poly)
    marupe_poly = read_poly(f"{TEMP}/marupe.poly")
    combined_poly = unary_union([riga_poly_buffered, marupe_poly])
    write_poly(combined_poly)
