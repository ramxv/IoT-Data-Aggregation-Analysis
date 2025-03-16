# IoT Sensor Data Collection System

## Project Overview

This project collects, stores, and analyzes IoT sensor data using Flask and Hadoop. The system runs multiple sensor containers, a Flask API for data ingestion, and a Hadoop container for batch processing.

## Folder Structure

```
project-root/
│── flask-server/         # Flask application
│   ├── app.py           # Main Flask app
│   ├── templates/       # HTML templates (if using render_template)
│   ├── static/          # Static files (CSS, JS, images)
│   ├── Dockerfile       # Dockerfile for Flask container
│
│── sensors/             # Virtual sensor container
│   ├── sensor.py        # Sensor script
│   ├── Dockerfile       # Dockerfile for sensor containers
│
│── hadoop/              # Hadoop batch processing container
│   ├── process.py       # Hadoop processing script
│   ├── Dockerfile       # Dockerfile for Hadoop container
│
│── database.py
```

## Setup Instructions

### 1. Build Docker Images

Run the following commands to build the Docker images for each component:

```sh
# Flask server image
cd flask-server
docker build -t flask-server .

# Sensor image
cd ../sensors
docker build -t sensor-image .

# Hadoop image
cd ../hadoop
docker build -t hadoop-container .
```

### 2. Run Containers

#### Flask Server

```sh
docker run -d --name flask-server -p 5000:5000 flask-server
```

#### Sensors

You can run multiple sensors with different types:

```sh
docker run -d --name temp_sensor sensor-image python sensor.py temperature
docker run -d --name pressure_sensor sensor-image python sensor.py pressure
docker run -d --name air_quality_sensor sensor-image python sensor.py air-quality
docker run -d --name co2_sensor sensor-image python sensor.py co2
```

#### Hadoop

```sh
docker run -d --name hadoop-container hadoop-container
```

### 3. Network Setup

Since Docker Compose is not used, create a network manually and connect all containers:

```sh
docker network create iot-network

# Connect containers to the network
docker network connect iot-network flask-server
docker network connect iot-network sensor-image
docker network connect iot-network hadoop-container
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
