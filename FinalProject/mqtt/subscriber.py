import paho.mqtt.client as mqtt
import sys

host = '127.0.0.1'
port = 1883

# klasa subscribera mqtt; w konstruktorze rejestruje klienta mqtt i podłącza funkcję
# do obsługi przychodzących wiadomości, która je wypisuje
class Subscriber:
    def __init__(self, topic, name):
        self.client = mqtt.Client(name)
        self.client.on_message = self.message_received
        self.client.connect(host, port)
        self.client.subscribe(topic)

    def message_received(self, client, user, message):
        payload = str(message.payload.decode('utf-8'))
        print('Subscriber: received message: ' + payload + ' on topic: ' + message.topic)


# skrypt tworzący subscribera i uruchamiający jego nieskończoną pętlę
subscriber = Subscriber(sys.argv[1], sys.argv[2])
subscriber.client.loop_forever()
