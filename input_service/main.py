# MQTT consumer and HTTP gateway for the input data
import os
import json
import socket
import requests
from fastapi import FastAPI, BackgroundTasks
import paho.mqtt.client as mqtt
from confluent_kafka import Producer
from contextlib import asynccontextmanager
import datetime

app = FastAPI(
    title='Input Service',
)

# MQTT broker details
MQTT_BROKER = "mosquitto"  # Docker service name
MQTT_PORT = os.environ['MQTT_PORT']
MQTT_USER = os.environ['MQTT_USER']
MQTT_PASSWORD = os.environ['MQTT_PASSWORD']

MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_CLIENT_ID = f'fastapi_{os.environ["DOCKER_INFLUXDB_INIT_ORG"]}'
mqtt.Client.connected_flag = False
KAFKA_TOPIC = os.environ['KAFKA_INFLUXDB_TOPIC']

# Kafka producer details
conf = {'bootstrap.servers': f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
        'client.id': socket.gethostname(), "compression.type": "gzip", "linger.ms": 0, "batch.num.messages": 100,
        "queue.buffering.max.messages": 100000, "queue.buffering.max.ms": 1000, "message.send.max.retries": 10,
        "retry.backoff.ms": 100, "socket.keepalive.enable": True,
        "socket.nagle.disable": True, "socket.max.fails": 3, "broker.address.ttl": 1000,
        "api.version.request": True, "api.version.fallback.ms": 0}

producer = Producer(conf)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # on shutdown
    producer.flush()
    gc.collect()


async def flush_producer(producer):
    while True:
        await asyncio.sleep(1)
        # Flush the producer every 1000 messages sent to avoid memory leak
        if producer.produce_count() >= 1000:
            producer.flush()


@app.on_event('shutdown')
async def shutdown_event():
    client.loop_stop()
    producer.flush()
    producer.close()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker.")
        client.connected_flag = True
    else:
        print("Connection failed: ", reason_code)
        client.connected_flag = False


def on_disconnect(client, userdata, flags, reason_code, properties):
    print("Disconnected from MQTT broker.")
    client.connected_flag = False


def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(MQTT_TOPIC+" "+str(message.payload), flush=True)
    # Process incoming sensor data
    # the message format is as follows {"equipmentId": "EQ-12495", "value": 12.34, "timestamp": "2024-04-14T16:54:49-03:00"}
    print("Parsing message", flush=True)
    message = json.loads(payload)
    # verify the message format
    if "equipmentId" not in message or "value" not in message or "timestamp" not in message:
        print("Invalid message format", flush=True)
        return
    # format the message
    # sensors transmit the timestamp in the format "2024-04-14T16:54:49-03:00"
    # the -03:00 is the timezone offset
    # but we want to store the timestamp in UTC in the format "2006-01-02T15:04:05Z07:00"
    # so we need to remove the timezone offset and convert the timestamp to UTC
    message["timestamp"] = datetime.datetime.fromisoformat(
        message["timestamp"]).astimezone(datetime.timezone.utc).replace(tzinfo=None).isoformat()

    # send the message to Kafka
    try:
        producer.produce(KAFKA_TOPIC, value=json.dumps(message, default=str))
        producer.poll(0)
        producer.flush()
        print("Message sent to Kafka", flush=True)
    except Exception as e:
        print(f'Failed to process sensor data: {str(e)}')


mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2, client_id=MQTT_CLIENT_ID)
# Set username and password
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, int(MQTT_PORT), 60)  # Connect to MQTT broker
mqtt_client.subscribe(MQTT_TOPIC)  # Subscribe to sensor topic
mqtt_client.loop_start()


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI service"}


@app.on_event("startup")
async def startup_event():
    mqtt_client.loop_start()  # Start MQTT client loop


@app.on_event("shutdown")
async def shutdown_event():
    mqtt_client.loop_stop()  # Stop MQTT client loop


@app.post('/sensor-data/{password}')
async def add_sensor_data(sensor_data: dict, password: str):
    if password != os.environ['MQTT_PASSWORD']:
        return {"message": "Invalid password"}

    if "equipmentId" not in message or "value" not in message or "timestamp" not in message:
        print("Invalid message format", flush=True)
        return
    # format the message
    # sensors transmit the timestamp in the format "2024-04-14T16:54:49-03:00"
    # the -03:00 is the timezone offset
    # but we want to store the timestamp in UTC in the format "2006-01-02T15:04:05Z07:00"
    # so we need to remove the timezone offset and convert the timestamp to UTC
    sensor_data["timestamp"] = datetime.datetime.fromisoformat(
        sensor_data["timestamp"]).astimezone(datetime.timezone.utc).replace(tzinfo=None).isoformat()
    try:
        producer.produce(KAFKA_TOPIC, value=json.dumps(
            sensor_data, default=str))
        producer.poll(0)
        producer.flush()
        print("Message sent to Kafka", flush=True)
        return {"message": "Sensor data added successfully"}
    except Exception as e:
        print(f'Failed to process sensor data: {str(e)}')
        return {"message": "Failed to process sensor data"}
