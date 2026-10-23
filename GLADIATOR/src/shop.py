# ============================================================
#  GLADIATOR ARENA - Shop
# ============================================================
import pygame, random, math, os
from settings import *
from src.ui import draw_panel, draw_text, Button, draw_tooltip, get_font, load_icon
from src.items import Item


SHOP_DIALOGUES = [
    "Fine weapons for a fine gladiator!",
    "Only the best equipment in the arena!",
    "Your enemies won't know what hit them!",
    "Gold well spent is gold that wins battles!",
    "I once slew a minotaur with that very axe!",
    "Ah, a champion! I have just the thing...",
    "Buy now, survive later!",
]

SHOP_STOCK = [
    'Iron Sword','Steel Sword','Gladius','Dual Blades','Battle Axe',
    'War Hammer','Iron Spear','Dragon Mace','Aether Blade','Prismatic Starfall',
    'Iron Helm','Gladiator Helm','Steel Helm','Dragon Helm','Crown of Kings',
    'Iron Chest','Steel Plate','Plate Mail','Dragon Scale','Aegis Cuirass',
    'Leather Boots','Iron Boots','Storm Striders','Swift Greaves','Celestial Sabatons',
    'Wooden Shield','Iron Shield','Tower Shield','Aegis Shield','Dragon Ward',
    'Leather Pants','Iron Greaves','Steel Legguards','Arcane Trousers','Dragonhide Greaves',
    'Iron Ring','Silver Ring','Golden Band','Ring of Vigor','Ring of Eternity',
    'Silver Necklace','Amulet of Warding','Pendant of Strength','Phoenix Necklace','Celestial Locket',
    'Health Potion','Mana Potion','Elixir','Rage Potion',
]


