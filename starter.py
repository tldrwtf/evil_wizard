# Fk off people from class copying ideas.

import random
import time
import inspect
import sys
import re
import unicodedata


# --- Color System ---
class Colors:
    """ANSI color codes for terminal output."""

    # Basic colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

    # Bright colors
    BRIGHT_RED = "\033[91;1m"
    BRIGHT_GREEN = "\033[92;1m"
    BRIGHT_YELLOW = "\033[93;1m"
    BRIGHT_BLUE = "\033[94;1m"
    BRIGHT_PURPLE = "\033[95;1m"
    BRIGHT_CYAN = "\033[96;1m"

    # Special formatting
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"

    # Background colors
    BG_RED = "\033[101m"
    BG_GREEN = "\033[102m"
    BG_YELLOW = "\033[103m"
    BG_BLUE = "\033[104m"

    # Reset
    RESET = "\033[0m"

    @staticmethod
    def disable():
        """Disable colors (useful for Windows compatibility issues)."""
        for attr in dir(Colors):
            if not attr.startswith("_") and attr != "disable" and attr != "enable":
                setattr(Colors, attr, "")

    @staticmethod
    def enable():
        """Re-enable colors."""
        Colors.__init__()


# Enable colors for Windows terminal
if sys.platform == "win32":
    try:
        import colorama

        colorama.init()
    except ImportError:
        # If colorama isn't available, try to enable ANSI support
        import os

        os.system("color")


def colorize(text, color):
    """Apply color to text."""
    return f"{color}{text}{Colors.RESET}"


def get_class_color(class_name):
    """Get thematic color for character classes."""
    class_colors = {
        "Warrior": Colors.RED,
        "Mage": Colors.BLUE,
        "Archer": Colors.GREEN,
        "Paladin": Colors.YELLOW,
        "Rogue": Colors.PURPLE,
        "Necromancer": Colors.GRAY,
        "Monk": Colors.CYAN,
        "Barbarian": Colors.BRIGHT_RED,
        "Druid": Colors.BRIGHT_GREEN,
    }
    return class_colors.get(class_name, Colors.WHITE)


def get_damage_color(damage_type):
    """Get color for different damage types."""
    damage_colors = {
        "physical": Colors.RED,
        "fire": Colors.BRIGHT_RED,
        "ice": Colors.BRIGHT_CYAN,
        "poison": Colors.GREEN,
        "holy": Colors.BRIGHT_YELLOW,
        "dark": Colors.PURPLE,
        "healing": Colors.BRIGHT_GREEN,
    }
    return damage_colors.get(damage_type, Colors.WHITE)


# --- Utility Functions ---
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text):
    """Remove ANSI escape sequences from a string."""
    return ANSI_ESCAPE.sub("", text)


def get_display_width(text):
    """Calculate rendered width, accounting for ANSI codes and wide Unicode chars."""
    clean_text = strip_ansi(text)
    width = 0
    for char in clean_text:
        if unicodedata.combining(char) or unicodedata.category(char) == "Cf":
            continue
        if unicodedata.east_asian_width(char) in {"F", "W"}:
            width += 2
        else:
            width += 1
    return width


def pad_to_width(text, target_width):
    """Right-pad a string with spaces until it reaches the desired display width."""
    padding_needed = max(0, target_width - get_display_width(text))
    return f"{text}{' ' * padding_needed}"


def wrap_text(text, width):
    """Wrap text based on rendered width, preserving color codes."""
    if width <= 0 or get_display_width(text) <= width:
        return [text]

    words = text.split()
    if not words:
        return [text]

    lines = []
    current_line = words[0]
    for word in words[1:]:
        candidate = f"{current_line} {word}"
        if get_display_width(candidate) > width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = candidate

    lines.append(current_line)
    return lines


def print_box(title, lines, width=54):
    """Print a framed box with proper alignment for colored and emoji text."""
    inner_width = width - 2

    content_width = (
        max((get_display_width(line) for line in lines), default=0) + 1
    )  # +1 for left padding inside the box

    title_segment = f"─ {title} "
    title_width = get_display_width(title_segment)

    inner_width = max(inner_width, content_width, title_width)

    top_border = f"┌{title_segment}{'─' * max(0, inner_width - title_width)}┐"
    print(top_border, flush=True)

    if not lines:
        lines = [""]

    for line in lines:
        for segment in wrap_text(line, inner_width - 1):
            padded_line = pad_to_width(f" {segment}", inner_width)
            print(f"│{padded_line}│", flush=True)

    print(f"└{'─' * inner_width}┘", flush=True)


def clear_screen():
    """Clears the console screen by printing many newlines."""
    print("\n" * 50)


def print_slow(text, delay=0.03, color=None):
    """Prints text with a slight delay for a more dramatic effect."""
    if color:
        text = colorize(text, color)
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print(flush=True)


def print_header(title, color=Colors.BRIGHT_CYAN):
    """Prints a styled header with color and nice spacing."""
    print()  # Add space before header
    border = "=" * 50
    print(colorize(border, color), flush=True)
    print(colorize(f"{title:^50}", Colors.BOLD + color), flush=True)
    print(colorize(border, color), flush=True)
    print()  # Add space after header


def print_section_break():
    """Prints a visual break between sections."""
    print(colorize("-" * 50, Colors.GRAY), flush=True)
    print()


def print_with_spacing(text, color=None, spacing_before=0, spacing_after=1):
    """Print text with customizable spacing before and after."""
    for _ in range(spacing_before):
        print()
    if color:
        print(colorize(text, color), flush=True)
    else:
        print(text, flush=True)
    for _ in range(spacing_after):
        print()


# --- Weapon System ---


class Weapon:
    """Base class for all weapons."""

    def __init__(
        self, name, attack_bonus, defense_bonus, crit_chance, special_effect=None
    ):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.crit_chance = crit_chance  # Additional crit chance beyond base 10%
        self.special_effect = special_effect  # Function to call on attack

    def apply_special_effect(self, wielder, target):
        """Apply the weapon's special effect if it has one."""
        if self.special_effect:
            self.special_effect(wielder, target)


# --- Character and Boss Blueprints (Classes) ---


