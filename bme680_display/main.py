from datetime import datetime
from time import sleep
import logging
import board

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBServerError
import adafruit_bme680
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(filename='bme680.log', level=logging.DEBUG)


def configure_bme680():
    i2c = board.I2C()
    return adafruit_bme680.Adafruit_BME680_I2C(i2c) # address=int(0x77)


def fetch_sensor_readings(sensor, sensor_name, value_names):

    return {
        ".".join([sensor_name, value_name]): getattr(sensor, value_name) for value_name in value_names
    }


def configure_display():
    i2c = board.I2C()
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    display.fill(0)
    display.show()
    return display


def update_display(display, values):

    image = Image.new("1", (display.width, display.height))
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
    draw.text((0, 0), f"T: {values['bme680.temperature']:.1f} C", font=font, fill=255)
    draw.text((55, 15), f"P: {values['bme680.pressure']:.1f} hPa ", font=font, fill=255)
    draw.text((0, 15), f"H: {values['bme680.humidity']:.1f} %", font=font, fill=255)
    draw.text((55, 0), f"G: {values['bme680.gas']:d} Ohm", font=font, fill=255)
    display.image(image)
    display.show()


if __name__ == "__main__":
    
    sensor = configure_bme680()
    display = configure_display()
    idb = InfluxDBClient(host='influxdb', port=8086)

    while True:

        values = fetch_sensor_readings(
            sensor,
            "bme680",
            ["temperature", "humidity", "pressure", "gas"]
        )

        ts = datetime.now()
        print(ts, " | ".join([f"{v:10.2f}" for v in values.values()]))
        logging.info(",".join([ts.isoformat()] + [str(v) for v in values.values()]))
        
        data = {
            "measurement": "lakkegata.office",
            "time": ts.isoformat(),
            "fields": values
        }

        try:
            idb.write_points([data], database="skeletor.sensors")
        except InfluxDBServerError as e:
            logging.error('InfluxDB Error: {}'.format(e))

        update_display(display, values)
        sleep(30)