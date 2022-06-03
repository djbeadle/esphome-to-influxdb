import requests
import json
from influxdb import InfluxDBClient
from config import INFLUX_DB_CONFIG
import datetime

# INFLUX_DB = {'host':'raspberrypi.local', 'port':'8086', 'config':'database_name'}

SENSORS = [
        {
           "hostname": "airgradient-two.local",
           "sensor_id": "temperature",
           "influx_db_measurement": "office",
           "influx_db_field": "celsius",
        },
        {
           "hostname": "airgradient-two.local",
           "sensor_id": "humidity",
           "influx_db_measurement": "office",
           "influx_db_field": "relative_humidity_pct",
           "custom_parser": lambda x: x
        },
    ]

#--------------------------------------------------------
# Get sensor data
#--------------------------------------------------------
client = InfluxDBClient(**INFLUX_DB_CONFIG)
for sensor in SENSORS:
    print('.', end='')
    json_data = None
    try:
        sensor_type = sensor.get("type", "sensor")
        response = requests.request("GET", f'http://{sensor["hostname"]}/{sensor_type}/{sensor["sensor_id"]}')

        json_data = json.loads(response.text)

        if json_data.strip() == '':
            print("ERROR: The response was empty, perhaps the sensor_id is invalid.")
            if sensor['sensor_id'].startswith('sensor'):
                print('    Try removing "sensor" from the sensor_id specified in this file')

        # print("Got this data back:")
        # print(json_data)

        #--------------------------------------------------------
        # post data to influxdb
        #--------------------------------------------------------
        json_body = [
            {
                "measurement": sensor["influx_db_measurement"],
                "fields": { sensor["influx_db_field"]: float(json_data["value"])}
            }
        ]

        # print(json.dumps(json_body))
        response = client.write_points(json_body)

        # print(response)
    except Exception as e:
        print(f'EXCEPTION: {datetime.datetime.now()} - {sensor["hostname"]} - {sensor["influx_db_field"]}')
        print(f'  {e}')

        print(json.dumps(json_data, indent=4))




