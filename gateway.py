import paho.mqtt.client as mqtt

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

def main():
    broker_address = "127.0.0.1"  # Replace with your MQTT broker address
    gateway = Gateway(broker_address)
    gateway.connect()

if __name__ == "__main__":
    main()