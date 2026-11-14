from fastapi import FastAPI
from influxdb_connection import InfluxDBConnection

app = FastAPI()
influx_db = InfluxDBConnection()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Digital Twin Farm API!"}

@app.post("/readings")
async def create_data(data: dict):
    influx_db.write_data(data)
    return {"message": "Data created successfully!", "data": data}

@app.get("/readings/{sensor_id}")
async def read_sensor_data(sensor_id: str):
    data = influx_db.read_data(sensor_id)
    return {"message": "Data retrieved successfully!", "data": data}