class Character:
    """Base class for all characters, including the player."""

    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_attack = attack
        self.attack = attack
        self.base_defense = defense
        self.defense = defense
        self.abilities = {}
        self.is_defending = False
        self.status_effects = {}  # e.g., {'poison': 3} for 3 turns of poison
        self.weapon = None

    def equip_weapon(self, weapon):
        """Equip a weapon and apply its bonuses."""
        self.weapon = weapon
        self.attack = self.base_attack + weapon.attack_bonus
        self.defense = max(0, self.base_defense + weapon.defense_bonus)

    def get_total_crit_chance(self):
        """Calculate total critical hit chance."""
        base_crit = 0.10  # 10% base
        weapon_crit = self.weapon.crit_chance if self.weapon else 0
        return base_crit + weapon_crit

    def is_alive(self):
        """Check if the character's HP is above 0."""
        return self.hp > 0

    def take_damage(self, damage, attacker_name="An opponent", attacker=None):
        """Calculates and applies damage to the character, with a chance for a critical hit."""
        # Critical Hit Chance
        crit_chance = attacker.get_total_crit_chance() if attacker else 0.10
        is_critical = random.random() < crit_chance
        if is_critical:
            damage = int(damage * 1.5)
            print_slow(
                f"*** CRITICAL HIT from {attacker_name}! ***",
                color=Colors.BRIGHT_RED + Colors.BLINK,
            )

        # Apply weapon special effects if attacker has a weapon
        if attacker and attacker.weapon:
            attacker.weapon.apply_special_effect(attacker, self)

        actual_defense = self.defense * 2 if self.is_defending else self.defense
        damage_taken = max(0, damage - actual_defense)
        self.hp -= damage_taken
        self.hp = max(0, self.hp)  # Can't have negative HP
        if self.is_defending:
            print_slow(
                f"{self.name} defends and mitigates some damage!", color=Colors.BLUE
            )
        print_slow(f"{self.name} takes {damage_taken} damage!", color=Colors.RED)
        return damage_taken

    def heal(self, amount):
        """Heals the character."""
        self.hp += amount
        self.hp = min(self.max_hp, self.hp)
        print_slow(f"{self.name} heals for {amount} HP!", color=Colors.BRIGHT_GREEN)

    def display_status(self):
        """Shows the character's current status with colored HP bars and nice formatting."""
        # Calculate HP percentage for color coding
        hp_percentage = self.hp / self.max_hp
        if hp_percentage > 0.6:
            hp_color = Colors.GREEN
        elif hp_percentage > 0.3:
            hp_color = Colors.YELLOW
        else:
            hp_color = Colors.RED

        # Create colored HP bar with better visual design
        filled_blocks = int((self.hp / self.max_hp) * 25)
        empty_blocks = 25 - filled_blocks
        hp_bar = f"[{colorize('█' * filled_blocks, hp_color)}{colorize('░' * empty_blocks, Colors.GRAY)}]"

        name_color = get_class_color(getattr(self, "role", "default"))

        lines = [
            f"HP: {colorize(f'{self.hp:3d}', hp_color)}/{self.max_hp:<3d} {hp_bar}"
        ]

        if self.status_effects:
            effects = []
            for effect, turns in self.status_effects.items():
                if effect == "poison":
                    effect_color = Colors.GREEN
                elif effect == "stunned":
                    effect_color = Colors.YELLOW
                elif effect == "frozen":
                    effect_color = Colors.CYAN
                elif effect == "burning":
                    effect_color = Colors.RED
                else:
                    effect_color = Colors.PURPLE
                effects.append(
                    f"{colorize(effect.capitalize(), effect_color)} ({turns})"
                )
            lines.append(f"Status: {', '.join(effects)}")

        print_box(colorize(self.name, Colors.BOLD + name_color), lines)


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
        """Shows the player's current status with enhanced formatting including mana and potions."""
        # Calculate HP percentage for color coding
        hp_percentage = self.hp / self.max_hp
        if hp_percentage > 0.6:
            hp_color = Colors.GREEN
        elif hp_percentage > 0.3:
            hp_color = Colors.YELLOW
        else:
            hp_color = Colors.RED

        # Create colored HP bar with better visual design
        filled_blocks = int((self.hp / self.max_hp) * 25)
        empty_blocks = 25 - filled_blocks
        hp_bar = f"[{colorize('█' * filled_blocks, hp_color)}{colorize('░' * empty_blocks, Colors.GRAY)}]"

        # Colored mana bar
        mana_percentage = self.mana / self.max_mana
        if mana_percentage > 0.6:
            mana_color = Colors.BRIGHT_BLUE
        elif mana_percentage > 0.3:
            mana_color = Colors.BLUE
        else:
            mana_color = Colors.PURPLE

        filled_mana = int((self.mana / self.max_mana) * 15)
        empty_mana = 15 - filled_mana
        mana_bar = f"[{colorize('▓' * filled_mana, mana_color)}{colorize('░' * empty_mana, Colors.GRAY)}]"

        # Colored potion count
        potion_color = Colors.GREEN if self.potions > 0 else Colors.RED

        name_color = get_class_color(self.role)

        potion_icons = "🧪" * self.potions
        potions_line = (
            f"Potions: {colorize(str(self.potions), potion_color)} {potion_icons}"
        ).rstrip()

        lines = [
            f"HP: {colorize(f'{self.hp:3d}', hp_color)}/{self.max_hp:<3d} {hp_bar}",
            f"MP: {colorize(f'{self.mana:3d}', mana_color)}/{self.max_mana:<3d} {mana_bar}",
            potions_line,
        ]

        if self.status_effects:
            effects = []
            for effect, turns in self.status_effects.items():
                if effect == "poison":
                    effect_color = Colors.GREEN
                elif effect == "stunned":
                    effect_color = Colors.YELLOW
                elif effect == "frozen":
                    effect_color = Colors.CYAN
                elif effect == "burning":
                    effect_color = Colors.RED
                else:
                    effect_color = Colors.PURPLE
                effects.append(
                    f"{colorize(effect.capitalize(), effect_color)} ({turns})"
                )
            lines.append(f"Status: {', '.join(effects)}")

        print_box(
            colorize(f"{self.name} ({self.role})", Colors.BOLD + name_color), lines
        )

    def regenerate_mana(self):
        """Regenerate a small amount of mana each turn."""
        mana_regen = 5
        self.mana = min(self.max_mana, self.mana + mana_regen)

    # --- Centralized Damage Calculation Methods ---
    def deal_basic_damage(self, target, multiplier=1.0, bonus_min=0, bonus_max=0):
        """Deal basic attack damage with optional multiplier and random bonus."""
        base_damage = int(self.attack * multiplier)
        if bonus_min or bonus_max:
            base_damage += random.randint(bonus_min, bonus_max)
        target.take_damage(base_damage, self.name, self)

    def deal_enhanced_damage(self, target, multiplier=1.5):
        """Deal enhanced damage (common 1.5x multiplier pattern)."""
        damage = int(self.attack * multiplier)
        target.take_damage(damage, self.name, self)

    def deal_random_bonus_damage(self, target, min_bonus=8, max_bonus=15):
        """Deal attack + random bonus damage (common pattern)."""
        damage = self.attack + random.randint(min_bonus, max_bonus)
        target.take_damage(damage, self.name, self)

    def apply_status_effect(self, target, effect_name, duration, message=None):
        """Apply a status effect to target with optional message."""
        if effect_name not in target.status_effects:
            target.status_effects[effect_name] = duration
            if message:
                # Color the message based on effect type
                if "poison" in effect_name.lower():
                    print_slow(message, color=Colors.GREEN)
                elif "burn" in effect_name.lower() or "fire" in effect_name.lower():
                    print_slow(message, color=Colors.RED)
                elif "freeze" in effect_name.lower() or "frost" in effect_name.lower():
                    print_slow(message, color=Colors.CYAN)
                elif "stun" in effect_name.lower():
                    print_slow(message, color=Colors.YELLOW)
                else:
                    print_slow(message, color=Colors.PURPLE)
            else:
                # Default colored message
                if effect_name == "poison":
                    color = Colors.GREEN
                elif effect_name == "burning":
                    color = Colors.RED
                elif effect_name == "frozen":
                    color = Colors.CYAN
                elif effect_name == "stunned":
                    color = Colors.YELLOW
                else:
                    color = Colors.PURPLE
                print_slow(f"{target.name} is affected by {effect_name}!", color=color)

    def _initialize_abilities(self):
        """Sets abilities based on the player's role."""
        if self.role == "Warrior":
            self.abilities = {
                "1": {"name": "Power Strike", "cost": 10, "effect": self._power_strike},
                "2": {"name": "Shield Wall", "cost": 5, "effect": self._shield_wall},
                "3": {
                    "name": "Reckless Swing",
                    "cost": 20,
                    "effect": self._reckless_swing,
                },
            }
        elif self.role == "Mage":
            self.abilities = {
                "1": {"name": "Fireball", "cost": 15, "effect": self._fireball},
                "2": {"name": "Heal", "cost": 20, "effect": self._heal_spell},
                "3": {
                    "name": "Arcane Shield",
                    "cost": 25,
                    "effect": self._arcane_shield,
                },
            }
            self.base_attack = 5  # Mages have low base attack
        elif self.role == "Archer":
            self.abilities = {
                "1": {"name": "Aimed Shot", "cost": 10, "effect": self._aimed_shot},
                "2": {"name": "Poison Arrow", "cost": 15, "effect": self._poison_arrow},
                "3": {"name": "Double Shot", "cost": 20, "effect": self._double_shot},
            }
        elif self.role == "Paladin":
            self.abilities = {
                "1": {
                    "name": "Holy Strike",
                    "cost": 15,
                    "effect": self._paladin_holy_strike,
                },
                "2": {
                    "name": "Divine Shield",
                    "cost": 15,
                    "effect": self._divine_shield,
                },
                "3": {"name": "Lay on Hands", "cost": 30, "effect": self._lay_on_hands},
            }
        elif self.role == "Rogue":
            self.abilities = {
                "1": {"name": "Backstab", "cost": 15, "effect": self._rogue_backstab},
                "2": {"name": "Evasion", "cost": 10, "effect": self._evasion},
                "3": {"name": "Flurry", "cost": 25, "effect": self._flurry},
            }
        elif self.role == "Necromancer":
            self.abilities = {
                "1": {"name": "Drain Life", "cost": 20, "effect": self._drain_life},
                "2": {"name": "Bone Armor", "cost": 15, "effect": self._bone_armor},
                "3": {"name": "Curse", "cost": 25, "effect": self._curse},
            }
        elif self.role == "Monk":
            self.abilities = {
                "1": {"name": "Chi Strike", "cost": 15, "effect": self._chi_strike},
                "2": {"name": "Inner Peace", "cost": 10, "effect": self._inner_peace},
                "3": {
                    "name": "Flurry of Blows",
                    "cost": 20,
                    "effect": self._flurry_of_blows,
                },
            }
        elif self.role == "Barbarian":
            self.abilities = {
                "1": {"name": "Rage", "cost": 10, "effect": self._rage},
                "2": {"name": "Intimidate", "cost": 5, "effect": self._intimidate},
                "3": {
                    "name": "Berserker Strike",
                    "cost": 25,
                    "effect": self._berserker_strike,
                },
            }
        elif self.role == "Druid":
            self.abilities = {
                "1": {
                    "name": "Nature's Wrath",
                    "cost": 15,
                    "effect": self._natures_wrath,
                },
                "2": {"name": "Wild Shape", "cost": 20, "effect": self._wild_shape},
                "3": {
                    "name": "Healing Spring",
                    "cost": 25,
                    "effect": self._healing_spring,
                },
            }

    # --- Warrior Abilities ---
    def _power_strike(self, target):
        print_slow(f"{self.name} uses Power Strike!", color=Colors.RED)
        self.deal_enhanced_damage(target, 1.5)

    def _shield_wall(self):
        print_slow(
            f"{self.name} raises their shield, preparing for the next attack!",
            color=Colors.BLUE,
        )
        self.is_defending = True  # Handled in the main game loop

    def _reckless_swing(self, target):
        print_slow(
            f"{self.name} throws caution to the wind with a Reckless Swing!",
            color=Colors.BRIGHT_RED,
        )
        self.defense -= 3
        print_slow(
            f"{self.name}'s defense is temporarily lowered!", color=Colors.YELLOW
        )
        self.deal_basic_damage(target, 2.0)

    # --- Mage Abilities ---
    def _fireball(self, target):
        print_slow(f"{self.name} casts Fireball!", color=Colors.BRIGHT_RED)
        damage = random.randint(15, 25)
        target.take_damage(damage, self.name, self)

    def _heal_spell(self):
        print_slow(f"{self.name} casts a healing spell!", color=Colors.BRIGHT_GREEN)
        heal_amount = random.randint(20, 30)
        self.heal(heal_amount)

    def _arcane_shield(self):
        print_slow(f"{self.name} conjures an Arcane Shield!", color=Colors.BRIGHT_BLUE)
        # For simplicity, we'll just boost defense temporarily
        self.defense += 5
        print_slow(f"{self.name}'s defense is temporarily boosted!", color=Colors.CYAN)

    # --- Archer Abilities ---
    def _aimed_shot(self, target):
        print_slow(f"{self.name} takes careful aim for an Aimed Shot!")
        if random.random() > 0.15:  # 85% chance to hit
            self.deal_random_bonus_damage(target, 8, 15)
        else:
            print_slow(f"{self.name}'s arrow misses!")

    def _poison_arrow(self, target):
        print_slow(f"{self.name} fires a Poison Arrow!")
        target.take_damage(self.attack, self.name, self)
        self.apply_status_effect(
            target, "poison", 3, f"{target.name} has been poisoned!"
        )

    def _double_shot(self, target):
        print_slow(f"{self.name} fires two arrows in quick succession!")
        target.take_damage(self.attack, self.name, self)
        time.sleep(0.5)
        target.take_damage(self.attack, self.name, self)

    # --- Paladin Abilities ---
    def _paladin_holy_strike(self, target):
        print_slow(
            f"{self.name} delivers a radiant Holy Strike!", color=Colors.BRIGHT_YELLOW
        )
        self.deal_random_bonus_damage(target, 10, 18)

    def _divine_shield(self):
        print_slow(
            f"{self.name} is blessed with a Divine Shield!", color=Colors.BRIGHT_YELLOW
        )
        self.is_defending = True
        self.defense += 6
        print_slow(f"{self.name}'s defense surges temporarily!", color=Colors.YELLOW)

    def _lay_on_hands(self):
        print_slow(
            f"{self.name} uses Lay on Hands to heal wounds!", color=Colors.BRIGHT_GREEN
        )
        heal_amount = random.randint(25, 35)
        self.heal(heal_amount)

    # --- Rogue Abilities ---
    def _rogue_backstab(self, target):
        print_slow(f"{self.name} attempts a deadly Backstab!")
        if random.random() < 0.2:
            print_slow(f"{self.name} misses the mark!")
            return
        self.deal_basic_damage(target, 1.6, 5, 10)

    def _evasion(self):
        print_slow(f"{self.name} focuses on Evasion, ready to slip past attacks!")
        self.is_defending = True
        self.defense += 3
        print_slow(f"{self.name}'s agility increases defense temporarily!")

    def _flurry(self, target):
        print_slow(f"{self.name} unleashes a Flurry of strikes!")
        for _ in range(3):
            target.take_damage(max(1, self.attack - 2), self.name, self)
            time.sleep(0.3)

    # --- Necromancer Abilities ---
    def _drain_life(self, target):
        print_slow(f"{self.name} drains the life force from {target.name}!")
        damage = random.randint(10, 18)
        actual_damage = target.take_damage(damage, self.name, self)
        heal_amount = actual_damage // 2
        self.heal(heal_amount)
        print_slow(f"{self.name} absorbs {heal_amount} HP!")

    def _bone_armor(self):
        print_slow(f"{self.name} conjures protective bone armor!")
        self.defense += 8
        print_slow(f"{self.name}'s defense is significantly boosted!")

    def _curse(self, target):
        print_slow(f"{self.name} places a dark curse on {target.name}!")
        self.apply_status_effect(
            target, "cursed", 4, f"{target.name} feels weakened by the curse!"
        )
        target.attack = max(1, target.attack - 5)

    # --- Monk Abilities ---
    def _chi_strike(self, target):
        print_slow(f"{self.name} focuses chi energy into a powerful strike!")
        self.deal_random_bonus_damage(target, 8, 15)
        # Chi strike restores some mana
        self.mana = min(self.max_mana, self.mana + 5)
        print_slow(f"{self.name} regains 5 mana through meditation!")

    def _inner_peace(self):
        print_slow(f"{self.name} achieves inner peace, restoring body and mind!")
        heal_amount = random.randint(15, 25)
        mana_restore = random.randint(10, 20)
        self.heal(heal_amount)
        self.mana = min(self.max_mana, self.mana + mana_restore)
        print_slow(f"{self.name} restores {mana_restore} mana!")

    def _flurry_of_blows(self, target):
        print_slow(f"{self.name} unleashes a disciplined flurry of blows!")
        for i in range(4):
            damage = max(1, self.attack - 3 + i)  # Each hit gets slightly stronger
            target.take_damage(damage, self.name, self)
            time.sleep(0.2)

    # --- Barbarian Abilities ---
    def _rage(self):
        print_slow(f"{self.name} enters a berserker RAGE!")
        self.attack += 8
        self.defense -= 2  # Trade defense for offense
        print_slow(f"{self.name}'s attack increases but defense drops!")

    def _intimidate(self, target):
        print_slow(f"{self.name} lets out a terrifying war cry!")
        target.attack = max(1, target.attack - 4)
        self.apply_status_effect(
            target,
            "intimidated",
            3,
            f"{target.name} is intimidated and deals less damage!",
        )

    def _berserker_strike(self, target):
        print_slow(f"{self.name} strikes with wild, uncontrolled fury!")
        # High damage but chance to miss
        if random.random() > 0.25:  # 75% chance to hit
            self.deal_basic_damage(target, 2.0, 5, 15)
        else:
            print_slow(f"{self.name}'s wild swing misses completely!")

    # --- Druid Abilities ---
    def _natures_wrath(self, target):
        print_slow(f"{self.name} calls upon nature's wrath!")
        # Random nature effect
        effects = ["thorns", "lightning", "earthquake"]
        effect = random.choice(effects)
        if effect == "thorns":
            print_slow("Thorny vines erupt from the ground!")
            damage = random.randint(12, 20)
            target.take_damage(damage, "Nature", self)
            target.status_effects["entangled"] = 2
        elif effect == "lightning":
            print_slow("Lightning strikes from above!")
            damage = random.randint(15, 25)
            target.take_damage(damage, "Lightning", self)
        else:  # earthquake
            print_slow("The ground shakes violently!")
            damage = random.randint(10, 18)
            target.take_damage(damage, "Earthquake", self)
            target.defense = max(1, target.defense - 3)

    def _wild_shape(self):
        print_slow(f"{self.name} transforms into a powerful bear!")
        self.attack += 6
        self.defense += 4
        self.hp = min(self.max_hp, self.hp + 15)
        print_slow(f"{self.name}'s combat stats increase in bear form!")

    def _healing_spring(self):
        print_slow(f"{self.name} creates a magical healing spring!")
        heal_amount = random.randint(30, 45)
        self.heal(heal_amount)
        # Remove negative status effects
        if "poison" in self.status_effects:
            del self.status_effects["poison"]
            print_slow(f"{self.name} is cleansed of poison!")
        if "cursed" in self.status_effects:
            del self.status_effects["cursed"]
            print_slow(f"{self.name} is freed from the curse!")


