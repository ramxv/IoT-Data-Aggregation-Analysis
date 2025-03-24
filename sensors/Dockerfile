FROM python:3.12-bookworm

WORKDIR /sensor-data

COPY sensordata.py .

RUN pip install requests

CMD ["python3", "sensordata.py"]
