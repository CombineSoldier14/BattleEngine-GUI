import json
import random
from tkinter import *
from tkinter import ttk

version = "1.4.0"

root = Tk()

root.title(f"BattleEngine v{version} by CombineSoldier14")

playerName = Label(root, text="Loading...")
playerName.place(x=10, y=10)

playerHealth = Label(root, text="Loading...")
playerHealth.place(x=10, y=30)

scrollbar = Scrollbar(root)
scrollbar.place(x=480, y=60, height=300)

mainLogView = Listbox(root, yscrollcommand=scrollbar.set)
mainLogView.place(x=10, y=60, width=470, height=300)

scrollbar.config(command=mainLogView.yview)

minionActive = Label(root, text="Loading...")
minionActive.place(x=500, y=0)

shieldActive = Label(root, text="Loading...")
shieldActive.place(x=500, y=20)

shieldsLeft = Label(root, text="Loading...")
shieldsLeft.place(x=500, y=60)

shieldDesc = Label(root, text="Loading...")
shieldDesc.place(x=500, y=80)

minionsLeft = Label(root, text="Loading...")
minionsLeft.place(x=500, y=100)

with open ('settings.json') as file:
    data = json.load(file)

def getDivider():
    divider = ""
    for i in range(56):
        divider += data["DIVIDER"]
    return divider

def rangeRNG(lowest: int, highest: int):
    return random.randint(lowest, highest)

class Player:
    def __init__(self, name: str, health: int, max_health: int, healingPotions: int, HealingPotionsName: str, minionActive: int, minions: int, minionTurns: int, minionMaxTurns: int, shieldActive: int, shields: int, shieldTurns: int, shieldMaxTurns: int, shieldDamage: int, shieldName: str, minionName: str):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.healingPotions = healingPotions
        self.HealingPotionsName = HealingPotionsName
        self.minionActive = minionActive
        self.minions = minions
        self.minionTurns = minionTurns
        self.minionMaxTurns = minionMaxTurns
        self.shieldActive = shieldActive
        self.shields = shields
        self.shieldTurns = shieldTurns
        self.shieldMaxTurns = shieldMaxTurns
        self.shieldDamage = shieldDamage
        self.shieldName = shieldName
        self.minionName = minionName
        
    def attack(self, opposingPlayer: object, lowest: int, highest: int, testlowest: int, testhighest: int, missPercent: int):
        if self.shieldActive:
            self.shieldTurns -= 1
            if self.shieldTurns <= 0:
                self.shieldActive = False
                print(f"{self.name}'s {self.shieldName} has worn off!")
                mainLogView.insert(END, f"{self.name}'s {self.shieldName} has worn off!")
                pass
        minionDamage = 0
        if self.minionActive:
            if self.minionTurns == 1:
                print(f"{self.name}'s {self.minionName} will be deactivated next turn!")
                mainLogView.insert(END, f"{self.name}'s {self.minionName} will be deactivated next turn!")
                pass
            self.minionTurns -= 1
            minionDamage = rangeRNG(lowest, highest)
            testhighest += 25
        testRng = rangeRNG(testlowest, testhighest)
        if testRng > missPercent:
            hitRng = rangeRNG(lowest, highest)
            damage = hitRng + minionDamage
            finalDamage = damage
            if opposingPlayer.shieldActive:
                finalDamage = finalDamage / self.shieldDamage
            opposingPlayer.health -= finalDamage
            print(f"\nThat's a hit! {hitRng} damage.\n")
            mainLogView.insert(END, f"\nThat's a hit! {hitRng} damage.\n")
            pass
            if self.minionActive:
                print(f"Active {self.minionName} added {minionDamage} damage.")
                mainLogView.insert(END, f"Active {self.minionName} added {minionDamage} damage.")
                pass
                if self.minionTurns <= 0:
                    self.minionActive = False
            if opposingPlayer.shieldActive:
                print(f"{opposingPlayer.name}'s {opposingPlayer.shieldName} blocked {damage - finalDamage} damage.")
                mainLogView.insert(END, f"{opposingPlayer.name}'s {opposingPlayer.shieldName} blocked {damage - finalDamage} damage.")
                pass
            print("\n")
            return 1
    
    def heal(self):
        if self.health >= self.max_health:
            return 2
        if self.healingPotions <= 0:
            return 3
        self.healingPotions -= 1
        healedHealth = rangeRNG(7, 20)
        self.health += healedHealth
        if self.health > self.max_health:
            total = 0
            while self.health > self.max_health:
                total += 1
                self.health -= 1
            healedHealth -= total
        print(f"{self.name} healed {healedHealth} health!\n")
        mainLogView.insert(END, f"{self.name} healed {healedHealth} health!\n")
        pass
        return 0

    def shield(self):
        if self.shields <= 0:
            return 6
        elif self.shieldActive:
            return 7
        else:
            print(f"{self.shieldName} enabled and active!")
            mainLogView.insert(END, f"{self.shieldName} enabled and active!")
            pass
            self.shieldActive = True
            self.shieldTurns = self.shieldMaxTurns
            self.shields -= 1
            return 0
    
    def summonMinion(self):
        if self.minions <= 0:
            return 4
        if(self.minionActive):
            return 5
        self.minions -= 1
        self.minionActive = True
        self.minionTurns = data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"]
        print(f"{self.minionName} summoned and active!\n")
        mainLogView.insert(END, f"{self.minionName} summoned and active!\n")
        pass
        return 0

    def getList(self, opposingPlayer: object):
        attacks = {}
        attacks["Small Attack"] = {}
        attacks["Small Attack"]["function"] = lambda: self.attack(opposingPlayer, 1, 15, 1, 100, 25)
        attacks["Small Attack"]["name"] = "Small Attack"
        
        attacks["Large Attack"] = {}
        attacks["Large Attack"]["function"] = lambda: self.attack(opposingPlayer, 15, 30, 1, 100, 50)
        attacks["Large Attack"]["name"] = "Large Attack"
        
        attacks[self.HealingPotionsName] = {}
        attacks[self.HealingPotionsName]["function"] = self.heal
        attacks[self.HealingPotionsName]["name"] = self.HealingPotionsName
        
        attacks[f"Summon {self.minionName}"] = {}
        attacks[f"Summon {self.minionName}"]["function"] = self.summonMinion
        attacks[f"Summon {self.minionName}"]["name"] = f"Summon {self.minionName}"
        
        attacks[f"Use {self.shieldName}"] = {}
        attacks[f"Use {self.shieldName}"]["function"] = self.shield
        attacks[f"Use {self.shieldName}"]["name"] = f"Use {self.shieldName}"
        return attacks

