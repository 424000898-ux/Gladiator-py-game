# ============================================================
#  GLADIATOR ARENA - Item, Equipment, and Loot System
# ============================================================
import copy
import random
from settings import (
    BASE_ITEMS,
    RARITY_COLORS,
    RARITY_TIERS,
    RARITY_WEIGHTS,
    ITEM_PREFIXES,
    ITEM_SUFFIXES,
)

WEAPON_BASES = {
    'Sword': 8, 'Axe': 10, 'Mace': 9, 'Spear': 7,
    'Dagger': 6, 'Gladius': 9, 'Hammer': 11,
}
ARMOR_BASE_NAMES = {
    'helmet': ['Helm', 'Mask', 'Hood', 'Visor'],
    'chest': ['Chestplate', 'Mail', 'Breastplate', 'Carapace'],
    'boots': ['Boots', 'Greaves', 'Sabatons', 'Treads'],
    'gloves': ['Gauntlets', 'Gloves', 'Handwraps', 'Grips'],
    'shield': ['Shield', 'Buckler', 'Kite Shield', 'Barrier'],
}
ACCESSORY_BASE_NAMES = {
    'ring': ['Ring', 'Band', 'Seal', 'Signet'],
    'necklace': ['Amulet', 'Pendant', 'Talisman', 'Charm'],
}
LEGENDARY_EFFECTS = [
    'Burning Strike', 'Frost Ward', 'Life Steal', 'Mana Surge',
    'Quickening', 'Fortitude', 'Spell Ward', 'Thorns', 'Velocity',
]
PRISMATIC_EFFECTS = [
    'Prismatic Nova', 'Reality Break', 'Soul Rend', 'Celestial Judgment',
    'Radiant Tempest', 'Chaos Echo', 'Astral Surge',
]

RARITY_MULTIPLIERS = {
    'common': 1.0,
    'uncommon': 1.7,
    'rare': 2.6,
    'epic': 4.2,
    'legendary': 6.5,
    'prismatic': 10.0,
}

