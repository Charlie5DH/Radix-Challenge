import os
import pymongo

# Connect to MongoDB


def connect_to_mongo():
    url_auth = f'{os.environ["MONGO_INITDB_ROOT_USERNAME"]}:{os.environ["MONGO_INITDB_ROOT_PASSWORD"]}@'
    ip_port = f'{os.environ["CLIENT_DB_HOST"]}:{os.environ["CLIENT_DB_PORT"]}'
    db = pymongo.MongoClient(f'mongodb://{url_auth}{ip_port}')
    return db


def get_sensors_collection():
    db = connect_to_mongo()
    sensors_collection = db[os.environ["CLIENT_DB_NAME"]
                            ][os.environ["SENSORS_DB_COLLECTION"]]
    return sensors_collection


def get_sensor_data_collection():
    db = connect_to_mongo()
    sensor_data_collection = db[os.environ["CLIENT_DB_NAME"]
                                ][os.environ["SENSORS_MEASURES_DB_COLLECTION"]]
    return sensor_data_collection
