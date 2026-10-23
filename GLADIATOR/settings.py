# ============================================================
#  GLADIATOR ARENA - Settings & Constants
# ============================================================
import os

# --- Window ---
SCREEN_W = 1280
SCREEN_H = 720
FPS = 60
TITLE = "Gladiator Arena"

# --- Colors ---
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
RED         = (200, 30,  30)
DARK_RED    = (120, 0,   0)
GREEN       = (30,  180, 30)
DARK_GREEN  = (0,   100, 0)
BLUE        = (30,  80,  200)
YELLOW      = (255, 210, 0)
ORANGE      = (255, 140, 0)
PURPLE      = (140, 0,   200)
BROWN       = (100, 60,  20)
DARK_BROWN  = (60,  30,  10)
GRAY        = (120, 120, 120)
DARK_GRAY   = (50,  50,  50)
LIGHT_GRAY  = (200, 200, 200)

# Bronze / gold UI theme
BRONZE      = (180, 110, 40)
BRONZE_DK   = (110, 65,  15)
GOLD        = (212, 175, 55)
GOLD_LT     = (255, 220, 80)
STONE       = (80,  72,  60)
STONE_LT    = (130, 120, 100)
PARCHMENT   = (220, 195, 145)
BLOOD       = (160, 20,  20)
BLOOD_LT    = (200, 50,  50)
SAND        = (194, 178, 128)
SAND_DK     = (160, 140, 90)
FIRE_ORANGE = (255, 120, 20)
FIRE_YELLOW = (255, 220, 60)
SKY_BLUE    = (80,  140, 200)
CROWD_TAN   = (200, 170, 130)

# Rarity colors
RARITY_COLORS = {
    'common':    (180, 180, 180),
    'uncommon':  (60,  200, 60),
    'rare':      (60,  100, 220),
    'epic':      (160, 40,  220),
    'legendary': (255, 165, 0),
    'prismatic': (220, 180, 255),
}

# Item rarity and loot generation
RARITY_TIERS = ['common','uncommon','rare','epic','legendary','prismatic']
RARITY_WEIGHTS = {
    'common':    55,
    'uncommon':  25,
    'rare':      12,
    'epic':       6,
    'legendary':  2,
    'prismatic':  1,
}
ITEM_PREFIXES = {
    'weapon': ['Flaming','Glacial','Vicious','Shadow','Storm','Celestial','Rugged','Wicked','Ancient','Savage'],
    'helmet': ['Cursed','Guardian','Mystic','Ironhide','Vigilant','Stormforged','Dragon','Runic','Tempered','Warden'],
    'chest': ['Valor','Titan','Battle','Warborn','Heroic','Paladin','Dragon','Runic','Aegis','Fortified'],
    'boots': ['Swift','Fleet','Anchor','Storm','Silent','Windwalk','Ironclad','Gale','Shadow','Ranger'],
    'gloves': ['Grasp','Fury','Razor','Stone','Phantom','Storm','Iron','Berserker','Archon','Vigil'],
    'shield': ['Bulwark','Aegis','Defiant','Obsidian','Storm','Dragon','Guardian','Fortress','Titan','Ironclad'],
    'ring': ['Band','Seal','Loop','Circle','Signet','Ring','Band','Shard','Eye','Glyph'],
    'necklace': ['Pendant','Amulet','Talisman','Charm','Locket','Orb','Medallion','Collar','Wreath','Necklace'],
}
ITEM_SUFFIXES = {
    'weapon': ['of Fury','of the Phoenix','of Ruin','of the Tempest','of the Warlord','of Shadows','of Might','of the Dragon','of Surge','of Blood'],
    'helmet': ['of Insight','of Resistance','of Warding','of the Sentinel','of Courage','of the Ancients','of Clarity','of the Storm','of the Protector','of Wisdom'],
    'chest': ['of Fortitude','of the Colossus','of the Vanguard','of Endurance','of the Phoenix','of Earth','of the Gladiator','of Sacrifice','of Stone','of Resolve'],
    'boots': ['of Swiftness','of the Wind','of Evasion','of the Sentinel','of Shadows','of Leap','of the Pathfinder','of the Gale','of Fleetness','of the Traveler'],
    'gloves': ['of Precision','of Vigor','of the Berserker','of Reflexes','of Strength','of the Phantom','of Mastery','of the Duelist','of Might','of Wrath'],
    'shield': ['of Protection','of Invincibility','of the Warden','of the Ironclad','of Deflection','of the Guardian','of Bastion','of Aegis','of Stone','of the Bulwark'],
    'ring': ['of Power','of the Phoenix','of Focus','of Fortitude','of Luck','of Devotion','of Fury','of the Moon','of Flame','of Grace'],
    'necklace': ['of Wisdom','of Renewal','of Vigor','of the Serpent','of the Mystic','of the Archmage','of Harmony','of Souls','of Radiance','of Resilience'],
}

