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
    if len(fields) != 4:  # Cambiar a 4 campos
        continue  # Saltar líneas mal formateadas

    timestamp, value, lat, lon = fields  # Sólo 4 campos
    try:
        lat, lon, value = float(lat), float(lon), float(value)
    except ValueError:
        continue  # Ignorar líneas con valores no numéricos

    # Calcular la distancia al punto de referencia
    distance = haversine(lat, lon, REFERENCE_LAT, REFERENCE_LON)

    if distance <= MAX_DISTANCE_KM:
        # Emitir clave-valor (sensor_type, value) — puedes cambiar 'sensor_type' por una constante si no lo tienes
        print(f"sensor_value\t{value}")  # Simple clave-valor, sin sensor_type en este caso