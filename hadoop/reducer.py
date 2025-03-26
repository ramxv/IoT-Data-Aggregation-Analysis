#!/usr/bin/env python3
import sys

current_sensor = None
values = []

# Leer line por line desde el Mapper
for line in sys.stdin:
    sensor_type, value = line.strip().split("\t")
    try:
        value = float(value)
    except ValueError:
        continue  # Ignorar valores no numericos

    # Si cambiamos de sensor, procesamos el anterior
    if current_sensor and sensor_type != current_sensor:
        min_val = min(values)
        max_val = max(values)
        avg_val = sum(values) / len(values)
        print(f"{current_sensor}: min={min_val}, max={max_val}, avg={avg_val:.2f}")
        values = []  # Reiniciar lista de valores

    current_sensor = sensor_type
    values.append(value)

# Procesar el last sensor
if current_sensor:
    min_val = min(values)
    max_val = max(values)
    avg_val = sum(values) / len(values)
    print(f"{current_sensor}: min={min_val}, max={max_val}, avg={avg_val:.2f}")
