#!/bin/bash

docker run -p 8086:8086 -p 8083:8083 \
    -v $PWD/influxdb:/var/lib/influxdb \
    -v $PWD/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
    influxdb -config /etc/influxdb/influxdb.conf


# docker run -p 8086:8086 \
#       -v $PWD/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
#       influxdb -config /etc/influxdb/influxdb.conf