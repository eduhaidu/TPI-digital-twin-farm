import paho.mqtt.client as mqtt

class Gateway:
    def __init__(self, broker_address, port=1883):
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker_address, self.port)
        print(f"Connected to MQTT broker at {self.broker_address}:{self.port}")