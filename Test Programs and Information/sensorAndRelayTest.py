#!/usr/bin/env python

#import sys
#sys.path.append('/home/pi/Desktop/Programs/Sensor Files/sensorFunctions.py')
#import sensorFunctions
import RPi.GPIO as GPIO
import time
import sensorFunctions

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.IN)
GPIO.output(21, GPIO.LOW)

def reading(sensor):

    if sensor == 0:
        #required delay
        time.sleep(0.9)

        #need to pulse ultrasonic sensor
        #datasheet says to pulse @ 10 microseconds
        GPIO.output(21, True)
        time.sleep(0.00001)

        #end pulse
        GPIO.output(21, False)
        
        #echo pins listens for
        #signal recieved, keep track of time
        #signal not recieved and signal recieved
        #0 vs 1
        while GPIO.input(22) == 0:
            signaloff = time.time()

        while GPIO.input(22) == 1:
            signalon = time.time()
        
        timepassed = signalon - signaloff

        distance = timepassed * 17000

        return distance

        GPIO.cleanup()
    else:
        print "NOTHING TO SEE HERE"

#while True:
#    print reading(0)





while True:
    print "Reading Phototransistor"
    phototransValue = sensorFunctions.readPhototransistor(5)
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

