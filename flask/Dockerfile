FROM python:3.12-bookworm

WORKDIR /app

RUN pip install Flask

COPY /app.py .

EXPOSE 8080

CMD ["python3", "app.py"]
