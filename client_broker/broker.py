
import sys
import json

import paho.mqtt.client
from sqlalchemy.orm import sessionmaker

from client_broker import SETTINGS
from client_broker.session import ENGINE
from client_broker.utils import insert_payload


def on_connect(client, userdata, flags, rc):
    print("connected (%s)" % client._client_id)
    client.subscribe(topic="#", qos=2)

def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    insert_payload(payload)

def main():
    client = paho.mqtt.client.Client(client_id="albert-subs", clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host=SETTINGS.BROKER_HOST, port=1883)
    client.loop_forever()

if __name__ == "__main__":
    main()

sys.exit(0)
