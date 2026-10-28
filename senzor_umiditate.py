import pandas as pd
import numpy as np
import paho.mqtt.client as mqtt
import time

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

    def send_data_to_gateway(self, data, topic, time_interval=1):
        if data is not None:
            for index, row in data.iterrows():
                message = row.to_json()
                self.publish(topic, message)
                time.sleep(time_interval)
        else:
            print("No data to send to the gateway.")

def main():
    broker_address = "localhost"  # Replace with your MQTT broker address
    topic = "senzor/umiditate"
    file_path = "datasets/plant_vase1.csv"  # Replace with your CSV file path

    senzor = SenzorUmiditate(broker_address)
    senzor.subscribe(topic)

    data = SenzorUmiditate.read_data(file_path)
    senzor.send_data_to_gateway(data, topic)

if __name__ == "__main__":
    main()

    


