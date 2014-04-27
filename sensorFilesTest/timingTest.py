#!/usr/bin/env python

#import sys
#sys.path.append('/home/pi/Desktop/Programs/Sensor Files/sensorFunctions.py')
import sensorFunctions
import RPi.GPIO as GPIO
import time

lightRELAY = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(lightRELAY, GPIO.OUT)

while True:

    #loop through 0.5 second delay 101 times, 30.5 seconds
    for i in range(0, 100):
        print "Reading Phototransistor"
        phototransValue = sensorFunctions.readPhototransistor(0)
        print "Phototransistor Read: ", phototransValue
        lumens = sensorFunctions.convertToLumens(phototransValue)
        print "Analog Converted to Lumens: ", lumens
        
        if (lumens > 700):
            print "KEEP RELAYS ON, COUNT: ", i
            GPIO.output(lightRELAY, True)
            time.sleep(0.5)
        else:
            print "ERROR, TIME NOT EXPIRED, RELAYS OFF?"
            print ""
            print "ABORTING OPERATION"
            break

    print "DONE, TURNING OFF RELAYS"
    GPIO.output(lightRELAY, False)
    time.sleep(10)
