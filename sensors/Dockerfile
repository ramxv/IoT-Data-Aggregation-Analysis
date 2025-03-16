FROM python:3.12-bookworm

WORKDIR /app

RUN pip install requests

COPY sensordata.py .

CMD ["python3", "sensordata.py"]
