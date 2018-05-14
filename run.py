from app import app, socketio
import paho.mqtt.client as mqtt
from app.models.data import Data
from app.controllers.data import save_data
from json import loads
from pprint import pprint

topic = 'Tapajos-IoT'

# MQTT ON CONNECT FOR SUBSCRIBE THE TOPIC
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print('Subscribe on topic: {}'.format(topic))
    client.subscribe(topic)


# RECEIVE THE MESSAGE SENT TO BROKER 
def on_message(client, userdata, msg):
    msg = loads(msg.payload.decode())
    pprint(msg)
    save_data(msg)
    socketio.emit('received-data',msg)
    

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost")
    client.loop_start()
    socketio.run(
        app,
        host='0.0.0.0'
    )

