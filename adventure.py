#!/usr/bin/env python3

import os, time, random
from functools import partial
class YouDied(Exception):
    pass
class Mob:
    def __init__(self, name, stats, level):
        self.name = name
        self.stats = stats
        self.level = level
class Monster(Mob):
    def __init__(self, attacks, name, stats, level):
        Mob.__init__(self, name, stats, level)
        self.attacks = attacks
class Inventory:
    items = [None, None, None, None, None, None, None, None, None]
    def push(self, Item, spot):
        
        if spot < 0 or spot > 8:
            print("Dieser Spot ist belegt!")
        else:
            self.items[spot] = Item
class Item:
    name = "Item"
    def __init__(self, name):
        self.name = name
class Weapon(Item):
    def __init__(self, additonalStats, name):
        self.additonalStats = {
                                "strength": additonalStats[0],
                                "health": additonalStats[1],
                                "intelligence": additonalStats[2],
                                "defense": additonalStats[3]
                              }
        Item.__init__(self, name)
class Player:
    targettedSpot = 0
    coins = 0
    exp = 0
    inventory = Inventory()
    stats = {
            "strength": 0,
            "health": 10,
            "intelligence": 0,
            "defense": 0
            }
    def swapTargettedSpot(self, desiredSpot):
        self.targettedSpot = desiredSpot
        self.giveBonusStats()
    def giveBonusStats(self):
        if self.inventory.items[self.targettedSpot] == None:
            pass
        else:
            self.stats["strength"] += self.inventory.items[self.targettedSpot].additonalStats["strength"]
            self.stats["health"] += self.inventory.items[self.targettedSpot].additonalStats["health"]
            self.stats["intelligence"] += self.inventory.items[self.targettedSpot].additonalStats["intelligence"]
            self.stats["defense"] += self.inventory.items[self.targettedSpot].additonalStats["defense"]

    def getName(self):
        return input("Wähle einen Namen!\n")
    def __init__(self, attacks):
        self.name = self.getName()
        self.attacks = attacks
class Game:
    def die(self):
        quit()
    def showMenu(self, player):
        os.system("clear")
        menupoint = input("Hauptmenü: \n\n 1) Stats\n 2) Inventar\n 3) Save\n 4) Exit\n")
        if menupoint == "2":
            self.showInventory(player)
        if menupoint == "1":
            self.showStats(player)
        if menupoint == "4":
            return 4
    def showInventory(self, player):
        os.system("clear")
        for i in range(len(player.inventory.items)):
            if player.inventory.items[i] == None:
                print(f"Slot {i + 1}: Nothing")
            else:
                print(f"Slot {i + 1}: {player.inventory.items[i].name}")
        exitinp = input("Exit by typing exit\n")
        if exitinp.lower() == "exit":
            self.showMenu(player)
    def showStats(self, player, clear = True):
        if clear:
            os.system("clear")
        print(f"Stärke: {player.stats['strength']}")
        print(f"Leben: {player.stats['health']}")
        print(f"Weisheit: {player.stats['intelligence']}")
        print(f"Verteidigung: {player.stats['defense']}")
        if clear:
            exitinp = input("Exit by typing exit\n")
            if exitinp.lower() == "exit":
                self.showMenu(player)
    def makeCommandMenu(self, params, clear=False):
        if clear:
            os.system("clear")
        userinput = input(params["prompt"] + "\n").lower()
        for key in params:
            if userinput == key:
                params[key]()
