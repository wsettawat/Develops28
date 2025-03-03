# python3.6

import random

from paho.mqtt import client as mqtt_client


broker = '192.168.68.102'
topic = "display/uwb/floor1"
#topic = "sensor/uwb_tag"
#broker = 'broker.emqx.io'
port = 1883
#topic = "python/mqtt"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 1000)}'
username = "wedo"
password = "123456"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):        
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #print("sub")
    client.subscribe(topic)
    client.on_message = on_message


def run():

    client = connect_mqtt()
    print("connect done")
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()