import paho.mqtt.client as mqtt

host = '127.0.0.1'
port = 1883

class Subscriber:
    def __init__(self):
        self.client = mqtt.Client('subscriber')
        self.client.on_message = self.message_received
        self.client.on_subscribe = self.subscribe_to_cmd
        self.client.connect(host, port)

    def message_received(self, client, user, message):
        payload = str(message.payload.decode('utf-8'))
        print('Subscriber: received message: ' + payload + ' on topic: ' + message.topic)

    def subscribe_to_cmd(self):
        self.client.subscribe('cmd/#')
