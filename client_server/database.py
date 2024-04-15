import os
import pymongo
# Client mongoDB database connection
MONGO_URL_AUTH = f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{
    os.environ['MONGO_INITDB_ROOT_PASSWORD']}@{os.environ['SERVER_DB_HOST']}:27017"
db_client = pymongo.MongoClient(MONGO_URL_AUTH)


def get_collections():
    sensors_collection = db_client[os.environ['SERVER_DB_NAME']
                                   ][os.environ['SENSORS_DB_COLLECTION']]
    notifications_collection = db_client[os.environ['SERVER_DB_NAME']
                                         ][os.environ['NOTIFICATIONS_DB_COLLECTION']]
    return sensors_collection, notifications_collection
