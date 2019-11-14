
from datetime import datetime
import csv
import logging
import serial


ARDUINO_PORT = "/dev/ttyUSB0"
BAUDRATE = 9600

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
        return dict()

def main():

    ser = serial.Serial(port=ARDUINO_PORT, baudrate=BAUDRATE)
    ser.flushInput()


    with open('arduino_data.csv', 'w') as fo:
        writer = csv.DictWriter(fo, fieldnames=['DT', 'LDR', 'MQ3', 'MQ9'], delimiter=',')
        writer.writeheader()

    while True:
        try:
            line_raw = ser.readline()
            line = line_raw.decode("utf-8")
            parsed = parse_serial(line)
            logger.info(str(parsed))
            with open('arduino_data.csv', 'a') as fo:
                writer = csv.DictWriter(fo, fieldnames=['DT', 'LDR', 'MQ3', 'MQ9'], delimiter=',')
                writer.writerow({'DT': datetime.now(), **parsed})
        except KeyboardInterrupt:
            print("see you")
            break


if __name__ == "__main__":
    main()
