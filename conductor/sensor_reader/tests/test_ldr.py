
from datetime import datetime
import requests
import time

import RPi.GPIO as GPIO


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


def test_ldr_read():

	GPIO.setmode(GPIO.BOARD)
	ldr_pin_no = 7
	ldr_res = measure_ldr_resistance(ldr_pin_no)
	print(ldr_res)

if __name__ == '__main__':

	test_ldr_read()

