# ============================================================
#  GLADIATOR ARENA - Enemy & AI
# ============================================================
import random, math
from settings import *
from src.player import GladiatorRenderer
from src.items import Item, Equipment, Inventory


class Enemy:
    def __init__(self, enemy_type='Slave', level_scale=1):
        data = ENEMY_TYPES[enemy_type].copy()
        self.name      = enemy_type
        self.type      = enemy_type
        self.ai_type   = data['ai_type']
        self.size      = data['size']
        scale = 1 + (level_scale - 1) * 0.08
        self.max_hp    = int(data['hp'] * scale)
        self.hp        = self.max_hp
        self.strength  = int(data['strength'] * scale)
        self.defense   = int(data['defense'] * scale)
        self.agility   = data['agility']
        self.level     = data['level'] + (level_scale - 1)
        self.xp_reward = int(data['xp'] * scale)
        self.gold_reward = int(data['gold'] * scale * random.uniform(0.8, 1.3))
        self.weapon    = data['weapon']
        self.color     = data['color']
        # Combat
        self.accuracy       = 75
        self.crit_chance    = 8
        self.dodge_chance   = self.agility // 2
        self.block_chance   = 10
        # Status
        self.stunned     = False
        self.raged       = False
        self.dodge_next  = False
        self.potions     = random.randint(0, 2)
        self.taunts_left = 2
        # Skin varies
        skins = [(200,160,100),(180,140,80),(160,120,60),(220,190,140),(190,150,100)]
        sk = random.choice(skins)
        self.renderer  = GladiatorRenderer(
            0, 0, facing=-1, scale=data['size'],
            skin=sk, armor_color=self.color,
            weapon_name=self.weapon, class_name='Warrior')
        self.equipment = Equipment()
        self.equipment.equip(Item(self.weapon))

    @property
    def alive(self):
        return self.hp > 0

    def get_attack_damage(self):
        weapon = self.equipment.weapon
        base   = weapon.dmg if weapon else 5
        raw    = base + self.strength * 1.2
        if self.raged:
            raw *= 1.6
        return max(1, int(raw))

    def get_defense(self):
        return self.defense

    def take_damage(self, dmg):
        actual = max(0, dmg - self.defense // 3)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def tick_status(self):
        self.stunned    = False
        self.dodge_next = False
        self.raged      = False

    def decide_action(self, player_hp, player_max_hp, turn_number):
        """Return action string based on AI type."""
        hp_ratio   = self.hp / self.max_hp
        p_hp_ratio = player_hp / player_max_hp

        if self.stunned:
            return 'stunned'

        if self.ai_type == 'basic':
            return random.choices(
                ['attack','attack','heavy_attack','defend'],
                weights=[4,4,1,1])[0]

        elif self.ai_type == 'aggressive':
            if random.random() < 0.05 and self.taunts_left > 0:
                self.taunts_left -= 1
                return 'taunt'
            if hp_ratio < 0.3 and self.potions > 0 and random.random() < 0.7:
                self.potions -= 1
                return 'potion'
            if p_hp_ratio < 0.4:
                return random.choices(['heavy_attack','heavy_attack','attack'],
                                       weights=[3,2,1])[0]
            return random.choices(['attack','attack','heavy_attack'],
                                   weights=[4,3,2])[0]

        elif self.ai_type == 'defensive':
            if hp_ratio < 0.5 and self.potions > 0 and random.random() < 0.6:
                self.potions -= 1
                return 'potion'
            if p_hp_ratio > 0.7:
                return random.choices(['defend','attack','attack'],
                                       weights=[3,3,2])[0]
            return random.choices(['attack','heavy_attack','defend'],
                                   weights=[4,2,2])[0]

        elif self.ai_type == 'erratic':
            return random.choices(
                ['attack','heavy_attack','defend','taunt','attack'],
                weights=[4,3,2,1,3])[0]

        elif self.ai_type == 'boss':
            if turn_number % 4 == 0:
                return 'heavy_attack'
            if hp_ratio < 0.4 and self.potions > 0:
                self.potions -= 1
                return 'potion'
            if p_hp_ratio < 0.3:
                return 'heavy_attack'
            return random.choices(['attack','attack','heavy_attack','defend'],
                                   weights=[4,3,3,1])[0]

        return 'attack'
