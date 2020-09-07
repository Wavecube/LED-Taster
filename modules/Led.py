from modules.Component import Component

from RPi import GPIO as io


class Led(Component):
    
    status = False

    def __init__(self, ioPin:int, ioMode=io.BOARD):
        super().__init__(ioPin, io.OUT, ioMode)

    def switch(self, status:bool = None):
        if status == None:
            if self.status == False:
                self.status = True
                self._on()
            else:
                self.status = False
                self._off()
        elif status == True:
            self.status = status
            self._on()
        else:
            self.status = status
            self._off()
    
    def _on(self):
        io.output(self._ioPin, True)

    def _off(self):
        io.output(self._ioPin, False)