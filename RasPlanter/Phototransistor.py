#!/usr/bin/env python

#must have imports in same directory
#import read ADC function
import constants
import mcp3008
import time
import RPi.GPIO as GPIO

class Phototransistor():
    def __init__(self, phototransistorPin):
        self.phototransistorPin = phototransistorPin
        #pin numbering system (relative to revision number)
        GPIO.setmode(GPIO.BCM)

        #instantiate SPI interface
        GPIO.setup(constants.SPIMOSI, GPIO.OUT)
        GPIO.setup(constants.SPIMISO, GPIO.IN)
        GPIO.setup(constants.SPICLK, GPIO.OUT)
        GPIO.setup(constants.SPICS, GPIO.OUT)
        
    #outputs 0-1023 (2^10, 10 bits) analog value from thermistor
    def getAnalog(self):
        phototransValue=mcp3008.readadc(self.phototransistorPin, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
        
        return phototransValue

    #convert analog value to rough lumens (needs tuning)
    def getLumens(self):
        lumens=abs((self.getAnalog()-180)*1.99)

        return lumens
            

