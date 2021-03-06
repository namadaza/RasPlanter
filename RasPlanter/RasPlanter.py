#!/usr/bin/env python

#import Phototransistor, Thermistor, Tensiometer
from Phototransistor import Phototransistor
from Thermistor import Thermistor
from Tensiometer import Tensiometer
from Relay import Relay
from ServerCommand import ServerCommand

import RPi.GPIO as GPIO
import time
import thread

#imports for websocket handling
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

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


#instantiate sensor classes
phototransistor = Phototransistor(phototransPIN)
thermistor = Thermistor(thermistorPIN)
tensiometer = Tensiometer(tensiometerPIN)

#instantiate relay classes
lightRelay = Relay(lightRelayPIN)
fanRelay = Relay(fanRelayPIN)
pumpRelay = Relay(pumpRelayPIN)

#variables for test parameters
rerun_test = 0
setDays = 0
setLightcycle = 0
setLumens = 0
setTemperature = 0
setHumidity = 0
isTestFinished = True

#class handles websocket events
class WSHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print 'New connection was opened'

	def on_message(self, data):
		#print 'Incoming data...', data
		server_command = ServerCommand(data)
		global setDays
		global setLightcycle
		global setLumens
		global setTemperature
		global setHumidity
		global rerun_test
		global isTestFinished
		
		#print "server command type: ", server_command.command_type
		#print "server command data: ", server_command.command_data
		
		#DAYS
		if (server_command.command_type=="setDays"):
			setDays = int(server_command.command_data)
			#print "setdays"
		elif (server_command.command_type=="getDays"):
			time_of_testSTR = (str(time_of_test))
			self.write_message(str("returnedDays::"+time_of_testSTR))
			
		#LIGHTCYCLE
		elif (server_command.command_type=="setLightcycle"):
			setLightcycle = int(server_command.command_data)
			#print "lightcycle"
		elif (server_command.command_type=="getLightcycle"):
			time_of_lightcycleSTR = (str(time_of_lightcycle))
			self.write_message(str("returnedLightcycle::"+time_of_lightcycleSTR))
			
		#LUMENS
		elif (server_command.command_type=="setLumens"):
			setLumens = int(server_command.command_data)
			#print "lumens"
		elif (server_command.command_type=="getLumens"):
			lumensSTR = (str(lumens))
			self.write_message(str("returnedLumens::"+lumensSTR))
		
		#TEMPERATURE
		elif (server_command.command_type=="setTemperature"):
			setTemperature = int(server_command.command_data)
			#print "temp"
		elif (server_command.command_type=="getTemp"):
			temp_FSTR = (str(temp_F))
			self.write_message(str("returnedTemp::"+temp_FSTR))
		
		#HUMIDITY
		elif (server_command.command_type=="setHumidity"):
			setHumidity = int(server_command.command_data)
			#print "humidity"
		elif (server_command.command_type=="getHumidity"):
			humiditySTR = (str(humidity))
			self.write_message(str("returnedHumidity::"+humiditySTR))
		
		#START/STOP TEST
		elif (server_command.command_type=="startTest"):
			rerun_test = 1
		elif (server_command.command_type=="stopTest"):
			rerun_test = 0
			
		#IS TEST RUNNING
		elif (server_command.command_type=="isTestOn"):
			#print "ISTEST FINISHED:", isTestFinished
			#print "++++++++++++++++++++++++++++++++++"
			if (isTestFinished==False):
				self.write_message(str("testOn::1"))
				#print "sending back TEST ON"
			else:
				self.write_message(str("testOn::0"))
				#print "sending back TEST OFF"
			
		#END TEST
		#put code
			
	def on_close(self):
		print 'Connection was closed...'
 
application = tornado.web.Application([
  (r'/ws', WSHandler),
])

