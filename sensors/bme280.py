import logging

import board
import digitalio
import busio
import time
import adafruit_bme280

logger = logging.getLogger('bme280')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create library object using our Bus SPI port
#spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
#bme_cs = digitalio.DigitalInOut(board.D10)
#bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

def get_bme280():
    '''
    Read the temperature humidity and pressure from the BME280
    and return a dict with the values
    '''

    values = {
        'bme280.temperature': bme280.temperature,
        'bme280.humidity': bme280.humidity,
        'bme280.pressure': bme280.pressure
    }

    return values

if __name__ == '__main__':

    while True:

        tph = get_bme280()
        logger.info(str(tph))
        time.sleep(2)

