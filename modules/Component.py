from RPi import GPIO as io


class Component:

    def __init__(self, ioPin, ioType, ioMode=io.BOARD):
        self._ioPin = ioPin
        io.setmode(ioMode)
        io.setup(self._ioPin, ioType)