class Fight:
    def __init__(self, player, foe, game):
        self.turnCount = 0
        self.player = player
        self.foe = foe
        self.game = game
    def showFightMenu(self):
        os.system("clear")
        print("Your attacks:")
        for key in self.player.attacks:
            print(f"{self.player.attacks[key]['id']}) Does {self.player.stats['strength'] * self.player.attacks[key]['damageMultiplier']} damage. Heals you for {self.player.stats['health'] * self.player.attacks[key]['healing']} health.")
        print(f"Your stats: ")
        self.game.showStats(self.player, False)
        print("\n\n\n\nOpponents Stats:")
        self.game.showStats(self.foe, False)
        
        
        
        if self.turnCount % 2 == 0:
            self.makeHumanTurn()
        else:
            self.makeFoeTurn()
            self.turnCount += 1
            
    def doAttack(self, executor, attack):
        if executor == 1:
            self.foe.stats['health'] -= attack['damageMultiplier'] * self.player.stats['strength']
            self.player.stats['health'] += attack['healing'] * self.player.stats['health']
            os.system("clear")
            print(f"You used attack {attack['id']} on your enemy!")
            time.sleep(1.6)
            os.system("clear")
        elif executor == 0:
            self.foe.stats['health'] += attack['healing'] * self.foe.stats['health']
            self.player.stats['health'] -= attack['damageMultiplier'] * self.foe.stats['strength']
            os.system("clear")
            print(f"Your enemy used attack {attack['id']} on you!")
            time.sleep(1.6)
            os.system("clear")
        
        if self.foe.stats['health'] <= 0:
            print("Du hast den Kampf gewonnen!\nLoot:")
            print(str(self.foe.level * 10) + " Münzen!")
            print(str(self.foe.level) + " Exp")
            return
        if self.player.stats['health'] <= 0:
            print("Du hast verloren!")
            self.game.die()
            
        self.turnCount += 1
        self.showFightMenu()
    def makeHumanTurn(self):
        params = {
            "prompt": "Which attack do you choose?"
        }
        for key in self.player.attacks:
            for id in self.player.attacks[key]:
                params[str(self.player.attacks[key]['id'])] = partial(self.doAttack, 1, self.player.attacks[key])   
        self.game.makeCommandMenu(params)
    def makeFoeTurn(self):
        self.doAttack(0, self.foe.attacks[random.choice(list(self.foe.attacks.keys()))])
    def startFight(self):
        os.system("clear")
        print(f"A wild {self.foe.name} appeared!")
        time.sleep(1.5)
        os.system("clear")
        self.showFightMenu()
        
if __name__ == "__main__":
    os.system("clear")
    game = Game()
    player = Player({"Hit": {
                        "displayname": "Hit with your equipped weapon",
                        "damageMultiplier": 1.5,
                        "healing": 0,
                        "id": 1
                        },
                "Heal": {
                            "displayname": "Heal yourself for 0.2 times your health",
                            "damageMultiplier": 0,
                            "healing": 0.2,
                            "id": 2
                        }
                    })
    print(f"Willkommen zu deinem Abenteuer, {player.name}. \n")
    time.sleep(3)
    os.system("clear")
    woodenSword = Weapon([2, 0, 0, 0], "Holzschwert")
    jn = input("Du wachst auf einer grünen Wiese auf. \nDu schaust dich um, doch siehst niemanden. Neben dir liegt ein Schwert.\nWillst du es aufnehmen(J/N)\n").lower()
    if(jn == "n"):
        print("Du nimmst das Schwert nicht und gehst weiter.")
    elif jn == "j":
        print(f"Du nimmst das {woodenSword.name}!")
        player.inventory.push(woodenSword, 0)
        player.swapTargettedSpot(0)
    moepel = Monster({
                        "Suck": {
                            "displayname": "Sucks your blood and heals itself!",
                            "damageMultiplier": 1.3,
                            "healing": 0.1,
                            "id": 1
                        }, 
                        "Heal": {
                            "displayname": "Heal",
                            "damageMultiplier": 0,
                            "healing": 0.3,
                            "id": 2
                        }
                    }, "Möpel", {
                        "strength": 3,
                        "health": 8,
                        "intelligence": 0,
                        "defense": 1
                    }, 2)
    fightAgainstMoepel = Fight(player, moepel, game)
    fightAgainstMoepel.startFight()
    print("Du hast das Spil gewonnered!")
