import os
import json
import pymongo
import numpy as np
import pandas as pd
import requests
from time import time
from database import get_collections
import datetime
from fastapi import FastAPI, HTTPException, status, APIRouter, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from models import Sensor, Notification, FormatOptions, JoinOptions
from utils import convert_object_id
from influxdb_client import InfluxDBClient
from influx_src import InfluxSource
from io import BytesIO

sensors_collection, notifications_collection = get_collections()

# InfluxDB configuration
INFLUX_URL = f"http://{os.environ['DOCKER_INFLUXDB_INIT_HOST']
                       }:{os.environ['DOCKER_INFLUXDB_INIT_PORT']}"
INFLUX_TOKEN = os.environ['DOCKER_INFLUX_TOKEN']
INFLUX_ORG = os.environ['DOCKER_INFLUXDB_INIT_ORG']
INFLUX_BUCKET = os.environ['DOCKER_INFLUXDB_INIT_BUCKET']

src = InfluxSource(INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG)

influx_client = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
influx_write_api = influx_client.write_api()

EXPECTED_COLUMNS = ["equipmentId", "timestamp", "value"]

app = FastAPI(title="Client Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/sensors", response_model=list[Sensor])
async def get_sensors():
    sensors = sensors_collection.find()
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(list(sensors), default=convert_object_id)))


@app.get("/sensors/{equipmentId}", response_model=Sensor)
async def get_sensor(equipmentId: str):
    sensor = sensors_collection.find_one({"equipmentId": equipmentId})
    if sensor:
        return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(sensor, default=convert_object_id)))
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")


@app.get("/notifications", response_model=list[Notification])
async def get_notifications():
    notifications = notifications_collection.find()
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json.dumps(list(notifications), default=convert_object_id)))


@app.post("/sensors", response_model=Sensor)
async def create_sensor(sensor: Sensor):
    sensor_data = sensor.__dict__
    sensor_data["createdAt"] = datetime.datetime.now()
    sensor_data["updatedAt"] = datetime.datetime.now()
    # check if sensor already exists
    sensor_exists = sensors_collection.find_one(
        {"equipmentId": sensor_data["equipmentId"]})
    if sensor_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sensor already exists")

    new_sensor = sensors_collection.insert_one(sensor_data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(json.dumps(sensor_data, default=convert_object_id)))


def get_dataframe(equipment_ids,
                  init_timestamp, end_timestamp,
                  aggregation_window, aggregation_function, merge_matrices, createEmpty):

    df = src.query(equipment_ids, init_timestamp, end_timestamp,
                   aggregation_window, aggregation_function, merge_matrices, createEmpty)
    try:
        df.sort_values('time', inplace=True)
    except KeyError:
        pass
    return df


def assert_equipment_ids_list(equipment_ids):
    if equipment_ids is None:
        return []
    if type(equipment_ids) is list:
        return equipment_ids
    if type(equipment_ids) is not str:
        raise TypeError('{equipment_ids} is neither a str nor list')
    if '[' in equipment_ids:
        return json.loads(equipment_ids)
    return [equipment_ids]


