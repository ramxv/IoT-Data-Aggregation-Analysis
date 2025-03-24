import urllib.request
import urllib.parse
import json
import random
import time
import sys
from datetime import datetime

# 1. Variables Declaration
URL = "http://flask_server:8080/store"
sensor_type_argument = sys.argv[1]
sensor_type = ["temperature", "pressure", "air-quality", "co2"]
sensor_unit = {
    "temperature": "°C",
    "pressure": "hPa",
    "air-quality": "PM10",
    "co2": "ppm",
}
# 2. Validation of argument in case the user forget to introduce a sensor type
if len(sys.argv) > 1:
    sensor_type_argument = sys.argv[1]
else:
    print("No sensor type provided. Please introduce a sensor type.")
    sys.exit(1)

# 3. Declarate function for each sensor
def temperature_sensor(argv):
    sensor_value = round(random.uniform(-30, 20), 2)
    send_sensor_data(argv, sensor_value)


def pressure_sensor(argv):
    sensor_value = random.randint(300, 1100)
    send_sensor_data(argv, sensor_value)


def air_quality_sensor(argv):
    sensor_value = random.randint(0, 600)
    send_sensor_data(argv, sensor_value)


def co2_sensor(argv):
    sensor_value = random.randint(400, 5000)
    send_sensor_data(argv, sensor_value)

# 4. Send the sensor data periodically (within 5 seconds) 
def send_sensor_data(sensor_type, sensor_value):
    while True:
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
				#	4.1 Send the POST request to the flask server 
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


# 6. Validation of the arguments passed through cli
if len(sensor_type_argument) > 1:
    if sensor_type_argument in sensor_type:
        if sensor_type_argument == "temperature":
            temperature_sensor(sensor_type_argument)
        elif sensor_type_argument == "pressure":
            pressure_sensor(sensor_type_argument)
        elif sensor_type_argument == "air-quality":
            air_quality_sensor(sensor_type_argument)
        else:
            co2_sensor(sensor_type_argument)

    else:
        # print invalid sensor type...
        print("Invalid sensor type... Try again.")
else:
    print("Any sensor was introduced... Please introduce a sensor type.")
    # print error message...
