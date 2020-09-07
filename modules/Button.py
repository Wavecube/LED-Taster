from modules.Component import Component

from RPi import GPIO as io


class Button(Component):

    def __init__(self, ioPin, ioMode=io.BOARD):
        super().__init__(ioPin, io.IN, ioMode)

    def getStatus(self):
        return io.input(self._ioPin)
    
    def waitForPress(self):
        while not self.getStatus():
            pass
        
    def waitForRelease(self):
        while self.getStatus():
            pass