import json
import random
from tkinter import *
from tkinter import ttk

VERSION = "1.4.0"

def rangeRNG(lowest: int, highest: int):
    return random.randint(lowest, highest)

class BattleEngine:
    def __init__(self, root):
        self.root = root
        self.root.title(f"BattleEngine v{VERSION} by CombineSoldier14")
        self.root.geometry("700x500")
        
        # Add the action_completed variable
        self.action_completed = BooleanVar()
        
        # Load game settings
        with open('settings.json') as file:
            self.data = json.load(file)
            
        self.setup_ui()
        self.initialize_players()
        
    def setup_ui(self):
        # Main frame for status information
        status_frame = Frame(self.root)
        status_frame.pack(fill=X, padx=10, pady=10)
        
        # Player status
        self.player_name = Label(status_frame, text="Loading...")
        self.player_name.grid(row=0, column=0, sticky=W)
        
        self.player_health = Label(status_frame, text="Loading...")
        self.player_health.grid(row=1, column=0, sticky=W)
        
        # Combat log section
        log_frame = Frame(self.root)
        log_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.main_log_view = Listbox(log_frame)
        self.main_log_view.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(log_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.main_log_view.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.main_log_view.yview)
        
        # Right side status panel
        status_panel = Frame(self.root)
        status_panel.pack(side=RIGHT, fill=Y, padx=10)
        
        self.minion_active = Label(status_panel, text="Minion Active: No")
        self.minion_active.pack(anchor=W, pady=2)
        
        self.shield_active = Label(status_panel, text="Shield Active: No")
        self.shield_active.pack(anchor=W, pady=2)
        
        self.shields_left = Label(status_panel, text="Shields Left: 0")
        self.shields_left.pack(anchor=W, pady=2)
        
        self.shield_desc = Label(status_panel, text="Shield description", wraplength=200)
        self.shield_desc.pack(anchor=W, pady=2)
        
        self.minions_left = Label(status_panel, text="Available minions: 0")
        self.minions_left.pack(anchor=W, pady=2)
        
        # Action buttons frame
        self.action_frame = Frame(self.root)
        self.action_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)
    
    def log_message(self, message):
        """Add message to both console and log view"""
        print(message)
        self.main_log_view.insert(END, message)
        self.main_log_view.see(END)  # Auto-scroll to the end
        self.root.update_idletasks()
    
    def initialize_players(self):
        """Initialize player objects from settings"""
        self.p1 = Player(
            name=self.data["PLAYER1"]["NAME"],
            health=self.data["PLAYER1"]["STARTING_HEALTH"],
            max_health=self.data["PLAYER1"]["STARTING_HEALTH"],
            healingPotions=self.data["PLAYER1"]["ATTACKS"]["HEALING_POTIONS"]["AMOUNT"],
            HealingPotionsName=self.data["PLAYER1"]["ATTACKS"]["HEALING_POTIONS"]["NAME"],
            minions=self.data["PLAYER1"]["ATTACKS"]["MINIONS"]["AMOUNT"],
            minionActive=False,
            minionTurns=self.data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"],
            minionMaxTurns=self.data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"],
            minionName=self.data["PLAYER1"]["ATTACKS"]["MINIONS"]["NAME"],
            shieldTurns=0,
            shieldMaxTurns=self.data["PLAYER1"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
            shieldActive=False,
            shieldDamage=self.data["PLAYER1"]["ATTACKS"]["SHIELDS"]["DIVIDE_DAMAGE"],
            shields=self.data["PLAYER1"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
            shieldName=self.data["PLAYER1"]["ATTACKS"]["SHIELDS"]["NAME"]
        )

        self.p2 = Player(
            name=self.data["PLAYER2"]["NAME"],
            health=self.data["PLAYER2"]["STARTING_HEALTH"],
            max_health=self.data["PLAYER2"]["STARTING_HEALTH"],
            healingPotions=self.data["PLAYER2"]["ATTACKS"]["HEALING_POTIONS"]["AMOUNT"],
            HealingPotionsName=self.data["PLAYER2"]["ATTACKS"]["HEALING_POTIONS"]["NAME"],
            minions=self.data["PLAYER2"]["ATTACKS"]["MINIONS"]["AMOUNT"],
            minionActive=False,
            minionTurns=self.data["PLAYER2"]["ATTACKS"]["MINIONS"]["TURNS"],
            minionMaxTurns=self.data["PLAYER2"]["ATTACKS"]["MINIONS"]["TURNS"],
            minionName=self.data["PLAYER2"]["ATTACKS"]["MINIONS"]["NAME"],
            shieldTurns=0,
            shieldMaxTurns=self.data["PLAYER2"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
            shieldActive=False,
            shieldDamage=self.data["PLAYER2"]["ATTACKS"]["SHIELDS"]["DIVIDE_DAMAGE"],
            shields=self.data["PLAYER2"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
            shieldName=self.data["PLAYER2"]["ATTACKS"]["SHIELDS"]["NAME"]
        )
        
        # Link players to the game engine
        self.p1.set_game_engine(self)
        self.p2.set_game_engine(self)
        
    def start_game(self):
        """Begin the game battle"""
        self.log_message(f"Made with BattleEngine v{VERSION} by CombineSoldier14")
        self.log_message(self.get_divider())
        self.log_message(f"The battle has begun! {self.p1.name} vs {self.p2.name}")
        
        # Start the battle loop
        self.battle_loop()
    
    def battle_loop(self):
        """Main battle loop between players"""
        while self.p1.health > 0 and self.p2.health > 0:
            self.process_turn(self.p1, self.p2)
            if self.p2.health <= 0:
                self.finish_battle(self.p1)
                break
            self.process_turn(self.p2, self.p1)
            if self.p1.health <= 0:
                self.finish_battle(self.p2)
                break
    
    def process_turn(self, attacker, defender):
        """Handle a single player's turn"""
        # Reset the action completed flag
        self.action_completed.set(False)
        
        self.log_message(f"\n{self.get_divider()}\n")
        self.log_message(f"Current Turn: {attacker.name}")
        self.log_message(f"{attacker.name}'s Health: {attacker.health}")
        self.log_message(f"{defender.name}'s Health: {defender.health}\n")
        
        # Update UI
        self.update_player_ui(attacker)
        
        # Get available attacks
        attacks = attacker.get_list(defender)
        
        # Clear previous action buttons
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        
        # Create new action buttons
        for name, attack_info in attacks.items():
            Button(
                self.action_frame, 
                text=attack_info["name"], 
                width=15, 
                command=lambda f=attack_info["function"]: self.execute_action(f)
            ).pack(side=LEFT, padx=5)
        
        # Wait for button click
        self.root.wait_variable(self.action_completed)
    
    def execute_action(self, action_function):
        """Execute the selected action and continue the game"""
        result = action_function()
        self.handle_action_result(result)
        self.action_completed.set(True)
    
    def handle_action_result(self, result):
        """Handle the result code from an action"""
        if result == 2:
            self.log_message("Your health is already at max!\n")
        elif result == 3:
            self.log_message(f"You don't have any healing potions!\n")
        elif result == 4:
            self.log_message(f"You don't have any minions left!")
        elif result == 5:
            self.log_message(f"You already have a minion active!")
        elif result == 6:
            self.log_message(f"You don't have any shields left!")
        elif result == 7:
            self.log_message(f"You already have a shield active!")
    
    def update_player_ui(self, player):
        """Update the UI to show current player status"""
        self.player_name.config(text=f"Current Turn: {player.name}")
        self.player_health.config(text=f"Health: {player.health}")
        self.minion_active.config(text=f"Minion Active: {player.minionActive}")
        self.shield_active.config(text=f"Shield Active: {player.shieldActive}")
        self.shields_left.config(text=f"Shields Left: {player.shields}")
        self.shield_desc.config(
            text=f"{player.shieldName}s divide damage by {player.shieldDamage}. "
                 f"They last for 2 of your turns."
        )
        self.minions_left.config(text=f"Available {player.minionName}s: {player.minions}")
    
    def finish_battle(self, winner):
        """End the battle with a winner"""
        self.log_message(f"\n{winner.name} has won the battle with {winner.health} health!\n")
        
        # Create a "Play Again" button
        Button(
            self.action_frame,
            text="Play Again", 
            width=15,
            command=self.restart_game
        ).pack(fill=X)
    
    def restart_game(self):
        """Restart the game"""
        # Clear log
        self.main_log_view.delete(0, END)
        
        # Reinitialize players
        self.initialize_players()
        
        # Start a new game
        self.start_game()
    
    def get_divider(self):
        """Return a divider string from settings"""
        divider = ""
        for i in range(56):
            divider += self.data["DIVIDER"]
        return divider


class Player:
    def __init__(self,
                name: str, 
                health: int,
                max_health: int,
                healingPotions: int,
                HealingPotionsName: str,
                minionActive: int,
                minions: int,
                minionTurns: int,
                minionMaxTurns: int,
                shieldActive: int,
                shields: int,
                shieldTurns: int,
                shieldMaxTurns: int,
                shieldDamage: int,
                shieldName: str,
                minionName: str):
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
        self.game_engine = None
    
    def set_game_engine(self, engine):
        """Connect player to the game engine for logging"""
        self.game_engine = engine
    
    def log(self, message):
        """Log messages through the game engine"""
        if self.game_engine:
            self.game_engine.log_message(message)
        else:
            print(message)  # Fallback if no game engine is set
        
    def attack(self, opposingPlayer: object, lowest: int, highest: int, testlowest: int, testhighest: int, missPercent: int):
        if self.shieldActive:
            self.shieldTurns -= 1
            if self.shieldTurns <= 0:
                self.shieldActive = False
                self.log(f"{self.name}'s {self.shieldName} has worn off!")
                pass
        minionDamage = 0
        if self.minionActive:
            if self.minionTurns == 1:
                self.log(f"{self.name}'s {self.minionName} will be deactivated next turn!")
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
            self.log(f"\nThat's a hit! {hitRng} damage.\n")
            pass
            if self.minionActive:
                self.log(f"Active {self.minionName} added {minionDamage} damage.")
                pass
                if self.minionTurns <= 0:
                    self.minionActive = False
            if opposingPlayer.shieldActive:
                self.log(f"{opposingPlayer.name}'s {opposingPlayer.shieldName} blocked {damage - finalDamage} damage.")
                pass
            self.log("\n")
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
        self.log(f"{self.name} healed {healedHealth} health!\n")
        pass
        return 0

    def shield(self):
        if self.shields <= 0:
            return 6
        elif self.shieldActive:
            return 7
        else:
            self.log(f"{self.shieldName} enabled and active!")
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
        # Fix reference to data - use the instance variable instead
        self.minionTurns = self.minionMaxTurns
        self.log(f"{self.minionName} summoned and active!\n")
        return 0

    def get_list(self, opposingPlayer: object):
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

def main():
    """Main entry point for the application"""
    root = Tk()
    game = BattleEngine(root)
    game.start_game()
    root.mainloop()

if __name__ == "__main__":
    main()
