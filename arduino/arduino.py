
from datetime import datetime
import logging
import serial
import time


PORT = "/dev/ttyUSB0"
BAUDRATE = 9600

ser = serial.Serial(port=PORT, baudrate=BAUDRATE)

logger = logging.getLogger('catch_serial_arudino')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def parse_serial(string):
    '''
    Parse a comma separated string of key:value pairs into a dict
    '''

    if ',' in string and len(string.split(',')) > 0:
        split = [tag.split(':') for tag in string.split(',')]
        return dict((t[0], int(t[1])) for t in split)
    else:
        return {'LDR': None, 'MQ3': None, 'MQ9': None}


def read_arduino(ser):
    '''
    Read the Arduino sensors through USB

    Args:
        port (str): USB port address
        baudrate (int): baudrate
    '''

    ser.flushInput()

    line_raw = ser.readline()
    line = line_raw.decode("utf-8")
    parsed = parse_serial(line)

    return parsed


if __name__ == "__main__":

    while True:

        values = read_arduino(ser)
        logger.info(str(values))
        time.sleep(2)

