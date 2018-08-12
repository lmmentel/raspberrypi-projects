
from datetime import datetime
from time import sleep
from influxdb import InfluxDBClient
import requests
import toml

import RPi.GPIO as GPIO
from Adafruit_BME280 import *


GPIO.setmode(GPIO.BOARD)
DT_MFT = 'YYYY-MM-DD HH:mm:SS'
FREQ = 5   # frequency of data collection in sec


# load config
with open('config.toml', 'r') as fo:
    config = toml.load(fo)


def measure_tph(sensor):
    '''
    Measure temperature, pressure and humidity with BME280 sensor

    Args:
        sensor

    Returns:
        tuple:
            - temperature in degrees C
            - pressure in kPa
            - realtive humidity in %
    '''

    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    pressure = pascals / 100
    humidity = sensor.read_humidity()

    return degrees, pressure, humidity


if __name__ == '__main__':

    print('started: ', datetime.now().isoformat())


    sensor = BME280(t_mode=BME280_OSAMPLE_8,
                    p_mode=BME280_OSAMPLE_8,
                    h_mode=BME280_OSAMPLE_8)

    idb = InfluxDBClient()

    while True:
        try:
            ts = datetime.now()
            temp, pressure, humidity = measure_tph(sensor)

            print(' | '.join([
                  ts.isoformat(),
                  '{0:0.3f} deg C'.format(temp),
                  '{0:0.2f} hPa'.format(pressure),
                  '{0:0.2f} %'.format(humidity)
                  ]))

            data = {
                "measurement": "PF41-livingroom",
                "time": ts.isoformat(),
                "fields": {
                    "temperature": temp,
                    "pressure": pressure,
                    "humidity": humidity,
                },
            }

            idb.write_points([data], database='sensors')

            # ping healthcheck
            requests.get(config['healthcheck']['url'])
            sleep(FREQ)

        except KeyboardInterrupt:
            print('bye bye...')
            break
        except:
            raise
            break

    # cleanup
    GPIO.cleanup()
    idb.close()
