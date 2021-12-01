import requests
import json
from influxdb import InfluxDBClient
from config import INFLUX_DB_CONFIG

# INFLUX_DB = {'host':'raspberrypi.local', 'port':'8086', 'config':'database_name'}

SENSORS = [
        {
            "hostname": "outdoors.local",
            "sensor_id": "outdoor_temperature",
            "influx_db_measurement": "outdoors",
            "influx_db_field": "celsius",
        }
    ]

#--------------------------------------------------------
# Get sensor data
#--------------------------------------------------------
for sensor in SENSORS:
    response = requests.request("GET", f'http://{sensor["hostname"]}/sensor/{sensor["sensor_id"]}')
    json_data = json.loads(response.text)

    print("Got this data back:")
    print(json_data)

    #--------------------------------------------------------
    # post data to influxdb
    #--------------------------------------------------------
    json_body = [
        {
            "measurement": sensor["influx_db_measurement"],
            "fields": { sensor["influx_db_field"]: json_data["value"] }
        }
    ]

print(json.dumps(json_body))
client = InfluxDBClient(**INFLUX_DB_CONFIG)
response = client.write_points(json_body)

print(response)




