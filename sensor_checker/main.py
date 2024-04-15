from confluent_kafka import Consumer, Producer
from dateutil.parser import parse
import socket
import json
import os
import datetime
import requests
import time
import pymongo
from pydantic import BaseModel

consumer_conf = {'bootstrap.servers': f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
                 'group.id': "id_checker",
                 'enable.auto.commit': True,
                 'auto.offset.reset': 'earliest'}

# Kafka producer details
producer_conf = {'bootstrap.servers': f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
                 'client.id': socket.gethostname(), "compression.type": "gzip", "linger.ms": 0, "batch.num.messages": 100,
                 "queue.buffering.max.messages": 100000, "queue.buffering.max.ms": 1000, "message.send.max.retries": 10,
                 "retry.backoff.ms": 100, "socket.keepalive.enable": True,
                 "socket.nagle.disable": True, "socket.max.fails": 3, "broker.address.ttl": 1000,
                 "api.version.request": True, "api.version.fallback.ms": 0}


# Client mongoDB database connection
MONGO_URL_AUTH = f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{
    os.environ['MONGO_INITDB_ROOT_PASSWORD']}@{os.environ['SERVER_DB_HOST']}:27017"
db_client = pymongo.MongoClient(MONGO_URL_AUTH)
# get the database and collection
sensors_collection = db_client[os.environ['SERVER_DB_NAME']
                               ][os.environ['SENSORS_DB_COLLECTION']]
notifications_collection = db_client[os.environ['SERVER_DB_NAME']
                                     ][os.environ['NOTIFICATIONS_DB_COLLECTION']]

# get all sensors from the database and store their equipmentId
sensors = sensors_collection.find()
equipment_ids = [sensor['equipmentId'] for sensor in sensors]


class Sensor(BaseModel):
    equipmentId: str
    name: str
    type: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime


class Notification(BaseModel):
    equipmentId: str
    type: str
    message: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime


def new_sensor(equipment_id):
    # create a new Sensor with the equipment_id and insert it into the database
    sensor = Sensor(equipmentId=equipment_id, name='Sensor', type='Temperature',
                    createdAt=datetime.datetime.now(), updatedAt=datetime.datetime.now())
    notification = Notification(equipmentId=equipment_id, type='info',
                                message='New sensor created', createdAt=datetime.datetime.now(), updatedAt=datetime.datetime.now())
    try:
        sensors_collection.insert_one(sensor.dict())
        equipment_ids.append(equipment_id)
        print(f'New sensor inserted: {equipment_id}', flush=True)
        try:
            producer.produce("sensors_created", key='new_sensor',
                             value=json.dumps(sensor.dict(), default=str))
            producer.flush()
        except Exception as e:
            print(f'Failed to send new sensor to kafka: {str(e)}')

        try:
            notifications_collection.insert_one(notification.dict())
            print(f'New notification inserted: {
                  notification.dict()}', flush=True)
        except Exception as e:
            print(f'Failed to insert new notification: {str(e)}')

    except Exception as e:
        print(f'Failed to insert new sensor: {str(e)}')
        return False


def check_new_sensor(measure):
    # check if the sensor is new
    if measure['equipmentId'] not in equipment_ids:
        new_sensor(measure['equipmentId'])
    return measure


# iniatialization
time.sleep(1)
consumer = Consumer(consumer_conf)
time.sleep(1)
producer = Producer(producer_conf)
time.sleep(1)
consumer.subscribe([os.environ['KAFKA_INFLUXDB_TOPIC']])

print('Sensor Checker is running', flush=True)
print(f'Connected to database {os.environ["SERVER_DB_NAME"]}\nURL={
      MONGO_URL_AUTH}', flush=True)
print(f'Connected to kafka broker {os.environ["KAFKA_HOST"]}:{
      os.environ["KAFKA_PORT"]}', flush=True)
print(f'equipment_ids: {equipment_ids}', flush=True)

running = True
while running:
    try:
        raw_measure_msgs = consumer.consume(100, timeout=1)
        for raw_measure_msg in raw_measure_msgs:
            if raw_measure_msg.error():
                print('Message error!')
                continue
            else:
                measure = json.loads(raw_measure_msg.value().decode())
                # print(measure, flush=True)

            measure = check_new_sensor(measure)
        producer.poll(0)

    except KeyboardInterrupt:
        running = False
    except Exception as e:
        print(e, flush=True)
