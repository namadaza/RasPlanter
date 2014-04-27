#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

while True:
    GPIO.output(11, False)
    time.sleep(4.0)

    GPIO.output(11, True)
    time.sleep(4.0)