class Item:
    """Runtime item instance with all stats."""
    def __init__(self, name, data=None):
        self.name = name
        if data is None:
            data = BASE_ITEMS.get(name, {})
        self.data = copy.deepcopy(data)
        self.type = self.data.get('type', 'misc')
        self.slot = self.data.get('slot', '')
        self.rarity = self.data.get('rarity', 'common')
        self.price = self.data.get('price', 10)
        self.desc = self.data.get('desc', '')
        self.count = int(self.data.get('count', 1))
        self.dmg = int(self.data.get('dmg', 0))
        # Consumable heal value (some items use 'heal' while others may use 'health')
        self.heal = int(self.data.get('heal', self.data.get('health', 0)))
        self.spd = float(self.data.get('spd', 1.0))
        self.crit_chance = int(self.data.get('crit_chance', 0))
        self.elemental = int(self.data.get('elemental', 0))
        self.defense = int(self.data.get('def', 0))
        self.health = int(self.data.get('health', 0))
        self.resistance = int(self.data.get('resistance', 0))
        self.dodge = int(self.data.get('dodge', 0))
        self.move_speed = float(self.data.get('move_speed', 0.0))
        self.stamina = int(self.data.get('stamina', 0))
        self.mp = int(self.data.get('mp', 0))
        self.block = int(self.data.get('block', 0))
        self.passive = self.data.get('passive', '')
        self.glow = bool(self.data.get('glow', self.rarity in ('legendary', 'prismatic')))
        self.unique = bool(self.data.get('unique', self.rarity in ('legendary', 'prismatic')))
        self._patch_data()

    def _patch_data(self):
        self.data.update({
            'type': self.type,
            'slot': self.slot,
            'rarity': self.rarity,
            'price': self.price,
            'desc': self.desc,
            'count': self.count,
            'heal': self.heal,
            'dmg': self.dmg,
            'spd': self.spd,
            'crit_chance': self.crit_chance,
            'elemental': self.elemental,
            'def': self.defense,
            'health': self.health,
            'resistance': self.resistance,
            'dodge': self.dodge,
            'move_speed': self.move_speed,
            'stamina': self.stamina,
            'mp': self.mp,
            'block': self.block,
            'passive': self.passive,
            'glow': self.glow,
            'unique': self.unique,
        })

    @property
    def color(self):
        return RARITY_COLORS.get(self.rarity, (180, 180, 180))

    @property
    def is_legendary(self):
        return self.rarity in ('legendary', 'prismatic')

    def sell_price(self):
        return max(1, int(self.price * 0.5))

    def to_dict(self):
        d = {'name': self.name, 'data': self.data}
        if self.count != 1:
            d['count'] = self.count
        return d

    @classmethod
    def from_dict(cls, d):
        item = cls(d['name'], d.get('data'))
        item.count = d.get('count', 1)
        item._patch_data()
        return item

    @classmethod
    def roll_rarity(cls, is_boss=False):
        weights = RARITY_WEIGHTS.copy()
        if is_boss:
            weights['legendary'] = weights.get('legendary', 2) + 4
            weights['epic'] = weights.get('epic', 6) + 3
            weights['rare'] = weights.get('rare', 12) + 5
        tiers = list(weights.keys())
        return random.choices(tiers, weights=[weights[t] for t in tiers], k=1)[0]

    @classmethod
    def _choose_base_name(cls, slot):
        if slot == 'weapon':
            return random.choice(list(WEAPON_BASES.keys()))
        if slot in ARMOR_BASE_NAMES:
            return random.choice(ARMOR_BASE_NAMES[slot])
        return random.choice(ACCESSORY_BASE_NAMES.get(slot, ['Trinket']))

    @classmethod
    def _prefix_for_slot(cls, slot, rarity):
        if rarity == 'common':
            return ''
        pool = ITEM_PREFIXES.get(slot, ITEM_PREFIXES.get('weapon', []))
        return random.choice(pool)

    @classmethod
    def _suffix_for_slot(cls, slot, rarity):
        if rarity == 'common':
            return ''
        pool = ITEM_SUFFIXES.get(slot, ITEM_SUFFIXES.get('weapon', []))
        return random.choice(pool)

    @classmethod
    def _legendary_passive(cls):
        return random.choice(LEGENDARY_EFFECTS)

    @classmethod
    def _prismatic_passive(cls):
        return random.choice(PRISMATIC_EFFECTS)

    @classmethod
    def _weapon_stats(cls, base_name, rarity, level):
        rarity_index = RARITY_TIERS.index(rarity)
        scale = RARITY_MULTIPLIERS[rarity]
        base = WEAPON_BASES.get(base_name, 8)
        dmg = max(1, int((base + level * 1.4) * scale + random.randint(0, 4 + rarity_index * 3)))
        spd = round(0.9 + 0.05 * rarity_index + random.uniform(-0.08, 0.08), 2)
        crit = max(0, int([0, 3, 8, 15, 25, 35][rarity_index] + random.randint(0, 3)))
        elemental = max(0, int([0, 3, 8, 15, 28, 40][rarity_index] + level // 5))
        return {
            'dmg': dmg,
            'spd': spd,
            'crit_chance': crit,
            'elemental': elemental,
        }

    @classmethod
    def _armor_stats(cls, slot, rarity, level):
        rarity_index = RARITY_TIERS.index(rarity)
        scale = RARITY_MULTIPLIERS[rarity]
        base_values = {
            'helmet': 4,
            'chest': 8,
            'boots': 3,
            'gloves': 2,
            'shield': 6,
        }
        base = base_values.get(slot, 3)
        defense = max(0, int((base + level * 1.2) * scale + random.randint(0, 4 + rarity_index * 3)))
        health = int([0, 12, 22, 36, 58, 78][rarity_index] + level * 2)
        resistance = int([0, 2, 6, 12, 20, 28][rarity_index] + rarity_index)
        dodge = int([0, 1, 3, 7, 12, 18][rarity_index] + (1 if slot == 'boots' else 0))
        move_speed = round([0.0, 0.02, 0.05, 0.10, 0.16, 0.22][rarity_index] + (0.03 if slot == 'boots' else 0.0), 2)
        stamina = int([0, 4, 8, 14, 24, 36][rarity_index] + (10 if slot == 'boots' else 0))
        mp = int([0, 2, 5, 10, 18, 28][rarity_index] + (5 if slot == 'helmet' else 0))
        block = int([0, 6, 12, 20, 30, 42][rarity_index] + (12 if slot == 'shield' else 0))
        return {
            'def': defense,
            'health': health,
            'resistance': resistance,
            'dodge': dodge,
            'move_speed': move_speed,
            'stamina': stamina,
            'mp': mp,
            'block': block,
        }

    @classmethod
    def _accessory_stats(cls, slot, rarity, level):
        rarity_index = RARITY_TIERS.index(rarity)
        return {
            'health': int([4, 12, 20, 32, 48, 70][rarity_index] + level * 2),
            'mp': int([2, 8, 14, 24, 38, 60][rarity_index] + level),
            'crit_chance': int([0, 2, 5, 10, 18, 28][rarity_index] + random.randint(0, 2)),
            'dodge': int([0, 1, 3, 6, 10, 15][rarity_index]),
            'resistance': int([0, 1, 4, 8, 14, 22][rarity_index]),
        }

    @classmethod
    def _make_name(cls, base_name, slot, rarity):
        prefix = cls._prefix_for_slot(slot, rarity)
        suffix = cls._suffix_for_slot(slot, rarity)
        pieces = []
        if prefix:
            pieces.append(prefix)
        pieces.append(base_name)
        if suffix:
            pieces.append(suffix)
        return ' '.join(pieces).strip()

    @classmethod
    def generate_random(cls, slot=None, level=1, is_boss=False):
        if slot is None:
            slot = random.choice(['weapon', 'helmet', 'chest', 'gloves', 'boots', 'shield', 'ring', 'necklace'])
        rarity = cls.roll_rarity(is_boss)
        base_name = cls._choose_base_name(slot)
        name = cls._make_name(base_name, slot, rarity)
        data = {
            'type': 'weapon' if slot == 'weapon' else 'armor' if slot in ARMOR_BASE_NAMES else 'accessory',
            'slot': slot,
            'rarity': rarity,
            'price': 30,
            'desc': 'A finely balanced item that scales with rarity.',
        }
        if slot == 'weapon':
            data.update(cls._weapon_stats(base_name, rarity, level))
        elif slot in ARMOR_BASE_NAMES:
            data.update(cls._armor_stats(slot, rarity, level))
        else:
            data.update(cls._accessory_stats(slot, rarity, level))
        data['price'] = max(20, int((data.get('dmg', 0) + data.get('def', 0) + data.get('health', 0) + data.get('crit_chance', 0) * 3) * (RARITY_MULTIPLIERS[rarity] * 2)))
        if rarity == 'legendary' or rarity == 'prismatic':
            if rarity == 'prismatic':
                if slot == 'weapon':
                    effect = 'Lifesteal'
                    data['desc'] = 'Prismatic weapon that can heal its wielder.'
                    data['price'] = int(data['price'] * 2.0)
                else:
                    effect = cls._prismatic_passive()
                    data['desc'] = f'Prismatic gear that grants {effect.lower()} and reality-bending power.'
                    data['price'] = int(data['price'] * 1.8)
            else:
                effect = cls._legendary_passive()
                data['desc'] = f'Legendary gear that grants {effect.lower()} and stronger scaling.'
                data['price'] = int(data['price'] * 1.5)
            data['passive'] = effect
            data['glow'] = True
            data['unique'] = True
        if slot == 'boots' and rarity in ('rare', 'epic', 'legendary', 'prismatic'):
            data['move_speed'] = round(data.get('move_speed', 0) + 0.05, 2)
        return cls(name, data)

    @classmethod
    def generate_loot(cls, level=1, is_boss=False, drop_count=1):
        loot = []
        for _ in range(drop_count):
            if random.random() < (0.5 if is_boss else 0.35):
                loot.append(cls.generate_random(level=level, is_boss=is_boss))
        return loot

    def tooltip_lines(self):
        slot_label = self.slot.title() if self.slot else self.type.title()
        lines = [self.name, f'{slot_label}', f'Rarity: {self.rarity.title()}']
        if self.passive:
            lines.append(f'Passive: {self.passive}')
        if self.dmg:
            lines.append(f'Attack: {self.dmg}')
        if self.crit_chance:
            lines.append(f'Crit: {self.crit_chance}%')
        if self.elemental:
            lines.append(f'Elemental: {self.elemental}')
        if self.defense:
            lines.append(f'Defense: {self.defense}')
        if self.health:
            lines.append(f'+{self.health} HP')
        if self.resistance:
            lines.append(f'Resistance: {self.resistance}')
        if self.dodge:
            lines.append(f'Dodge: {self.dodge}%')
        if self.move_speed:
            lines.append(f'Move Spd: +{self.move_speed:.2f}')
        if self.stamina:
            lines.append(f'+{self.stamina} Stamina')
        if self.mp:
            lines.append(f'+{self.mp} MP')
        if self.block:
            lines.append(f'Block: {self.block}%')
        if self.desc:
            lines.append(self.desc)
        lines.append(f'Value: {self.price}g')
        return lines


class Equipment:
    """What a character currently has equipped."""
    SLOTS = ['helmet', 'weapon', 'chest', 'gloves', 'pants', 'boots', 'shield', 'ring_l', 'ring_r', 'necklace']

    def __init__(self):
        self.slots = {s: None for s in self.SLOTS}

    def equip(self, item: Item, preferred_slot: str = None):
        target = None
        if preferred_slot and preferred_slot in self.slots and self._slot_matches_item(preferred_slot, item):
            target = preferred_slot
        if not target and item.slot:
            if item.slot == 'ring':
                if not self.slots.get('ring_l'):
                    target = 'ring_l'
                elif not self.slots.get('ring_r'):
                    target = 'ring_r'
                else:
                    target = 'ring_l'
            elif item.slot in self.slots:
                target = item.slot
        if not target:
            for s in self.SLOTS:
                if self._slot_matches_item(s, item):
                    target = s
                    break
        if not target:
            return None
        old = self.slots.get(target)
        self.slots[target] = item
        return old

    def unequip(self, slot):
        old = self.slots.get(slot)
        if old:
            self.slots[slot] = None
        return old

    def _slot_matches_item(self, slot, item: Item):
        if not item or not item.slot:
            return False
        if item.slot == 'ring' and slot.startswith('ring'):
            return True
        return slot == item.slot

    def _stat_total(self, attr):
        return sum(getattr(item, attr, 0) for item in self.slots.values() if item)

    @property
    def weapon(self):
        return self.slots.get('weapon')

    @property
    def total_defense(self):
        return self._stat_total('defense')

    @property
    def total_block(self):
        return self._stat_total('block')

    @property
    def total_health(self):
        return self._stat_total('health')

    @property
    def total_resistance(self):
        return self._stat_total('resistance')

    @property
    def total_dodge(self):
        return self._stat_total('dodge')

    @property
    def total_move_speed(self):
        return self._stat_total('move_speed')

    @property
    def total_stamina(self):
        return self._stat_total('stamina')

    @property
    def total_mana(self):
        return self._stat_total('mp')

    @property
    def total_crit(self):
        return self._stat_total('crit_chance')

    def to_dict(self):
        return {s: (i.to_dict() if i else None) for s, i in self.slots.items()}

    @classmethod
    def from_dict(cls, d):
        eq = cls()
        for s, v in d.items():
            if s in eq.slots and v:
                eq.slots[s] = Item.from_dict(v)
        return eq


class Inventory:
    """Player's bag of items."""
    MAX_SIZE = 24

    def __init__(self):
        self.items = []
        self.gold = 100

    def add(self, item: Item) -> bool:
        if item.type == 'consumable':
            for it in self.items:
                if it.name == item.name and it.rarity == item.rarity:
                    it.count += item.count
                    return True
        if len(self.items) >= self.MAX_SIZE:
            return False
        self.items.append(item)
        return True

    def remove(self, item: Item):
        if item in self.items:
            self.items.remove(item)

    def has(self, name) -> bool:
        return any(i.name == name for i in self.items)

    def count(self, name) -> int:
        return sum(i.count for i in self.items if i.name == name)

    def consumables(self):
        return [i for i in self.items if i.type == 'consumable']

    def to_dict(self):
        return {
            'gold': self.gold,
            'items': [i.to_dict() for i in self.items],
        }

    @classmethod
    def from_dict(cls, d):
        inv = cls()
        inv.gold = d.get('gold', 100)
        inv.items = [Item.from_dict(i) for i in d.get('items', [])]
        return inv
