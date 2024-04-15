import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime, timedelta, timezone

# MQTT broker details
broker_address = "localhost"  # Docker service name
port = 1883
username = "radix"
password = "123456789"
topic = "measures"


def generate_dummy_data():
    # Generate dummy data in JSON format
    equipment_id = "EQ-22498"
    value = round(random.uniform(0, 100), 2)
    # The timestamp must have the format "2023-02-15T01:30:00.000-05:00"
    # The -05:00 is the timezone offset
    # So we want to transmit the timestamp in the format above, with the local timezone offset
    timestamp = datetime.now(timezone.utc).astimezone().replace(
        microsecond=0).isoformat()

    return {
        "equipmentId": equipment_id,
        "value": value,
        "timestamp": timestamp
    }


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker.")
        client.connected_flag = True
        client.subscribe(topic)
    else:
        print("Connection failed: ", reason_code)
        client.connected_flag = False


def on_disconnect(client, userdata, flags, reason_code, properties):
    print("Disconnected from MQTT broker.")
    client.connected_flag = False


def on_connect_fail(client, userdata, flags, reason_code, properties):
    print("Connection failed: ", reason_code)
    client.connected_flag = False


def on_message(client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server.
    print(msg.topic+" "+str(msg.payload))


# Initialize MQTT client
mqtt.Client.connected_flag = False
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                     client_id="dummy_producer")
client.username_pw_set(username, password)
client.on_connect = on_connect
client.loop_start()
print("Connecting to broker ", broker_address)
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to MQTT broker
client.connect(broker_address, port)


# retry to connect to the broker 5 times if the connection failed
retry = 0
while not client.connected_flag and retry < 5:
    time.sleep(2)
    print("Retrying to connect to the broker...")
    client.connect(broker_address, port)
    retry += 1

if not client.connected_flag:
    print("Failed to connect to the broker. Exiting...")
    exit(1)
else:
    try:
        while client.connected_flag:
            # Generate dummy data
            data = generate_dummy_data()

            # Convert data to JSON
            payload = json.dumps(data)

            # Publish data to MQTT broker
            client.publish(topic, payload)

            # Print published message for debugging
            print("Published:", payload)

            # Wait for some time before publishing the next message
            time.sleep(1)

    except KeyboardInterrupt:
        # Gracefully handle keyboard interrupt
        print("Exiting...")
        client.disconnect()
