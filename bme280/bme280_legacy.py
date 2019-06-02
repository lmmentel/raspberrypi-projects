from __future__ import print_function
from datetime import datetime
from time import sleep, time

import RPi.GPIO as GPIO
from Adafruit_BME280 import *


GPIO.setmode(GPIO.BOARD)
DT_MFT = 'YYYY-MM-DD HH:mm:SS'
FREQ = 60   # frequency of data collection in sec


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

    sensor = BME280(t_mode=BME280_OSAMPLE_8,
                    p_mode=BME280_OSAMPLE_8,
                    h_mode=BME280_OSAMPLE_8)

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

            sleep(FREQ)

        except KeyboardInterrupt:
            print('bye bye...')
            break
        except:
            raise
            break

    # cleanup
    GPIO.cleanup()
