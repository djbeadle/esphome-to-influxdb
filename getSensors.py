import requests
import json
from influxdb import InfluxDBClient
from config import INFLUX_DB_CONFIG
import datetime

# INFLUX_DB = {'host':'raspberrypi.local', 'port':'8086', 'config':'database_name'}

"""{
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
},"""
"""{
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
},"""
SENSORS = [
        #{
        #    "hostname": "outdoors.local",
        #    "sensor_id": "outdoor_temperature",
        #    "influx_db_measurement": "outdoors",
        #    "influx_db_field": "celsius",
        #},
        {
            "hostname": "s31_two",
            "sensor_id": "sonoff_s31_power",
            "influx_db_measurement": "danielsroom",
            "influx_db_field": "desk_watts",
        },
        {
            "hostname": "s31_one",
            "sensor_id": "sonoff_s31_relay",
            "influx_db_measurement": "livingroom",
            "influx_db_field": "filter_state",
            "type": "switch"
        },
        {
            "hostname": "s31_one",
            "sensor_id": "sonoff_s31_power",
            "influx_db_measurement": "livingroom",
            "influx_db_field": "filter_watts_2",
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
           "sensor_id": "temperature",
           "influx_db_measurement": "office",
           "influx_db_field": "celsius",
        },
        {
           "hostname": "airgradient-two.local",
           "sensor_id": "humidity",
           "influx_db_measurement": "office",
           "influx_db_field": "relative_humidity_pct",
        },
        {
            "hostname": "apt_tvoc.local",
            "sensor_id": "tvoc",
            "influx_db_measurement": "danielsroom",
            "influx_db_field": "tvoc",
        },
        {
            "hostname": "livingroom_tvoc.local",
            "sensor_id": "tvoc",
            "influx_db_measurement": "livingroom",
            "influx_db_field": "tvoc",
        },
        {
            "hostname": "adafruit_sensor.local",
            "sensor_id": "adafruitvoc",
            "influx_db_measurement": "adafruit",
            "influx_db_field": "voc",
        },
        {
            "hostname": "adafruit_sensor.local",
            "sensor_id": "bme688temperature",
            "influx_db_measurement": "adafruit",
            "influx_db_field": "celsius",
        },
        {
            "hostname": "adafruit_sensor.local",
            "sensor_id": "bme688pressure",
            "influx_db_measurement": "adafruit",
            "influx_db_field": "pressure hPa",
        },
        {
            "hostname": "adafruit_sensor.local",
            "sensor_id": "bme688humidity",
            "influx_db_measurement": "adafruit",
            "influx_db_field": "relative humidity",
        },
        {
            "hostname": "adafruit_sensor.local",
            "sensor_id": "bme688gasresistance",
            "influx_db_measurement": "adafruit",
            "influx_db_field": "gas resistance ohms",
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

        if type(json_data) is not dict and json_data.strip() == '':
            print("ERROR: The response was empty, perhaps the sensor_id is invalid.")
            if sensor['sensor_id'].startswith('sensor'):
                print('    Try removing "sensor" from the sensor_id specified in this file')

        print("Got this data back:")
        print(json_data)

        if type(json_data["value"]) is bool:
            value = json_data["value"]
        else:
            value = float(json_data["value"])

        #--------------------------------------------------------
        # post data to influxdb
        #--------------------------------------------------------
        json_body = [
            {
                "measurement": sensor["influx_db_measurement"],
                "fields": { sensor["influx_db_field"]: value } 
            }
        ]

        # print(json.dumps(json_body))
        response = client.write_points(json_body)

        # print(response)
    except Exception as e:
        print(f'EXCEPTION: {datetime.datetime.now()} - {sensor["hostname"]} - {sensor["influx_db_field"]}')
        print(f'  {e}')

        print(json.dumps(json_data, indent=4))
        print("---")


