import sqlite3

DATABASE = "iot_data.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.executescript("""

        DROP TABLE IF EXISTS measurements;
        DROP TABLE IF EXISTS sensors;
        DROP TABLE IF EXISTS sensortypes;

        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id INTEGER PRIMARY KEY,
            latitude REAL,
            longitude REAL
        );

        CREATE TABLE IF NOT EXISTS sensortypes (
            type_id INTEGER PRIMARY KEY,
            type_name TEXT NOT NULL,
            unit TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS measurements (
            measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER,
            type_id INTEGER,
            timestamp TEXT,
            value REAL,
            FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE,
            FOREIGN KEY (type_id) REFERENCES sensortypes(type_id) ON DELETE CASCADE
        );
        """)
        db.commit()


if __name__ == "__main__":
    init_db()
    print("Database successfuly initialized.")

