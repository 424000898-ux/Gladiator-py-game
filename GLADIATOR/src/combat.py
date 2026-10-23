# ============================================================
#  GLADIATOR ARENA - Combat System
# ============================================================
import random, math
from settings import SKILLS


class CombatResult:
    def __init__(self):
        self.damage    = 0
        self.is_crit   = False
        self.is_miss   = False
        self.is_dodge  = False
        self.is_block  = False
        self.is_stun   = False
        self.is_heal   = 0
        self.is_mp     = 0
        self.buff      = ''
        self.message   = ''
        self.skill_msg = ''

    def __str__(self):
        if self.is_miss:
            return 'MISS!'
        if self.is_dodge:
            return 'DODGED!'
        if self.is_block:
            return f'BLOCKED! {self.damage} dmg'
        if self.is_crit:
            return f'CRITICAL! {self.damage} dmg'
        return f'{self.damage} damage'


class Combat:
    """All combat calculation logic."""

    @staticmethod
    def roll_hit(attacker_acc, defender_dodge, defender_block=0) -> tuple:
        """Returns (hit: bool, crit: bool, block: bool, dodge: bool)"""
        # Dodge check
        if random.randint(1, 100) <= defender_dodge:
            return False, False, False, True
        # Hit check
        if random.randint(1, 100) > attacker_acc:
            return False, False, False, False
        # Block check
        if random.randint(1, 100) <= defender_block:
            return True, False, True, False
        # Crit is determined by attacker
        return True, False, False, False

    @staticmethod
    def player_attack(player, enemy, action='attack') -> CombatResult:
        res = CombatResult()

        if action == 'defend':
            res.message = f'{player.name} takes a defensive stance!'
            return res

        if action == 'dodge':
            player.dodge_next = True
            res.message = f'{player.name} prepares to dodge!'
            return res

        # Accuracy / dodge
        acc   = player.get_accuracy()
        dodge = enemy.dodge_chance
        block = enemy.block_chance if action != 'heavy_attack' else 0

        hit, crit, blocked, dodged = Combat.roll_hit(acc, dodge, block)

        if dodged:
            res.is_dodge = True
            res.message  = f'{enemy.name} dodged the attack!'
            return res

        if not hit:
            res.is_miss = True
            res.message = f'{player.name} missed!'
            return res

        # Base damage
        raw = player.get_attack_damage()

        if action == 'heavy_attack':
            raw = int(raw * 1.7)
        elif action == 'special':
            skill = _get_player_skill(player)
            if skill:
                return Combat._use_skill(player, enemy, skill, res)

        # Crit
        if random.randint(1, 100) <= player.get_crit_chance():
            raw    = int(raw * 2.0)
            crit   = True
            res.is_crit = True

        if blocked:
            raw = max(1, raw // 3)
            res.is_block = True

        actual = enemy.take_damage(raw)
        res.damage  = actual

        weapon = player.equipment.weapon if hasattr(player, 'equipment') else None
        if weapon and weapon.rarity == 'prismatic' and random.random() <= 0.30:
            heal_amount = player.heal(30)
            if heal_amount > 0:
                res.is_heal = heal_amount
                res.buff = 'Lifesteal'

        res.message = f'{player.name} deals {actual} damage!'
        if res.is_crit:
            res.message = f'CRITICAL HIT! {actual} damage!'
        if blocked:
            res.message += ' (blocked)'
        if res.is_heal:
            res.message += f' Lifesteal +{res.is_heal} HP!'

        return res

    @staticmethod
    def enemy_attack(enemy, player, action='attack') -> CombatResult:
        res = CombatResult()

        if action == 'stunned':
            res.message = f'{enemy.name} is stunned!'
            return res

        if action == 'defend':
            res.message = f'{enemy.name} braces for impact!'
            return res

        if action == 'taunt':
            player.accuracy = max(50, player.accuracy - 10)
            res.message = f'{enemy.name} taunts you! Your accuracy drops!'
            return res

        if action == 'potion':
            heal = int(enemy.max_hp * 0.25)
            enemy.heal(heal)
            res.is_heal = heal
            res.message = f'{enemy.name} drinks a potion and heals {heal} HP!'
            return res

        # Dodge check
        if player.dodge_next or random.randint(1,100) <= player.get_dodge_chance():
            res.is_dodge = True
            res.message  = f'{player.name} dodged the attack!'
            return res

        # Hit check
        if random.randint(1,100) > enemy.accuracy:
            res.is_miss = True
            res.message = f'{enemy.name} missed!'
            return res

        raw = enemy.get_attack_damage()

        if action == 'heavy_attack':
            raw = int(raw * 1.7)

        # Block
        if random.randint(1,100) <= player.get_block():
            raw = max(1, raw // 3)
            res.is_block = True

        # Crit
        if random.randint(1,100) <= enemy.crit_chance:
            raw = int(raw * 2.0)
            res.is_crit = True

        actual = player.take_damage(raw)
        res.damage = actual
        res.message = f'{enemy.name} attacks for {actual} damage!'
        if res.is_crit:
            res.message = f'{enemy.name} CRITICAL! {actual} damage!'

        return res

    @staticmethod
    def _use_skill(player, enemy, skill_data, res) -> 'CombatResult':
        mp_cost = skill_data.get('mp', 0)
        if player.mp < mp_cost:
            res.message = 'Not enough mana!'
            return res
        player.mp -= mp_cost

        if 'dmg_mult' in skill_data:
            raw    = int(player.get_attack_damage() * skill_data['dmg_mult'])
            actual = enemy.take_damage(raw)
            res.damage  = actual
            res.is_crit = True
            res.message = f'{skill_data.get("desc","")} — {actual} damage!'

        if skill_data.get('stun'):
            enemy.stunned = True
            res.is_stun   = True
            res.message  += ' Enemy stunned!'

        if skill_data.get('dodge_turn'):
            player.dodge_next = True
            res.message = f'{skill_data.get("desc","")} — dodge ready!'

        if skill_data.get('str_boost'):
            player.str_boost += skill_data['str_boost']
            res.message = f'War Cry! +{skill_data["str_boost"]} strength!'

        if 'dmg' in skill_data and skill_data.get('type') == 'magic':
            from settings import CLASSES
            dmg = int(skill_data['dmg'] + player.intelligence * 2)
            actual = enemy.take_damage(dmg)
            res.damage  = actual
            res.is_crit = True
            res.message = f'Fireball! {actual} magic damage!'

        return res


def _get_player_skill(player):
    from settings import SKILLS
    for name, data in SKILLS.items():
        cls = data.get('class', '')
        if cls == 'all' or cls == player.class_name:
            return data
    return None
