#!/usr/bin/env python

#must have imports in same directory
#import read ADC function
import constants
import mcp3008
import time
import RPi.GPIO as GPIO

class Thermistor():
    def __init__(self, thermistorPin):
        self.thermistorPin = thermistorPin
        #pin numbering system (relative to revision number)
        GPIO.setmode(GPIO.BCM)

        #instantiate SPI interface
        GPIO.setup(constants.SPIMOSI, GPIO.OUT)
        GPIO.setup(constants.SPIMISO, GPIO.IN)
        GPIO.setup(constants.SPICLK, GPIO.OUT)
        GPIO.setup(constants.SPICS, GPIO.OUT)
        
    #outputs 0-1023 (2^10, 10 bits) analog value from thermistor
    def getAnalog(self):
        thermistorValue=mcp3008.readadc(self.thermistorPin, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
        
        return thermistorValue

    #convert analog value to celsius
    def getTempC(self):
        temp_C=25+((self.getAnalog()-520)*(0.25))
    
        return temp_C

    #convert analog value to fahrenheit
    def getTempF(self):
    #    temp_C=25+((self.getAnalog()-520)*(0.25))                                                                                 ()-520)/4)
        temp_F=((self.getTempC()*9)/5)+32
    
        return temp_F

#TEST CLASS
#therm = Thermistor(2)
#print therm.getAnalog()
#print therm.getTempC()
#print therm.getTempF()
