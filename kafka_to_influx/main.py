import os
import socket
import uuid
import json
from confluent_kafka import Consumer
from influxdb_client import InfluxDBClient

# Kafka producer details
consumer_conf = {'bootstrap.servers': f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
                 'group.id': uuid.uuid4(),
                 'enable.auto.commit': True,
                 'auto.offset.reset': 'latest'}
KAFKA_TOPIC = os.environ['KAFKA_INFLUXDB_TOPIC']
# InfluxDB configuration
INFLUX_URL = f"http://{os.environ['DOCKER_INFLUXDB_INIT_HOST']
                       }:{os.environ['DOCKER_INFLUXDB_INIT_PORT']}"
INFLUX_TOKEN = os.environ['DOCKER_INFLUX_TOKEN']
INFLUX_ORG = os.environ['DOCKER_INFLUXDB_INIT_ORG']
INFLUX_BUCKET = os.environ['DOCKER_INFLUXDB_INIT_BUCKET']

influx_client = InfluxDBClient(
    url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
influx_write_api = influx_client.write_api()

consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

running = True
while running:
    try:
        measures = consumer.consume(1, timeout=1)
        for measure in measures:
            if measure.error():
                print('Message error!')
                continue
            else:
                measure = json.loads(measure.value().decode())
                print(measure, flush=True)
                # send to InfluxDB
                try:
                    json_body = {
                        "measurement": "measures",
                        "tags": {
                            "equipment_id": measure["equipmentId"],
                        },
                        "fields": {
                            "value": measure["value"]
                        },
                        "time": measure["timestamp"]
                    }

                    influx_write_api.write(
                        INFLUX_BUCKET, INFLUX_ORG, json_body)
                except Exception as e:
                    print(f'Failed to process sensor data: {str(e)}')

    except KeyboardInterrupt:
        running = False

    except Exception as e:
        measure['error'] = repr(e)
        producer.produce("errors",
                         json.dumps(measure, default=str))
        producer.poll(0)
        producer.flush()