# --- Weapon Definitions and Special Effects ---


def vampiric_effect(wielder, target):
    """Vampiric weapons heal the wielder."""
    if random.random() < 0.3:  # 30% chance
        heal_amount = 3
        wielder.heal(heal_amount)
        print_slow(
            f"{wielder.name}'s weapon drains life, healing for {heal_amount} HP!",
            color=Colors.PURPLE,
        )


def burning_effect(wielder, target):
    """Burning weapons can set enemies on fire."""
    if random.random() < 0.25:  # 25% chance
        if "burning" not in target.status_effects:
            target.status_effects["burning"] = 3
            print_slow(f"{target.name} catches fire!", color=Colors.BRIGHT_RED)


def frost_effect(wielder, target):
    """Frost weapons can slow enemies."""
    if random.random() < 0.30:  # 30% chance
        target.attack = max(1, target.attack - 2)
        print_slow(
            f"{target.name} is chilled, reducing their attack!",
            color=Colors.BRIGHT_CYAN,
        )


def poison_effect(wielder, target):
    """Poison weapons can poison enemies."""
    if random.random() < 0.35:  # 35% chance
        if "poison" not in target.status_effects:
            target.status_effects["poison"] = 2
            print_slow(f"{target.name} is poisoned by the weapon!", color=Colors.GREEN)


