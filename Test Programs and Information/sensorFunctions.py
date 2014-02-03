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

#outputs 0-1023 (2^10, 10 bits) analog value from phototransistor
def readPhototransistor(phototransPIN):
    phototransValue=mcp3008.readadc(phototransPIN, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
    return phototransValue

#convert analog value to rough lumens (needs tuning)
def convertToLumens(phototransValue):
    lumens=abs((phototransValue-180)*1.99)

    return lumens

#outputs 0-1023 (2^10, 10 bits) analog value from thermistor
def readThermistor(thermistorPIN):
    thermistorValue=mcp3008.readadc(thermistorPIN, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)

    return thermistorValue

#convert analog value to celsius
def convertToC(thermistorValue):
    temp_C=25+((thermistorValue-520)/4)

    return temp_C

#convert analog value to fahrenheit
def convertToF(thermistorValue):
    temp_C=25+((thermistorValue-520)/4)
    temp_F=((temp_C*9)/5)+32

    return temp_F

def readTensiometer(tensiometerPIN):
    humidity=mcp3008.readadc(tensiometerPIN, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
    
    return humidity
