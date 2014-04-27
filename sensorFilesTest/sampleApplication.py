#!/usr/bin/env python

import sensorFunctions
import RPi.GPIO as GPIO
import time

phototransPIN = 0;
thermistorPIN = 2;

lightRELAY = 17
fanRELAY = 21#either 21, or 27; revision 1/2 respectivley 
pumpRELAY = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(lightRELAY, GPIO.OUT)
GPIO.setup(fanRELAY, GPIO.OUT)
GPIO.setup(pumpRELAY, GPIO.OUT)

#INITIALLY SET TO FALSE
GPIO.output(lightRELAY, False)
GPIO.output(fanRELAY, False)
GPIO.output(pumpRELAY, False)

#range of 0 to 240 lasts roughly 3 minutes
#half second delay on each relay setting change
#for watering, roughly estimate time intervals using variable 'i'
for i in range(0, 240):
    #################
    #VALUES FOR LIGHT CONTROL
    print "Reading Phototransistor..."
    phototransValue = sensorFunctions.readPhototransistor(phototransPIN)
    #convert to lumens
    lumens = sensorFunctions.convertToLumens(phototransValue)
    print "Lumens: ", lumens
    print ""
    print ""

    #################
    #VALUES FOR FAN CONTROL
    print "Reading Thermistor..."
    thermistorValue = sensorFunctions.readThermistor(thermistorPIN)
    #convert to fahrenheit and celsius
    temp_C = sensorFunctions.convertToC(thermistorValue)
    temp_F = sensorFunctions.convertToF(thermistorValue)
    print"Temperature in C: ", temp_C, " Temperature in F: ", temp_F
    print ""
    print ""

    #lumens is greater than 700, turn on light relay
    if (lumens < 700):
        print "##################"
        print "ERROR"
        print "NOT ENOUGH LIGHT, TURNING ON LIGHTS"
        print "##################"
        GPIO.output(lightRELAY, True)
    elif (lumens >700):
        GPIO.output(lightRELAY, False)

    #temperature above roughly 75F (NEEDS TUNING), turn on fan
    if (temp_F > 80):
        print "##################"
        print "ERROR"
        print "TEMPERATURE HOTTER THAN 75F, TURNING ON FAN"
        print "##################"
        GPIO.output(fanRELAY, True)
    elif (temp_F < 79):
        GPIO.output(fanRELAY, False)

    #at 10 seconds, water for 5 seconds (i==30)
    if (i == 20):
        print "##################"
        print "TIME TO WATER, TURNING ON PUMP"
        print "##################"
        GPIO.output(pumpRELAY, True)
    if (i ==30):
        print "##################"
        print "5 SECONDS ELAPSED, TURNING OFF  PUMP"
        print "##################"
        GPIO.output(pumpRELAY, False)

    #delay for timekeeping
    time.sleep(0.5)
        

        
        
    