# --- Classes ---
CLASSES = {
    'Warrior': {
        'hp': 120, 'mp': 40, 'stamina': 100,
        'strength': 14, 'defense': 10, 'agility': 8,
        'intelligence': 4, 'crit': 10, 'dodge': 5,
        'accuracy': 80, 'block': 20,
        'weapon': 'Sword', 'color': (180, 60, 60),
        'desc': 'Balanced fighter with sword and shield.'
    },
    'Berserker': {
        'hp': 130, 'mp': 20, 'stamina': 120,
        'strength': 18, 'defense': 6, 'agility': 10,
        'intelligence': 2, 'crit': 20, 'dodge': 8,
        'accuracy': 75, 'block': 5,
        'weapon': 'Axe', 'color': (200, 80, 30),
        'desc': 'High damage, low defense berserker.'
    },
    'Rogue': {
        'hp': 90, 'mp': 60, 'stamina': 110,
        'strength': 10, 'defense': 6, 'agility': 18,
        'intelligence': 8, 'crit': 30, 'dodge': 20,
        'accuracy': 90, 'block': 5,
        'weapon': 'Dual Blades', 'color': (60, 160, 60),
        'desc': 'Fast attacker with high critical chance.'
    },
    'Knight': {
        'hp': 150, 'mp': 30, 'stamina': 90,
        'strength': 12, 'defense': 18, 'agility': 5,
        'intelligence': 5, 'crit': 8, 'dodge': 3,
        'accuracy': 78, 'block': 40,
        'weapon': 'Spear', 'color': (60, 80, 200),
        'desc': 'Tank with high block and defense.'
    },
    'Gladiator Mage': {
        'hp': 80, 'mp': 140, 'stamina': 70,
        'strength': 8, 'defense': 7, 'agility': 10,
        'intelligence': 20, 'crit': 15, 'dodge': 10,
        'accuracy': 85, 'block': 10,
        'weapon': 'Mace', 'color': (160, 40, 220),
        'desc': 'Magic-infused gladiator with spells.'
    },
}

