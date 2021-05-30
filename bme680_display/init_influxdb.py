from influxdb import InfluxDBClient

dbs = ["skeletor.sensors", "skeletor.device"]

ic = InfluxDBClient(host="influxdb")
existing_dbs = ic.get_list_database()

for db in dbs:
    if db not in [i["name"] for i in existing_dbs]:
        ic.create_database(db)

ic.close()