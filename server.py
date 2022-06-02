import time
from paho.mqtt import client as mqtt_client
from pylsl import StreamInlet, resolve_streams

broker = 'localhost'
port = 1883
client_id = f'python-lsl-mqtt-bridge'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        pass
        #print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

""" def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(topic)
    client.on_message = on_message """

def run():
    client = connect_mqtt()
    client.loop_start()
    while True:
        # looking for streams
        streams = list(resolve_streams(0.5))
        for streamnum in range(len(streams)):
            print(" ", streamnum,
                streams[streamnum].name().ljust(40),
                streams[streamnum].type().ljust(15),
                streams[streamnum].hostname())
        if (len(streams) >= 1):
            topic = f"test/lsl/{streams[0].hostname()}/{streams[0].type().strip()}/{streams[0].name().replace(' ','')}"
            inlet = StreamInlet(streams[int(0)])
            break
    while True:
        sample, timestamp = inlet.pull_sample(timeout=0.0)
        if sample is None:
            pass
        else:
            #print(str(sample))
            publish(client, topic, str(sample))

if __name__ == '__main__':
    run()
