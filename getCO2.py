import requests, json, time
from influxdb import InfluxDBClient
from config import INFLUX_DB_CONFIG

# INFLUX_DB = {'host':'raspberrypi.local', 'port':'8086', 'config':'database_name'}

SENSORS = [
        {
            "hostname": "airgradient-two.local",
            "sensor_id": "senseair_co2",
            "influx_db_measurement": "airgradient_two",
            "influx_db_field": "co2",
        },
    ]

#--------------------------------------------------------
# Get sensor data
#--------------------------------------------------------
client = InfluxDBClient(**INFLUX_DB_CONFIG)
for i in list(range(0,2)):
    print(i)
    for sensor in SENSORS:
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
            print(e)
    time.sleep(30)