class Shop:
    def __init__(self, screen_w, screen_h):
        self.sw = screen_w
        self.sh = screen_h
        self.t  = 0.0
        self.dialogue = random.choice(SHOP_DIALOGUES)
        self.dialogue_timer = 0.0

        # Random shop stock (12 items)
        items_pool = SHOP_STOCK.copy()
        random.shuffle(items_pool)
        self.stock = [Item(n) for n in items_pool[:12]]

        self.selected = None
        self.hover    = None
        self.msg      = ''
        self.msg_timer= 0.0

        # Sell mode
        self.sell_mode = False

        # Buttons
        cx = screen_w // 2
        # Confirm action (buy/sell selected)
        self.btn_confirm = Button(cx - 260, screen_h - 70, 110, 40, 'BUY', 20)
        # Mode buttons (placed close together)
        self.btn_buy_mode = Button(cx - 120, screen_h - 70, 110, 40, 'BUY MODE', 20,
                       color=BRONZE_DK, hover_color=BRONZE)
        self.btn_sell = Button(cx + 10,  screen_h - 70, 110, 40, 'SELL MODE', 20,
                    color=BRONZE_DK, hover_color=BRONZE)
        self.btn_close= Button(screen_w - 130, screen_h - 70, 110, 40, 'LEAVE', 20,
                    color=(80,30,30), hover_color=(150,50,50))

        # Merchant image (optional)
        self.merchant_img = None
        try:
            root = os.path.dirname(os.path.dirname(__file__))
            img_path = os.path.join(root, 'assets', 'merchant.png')
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                # Scale to reasonable size (height ~220 to be more visible)
                iw, ih = img.get_size()
                target_h = 220
                scale = target_h / max(1, ih)
                self.merchant_img = pygame.transform.smoothscale(img, (int(iw*scale), int(ih*scale)))
        except Exception:
            self.merchant_img = None

    def update(self, dt, mouse_pos, player):
        self.t += dt
        self.dialogue_timer += dt
        if self.dialogue_timer > 6.0:
            self.dialogue_timer = 0.0
            self.dialogue = random.choice(SHOP_DIALOGUES)
        if self.msg_timer > 0:
            self.msg_timer -= dt
        else:
            self.msg = ''
        self.btn_confirm.update(dt, mouse_pos)
        self.btn_buy_mode.update(dt, mouse_pos)
        self.btn_sell.update(dt, mouse_pos)
        self.btn_close.update(dt, mouse_pos)
        # Confirm button label reflects current action
        self.btn_confirm.text = 'SELL' if self.sell_mode else 'BUY'
        # Mode button texts are static
        self.btn_buy_mode.text = 'BUY MODE'
        self.btn_sell.text = 'SELL MODE'
        # Mode button colors: active mode is green
        if self.sell_mode:
            self.btn_sell.color = GREEN
            self.btn_buy_mode.color = BRONZE_DK
        else:
            self.btn_buy_mode.color = GREEN
            self.btn_sell.color = BRONZE_DK
        # Hover detection
        self.hover = None
        items_to_show = player.inventory.items if self.sell_mode else self.stock
        for i, item in enumerate(items_to_show):
            r = self._item_rect(i)
            if r.collidepoint(mouse_pos):
                self.hover = item
                break

    def _item_rect(self, i):
        cols = 4
        iw, ih = 140, 70
        ox = self.sw//2 - (cols*iw)//2
        oy = int(self.sh * 0.32)
        row = i // cols
        col = i % cols
        return pygame.Rect(ox + col*(iw+8), oy + row*(ih+8), iw, ih)

    def handle_event(self, event, player):
        result = None
        from src.sound_manager import sounds
        if self.btn_close.is_clicked(event):
            result = 'close'
        elif self.btn_buy_mode.is_clicked(event):
            self.sell_mode = False
            self.selected = None
        elif self.btn_sell.is_clicked(event):
            self.sell_mode = True
            self.selected  = None
        elif self.btn_confirm.is_clicked(event) and self.selected:
            item = self.selected
            if self.sell_mode:
                # Sell from inventory
                if item in player.inventory.items:
                    player.inventory.remove(item)
                    player.inventory.gold += item.sell_price()
                    sounds.play('gold_coin')
                    self.msg = f'Sold {item.name} for {item.sell_price()}g'
                    self.msg_timer = 2.0
                    self.selected = None
            else:
                if player.inventory.gold >= item.price:
                    from copy import deepcopy
                    purchased = Item(item.name, deepcopy(item.data))
                    if player.inventory.add(purchased):
                        player.inventory.gold -= item.price
                        sounds.play('gold_coin')
                        self.msg = f'Bought {item.name}!'
                        self.msg_timer = 2.0
                    else:
                        self.msg = 'Inventory full!'
                        self.msg_timer = 2.0
                else:
                    self.msg = 'Not enough gold!'
                    self.msg_timer = 2.0

        # Item selection
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            items_to_show = player.inventory.items if self.sell_mode else self.stock
            for i, item in enumerate(items_to_show):
                r = self._item_rect(i)
                if r.collidepoint(event.pos):
                    self.selected = item
                    sounds.play('button_click')
                    break
        return result

    def draw(self, surface, player, mouse_pos=None):
        # Darken background
        overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        surface.blit(overlay, (0,0))

        # Main panel
        pw, ph = 900, 540
        panel_r = pygame.Rect(self.sw//2 - pw//2, self.sh//2 - ph//2, pw, ph)
        draw_panel(surface, panel_r, color=STONE, border=GOLD)

        # Title
        draw_text(surface, "MERCHANT'S BAZAAR", self.sw//2, panel_r.y + 16,
                  34, GOLD, bold=True, center=True)

        # Shopkeeper
        sk_x = panel_r.x + 70
        sk_y = panel_r.y + 120
        self._draw_shopkeeper(surface, sk_x, sk_y)

        # Dialogue bubble
        self._draw_dialogue(surface, sk_x + 80, sk_y - 30)

        # Gold display
        gold_text = f'Gold: {player.inventory.gold}g'
        gold_width = get_font(20, True).size(gold_text)[0]
        draw_text(surface, gold_text,
                  panel_r.right - 20 - gold_width, panel_r.y + 16,
                  20, GOLD, bold=True, shadow=True)
        # (Removed mode label above merchant as requested)

        # Items grid
        items_to_show = player.inventory.items if self.sell_mode else self.stock
        for i, item in enumerate(items_to_show):
            self._draw_item_slot(surface, i, item)

        # Message
        if self.msg:
            col = GREEN if 'Bought' in self.msg or 'Sold' in self.msg else RED
            draw_text(surface, self.msg, self.sw//2,
                      panel_r.bottom - 90, 20, col, bold=True, center=True)

        # Tooltip
        if self.hover:
            mx, my = mouse_pos if mouse_pos is not None else pygame.mouse.get_pos()
            draw_tooltip(surface, self.hover, mx, my)

        # Buttons
        self.btn_confirm.draw(surface)
        self.btn_buy_mode.draw(surface)
        self.btn_sell.draw(surface)
        self.btn_close.draw(surface)

        if self.selected:
            lbl = 'sell' if self.sell_mode else 'buy'
            price = self.selected.sell_price() if self.sell_mode else self.selected.price
            draw_text(surface, f'Selected: {self.selected.name}  ({price}g to {lbl})',
                      self.sw//2, self.sh - 110, 18, PARCHMENT, center=True)

    def _draw_item_slot(self, surface, i, item):
        r = self._item_rect(i)
        sel = (item == self.selected)
        hov = (item == self.hover)
        col = DARK_GRAY
        if sel: col = BRONZE_DK
        elif hov: col = (60,50,40)
        draw_panel(surface, r, color=col, border=item.color if sel else BRONZE)
        draw_text(surface, item.name,  r.x+6, r.y+6,  13, item.color, bold=True, shadow=True)
        draw_text(surface, item.type,  r.x+6, r.y+22, 11, STONE_LT)
        # Right-align the price so it stays inside the item slot border
        price_str = f'{item.sell_price() if self.sell_mode else item.price}g'
        price_w = get_font(13, True).size(price_str)[0]
        px = max(r.x + 6, r.right - 8 - price_w)
        draw_text(surface, price_str, px, r.y+6, 13, GOLD, bold=True)
        # Stat preview
        stats = []
        if item.dmg:  stats.append(f'Dmg:{item.dmg}')
        if item.defense: stats.append(f'Def:{item.defense}')
        if item.heal: stats.append(f'Heal:{item.heal}')
        if stats:
            draw_text(surface, '  '.join(stats), r.x+6, r.y+36, 11, PARCHMENT)
        # Icon (right side)
        try:
            icon = load_icon(item.name, size=(48,48))
            if icon:
                ix = r.right - 52
                iy = r.y + (r.height - icon.get_height())//2
                surface.blit(icon, (ix, iy))
        except Exception:
            pass

    def _draw_shopkeeper(self, surface, x, y):
        # Draw merchant image if available, otherwise fall back to procedural drawing
        if self.merchant_img:
            img = self.merchant_img
            ix = x - img.get_width() // 2
            iy = y
            surface.blit(img, (ix, iy))
            return
        # Fallback: simple static portrait (no animation)
        # Body
        pts = [(x-25, y), (x+25, y), (x+30, y+80), (x-30, y+80)]
        pygame.draw.polygon(surface, (80,60,100), pts)
        pygame.draw.polygon(surface, (120,90,140), pts, 2)
        # Head
        pygame.draw.circle(surface, (210,165,100), (x, y - 25), 22)
        # Beard
        bpts = [(x-14, y-10), (x+14, y-10), (x+10, y+20), (x, y+25), (x-10, y+20)]
        pygame.draw.polygon(surface, (180,160,100), bpts)
        # Eyes
        pygame.draw.circle(surface, (30,20,10), (x-8, y-28), 4)
        pygame.draw.circle(surface, (30,20,10), (x+8, y-28), 4)
        # Hat
        hat_pts = [(x-26, y-40), (x+26, y-40), (x+18, y-60), (x-18, y-60)]
        pygame.draw.polygon(surface, (60,40,80), hat_pts)
        pygame.draw.line(surface, GOLD, (x-26, y-40), (x+26, y-40), 3)
        # Arms
        pygame.draw.line(surface, (80,60,100), (x-25, y+10), (int(x-45), y+30), 6)
        pygame.draw.line(surface, (80,60,100), (x+25, y+10), (int(x+45), y+30), 6)

    def _draw_dialogue(self, surface, x, y):
        txt = self.dialogue
        font = get_font(15)
        tw = font.size(txt)[0] + 20
        bh = 36
        r = pygame.Rect(x, y - bh, tw, bh)
        draw_panel(surface, r, color=PARCHMENT, border=BRONZE)
        draw_text(surface, txt, r.x+8, r.y+8, 15, DARK_BROWN, shadow=False)
        # Tail
        pygame.draw.polygon(surface, PARCHMENT,
                            [(x+10, y), (x+20, y), (x+15, y+10)])
