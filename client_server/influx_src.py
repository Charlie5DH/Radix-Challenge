# Retrieve raw_measures from Influx
import os
import re
from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta
from typing import List
from time import time
import pandas as pd
import numpy as np

import warnings
from influxdb_client.client.warnings import MissingPivotFunction
warnings.simplefilter("ignore", MissingPivotFunction)


class InfluxSource:
    def __init__(self, url, token, org):
        self._client = InfluxDBClient(
            url=url, token=token, org=org, timeout=120_000)
        self.query_api = self._client.query_api()
        self.write_api = self._client.write_api()

    def ready(self):
        return self._client.ping()

    def query(self, sensor_ids: list, init_timestamp, end_timestamp, aggregation_window, aggregation_function: str = 'mean',
              merge_matrices=False, createEmpty: bool = False, debug=True, function=None):
        if (aggregation_window is None) or (aggregation_window == '') or (aggregation_window == 'none'):
            aggregation_window = '1s'
            query = self._gen_query_str(
                sensor_ids, init_timestamp, aggregation_window, end_timestamp, aggregation_function, createEmpty)
        else:
            query = self._gen_query_str(
                sensor_ids, init_timestamp, aggregation_window, end_timestamp, aggregation_function, createEmpty)
        if debug:
            print(f'Influx query debug:\n{query}\n\n', flush=True)
        df = self.query_api.query_data_frame(query)
        if type(df) is list:
            df = pd.concat(df).reset_index(drop=True)
        try:
            df.drop(columns=['result', 'table',
                    '_stop', '_start'], inplace=True)
        except KeyError:
            pass
        df.rename(columns={
                  col: col[1:] for col in df.columns if col.startswith('_')}, inplace=True)
        return df

    def _gen_query_str(self, sensor_ids, init_timestamp, aggregation_window, end_timestamp, aggregation_function, createEmpty):

        query_str = f'''from(bucket: "{os.environ['DOCKER_INFLUXDB_INIT_BUCKET']}")
        |> range({self._gen_range(init_timestamp, end_timestamp)})
        |> filter(fn: (r) => r["_measurement"] == "measures")
        |> filter(fn: (r) => {self._gen_filter(sensor_ids)})
        |> aggregateWindow(every: {aggregation_window}, fn: {aggregation_function}, createEmpty: {"true" if createEmpty else "false"})
        |> pivot(columnKey:["_field"], rowKey:["_time"], valueColumn:"_value")'''

        return query_str

    def _gen_range(self, init_timestamp, end_timestamp):

        if type(init_timestamp) is datetime:
            init_timestamp = init_timestamp.isoformat(' ')
        resp = f'start: {init_timestamp}'

        if end_timestamp:
            if type(end_timestamp) is datetime:
                end_timestamp = end_timestamp.isoformat(' ')
            resp += f' , stop: {end_timestamp}'
        return resp

    def _gen_filter(self, sensor_ids) -> List:
        return ' or '.join([f'r["equipment_id"] == "{sensor_id}"' for sensor_id in sensor_ids])


if __name__ == '__main__':
    print('InfluxSource')
