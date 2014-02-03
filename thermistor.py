class Thermistor():
    def __init__(self, thermistorPin):
        self.thermistorPin = thermistorPin

    def readAnalog(self):
        thermistorValue=mcp3008.readadc(self.thermistorPin, constants.SPICLK, constants.SPIMOSI,
                                        constants.SPIMISO, constants.SPICS)
        
        return thermistorValue

    def convertToTemperature
        
        
        