# --- Enemy Types ---
ENEMY_TYPES = {
    'Slave': {
        'hp': 50, 'strength': 6, 'defense': 2, 'agility': 5,
        'level': 1, 'xp': 30, 'gold': 10,
        'color': (160, 130, 90), 'weapon': 'Hammer',
        'ai_type': 'basic', 'size': 0.7,
    },
    'Rogue Gladiator': {
        'hp': 80, 'strength': 10, 'defense': 6, 'agility': 12,
        'level': 3, 'xp': 60, 'gold': 25,
        'color': (60, 160, 60), 'weapon': 'Dual Blades',
        'ai_type': 'aggressive', 'size': 0.85,
    },
    'Knight': {
        'hp': 130, 'strength': 12, 'defense': 18, 'agility': 5,
        'level': 5, 'xp': 100, 'gold': 50,
        'color': (60, 80, 180), 'weapon': 'Spear',
        'ai_type': 'defensive', 'size': 0.95,
    },
    'Orc': {
        'hp': 160, 'strength': 20, 'defense': 10, 'agility': 6,
        'level': 7, 'xp': 150, 'gold': 75,
        'color': (60, 120, 40), 'weapon': 'Axe',
        'ai_type': 'aggressive', 'size': 1.1,
    },
    'Skeleton': {
        'hp': 70, 'strength': 14, 'defense': 4, 'agility': 14,
        'level': 6, 'xp': 120, 'gold': 60,
        'color': (220, 210, 190), 'weapon': 'Sword',
        'ai_type': 'erratic', 'size': 0.85,
    },
    'Minotaur': {
        'hp': 220, 'strength': 26, 'defense': 14, 'agility': 8,
        'level': 10, 'xp': 280, 'gold': 150,
        'color': (100, 60, 30), 'weapon': 'Hammer',
        'ai_type': 'boss', 'size': 1.3,
    },
    'Arena Champion': {
        'hp': 300, 'strength': 30, 'defense': 22, 'agility': 16,
        'level': 15, 'xp': 500, 'gold': 300,
        'color': (200, 160, 30), 'weapon': 'Axe',
        'ai_type': 'boss', 'size': 1.15,
    },
}

# --- Arena Tiers ---
ARENA_TIERS = [
    {'name': 'The Pit',         'min_rank': 1,  'enemy_pool': ['Slave','Slave','Rogue Gladiator'],           'crowd_size': 200},
    {'name': 'Sand & Blood',    'min_rank': 3,  'enemy_pool': ['Rogue Gladiator','Knight','Orc'],            'crowd_size': 500},
    {'name': 'Iron Colosseum',  'min_rank': 6,  'enemy_pool': ['Knight','Orc','Skeleton','Minotaur'],        'crowd_size': 1000},
    {'name': 'Golden Arena',    'min_rank': 10, 'enemy_pool': ['Minotaur','Arena Champion','Arena Champion'], 'crowd_size': 2000},
]

