# Fk off people from class copying ideas.

import random
import time

# --- Utility Functions ---
def clear_screen():
    """Clears the console screen by printing many newlines."""
    print("\n" * 50)

def print_slow(text, delay=0.03):
    """Prints text with a slight delay for a more dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_header(title):
    """Prints a styled header."""
    print("=" * 40)
    print(f"{title:^40}")
    print("=" * 40)

# --- Character and Boss Blueprints (Classes) ---

class Character:
    """Base class for all characters, including the player."""
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.abilities = {}
        self.is_defending = False
        self.status_effects = {} # e.g., {'poison': 3} for 3 turns of poison

    def is_alive(self):
        """Check if the character's HP is above 0."""
        return self.hp > 0

    def take_damage(self, damage, attacker_name="An opponent"):
        """Calculates and applies damage to the character, with a chance for a critical hit."""
        # Critical Hit Chance
        is_critical = random.random() < 0.10 # 10% chance for a critical hit
        if is_critical:
            damage = int(damage * 1.5)
            print_slow(f"*** CRITICAL HIT from {attacker_name}! ***")

        actual_defense = self.defense * 2 if self.is_defending else self.defense
        damage_taken = max(0, damage - actual_defense)
        self.hp -= damage_taken
        self.hp = max(0, self.hp) # Can't have negative HP
        if self.is_defending:
            print_slow(f"{self.name} defends and mitigates some damage!")
        print_slow(f"{self.name} takes {damage_taken} damage!")
        return damage_taken

    def heal(self, amount):
        """Heals the character."""
        self.hp += amount
        self.hp = min(self.max_hp, self.hp)
        print_slow(f"{self.name} heals for {amount} HP!")

    def display_status(self):
        """Shows the character's current status."""
        # Using a simple '#' for the HP bar to avoid potential encoding errors in some terminals.
        hp_bar = f"[{'#' * int((self.hp / self.max_hp) * 20):<20}]"
        print(f"{self.name}: HP {self.hp}/{self.max_hp} {hp_bar}")
        if self.status_effects:
            effects = ", ".join([f"{k.capitalize()} ({v} turns)" for k, v in self.status_effects.items()])
            print(f"  Status: {effects}")


class Player(Character):
    """Player character class with specific abilities based on their role."""
    def __init__(self, name, hp, attack, defense, mana, role):
        super().__init__(name, hp, attack, defense)
        self.role = role
        self.max_mana = mana
        self.mana = mana
        self.potions = 3
        self._initialize_abilities()

    def display_status(self):
        """Shows the player's current status, including mana."""
        super().display_status()
        mana_bar = f"[{'@' * int((self.mana / self.max_mana) * 10):<10}]"
        print(f"  Mana: {self.mana}/{self.max_mana} {mana_bar} | Potions: {self.potions}")

    def regenerate_mana(self):
        """Regenerate a small amount of mana each turn."""
        mana_regen = 5
        self.mana = min(self.max_mana, self.mana + mana_regen)


    def _initialize_abilities(self):
        """Sets abilities based on the player's role."""
        if self.role == "Warrior":
            self.abilities = {
                "1": {"name": "Power Strike", "cost": 10, "effect": self._power_strike},
                "2": {"name": "Shield Wall", "cost": 5, "effect": self._shield_wall},
                "3": {"name": "Reckless Swing", "cost": 20, "effect": self._reckless_swing}
            }
        elif self.role == "Mage":
            self.attack = 5 # Mages have low base attack
            self.abilities = {
                "1": {"name": "Fireball", "cost": 15, "effect": self._fireball},
                "2": {"name": "Heal", "cost": 20, "effect": self._heal_spell},
                "3": {"name": "Arcane Shield", "cost": 25, "effect": self._arcane_shield}
            }
        elif self.role == "Archer":
            self.abilities = {
                "1": {"name": "Aimed Shot", "cost": 15, "effect": self._aimed_shot},
                "2": {"name": "Poison Arrow", "cost": 10, "effect": self._poison_arrow},
                "3": {"name": "Double Shot", "cost": 25, "effect": self._double_shot}
            }

    # --- Warrior Abilities ---
    def _power_strike(self, target):
        print_slow(f"{self.name} uses Power Strike!")
        damage = int(self.attack * 1.5)
        target.take_damage(damage, self.name)

    def _shield_wall(self, target):
        print_slow(f"{self.name} raises their shield, preparing for the next attack!")
        self.is_defending = True # Handled in the main game loop
    
    def _reckless_swing(self, target):
        print_slow(f"{self.name} throws caution to the wind with a Reckless Swing!")
        self.defense -= 3
        print_slow(f"{self.name}'s defense is temporarily lowered!")
        damage = self.attack * 2
        target.take_damage(damage, self.name)

    # --- Mage Abilities ---
    def _fireball(self, target):
        print_slow(f"{self.name} casts Fireball!")
        damage = random.randint(15, 25)
        target.take_damage(damage, self.name)

    def _heal_spell(self, target):
        print_slow(f"{self.name} casts a healing spell!")
        heal_amount = random.randint(20, 30)
        self.heal(heal_amount)
    
    def _arcane_shield(self, target):
        print_slow(f"{self.name} conjures an Arcane Shield!")
        # For simplicity, we'll just boost defense temporarily
        self.defense += 5
        print_slow(f"{self.name}'s defense is temporarily boosted!")

    # --- Archer Abilities ---
    def _aimed_shot(self, target):
        print_slow(f"{self.name} takes careful aim for an Aimed Shot!")
        if random.random() > 0.15: # 85% chance to hit
            damage = self.attack + random.randint(8, 15)
            target.take_damage(damage, self.name)
        else:
            print_slow(f"{self.name}'s arrow misses!")

    def _poison_arrow(self, target):
        print_slow(f"{self.name} fires a Poison Arrow!")
        target.take_damage(self.attack, self.name)
        if 'poison' not in target.status_effects:
            print_slow(f"{target.name} has been poisoned!")
            target.status_effects['poison'] = 3
        else:
            print_slow(f"{target.name} is already poisoned!")
    
    def _double_shot(self, target):
        print_slow(f"{self.name} fires two arrows in quick succession!")
        target.take_damage(self.attack, self.name)
        time.sleep(0.5)
        target.take_damage(self.attack, self.name)