def stunning_effect(wielder, target):
    """Stunning weapons can stun enemies."""
    if random.random() < 0.15:  # 15% chance
        target.status_effects["stunned"] = 1
        print_slow(
            f"{target.name} is stunned and will lose their next turn!",
            color=Colors.YELLOW,
        )


def blessed_effect(wielder, target):
    """Blessed weapons provide protection."""
    if random.random() < 0.20:  # 20% chance
        wielder.defense += 2
        print_slow(
            f"{wielder.name} is blessed with divine protection!",
            color=Colors.BRIGHT_YELLOW,
        )


# --- Weapon Collections by Class ---

WARRIOR_WEAPONS = {
    "1": Weapon("Iron Sword", 5, 2, 0.05, None),
    "2": Weapon("Vampiric Blade", 4, 1, 0.10, vampiric_effect),
    "3": Weapon("Flame Sword", 6, 0, 0.08, burning_effect),
    "4": Weapon("Defender's Blade", 3, 5, 0.02, None),
}

MAGE_WEAPONS = {
    "1": Weapon("Wooden Staff", 2, 1, 0.03, None),
    "2": Weapon("Staff of Frost", 3, 0, 0.12, frost_effect),
    "3": Weapon("Arcane Crystal Staff", 5, 2, 0.15, None),
    "4": Weapon("Staff of Healing", 1, 3, 0.05, blessed_effect),
}

