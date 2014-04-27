#!/usr/bin/env python

import sensorFunctions
import RPi.GPIO as GPIO
import time

phototransPIN = 0;
thermistorPIN = 2;

lightRELAY = 17
fanRELAY = 21#either 21, or 27
pumpRELAY = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(lightRELAY, GPIO.OUT)
GPIO.setup(fanRELAY, GPIO.OUT)
GPIO.setup(pumpRELAY, GPIO.OUT)

while True:
    GPIO.output(fanRELAY, False)
    GPIO.output(lightRELAY, False)
    GPIO.output(pumpRELAY, False)
    #run through all three relays, test each one, rough setup
    #loop through 0.5 second delay 101 times, 30.5 seconds
    for i in range(0, 30):
        print "Reading Phototransistor"
        phototransValue = sensorFunctions.readPhototransistor(phototransPIN)
        print "Phototransistor Read: ", phototransValue
        lumens = sensorFunctions.convertToLumens(phototransValue)
        print "Analog Converted to Lumens: ", lumens
        
        if (lumens > 700):
            print "KEEP RELAYS ON, COUNT: ", i
            GPIO.output(lightRELAY, True)
            time.sleep(0.5)
        else:
            print "ERROR, TIME NOT EXPIRED, LIGHTS OFF?"
            time.sleep(0.5)

    for i in range(0, 30):
        print "Reading Thermistor"
        thermistorValue = sensorFunctions.readThermistor(thermistorPIN)
        temp_F = sensorFunctions.convertToF(thermistorValue)
        print "DEGRESS IN F: ", temp_F

        if (temp_F > 75):
            print "TURNIN ON FAN, HOTTER THAN 75F, TEMP = ", temp_F
            GPIO.output(fanRELAY, True)
            time.sleep(0.5)
        else:
            print "TEMPERATURE OK! TEMP = ", temp_F
            GPIO.output(fanRELAY, False)
            time.sleep(0.5)

    for i in range(0, 30):
        if (i < 100):
            print "WATERING"
            GPIO.output(pumpRELAY, True)
            time.sleep(0.5)
        else:
            print "DONE"
            GPIO.output(pumpRELAY, False)
            break
        
        

    print "DONE, TURNING OFF RELAYS"
    GPIO.output(lightRELAY, False)
    GPIO.output(fanRELAY, False)
    GPIO.output(pumpRELAY, False)
    time.sleep(10)
