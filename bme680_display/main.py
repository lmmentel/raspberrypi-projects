
import logging
import board
import adafruit_bme680
from time import sleep
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


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
    draw.text((0, 0), f"T: {values['temperature']:.1f} C", font=font, fill=255)
    draw.text((55, 15), f"P: {values['pressure']:.1f} hPa ", font=font, fill=255)
    draw.text((0, 15), f"H: {values['humidity']:.1f} %", font=font, fill=255)
    draw.text((55, 0), f"G: {values['gas']:d} Ohm", font=font, fill=255)
    display.image(image)
    display.show()


if __name__ == "__main__":
    
    sensor = configure_bme680()
    display = configure_display()

    while True:

        values = fetch_sensor_readings(
            sensor,
            "bme680",
            ["temperature", "humidity", "pressure", "gas"]
        )

        print(datetime.now(), " | ".join([f"{v:10.2f}" for v in values.values()]))
        logging.info(",".join([datetime.now().isoformat()] + [str(v) for v in values.values()]))
        
        update_display(display, values)

        sleep(30)