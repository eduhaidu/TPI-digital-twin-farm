import paho.mqtt.client as mqtt
import asyncio
import json
import requests
import os

class Gateway:
    def __init__(self, broker_address, port=1883):
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker_address, self.port)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected to MQTT broker at {self.broker_address}:{self.port}")
        self.subscribe("senzor/umiditate")

    def publish(self, topic, message):
        self.client.publish(topic, message)
        print(f"Published message to topic '{topic}': {message}")

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f"Subscribed to topic '{topic}'")

    def on_message(self, client, userdata, message):
        print(f"Received message from topic '{message.topic}': {message.payload.decode()}")
        self.store_data(message.payload.decode())
        self.send_data_to_backend(json.loads(message.payload.decode()))
        print(f"Data stored in 'date_umiditate.json': {message.payload.decode()}")

    def store_data(self, data):
        json_data = json.loads(data)
        try:
            with open("date_umiditate.json", "r", encoding="utf-8") as file:
                records = json.load(file)
        except FileNotFoundError:
            records = []

        if not isinstance(records, list):
            raise ValueError("date_umiditate.json must contain a JSON list")

        records.append(json_data)
        with open("date_umiditate.json", "w", encoding="utf-8") as file:
            json.dump(records, file, indent=2)
            file.write("\n")

    def send_data_to_backend(self, data):
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(f"{backend_url}/readings", headers=headers, json=data)
            if response.status_code == 200:
                print(f"Data sent to backend successfully: {data}")
            else:
                print(f"Failed to send data to backend. Status code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to backend: {e}")


def main():
    broker_address = "127.0.0.1"  
    gateway = Gateway(broker_address)
    gateway.connect()

if __name__ == "__main__":
    main()