#!/usr/bin/env python

import Phototransistor, Thermistor, Tensiometer, Relay
import RPi.GPIO as GPIO
import time

###########################
#RASPLANTER
###########################
phototransPIN = 0;
thermistorPIN = 2;
tensiometerPIN = 4;

lightRELAY = 17
#either 21, or 27; revision 1/2 respectivley
fanRELAY = 21
pumpRELAY = 22

rerun_bool = True

phototransistor = new Phototransistor(phototransPIN)
thermistor = new Thermistor(thermistorPIN)
tensiometer = new Tensiometer(tensiometerPIN)

phototransRelay = new Relay(phototransPIN)
thermistorRelay = new Relay(thermistorPIN)
tensiometerRelay = new Relay(tensiometerPIN)


while True:
    while (rerun_bool):
        #Ask user how long to run the test in DAYS
        time_of_test = input("Days to run the test (INT): ")

        #Ask user how long each light cycle is
        time_of_lightcycle = input("Length of each light cycle (IN HOURS): ")
        desired_temperature = input("Desired temperature to be maintained (F): ")
        desired_humidity = input("Desired humidity of soil (0-1024): ")

        #caclulate time of rest (no lights)
        time_of_rest = (24-time_of_lightcycle)
        time_of_rest_in_s = time_of_rest*60*60

        #range of 0 to 240 lasts roughly 3 minutes
        #half second delay on each relay setting change
        #for watering, roughly estimate time intervals using variable 'i'
        time_of_lightcycle_in_s = time_of_lightcycle*60*60

        #cycle through number of days defined
        for days in range(1, time_of_test):
            #simulated daytime (first half of program)
            for i in range(0, time_of_lightcycle_in_s):
                #################
                #VALUES FOR LIGHT CONTROL
                #print "Reading Phototransistor..."
                lumens = phototransistor.getLumens()
                print "Lumens: ", lumens, " ANALOG VALUE: ", phototransValue
                print "Maintaining for: ", (time_of_lightcycle-(i/3600)), " hours"

                #################
                #VALUES FOR FAN CONTROL
                #print "Reading Thermistor..."
                temp_C = thermistor.getTempC()
                temp_F = thermistor.getTempF()
                print "Temperature in C: ", temp_C, " Temperature in F: ", temp_F, " ANALOG VALUE: ", thermistorValue
                print "Maintaing @: ", desired_temperature, " Degrees F"

                #################
                #VALUES FOR PUMP CONTROL
                #print "Reading Tensiometer..."
                humidity = tensiometer.getHumidity()
                print "RAW Tensiometer Reading: ", humidity
                print "Maintaing @: ", desired_humidity, " humidity"


                ################
                #RELAY CONTROL
                ################
                #is greater than 700, turn on light relay
                phototransRelay.regulateThreshold(700, lumens)

                #temperature above roughly 75F (NEEDS TUNING), turn on fan
                thermistorRelay.regulateThreshold(75, temp_F)

                #check analog values, at roughly 170 equals full conductivity/highest humidity
                tensiometerRelay.regulateThreshold(300, humidity)

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
                
            #simulated night time, lights shutoff, humidity and temp still on
            for i in range(0, time_of_rest_in_s):
                #################
                #VALUES FOR FAN CONTROL
                #print "Reading Thermistor..."
                temp_C = thermistor.getTempC()
                temp_F = thermistor.getTempF()
                print"Temperature in C: ", temp_C, " Temperature in F: ", temp_F, " ANALOG VALUE: ", thermistorValue

                #################
                #VALUES FOR PUMP CONTROL
                #print "Reading Tensiometer..."
                humidity = tensiometer.getHumidity()
                print "RAW Tensiometer Reading: ", humidity


                ################
                #RELAY CONTROL
                ################
                #temperature above roughly 75F (NEEDS TUNING), turn on fan
                thermistorRelay.regulateThreshold(75, temp_F)

                #check analog values, at roughly 170 equals full conductivity/highest humidity
                tensiometerRelay.regulateThreshold(300, humidity)

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
                
        rerun_test = input("Rerun test? (y/n): ")
        while (rerun_test!="y" or "n"):
            print "Could not understand answer, enter only 'y' or 'n'"
            rerun_test = input("Rerun test? (y/n): ")
        if (rerun_test=="n"):
            rerun_bool = True
        elif (rerun_test=="n"):
            rerun_bool = False
        
        
    
            

        
        
    
