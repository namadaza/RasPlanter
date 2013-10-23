#!/usr/bin/env python

#import read ADC function
import mcp3008
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG=1
LOGGER=1

#SPI pins on RasPi connected to ADC
SPICLK=18
SPIMISO=23
SPIMOSI=24
SPICS=25

#instantiate SPI interface
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#Xively variables to publish data on web
#specifc to amanazad account @ http://www.xivley.com
API_KEY='DhYvcI3WAbO1o5sKk9p7e47Q9bcptc5r81c2NX87RA72ZR'
FEEDID=1141885015

#pins on MCP3008 to sensors
phototransPIN=0
thermistorPIN=2

#main
#run with 1min load average from Xively
try:
    while True:       
        #read raw analog values (0-1023, 2^10)
        read_Phototrans=mcp3008.readadc(phototransPIN, SPICLK, SPIMOSI,
                                        SPIMISO, SPICS)
        #convert analog to lumens
        lumens=(read_Phototrans-180)*1.99

        read_Thermistor=mcp3008.readadc(thermistorPIN, SPICLK, SPIMOSI,
                                        SPIMISO, SPICS)
        #convert analog to C
        temp_C=25+((read_Thermistor-520)/4)
        #convert C to F
        temp_F=((temp_C*9)/5)+32
    
        #print out values to terminal
        if DEBUG:
            print "Phototransistor Analog Value = ", read_Phototrans
            print "Lumens: ", lumens
            print ""
            print "Thermistor Analog Value = ", read_Thermistor
            print "Degrees C: ", temp_C
            print "Degrees F: ", temp_F
            print ""
            print ""
            
        #required delay, avoid flooding information
        time.sleep(1.0);
except KeyboardInterrupt:
    GPIO.cleanup()
    
