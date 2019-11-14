
'''
Read temperature from DS18B20 temperature sensor
'''

import os
import re
import time

from path import Path

base_path = Path('/sys/bus/w1/devices')
# device_dir = '28-020791774310'
devide_dir = '28-021192460aa7'

device_file = base_path.joinpath(device_dir, 'w1_slave')

def read_temp_sensor(device_file):
	'''
	Read the temp from file

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

if __name__ == '__main__':
	
	while True:
		
		lines = read_temp_sensor(device_file) 
		temp = parse_temp(lines)
		print(temp, 'C')
		time.sleep(0.5)


