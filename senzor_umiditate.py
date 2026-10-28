import pandas as pd
import numpy as np
import paho.mqtt.client as mqtt
import time
import argparse
import json

class SenzorUmiditate:
    def __init__(self, broker_address, port=1883):
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client()
        self.client.connect(self.broker_address, self.port)

    def publish(self, topic, message):
        self.client.publish(topic, message)
        print(f"Published message to topic '{topic}': {message}")

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f"Subscribed to topic '{topic}'")

    def on_message(self, client, userdata, message):
        print(f"Received message from topic '{message.topic}': {message.payload.decode()}")

    def read_data(file_path):
        try:
            data = pd.read_csv(file_path)
            return data
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return None

    def send_data_to_gateway(self, data, topic, time_interval=1, sensor_id=0):
        if data is not None:
            sensor_column_name = f"moisture{sensor_id}"
            if sensor_column_name not in data.columns:
                raise ValueError(f"Column '{sensor_column_name}' not found in the data.")

            for _, row in data.iterrows():
                message = json.dumps({
                    "sensor_id": sensor_id,
                    "hour": int(row["hour"]),
                    "minute": int(row["minute"]),
                    "moisture": float(row[sensor_column_name]),
                })
                self.publish(topic, message)
                time.sleep(time_interval)
        else:
            print("No data to send to the gateway.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sensor_id", type=int, choices=range(5), nargs="?", default=0)
    sensor_id = parser.parse_args().sensor_id

    broker_address = "localhost"  # Replace with your MQTT broker address
    topic = "senzor/umiditate"
    file_path = "datasets/plant_vase1.CSV"

    senzor = SenzorUmiditate(broker_address)
    senzor.subscribe(topic)

    data = SenzorUmiditate.read_data(file_path)
    senzor.send_data_to_gateway(data, topic, sensor_id=sensor_id)

if __name__ == "__main__":
    main()

    


