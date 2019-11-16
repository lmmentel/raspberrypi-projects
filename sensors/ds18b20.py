
'''
Read temperature from DS18B20 temperature sensor
'''

import os
import re
import sys
import time

from path import Path


def read_device_file(device_file):
    '''
    Read the temperature from file

    The file looks something like this:
    c2 01 55 05 7f 7e 81 66 0d : crc=0d YES
    c2 01 55 05 7f 7e 81 66 0d t=28125

    '''

    with open(device_file, 'r') as fo:
        lines = fo.readlines()
    return lines


def parse_temp(lines):
    '''
    Parse the temp in degrees C from the lines
    '''

    patt = re.compile(r'.*t=(\d+)$')
    match = re.match(patt, lines[-1])
    if match:
        return float(match.group(1)) / 1000.0
    else:
        return match


def get_temperature(device_dir):
    '''
    Return the temperature in C from DS18B20

    Args:
        device_dir (str): directory/id for DS18B20
    '''

    base_path = Path('/sys/bus/w1/devices')
    device_file = base_path.joinpath(device_dir, 'w1_slave')
    lines = read_device_file(device_file)
    temp = parse_temp(lines)
    return temp


if __name__ == '__main__':

    device_dir = sys.argv[1]

    while True:

        temp = get_temperature(device_dir)
        print(temp, 'C')
        time.sleep(0.5)