@app.get('/by_timestamp', tags=['Measures'])
async def measures_by_timestamp(equipment_ids: str, init_timestamp: str = '-inf', end_timestamp: str = 'now()',
                                aggregation_window='1d', aggregation_function='mean', merge_matrices: bool = False,
                                format: FormatOptions = FormatOptions.records, resample: bool = True,
                                createEmpty: bool = False):
    """
    **Retrieve measures from a set of sensors by timestamp**\n\n

    \tequipment_ids             json-like list of equipment_ids or single equipment_id\n
    \tinit_timestamp            Flux query compatible time (default: '-inf')\n
    \tend_timestamp             Flux query compatible time (default: 'now()')\n
    \taggregation_window        Flux query compatible relative time range: 1w, 1d, 10m, 4s, 1ms (default: '1d')\n
    \taggregation_function      Flux query compatible function (default: 'mean')\n
    \tformat string             Pandas compatible orientation (default: 'records')

    More info:\n
    [Flux query compatible time](https://docs.influxdata.com/flux/v0.x/stdlib/universe/range/#query-a-time-range-relative-to-now)\n
    [Flux query compatible function](https://docs.influxdata.com/flux/v0.x/stdlib/universe/#functions)\n
    [Pandas compatible orientation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html#pandas-dataframe-to-dict)
    """

    equipment_ids = assert_equipment_ids_list(equipment_ids)
    df = get_dataframe(equipment_ids,
                       init_timestamp, end_timestamp,
                       aggregation_window, aggregation_function, merge_matrices, createEmpty)

    if df.empty:
        return []

    if resample and createEmpty == False and aggregation_window != 'none':
        if aggregation_window[-1] == 'm':
            # Convert the aggregation window to match the expected format ('10m' to '10min', '5m' to '5min', etc.)
            aggregation_window = aggregation_window.replace('m', 'min')

        sensors = df['equipment_id'].unique()
        # extract subset of data for each sensor
        dfs = []
        for sensor in sensors:
            sub_df = df[df['equipment_id'] == sensor]
            sub_df.index = pd.to_datetime(sub_df.index)
            sub_df = sub_df.reset_index()
            sub_df = sub_df.resample(
                aggregation_window, on="time").mean(numeric_only=True)
            sub_df['equipment_id'] = sensor
            dfs.append(sub_df)

        df = pd.concat(dfs)
        for i in dfs:
            del i
        df.sort_values('time', inplace=True)
        df.reset_index(inplace=True, drop=False)
        resp = df.fillna('null').to_dict(orient=format.name)
    else:
        df.reset_index(inplace=True, drop=True)
        resp = df.fillna('null').to_dict(orient=format.name)

    del df
    return resp


@app.post('/upload_csv', tags=['Measures'])
async def upload_csv(file: UploadFile = File(...)):
    """
    Some of the plant's sensors may experience technical failures, resulting in gaps in the data. 
    To deal with this, the vendor can send CSV files with the lost data. 
    Add an endpoint to the API that receives a CSV file, parses the data and saves the values in the database.
    Table 1: CSV Format

    | equipmentId | timestamp                     | value |
    | ----------- | ----------------------------- | ----- |
    | EQ-12495    | 2023-02-15T01:30:00.000-05:00 | 78.42 |

    \tfile              CSV file with sensor data\n
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    try:
        df = pd.read_csv(BytesIO(contents))
    except pd.errors.ParserError as e:
        raise HTTPException(
            status_code=400, detail=f"Error parsing CSV: {str(e)}")

    # Validate CSV format
    # Check if all expected columns are present
    if not all(col in df.columns for col in EXPECTED_COLUMNS):
        raise HTTPException(
            status_code=400, detail="Missing columns in CSV file")

    # Process the DataFrame and save to InfluxDB

    for index, row in df.iterrows():

        # checl if the timestamp is in the correct format
        try:
            datetime.datetime.fromisoformat(row["timestamp"])
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid timestamp format")
        try:
            # create sensor if it does not exist
            sensor = sensors_collection.find_one(
                {"equipmentId": row["equipmentId"]})
            if not sensor:
                new_sensor = sensors_collection.insert_one(
                    {"equipmentId": row["equipmentId"]})
        except Exception as e:
            pass

        json_body = {
            "measurement": "measures",
            "tags": {
                "equipment_id": row["equipmentId"],
            },
            "fields": {
                "value": float(row["value"])
            },
            "time": row["timestamp"]
        }
        try:
            influx_write_api.write(INFLUX_BUCKET, INFLUX_ORG, json_body)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to process sensor data: {str(e)}")

    return JSONResponse(status_code=201, content={"message": "Data saved successfully"})


if __name__ == '__main__':
    print('Starting server...')
