#!/usr/bin/env python3
import sys
import math

# Punto de referencia (X, Y) y radio en km
REFERENCE_LAT = 6.2518  # Cambiar segun sea necesario
REFERENCE_LON = -75.5636  # Cambiar segun sea necesario
MAX_DISTANCE_KM = 10  # Radio max en km


# Funcion para calcular la distancia entre dos puntos usando la formula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Leer entrada line por line
for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) != 7:
        continue  # Saltar lines mal formateadas

    sensor_id, lat, lon, timestamp, value, sensor_type, unit = fields
    try:
        lat, lon, value = float(lat), float(lon), float(value)
    except ValueError:
        continue  # Ignorar lines con valores no numéricos

    # Calcular la distancia al punto de referencia
    distance = haversine(lat, lon, REFERENCE_LAT, REFERENCE_LON)

    if distance <= MAX_DISTANCE_KM:
        print(f"{sensor_type}\t{value}")  # Emitir clave-valor (sensor_type, value)
