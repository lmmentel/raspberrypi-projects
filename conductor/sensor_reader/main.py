
from datetime import datetime
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBServerError
import requests
import time
import toml

import RPi.GPIO as GPIO
from Adafruit_BME280 import *


GPIO.setmode(GPIO.BOARD)
DT_MFT = 'YYYY-MM-DD HH:mm:SS'
FREQ = 30   # frequency of data collection in sec


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


def measure_ldr_resistance(pin_no, capacitance=0.000001):
    '''
    Calculate the resistance from the measured
    capacitor charging time and LDR

    Args:
        pin_no (int): pin numer
        capacitance (float): capacitance
    '''

    # output on the pin for
    GPIO.setup(pin_no, GPIO.OUT)
    GPIO.setup(pin_no, GPIO.LOW)
    time.sleep(0.1)

    # change the pin back to input
    GPIO.setup(pin_no, GPIO.IN)

    # count until pin goes to HIGH
    start = time.time()
    end = time.time()
    while (GPIO.input(pin_no) == GPIO.LOW):
        end = time.time()

    return (end - start) / capacitance


if __name__ == '__main__':

    print('started: ', datetime.now().isoformat())

    # define pin that goes to the LDR circuit
    ldr_pin_no = 7

    sensor = BME280(t_mode=BME280_OSAMPLE_8,
                    p_mode=BME280_OSAMPLE_8,
                    h_mode=BME280_OSAMPLE_8)

    idb = InfluxDBClient(host='influxdb', port=8086)

    while True:
        try:
            ts = datetime.now()
            temp, pressure, humidity = measure_tph(sensor)
            ldr_res = measure_ldr_resistance(ldr_pin_no)

            print(' | '.join([
                  ts.isoformat(),
                  '{0:0.3f} deg C'.format(temp),
                  '{0:0.2f} hPa'.format(pressure),
                  '{0:0.2f} %'.format(humidity),
                  '{0:0.2f} Ohm'.format(ldr_res)
                  ]))

            data = {
                "measurement": "PF41-livingroom",
                "time": ts.isoformat(),
                "fields": {
                    "temperature": temp,
                    "pressure": pressure,
                    "humidity": humidity,
                    "ldr": ldr_res,
                },
            }

            try:
                idb.write_points([data], database='sensors')
            except InfluxDBServerError as e:
                print('Error: {}'.format(e))

            # ping healthcheck
            requests.get(config['healthcheck']['url'])
            time.sleep(FREQ)

        except KeyboardInterrupt:
            print('bye bye...')
            break
        except:
            raise
            break

    # cleanup
    GPIO.cleanup()
    idb.close()
