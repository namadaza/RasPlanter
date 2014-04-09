#!/usr/bin/env python
##^-----------------^ required to make executable
#use 'sudo chmod +x filename.py' to make exec
#use 'sudo ./filename.py' to run in terminal
import RPi.GPIO as GPIO
import os
import eeml

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

#read SPI data from MPC3008 chip, 8 possible ADC inputs (0-7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    #reject invalid adc pin numbers
    if ((adcnum>7) or (adcnum<0)):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False) #start clock low
    GPIO.output(cspin, False) #bring cs low

    commandout = adcnum
    commandout |= 0x18 #start bit + single-ended bit, whatis '|=' operator
    commandout <<=3 #only need to send 5 bits here, whatis '<<=' operator
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
    adcout = 0
    #read one empty bit, one null bit, 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<=1
        if (GPIO.input(misopin)):
            adcout |= 0x1
    GPIO.output(cspin, True)

    adcout /= 2 #first bit is 'null', drop it
    return adcout

while True:
    value = readadc(2, 18, 24, 23, 25)
    print value
