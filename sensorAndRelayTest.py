#!/usr/bin/env python

#import sys
#sys.path.append('/home/pi/Desktop/Programs/Sensor Files/sensorFunctions.py')
import sensorFunctions
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

while True:
    print "Reading Phototransistor"
    phototransValue = sensorFunctions.readPhototransistor(0)
    print "Phototransistor Read: ", phototransValue
    lumens = sensorFunctions.convertToLumens(phototransValue)
    print "Analog Converted to Lumens: ", lumens

    if (lumens < 500):
        print "TURN OFF RELAY"
        GPIO.output(17, False)
        time.sleep(1.0)
    else:
        print "TURN ON RELAY"
        GPIO.output(17, True)
        time.sleep(1.0)

