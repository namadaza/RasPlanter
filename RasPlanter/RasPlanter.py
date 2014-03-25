#!/usr/bin/env python

#import Phototransistor, Thermistor, Tensiometer
from Phototransistor import Phototransistor
from Thermistor import Thermistor
from Tensiometer import Tensiometer
from Relay import Relay

import RPi.GPIO as GPIO
import time
import thread

###########################
#RASPLANTER
###########################
phototransPIN = 0;
thermistorPIN = 2;
tensiometerPIN = 4;

lightRelayPIN = 17
fanRelayPIN = 21#either 21, or 27; revision 1/2 respectivley 
pumpRelayPIN = 22
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(lightRELAY, GPIO.OUT)
#GPIO.setup(fanRELAY, GPIO.OUT)
#GPIO.setup(pumpRELAY, GPIO.OUT)

#INITIALLY SET TO FALSE
#GPIO.output(lightRELAY, False)
#GPIO.output(fanRELAY, False)
#GPIO.output(pumpRELAY, False)

rerun_test = True

#instantiate sensor classes
phototransistor = Phototransistor(phototransPIN)
thermistor = Thermistor(thermistorPIN)
tensiometer = Tensiometer(tensiometerPIN)

#instantiate relay classes
lightRelay = Relay(lightRelayPIN)
fanRelay = Relay(fanRelayPIN)
pumpRelay = Relay(pumpRelayPIN)

def RasPlanter(rerun_bool):
	#set relays to false
	lightRelay.setModeOff()
	fanRelay.setModeOff()
	pumpRelay.setModeOff()
        while (rerun_bool):
		#Ask user how long to run the test in DAYS
		time_of_test = input("Days to run the test (INT): ")
		print "Running for:", time_of_test, " days"
                
		#Ask user how long each light cycle is
		time_of_lightcycle = input("Length of each light cycle (IN HOURS): ")
		print "Light cycles set at:", time_of_lightcycle, " hours"

		#caclulate time of rest (no lights)
		time_of_rest = (24-time_of_lightcycle)
		time_of_rest_in_s = time_of_rest*60*60

		#range of 0 to 240 lasts roughly 3 minutes
		#half second delay on each relay setting change
		#for watering, roughly estimate time intervals using variable 'i'
		time_of_lightcycle_in_s = time_of_lightcycle*60*60
		for days in range(0, time_of_test):
			#simulated daytime (first half of program)
			for i in range(0, time_of_lightcycle_in_s):
				print "Light Cylce Active"
				#################
				#VALUES FOR LIGHT CONTROL
				#print "Reading Phototransistor..."
				lumens = phototransistor.getLumens()
				print "Lumens: ", lumens, " ANALOG VALUE: ", phototransistor.getAnalog()
	
				#################
				#VALUES FOR FAN CONTROL
				#print "Reading Thermistor..."
				#convert to fahrenheit and celsius
				temp_C = thermistor.getTempC()
				temp_F = thermistor.getTempF()
				print "Temperature in C: ", temp_C, " Temperature in F: ", temp_F, " ANALOG VALUE: ", thermistor.getAnalog()

				#################
				#VALUES FOR PUMP CONTROL
				#print "Reading Tensiometer..."
				humidity = tensiometer.getHumidity()
				print "RAW Tensiometer Reading: ", humidity


				################
				#RELAY CONTROL
				################
				#is greater than 700, turn on light relay
				lightRelay.regulateThreshold(700, lumens)                        

				#temperature above roughly 75F (NEEDS TUNING), turn on fan
				fanRelay.regulateThreshold(75, temp_F)
	
				#check analog values, at roughly 170 equals full conductivity/highest humidity
				pumpRelay.regulateThreshold(50, humidity)

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
			for l in range(0, time_of_rest_in_s):
				print "Night Cycle Active"
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
				#temperature above roughly 75F (NEEDS TUNING), turn on fan
				fanRelay.regulateThreshold(75, temp_F)

				#check analog values, at roughly 170 equals full conductivity/highest humidity
				pumpRelay.regulateThreshold(50, humidity)

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
		rerun_test = raw_input("Rerun test? (y/n): ")
		print "You entered: ", rerun_test.lower()
		while rerun_test.lower() not in ['y', 'yes', 'ye', 'n', 'nay', 'no']:
			print "Could not understand answer, please enter 'y' or 'n'"
			rerun_test = raw_input("Rerun test? (y/n): ")
		if rerun_test.lower() in ['y', 'yes', 'ye']:
			rerun_bool = True
			print "Rerunning test"
		elif rerun_test.lower() in ['n', 'nay', 'no']:
			rerun_bool = False
			print "Test complete"
			#set relays to false
			lightRelay.setModeOff()
			fanRelay.setModeOff()
			pumpRelay.setModeOff()
			
def print_message():
	print "Message 1!"

while True:
	try:
		thread.start_new_thread(RasPlanter, (rerun_test, ))
		thread.start_new_thread(print_message, ( ))
		time.sleep(5)
	except:
		print "err"


	
		
        
    
            

        
        
    
