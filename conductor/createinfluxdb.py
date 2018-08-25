# coding: utf-8
from influxdb import InfluxDBClient

ic = InfluxDBClient()
ic.get_list_database()
ic = InfluxDBClient()
ic.create_database('sensors')
ic.get_list_database()