def finish(winningPlayer: Player):
    print(f"\n{winningPlayer.name} has won the battle with {winningPlayer.health} health!\n")

def turn(player1: Player, player2: Player):
    print(f"\n{getDivider()}\n")
    print(f"Current Turn: {player1.name}\n{player1.name}'s Health: {player1.health}\n{player2.name}'s Health: {player2.health}\n")
    attacks = player1.getList(player2)
    print("Attacks:")
    index = 0
    for i in attacks:
        print(f"{index + 1}. {i}")
        index += 1
    print(f"\n{player1.HealingPotionsName}s left: {player1.healingPotions}\n")
    print(f"{player1.shieldName}s left: {player1.shields}")
    print(f"{player1.shieldName}s divide damage by {player1.shieldDamage}. They last for 2 of your turns.")
    print(f"\nAvailable {player1.minionName}s: {player1.minions}\n{player1.minionName}s add a random damage boost (potentially double) but lower your chances of hitting. They last for {player1.minionMaxTurns} of your turns.")
    print(f"\n{player1.minionName} Active?: ")

    if player1.minionActive:
        print("Yes\n")
    else:
        print("No\n")
    
    print("Shield Active?: ")

    if player1.shieldActive:
        print("Yes")
    else:
        print("No")

    print(f"\n{getDivider()}\n")
    print("Type the name of your attack.\n")
    playerName.config(text=f"Current Turn: {player1.name}")
    playerHealth.config(text=f"Health: {player1.health}")
    minionActive.config(text=f"Minion Active: {player1.minionActive}")
    shieldActive.config(text=f"Shield Active: {player1.shieldActive}")
    shieldsLeft.config(text=f"Shields Left: {player1.shields}")
    shieldDesc.config(text=f"{player1.shieldName}s divide damage by {player1.shieldDamage}. They last for 2 of your turns.")
    minionsLeft.config(text=f"\nAvailable {player1.minionName}s: {player1.minions}")
    y = 140

    def on_button_click(func):
        func()
        root.quit()

    for x in attacks:
        Button(root, text=attacks[x]["name"], width=10, height=2, command=lambda func=attacks[x]["function"]: on_button_click(func)).place(x=500, y=y)
        y += 50

    root.mainloop()
    root.update_idletasks()
    """
    while True:
        x = input("> ")
        try:
            attak = attacks[x]()
            if attak == 2:
                print("Your health is already at max!\n")
            elif attak == 3:
                print(f"You don't have any {player1.HealingPotionsName}s!\n")
            elif attak == 4:
                print(f"You don't have any {player1.minionName}s left!")
            elif attak == 5:
                print(f"You already have a {player1.minionName} active!")
            elif attak == 6:
                print(f"You don't have any {player1.shieldName}s left!")
            elif attak == 7:
                print(f"You already have a {player1.shieldName} active!")
            else:
                break
        except:
            print(f"Attack \"{x}\" not found!\n")"
    """

