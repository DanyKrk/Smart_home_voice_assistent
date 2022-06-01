import paho.mqtt.client as mqtt
import sys

host = '127.0.0.1'
port = 1883

class Subscriber:
    def __init__(self, topic, name):
        self.client = mqtt.Client(name)
        self.client.on_message = self.message_received
        self.client.connect(host, port)
        self.client.subscribe(topic)

    def message_received(self, client, user, message):
        payload = str(message.payload.decode('utf-8'))
        print('Subscriber: received message: ' + payload + ' on topic: ' + message.topic)


subscriber = Subscriber(sys.argv[1], sys.argv[2])
subscriber.client.loop_forever()
