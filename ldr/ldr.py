
from __future__ import print_function
from datetime import datetime
from time import sleep, time

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
DT_MFT = 'YYYY-MM-DD HH:mm:SS'
FREQ = 60   # frequency of data collection in sec


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
    sleep(0.1)

    # change the pin back to input
    GPIO.setup(pin_no, GPIO.IN)

    # count until pin goes to HIGH
    start = time()
    end = time()
    while (GPIO.input(pin_no) == GPIO.LOW):
        end = time()

    return (end - start) / capacitance


if __name__ == '__main__':

    # define pin that goes to the LDR circuit
    ldr_pin_no = 7

    while True:
        try:
            ts = datetime.now()
            ldr_res = measure_ldr_resistance(ldr_pin_no)

            print(' | '.join([
                  ts.isoformat(),
                  '{0:0.2f} Ohm'.format(ldr_res)
                  ]))

            sleep(FREQ)

        except KeyboardInterrupt:
            print('bye bye...')
            break
        except:
            raise
            break

    # cleanup
    GPIO.cleanup()