# --- Items ---
BASE_ITEMS = {
    # Weapons
    'Wooden Sword':   {'type':'weapon','slot':'weapon','dmg':8,'spd':1.0,'rarity':'common','price':20,'desc':'A basic training sword.'},
    'Iron Sword':     {'type':'weapon','slot':'weapon','dmg':16,'spd':1.0,'rarity':'common','price':80,'desc':'Reliable iron blade.'},
    'Steel Sword':    {'type':'weapon','slot':'weapon','dmg':28,'spd':1.1,'rarity':'uncommon','price':200,'desc':'Finely crafted steel.'},
    'Gladius':        {'type':'weapon','slot':'weapon','dmg':22,'spd':1.3,'rarity':'uncommon','price':160,'desc':'Classic arena sword.'},
    'Dual Blades':    {'type':'weapon','slot':'weapon','dmg':20,'spd':1.6,'rarity':'rare','price':320,'desc':'Twin blades, double strikes.'},
    'Battle Axe':     {'type':'weapon','slot':'weapon','dmg':34,'spd':0.8,'rarity':'uncommon','price':180,'desc':'Slow but devastating.'},
    'War Hammer':     {'type':'weapon','slot':'weapon','dmg':40,'spd':0.6,'rarity':'rare','price':350,'desc':'Crushes armor.'},
    'Iron Spear':     {'type':'weapon','slot':'weapon','dmg':24,'spd':1.2,'rarity':'common','price':100,'desc':'Long reach thrusts.'},
    'Dragon Mace':    {'type':'weapon','slot':'weapon','dmg':38,'spd':0.9,'rarity':'epic','price':700,'desc':'Imbued with dragon essence.'},
    'Aether Blade':   {'type':'weapon','slot':'weapon','dmg':58,'spd':1.4,'rarity':'legendary','price':2200,'desc':'A legendary blade forged from celestial aether.'},
    'Prismatic Starfall': {'type':'weapon','slot':'weapon','dmg':75,'spd':1.5,'rarity':'prismatic','price':3200,'desc':'A prismatic weapon radiating limitless power.', 'passive': 'Lifesteal', 'glow': True, 'unique': True},
    'Excalibur':      {'type':'weapon','slot':'weapon','dmg':60,'spd':1.4,'rarity':'legendary','price':2000,'desc':'Legendary blade of kings.'},
    # Armor
    'Leather Helm':   {'type':'armor','slot':'helmet','def':3,'rarity':'common','price':30},
    'Iron Helm':      {'type':'armor','slot':'helmet','def':7,'rarity':'common','price':90},
    'Gladiator Helm': {'type':'armor','slot':'helmet','def':12,'rarity':'uncommon','price':220},
    'Steel Helm':     {'type':'armor','slot':'helmet','def':18,'rarity':'rare','price':320,'desc':'A solid steel helm built for strong defense.'},
    'Dragon Helm':    {'type':'armor','slot':'helmet','def':32,'rarity':'epic','price':640,'desc':'An epic helm imbued with dragonfire resilience.'},
    'Crown of Kings': {'type':'armor','slot':'helmet','def':48,'rarity':'legendary','price':1300,'desc':'A legendary helm worn by the greatest champions.'},
    'Leather Chest':  {'type':'armor','slot':'chest','def':5,'rarity':'common','price':50},
    'Iron Chest':     {'type':'armor','slot':'chest','def':14,'rarity':'common','price':130},
    'Steel Plate':    {'type':'armor','slot':'chest','def':24,'rarity':'uncommon','price':380},
    'Plate Mail':     {'type':'armor','slot':'chest','def':32,'rarity':'rare','price':520,'desc':'Rare plated mail for dependable protection.'},
    'Dragon Scale':   {'type':'armor','slot':'chest','def':40,'rarity':'epic','price':900},
    'Aegis Cuirass':  {'type':'armor','slot':'chest','def':50,'rarity':'legendary','price':1400,'desc':'A legendary cuirass forged in ancient fire.'},
    'Leather Boots':  {'type':'armor','slot':'boots','def':2,'rarity':'common','price':25},
    'Iron Boots':     {'type':'armor','slot':'boots','def':5,'rarity':'common','price':70},
    'Storm Striders': {'type':'armor','slot':'boots','def':12,'move_speed':0.08,'rarity':'rare','price':260,'desc':'Light boots granting swift movement.'},
    'Swift Greaves':  {'type':'armor','slot':'boots','def':18,'move_speed':0.12,'rarity':'epic','price':520,'desc':'Greaves made for quick strikes.'},
    'Celestial Sabatons': {'type':'armor','slot':'boots','def':26,'move_speed':0.18,'rarity':'legendary','price':900,'desc':'Blessed boots that quicken every step.'},
    'Leather Pants':  {'type':'armor','slot':'pants','def':6,'rarity':'common','price':85,'desc':'Simple cloth pants for light protection.'},
    'Iron Greaves':   {'type':'armor','slot':'pants','def':15,'rarity':'uncommon','price':160,'desc':'Sturdy greaves that protect your legs.'},
    'Steel Legguards':{'type':'armor','slot':'pants','def':22,'rarity':'rare','price':280,'desc':'Heavy legguards built for battle.'},
    'Arcane Trousers':{'type':'armor','slot':'pants','def':28,'mp':12,'rarity':'epic','price':520,'desc':'Mystic trousers that restore mana.'},
    'Dragonhide Greaves':{'type':'armor','slot':'pants','def':42,'health':18,'rarity':'legendary','price':980,'desc':'Legendary leg armor from dragon hide.'},
    'Wooden Shield':  {'type':'armor','slot':'shield','def':8,'block':10,'rarity':'common','price':60},
    'Iron Shield':    {'type':'armor','slot':'shield','def':18,'block':20,'rarity':'uncommon','price':200},
    'Tower Shield':   {'type':'armor','slot':'shield','def':28,'block':35,'rarity':'rare','price':500},
    'Aegis Shield':   {'type':'armor','slot':'shield','def':36,'block':40,'rarity':'epic','price':900,'desc':'A shield blessed with protective wards.'},
    'Dragon Ward':    {'type':'armor','slot':'shield','def':52,'block':55,'rarity':'legendary','price':1600,'desc':'A legendary shield forged from dragon scales.'},
    'Iron Ring':      {'type':'accessory','slot':'ring','crit_chance':3,'rarity':'common','price':90,'desc':'A simple ring to sharpen your focus.'},
    'Silver Ring':    {'type':'accessory','slot':'ring','crit_chance':5,'rarity':'uncommon','price':140,'desc':'A silver ring that sharpens your strikes.'},
    'Golden Band':    {'type':'accessory','slot':'ring','crit_chance':8,'rarity':'rare','price':280,'desc':'A rare ring favored by duelists.'},
    'Ring of Vigor':  {'type':'accessory','slot':'ring','stamina':8,'rarity':'epic','price':520,'desc':'An epic ring that strengthens your stamina.'},
    'Ring of Eternity':{'type':'accessory','slot':'ring','mp':12,'rarity':'legendary','price':980,'desc':'A legendary ring infused with endless energy.'},
    'Silver Necklace':{'type':'accessory','slot':'necklace','mp':18,'resistance':2,'rarity':'common','price':100,'desc':'A silver pendant that aids in mana recovery.'},
    'Amulet of Warding':{'type':'accessory','slot':'necklace','resistance':6,'rarity':'uncommon','price':170,'desc':'An amulet that protects against attacks.'},
    'Pendant of Strength':{'type':'accessory','slot':'necklace','health':12,'rarity':'rare','price':320,'desc':'A rare pendant that bolsters your strength.'},
    'Phoenix Necklace':{'type':'accessory','slot':'necklace','mp':24,'rarity':'epic','price':620,'desc':'An epic necklace fanning your magical power.'},
    'Celestial Locket':{'type':'accessory','slot':'necklace','mp':32,'rarity':'legendary','price':1200,'desc':'A legendary locket filled with celestial energy.'},
    # Consumables
    'Health Potion':  {'type':'consumable','heal':50,'rarity':'common','price':30,'desc':'Restores 50 HP.'},
    'Mana Potion':    {'type':'consumable','mp':40,'rarity':'common','price':30,'desc':'Restores 40 MP.'},
    'Elixir':         {'type':'consumable','heal':120,'mp':60,'rarity':'rare','price':150,'desc':'Full restoration.'},
    'Rage Potion':    {'type':'consumable','buff':'rage','rarity':'uncommon','price':80,'desc':'Doubles damage for 2 turns.'},
}