def start(player1: Player, player2: Player):
    print(f"Made with BattleEngine v{version} by CombineSoldier14\n")
    mainLogView.insert(END, f"Made with BattleEngine v{version} by CombineSoldier14")
    pass  # add this after an insert to update tk root
    print(f"{getDivider()}\n")
    print(f"The battle has begun!\n {player1.name} vs {player2.name}")
    mainLogView.insert(END, f"The battle has begun! {player1.name} vs {player2.name}")
    pass
    
    while player1.health > 0 and player2.health > 0:
        turn(player1, player2)
        if player2.health <= 0:
            finish(player1)
            break
        turn(player2, player1)
        if player1.health <= 0:
            finish(player2)
            break


p1 = Player(
    name = data["PLAYER1"]["NAME"],
    health = data["PLAYER1"]["STARTING_HEALTH"],
    max_health = data["PLAYER1"]["STARTING_HEALTH"],
    healingPotions = data["PLAYER1"]["ATTACKS"]["HEALING_POTIONS"]["AMOUNT"],
    HealingPotionsName = data["PLAYER1"]["ATTACKS"]["HEALING_POTIONS"]["NAME"],
    minions = data["PLAYER1"]["ATTACKS"]["MINIONS"]["AMOUNT"],
    minionActive = False,
    minionTurns =  data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionMaxTurns = data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionName = data["PLAYER1"]["ATTACKS"]["MINIONS"]["NAME"],
    shieldTurns = 0,
    shieldMaxTurns = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldActive = False,
    shieldDamage = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["DIVIDE_DAMAGE"],
    shields = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldName = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["NAME"]
)

p2 = Player(
    name = data["PLAYER2"]["NAME"],
    health = data["PLAYER2"]["STARTING_HEALTH"],
    max_health = data["PLAYER2"]["STARTING_HEALTH"],
    healingPotions = data["PLAYER2"]["ATTACKS"]["HEALING_POTIONS"]["AMOUNT"],
    HealingPotionsName = data["PLAYER2"]["ATTACKS"]["HEALING_POTIONS"]["NAME"],
    minions = data["PLAYER2"]["ATTACKS"]["MINIONS"]["AMOUNT"],
    minionActive = False,
    minionTurns =  data["PLAYER2"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionMaxTurns = data["PLAYER2"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionName = data["PLAYER2"]["ATTACKS"]["MINIONS"]["NAME"],
    shieldTurns = 0,
    shieldMaxTurns = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldActive = False,
    shieldDamage = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["DIVIDE_DAMAGE"],
    shields = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldName = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["NAME"]
)

start(p1, p2)

mainloop()