def RasPlanter():
	#set variables to global, so other functions can have access
	global time_of_test
	global time_of_lightcycle
	global lumens
	global temp_F
	global humidity
	global isTestFinished
	
	#set relays to false
	lightRelay.setModeOff()
	fanRelay.setModeOff()
	pumpRelay.setModeOff()
	while (True):
		print "RasPlanter standing by...."
		time.sleep(1.5)
		while (rerun_test):
			isTestFinished = False
			#Ask user how long to run the test in DAYS
			#time_of_test = input("Days to run the test (INT): ")
			time_of_test = setDays
			print "Running for:", time_of_test, " days"
			
			#Ask user how long each light cycle is
			#time_of_lightcycle = input("Length of each light cycle (IN HOURS): ")
			time_of_lightcycle = setLightcycle
			print "Light cycles set at:", time_of_lightcycle, " hours"

			#caclulate time of rest (no lights)
			time_of_rest = (24-time_of_lightcycle)
			time_of_rest_in_s = time_of_rest*60*60

			#range of 0 to 240 lasts roughly 3 minutes
			#half second delay on each relay setting change
			#for watering, roughly estimate time intervals using variable 'i'
			time_of_lightcycle_in_s = time_of_lightcycle*60*60
			for days in range(0, time_of_test):
				if (not rerun_test):
					break
				#simulated daytime (first half of program)
				for i in range(0, time_of_lightcycle_in_s):
					isTestFinished = False
					if(not rerun_test):
						print "rerun_test: ", rerun_test
						break
					print "rerun_test: ", rerun_test
					print "Light Cylce Active"
					#################
					#VALUES FOR LIGHT CONTROL
					#print "Reading Phototransistor..."
					lumens = phototransistor.getLumens()
					print "Lumens: ", lumens, " ANALOG VALUE: ", phototransistor.getAnalog()
					print "Holding at: ", setLumens, " lumens"
					
					#################
					#VALUES FOR FAN CONTROL
					#print "Reading Thermistor..."
					#convert to fahrenheit and celsius
					temp_C = thermistor.getTempC()
					temp_F = thermistor.getTempF()
					print "Temperature in C: ", temp_C, " Temperature in F: ", temp_F, " ANALOG VALUE: ", thermistor.getAnalog()
					print "Holding at: ", setTemperature, " degrees F"
					
					#################
					#VALUES FOR PUMP CONTROL
					#print "Reading Tensiometer..."
					humidity = tensiometer.getHumidity()
					print "RAW Tensiometer Reading: ", humidity
					print "Holding at: ", setHumidity, " humidity"


					################
					#RELAY CONTROL
					################
					#is greater than 700, turn on light relay
					lightRelay.regulateThreshold(setLumens, lumens)                        
					if (lumens<setLumens):
						lightRelay.setModeOn()
					
					#temperature above roughly 75F (NEEDS TUNING), turn on fan
					if (setTemperature<temp_F):
						fanRelay.setModeOn()
					else:
						fanRelay.setModeOff()
		
					#check analog values, at roughly 170 equals full conductivity/highest humidity
					pumpRelay.regulateThreshold(setHumidity, humidity)

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
				lightRelay.setModeOff()
				for l in range(0, time_of_rest_in_s):
					isTestFinished = False
					if(not rerun_test):
						break
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
					if (setTemperature<temp_F):
						fanRelay.setModeOn()
					else:
						fanRelay.setModeOff()

					#check analog values, at roughly 170 equals full conductivity/highest humidity
					pumpRelay.regulateThreshold(setHumidity, humidity)

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
			lightRelay.setModeOff()
			fanRelay.setModeOff()
			pumpRelay.setModeOff()
			print "Test Complete...Please Reset Variables or Shutoff RasPlanter"
			isTestFinished = True
			time.sleep(5)
		#time.sleep(5)

try:
	print "err?1"
	thread.start_new_thread(RasPlanter, ( ))
	print "err @ RasPlanter?"
	while (True):
		#server_read_socket()
		print "err @ starting server?"
		http_server = tornado.httpserver.HTTPServer(application)
		print "err @ listening 8080?"
		http_server.listen(8000)
		print "err @ starting loops?"
		tornado.ioloop.IOLoop.instance().start()
	#delay sets times inbetween running of threads
except:
	print "err"


	
		
        
    
            

        
        
    