ARCHER_WEAPONS = {
    "1": Weapon("Hunter's Bow", 4, 1, 0.15, None),
    "2": Weapon("Poison Bow", 3, 0, 0.12, poison_effect),
    "3": Weapon("Elven Longbow", 6, 1, 0.20, None),
    "4": Weapon("Crossbow of Precision", 5, 2, 0.25, None),
}

PALADIN_WEAPONS = {
    "1": Weapon("Holy Mace", 4, 3, 0.08, None),
    "2": Weapon("Blessed Hammer", 5, 4, 0.10, blessed_effect),
    "3": Weapon("Divine Sword", 6, 2, 0.12, None),
    "4": Weapon("Shield of Faith", 2, 7, 0.05, blessed_effect),
}

ROGUE_WEAPONS = {
    "1": Weapon("Steel Dagger", 3, 0, 0.20, None),
    "2": Weapon("Poisoned Blade", 4, 0, 0.18, poison_effect),
    "3": Weapon("Shadow Blade", 5, 1, 0.25, None),
    "4": Weapon("Stunning Dagger", 3, 0, 0.15, stunning_effect),
}

NECROMANCER_WEAPONS = {
    "1": Weapon("Bone Wand", 3, 1, 0.08, None),
    "2": Weapon("Soul Reaper", 4, 0, 0.12, vampiric_effect),
    "3": Weapon("Cursed Staff", 5, 1, 0.10, None),
    "4": Weapon("Death's Touch", 6, 0, 0.15, vampiric_effect),
}

MONK_WEAPONS = {
    "1": Weapon("Quarterstaff", 3, 2, 0.10, None),
    "2": Weapon("Iron Knuckles", 4, 1, 0.15, stunning_effect),
    "3": Weapon("Jade Staff", 3, 3, 0.12, blessed_effect),
    "4": Weapon("Fists of Fury", 5, 0, 0.20, None),
}

BARBARIAN_WEAPONS = {
    "1": Weapon("Battle Axe", 6, 0, 0.12, None),
    "2": Weapon("Berserker's Maul", 8, -1, 0.15, None),
    "3": Weapon("Tribal Club", 5, 1, 0.10, stunning_effect),
    "4": Weapon("Rage Blade", 7, 0, 0.18, burning_effect),
}