class Boss(Character):
    """The main antagonist."""
    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)
        self.is_enraged = False
        self.abilities = {
            self._stomp: 0.5, # Ability function: probability
            self._dark_breath: 0.3,
            self._frightening_roar: 0.2
        }

    def choose_action(self, target):
        """Boss AI: Chooses an action based on probabilities and enrage state."""
        print_slow(f"\n{self.name}'s turn...")
        time.sleep(1)

        # Enrage mechanic
        if self.hp < self.max_hp * 0.3 and not self.is_enraged:
            self.is_enraged = True
            self.attack += 5
            print_slow(f"{self.name} becomes ENRAGED! Its attack power has increased!")
        
        abilities = list(self.abilities.keys())
        weights = list(self.abilities.values())
        chosen_ability = random.choices(abilities, weights, k=1)[0]
        
        chosen_ability(target)

    # --- Boss Abilities ---
    def _stomp(self, target):
        print_slow(f"{self.name} rears back and STOMPS the ground!")
        damage = self.attack + random.randint(-3, 5)
        target.take_damage(damage, self.name)

    def _dark_breath(self, target):
        print_slow(f"{self.name} unleashes a torrent of dark energy!")
        damage = self.attack + random.randint(5, 10)
        target.take_damage(damage, self.name)

    def _frightening_roar(self, target):
        print_slow(f"{self.name} lets out a Frightening Roar!")
        print_slow(f"{target.name}'s defense is lowered!")
        target.defense = max(1, target.defense - 2) # Lower defense, min of 1

# --- Game Logic ---

def choose_class():
    """Lets the player select their character class."""
    print_header("Choose Your Class")
    print("1: Warrior - A sturdy fighter with high defense and reliable damage.")
    print("2: Mage - A powerful spellcaster with high damage and healing abilities.")
    print("3: Archer - A nimble marksman who uses precision and status effects.")
    
    choice = ""
    while choice not in ["1", "2", "3"]:
        choice = input("Enter your choice (1-3): ")

    player_name = input("Enter your hero's name: ")
    if not player_name:
        player_name = "Hero"

    if choice == "1":
        return Player(player_name, 120, 12, 8, 50, "Warrior")
    elif choice == "2":
        return Player(player_name, 80, 10, 4, 100, "Mage")
    elif choice == "3":
        return Player(player_name, 100, 15, 6, 70, "Archer")

