import os
import json
import requests
from fastapi import FastAPI, BackgroundTasks
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt

app = FastAPI(
    title='Input Service',
)

equipments_ids = []

# InfluxDB configuration
INFLUX_URL = f"http://{os.environ['DOCKER_INFLUXDB_INIT_HOST']}:{os.environ['DOCKER_INFLUXDB_INIT_PORT']}"
INFLUX_TOKEN = os.environ['DOCKER_INFLUX_TOKEN']
INFLUX_ORG = os.environ['DOCKER_INFLUXDB_INIT_ORG']
INFLUX_BUCKET = os.environ['DOCKER_INFLUXDB_INIT_BUCKET']

# MQTT broker details
MQTT_BROKER = "mosquitto"  # Docker service name
MQTT_PORT = os.environ['MQTT_PORT']
MQTT_USER = os.environ['MQTT_USER']
MQTT_PASSWORD = os.environ['MQTT_PASSWORD']

MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_CLIENT_ID = f'fastapi_{os.environ["DOCKER_INFLUXDB_INIT_ORG"]}'
mqtt.Client.connected_flag = False

influx_client = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
influx_write_api = influx_client.write_api()


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
    # the message format is as follows {"equipmentId": "EQ-12495", "value": 12.34, "timestamp": "2021-09-01T12:00:00-05:00"}
    print("Parsing message", flush=True)
    message = json.loads(payload)
    try:
        json_body = [
            {
                "measurement": "sensor_data",
                "tags": {
                    "equipment_id": message["equipmentId"],
                },
                "fields": {
                    "value": message["value"]
                },
                "time": message["timestamp"]
            }
        ]
        influx_write_api.write(INFLUX_BUCKET, INFLUX_ORG, json_body)
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

    try:
        json_body = [
            {
                "measurement": "sensor_data",
                "tags": {
                    "equipment_id": sensor_data["equipmentId"],
                },
                "fields": {
                    "value": sensor_data["value"]
                },
                "time": sensor_data["timestamp"]
            }
        ]
        influx_write_api.write(INFLUX_BUCKET, INFLUX_ORG, json_body)
        return {"message": "Sensor data added successfully through HTTP"}
    except Exception as e:
        return {"message": f"Failed to process sensor data: {str(e)}"}