DRUID_WEAPONS = {
    "1": Weapon("Nature's Staff", 3, 2, 0.08, None),
    "2": Weapon("Thorn Whip", 4, 1, 0.10, poison_effect),
    "3": Weapon("Moonstone Staff", 4, 3, 0.12, blessed_effect),
    "4": Weapon("Storm Branch", 5, 1, 0.15, frost_effect),
}

WEAPON_COLLECTIONS = {
    "Warrior": WARRIOR_WEAPONS,
    "Mage": MAGE_WEAPONS,
    "Archer": ARCHER_WEAPONS,
    "Paladin": PALADIN_WEAPONS,
    "Rogue": ROGUE_WEAPONS,
    "Necromancer": NECROMANCER_WEAPONS,
    "Monk": MONK_WEAPONS,
    "Barbarian": BARBARIAN_WEAPONS,
    "Druid": DRUID_WEAPONS,
}


class Boss(Character):
    """The main antagonist."""

    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)
        self.is_enraged = False
        self.abilities = {
            self._stomp: 0.5,  # Ability function: probability
            self._dark_breath: 0.3,
            self._frightening_roar: 0.2,
        }

    def choose_action(self, target):
        """Boss AI: Chooses an action based on probabilities and enrage state."""
        print_section_break()
        print_with_spacing(
            f"🐉 {self.name}'s turn...", Colors.BRIGHT_RED, spacing_before=1
        )
        time.sleep(1)

        # Enrage mechanic
        if self.hp < self.max_hp * 0.3 and not self.is_enraged:
            self.is_enraged = True
            self.attack += 5
            print()
            print_slow(
                f"💀 {self.name} becomes ENRAGED! Its attack power has increased!",
                color=Colors.BRIGHT_RED + Colors.BLINK,
            )
            print()
            time.sleep(1)

        abilities = list(self.abilities.keys())
        weights = list(self.abilities.values())
        chosen_ability = random.choices(abilities, weights, k=1)[0]

        chosen_ability(target)

    # --- Boss Abilities ---
    def _stomp(self, target):
        print_slow(
            f"{self.name} rears back and STOMPS the ground!", color=Colors.BRIGHT_RED
        )
        damage = self.attack + random.randint(-3, 5)
        target.take_damage(damage, self.name, self)

    def _dark_breath(self, target):
        print_slow(
            f"{self.name} unleashes a torrent of dark energy!", color=Colors.PURPLE
        )
        damage = self.attack + random.randint(5, 10)
        target.take_damage(damage, self.name, self)

    def _frightening_roar(self, target):
        print_slow(f"{self.name} lets out a Frightening Roar!", color=Colors.GRAY)
        print_slow(f"{target.name}'s defense is lowered!", color=Colors.YELLOW)
        target.defense = max(1, target.defense - 2)  # Lower defense, min of 1


# --- Game Logic ---


def choose_class():
    """Lets the player select their character class."""
    print_header("Choose Your Class")

    # Display classes with their themed colors in a nice formatted table
    classes = [
        (
            "1",
            "Warrior",
            Colors.RED,
            "A sturdy fighter with high defense and reliable damage.",
        ),
        (
            "2",
            "Mage",
            Colors.BLUE,
            "A powerful spellcaster with high damage and healing abilities.",
        ),
        (
            "3",
            "Archer",
            Colors.GREEN,
            "A nimble marksman who uses precision and status effects.",
        ),
        (
            "4",
            "Paladin",
            Colors.YELLOW,
            "A holy knight with strong defenses and supportive magic.",
        ),
        (
            "5",
            "Rogue",
            Colors.PURPLE,
            "A swift striker specializing in burst damage and evasion.",
        ),
        (
            "6",
            "Necromancer",
            Colors.GRAY,
            "A dark mage who drains life and curses enemies.",
        ),
        (
            "7",
            "Monk",
            Colors.CYAN,
            "A martial artist balancing offense and spiritual power.",
        ),
        (
            "8",
            "Barbarian",
            Colors.BRIGHT_RED,
            "A fierce warrior trading defense for overwhelming offense.",
        ),
        (
            "9",
            "Druid",
            Colors.BRIGHT_GREEN,
            "A nature wielder with versatile elemental abilities.",
        ),
    ]

    class_lines = []
    for num, name, color, desc in classes:
        name_block = colorize(name, Colors.BOLD + color)
        class_lines.append(f"{num}: {name_block} - {desc}")

    print_box(colorize("Available Classes", Colors.BOLD), class_lines, width=90)
    print()

    choice = ""
    while choice not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        choice = input("Enter your choice (1-9): ")

    player_name = input("Enter your hero's name: ")
    if not player_name:
        player_name = "Hero"

    # Create player based on choice
    if choice == "1":
        player = Player(player_name, 120, 12, 8, 50, "Warrior")
    elif choice == "2":
        player = Player(player_name, 80, 10, 4, 100, "Mage")
    elif choice == "3":
        player = Player(player_name, 100, 15, 6, 70, "Archer")
    elif choice == "4":
        player = Player(player_name, 130, 11, 10, 80, "Paladin")
    elif choice == "5":
        player = Player(player_name, 90, 17, 4, 60, "Rogue")
    elif choice == "6":
        player = Player(player_name, 85, 13, 5, 90, "Necromancer")
    elif choice == "7":
        player = Player(player_name, 110, 14, 7, 75, "Monk")
    elif choice == "8":
        player = Player(player_name, 140, 18, 3, 40, "Barbarian")
    elif choice == "9":
        player = Player(player_name, 105, 12, 6, 85, "Druid")

    # Now let player choose weapon
    choose_weapon(player)
    return player


