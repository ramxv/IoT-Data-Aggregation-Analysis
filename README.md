# IoT Sensor Data Collection System

## Project Overview

This project collects, stores, and analyzes IoT sensor data using Flask and Hadoop. The system runs multiple sensor containers, a Flask API for data ingestion, and a Hadoop container for batch processing.

## Folder Structure

```
project-root/
│── flask/         # Flask application
│   ├── app.py           # Main Flask app
│   ├── templates/       # HTML templates (if using render_template)
│   ├── static/          # Static files (CSS, JS, images)
│   ├── Dockerfile       # Dockerfile for Flask container
│
│── sensors/             # Virtual sensor container
│   ├── sensor.py        # Sensor script
│   ├── Dockerfile       # Dockerfile for sensor containers
│
```

## Setup Instructions

### 1. Build Docker Images

Run the following commands to build the Docker images for each component:

```sh
# Flask server image
cd flask
docker build -t flask-server .

# Sensor image
cd sensors
docker build -t sensor-image .

```

### 2. Create Docker network

Run the following command to create the Docker network:

```sh
docker network create iot-network
```

### 3. Run Containers

#### Flask Server

```sh
docker run -d --name flask_server --network=iot-network -p 8080:8080 flask-server
```

#### Sensors

You can run multiple sensors with different types:

```sh
docker run -d --name temp_sensor --network=iot-network sensor-image python sensor.py temperature
docker run -d --name pressure_sensor --network=iot-network sensor-image python sensor.py pressure
docker run -d --name air_quality_sensor --network=iot-network sensor-image python sensor.py air-quality
docker run -d --name co2_sensor --network=iot-network sensor-image python sensor.py co2
```

## Troubleshooting

- If a container fails to start, check the logs:

  ```sh
  docker logs <container_name>
  ```

- Ensure all containers are connected to `iot-network`:

  ```sh
  docker network inspect iot-network
  ```
