#!/usr/bin/env python

#must have imports in same directory
#import read ADC function
import constants
import mcp3008
import time
import RPi.GPIO as GPIO

class Tensiometer():
    def __init__(self, tensiometerPin):
        self.tensiometerPin = tensiometerPin
        #pin numbering system (relative to revision number)
        GPIO.setmode(GPIO.BCM)

        #instantiate SPI interface
        GPIO.setup(constants.SPIMOSI, GPIO.OUT)
        GPIO.setup(constants.SPIMISO, GPIO.IN)
        GPIO.setup(constants.SPICLK, GPIO.OUT)
        GPIO.setup(constants.SPICS, GPIO.OUT)
        
    #outputs 0-1023 (2^10, 10 bits) analog value from thermistor
    def getHumidity(self):
        humidity=mcp3008.readadc(self.tensiometerPin, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
        
        return humidity
            

