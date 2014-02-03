#!/usr/bin/env python

import Phototransistor, Thermistor, Tensiometer
import RPi.GPIO as GPIO
import time

###########################
#12 HOUR APPLICATION
###########################
phototransPIN = 0;
thermistorPIN = 2;
tensiometerPIN = 4;

lightRELAY = 17
fanRELAY = 21#either 21, or 27; revision 1/2 respectivley 
pumpRELAY = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(lightRELAY, GPIO.OUT)
GPIO.setup(fanRELAY, GPIO.OUT)
GPIO.setup(pumpRELAY, GPIO.OUT)

def twelveHourApplication(timeInHours):
    #INITIALLY SET TO FALSE
    GPIO.output(lightRELAY, False)
    GPIO.output(fanRELAY, False)
    GPIO.output(pumpRELAY, False)


    #range of 0 to 240 lasts roughly 3 minutes
    #half second delay on each relay setting change
    #for watering, roughly estimate time intervals using variable 'i'
    timeInSeconds = timeInHours*3600
    for i in range(0, timeInSeconds):
        #################
        #VALUES FOR LIGHT CONTROL
        #print "Reading Phototransistor..."
        phototransValue = sensorFunctions.readPhototransistor(phototransPIN)
        #convert to lumens
        lumens = sensorFunctions.convertToLumens(phototransValue)
        print "Lumens: ", lumens, " ANALOG VALUE: ", phototransValue

        #################
        #VALUES FOR FAN CONTROL
        #print "Reading Thermistor..."
        thermistorValue = thermistorFunctions.readThermistor(thermistorPIN)
        #convert to fahrenheit and celsius
        temp_C = thermistorFunctions.convertToC(thermistorValue)
        temp_F = thermistorFunctions.convertToF(thermistorValue)
        print"Temperature in C: ", temp_C, " Temperature in F: ", temp_F, " ANALOG VALUE: ", thermistorValue

        #################
        #VALUES FOR PUMP CONTROL
        #print "Reading Tensiometer..."
        humidity = sensorFunctions.readTensiometer(tensiometerPIN)
        print "RAW Tensiometer Reading: ", humidity


        ################
        #RELAY CONTROL
        ################
        #is greater than 700, turn on light relay
        if (lumens < 700):
            print "##################"
            print "ERROR 1"
            print "NOT ENOUGH LIGHT, TURNING ON LIGHTS"
            print "##################"
            GPIO.output(lightRELAY, True)
        elif (lumens >700):
            GPIO.output(lightRELAY, False)

        #temperature above roughly 75F (NEEDS TUNING), turn on fan
        if (temp_F > 75):
            print "##################"
            print "ERROR 2"
            print "TEMPERATURE HOTTER THAN 75F, TURNING ON FAN"
            print "##################"
            GPIO.output(fanRELAY, True)
        elif (temp_F < 72):
            GPIO.output(fanRELAY, False)

        #check analog values, at roughly 170 equals full conductivity/highest humidity
        if (humidity < 50):
            print "#################"
            print "ERROR 3"
            print "SOIL IS DRY, ACTIVATING WATER PUMP"
            print "#################"
            GPIO.output(pumpRELAY, True)
        elif (humidity > 50):
            GPIO.output(pumpRELAY, False)

        #time keeping variables
        timeElapsedHour = i/3600
        timeElapsedMin = i/60
        timeElapsedSec = i

        #formatting for time
        if (timeElapsedSec>=60):
            timeElapsedSec= timeElapsedSec - (timeElapsedMin*60)
        if (timeElapsedMin>=60):
            timeElapsedMin= timeElapsedMin - (timeElapsedHour*60)
            
        #delay for timekeeping, line breaks for formatting on terminal
        print "Time Elapsed : ", timeElapsedHour, ":", timeElapsedMin,":", timeElapsedSec
        print ""
        print ""
        time.sleep(1.0)

def timeKeeper(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print threadName, time.ctime(time.time())

try:
    thread.start_new_thread(timeKeeper, ("Thread1", 2))
    thrad.start_new_thread(twelveHourApplication, (43200))
except:
    print "ERROR: Unable to start threds"

while 1:
    pass

        
        
    
