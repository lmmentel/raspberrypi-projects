
# sensor: HC-SR04

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# set the GPIO pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# set GPIO direction(IN/OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
	'get the distance reading'
	
	# set the TIRGGER to HIGH
	GPIO.output(GPIO_TRIGGER, True)
	
	# set TRIGGER after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	
	StartTime = time.time()
	StopTime = time.time()
	
	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
		
	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()
	
	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	return (TimeElapsed * 34300.0 ) / 2.0
	
if __name__ == "__main__":

	try:
		while True:
			dist = distance()
			print("Measured distance: {0:.1f} cm".format(dist))
			time.sleep(1)
	except KeyboardInterrupt:
		print("Measurement stopped")
	except:
		print("Unexpected error:")
		raise
	finally:
		GPIO.cleanup()
