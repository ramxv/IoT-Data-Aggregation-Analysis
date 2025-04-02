from flask import Flask, jsonify, request, render_template, Response
import sqlite3

app = Flask(__name__)

DB = "iot_data.db"


@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")


@app.route("/store", methods=["POST"])
def store_sensor_data():
    try:
        data = request.get_json()  # Ensure proper JSON parsing
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        print("Received data:", data)  # Debugging line

        sensor_id = get_sensor_id(
            data["sensor_location_lat"], data["sensor_location_lon"]
        )
        type_id = get_sensor_type(data["sensor_type"], data["unit"])

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO measurements (sensor_id, type_id, timestamp, value) VALUES (?,?,?,?)""",
            (sensor_id, type_id, data["timestamp"], data["value"]),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Data received successfully"}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500  # Return JSON error response


@app.route("/retrieve")
def retrieve_sensor_data():
    sensor_id = request.args.get("sensor_id")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    if not sensor_id or not start_time or not end_time:
        return render_template(
            "error.html", message="Error. Missing parameter on the URL"
        )

    retrieve_query = """
        SELECT type_id, timestamp, value 
        FROM measurements 
        WHERE type_id = ? 
        AND timestamp BETWEEN ? AND ? 
        ORDER BY type_id, timestamp ASC
    """
    table_col_query = """ SELECT unit FROM sensortypes WHERE type_id = ? """

    cursor.execute(retrieve_query, (sensor_id, start_time, end_time))
    result = cursor.fetchall()

    cursor.execute(table_col_query, (sensor_id))
    result_col = cursor.fetchone()

    conn.close()

    retrieve_data = [
        {"type_id": row[0], "timestamp": row[1], "value": row[2]} for row in result
    ]

    return render_template(
        "retrieve.html", sensor_id=sensor_id, sensor_col=result_col, data=retrieve_data
    )


@app.route("/fetch")
def fetch_sensor_data():
    type_sensor = request.args.get("type")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    fetch_query = """
        SELECT m.timestamp, m.value, s.latitude, s.longitude 
        FROM measurements m 
        JOIN sensors s ON m.sensor_id = s.sensor_id 
        JOIN sensortypes st ON m.type_id = st.type_id 
        WHERE st.type_name = ?
    """

    cursor.execute(fetch_query, (type_sensor,))
    result_fetch = cursor.fetchall()
    conn.close()

    if not type_sensor:
        return render_template(
            "error.html", message="Error. Missing parameter on the URL"
        )

    fetch_data = format_fetch_output(result_fetch)

    return Response(
        fetch_data,
        mimetype="text/plain",
        headers={
            "Content-disposition": "attachment; filename=sensor_measurements_data.txt"
        },
    )


@app.route("/store", methods=["GET"])
def get_sensor_data():
    """Retrieve all sensor data."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.measurement_id, s.latitude, s.longitude, t.type_name, t.unit, m.timestamp, m.value
        FROM measurements m
        JOIN sensors s ON m.sensor_id = s.sensor_id
        JOIN sensortypes t ON m.type_id = t.type_id
    """)

    rows = cursor.fetchall()
    conn.close()

    # Convert to JSON format
    sensor_data_list = [
        {
            "measurement_id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "sensor_type": row[3],
            "unit": row[4],
            "timestamp": row[5],
            "value": row[6],
        }
        for row in rows
    ]

    return jsonify(sensor_data_list), 200


def format_fetch_output(fetch_output):
    format_fetch_rows = []
    for rows in fetch_output:
        string_output = [str(output) for output in rows]
        txt_output = ",".join(string_output)
        format_fetch_rows.append(txt_output)

    txt_content = "\n".join(format_fetch_rows)

    return txt_content


def get_sensor_id(lat, lon):
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sensor_id FROM sensors WHERE latitude = ? AND longitude = ?",
            (lat, lon),
        )
        result = cursor.fetchone()
        if result:
            sensor_id = result[0]
        else:
            cursor.execute(
                "INSERT INTO sensors (latitude, longitude) VALUES (?, ?)", (lat, lon)
            )
            conn.commit()
            sensor_id = cursor.lastrowid
        conn.close()
        return sensor_id
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return None


def get_sensor_type(type_name, unit):
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT type_id FROM sensortypes WHERE type_name = ? AND unit = ?",
            (type_name, unit),
        )
        result = cursor.fetchone()

        if result:
            type_id = result[0]
        else:
            cursor.execute(
                "INSERT INTO sensortypes (type_name, unit) VALUES (?,?)",
                (type_name, unit),
            )
            conn.commit()
            type_id = cursor.lastrowid

        conn.close()
        return type_id

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
