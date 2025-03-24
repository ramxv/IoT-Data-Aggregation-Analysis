FROM python:3.12-bookworm

WORKDIR /flask-server

COPY app.py .

COPY iot_data.db .

COPY ./templates /flask-server/templates

COPY ./static /flask-server/static

RUN apt update && apt install -y sqlite3

RUN pip install Flask

EXPOSE 8080

CMD ["python3", "app.py"]