def choose_weapon(player):
    """Lets the player choose their weapon with enhanced display."""
    class_color = get_class_color(player.role)
    print_header(f"Choose Your {player.role} Weapon", class_color)

    weapons = WEAPON_COLLECTIONS[player.role]

    weapon_lines = []
    for key, weapon in weapons.items():
        special_text = ""
        if weapon.special_effect:
            effect_name = getattr(
                weapon.special_effect,
                "__name__",
                str(type(weapon.special_effect).__name__),
            )
            # Color special effects
            if "vampiric" in effect_name:
                special_text = colorize("Vampiric", Colors.PURPLE)
            elif "poison" in effect_name:
                special_text = colorize("Poison", Colors.GREEN)
            elif "frost" in effect_name:
                special_text = colorize("Frost", Colors.CYAN)
            elif "burning" in effect_name:
                special_text = colorize("Burning", Colors.RED)
            elif "blessed" in effect_name:
                special_text = colorize("Blessed", Colors.YELLOW)
            elif "stunning" in effect_name:
                special_text = colorize("Stunning", Colors.BRIGHT_YELLOW)
            else:
                special_text = colorize(effect_name, Colors.WHITE)

        attack_text = colorize(f"ATK+{weapon.attack_bonus}", Colors.RED)
        defense_text = colorize(f"DEF+{weapon.defense_bonus}", Colors.BLUE)
        crit_text = colorize(f"CRIT+{weapon.crit_chance*100:.0f}%", Colors.YELLOW)

        name_block = pad_to_width(colorize(weapon.name, Colors.BOLD + class_color), 22)
        stats_segments = f"{attack_text}  {defense_text}  {crit_text}"
        if special_text:
            stats_segments = f"{stats_segments}  [{special_text}]"

        line = f"{key}: {name_block}{stats_segments}"
        weapon_lines.append(line)

    width_hint = max((get_display_width(line) for line in weapon_lines), default=0)
    frame_width = max(70, width_hint + 3)

    print_box(
        colorize("Available Weapons", Colors.BOLD),
        weapon_lines,
        width=frame_width + 2,
    )
    print()

    choice = ""
    while choice not in weapons.keys():
        choice = input(f"Choose weapon (1-{len(weapons)}): ").strip()

    chosen_weapon = weapons[choice]
    player.equip_weapon(chosen_weapon)

    print()
    print_slow(f"⚔️  {player.name} equips the {chosen_weapon.name}!", color=class_color)
    print_section_break()
    time.sleep(1)


def process_status_effects(character):
    """Applies and removes status effects at the start of a turn."""
    effects_to_remove = []

    if "poison" in character.status_effects:
        poison_damage = 5
        print_slow(
            f"{character.name} takes {poison_damage} damage from poison!",
            color=Colors.GREEN,
        )
        character.hp -= poison_damage
        character.hp = max(0, character.hp)
        character.status_effects["poison"] -= 1
        if character.status_effects["poison"] <= 0:
            print_slow(f"{character.name} is no longer poisoned.", color=Colors.GREEN)
            effects_to_remove.append("poison")

    if "burning" in character.status_effects:
        burn_damage = 4
        print_slow(
            f"{character.name} takes {burn_damage} damage from burning!",
            color=Colors.BRIGHT_RED,
        )
        character.hp -= burn_damage
        character.hp = max(0, character.hp)
        character.status_effects["burning"] -= 1
        if character.status_effects["burning"] <= 0:
            print_slow(
                f"{character.name} is no longer burning.", color=Colors.BRIGHT_RED
            )
            effects_to_remove.append("burning")

    if "stunned" in character.status_effects:
        print_slow(f"{character.name} is stunned and loses their turn!")
        character.status_effects["stunned"] -= 1
        if character.status_effects["stunned"] <= 0:
            effects_to_remove.append("stunned")
        # Clean up effects and return True to skip turn
        for effect in effects_to_remove:
            del character.status_effects[effect]
        return True

    if "cursed" in character.status_effects:
        character.status_effects["cursed"] -= 1
        if character.status_effects["cursed"] <= 0:
            print_slow(f"{character.name} is no longer cursed.")
            character.attack += 5  # Restore attack
            effects_to_remove.append("cursed")

    if "intimidated" in character.status_effects:
        character.status_effects["intimidated"] -= 1
        if character.status_effects["intimidated"] <= 0:
            print_slow(f"{character.name} is no longer intimidated.")
            character.attack += 4  # Restore attack
            effects_to_remove.append("intimidated")

    if "entangled" in character.status_effects:
        print_slow(f"{character.name} is entangled and struggles to move!")
        character.status_effects["entangled"] -= 1
        if character.status_effects["entangled"] <= 0:
            print_slow(f"{character.name} breaks free from the entanglement.")
            effects_to_remove.append("entangled")

    for effect in effects_to_remove:
        del character.status_effects[effect]

    return False  # Normal turn


