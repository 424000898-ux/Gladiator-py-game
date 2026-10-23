# GLADIATOR ARENA
### A Swords & Sandals-inspired Python RPG

---

## Requirements
- Python 3.8+
- pygame 2.x
- numpy

## Install dependencies
```bash
pip install pygame numpy
```

## Run the game
```bash
python main.py
```

---

## Controls

### Menus
- **Mouse** — Navigate all menus
- **ESC** — Go back / close panels

### Combat
| Button | Action |
|--------|--------|
| ATTACK | Quick sword strike |
| HEAVY | Powerful slow swing (1.7× damage) |
| SPECIAL | Class skill (costs MP) |
| DEFEND | Raise block chance this turn |
| POTION | Use first consumable in bag |
| DODGE | Prepare guaranteed dodge next hit |

---

## Game Features

### Character Creation
- 5 classes: Warrior, Berserker, Rogue, Knight, Gladiator Mage
- Customizable skin tone, armor color, gender, name

### RPG Systems
- Full stat system: HP, MP, STR, DEF, AGI, INT, CRIT, DODGE, ACCURACY, BLOCK
- Level-up system (max 20+) with stat gains each level
- XP progression curve
- Arena rank ladder (1–15)

### Combat
- Turn-based cinematic combat
- Critical hits (2× damage, screen shake, slow-mo)
- Miss chance, dodge, block mitigation
- Screen shake, freeze-frame, flash on crits
- Floating damage numbers
- 5 particle effects: blood, sparks, dust, fire, magic

### Equipment
- Weapons: Sword, Axe, Spear, Hammer, Mace, Dual Blades, Excalibur…
- Armor: Helmet, Chest, Boots, Shield — all affect stats & visuals
- Item rarities: Common, Uncommon, Rare, Epic, Legendary

### AI Enemies
- 7 enemy types with unique AI: basic, aggressive, defensive, erratic, boss
- Enemies use potions, taunt, stun, and scale with player level

### Arena
- 4 tier brackets unlocked by rank
- Auto-saves after every victory

### Shop
- Animated shopkeeper with random dialogue
- Buy/sell items, equipment preview, tooltip on hover

### Save System
- JSON save at `save/savegame.json`
- Auto-saves on victory

---

## Project Structure
```
gladiator/
├── main.py           # Entry point
├── settings.py       # All constants, item/enemy/class data
├── game.py           # Main game loop & state machine
└── src/
    ├── animation.py      # Tween, state machine, animation manager
    ├── particle_system.py# Blood, sparks, fire, dust, magic
    ├── sound_manager.py  # Procedural audio (no external files)
    ├── items.py          # Item, Equipment, Inventory classes
    ├── player.py         # Player + GladiatorRenderer (pure pygame drawing)
    ├── enemy.py          # Enemy types + AI decision engine
    ├── combat.py         # All combat math & resolution
    ├── ui.py             # Buttons, HUD, bars, tooltips, arena background
    ├── shop.py           # Shop screen with animated shopkeeper
    ├── arena.py          # Arena rankings & tier system
    └── save_system.py    # JSON save/load
```

---

## Architecture Notes
- **No external asset files** — everything is drawn with pygame primitives
- **Procedural audio** — all sounds generated with numpy waveforms
- **Delta-time** — all animations & movement use dt for frame-rate independence
- **Expandable** — add enemies in `settings.py ENEMY_TYPES`, items in `BASE_ITEMS`, skills in `SKILLS`
