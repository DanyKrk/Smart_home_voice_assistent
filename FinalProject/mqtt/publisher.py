import paho.mqtt.client as mqtt

host = '127.0.0.1'
port = 1883

# klasa publishera mqtt; w metodzie publish wysyła dany jako argument payload na odpowiedni temat
class Publisher:
    def __init__(self):
        self.client = mqtt.Client('publisher')
        self.client.connect(host, port)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
