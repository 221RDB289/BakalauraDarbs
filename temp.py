riga_poly = read_poly(f"{TEMP}/riga.poly")
riga_poly_buffered = buffer_polygon(
    riga_poly, extended_distance_meters=5000
)  # + 5 km
marupe_poly = read_poly(f"{TEMP}/marupe.poly")
combined_poly = unary_union([riga_poly_buffered, marupe_poly])
write_poly(combined_poly)