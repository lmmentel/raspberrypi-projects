"""
# BME680 

- temperature
- pressure
- humidity
- gas quality

# Wiring

board | RPI              | RPI pin no
------|------------------|-----------
VIN   | 3v3 Power        |   1
GND   | Ground           |   6
SDI   | I2C1 SDA, GPIO 2 |   3
SCK   | I2C1 SCL, GPIO 3 |   5

"""

import board
import adafruit_bme680
from time import sleep
from datetime import datetime


def configure_sensor():

    i2c = board.I2C()
    return adafruit_bme680.Adafruit_BME680_I2C(i2c) # address=int(0x77)


if __name__ == "__main__":
    
    sensor = configure_sensor()
    while True:

        values = [
            sensor.temperature,
            sensor.humidity,
            sensor.pressure,
            sensor.gas,
        ]

        print(datetime.now(), " | ".join([f"{v:10.2f}" for v in values]))
        sleep(1)