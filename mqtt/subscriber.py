import paho.mqtt.client as mqtt
import sys

host = 'test.mosquitto.org'
port = 1883

class Subscriber:
    def __init__(self, topic):
        self.client = mqtt.Client('subscriber')
        self.client.on_message = self.message_received
        self.client.connect(host, port)
        self.client.subscribe(topic)

    def message_received(self, client, user, message):
        payload = str(message.payload.decode('utf-8'))
        print('Subscriber: received message: ' + payload + ' on topic: ' + message.topic)


subscriber = Subscriber(sys.argv[1])
subscriber.client.loop_forever()
