from __future__ import print_function
from datetime import datetime
from time import sleep, time

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, MetaData, DateTime

import RPi.GPIO as GPIO
from Adafruit_BME280 import *

GPIO.setmode(GPIO.BOARD)
DT_MFT = 'YYYY-MM-DD HH:mm:SS'
FREQ = 60   # frequency of data collection in sec

# db (SQLite) configuration

metadata = MetaData()

sensor_data = Table('sensor_data', metadata,
			  Column('timestamp', DateTime, primary_key=True),
			  Column('temperature', Float),
			  Column('pressure', Float),
			  Column('humidity', Float),
			  Column('light_dep_resistance', Float)
			 )

DB_PATH = '/home/pi/devel/raspi-sensors/BME280/rpisensors.db'
engine = create_engine('sqlite:///{}'.format(DB_PATH),
					   echo=False)


def measure_tph(sensor):
	'''
	Measure temperature, pressure and humidity
	with BME280 sensor
	
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
	
	# define pin that goes to the LDR circuit
	ldr_pin_no = 7

	sensor = BME280(t_mode=BME280_OSAMPLE_8,
					p_mode=BME280_OSAMPLE_8,
					h_mode=BME280_OSAMPLE_8)


	try :
	
		while True:
	
			ts = datetime.now()
			temp, pressure, humidity = measure_tph(sensor)
			ldr_res = measure_ldr_resistance(ldr_pin_no)

			# save to the db
#			with engine.begin() as conn:
#				conn.execute(sensor_data.insert(),
#							 timestamp=ts,
#							 temperature=temp,
#							 pressure=pressure,
#							 humidity=humidity,
#							 light_dep_resistance=ldr_res)			
						
			print(' | '.join([
				ts.isoformat(),
				'{0:0.3f} deg C'.format(temp),
				'{0:0.2f} hPa'.format(pressure),
				'{0:0.2f} %'.format(humidity),
				'{0:0.2f} Ohm'.format(ldr_res)
			]))
			
			sleep(FREQ)
	
	except KeyboardInterrupt:
		print('bye bye...')
	except:
		raise
	finally:
		GPIO.cleanup()

