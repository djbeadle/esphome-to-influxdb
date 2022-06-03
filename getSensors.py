import requests
import json
from influxdb import InfluxDBClient
from config import INFLUX_DB_CONFIG
import datetime

# INFLUX_DB = {'host':'raspberrypi.local', 'port':'8086', 'config':'database_name'}

SENSORS = [
        {
            "hostname": "danielsroom.local",
            "sensor_id": "temperature",
            "influx_db_measurement": "danielsroom",
            "influx_db_field": "celsius",
        },
        {
            "hostname": "danielsroom.local",
            "sensor_id": "temperature",
            "influx_db_measurement": "danielsroom",
            "influx_db_field": "relative_humidity_pct"
        },
        {
            "hostname": "outdoors.local",
            "sensor_id": "outdoor_temperature",
            "influx_db_measurement": "outdoors",
            "influx_db_field": "celsius",
        },
        {
            "hostname": "laundry.local",
            "sensor_id": "laundry_room_temperature",
            "influx_db_measurement": "laundryroom",
            "influx_db_field": "celsius"
        },
        {
            "hostname": "laundry.local",
            "sensor_id": "laundry_room_humidity",
            "influx_db_measurement": "laundryroom",
            "influx_db_field": "relative_humidity_pct"
        },
        {
            "hostname": "s31_two.local",
            "sensor_id": "sonoff_s31_power",
            "influx_db_measurement": "danielsroom",
            "influx_db_field": "desk_watts",
        },
        #{
        #    "hostname": "desk.local",
        #    "type": "binary_sensor",
        #    "sensor_id": "desk",
        #    "influx_db_measurement": "danielsroom",
        #    "influx_db_field": "desk_standing",
        #},
        {
            "hostname": "airgradient-two.local",
            "sensor_id": "particulate_matter_25m_concentration",
            "influx_db_measurement": "office",
            "influx_db_field": "pm_two_five"
        },
        {
           "hostname": "airgradient-two.local",
           "sensor_id": "sensor-temperature",
           "influx_db_measurement": "office",
           "influx_db_field": "celsius",
        },
        {
           "hostname": "airgradient-two.local",
           "sensor_id": "sensor-humidity",
           "influx_db_measurement": "office",
           "influx_db_field": "relative_humidity_pct",
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




