#!/usr/bin/env python

#must have imports in same directory
#import read ADC function
import constants
import mcp3008
import time
import RPi.GPIO as GPIO

class Relay():
    def __init__(self, relayPIN):
        self.relayPIN = relayPIN
        #pin numbering system (relative to revision number)
        GPIO.setmode(GPIO.BCM)

        #instantiate relay @ the relay pin
        GPIO.setup(self.relayPIN, GPIO.OUT)
        
    #turn relay on and off depending on an input value
    def regulateThreshold(self, thresholdValue, inputValue):
        self.thresholdValue = thresholdValue
        self.inputValue = inputValue
        if (inputValue<thresholdValue):
            GPIO.output(self.relayPIN, True)
            return 1
        elif (inputValue>thresholdValue):
            GPIO.output(self.relayPIN, False)
            return 0
        else:
            GPIO.output(self.relayPIN, False)
            return 0

    def setModeOff(self):
        GPIO.output(self.relayPIN, False)

    def setModeOn(self):
        GPIO.output(self.relayPIN, True)