class Game:
    """Coordinates the flow of the boss battle."""

    def __init__(self):
        self.player = None
        self.boss = None
        self.player_original_defense = 0
        self.turn = 1

    def setup(self):
        clear_screen()
        print_header("🐉 BOSS BATTLE 🐉", Colors.BRIGHT_RED)

        print_with_spacing(
            "⚠️  A fearsome beast emerges from the shadows!",
            Colors.BRIGHT_RED,
            spacing_before=1,
            spacing_after=2,
        )
        time.sleep(1.5)

        self.player = choose_class()

        print_header("🐉 THE GARGANTUAN HYDRA AWAKENS 🐉", Colors.BRIGHT_RED)
        print_with_spacing(
            "A massive three-headed dragon blocks your path!",
            Colors.GRAY,
            spacing_before=1,
        )
        print_with_spacing(
            "Prepare for the battle of your life!",
            Colors.BRIGHT_YELLOW,
            spacing_after=2,
        )

        self.boss = Boss("Gargantuan Hydra", 250, 15, 5)
        # Store base defense (before weapon bonuses)
        self.player_original_defense = self.player.base_defense

        print_with_spacing(
            "🎮 Battle begins!", Colors.BRIGHT_CYAN, spacing_before=1, spacing_after=1
        )
        time.sleep(2)

    def run(self):
        self.setup()
        while self.player.is_alive() and self.boss.is_alive():
            self._reset_player_state()
            if not self._player_turn():
                break
            if not self._boss_turn():
                break
        self._end_game()

    def _player_turn(self):
        clear_screen()

        # Display current status for both player and boss
        print_header(f"Turn {self.turn}", Colors.CYAN)
        print()  # Add some spacing
        self.player.display_status()
        print()  # Add spacing between player and boss
        self.boss.display_status()
        print_section_break()

        skip_turn = process_status_effects(self.player)
        if skip_turn:  # Player is stunned
            print_slow(
                f"💫 {self.player.name} is stunned and loses their turn!",
                color=Colors.YELLOW,
            )
            time.sleep(2)
            return True
        if not self.player.is_alive():
            return False

        print_with_spacing(
            f"⚔️  Your turn, {self.player.name}!",
            get_class_color(self.player.role),
            spacing_before=1,
        )

        while True:
            action = self._prompt_player_action()
            if self._handle_player_action(action):
                break
        time.sleep(1.5)
        return True

    def _reset_player_state(self):
        self.player.is_defending = False
        # Reset defense to base + weapon bonus
        self.player.defense = self.player.base_defense + (
            self.player.weapon.defense_bonus if self.player.weapon else 0
        )
        self.player.regenerate_mana()

    def _prompt_player_action(self):
        print()
        potion_color = Colors.GREEN if self.player.potions > 0 else Colors.GRAY
        potion_text = colorize(
            f"🧪 Use Health Potion ({self.player.potions} left)", potion_color
        )

        options = [
            f"1: {colorize('⚔️  Basic Attack', Colors.RED)}",
            f"2: {colorize('🛡️  Defend', Colors.BLUE)}",
            f"3: {colorize('✨ Use Ability', Colors.PURPLE)}",
            f"4: {potion_text}",
        ]

        print_box(colorize("Combat Actions", Colors.BOLD), options)

        action = input(f"\n{colorize('>', Colors.BOLD)} ").strip()
        return action

    def _handle_player_action(self, action):
        if action == "1":
            player_color = get_class_color(self.player.role)
            print_slow(f"{self.player.name} attacks!", color=player_color)
            self.boss.take_damage(self.player.attack, self.player.name, self.player)
            return True
        elif action == "2":
            self.player.is_defending = True
            print_slow(
                f"{self.player.name} takes a defensive stance.", color=Colors.BLUE
            )
            return True
        elif action == "3":
            return self._handle_ability_choice()
        elif action == "4":
            return self._use_potion()
        print_slow("Invalid action. Please choose again.", color=Colors.RED)
        return False

    def _handle_ability_choice(self):
        if not self.player.abilities:
            print_slow("🚫 You have no abilities available.", color=Colors.GRAY)
            return False

        print()
        print(
            f"┌─ {colorize('Available Abilities', Colors.BOLD)} {'─' * 47}┐", flush=True
        )

        for key, ability in self.player.abilities.items():
            mana_color = (
                Colors.BLUE if self.player.mana >= ability["cost"] else Colors.RED
            )
            ability_name = colorize(
                f"{ability['name']:<18}", get_class_color(self.player.role)
            )
            mana_cost = colorize(f"Cost: {ability['cost']} MP", mana_color)

            # Add icon for ability affordability
            icon = "✨" if self.player.mana >= ability["cost"] else "❌"

            print(f"│ {key}: {icon} {ability_name} {mana_cost:<15} │", flush=True)

        print(f"└{'─' * 47}┘", flush=True)

        ability_choice = input(
            f"\n{colorize('Choose ability >', Colors.BOLD)} "
        ).strip()

        if ability_choice not in self.player.abilities:
            print_slow("❌ Invalid choice.", color=Colors.RED)
            return False

        chosen_ability = self.player.abilities[ability_choice]
        if self.player.mana < chosen_ability["cost"]:
            print_slow("💧 Not enough mana!", color=Colors.RED)
            time.sleep(1)
            return False

        self.player.mana -= chosen_ability["cost"]
        print()  # Add spacing before ability execution
        effect = chosen_ability["effect"]
        # Support both targeted and targetless abilities
        try:
            params = inspect.signature(effect).parameters
            if len(params) == 0:
                effect()
            else:
                effect(self.boss)
        except Exception:
            # Fallback: try targeted call
            try:
                effect(self.boss)
            except Exception:
                # Last resort: try without arguments
                effect()
        return True

    def _use_potion(self):
        if self.player.potions <= 0:
            print_slow("You are out of health potions!", color=Colors.RED)
            time.sleep(1)
            return False
        self.player.potions -= 1
        heal_amount = 40
        self.player.heal(heal_amount)
        print_slow(
            f"You used a health potion and recovered {heal_amount} HP.",
            color=Colors.BRIGHT_GREEN,
        )
        return True

    def _boss_turn(self):
        skip_turn = process_status_effects(self.boss)
        if not self.boss.is_alive():
            return False
        if skip_turn:  # Boss is stunned
            print_slow(f"{self.boss.name} is stunned and loses their turn!")
            time.sleep(2)
            self.turn += 1
            return True
        self.boss.choose_action(self.player)
        time.sleep(2)
        self.turn += 1
        return True

    def _end_game(self):
        clear_screen()
        if self.player.is_alive():
            print_header("🎉 VICTORY! 🎉", Colors.BRIGHT_GREEN)
            print()
            print_slow(
                "🎊 Congratulations! You have defeated the Gargantuan Hydra! 🎊",
                color=Colors.BRIGHT_GREEN,
            )
            print_slow(
                "🏆 The realm is safe once more thanks to your heroic deeds! 🏆",
                color=Colors.BRIGHT_YELLOW,
            )
            print()
            print_section_break()
            print_with_spacing("📊 Final Status:", Colors.BOLD, spacing_before=1)
            self.player.display_status()
            print()
            print_with_spacing(
                "✨ Thank you for playing! ✨",
                Colors.BRIGHT_CYAN,
                spacing_before=1,
                spacing_after=2,
            )
        else:
            print_header("💀 DEFEAT 💀", Colors.BRIGHT_RED)
            print()
            print_slow(
                "⚰️  You have been defeated... The world is shrouded in darkness.",
                color=Colors.GRAY,
            )
            print_slow(
                "🌑 The Gargantuan Hydra's reign of terror continues...",
                color=Colors.RED,
            )
            print()
            print_section_break()
            print_with_spacing("📊 Final Status:", Colors.BOLD, spacing_before=1)
            self.boss.display_status()
            print()
            print_with_spacing(
                "💪 Better luck next time, hero! 💪",
                Colors.YELLOW,
                spacing_before=1,
                spacing_after=2,
            )


if __name__ == "__main__":
    Game().run()
