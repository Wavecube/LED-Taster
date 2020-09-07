from modules.Properties import Properties
from modules.Properties import Lang
from modules.Button import Button
from modules.Led import Led


from RPi import GPIO as io
from sys import argv
from time import sleep as wait
from random import randint
import time


class Game:

    def __init__(self, properties):
        presc = lambda s:  int(self.__properties.get(s)) * int(self.__properties.get("precision"))
        self.__properties = properties
        self.__button = Button(int(self.__properties.get("button")))
        self.__led = Led(int(self.__properties.get("led")))
        self.__min_time = presc("min_time")
        self.__max_time = presc("max_time")
        self.__default_lang = Lang(self.__properties.get("lang"))
        self.__prescision = int(self.__properties.get("precision"))
        self.__wait = int(self.__properties.get("wait"))
        print(self.__min_time, self.__max_time)
    
    # Prompts the player to select the Language.
    def __selectLanguage(self):
        self.selected_lang = input(self.__default_lang.get("language", default=self.__properties.get("lang"), languages=Lang.langsToString()))
        self.lang = Lang(self.selected_lang) if self.selected_lang in Lang.listLangs() else self.__default_lang
        print(self.lang.get("language_selected", language=self.lang.toString()))
    
    # Asks the players if they know the rules and tells them.
    def __rules(self):
        if input(self.lang.get("rules_know")).lower() == "n": print(self.lang.get("rules"))
    
    # Asks for the names of the players saves them, and prints them out.
    def __registerPlayers(self):
        self.registered_players = self.lang.promptL("names", strip=True)
        while len(self.registered_players) is not 2:
            print(self.lang.get("names_min"))
            self.registered_players += self.lang.promptL("names", strip=True)
        p_index = 1
        for player in range(len(self.registered_players)):
            if self.registered_players[player] is "":
                self.registered_players[player] = self.lang.get("names_def_player", i=str(p_index)).replace("\n", "")
                p_index += 1
                
        print(self.lang.get("names_registered", players=self.__playersToString()))

    # Converts the registered Players to a readable string.
    def __playersToString(self):
        players = ""    
        for player in self.registered_players: 
            if player is self.registered_players[0]:
                players += player
            else:
                players += ", " + player
        return players

    # starts the main-game
    def __start(self):
        print(self.lang.get("start", player=self.registered_players[0]))
        for player in self.registered_players: self.__session(player)

    # Simulates one phase of the game.
    def __session(self, player):
        # init
        self.timings = {}
        self.__led.switch(True)

        # Phase 1
        print(self.lang.get("next", player=player))
        self.__button.waitForPress()
        wait(float(self.__properties.get("delay")))

        # Phase 2
        self.__led.switch(False)
        rand_time = time.time() + (randint(self.__min_time, self.__max_time) / self.__prescision)
        
        lost = False
        while rand_time > time.time():
            if self.__button.getStatus():
                self.__button.getStatus()
                lost = True
                break
        # Phase 3
        if not lost:
            self.__led.switch(True)
            swiched = time.time()
            self.__button.waitForPress()
            pressed = time.time()
            self.timings[player] = pressed - swiched
            self.__led.switch(False)
        else:
            print(self.lang.get("lost", player=player))

        wait(self.__wait)
    
    # Determines who the winner is
    def __determineWinner(self):
        winner = [None, None]
        if len(self.timings) is not 0:
            for player, w_time in self.timings.items():
                if winner[0] is None: winner[0] = player; winner[1] = w_time
                if winner[1] > w_time: winner[0] = player; winner[1] = w_time
            print(self.lang.get("winner", player=winner[0], time=str(round(winner[1], 3)) + "s"))
        else:
            print(self.lang.get("no_winner"))

    def run(self):
        self.__selectLanguage()
        self.__rules()
        self.__registerPlayers()
        self.__start()
        self.__determineWinner()

class Worker:

    def __init__(self, args):
        self.defaults = {
            "button":"8",
            "led":"10",
            "lang":"de_de",
            "min_time":"3",
            "max_time":"10",
            "precision":"1000",
            "wait":"2",
            "delay":".5"
        }

        self.properties = Properties(args, self.defaults)
        self.game = Game(self.properties)

    def run(self):
        try:
            self.game.run()
        except KeyboardInterrupt:
            print("\nThe programm has been aborted.")
        finally:
            io.cleanup()


def main():
    worker = Worker(argv)
    worker.run()

if __name__ == "__main__":
    main()