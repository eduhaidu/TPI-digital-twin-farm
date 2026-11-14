from influxdb_client_3 import InfluxDBClient3, WritePrecision, Point  # type: ignore
import dotenv
import os
import pandas as pd
from typing import cast
from datetime import datetime, timezone

class InfluxDBConnection:
    def __init__(self):
        dotenv.load_dotenv()
        self.host = os.getenv("INFLUXDB_HOST")
        self.token = os.getenv("INFLUXDB_TOKEN")
        self.database = os.getenv("INFLUXDB_DATABASE")
        self.client = InfluxDBClient3(host=self.host, token=self.token, database=self.database) 

    def write_data(self, data):
        if self.check_duplicate_timestamp(data):
            print(f"Duplicate timestamp found for data: {data}. Skipping write to InfluxDB.")
            return
        sensor_id = int(data["sensor_id"])
        if sensor_id < 0:
            raise ValueError("sensor_id must be a non-negative integer")

        point = Point("readings").field("moisture", str(data["moisture"]))
        reading_id = data.get("reading_id")
        if reading_id is not None:
            point = point.tag("reading_id", str(reading_id))
        point = point.time(self.convert_timestamp(data), WritePrecision.NS)
        line = point.to_line_protocol()
        measurement_and_tags, fields_and_timestamp = line.split(" ", 1)
        fields, timestamp = fields_and_timestamp.rsplit(" ", 1)
        line = f"{measurement_and_tags} sensor_id={sensor_id}u,{fields} {timestamp}"
        self.client.write(line, write_precision=WritePrecision.NS)

    def read_data(self, sensor_id):
        sensor_id_literal = str(sensor_id).replace("'", "''")
        query = (
            "SELECT * FROM readings "
            "WHERE time >= now() - INTERVAL '1 hour' "
            f"AND sensor_id = '{sensor_id_literal}'"
        )
        result = self.client.query(query)
        return result

    def check_duplicate_timestamp(self, data):
        timestamp = self.convert_timestamp(data)
        timestamp_literal = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
        sensor_id_literal = str(data.get("sensor_id", "")).replace("'", "''")
        query = (
            "SELECT 1 FROM readings "
            f"WHERE time = TIMESTAMP '{timestamp_literal}' "
            f"AND sensor_id = '{sensor_id_literal}' LIMIT 1"
        )
        result = cast(pd.DataFrame, self.client.query(query, mode="pandas"))
        return not result.empty

    def convert_timestamp(self, data):
        timestamp = datetime(data["year"], data["month"], data["day"], data["hour"], data["minute"], data["second"], tzinfo=timezone.utc)
        return timestamp