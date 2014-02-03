#!/usr/bin/env python

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

def readTensiometer(tensiometerPIN):
    humidity=mcp3008.readadc(tensiometerPIN, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
    
    return humidity
