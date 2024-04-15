import os
import pymongo
# import uvicorn
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, APIRouter, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
import paho.mqtt.client as mqtt

from models import SensorTimeSeries, Sensor
from database import get_sensors_collection, get_sensor_data_collection
from utils import convert_object_id

sensors_collection = get_sensors_collection()
sensor_data_collection = get_sensor_data_collection()

app = FastAPI(
    title='Input Service',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MQTT broker details
MQTT_BROKER = "mosquitto"  # Docker service name
MQTT_PORT = os.environ['MQTT_PORT']
MQTT_USER = os.environ['MQTT_USER']
MQTT_PASSWORD = os.environ['MQTT_PASSWORD']
MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_CLIENT_ID = f'fastapi_{os.environ["DOCKER_INFLUXDB_INIT_ORG"]}'
mqtt.Client.connected_flag = False


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
    # now we must insert the data into the database
    try:
        sensor_data = {
            "equipment_id": message["equipmentId"],
            "value": message["value"],
            "timestamp": message["timestamp"]
        }
        new_sensor_data = sensor_data_collection.insert_one(sensor_data)
        # chec if the equipment_id exists in the sensors collection
        sensor = sensors_collection.find_one(
            {"equipment_id": message["equipmentId"]})
        if sensor is None:
            # create a new sensor
            sensor = {
                "equipment_id": message["equipmentId"],
                "name": f"sensor-{message['equipmentId']}",
                "type": "sensor",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            new_sensor = sensors_collection.insert_one(sensor)
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


@app.post("/sensor-data")
async def post_sensor_data(sensor_data: SensorTimeSeries):
    try:
        sensor_data = sensor_data.__dict__
        new_sensor_data = sensor_data_collection.insert_one(sensor_data)

        # chec if the equipment_id exists in the sensors collection
        sensor = sensors_collection.find_one(
            {"equipment_id": sensor_data["equipment_id"]})
        if sensor is None:
            # create a new sensor
            sensor = {
                "equipment_id": sensor_data["equipment_id"],
                "name": f"sensor-{sensor_data['equipment_id']}",
                "type": "sensor",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            new_sensor = sensors_collection.insert_one(sensor)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Sensor data created successfully"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Failed to create sensor data: {str(e)}"})


@app.get("/sensors")
async def get_sensors():
    sensors = list(sensors_collection.find())

    if len(sensors) == 0:
        return []

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(sensors, default=convert_object_id)))


@app.get("/timerange/{start_date}/{end_date}")
async def get_sensor_data_by_timerange(start_date: str, end_date: str):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Invalid date format: {str(e)}"})

    sensor_data = list(sensor_data_collection.find(
        {"timestamp": {"$gte": start_date, "$lt": end_date}}))

    if len(sensor_data) == 0:
        return []

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(sensor_data, default=convert_object_id)))


@app.get("/range/{last_n_days}")
async def get_sensor_data_by_range(last_n_days: int):
    try:
        start_date = datetime.utcnow() - timedelta(days=last_n_days)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Invalid date format: {str(e)}"})

    sensor_data = list(sensor_data_collection.find(
        {"timestamp": {"$gte": start_date}}))

    if len(sensor_data) == 0:
        return []

    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(sensor_data, default=convert_object_id)))
