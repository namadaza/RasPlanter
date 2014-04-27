#!/usr/bin/env python

##################
#FUNCTIONS FOR PHOTOTRANSISTOR
#ANALOG VALUE, CONVERTED VALUE, PRINT VALUE FUNCTIONS#
##################

#must have imports in same directory
#import read ADC function
import constants
import mcp3008
import time
import RPi.GPIO as GPIO

#pin numbering system (relative to revision number)
GPIO.setmode(GPIO.BCM)

#instantiate SPI interface
GPIO.setup(constants.SPIMOSI, GPIO.OUT)
GPIO.setup(constants.SPIMISO, GPIO.IN)
GPIO.setup(constants.SPICLK, GPIO.OUT)
GPIO.setup(constants.SPICS, GPIO.OUT)

#outputs 0-1023 (2^10, 10 bits) analog value from phototransistor
def readPhototransistor(phototransPIN):
    phototransValue=mcp3008.readadc(phototransPIN, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
    return phototransValue

#convert analog value to rough lumens (needs tuning)
def convertToLumens(phototransValue):
    lumens=abs((phototransValue-180)*1.99)
        