def process_status_effects(character):
    """Applies and removes status effects at the start of a turn."""
    effects_to_remove = []
    if 'poison' in character.status_effects:
        poison_damage = 5
        print_slow(f"{character.name} takes {poison_damage} damage from poison!")
        character.hp -= poison_damage
        character.hp = max(0, character.hp)
        character.status_effects['poison'] -= 1
        if character.status_effects['poison'] <= 0:
            print_slow(f"{character.name} is no longer poisoned.")
            effects_to_remove.append('poison')

    for effect in effects_to_remove:
        del character.status_effects[effect]


class Game:
    """Coordinates the flow of the boss battle."""

    def __init__(self):
        self.player = None
        self.boss = None
        self.player_original_defense = 0
        self.turn = 1

    def setup(self):
        clear_screen()
        print_header("BOSS BATTLE")
        print_slow("A fearsome beast appears!")
        time.sleep(1)

        self.player = choose_class()
        self.boss = Boss("Gargantuan Hydra", 250, 15, 5)
        self.player_original_defense = self.player.defense

    def run(self):
        self.setup()
        while self.player.is_alive() and self.boss.is_alive():
            self._start_turn()
            if not self._player_turn():
                break
            if not self.boss.is_alive():
                break
            if not self._boss_turn():
                break
        self._end_game()

    def _start_turn(self):
        clear_screen()
        print_header(f"Turn {self.turn}")
        self.player.display_status()
        self.boss.display_status()
        print("-" * 40)

    def _player_turn(self):
        self._reset_player_state()
        process_status_effects(self.player)
        if not self.player.is_alive():
            return False

        print_slow(f"Your turn, {self.player.name}!")
        while True:
            action = self._prompt_player_action()
            if self._handle_player_action(action):
                break
        time.sleep(1.5)
        return True

    def _reset_player_state(self):
        self.player.is_defending = False
        self.player.defense = self.player_original_defense
        self.player.regenerate_mana()

    def _prompt_player_action(self):
        print("Choose your action:")
        print("1: Basic Attack")
        print("2: Defend")
        print("3: Use Ability")
        print(f"4: Use Health Potion ({self.player.potions} left)")
        return input("> ")

    def _handle_player_action(self, action):
        if action == "1":
            print_slow(f"{self.player.name} attacks!")
            self.boss.take_damage(self.player.attack, self.player.name)
            return True
        if action == "2":
            self.player.is_defending = True
            print_slow(f"{self.player.name} takes a defensive stance.")
            return True
        if action == "3":
            return self._handle_ability_choice()
        if action == "4":
            return self._use_potion()
        print_slow("Invalid action. Please choose again.")
        return False

    def _handle_ability_choice(self):
        if not self.player.abilities:
            print_slow("You have no abilities available.")
            return False
        print("Choose an ability:")
        for key, ability in self.player.abilities.items():
            print(f"{key}: {ability['name']} (Cost: {ability['cost']} Mana)")
        ability_choice = input("> ")
        if ability_choice not in self.player.abilities:
            print_slow("Invalid choice.")
            return False
        chosen_ability = self.player.abilities[ability_choice]
        if self.player.mana < chosen_ability['cost']:
            print_slow("Not enough mana!")
            time.sleep(1)
            return False
        self.player.mana -= chosen_ability['cost']
        chosen_ability['effect'](self.boss)
        return True

    def _use_potion(self):
        if self.player.potions <= 0:
            print_slow("You are out of health potions!")
            time.sleep(1)
            return False
        self.player.potions -= 1
        heal_amount = 40
        self.player.heal(heal_amount)
        print_slow(f"You used a health potion and recovered {heal_amount} HP.")
        return True

    def _boss_turn(self):
        process_status_effects(self.boss)
        if not self.boss.is_alive():
            return False
        self.boss.choose_action(self.player)
        time.sleep(2)
        self.turn += 1
        return True

    def _end_game(self):
        clear_screen()
        print_header("Battle Over")
        if self.player.is_alive():
            print_slow("Congratulations! You have defeated the Gargantuan Hydra!")
            self.player.display_status()
        else:
            print_slow("You have been defeated... The world is shrouded in darkness.")
            self.boss.display_status()

if __name__ == "__main__":
    Game().run()
