import urllib.request
import urllib.parse
import json
import random
import time
import sys
from datetime import datetime

# 1. Variables Declaration
URL = "http://flask_server:8080/store"
sensor_type = ["temperature", "pressure", "air-quality", "co2"]
sensor_unit = {
    "temperature": "°C",
    "pressure": "hPa",
    "air-quality": "PM10",
    "co2": "ppm",
}
# 2. Validate CLI arguments
if len(sys.argv) < 2:
    print("No sensor type provided. Please introduce a sensor type.")
    sys.exit(1)

sensor_type_argument = sys.argv[1]

if sensor_type_argument not in sensor_type:
    print("Invalid sensor type... Try again.")
    sys.exit(1)


# 3. Generate random sensor value for each sensor
def generate_sensor_value(sensor_type):
    if sensor_type == "temperature":
        return round(random.uniform(-30, 20), 2)
    elif sensor_type == "pressure":
        return random.randint(300, 1100)
    elif sensor_type == "air-quality":
        return random.randint(0, 600)
    elif sensor_type == "co2":
        return random.randint(400, 5000)


# 4. Send the sensor data periodically (within 5 seconds)
def send_sensor_data(sensor_type):
    while True:
        sensor_value = generate_sensor_value(sensor_type)
        sensor_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        sensor_latitud = random.randint(-90, 90)
        sensor_longitud = random.randint(-180, 180)

        data = {
            "sensor_type": sensor_type,
            "unit": sensor_unit[sensor_type],
            "sensor_location_lat": sensor_latitud,
            "sensor_location_lon": sensor_longitud,
            "timestamp": sensor_timestamp,
            "value": sensor_value,
        }
        # 4.1 Send the POST request to the flask server
        json_data = json.dumps(data).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        try:
            request = urllib.request.Request(
                URL, data=json_data, headers=headers, method="POST"
            )
            response = urllib.request.urlopen(request)
            print(f"Sent data: {data}, Response: {response.read().decode()}")
        except Exception as e:
            print(f"Error with the data: {e}")
        time.sleep(5)  # Send data every 5 seconds


send_sensor_data(sensor_type_argument)
