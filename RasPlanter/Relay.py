#!/usr/bin/env python

#must have imports in same directory
#import read ADC function
import constants
import mcp3008
import time
import RPi.GPIO as GPIO

class Relay():
    def __init__(self, relayPIN):
        self.relayPin = relayPin
        #pin numbering system (relative to revision number)
        GPIO.setmode(GPIO.BCM)

        #instantiate relay @ the relay pin
        GPIO.setup(self.relayPin, GPIO.OUT)
        
    #turn relay on and off depending on an input value
    def regulateThreshold(self, thresholdValue, inputValue):
        self.thresholdValue = thresholdValue
        self.inputValue = inputValue
        if (inputValue<ThresholdValue):
            GPIO.output(True)
        elif (inputValue>ThresholdValue):
            GPIO.output(False)
        else:
            GPIO.output(False)

    def setModeOff(self):
        GPIO.output(False)

    def setModeOn(self):
        GPIO.output(True)

