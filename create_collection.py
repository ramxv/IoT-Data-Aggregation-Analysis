import sqlite3

conn = sqlite3.connect('iot_data.db')
cursor = conn.cursor()

cursor.executescript('''
CREATE TABLE sensors (
    sensor_id INTEGER PRIMARY KEY,
    sensor_name TEXT NOT NULL,
    latitude REAL,
    longitude REAL
);

CREATE TABLE sensortypes (
    type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL,
    unit TEXT NOT NULL
);

CREATE TABLE measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER,
    type_id INTEGER,
    timestamp TEXT,
    value REAL,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id),
    FOREIGN KEY (type_id) REFERENCES sensortypes(type_id)
);
''')

conn.commit()
conn.close()