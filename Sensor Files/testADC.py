#!/usr/bin/env python
##^-----------------^ required to make executable
#use 'sudo chmod +x filename.py' to make exec
#use 'sudo ./filename.py' to run in terminal
import RPi.GPIO as GPIO
import time
import os
import eeml

GPIO.setmode(GPIO.BCM)
DEBUG = 1
LOGGER = 1

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

#pins connected from ADC to RasPi
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

#setup SPI interface
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

################################
#check for COSM interface
################################

#phototransistor on adc pin 0
adcnum = 6
adcnum2 = 5

while True:
    #read analog pin (phototransistor)
    read_adc5 = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
    read_adc6 = readadc(adcnum2, SPICLK, SPIMOSI, SPIMISO, SPICS)

    #print analog values (0-1023, 2^10)
    if DEBUG:
        print("read_adc0:\t", read_adc5)
        print("read_adc2:\t", read_adc6) 

    #required delay, avoid flooding information
        time.sleep(.75)

    