# --- Special Skills ---
SKILLS = {
    'Power Strike':  {'mp':15,'dmg_mult':2.0,'desc':'Double damage strike.','class':'Warrior'},
    'Berserk Rage':  {'mp':20,'dmg_mult':2.5,'def_pen':0.5,'desc':'Massive hit, lose some defense.','class':'Berserker'},
    'Shadow Step':   {'mp':12,'dodge_turn':True,'desc':'Guaranteed dodge next attack.','class':'Rogue'},
    'Shield Bash':   {'mp':10,'stun':True,'desc':'Stuns enemy for 1 turn.','class':'Knight'},
    'Fireball':      {'mp':30,'dmg':60,'type':'magic','desc':'Launches a magic fireball.','class':'Gladiator Mage'},
    'Taunt':         {'mp':5,'enemy_acc':-20,'desc':'Lowers enemy accuracy.','class':'all'},
    'War Cry':       {'mp':10,'str_boost':5,'desc':'Boosts your strength.','class':'all'},
}

# --- Progression ---
XP_PER_LEVEL = [0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3300,
                4000, 4800, 5700, 6700, 7800, 9000, 10300, 11700, 13200, 15000]

# --- Save path ---
SAVE_PATH = os.path.join(os.path.dirname(__file__), 'save', 'savegame.json')
