from modules.Led import Led
from modules.Button import Button
from modules.Properties import Properties
from modules.Database import Database
from modules.Database import Executor

from RPi import GPIO as io
from time import sleep as wait
from sys import argv
import time
import math


class Worker:

    __running = True

    def __init__(self, args):
        self.defaults = {
            "time":".25",
            "button":"8",
            "led":"10",
            "host":"localhost",
            "user":"admin",
            "password":"password",
            "database":"ledtasterdb"
        }

        self.__properties = Properties(args, self.defaults)

        self.__activation_time = float(self.__properties.get("time"))
        self.__button =  Button(int(self.__properties.get("button")))
        self.__led = Led(int(self.__properties.get("led")))

        self.__db = Database(
            self.__properties.get("user"),
            self.__properties.get("password"),
            self.__properties.get("database"),
            self.__properties.get("host"))

        self.__executor = Executor(self.__db)

    def run(self):
        try:
            while self.__running:
                print("hi")
                self.__button.waitForPress()
                pressed = time.time()
                print("hi")

                self.__button.waitForRelease()
                released = time.time()
                duration = released - pressed

                if duration < self.__activation_time:
                    self.__led.switch()
                    self.__executor.saveState(self.__led.status)

        except KeyboardInterrupt:
            print("\nThe programm has been aborted.")
        finally:
            io.cleanup()
            self.__executor.close()
        

def main():
    worker = Worker(argv)
    worker.run()

if __name__ == "__main__":
    main()