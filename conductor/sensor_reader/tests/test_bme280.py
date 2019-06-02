
from datetime import datetime
import time

import RPi.GPIO as GPIO
from Adafruit_BME280 import *


GPIO.setmode(GPIO.BOARD)
DT_MFT = 'YYYY-MM-DD HH:mm:SS'
FREQ = 5   # frequency of data collection in sec



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

    # define pin that goes to the LDR circuit

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
                  '{0:0.2f} %'.format(humidity),
                  ]))

            time.sleep(FREQ)

        except KeyboardInterrupt:
            print('bye bye...')
            break
        except:
            raise
            break

    # cleanup
    GPIO.cleanup()
